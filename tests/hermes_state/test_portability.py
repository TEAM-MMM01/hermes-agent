"""Tests for hermes_state_portability.SessionPortabilityMixin.

Export/import round-trips run against a real ``SessionDB`` on a temp path (no
mocked sqlite): the mixin's contract is what actually lands in the ``sessions``
and ``messages`` tables, including the parent-edge repair that keeps a partial
import importable.
"""

import json

import pytest

from hermes_state import SessionDB


@pytest.fixture
def db(tmp_path):
    database = SessionDB(db_path=tmp_path / "state.db")
    try:
        yield database
    finally:
        database.close()


@pytest.fixture
def other_db(tmp_path):
    database = SessionDB(db_path=tmp_path / "target.db")
    try:
        yield database
    finally:
        database.close()


def _session_with_turns(db, session_id, *, source="cli", title=None, **kwargs):
    db.create_session(session_id, source=source, **kwargs)
    if title:
        db.set_session_title(session_id, title)
    db.append_message(session_id, "user", content=f"hello from {session_id}")
    db.append_message(session_id, "assistant", content=f"hi from {session_id}")
    return session_id


# ── export ───────────────────────────────────────────────────────────────────


class TestExportSession:
    def test_missing_session_is_none(self, db):
        assert db.export_session("nope") is None

    def test_export_carries_the_session_row_and_its_messages(self, db):
        _session_with_turns(db, "s1")

        exported = db.export_session("s1")

        assert exported["id"] == "s1"
        assert exported["source"] == "cli"
        assert [m["role"] for m in exported["messages"]] == ["user", "assistant"]
        assert exported["messages"][0]["content"] == "hello from s1"


class TestExportSessionLineage:
    def test_missing_session_is_none(self, db):
        assert db.export_session_lineage("nope") is None

    def test_a_lone_session_exports_as_a_single_segment(self, db):
        _session_with_turns(db, "solo")

        lineage = db.export_session_lineage("solo")

        assert lineage["lineage_session_ids"] == ["solo"]
        assert lineage["message_count"] == 2

    def test_a_compression_chain_flattens_into_one_logical_session(self, db):
        _session_with_turns(db, "root")
        db.end_session("root", "compression")
        _session_with_turns(db, "tip", parent_session_id="root")

        lineage = db.export_session_lineage("tip")

        assert lineage["id"] == "tip", "identity comes from the newest segment"
        assert lineage["lineage_session_ids"] == ["root", "tip"]
        assert lineage["message_count"] == 4
        assert [m["content"] for m in lineage["messages"]] == [
            "hello from root",
            "hi from root",
            "hello from tip",
            "hi from tip",
        ]
        assert [seg["id"] for seg in lineage["segments"]] == ["root", "tip"]


class TestExportAll:
    def test_every_session_is_exported_with_its_messages(self, db):
        _session_with_turns(db, "a")
        _session_with_turns(db, "b", source="telegram")

        exported = db.export_all()

        by_id = {s["id"]: s for s in exported}
        assert set(by_id) == {"a", "b"}
        assert len(by_id["a"]["messages"]) == 2

    def test_source_filter_narrows_the_export(self, db):
        _session_with_turns(db, "a")
        _session_with_turns(db, "b", source="telegram")

        assert [s["id"] for s in db.export_all(source="telegram")] == ["b"]


# ── rich rows / listings ─────────────────────────────────────────────────────


class TestGetSessionRichRow:
    def test_missing_session_is_none(self, db):
        assert db.get_session_rich_row("nope") is None

    def test_row_carries_a_preview_and_last_activity(self, db):
        _session_with_turns(db, "s1")

        row = db.get_session_rich_row("s1")

        assert row["id"] == "s1"
        assert row["preview"] == "hello from s1"
        assert row["last_active"] >= row["started_at"]

    def test_a_session_without_messages_falls_back_to_started_at(self, db):
        db.create_session("empty", source="cli")

        row = db.get_session_rich_row("empty")

        assert row["preview"] == ""
        assert row["last_active"] == row["started_at"]

    def test_compact_rows_omit_the_system_prompt_blob(self, db):
        db.create_session("s1", source="cli", system_prompt="a very long prompt")

        full = db.get_session_rich_row("s1")
        compact = db.get_session_rich_row("s1", compact_rows=True)

        assert full["system_prompt"] == "a very long prompt"
        assert "system_prompt" not in compact
        # Everything else the caller renders is still there.
        assert compact["id"] == "s1"
        assert set(full) - set(compact) == {"system_prompt"}


