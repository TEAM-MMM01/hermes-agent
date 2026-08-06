"""Tests for hermes_cli/web_git.py — the dashboard/desktop git backend.

These exercise the real ``git`` binary against throwaway repos under tmp_path
rather than mocking ``subprocess``: the module is a thin translation layer over
porcelain output, so a mocked git would only assert the mock. The porcelain
parsers (``_walk_entries`` and friends) are also driven directly with recorded
records where constructing the state in git would be impractical (unmerged
entries, copy records).
"""

import os
import subprocess

import pytest

from hermes_cli import web_git


def _run(repo, *args):
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
    )


@pytest.fixture
def repo(tmp_path):
    """A repo with one commit on ``main`` and no remote."""
    root = tmp_path / "repo"
    root.mkdir()
    _run(root, "init", "-b", "main")
    _run(root, "config", "user.email", "test@test.com")
    _run(root, "config", "user.name", "Test")
    (root / "kept.txt").write_text("one\ntwo\n")
    _run(root, "add", "-A")
    _run(root, "commit", "-m", "initial")
    return root


# ── path/name helpers ────────────────────────────────────────────────────────


class TestResolveRenamePath:
    def test_plain_path_is_unchanged(self):
        assert web_git.resolve_rename_path("a/b.py") == "a/b.py"
        assert web_git.resolve_rename_path(None) == ""

    def test_flat_rename_resolves_to_the_new_path(self):
        assert web_git.resolve_rename_path("old.py => new.py") == "new.py"

    def test_braced_rename_keeps_the_surrounding_directories(self):
        assert web_git.resolve_rename_path("pkg/{old => new}/mod.py") == "pkg/new/mod.py"

    def test_braced_rename_into_the_parent_does_not_double_slash(self):
        assert web_git.resolve_rename_path("pkg/{old => }/mod.py") == "pkg/mod.py"


class TestSanitizeBranch:
    def test_whitespace_becomes_dashes_and_junk_is_dropped(self):
        assert web_git._sanitize_branch("my cool branch!") == "my-cool-branch"

    def test_runs_are_collapsed_and_edges_trimmed(self):
        assert web_git._sanitize_branch("--a//b..c--") == "a/b.c"

    def test_slashes_dots_and_dashes_survive_inside_the_name(self):
        assert web_git._sanitize_branch("hermes/fix-1.2") == "hermes/fix-1.2"

    def test_a_name_made_only_of_separators_sanitizes_to_empty(self):
        # worktree_add / branch_switch rely on "" to reject the request.
        assert web_git._sanitize_branch("///") == ""
        assert web_git._sanitize_branch(None) == ""


class TestSlugify:
    def test_lowercases_and_hyphenates(self):
        assert web_git._slugify("  Fix The Thing ") == "fix-the-thing"

    def test_falls_back_to_work_when_nothing_survives(self):
        assert web_git._slugify("***") == "work"
        assert web_git._slugify("") == "work"

    def test_is_capped_without_a_trailing_hyphen(self):
        slug = web_git._slugify("a" * 30 + " " + "b" * 30)
        assert len(slug) <= 40
        assert not slug.endswith("-")


# ── porcelain v2 parsing ─────────────────────────────────────────────────────


def _z(*records):
    return "\0".join(records) + "\0"


class TestWalkEntries:
    def test_branch_headers_are_skipped(self):
        raw = _z("# branch.head main", "# branch.ab +1 -2", "1 M. N... 100644 100644 100644 aaa bbb f.py")
        assert list(web_git._walk_entries(raw)) == [("1", "M.", "f.py")]

    def test_untracked_and_unmerged_entries_are_tagged(self):
        raw = _z(
            "? new.py",
            "u UU N... 100644 100644 100644 100644 aaa bbb ccc conflict.py",
        )
        assert list(web_git._walk_entries(raw)) == [
            ("?", "??", "new.py"),
            ("u", "UU", "conflict.py"),
        ]

    def test_rename_yields_the_new_path_and_consumes_the_origin_record(self):
        raw = _z(
            "2 R. N... 100644 100644 100644 aaa bbb R100 new.py",
            "old.py",
            "? after.py",
        )
        assert list(web_git._walk_entries(raw)) == [
            ("2", "R.", "new.py"),
            ("?", "??", "after.py"),
        ]

    def test_paths_with_spaces_survive_the_split(self):
        raw = _z("1 .M N... 100644 100644 100644 aaa bbb my file.py")
        assert list(web_git._walk_entries(raw)) == [("1", ".M", "my file.py")]


