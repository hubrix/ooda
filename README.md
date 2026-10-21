# ooda

John Boyd's OODA loop as a working Hermes plugin.

Boyd was a US fighter pilot — "40-Second Boyd" — who helped shape the F-15 and
F-16 and left behind one framework: **Observe. Orient. Decide. Act.** Almost
nobody uses it the way he meant. The popular reading is "be faster." Boyd's
actual point is that every arrow runs through **Orient**: you lose because you
are oriented to a world that stopped existing, not because you decided slowly.

This plugin turns @heynavtoor's nine Boyd prompts into a system: bundled skills,
persistent loop state, slash commands, a context hook, and a desktop pane.

## What it ships

| Layer | Contents |
|---|---|
| Skills | `ooda:ooda-loop` hub + 9 stage skills (`ooda:observe-audit`, `ooda:orient-audit`, `ooda:destruction-creation`, `ooda:mismatch-detector`, `ooda:tempo`, `ooda:main-effort`, `ooda:interaction-isolation`, `ooda:to-be-or-to-do`, `ooda:full-boyd-loop`) |
| Tools | `ooda_start`, `ooda_prompt`, `ooda_record`, `ooda_status`, `ooda_move`, `ooda_list` |
| Slash commands | `/ooda`, `/ooda-observe`, `/ooda-orient`, `/ooda-destroy`, `/ooda-mismatch`, `/ooda-tempo`, `/ooda-effort`, `/ooda-isolate`, `/ooda-tobetodo`, `/ooda-full` |
| CLI | `hermes ooda list\|show\|prompt` |
| Hook | `pre_llm_call` — injects the active loop's situation + latest orientation into each turn |
| Desktop | Pane (stage rail, prompt list, click-to-insert), status chip, two ⌘K commands |
| Dashboard | FastAPI routes at `/api/plugins/ooda/` |

## Install

From this repo:

```bash
hermes plugins install hubrix/ooda
hermes plugins enable ooda
```

Or link a checkout for development:

```bash
ln -s ~/code/ooda ~/.hermes/plugins/ooda
```

The desktop half is opt-in: flip it on in Capabilities → Plugins, then ⌘K →
Rescan so the pane lands.

## Use

```
/ooda a competitor just cut prices 20%      # opens a loop
/ooda-observe                               # run the Observe stage
/ooda-orient                                # ...then Orient, Decide, Act
```

Or let the model drive it — `ooda_start` opens a loop, `ooda_record` persists
each stage's findings, `ooda_move` records THE MOVE and closes it.

## Layout

```
plugin.yaml            manifest
__init__.py            registration (skills, tools, commands, hook)
prompts.py             the nine prompts — single source of truth
store.py               loop state (SQLite under plugin-data/)
schemas.py             tool schemas
tools.py               tool handlers
scripts/build_skills.py  regenerates skills/ from prompts.py
skills/                generated bundled skills
dashboard/             FastAPI backend routes
desktop/plugin.js      desktop pane + commands
tests/                 pytest suite
```

Edit `prompts.py`, then run `python scripts/build_skills.py` to regenerate the
skills so they never drift from the tool output.

## Source

Thread: https://x.com/heynavtoor/status/2112546579328733660
Framework: John Boyd (1927–1997) — *Destruction and Creation* (1976),
*Strategic Game of ? and ?*, the Energy-Maneuverability diagrams.
