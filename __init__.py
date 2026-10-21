"""
ooda — John Boyd's OODA loop as a working system.

Registers: bundled skills (the nine Boyd prompts + a hub), loop-state tools,
slash commands, a CLI subcommand, and a pre_llm_call hook that keeps the
active loop in context.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from . import prompts, schemas, store, tools

logger = logging.getLogger(__name__)

PLUGIN_DIR = Path(__file__).parent
SKILLS_DIR = PLUGIN_DIR / "skills"

# Slash-command -> prompt key
COMMANDS = {
    "ooda": None,
    "ooda-observe": "observe-audit",
    "ooda-orient": "orient-audit",
    "ooda-destroy": "destruction-creation",
    "ooda-mismatch": "mismatch-detector",
    "ooda-tempo": "tempo",
    "ooda-effort": "main-effort",
    "ooda-isolate": "interaction-isolation",
    "ooda-tobetodo": "to-be-or-to-do",
    "ooda-full": "full-boyd-loop",
}


# --------------------------------------------------------------------------- #
# hook
# --------------------------------------------------------------------------- #
def _inject_active_loop(session_id: str, user_message: str, **kwargs):
    """Prepend the active loop's situation + orientation to the turn."""
    try:
        if not _cfg("inject_active_loop", True):
            return None
        loop = store.active()
        if loop is None:
            return None
        budget = int(_cfg("max_inject_chars", 1200) or 1200)
        lines = [
            f"[OODA loop {loop['id']} — stage: {loop['stage']}]",
            f"Situation: {loop['situation']}",
        ]
        if loop["arena"]:
            lines.append(f"Arena: {loop['arena']}")
        # latest orient/decide entries are the ones that keep the model oriented
        for entry in loop["entries"][-6:]:
            lines.append(f"- ({entry['stage']}) {entry['content']}")
        lines.append(
            "Stay in Boyd's frame: orientation at the center, mismatches over speed. "
            "Use ooda_record to persist findings and ooda_move to converge."
        )
        text = "\n".join(lines)
        if len(text) > budget:
            text = text[:budget] + " …"
        return {"context": text}
    except Exception as exc:  # never break the turn
        logger.debug("ooda inject failed: %s", exc)
        return None


def _cfg(key: str, default):
    try:
        return _CTX.get_config(key, default=default)
    except Exception:
        return default


_CTX = None


# --------------------------------------------------------------------------- #
# slash commands
# --------------------------------------------------------------------------- #
def _handle_ooda(raw_args: str) -> str:
    arg = (raw_args or "").strip()
    if arg in ("", "status"):
        loop = store.active()
        if loop is None:
            return (
                "No open OODA loop. `/ooda <situation>` to start one, or "
                "`/ooda-full <situation>` for the master prompt."
            )
        return (
            f"Loop {loop['id']} — stage {loop['stage']} ({loop['status']})\n"
            f"Situation: {loop['situation']}\n"
            f"Entries: {len(loop['entries'])}\n"
            "Commands: /ooda-observe /ooda-orient /ooda-destroy /ooda-mismatch "
            "/ooda-tempo /ooda-effort /ooda-isolate /ooda-tobetodo /ooda-full"
        )
    if arg == "list":
        loops = store.list_loops(10)
        if not loops:
            return "No loops yet."
        return "\n".join(f"{l['id']} [{l['stage']}/{l['status']}] {l['situation'][:70]}" for l in loops)
    if arg.startswith("close"):
        loop_id = arg.split(maxsplit=1)[1].strip() if " " in arg else ""
        loop = store.close(loop_id) if loop_id else None
        return f"Closed {loop['id']}." if loop else "Usage: /ooda close <loop_id>"
    # otherwise treat the argument as a situation and start a loop
    loop = store.create(arg)
    return (
        f"Loop {loop['id']} opened.\n\n"
        + prompts.render("observe-audit", arg)
    )


def _make_stage_handler(key: str):
    def handler(raw_args: str) -> str:
        situation = (raw_args or "").strip()
        loop = store.active()
        if loop is None:
            if not situation:
                return "No open loop — pass a situation: `/ooda <situation>` first."
            loop = store.create(situation)
        text = prompts.render(key, situation or loop["situation"])
        return f"Loop {loop['id']} · {prompts.get(key)['title']}\n\n{text}"

    return handler


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _cli(args) -> None:
    sub = getattr(args, "ooda_command", None)
    if sub == "list":
        loops = store.list_loops(50)
        if not loops:
            print("No loops.")
            return
        for l in loops:
            print(f"{l['id']}  [{l['stage']}/{l['status']}]  {l['situation'][:80]}")
    elif sub == "show":
        loop = store.get(args.loop_id) if getattr(args, "loop_id", None) else store.active()
        if loop is None:
            print("No such loop.")
            return
        print(json.dumps(loop, indent=2, ensure_ascii=False))
    elif sub == "prompt":
        rec = prompts.get(args.key)
        if rec is None:
            print(f"Unknown prompt. Available: {', '.join(prompts.ORDER)}")
            return
        print(rec["title"])
        print()
        print(prompts.render(args.key, getattr(args, "situation", "") or ""))
    else:
        print("Usage: hermes ooda <list|show|prompt> [args]")


def _cli_setup(subparser) -> None:
    subs = subparser.add_subparsers(dest="ooda_command")
    subs.add_parser("list", help="List loops")
    p_show = subs.add_parser("show", help="Show a loop (default: active)")
    p_show.add_argument("loop_id", nargs="?")
    p_prompt = subs.add_parser("prompt", help="Print a Boyd prompt")
    p_prompt.add_argument("key", choices=prompts.ORDER)
    p_prompt.add_argument("--situation", default="")
    subparser.set_defaults(func=_cli)


# --------------------------------------------------------------------------- #
# register
# --------------------------------------------------------------------------- #
def register(ctx) -> None:
    global _CTX
    _CTX = ctx

    # bundled skills -> skill_view("ooda:<name>")
    if SKILLS_DIR.is_dir():
        for child in sorted(SKILLS_DIR.iterdir()):
            skill_md = child / "SKILL.md"
            if child.is_dir() and skill_md.exists():
                ctx.register_skill(child.name, skill_md)

    # tools
    ctx.register_tool(name="ooda_start", toolset="ooda", schema=schemas.OODA_START, handler=tools.ooda_start)
    ctx.register_tool(name="ooda_prompt", toolset="ooda", schema=schemas.OODA_PROMPT, handler=tools.ooda_prompt)
    ctx.register_tool(name="ooda_record", toolset="ooda", schema=schemas.OODA_RECORD, handler=tools.ooda_record)
    ctx.register_tool(name="ooda_status", toolset="ooda", schema=schemas.OODA_STATUS, handler=tools.ooda_status)
    ctx.register_tool(name="ooda_move", toolset="ooda", schema=schemas.OODA_MOVE, handler=tools.ooda_move)
    ctx.register_tool(name="ooda_list", toolset="ooda", schema=schemas.OODA_LIST, handler=tools.ooda_list)

    # slash commands
    ctx.register_command("ooda", handler=_handle_ooda, description="OODA loop: status, list, close, or start on a situation")
    for cmd, key in COMMANDS.items():
        if key is None:
            continue
        ctx.register_command(
            cmd,
            handler=_make_stage_handler(key),
            description=f"Run Boyd's {prompts.get(key)['title']}",
        )

    # CLI
    ctx.register_cli_command(
        name="ooda",
        help="Manage OODA loops",
        setup_fn=_cli_setup,
        handler_fn=_cli,
    )

    # hook
    ctx.register_hook("pre_llm_call", _inject_active_loop)