class TestEntryClassification:
    def test_staged_only_entry(self):
        assert web_git._classify("1", "M.", "f.py") == {
            "path": "f.py",
            "staged": True,
            "unstaged": False,
            "untracked": False,
            "conflicted": False,
        }

    def test_partially_staged_entry_is_both(self):
        entry = web_git._classify("1", "MM", "f.py")
        assert (entry["staged"], entry["unstaged"]) == (True, True)

    def test_untracked_entry_counts_as_unstaged(self):
        entry = web_git._classify("?", "??", "new.py")
        assert (entry["staged"], entry["unstaged"], entry["untracked"]) == (False, True, True)

    def test_unmerged_entry_is_conflicted_and_not_staged(self):
        entry = web_git._classify("u", "UU", "c.py")
        assert (entry["conflicted"], entry["staged"]) == (True, False)

    def test_status_letter_prefers_the_index_code(self):
        assert web_git._status_letter("1", "AM") == "A"
        assert web_git._status_letter("1", ".M") == "M"
        assert web_git._status_letter("2", "R.") == "R"
        assert web_git._status_letter("?", "??") == "?"
        assert web_git._status_letter("u", "UU") == "U"


class TestParseWorktrees:
    def test_records_are_split_on_the_worktree_line(self):
        out = (
            "worktree /repo\n"
            "HEAD aaa\n"
            "branch refs/heads/main\n"
            "\n"
            "worktree /repo/.worktrees/feat\n"
            "HEAD bbb\n"
            "branch refs/heads/hermes/feat\n"
            "locked\n"
        )
        assert web_git._parse_worktrees(out) == [
            {"path": "/repo", "branch": "main", "detached": False, "bare": False, "locked": False},
            {
                "path": "/repo/.worktrees/feat",
                "branch": "hermes/feat",
                "detached": False,
                "bare": False,
                "locked": True,
            },
        ]

    def test_detached_and_bare_flags(self):
        out = "worktree /bare\nbare\n\nworktree /d\nHEAD aaa\ndetached\n"
        trees = web_git._parse_worktrees(out)
        assert trees[0]["bare"] is True
        assert (trees[1]["detached"], trees[1]["branch"]) == (True, None)

    def test_leading_junk_before_the_first_worktree_is_ignored(self):
        assert web_git._parse_worktrees("branch refs/heads/main\n") == []


# ── untracked line counting ──────────────────────────────────────────────────


class TestUntrackedInsertions:
    def test_counts_a_final_unterminated_line(self, tmp_path):
        (tmp_path / "a.txt").write_bytes(b"one\ntwo")
        assert web_git._untracked_insertions(str(tmp_path), "a.txt") == 2

    def test_counts_terminated_lines(self, tmp_path):
        (tmp_path / "a.txt").write_bytes(b"one\ntwo\n")
        assert web_git._untracked_insertions(str(tmp_path), "a.txt") == 2

    def test_empty_missing_and_binary_files_count_zero(self, tmp_path):
        (tmp_path / "empty.txt").write_bytes(b"")
        (tmp_path / "bin").write_bytes(b"\x00\x01\x02")
        assert web_git._untracked_insertions(str(tmp_path), "empty.txt") == 0
        assert web_git._untracked_insertions(str(tmp_path), "bin") == 0
        assert web_git._untracked_insertions(str(tmp_path), "missing.txt") == 0

    def test_a_directory_counts_zero(self, tmp_path):
        (tmp_path / "sub").mkdir()
        assert web_git._untracked_insertions(str(tmp_path), "sub") == 0

    def test_oversized_files_are_skipped(self, tmp_path, monkeypatch):
        (tmp_path / "big.txt").write_bytes(b"x\n" * 10)
        monkeypatch.setattr(web_git, "_UNTRACKED_LINE_MAX_BYTES", 5)
        assert web_git._untracked_insertions(str(tmp_path), "big.txt") == 0


