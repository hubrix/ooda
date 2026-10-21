# ooda

John Boyd's OODA loop as a portable agent plugin.

Works in **Hermes**, **Claude Code**, and **Codex CLI** — same skills, same
tools, same prompts. One source of truth, three harnesses.

Boyd was a US fighter pilot — "40-Second Boyd" — who helped shape the F-15 and
F-16 and left behind one framework: **Observe. Orient. Decide. Act.** Almost
nobody uses it the way he meant. The popular reading is "be faster." Boyd's
actual point is that every arrow runs through **Orient**: you lose because you
are oriented to a world that stopped existing, not because you decided slowly.

## Install

### Hermes

```bash
hermes plugins install hubrix/ooda
hermes plugins enable ooda
```

### Claude Code + Codex CLI

```bash
git clone git@github.com:hubrix/ooda.git ~/code/ooda
~/code/ooda/scripts/install-agents.sh          # both
~/code/ooda/scripts/install-agents.sh --claude # Claude Code only
~/code/ooda/scripts/install-agents.sh --codex  # Codex only
```

Installs skills, slash commands / custom prompts, and the MCP server into
`~/.claude/` and `~/.codex/`, all symlinked back to the checkout so `git pull`
updates every agent at once. `--uninstall` reverses it.

### Any other MCP client

```bash
python3 mcp/ooda_mcp.py     # stdio, zero dependencies
```

## Use

```
/ooda a competitor just cut prices 20%      # opens a loop
/ooda-observe                               # run the Observe stage
/ooda-orient                                # ...then Orient, Decide, Act
```

Or let the model drive it — `ooda_start` opens a loop, `ooda_record` persists
each stage's findings, `ooda_move` records THE MOVE and closes it.

## What it ships

| Layer | Contents |
|---|---|
| Skills | `ooda-loop` hub + 9 stage skills (`observe-audit`, `orient-audit`, `destruction-creation`, `mismatch-detector`, `tempo`, `main-effort`, `interaction-isolation`, `to-be-or-to-do`, `full-boyd-loop`) |
| MCP tools | `ooda_start`, `ooda_prompt`, `ooda_record`, `ooda_status`, `ooda_move`, `ooda_list` |
| Slash commands | `/ooda`, `/ooda-observe`, `/ooda-orient`, `/ooda-destroy`, `/ooda-mismatch`, `/ooda-tempo`, `/ooda-effort`, `/ooda-isolate`, `/ooda-tobetodo`, `/ooda-full` |
| Hermes extras | CLI (`hermes ooda`), `pre_llm_call` context hook, desktop pane, dashboard routes |

## Layout

```
plugin.yaml            Hermes manifest
__init__.py            Hermes registration (skills, tools, commands, hook)
prompts.py             the nine prompts — single source of truth
store.py               loop state (SQLite; Hermes data dir, else ~/.ooda)
schemas.py             tool schemas
tools.py               tool handlers
mcp/ooda_mcp.py        stdio MCP server (stdlib only) — Claude Code, Codex, any client
agents/claude/         Claude Code slash commands
agents/codex/          Codex custom prompts
scripts/build_skills.py    regenerates skills/ + agents/ from prompts.py
scripts/install-agents.sh  wires the plugin into Claude Code and Codex
skills/                generated bundled skills
dashboard/             Hermes FastAPI backend routes
desktop/plugin.js      Hermes desktop pane + commands
tests/                 pytest suite
```

Edit `prompts.py`, then run `python scripts/build_skills.py` to regenerate
skills and agent commands so nothing drifts.

## Source

Thread: https://x.com/heynavtoor/status/2112546579328733660
Framework: John Boyd (1927–1997) — *Destruction and Creation* (1976),
*Strategic Game of ? and ?*, the Energy-Maneuverability diagrams.
