"""Tests for the stdio MCP server and the standalone store fallback."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
MCP = PLUGIN_DIR / "mcp" / "ooda_mcp.py"


def _run(messages: list[dict], env_home: str) -> list[dict]:
    payload = "\n".join(json.dumps(m) for m in messages) + "\n"
    proc = subprocess.run(
        [sys.executable, str(MCP)],
        input=payload,
        capture_output=True,
        text=True,
        env={"HERMES_HOME": env_home, "PATH": "/usr/bin:/bin", "HOME": env_home},
        timeout=30,
    )
    assert proc.returncode == 0, proc.stderr
    return [json.loads(line) for line in proc.stdout.splitlines() if line.strip()]


def test_initialize_handshake(tmp_path):
    out = _run(
        [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {}},
            }
        ],
        str(tmp_path),
    )
    assert out[0]["result"]["serverInfo"]["name"] == "ooda"
    assert out[0]["result"]["protocolVersion"] == "2025-06-18"
    assert "tools" in out[0]["result"]["capabilities"]


def test_tools_list_has_all_six(tmp_path):
    out = _run([{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}], str(tmp_path))
    names = [t["name"] for t in out[0]["result"]["tools"]]
    assert names == [
        "ooda_start",
        "ooda_prompt",
        "ooda_record",
        "ooda_status",
        "ooda_move",
        "ooda_list",
    ]
    for t in out[0]["result"]["tools"]:
        assert t["description"]
        assert t["inputSchema"]["type"] == "object"


def test_tools_call_roundtrip(tmp_path):
    out = _run(
        [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {"name": "ooda_start", "arguments": {"situation": "mcp test"}},
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {"name": "ooda_status", "arguments": {}},
            },
        ],
        str(tmp_path),
    )
    first = json.loads(out[0]["result"]["content"][0]["text"])
    assert first["ok"] is True
    second = json.loads(out[1]["result"]["content"][0]["text"])
    assert second["ok"] is True
    assert second["situation"] == "mcp test"


def test_prompts_list_and_get(tmp_path):
    out = _run(
        [
            {"jsonrpc": "2.0", "id": 1, "method": "prompts/list"},
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "prompts/get",
                "params": {"name": "orient-audit", "arguments": {"situation": "a launch"}},
            },
        ],
        str(tmp_path),
    )
    assert len(out[0]["result"]["prompts"]) == 9
    text = out[1]["result"]["messages"][0]["content"]["text"]
    assert "a launch" in text


def test_unknown_tool_and_method(tmp_path):
    out = _run(
        [
            {"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "nope"}},
            {"jsonrpc": "2.0", "id": 2, "method": "bogus/method"},
        ],
        str(tmp_path),
    )
    assert out[0]["error"]["code"] == -32602
    assert out[1]["error"]["code"] == -32601


def test_notifications_get_no_reply(tmp_path):
    out = _run(
        [
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 1, "method": "ping"},
        ],
        str(tmp_path),
    )
    assert len(out) == 1
    assert out[0]["id"] == 1


def test_store_falls_back_without_hermes(tmp_path, monkeypatch):
    """With no plugins.plugin_storage importable, store uses HERMES_HOME."""
    monkeypatch.setenv("HERMES_HOME", str(tmp_path))
    monkeypatch.setitem(sys.modules, "plugins", None)
    monkeypatch.setitem(sys.modules, "plugins.plugin_storage", None)

    import importlib

    import ooda.store as store

    importlib.reload(store)
    loop = store.create("standalone")
    assert loop["id"]
    assert (tmp_path / "plugin-data" / "ooda" / "data.db").exists()