# ── repo_status ──────────────────────────────────────────────────────────────


class TestRepoStatus:
    def test_non_repo_and_missing_dir_return_none(self, tmp_path):
        assert web_git.repo_status(str(tmp_path / "nope")) is None
        plain = tmp_path / "plain"
        plain.mkdir()
        assert web_git.repo_status(str(plain)) is None

    def test_clean_repo_reports_its_branch_and_no_changes(self, repo):
        status = web_git.repo_status(str(repo))
        assert status["branch"] == "main"
        assert status["defaultBranch"] == "main"
        assert status["detached"] is False
        assert (status["changed"], status["added"], status["removed"]) == (0, 0, 0)
        assert status["files"] == []

    def test_counts_split_across_staged_unstaged_and_untracked(self, repo):
        (repo / "staged.txt").write_text("s\n")
        _run(repo, "add", "staged.txt")
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        (repo / "untracked.txt").write_text("u1\nu2\n")

        status = web_git.repo_status(str(repo))

        # an untracked file is unstaged work too, so it lands in both counts
        assert (status["staged"], status["unstaged"], status["untracked"]) == (1, 2, 1)
        assert status["changed"] == 3
        # staged.txt (+1) and kept.txt (+1) vs HEAD, plus the 2 untracked lines
        # `git diff HEAD` never reports.
        assert status["added"] == 4
        assert status["removed"] == 0

    def test_detached_head_reports_no_branch(self, repo):
        _run(repo, "checkout", "--detach", "HEAD")
        status = web_git.repo_status(str(repo))
        assert status["detached"] is True
        assert status["branch"] is None

    def test_ahead_behind_come_from_the_tracking_branch(self, repo, tmp_path):
        remote = tmp_path / "remote.git"
        _run(repo, "init", "--bare", str(remote))
        _run(repo, "remote", "add", "origin", str(remote))
        _run(repo, "push", "-u", "origin", "main")
        (repo / "kept.txt").write_text("one\ntwo\nlocal\n")
        _run(repo, "commit", "-am", "local only")

        status = web_git.repo_status(str(repo))

        assert (status["ahead"], status["behind"]) == (1, 0)

    def test_file_list_is_capped_at_two_hundred(self, repo):
        for i in range(205):
            (repo / f"f{i:03d}.txt").write_text("x\n")
        status = web_git.repo_status(str(repo))
        assert status["changed"] == 205
        assert len(status["files"]) == 200


# ── review pane ──────────────────────────────────────────────────────────────


