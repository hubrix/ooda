#!/usr/bin/env python3
"""
build_skills.py — generate skills/<key>/SKILL.md from prompts.py.

prompts.py is the single source of truth; run this after editing it so the
bundled skills never drift from the tool output.
"""

from __future__ import annotations

import sys
from pathlib import Path

PLUGIN_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PLUGIN_DIR.parent))

from ooda import prompts  # noqa: E402

SKILLS = PLUGIN_DIR / "skills"

SLASH = {
    "observe-audit": "observe",
    "orient-audit": "orient",
    "destruction-creation": "destroy",
    "mismatch-detector": "mismatch",
    "tempo": "tempo",
    "main-effort": "effort",
    "interaction-isolation": "isolate",
    "to-be-or-to-do": "tobetodo",
    "full-boyd-loop": "full",
}

HUB = """---
name: ooda-loop
description: "Use when a decision, competitor, market, or stalled plan needs John Boyd's OODA loop. Runs Observe/Orient/Decide/Act with orientation at the center."
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, strategy, decision-making]
    category: productivity
---

# The OODA Loop (John Boyd)

Boyd was a US fighter pilot — "40-Second Boyd" — who helped shape the F-15 and
F-16 and left behind one framework: Observe, Orient, Decide, Act. Almost nobody
uses it the way he meant. The popular reading is "be faster." Boyd's actual
point is that **every arrow runs through Orient**: you lose because you are
oriented to a world that stopped existing, not because you decided slowly.

## When to use

- A decision, competitor, market, negotiation, or stalled plan needs structure.
- The user says "run OODA on this", "Boyd this", or asks for a strategic read.
- You want to persist a loop across turns instead of answering once.

## The loop

1. **Observe** — raw facts only, plus what you are *not* observing.
2. **Orient** — the lens: assumptions, history, culture, and where they mismatch reality.
3. **Decide** — tempo, main effort, interaction/isolation, to-be-or-to-do.
4. **Act** — the single move, the action that resets the loop, the observation that scores it.

## How to run it

```
ooda_start(situation="…", arena="…")     # opens a loop, returns the Observe prompt
ooda_prompt(key="orient-audit")          # any of the nine prompts, verbatim
ooda_record(loop_id, stage, content)     # persist findings, advances the stage
ooda_status()                            # current loop + entries
ooda_move(loop_id, decision, action, observation)   # THE MOVE, closes the loop
```

Slash commands: `/ooda <situation>` opens a loop; `/ooda-observe`,
`/ooda-orient`, `/ooda-destroy`, `/ooda-mismatch`, `/ooda-tempo`,
`/ooda-effort`, `/ooda-isolate`, `/ooda-tobetodo`, `/ooda-full` run a stage.
`/ooda status`, `/ooda list`, `/ooda close <id>` manage loops.

## The nine prompts

| Skill | Stage | Use when |
|---|---|---|
| `ooda:observe-audit` | Observe | You need raw facts and blind spots |
| `ooda:orient-audit` | Orient | Your read of the world may be stale |
| `ooda:destruction-creation` | Orient | The approach keeps failing the same way |
| `ooda:mismatch-detector` | Orient | Competitive gap analysis, both directions |
| `ooda:tempo` | Decide | The loop itself is slow |
| `ooda:main-effort` | Decide | Too many priorities |
| `ooda:interaction-isolation` | Decide | Position against an opponent |
| `ooda:to-be-or-to-do` | Decide | Career / life fork |
| `ooda:full-boyd-loop` | Act | Run the whole system at once |

## Rules

- **Orientation is the center.** Never skip it; every other stage feeds it.
- **Mismatches over speed.** Find the gap between expectation and reality first.
- **Raw facts before interpretation.** Flag any judgment line and rewrite it as a fact.
- **One move.** Converge on a single decision, not a menu.
- **Persist.** Record findings as you go; a loop that lives only in the reply is lost.
"""