class TestDistinctSessionCwds:
    def test_blank_and_missing_cwds_are_skipped(self, db):
        db.create_session("no_cwd", source="cli")
        db.create_session("blank", source="cli", cwd="   ")
        db.create_session("real", source="cli", cwd="/repo")

        assert [entry["cwd"] for entry in db.distinct_session_cwds()] == ["/repo"]

    def test_sessions_are_counted_per_cwd(self, db):
        db.create_session("a", source="cli", cwd="/repo")
        db.create_session("b", source="cli", cwd="/repo")
        db.create_session("c", source="cli", cwd="/other")

        counts = {e["cwd"]: e["sessions"] for e in db.distinct_session_cwds()}

        assert counts == {"/repo": 2, "/other": 1}

    def test_archived_sessions_are_excluded_unless_requested(self, db):
        db.create_session("live", source="cli", cwd="/live")
        db.create_session("old", source="cli", cwd="/archived")
        db.set_session_archived("old", True)

        assert [e["cwd"] for e in db.distinct_session_cwds()] == ["/live"]
        assert {e["cwd"] for e in db.distinct_session_cwds(include_archived=True)} == {
            "/live",
            "/archived",
        }

    def test_last_active_tracks_the_newest_session_in_the_cwd(self, db):
        db.create_session("older", source="cli", cwd="/repo")
        db.create_session("newer", source="cli", cwd="/repo")
        db._conn.execute("UPDATE sessions SET started_at = 100 WHERE id = 'older'")
        db._conn.execute("UPDATE sessions SET started_at = 900 WHERE id = 'newer'")
        db._conn.commit()

        assert db.distinct_session_cwds()[0]["last_active"] == 900


class TestListCronJobRuns:
    def test_only_the_requested_job_runs_are_returned_newest_first(self, db):
        for sid, started in (("cron_job_100", 100), ("cron_job_300", 300), ("cron_job_200", 200)):
            db.create_session(sid, source="cron")
            db.append_message(sid, "user", content=f"run {sid}")
            db._conn.execute("UPDATE sessions SET started_at = ? WHERE id = ?", (started, sid))
        db.create_session("cron_other_100", source="cron")
        db._conn.commit()

        runs = db.list_cron_job_runs("job")

        assert [r["id"] for r in runs] == ["cron_job_300", "cron_job_200", "cron_job_100"]
        assert runs[0]["preview"] == "run cron_job_300"

    def test_a_non_cron_session_sharing_the_prefix_is_ignored(self, db):
        db.create_session("cron_job_1", source="cli")
        assert db.list_cron_job_runs("job") == []

    def test_limit_and_offset_page_the_runs(self, db):
        for started in (100, 200, 300):
            sid = f"cron_job_{started}"
            db.create_session(sid, source="cron")
            db._conn.execute("UPDATE sessions SET started_at = ? WHERE id = ?", (started, sid))
        db._conn.commit()

        assert [r["id"] for r in db.list_cron_job_runs("job", limit=1)] == ["cron_job_300"]
        assert [r["id"] for r in db.list_cron_job_runs("job", limit=1, offset=1)] == ["cron_job_200"]


class TestGetFirstAssistantText:
    def test_the_first_reply_wins_over_later_ones(self, db):
        db.create_session("s1", source="cli")
        db.append_message("s1", "user", content="hello?")
        db.append_message("s1", "assistant", content="first reply")
        db.append_message("s1", "assistant", content="second reply")

        assert db.get_first_assistant_text("s1") == "first reply"

    def test_it_is_empty_without_a_reply(self, db):
        db.create_session("s1", source="cli")
        db.append_message("s1", "user", content="hello?")

        assert db.get_first_assistant_text("s1") == ""
        assert db.get_first_assistant_text("nope") == ""


# ── import validation ────────────────────────────────────────────────────────