class TestReviewList:
    def test_non_repo_returns_an_empty_result(self, tmp_path):
        assert web_git.review_list(str(tmp_path / "nope"), "working", None) == {
            "files": [],
            "base": None,
        }

    def test_working_scope_sums_staged_and_unstaged_counts(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        _run(repo, "add", "kept.txt")
        (repo / "kept.txt").write_text("one\ntwo\nthree\nfour\n")

        result = web_git.review_list(str(repo), "working", None)

        assert result["base"] is None
        assert result["files"] == [
            {"path": "kept.txt", "added": 2, "removed": 0, "status": "M", "staged": True}
        ]

    def test_working_scope_fills_untracked_insertions(self, repo):
        (repo / "new.txt").write_text("a\nb\nc\n")
        files = web_git.review_list(str(repo), "working", None)["files"]
        assert files == [
            {"path": "new.txt", "added": 3, "removed": 0, "status": "?", "staged": False}
        ]

    def test_files_are_sorted_by_path(self, repo):
        for name in ("c.txt", "a.txt", "b.txt"):
            (repo / name).write_text("x\n")
        files = web_git.review_list(str(repo), "working", None)["files"]
        assert [f["path"] for f in files] == ["a.txt", "b.txt", "c.txt"]

    def test_last_turn_scope_diffs_against_the_given_ref(self, repo):
        base = _run(repo, "rev-parse", "HEAD").stdout.strip()
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        _run(repo, "commit", "-am", "turn commit")
        (repo / "brand-new.txt").write_text("n\n")

        result = web_git.review_list(str(repo), "lastTurn", base)

        assert result["base"] == base
        assert result["files"] == [
            {"path": "brand-new.txt", "added": 1, "removed": 0, "status": "?", "staged": False},
            {"path": "kept.txt", "added": 1, "removed": 0, "status": "M", "staged": False},
        ]

    def test_last_turn_without_a_base_ref_is_empty(self, repo):
        assert web_git.review_list(str(repo), "lastTurn", None) == {"files": [], "base": None}

    def test_branch_scope_without_a_trunk_to_compare_is_empty(self, repo):
        _run(repo, "checkout", "-b", "feature")
        _run(repo, "branch", "-D", "main")
        assert web_git.review_list(str(repo), "branch", None) == {"files": [], "base": None}

    def test_branch_scope_diffs_the_merge_base_with_trunk(self, repo):
        _run(repo, "checkout", "-b", "feature")
        (repo / "kept.txt").write_text("one\ntwo\nfeature\n")
        _run(repo, "commit", "-am", "feature work")

        result = web_git.review_list(str(repo), "branch", None)

        assert result["base"]
        assert [f["path"] for f in result["files"]] == ["kept.txt"]


class TestReviewDiff:
    def test_non_repo_returns_empty(self, tmp_path):
        assert web_git.review_diff(str(tmp_path / "nope"), "f.py", "working", None, False) == ""

    def test_worktree_diff_for_a_modified_tracked_file(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        diff = web_git.review_diff(str(repo), "kept.txt", "working", None, False)
        assert "+three" in diff

    def test_staged_diff_ignores_later_worktree_edits(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nstaged\n")
        _run(repo, "add", "kept.txt")
        (repo / "kept.txt").write_text("one\ntwo\nstaged\nworktree\n")

        diff = web_git.review_diff(str(repo), "kept.txt", "working", None, True)

        assert "+staged" in diff
        assert "+worktree" not in diff

    def test_untracked_file_is_rendered_as_an_all_add_diff(self, repo):
        (repo / "new.txt").write_text("fresh\n")
        diff = web_git.review_diff(str(repo), "new.txt", "working", None, False)
        assert "+fresh" in diff

    def test_last_turn_scope_without_a_base_ref_is_empty(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        assert web_git.review_diff(str(repo), "kept.txt", "lastTurn", None, False) == ""

    def test_branch_scope_uses_the_merge_base(self, repo):
        _run(repo, "checkout", "-b", "feature")
        (repo / "kept.txt").write_text("one\ntwo\nfeature\n")
        _run(repo, "commit", "-am", "feature work")

        diff = web_git.review_diff(str(repo), "kept.txt", "branch", None, False)

        assert "+feature" in diff


class TestFileDiffVsHead:
    def test_clean_tracked_file_is_not_all_added(self, repo):
        assert web_git.file_diff_vs_head(str(repo), "kept.txt") == ""

    def test_modified_tracked_file_diffs_against_head(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nthree\n")
        assert "+three" in web_git.file_diff_vs_head(str(repo), "kept.txt")

    def test_untracked_file_is_all_added(self, repo):
        (repo / "new.txt").write_text("fresh\n")
        assert "+fresh" in web_git.file_diff_vs_head(str(repo), "new.txt")

    def test_non_repo_returns_empty(self, tmp_path):
        assert web_git.file_diff_vs_head(str(tmp_path / "nope"), "f.py") == ""


class TestStageUnstageRevert:
    def test_stage_all_then_unstage_one_file(self, repo):
        (repo / "a.txt").write_text("a\n")
        (repo / "b.txt").write_text("b\n")

        assert web_git.review_stage(str(repo), None) == {"ok": True}
        assert {f["path"] for f in web_git.review_list(str(repo), "working", None)["files"] if f["staged"]} == {
            "a.txt",
            "b.txt",
        }

        assert web_git.review_unstage(str(repo), "a.txt") == {"ok": True}
        staged = {f["path"] for f in web_git.review_list(str(repo), "working", None)["files"] if f["staged"]}
        assert staged == {"b.txt"}

    def test_stage_reports_git_failure_as_a_runtime_error(self, repo):
        with pytest.raises(RuntimeError):
            web_git.review_stage(str(repo), "does-not-exist.txt")

    def test_revert_restores_tracked_files_and_removes_untracked_ones(self, repo):
        (repo / "kept.txt").write_text("clobbered\n")
        (repo / "junk.txt").write_text("junk\n")

        assert web_git.review_revert(str(repo), None) == {"ok": True}

        assert (repo / "kept.txt").read_text() == "one\ntwo\n"
        assert not (repo / "junk.txt").exists()
        assert web_git.review_list(str(repo), "working", None)["files"] == []

    def test_revert_of_a_single_file_leaves_the_others_alone(self, repo):
        (repo / "kept.txt").write_text("clobbered\n")
        (repo / "junk.txt").write_text("junk\n")

        web_git.review_revert(str(repo), "kept.txt")

        assert (repo / "kept.txt").read_text() == "one\ntwo\n"
        assert (repo / "junk.txt").exists()


class TestReviewRevParse:
    def test_head_resolves_to_a_sha(self, repo):
        assert web_git.review_rev_parse(str(repo), None) == _run(repo, "rev-parse", "HEAD").stdout.strip()

    def test_unknown_ref_is_none(self, repo):
        assert web_git.review_rev_parse(str(repo), "no/such/ref") is None


class TestReviewCommit:
    def test_unstaged_changes_are_staged_before_committing(self, repo):
        (repo / "new.txt").write_text("n\n")

        assert web_git.review_commit(str(repo), "add new", push=False) == {"ok": True}

        assert _run(repo, "log", "-1", "--pretty=%s").stdout.strip() == "add new"
        assert web_git.review_list(str(repo), "working", None)["files"] == []

    def test_an_existing_staged_set_commits_alone(self, repo):
        (repo / "staged.txt").write_text("s\n")
        _run(repo, "add", "staged.txt")
        (repo / "later.txt").write_text("l\n")

        web_git.review_commit(str(repo), "only staged", push=False)

        committed = _run(repo, "show", "--name-only", "--pretty=format:", "HEAD").stdout.split()
        assert committed == ["staged.txt"]
        assert [f["path"] for f in web_git.review_list(str(repo), "working", None)["files"]] == ["later.txt"]

    def test_nothing_to_commit_raises(self, repo):
        with pytest.raises(RuntimeError):
            web_git.review_commit(str(repo), "empty", push=False)

    def test_push_sets_upstream_on_first_push(self, repo, tmp_path):
        remote = tmp_path / "remote.git"
        _run(repo, "init", "--bare", str(remote))
        _run(repo, "remote", "add", "origin", str(remote))
        (repo / "new.txt").write_text("n\n")

        web_git.review_commit(str(repo), "pushed", push=True)

        assert _run(repo, "rev-parse", "--abbrev-ref", "@{u}").stdout.strip() == "origin/main"
        assert _run(remote, "log", "-1", "--pretty=%s", "main").stdout.strip() == "pushed"

    def test_push_without_a_remote_raises(self, repo):
        (repo / "new.txt").write_text("n\n")
        with pytest.raises(RuntimeError):
            web_git.review_commit(str(repo), "no remote", push=True)


class TestReviewCommitContext:
    def test_non_repo_returns_empty_context(self, tmp_path):
        assert web_git.review_commit_context(str(tmp_path / "nope")) == {"diff": "", "recent": ""}

    def test_staged_changes_win_over_the_worktree_diff(self, repo):
        (repo / "kept.txt").write_text("one\ntwo\nstaged\n")
        _run(repo, "add", "kept.txt")
        (repo / "kept.txt").write_text("one\ntwo\nstaged\nunstaged\n")

        context = web_git.review_commit_context(str(repo))

        assert "+staged" in context["diff"]
        assert "+unstaged" not in context["diff"]
        assert context["recent"] == "initial"

    def test_untracked_files_are_appended_as_a_note(self, repo):
        (repo / "new.txt").write_text("n\n")
        assert "#   new.txt" in web_git.review_commit_context(str(repo))["diff"]

    def test_untracked_note_is_capped_with_an_omitted_count(self, repo, monkeypatch):
        monkeypatch.setattr(web_git, "_COMMIT_CONTEXT_UNTRACKED_MAX", 2)
        for name in ("a.txt", "b.txt", "c.txt", "d.txt"):
            (repo / name).write_text("x\n")

        diff = web_git.review_commit_context(str(repo))["diff"]

        assert "#   a.txt" in diff and "#   b.txt" in diff
        assert "#   c.txt" not in diff
        assert "... 2 more omitted" in diff

    def test_an_oversized_diff_is_truncated_with_a_marker(self, repo, monkeypatch):
        monkeypatch.setattr(web_git, "_COMMIT_CONTEXT_DIFF_MAX_CHARS", 40)
        (repo / "kept.txt").write_text("one\ntwo\n" + "padding line\n" * 20)

        diff = web_git.review_commit_context(str(repo))["diff"]

        assert "diff truncated" in diff
        assert "chars omitted" in diff


# ── ship flow ────────────────────────────────────────────────────────────────


class TestReviewShipInfo:
    def test_non_repo_is_not_gh_ready(self, tmp_path):
        assert web_git.review_ship_info(str(tmp_path / "nope")) == {"ghReady": False, "pr": None}

    def test_unauthenticated_gh_is_not_ready(self, repo, monkeypatch):
        monkeypatch.setattr(web_git, "_gh", lambda cwd, args: (False, ""))
        assert web_git.review_ship_info(str(repo)) == {"ghReady": False, "pr": None}

    def test_authenticated_gh_without_a_pr_is_ready(self, repo, monkeypatch):
        monkeypatch.setattr(
            web_git, "_gh", lambda cwd, args: (True, "") if args[:2] == ["auth", "status"] else (False, "")
        )
        assert web_git.review_ship_info(str(repo)) == {"ghReady": True, "pr": None}

    def test_pr_fields_are_projected(self, repo, monkeypatch):
        payload = '{"url": "https://example.com/pr/7", "state": "OPEN", "number": 7, "extra": "dropped"}'
        monkeypatch.setattr(
            web_git,
            "_gh",
            lambda cwd, args: (True, "") if args[:2] == ["auth", "status"] else (True, payload),
        )

        assert web_git.review_ship_info(str(repo)) == {
            "ghReady": True,
            "pr": {"url": "https://example.com/pr/7", "state": "OPEN", "number": 7},
        }

    def test_unparseable_gh_output_degrades_to_no_pr(self, repo, monkeypatch):
        monkeypatch.setattr(
            web_git,
            "_gh",
            lambda cwd, args: (True, "") if args[:2] == ["auth", "status"] else (True, "not json"),
        )
        assert web_git.review_ship_info(str(repo)) == {"ghReady": True, "pr": None}


class TestReviewCreatePr:
    def test_a_failed_push_does_not_block_pr_creation(self, repo, monkeypatch):
        monkeypatch.setattr(web_git, "_gh", lambda cwd, args: (True, "https://example.com/pr/9\n"))
        # No remote configured, so the push inside review_create_pr fails.
        assert web_git.review_create_pr(str(repo)) == {"url": "https://example.com/pr/9"}

    def test_the_url_is_the_last_non_empty_output_line(self, repo, monkeypatch):
        monkeypatch.setattr(
            web_git, "_gh", lambda cwd, args: (True, "noise\nhttps://example.com/pr/10\n\n")
        )
        assert web_git.review_create_pr(str(repo))["url"] == "https://example.com/pr/10"

    def test_gh_failure_raises(self, repo, monkeypatch):
        monkeypatch.setattr(web_git, "_gh", lambda cwd, args: (False, ""))
        with pytest.raises(RuntimeError):
            web_git.review_create_pr(str(repo))


class TestGhInvocation:
    def test_missing_gh_binary_is_reported_as_failure(self, repo, monkeypatch):
        monkeypatch.setattr(web_git.shutil, "which", lambda name: None)
        assert web_git._gh(str(repo), ["auth", "status"]) == (False, "")

    def test_prompts_are_disabled_for_gh(self, repo, monkeypatch):
        captured = {}

        def fake_run(args, **kwargs):
            captured.update(kwargs)
            return subprocess.CompletedProcess(args, 0, "out", "")

        monkeypatch.setattr(web_git.shutil, "which", lambda name: "/usr/bin/gh")
        monkeypatch.setattr(web_git.subprocess, "run", fake_run)

        assert web_git._gh(str(repo), ["auth", "status"]) == (True, "out")
        assert captured["env"]["GH_PROMPT_DISABLED"] == "1"
        assert captured["stdin"] is subprocess.DEVNULL


# ── worktrees & branches ─────────────────────────────────────────────────────


class TestWorktrees:
    def test_list_flags_the_main_checkout_first(self, repo):
        web_git.worktree_add(str(repo), {"name": "Feature One"})
        trees = web_git.worktree_list(str(repo))

        assert trees[0]["isMain"] is True
        assert trees[0]["path"] == str(repo)
        assert [t["isMain"] for t in trees[1:]] == [False]

    def test_list_on_a_non_repo_is_empty(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        assert web_git.worktree_list(str(plain)) == []

    def test_add_derives_the_branch_and_directory_from_the_name(self, repo):
        result = web_git.worktree_add(str(repo), {"name": "Feature One"})

        assert result["branch"] == "hermes/feature-one"
        assert result["repoRoot"] == str(repo)
        assert result["path"] == str(repo / ".worktrees" / "feature-one")
        assert os.path.isdir(result["path"])

    def test_add_honors_an_explicit_branch_name(self, repo):
        result = web_git.worktree_add(str(repo), {"name": "x", "branch": "my branch!"})
        assert result["branch"] == "my-branch"

    def test_a_second_worktree_with_the_same_name_gets_a_unique_directory(self, repo):
        first = web_git.worktree_add(str(repo), {"name": "dup", "branch": "dup-one"})
        second = web_git.worktree_add(str(repo), {"name": "dup", "branch": "dup-two"})

        assert first["path"] != second["path"]
        assert second["path"].endswith("dup-2")

    def test_an_existing_branch_is_reused_when_the_worktree_add_collides(self, repo):
        _run(repo, "branch", "taken")
        result = web_git.worktree_add(str(repo), {"name": "taken-work", "branch": "taken"})
        assert result["branch"] == "taken"
        assert os.path.isdir(result["path"])

    def test_add_from_a_base_ref(self, repo):
        base = _run(repo, "rev-parse", "HEAD").stdout.strip()
        (repo / "kept.txt").write_text("one\ntwo\nmoved on\n")
        _run(repo, "commit", "-am", "second")

        result = web_git.worktree_add(str(repo), {"name": "from-base", "base": base})

        head = _run(result["path"], "rev-parse", "HEAD").stdout.strip()
        assert head == base

    def test_add_initializes_a_plain_directory(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()

        result = web_git.worktree_add(str(plain), {"name": "first"})

        assert result["branch"] == "hermes/first"
        assert (plain / ".git").exists()

    def test_existing_branch_request_switches_in_place_on_trunk(self, repo):
        _run(repo, "checkout", "-b", "side")

        result = web_git.worktree_add(str(repo), {"existingBranch": "main"})

        assert result == {"path": str(repo), "branch": "main", "repoRoot": str(repo)}
        assert _run(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "main"

    def test_existing_non_trunk_branch_gets_its_own_worktree(self, repo):
        _run(repo, "branch", "side")

        result = web_git.worktree_add(str(repo), {"existingBranch": "side"})

        assert result["branch"] == "side"
        assert result["path"] == str(repo / ".worktrees" / "side")

    def test_an_unusable_existing_branch_name_is_rejected(self, repo):
        with pytest.raises(RuntimeError):
            web_git.worktree_add(str(repo), {"existingBranch": "///"})

    def test_remove_drops_the_worktree(self, repo):
        added = web_git.worktree_add(str(repo), {"name": "temp"})

        assert web_git.worktree_remove(str(repo), added["path"], force=False) == {
            "removed": added["path"]
        }
        assert [t["path"] for t in web_git.worktree_list(str(repo))] == [str(repo)]

    def test_remove_of_a_dirty_worktree_needs_force(self, repo):
        added = web_git.worktree_add(str(repo), {"name": "dirty"})
        (repo / ".worktrees" / "dirty" / "scratch.txt").write_text("x\n")

        with pytest.raises(RuntimeError):
            web_git.worktree_remove(str(repo), added["path"], force=False)

        web_git.worktree_remove(str(repo), added["path"], force=True)
        assert [t["path"] for t in web_git.worktree_list(str(repo))] == [str(repo)]


class TestBranchList:
    def test_default_and_checked_out_branches_are_flagged(self, repo):
        added = web_git.worktree_add(str(repo), {"name": "feat", "branch": "feat"})

        by_name = {b["name"]: b for b in web_git.branch_list(str(repo))}

        assert by_name["main"]["isDefault"] is True
        assert by_name["main"]["checkedOut"] is True
        assert by_name["feat"]["isDefault"] is False
        assert by_name["feat"]["worktreePath"] == added["path"]

    def test_non_repo_is_empty(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        assert web_git.branch_list(str(plain)) == []


class TestBranchSwitch:
    def test_switch_sanitizes_and_moves_head(self, repo):
        _run(repo, "branch", "target")
        assert web_git.branch_switch(str(repo), " target ") == {"branch": "target"}
        assert _run(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip() == "target"

    def test_an_empty_name_is_rejected_before_git_runs(self, repo):
        with pytest.raises(RuntimeError, match="required"):
            web_git.branch_switch(str(repo), "///")

    def test_an_unknown_branch_raises(self, repo):
        with pytest.raises(RuntimeError):
            web_git.branch_switch(str(repo), "missing")


class TestBaseBranchList:
    def test_local_trunk_is_flagged_when_there_is_no_remote(self, repo):
        _run(repo, "branch", "side")

        entries = web_git.base_branch_list(str(repo))

        by_name = {e["name"]: e for e in entries}
        assert by_name["main"]["isDefault"] is True
        assert by_name["main"]["isRemote"] is False
        assert by_name["side"]["isDefault"] is False

    def test_remote_default_wins_and_remotes_are_flagged(self, repo, tmp_path):
        remote = tmp_path / "remote.git"
        _run(repo, "init", "--bare", str(remote))
        _run(repo, "remote", "add", "origin", str(remote))
        _run(repo, "push", "-u", "origin", "main")
        _run(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")

        by_name = {e["name"]: e for e in web_git.base_branch_list(str(repo))}

        assert by_name["origin/main"] == {"name": "origin/main", "isRemote": True, "isDefault": True}
        assert by_name["main"]["isDefault"] is False

    def test_non_repo_is_empty(self, tmp_path):
        plain = tmp_path / "plain"
        plain.mkdir()
        assert web_git.base_branch_list(str(plain)) == []


class TestDefaultBranchResolution:
    def test_configured_init_default_branch_is_used_without_a_remote(self, repo):
        _run(repo, "checkout", "-b", "trunk")
        _run(repo, "branch", "-D", "main")
        _run(repo, "config", "init.defaultBranch", "trunk")
        assert web_git._default_branch(str(repo)) == "trunk"

    def test_master_is_recognized_as_a_trunk(self, repo):
        _run(repo, "branch", "-m", "main", "master")
        assert web_git._default_branch(str(repo)) == "master"
        assert web_git._default_branch_name(str(repo)) == "master"

    def test_no_trunk_at_all_resolves_to_nothing(self, repo):
        _run(repo, "checkout", "-b", "only-branch")
        _run(repo, "branch", "-D", "main")
        assert web_git._default_branch(str(repo)) == ""
        assert web_git._default_branch_name(str(repo)) is None


class TestGitInvocation:
    def test_a_failed_invocation_is_reported_not_raised(self, repo, monkeypatch):
        def boom(*args, **kwargs):
            raise OSError("no git")

        monkeypatch.setattr(web_git.subprocess, "run", boom)

        assert web_git._git(str(repo), ["status"]) == (1, "", "git invocation failed")
        assert web_git._git_out(str(repo), ["status"]) == ""

    def test_git_runs_non_interactively(self, repo, monkeypatch):
        captured = {}

        def fake_run(args, **kwargs):
            captured.update(kwargs)
            return subprocess.CompletedProcess(args, 0, "out", "")

        monkeypatch.setattr(web_git.subprocess, "run", fake_run)

        assert web_git._git(str(repo), ["status"]) == (0, "out", "")
        assert captured["stdin"] is subprocess.DEVNULL
        assert captured["env"]["GIT_TERMINAL_PROMPT"] == "0"