def main() -> None:
    SKILLS.mkdir(parents=True, exist_ok=True)
    (SKILLS / "ooda-loop").mkdir(exist_ok=True)
    (SKILLS / "ooda-loop" / "SKILL.md").write_text(HUB, encoding="utf-8")

    for key in prompts.ORDER:
        rec = prompts.PROMPTS[key]
        why = rec["why"].replace('"', "'")
        why = why[:110].rsplit(" ", 1)[0]
        body = f"""---
name: {key}
description: "Use when running Boyd's {rec['title']} ({rec['stage']} stage). {why}"
version: 1.0.0
metadata:
  hermes:
    tags: [ooda, boyd, {rec['stage']}]
    category: productivity
---

# {rec['title']}

**Stage:** {rec['stage']}

{rec['why']}

## Prompt

```
{rec['prompt']}
```

## How to run it

- `ooda_prompt(key="{key}", situation="…")` returns this verbatim.
- Or the matching slash command: `/ooda-{SLASH[key]}` if a loop is open.
- Record the output with `ooda_record(loop_id, "{rec['stage']}", …)` before moving on.
"""
        d = SKILLS / key
        d.mkdir(exist_ok=True)
        (d / "SKILL.md").write_text(body, encoding="utf-8")

    print(f"wrote {len(prompts.ORDER) + 1} skills to {SKILLS}")

    build_agent_commands()


CLAUDE_CMDS = PLUGIN_DIR / "agents" / "claude" / "commands"
CODEX_PROMPTS = PLUGIN_DIR / "agents" / "codex" / "prompts"

HUB_CMD = """---
description: OODA loop — status, list, close, or start a loop on a situation
argument-hint: [situation | status | list | close <id>]
---

Use the `ooda` MCP tools.

- No argument or `status`: call `ooda_status` and report the active loop.
- `list`: call `ooda_list`.
- `close <id>`: call `ooda_move` if you have a decision, else report the loop.
- Anything else: treat it as a situation, call `ooda_start`, then run the
  Observe prompt it returns.

$ARGUMENTS
"""


def build_agent_commands() -> None:
    """Emit Claude Code slash commands and Codex custom prompts."""
    CLAUDE_CMDS.mkdir(parents=True, exist_ok=True)
    CODEX_PROMPTS.mkdir(parents=True, exist_ok=True)

    (CLAUDE_CMDS / "ooda.md").write_text(HUB_CMD, encoding="utf-8")
    (CODEX_PROMPTS / "ooda.md").write_text(HUB_CMD, encoding="utf-8")

    for key in prompts.ORDER:
        rec = prompts.PROMPTS[key]
        slash = SLASH[key]
        why = rec["why"].replace('"', "'")
        why = why[:110].rsplit(" ", 1)[0]

        claude = f"""---
description: Boyd's {rec['title']} ({rec['stage']} stage)
argument-hint: [situation]
---

Call `ooda_prompt` with key="{key}" and situation="$ARGUMENTS" (or the active
loop's situation if no argument). Then run the returned prompt in full.

Record the findings with `ooda_record` at stage "{rec['stage']}" before moving on.
"""
        (CLAUDE_CMDS / f"ooda-{slash}.md").write_text(claude, encoding="utf-8")

        codex = f"""# Boyd's {rec['title']} ({rec['stage']} stage)

{why}

Call `ooda_prompt` with key="{key}" and situation="$ARGUMENTS" (or the active
loop's situation if no argument). Then run the returned prompt in full.

Record the findings with `ooda_record` at stage "{rec['stage']}" before moving on.
"""
        (CODEX_PROMPTS / f"ooda-{slash}.md").write_text(codex, encoding="utf-8")

    print(f"wrote {len(prompts.ORDER) + 1} commands to {CLAUDE_CMDS} and {CODEX_PROMPTS}")


if __name__ == "__main__":
    main()
