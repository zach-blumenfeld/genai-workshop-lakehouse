#!/usr/bin/env bash
# Codespace setup for the AI on Your Lakehouse workshop.
set -e

pip install -r requirements.txt

# The agentic Neo4j CLI + the agent skills that teach coding agents to use it
curl -sSfL https://neo4j.sh/install.sh | bash
export PATH="$HOME/.local/bin:$PATH"
neo4j-cli skill install || true

# Claude Code - the coding agent used in the workshop (any skills-capable agent works)
npm install -g @anthropic-ai/claude-code

# Connection template - the workshop lesson provides the values
[ -f .env ] || cp .env.example .env

echo ""
echo "Setup complete. Next steps (from the workshop lesson):"
echo "  1. Paste your sandbox credentials into .env"
echo "  2. python load/load_graph.py"
echo "  3. uvicorn api.parts_api:app --port 8800   (second terminal)"
echo "  4. claude   (and let the skill in skill/ do the talking)"
