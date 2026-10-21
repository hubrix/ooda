"""
plugin_api.py — backend routes for the OODA desktop pane.

Mounted at /api/plugins/ooda/. Reached from desktop/plugin.js via ctx.rest.
"""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter

# The plugin package sits one level up; import it directly.
_PLUGIN_DIR = Path(__file__).resolve().parent.parent
if str(_PLUGIN_DIR.parent) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_DIR.parent))

from ooda import prompts, store  # noqa: E402

router = APIRouter()


@router.get("/prompts")
async def list_prompts():
    return {
        "prompts": [
            {
                "key": k,
                "title": prompts[k]["title"],
                "stage": prompts[k]["stage"],
                "why": prompts[k]["why"],
                "prompt": prompts[k]["prompt"],
            }
            for k in prompts.ORDER
        ]
    }


@router.get("/loops")
async def list_loops(limit: int = 20):
    return {"loops": store.list_loops(limit)}


@router.get("/active")
async def active_loop():
    return {"loop": store.active()}


@router.get("/loops/{loop_id}")
async def get_loop(loop_id: str):
    loop = store.get(loop_id)
    return {"loop": loop} if loop else {"error": "not found"}


@router.post("/loops")
async def create_loop(body: dict):
    situation = (body.get("situation") or "").strip()
    if not situation:
        return {"error": "situation required"}
    loop = store.create(situation, (body.get("arena") or "").strip())
    return {"loop": loop}


@router.post("/loops/{loop_id}/record")
async def record(loop_id: str, body: dict):
    stage = (body.get("stage") or "observe").strip().lower()
    content = (body.get("content") or "").strip()
    if not content:
        return {"error": "content required"}
    loop = store.record(loop_id, stage, content)
    return {"loop": loop} if loop else {"error": "not found"}


@router.post("/loops/{loop_id}/close")
async def close(loop_id: str):
    loop = store.close(loop_id)
    return {"loop": loop} if loop else {"error": "not found"}


@router.post("/loops/{loop_id}/reopen")
async def reopen(loop_id: str):
    loop = store.reopen(loop_id)
    return {"loop": loop} if loop else {"error": "not found"}
