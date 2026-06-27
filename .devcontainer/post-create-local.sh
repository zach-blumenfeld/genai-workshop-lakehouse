#!/usr/bin/env bash
# Local (laptop) setup for the AI on Your Lakehouse workshop.
# Mirrors .devcontainer/post-create.sh but with an isolated venv and a
# repo-relative .env path. Each step is independent - one failure must not
# block the others.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "--- Python dependencies (isolated venv)"
[ -d "$REPO_ROOT/.venv" ] || python3 -m venv "$REPO_ROOT/.venv"
"$REPO_ROOT/.venv/bin/pip" install -r "$REPO_ROOT/requirements.txt" || echo "WARN: pip install failed - run it manually"

#echo "--- Claude Code"
#npm install -g @anthropic-ai/claude-code || echo "WARN: claude install failed - run: npm install -g @anthropic-ai/claude-code"
#mkdir -p "$HOME/.claude"

echo "--- Neo4j CLI + agent skills"
if curl -sSfL https://neo4j.sh/install.sh -o /tmp/n4jcli-install.sh && NEO4J_CLI_AUTO_INSTALL_SKILL=0 bash /tmp/n4jcli-install.sh < /dev/null; then
  export PATH="$HOME/.local/bin:$PATH"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  # Self-skill (the neo4j-cli skill itself) ...
  neo4j-cli skill install --agent claude-code --rw \
    || echo "WARN: skill install failed - run: neo4j-cli skill install --agent claude-code --rw"
  # ... plus the catalog skills the workshop leans on: neo4j-cypher-skill (write
  # Cypher from a spec, Modules 3-5) and neo4j-gds-skill (Leiden, Module 4).
  for s in neo4j-cypher-skill neo4j-gds-skill; do
    neo4j-cli skill install "$s" --agent claude-code --rw \
      || echo "WARN: $s install failed - run: neo4j-cli skill install $s --agent claude-code --rw"
  done
else
  echo "WARN: neo4j-cli install failed - run: curl -sSfL https://neo4j.sh/install.sh | bash"
fi

echo "--- Environment file"
[ -f .env ] || cp .env.example .env
# Export .env into every shell so neo4j-cli, scripts, and Claude Code all see it
LINE="set -a; [ -f $REPO_ROOT/.env ] && . $REPO_ROOT/.env; set +a"
grep -qF "$LINE" "$HOME/.bashrc" || echo "$LINE" >> "$HOME/.bashrc"

echo ""
echo "Setup check:"
command -v neo4j-cli >/dev/null && echo "  neo4j-cli:    OK" || echo "  neo4j-cli:    MISSING"
command -v claude >/dev/null && echo "  claude:       OK" || echo "  claude:       MISSING"
for s in neo4j-cli neo4j-cypher-skill neo4j-gds-skill; do
  [ -d "$HOME/.claude/skills/$s" ] && echo "  $s: OK" || echo "  $s: MISSING"
done
echo ""
echo "Next steps (from the workshop lesson):"
echo "  1. Paste your Neo4j sandbox credentials into .env (BigQuery is pre-wired)"
echo "  2. python load/build_connections.py   (Module 2: connections from BigQuery)"
echo "  3. python load/load_documents.py                 (Module 3: documents)"
echo "  4. claude                                    (second terminal)"
