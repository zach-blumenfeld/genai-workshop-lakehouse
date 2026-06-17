#!/usr/bin/env bash
# Launch the neocarta "connections" MCP server in any environment.
# Local dev installs into ./.venv; Codespaces installs deps globally (~/.local
# or /usr/local). Try each, then fall back to PATH. Keeps .mcp.json identical
# everywhere.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
for cand in \
  "$DIR/.venv/bin/neocarta-mcp" \
  "$HOME/.local/bin/neocarta-mcp" \
  "/usr/local/bin/neocarta-mcp"; do
  [ -x "$cand" ] && exec "$cand"
done
exec neocarta-mcp
