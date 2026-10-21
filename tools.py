"""tools.py — tool handlers. Always return a JSON string, never raise."""

from __future__ import annotations

import json

from . import prompts, store


def _ok(**kw) -> str:
    return json.dumps({"ok": True, **kw}, ensure_ascii=False)


def _err(msg: str, **kw) -> str:
    return json.dumps({"ok": False, "error": msg, **kw}, ensure_ascii=False)


def ooda_start(args: dict, **kwargs) -> str:
    situation = (args.get("situation") or "").strip()
    if not situation:
        return _err("situation is required")
    arena = (args.get("arena") or "").strip()
    try:
        loop = store.create(situation, arena)
    except Exception as exc:  # pragma: no cover - defensive
        return _err(f"could not create loop: {exc}")
    return _ok(
        loop_id=loop["id"],
        stage=loop["stage"],
        situation=loop["situation"],
        next_prompt=prompts.render("observe-audit", situation),
        note="Run the Observe prompt, then ooda_record the findings.",
    )


def ooda_prompt(args: dict, **kwargs) -> str:
    key = (args.get("key") or "").strip()
    rec = prompts.get(key)
    if rec is None:
        return _err(
            f"unknown prompt '{key}'",
            available=prompts.ORDER,
        )
    return _ok(
        key=key,
        title=rec["title"],
        stage=rec["stage"],
        why=rec["why"],
        prompt=prompts.render(key, (args.get("situation") or "").strip()),
    )


def ooda_record(args: dict, **kwargs) -> str:
    loop_id = (args.get("loop_id") or "").strip()
    stage = (args.get("stage") or "").strip().lower()
    content = (args.get("content") or "").strip()
    if not loop_id or not content:
        return _err("loop_id and content are required")
    if stage not in store.STAGES:
        return _err(f"stage must be one of {store.STAGES}")
    try:
        loop = store.record(loop_id, stage, content)
    except Exception as exc:  # pragma: no cover
        return _err(f"could not record: {exc}")
    if loop is None:
        return _err(f"no loop '{loop_id}'")
    return _ok(loop_id=loop["id"], stage=loop["stage"], entries=len(loop["entries"]))


def ooda_status(args: dict, **kwargs) -> str:
    loop_id = (args.get("loop_id") or "").strip()
    try:
        loop = store.get(loop_id) if loop_id else store.active()
    except Exception as exc:  # pragma: no cover
        return _err(f"could not read state: {exc}")
    if loop is None:
        return _err("no open loop" if not loop_id else f"no loop '{loop_id}'")
    return _ok(**loop)


def ooda_move(args: dict, **kwargs) -> str:
    loop_id = (args.get("loop_id") or "").strip()
    decision = (args.get("decision") or "").strip()
    action = (args.get("action") or "").strip()
    observation = (args.get("observation") or "").strip()
    if not all([loop_id, decision, action, observation]):
        return _err("loop_id, decision, action and observation are all required")
    try:
        if store.get(loop_id) is None:
            return _err(f"no loop '{loop_id}'")
        store.record(loop_id, "act", f"DECISION: {decision}")
        store.record(loop_id, "act", f"ACTION: {action}")
        loop = store.record(loop_id, "act", f"OBSERVATION: {observation}")
        loop = store.close(loop_id)
    except Exception as exc:  # pragma: no cover
        return _err(f"could not record move: {exc}")
    return _ok(loop_id=loop["id"], status=loop["status"], entries=len(loop["entries"]))


def ooda_list(args: dict, **kwargs) -> str:
    try:
        limit = int(args.get("limit") or 20)
    except Exception:
        limit = 20
    try:
        loops = store.list_loops(max(1, min(limit, 100)))
    except Exception as exc:  # pragma: no cover
        return _err(f"could not list: {exc}")
    return _ok(count=len(loops), loops=loops)
