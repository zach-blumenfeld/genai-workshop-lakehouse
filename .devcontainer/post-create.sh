#!/usr/bin/env bash
# Codespace setup for the AI on Your Lakehouse workshop.
# Each step is independent - one failure must not block the others.

echo "--- Python dependencies"
pip install -r requirements.txt || echo "WARN: pip install failed - run it manually"

echo "--- Claude Code"
npm install -g @anthropic-ai/claude-code || echo "WARN: claude install failed - run: npm install -g @anthropic-ai/claude-code"
mkdir -p "$HOME/.claude"

echo "--- Neo4j CLI + agent skills"
if curl -sSfL https://neo4j.sh/install.sh | NEO4J_CLI_AUTO_INSTALL_SKILL=0 bash < /dev/null; then
  export PATH="$HOME/.local/bin:$PATH"
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  neo4j-cli skill install --agent claude-code --rw \
    || echo "WARN: skill install failed - run: neo4j-cli skill install --agent claude-code --rw"
else
  echo "WARN: neo4j-cli install failed - run: curl -sSfL https://neo4j.sh/install.sh | bash"
fi

echo "--- Environment file"
[ -f .env ] || cp .env.example .env
# Export .env into every shell so neo4j-cli, scripts, and Claude Code all see it
LINE='set -a; [ -f /workspaces/genai-workshop-lakehouse/.env ] && . /workspaces/genai-workshop-lakehouse/.env; set +a'
grep -qF "$LINE" "$HOME/.bashrc" || echo "$LINE" >> "$HOME/.bashrc"

echo ""
echo "Setup check:"
command -v neo4j-cli >/dev/null && echo "  neo4j-cli:    OK" || echo "  neo4j-cli:    MISSING"
command -v claude >/dev/null && echo "  claude:       OK" || echo "  claude:       MISSING"
[ -d "$HOME/.claude/skills/neo4j-cli" ] && echo "  neo4j skills: OK" || echo "  neo4j skills: MISSING"
echo ""
echo "Next steps (from the workshop lesson):"
echo "  1. Paste your sandbox credentials into .env"
echo "  2. python load/load_graph.py"
echo "  3. uvicorn api.parts_api:app --port 8800   (second terminal)"
echo "  4. claude   (third terminal)"
