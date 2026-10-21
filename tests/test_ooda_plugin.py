"""Tests for the ooda plugin — store, prompts, tools, registration."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

PLUGIN_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_DIR.parent))

from ooda import prompts, schemas, store, tools  # noqa: E402


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path, monkeypatch):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    yield


def test_prompt_catalog_is_complete():
    assert len(prompts.ORDER) == 9
    assert set(prompts.ORDER) == set(prompts.PROMPTS)
    for key in prompts.ORDER:
        rec = prompts.PROMPTS[key]
        assert rec["stage"] in store.STAGES
        assert len(rec["prompt"]) > 200
        assert rec["title"]


def test_get_resolves_stage_names():
    assert prompts.get("observe")["stage"] == "observe"
    assert prompts.get("orient")["stage"] == "orient"
    assert prompts.get("nope") is None


def test_render_substitutes_situation():
    out = prompts.render("observe-audit", "a competitor launch")
    assert "a competitor launch" in out
    assert "[describe" not in out.split("\n")[0]


def test_store_lifecycle():
    loop = store.create("ship the thing", arena="market")
    assert loop["stage"] == "observe"
    assert loop["status"] == "open"
    assert store.active()["id"] == loop["id"]

    store.record(loop["id"], "observe", "three facts")
    assert store.get(loop["id"])["stage"] == "orient"

    store.record(loop["id"], "orient", "stale assumption found")
    store.close(loop["id"])
    assert store.get(loop["id"])["status"] == "closed"
    assert store.active() is None


def test_store_unknown_loop():
    assert store.get("nope") is None
    assert store.record("nope", "observe", "x") is None
    assert store.close("nope") is None


def test_tool_start_and_record():
    out = json.loads(tools.ooda_start({"situation": "a stalled launch"}))
    assert out["ok"] is True
    loop_id = out["loop_id"]
    assert "Observation" in out["next_prompt"]

    rec = json.loads(tools.ooda_record({"loop_id": loop_id, "stage": "observe", "content": "raw facts"}))
    assert rec["ok"] is True
    assert rec["stage"] == "orient"


def test_tool_start_requires_situation():
    assert json.loads(tools.ooda_start({}))["ok"] is False


def test_tool_prompt_unknown_key():
    out = json.loads(tools.ooda_prompt({"key": "bogus"}))
    assert out["ok"] is False
    assert "available" in out


def test_tool_move_closes_loop():
    loop_id = json.loads(tools.ooda_start({"situation": "s"}))["loop_id"]
    out = json.loads(
        tools.ooda_move(
            {"loop_id": loop_id, "decision": "d", "action": "a", "observation": "o"}
        )
    )
    assert out["ok"] is True
    assert out["status"] == "closed"
    assert store.get(loop_id)["status"] == "closed"


def test_tool_status_without_loop():
    assert json.loads(tools.ooda_status({}))["ok"] is False


def test_tool_list():
    tools.ooda_start({"situation": "one"})
    out = json.loads(tools.ooda_list({}))
    assert out["ok"] is True
    assert out["count"] == 1


def test_schemas_declared_in_manifest():
    import yaml

    manifest = yaml.safe_load((PLUGIN_DIR / "plugin.yaml").read_text())
    declared = set(manifest["provides_tools"])
    registered = {
        schemas.OODA_START["name"],
        schemas.OODA_PROMPT["name"],
        schemas.OODA_RECORD["name"],
        schemas.OODA_STATUS["name"],
        schemas.OODA_MOVE["name"],
        schemas.OODA_LIST["name"],
    }
    assert declared == registered


def test_register_wires_everything():
    class FakeCtx:
        def __init__(self):
            self.tools, self.commands, self.skills, self.hooks, self.cli = [], [], [], [], []

        def register_tool(self, name, toolset, schema, handler):
            self.tools.append(name)

        def register_command(self, name, handler, description=""):
            self.commands.append(name)

        def register_skill(self, name, path):
            self.skills.append(name)

        def register_hook(self, name, fn):
            self.hooks.append(name)

        def register_cli_command(self, name, help, setup_fn, handler_fn):
            self.cli.append(name)

        def get_config(self, key, default=None):
            return default

    import ooda

    ctx = FakeCtx()
    ooda.register(ctx)

    assert set(ctx.tools) == {
        "ooda_start", "ooda_prompt", "ooda_record", "ooda_status", "ooda_move", "ooda_list"
    }
    assert "ooda" in ctx.commands
    assert "ooda-full" in ctx.commands
    assert "ooda-loop" in ctx.skills
    assert len(ctx.skills) == 10
    assert ctx.hooks == ["pre_llm_call"]
    assert ctx.cli == ["ooda"]


def test_hook_injects_active_loop():
    import ooda

    class Ctx:
        def get_config(self, key, default=None):
            return default

    ooda._CTX = Ctx()
    loop_id = json.loads(tools.ooda_start({"situation": "a competitor launch"}))["loop_id"]
    tools.ooda_record({"loop_id": loop_id, "stage": "orient", "content": "stale read"})

    out = ooda._inject_active_loop("sess", "what next?")
    assert out is not None
    assert "a competitor launch" in out["context"]
    assert "stale read" in out["context"]


def test_hook_no_loop_returns_none():
    import ooda

    class Ctx:
        def get_config(self, key, default=None):
            return default

    ooda._CTX = Ctx()
    assert ooda._inject_active_loop("sess", "hi") is None


def test_hook_respects_disable_flag():
    import ooda

    class Ctx:
        def get_config(self, key, default=None):
            return False if key == "inject_active_loop" else default

    ooda._CTX = Ctx()
    tools.ooda_start({"situation": "s"})
    assert ooda._inject_active_loop("sess", "hi") is None
