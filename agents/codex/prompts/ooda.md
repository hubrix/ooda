---
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
