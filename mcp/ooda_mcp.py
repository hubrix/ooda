#!/usr/bin/env python3
"""
ooda_mcp.py — stdio MCP server exposing the OODA loop tools.

Zero dependencies: pure stdlib JSON-RPC 2.0 over newline-delimited stdio.
Works with Claude Code, Codex CLI, Hermes, or any MCP client.

    python3 mcp/ooda_mcp.py

Tools: ooda_start, ooda_prompt, ooda_record, ooda_status, ooda_move, ooda_list
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_DIR.parent))

from ooda import prompts, schemas, tools  # noqa: E402

PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "ooda"
SERVER_VERSION = "1.0.0"

TOOL_SCHEMAS = [
    schemas.OODA_START,
    schemas.OODA_PROMPT,
    schemas.OODA_RECORD,
    schemas.OODA_STATUS,
    schemas.OODA_MOVE,
    schemas.OODA_LIST,
]

HANDLERS = {
    "ooda_start": tools.ooda_start,
    "ooda_prompt": tools.ooda_prompt,
    "ooda_record": tools.ooda_record,
    "ooda_status": tools.ooda_status,
    "ooda_move": tools.ooda_move,
    "ooda_list": tools.ooda_list,
}


def _send(msg: dict) -> None:
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _result(msg_id, result: dict) -> None:
    _send({"jsonrpc": "2.0", "id": msg_id, "result": result})


def _error(msg_id, code: int, message: str) -> None:
    _send({"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}})


def _text(payload: str) -> dict:
    return {"content": [{"type": "text", "text": payload}]}


def handle(msg: dict) -> None:
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    if method == "initialize":
        _result(
            msg_id,
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "instructions": (
                    "John Boyd's OODA loop. Orientation is the center, not speed. "
                    "ooda_start opens a loop; ooda_prompt returns a Boyd prompt verbatim; "
                    "ooda_record persists findings and advances the stage; ooda_move "
                    "records THE MOVE and closes the loop."
                ),
            },
        )
        return

    if method in ("notifications/initialized", "notifications/cancelled"):
        return

    if method == "ping":
        _result(msg_id, {})
        return

    if method == "tools/list":
        _result(
            msg_id,
            {
                "tools": [
                    {
                        "name": s["name"],
                        "description": s["description"],
                        "inputSchema": s["parameters"],
                    }
                    for s in TOOL_SCHEMAS
                ]
            },
        )
        return

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        handler = HANDLERS.get(name)
        if handler is None:
            _error(msg_id, -32602, f"unknown tool '{name}'")
            return
        try:
            payload = handler(args)
        except Exception as exc:  # handlers already catch, this is belt-and-braces
            payload = json.dumps({"ok": False, "error": str(exc)})
        _result(msg_id, _text(payload))
        return

    if method == "resources/list":
        _result(msg_id, {"resources": []})
        return

    if method == "prompts/list":
        _result(
            msg_id,
            {
                "prompts": [
                    {
                        "name": k,
                        "description": prompts.PROMPTS[k]["title"],
                        "arguments": [
                            {
                                "name": "situation",
                                "description": "Situation to substitute into the prompt",
                                "required": False,
                            }
                        ],
                    }
                    for k in prompts.ORDER
                ]
            },
        )
        return

    if method == "prompts/get":
        key = params.get("name") or ""
        rec = prompts.get(key)
        if rec is None:
            _error(msg_id, -32602, f"unknown prompt '{key}'")
            return
        situation = (params.get("arguments") or {}).get("situation", "")
        _result(
            msg_id,
            {
                "description": rec["title"],
                "messages": [
                    {
                        "role": "user",
                        "content": {"type": "text", "text": prompts.render(key, situation)},
                    }
                ],
            },
        )
        return

    if msg_id is not None:
        _error(msg_id, -32601, f"method not found: {method}")


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        try:
            handle(msg)
        except Exception as exc:  # never die on one bad message
            if msg.get("id") is not None:
                _error(msg["id"], -32603, str(exc))


if __name__ == "__main__":
    main()
