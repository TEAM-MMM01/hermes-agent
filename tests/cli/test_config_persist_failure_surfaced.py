"""A failed config.yaml write must never be reported as a saved setting.

``save_config_value()`` signals failure by logging and returning ``False`` —
nothing raises. Several settings surfaces called it for effect and printed
their confirmation unconditionally, so a read-only / full / root-owned
``config.yaml`` produced "Saved to config.yaml", "Reasoning display: ON
(saved)" or ``scope: "global"`` while the value only ever existed in memory.
The user then found the setting reverted on the next launch with no visible
explanation (the only trace was an ERROR line in errors.log).

These tests pin the contract on each fixed surface: on a failed write the
confirmation is downgraded to say the change is session-scoped, and the
write-approval gate (a safety toggle) reports an outright failure.
"""

import types

import pytest


def _switch_result(base_url="https://api.minimax.io/v1", api_mode="chat_completions"):
    return types.SimpleNamespace(
        success=True,
        new_model="MiniMax-M3",
        target_provider="custom:minimax",
        provider_changed=True,
        api_key="sk-minimax",
        base_url=base_url,
        api_mode=api_mode,
        warning_message="",
        provider_label="MiniMax (custom)",
        resolved_via_alias=False,
        capabilities=None,
        model_info=None,
        is_global=True,
        error_message="",
    )


class _StubCLI:
    """Minimum attrs `_apply_model_switch_result` reads on self."""

    agent = None
    model = "old-model"
    provider = "copilot"
    requested_provider = "copilot"
    api_key = "sk-old"
    base_url = "https://api.githubcopilot.com"
    api_mode = "chat_completions"
    _explicit_api_key = ""
    _explicit_base_url = ""
    conversation_history = []
    _pending_model_switch_note = ""


# ---------------------------------------------------------------------------
# CLI /model --global
# ---------------------------------------------------------------------------


def test_persist_global_model_switch_attempts_every_key_and_reports_failure(monkeypatch):
    """A failing key must not short-circuit the rest: a half-written ``model:``
    block (new model, previous provider's base_url) routes the next launch at
    the old host. The helper still reports the overall failure."""
    import cli as cli_mod

    attempted = []

    def _fake_save(key, value):
        attempted.append((key, value))
        return key != "model.provider"

    monkeypatch.setattr(cli_mod, "save_config_value", _fake_save)

    assert cli_mod._persist_global_model_switch(_switch_result()) is False
    assert [key for key, _ in attempted] == [
        "model.default",
        "model.provider",
        "model.base_url",
        "model.api_mode",
    ]


def test_persist_global_model_switch_reports_success_when_all_keys_land(monkeypatch):
    import cli as cli_mod

    monkeypatch.setattr(cli_mod, "save_config_value", lambda *a: True)

    assert cli_mod._persist_global_model_switch(_switch_result()) is True


@pytest.mark.parametrize("saved", [True, False])
def test_apply_model_switch_result_only_claims_saved_when_write_landed(monkeypatch, saved):
    import cli as cli_mod

    printed = []
    monkeypatch.setattr(cli_mod, "_cprint", lambda msg="", *a, **k: printed.append(str(msg)))
    monkeypatch.setattr(cli_mod, "save_config_value", lambda *a: saved)

    cli_mod.HermesCLI._apply_model_switch_result(_StubCLI(), _switch_result(), True)

    out = "\n".join(printed)
    if saved:
        assert "Saved to config.yaml" in out
        assert "session only" not in out
    else:
        assert "Saved to config.yaml" not in out
        assert "session only" in out


# ---------------------------------------------------------------------------
# CLI /reasoning display toggles
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("arg", ["show", "hide", "full", "clamp"])
@pytest.mark.parametrize("saved", [True, False])
def test_reasoning_display_toggle_reports_persist_failure(monkeypatch, arg, saved):
    import cli as cli_mod
    from hermes_cli.cli_commands_mixin import CLICommandsMixin

    printed = []
    monkeypatch.setattr(cli_mod, "_cprint", lambda msg="", *a, **k: printed.append(str(msg)))
    monkeypatch.setattr(cli_mod, "save_config_value", lambda *a: saved)

    cli = types.SimpleNamespace(
        agent=None,
        show_reasoning=False,
        reasoning_full=False,
        reasoning_config={},
    )
    CLICommandsMixin._handle_reasoning_command(cli, f"/reasoning {arg}")

    out = "\n".join(printed)
    if saved:
        assert "(saved)" in out
        assert "Failed to save" not in out
    else:
        assert "(saved)" not in out
        assert "Failed to save to config.yaml" in out


# ---------------------------------------------------------------------------
# write-approval gate (/memory approval, /skills approval)
# ---------------------------------------------------------------------------


def test_write_approval_gate_change_fails_loudly(monkeypatch):
    """The approval gate is a safety control: a persist failure must surface as
    a failure, matching the gateway's set_mode_fn (which raises from
    atomic_config_write)."""
    import cli as cli_mod
    from hermes_cli.cli_commands_mixin import CLICommandsMixin
    from hermes_cli.write_approval_commands import handle_pending_subcommand
    from tools import write_approval as wa

    monkeypatch.setattr(cli_mod, "save_config_value", lambda *a: False)
    cli = types.SimpleNamespace()

    with pytest.raises(RuntimeError):
        CLICommandsMixin._save_write_approval(cli, "memory", True)

    out = handle_pending_subcommand(
        wa.MEMORY,
        ["approval", "on"],
        set_mode_fn=lambda enabled: CLICommandsMixin._save_write_approval(
            cli, "memory", enabled
        ),
    )
    assert "Failed to set memory.write_approval" in out


def test_write_approval_gate_confirms_when_write_lands(monkeypatch):
    import cli as cli_mod
    from hermes_cli.cli_commands_mixin import CLICommandsMixin
    from hermes_cli.write_approval_commands import handle_pending_subcommand
    from tools import write_approval as wa

    monkeypatch.setattr(cli_mod, "save_config_value", lambda *a: True)
    cli = types.SimpleNamespace()

    out = handle_pending_subcommand(
        wa.SKILLS,
        ["approval", "off"],
        set_mode_fn=lambda enabled: CLICommandsMixin._save_write_approval(
            cli, "skills", enabled
        ),
    )
    assert "Failed" not in out
    assert "off" in out


# ---------------------------------------------------------------------------
# TUI gateway /model --global
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("saved", [True, False])
def test_tui_model_switch_scope_reflects_persist_outcome(monkeypatch, saved):
    from tui_gateway import server

    result = _switch_result(base_url="", api_mode="chat_completions")
    monkeypatch.setattr("hermes_cli.model_switch.switch_model", lambda **kw: result)
    monkeypatch.setattr(
        "hermes_cli.model_cost_guard.expensive_model_warning", lambda *a, **k: None
    )
    monkeypatch.setattr("cli.save_config_value", lambda *a: saved)

    out = server._apply_model_switch(
        "sid",
        {"agent": None},
        "MiniMax-M3 --provider nous --global",
        persist_override=True,
    )

    assert out["value"] == "MiniMax-M3"
    if saved:
        assert out["scope"] == "global"
        assert "config.yaml" not in out["warning"]
    else:
        # Reporting "global" for a config.yaml we failed to write is the lie
        # this guards: the switch is live, but only for this session.
        assert out["scope"] == "session"
        assert "current session only" in out["warning"]