class TestImportValidation:
    def test_a_non_list_payload_is_rejected(self, db):
        with pytest.raises(ValueError, match="must be a list"):
            db.import_sessions({"id": "s1"})

    def test_too_many_sessions_is_rejected(self, db, monkeypatch):
        monkeypatch.setattr(SessionDB, "_IMPORT_MAX_SESSIONS", 1)
        with pytest.raises(ValueError, match="at most"):
            db.import_sessions([{"id": "a"}, {"id": "b"}])

    @pytest.mark.parametrize(
        "payload, expected",
        [
            (["not an object"], "session must be an object"),
            ([{"id": "   "}], "session id is required"),
            ([{"id": "a"}, {"id": "a"}], "duplicate session id"),
            ([{"id": "a", "messages": {"role": "user"}}], "messages must be a list"),
            ([{"id": "a", "messages": ["nope"]}], "messages must contain only objects"),
            ([{"id": "a", "source": 5}], "source must be a string"),
            ([{"id": "a", "model_config": "{not json}"}], "model_config must be valid JSON"),
            ([{"id": "a", "model_config": "[1, 2]"}], "model_config must be a JSON object"),
            ([{"id": "a", "model_config": 7}], "model_config must be a JSON object"),
            ([{"id": "a", "messages": [{"role": ""}]}], "role must be a non-empty string"),
            (
                [{"id": "a", "messages": [{"role": "user", "token_count": "many"}]}],
                "token_count must be an integer",
            ),
        ],
    )
    def test_a_malformed_entry_reports_an_error_and_imports_nothing(self, db, payload, expected):
        result = db.import_sessions(payload)

        assert result["ok"] is False
        assert result["imported"] == 0
        assert expected in result["errors"][-1]["error"]
        assert db.get_session("a") is None

    def test_errors_carry_the_payload_index(self, db):
        result = db.import_sessions([{"id": "ok"}, {"id": "bad", "source": 5}])

        assert result["errors"] == [
            {"index": 1, "session_id": "bad", "error": "source must be a string"}
        ]
        # A single bad entry aborts the whole import — the good one is not written.
        assert db.get_session("ok") is None

    def test_an_unserializable_session_is_rejected(self, db):
        result = db.import_sessions([{"id": "a", "title": object()}])

        assert "JSON serializable" in result["errors"][0]["error"]

    def test_per_session_message_and_byte_limits(self, db, monkeypatch):
        monkeypatch.setattr(SessionDB, "_IMPORT_MAX_MESSAGES_PER_SESSION", 1)
        too_many = db.import_sessions(
            [{"id": "a", "messages": [{"role": "user"}, {"role": "assistant"}]}]
        )
        assert "per-session import limit" in too_many["errors"][0]["error"]

        monkeypatch.setattr(SessionDB, "_IMPORT_MAX_SESSION_BYTES", 10)
        too_big = db.import_sessions([{"id": "a", "title": "x" * 100}])
        assert "import size limit" in too_big["errors"][0]["error"]

    def test_total_message_and_byte_limits_span_the_payload(self, db, monkeypatch):
        monkeypatch.setattr(SessionDB, "_IMPORT_MAX_TOTAL_MESSAGES", 1)
        total_messages = db.import_sessions(
            [
                {"id": "a", "messages": [{"role": "user"}]},
                {"id": "b", "messages": [{"role": "user"}]},
            ]
        )
        assert "total import limit" in total_messages["errors"][0]["error"]

        monkeypatch.setattr(SessionDB, "_IMPORT_MAX_TOTAL_BYTES", 60)
        total_bytes = db.import_sessions(
            [{"id": "a", "title": "x" * 40}, {"id": "b", "title": "y" * 40}]
        )
        assert "total size limit" in total_bytes["errors"][0]["error"]


# ── import behavior ──────────────────────────────────────────────────────────


