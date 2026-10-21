#!/usr/bin/env bash
#
# install-agents.sh — wire the ooda plugin into Claude Code and Codex CLI.
#
# Installs: skills (Agent Skills format), slash commands / custom prompts, and
# the stdio MCP server. Everything is symlinked back to this checkout, so
# `git pull` updates all three agents at once.
#
#   ./scripts/install-agents.sh              # both agents
#   ./scripts/install-agents.sh --claude     # Claude Code only
#   ./scripts/install-agents.sh --codex      # Codex only
#   ./scripts/install-agents.sh --uninstall  # remove
#
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PYTHON:-python3}"
MCP="$ROOT/mcp/ooda_mcp.py"

DO_CLAUDE=0
DO_CODEX=0
UNINSTALL=0

for arg in "$@"; do
  case "$arg" in
    --claude) DO_CLAUDE=1 ;;
    --codex) DO_CODEX=1 ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "unknown flag: $arg" >&2; exit 2 ;;
  esac
done

if [ "$DO_CLAUDE" -eq 0 ] && [ "$DO_CODEX" -eq 0 ]; then
  DO_CLAUDE=1
  DO_CODEX=1
fi

link() { ln -sfn "$1" "$2"; }

# --------------------------------------------------------------------------- #
# Claude Code
# --------------------------------------------------------------------------- #
claude_install() {
  mkdir -p "$HOME/.claude/skills" "$HOME/.claude/commands"
  for d in "$ROOT"/skills/*/; do
    link "$d" "$HOME/.claude/skills/ooda-$(basename "$d")"
  done
  for f in "$ROOT"/agents/claude/commands/*.md; do
    link "$f" "$HOME/.claude/commands/$(basename "$f")"
  done
  if command -v claude >/dev/null 2>&1; then
    claude mcp remove -s user ooda >/dev/null 2>&1 || true
    claude mcp add -s user ooda -- "$PY" "$MCP"
  else
    echo "  ! claude not on PATH — add the MCP server manually:"
    echo "    claude mcp add -s user ooda -- $PY $MCP"
  fi
  echo "  ✓ Claude Code: skills, commands, MCP server"
}

claude_uninstall() {
  rm -f "$HOME"/.claude/skills/ooda-* 2>/dev/null || true
  rm -f "$HOME"/.claude/commands/ooda*.md 2>/dev/null || true
  command -v claude >/dev/null 2>&1 && claude mcp remove -s user ooda >/dev/null 2>&1 || true
  echo "  ✓ Claude Code: removed"
}

# --------------------------------------------------------------------------- #
# Codex CLI
# --------------------------------------------------------------------------- #
CODEX_CFG="$HOME/.codex/config.toml"

codex_install() {
  mkdir -p "$HOME/.codex/skills" "$HOME/.codex/prompts"
  for d in "$ROOT"/skills/*/; do
    link "$d" "$HOME/.codex/skills/ooda-$(basename "$d")"
  done
  for f in "$ROOT"/agents/codex/prompts/*.md; do
    link "$f" "$HOME/.codex/prompts/$(basename "$f")"
  done

  touch "$CODEX_CFG"
  "$PY" - "$CODEX_CFG" "$PY" "$MCP" <<'PYEOF'
import re, sys
cfg, py, mcp = sys.argv[1], sys.argv[2], sys.argv[3]
text = open(cfg).read()
text = re.sub(r"\n?# >>> ooda >>>.*?# <<< ooda <<<\n?", "\n", text, flags=re.S)
block = (
    "\n# >>> ooda >>>\n"
    "[mcp_servers.ooda]\n"
    f'command = "{py}"\n'
    f'args = ["{mcp}"]\n'
    "# <<< ooda <<<\n"
)
open(cfg, "w").write(text.rstrip("\n") + "\n" + block)
PYEOF
  echo "  ✓ Codex: skills, prompts, MCP server in $CODEX_CFG"
}

codex_uninstall() {
  rm -f "$HOME"/.codex/skills/ooda-* 2>/dev/null || true
  rm -f "$HOME"/.codex/prompts/ooda*.md 2>/dev/null || true
  if [ -f "$CODEX_CFG" ]; then
    "$PY" - "$CODEX_CFG" <<'PYEOF'
import re, sys
cfg = sys.argv[1]
text = open(cfg).read()
text = re.sub(r"\n?# >>> ooda >>>.*?# <<< ooda <<<\n?", "\n", text, flags=re.S)
open(cfg, "w").write(text)
PYEOF
  fi
  echo "  ✓ Codex: removed"
}

# --------------------------------------------------------------------------- #
echo "ooda → agents  (root: $ROOT)"
if [ "$UNINSTALL" -eq 1 ]; then
  [ "$DO_CLAUDE" -eq 1 ] && claude_uninstall
  [ "$DO_CODEX" -eq 1 ] && codex_uninstall
  echo "done."
  exit 0
fi

[ "$DO_CLAUDE" -eq 1 ] && claude_install
[ "$DO_CODEX" -eq 1 ] && codex_install

echo
echo "Restart the agent(s) to pick up the MCP server."
echo "Try: /ooda a competitor just cut prices 20%"
