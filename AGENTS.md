# ooda — agent context

This repo is a portable agent plugin implementing John Boyd's OODA loop.

## For any agent working in this repo

- `prompts.py` is the single source of truth for the nine Boyd prompts.
  After editing it, run `python scripts/build_skills.py` — that regenerates
  `skills/`, `agents/claude/commands/`, and `agents/codex/prompts/`.
- Never hand-edit generated files under `skills/` or `agents/`.
- `store.py` must keep working with no Hermes present (the MCP server runs
  standalone) — it falls back to `~/.ooda/` when `plugins.plugin_storage`
  is unavailable.
- `mcp/ooda_mcp.py` is stdlib-only on purpose. Do not add dependencies.
- Run `python -m pytest tests/` before committing.

## The framework

Observe → Orient → Decide → Act. Orientation is the center: every arrow runs
through it. Mismatches over speed. Raw facts before interpretation. One move.

## Tools (MCP server `ooda`)

`ooda_start`, `ooda_prompt`, `ooda_record`, `ooda_status`, `ooda_move`,
`ooda_list`. Run the server with `python3 mcp/ooda_mcp.py`.