class TestImportSessions:
    def test_an_exported_session_round_trips_into_a_fresh_db(self, db, other_db):
        _session_with_turns(db, "s1", model="test/model", cwd="/repo", title="Original")
        exported = db.export_session("s1")

        result = other_db.import_sessions([exported])

        assert result["ok"] is True
        assert (result["imported"], result["skipped"], result["detached"]) == (1, 0, 0)
        restored = other_db.get_session("s1")
        assert (restored["model"], restored["cwd"], restored["title"]) == (
            "test/model",
            "/repo",
            "Original",
        )
        assert [(m["role"], m["content"]) for m in other_db.get_messages("s1")] == [
            ("user", "hello from s1"),
            ("assistant", "hi from s1"),
        ]

    def test_message_counters_are_recomputed_from_the_imported_rows(self, db):
        result = db.import_sessions(
            [
                {
                    "id": "s1",
                    "message_count": 999,
                    "tool_call_count": 999,
                    "messages": [
                        {
                            "role": "assistant",
                            "content": "working",
                            "tool_calls": [{"id": "c1", "function": {"name": "terminal"}}],
                        },
                        {"role": "tool", "content": "done", "tool_name": "terminal"},
                    ],
                }
            ]
        )

        assert result["imported"] == 1
        row = db.get_session("s1")
        assert row["message_count"] == 2
        assert row["tool_call_count"] == 1

    def test_an_existing_session_id_is_skipped_not_overwritten(self, db):
        _session_with_turns(db, "s1", title="Live")

        result = db.import_sessions([{"id": "s1", "title": "Imported", "messages": []}])

        assert (result["imported"], result["skipped"]) == (0, 1)
        assert result["skipped_ids"] == ["s1"]
        assert db.get_session("s1")["title"] == "Live"
        assert len(db.get_messages("s1")) == 2

    def test_live_runtime_state_is_not_restored(self, db):
        result = db.import_sessions(
            [{"id": "s1", "session_key": "telegram:42", "chat_id": "42", "messages": []}]
        )

        assert result["imported"] == 1
        row = db.get_session("s1")
        assert row["session_key"] is None
        assert row["chat_id"] is None

    def test_a_missing_source_defaults_to_import(self, db):
        db.import_sessions([{"id": "s1", "messages": []}])

        assert db.get_session("s1")["source"] == "import"

    def test_a_missing_started_at_is_stamped_so_the_row_can_be_ordered(self, db):
        db.import_sessions([{"id": "s1", "messages": []}])

        assert db.get_session("s1")["started_at"] > 0

    def test_unparseable_numeric_fields_degrade_instead_of_failing(self, db):
        db.import_sessions(
            [
                {
                    "id": "s1",
                    "started_at": "not a number",
                    "input_tokens": "lots",
                    "estimated_cost_usd": "free",
                    "messages": [],
                }
            ]
        )

        row = db.get_session("s1")
        assert row["started_at"] > 0
        assert row["input_tokens"] == 0
        assert row["estimated_cost_usd"] is None

    def test_archived_flag_is_normalized_to_an_int(self, db):
        db.import_sessions([{"id": "s1", "archived": True, "messages": []}])

        assert db.get_session("s1")["archived"] == 1

    def test_a_model_config_dict_is_stored_as_json(self, db):
        db.import_sessions([{"id": "s1", "model_config": {"provider": "x"}, "messages": []}])

        assert json.loads(db.get_session("s1")["model_config"]) == {"provider": "x"}

    def test_json_encoded_reasoning_sidecars_are_decoded_before_insert(self, db):
        db.import_sessions(
            [
                {
                    "id": "s1",
                    "messages": [
                        {
                            "role": "assistant",
                            "content": "thought",
                            "reasoning_details": json.dumps([{"type": "text", "text": "why"}]),
                        }
                    ],
                }
            ]
        )

        # Stored as TEXT: the pre-decode is what keeps it from double-encoding.
        stored = db.get_messages("s1")[0]["reasoning_details"]
        assert json.loads(stored) == [{"type": "text", "text": "why"}]

    def test_a_parent_included_in_the_same_payload_keeps_its_edge(self, db):
        result = db.import_sessions(
            [
                {"id": "parent", "messages": []},
                {"id": "child", "parent_session_id": "parent", "messages": []},
            ]
        )

        assert result["detached"] == 0
        assert db.get_session("child")["parent_session_id"] == "parent"

    def test_a_parent_already_in_the_db_keeps_its_edge(self, db):
        db.create_session("parent", source="cli")

        result = db.import_sessions([{"id": "child", "parent_session_id": "parent", "messages": []}])

        assert result["detached"] == 0
        assert db.get_session("child")["parent_session_id"] == "parent"

    def test_an_unknown_parent_is_detached_instead_of_failing_the_import(self, db):
        result = db.import_sessions(
            [{"id": "orphan", "parent_session_id": "missing", "messages": []}]
        )

        assert (result["ok"], result["imported"], result["detached"]) == (True, 1, 1)
        assert db.get_session("orphan")["parent_session_id"] is None

    def test_a_cycle_in_the_payload_drops_only_the_closing_edge(self, db):
        result = db.import_sessions(
            [
                {"id": "a", "parent_session_id": "b", "messages": []},
                {"id": "b", "parent_session_id": "a", "messages": []},
            ]
        )

        assert result["imported"] == 2
        assert result["detached"] == 1
        edges = {sid: db.get_session(sid)["parent_session_id"] for sid in ("a", "b")}
        # Exactly one of the two edges survives: the lineage stays acyclic.
        assert sorted(edges.values(), key=lambda v: v or "") == [None, "a"]

    def test_a_self_parent_is_detached(self, db):
        result = db.import_sessions([{"id": "a", "parent_session_id": "a", "messages": []}])

        assert result["detached"] == 1
        assert db.get_session("a")["parent_session_id"] is None

    def test_a_lineage_export_can_be_reimported_as_its_segments(self, db, other_db):
        _session_with_turns(db, "root")
        db.end_session("root", "compression")
        _session_with_turns(db, "tip", parent_session_id="root")
        lineage = db.export_session_lineage("tip")

        result = other_db.import_sessions(lineage["segments"])

        assert (result["imported"], result["detached"]) == (2, 0)
        assert other_db.get_compression_lineage("tip") == ["root", "tip"]
