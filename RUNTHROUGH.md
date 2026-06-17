# Participant run-through — exact steps (shape-first version)

The course webpage is the entry point and tells you every step.
This file covers only the prep block and the local substitutions.

## Prep (once)

```bash
cd ~/dev/genai-workshop-lakehouse && source .venv/bin/activate
neo4j-cli query --uri neo4j://localhost:7690 --username neo4j --password workshop123 "MATCH (n) DETACH DELETE n" --rw
neo4j-cli query --uri neo4j://localhost:7690 --username neo4j --password workshop123 "DROP INDEX content_search IF EXISTS" --rw
```

## START HERE

**http://localhost:3000/courses/workshop-lakehouse/** — enroll, open Module 1,
follow every page in order. (Flip `:status:` to `active` in course.adoc
locally if it shows "Coming Soon" — don't commit.)

## Local substitutions

1. **Codespace button** → until the env repo push lands, your Codespace is
   this folder: `~/dev/genai-workshop-lakehouse` with the venv active.
   (After the push, the button works for real — delete + recreate to test it.)
2. **Credentials block in "Your Environment"** → the page renders working
   local-sandbox credentials; paste them into `.env` exactly as shown.
   If running a real cloud Codespace instead, use a sandbox.neo4j.com
   **Graph Data Science blank sandbox** (cloud-reachable, has GDS).

## What the flow looks like now (so nothing surprises you)

- **Module 1 (Setup):** wire BigQuery (read) + Neo4j in `.env`; `python load/load_graph.py`
  loads **documents only** (warehouse rows stay in BigQuery). Start the API:
  `uvicorn api.parts_api:app --port 8800`. Smoke test in `claude`.
- **Module 2 (Connections):** `python connections/build_connections.py` runs
  neocarta over BigQuery -> the metadata graph + the `connections` MCP. Approve the
  MCP in your agent, then ask it a warehouse question and watch it retrieve schema
  and write Text2SQL (executed with `python skill/scripts/run_sql.py`).
- **Module 3 (Trees):** read `docs/outline-format.md`; fill the blocks in
  `skill/scripts/outline.py` and `search.py`. Test `python skill/scripts/outline.py`.
- **Module 4 (Themes):** read `docs/theme-format.md`; fill `skill/scripts/themes.py`;
  run it, then `--gamma 2.0` for the dial. Optional: the neo4j-cli lesson.
- **Module 5 (Finale):** build the four judgment/action tools from the specs in
  `skill/SKILL.md` - the two judgment tools **federate** (Neo4j grounding +
  BigQuery SQL via `bq.py`). Then: `Work order event: events/wo-2026-0117.json.
  Handle it per the skill.` Second event (`wo-2026-0118.json`) must escalate.
- Check Database buttons verify your local sandbox throughout.

## If a lesson page 404s
The local app caches its route map - `cd ~/dev/courses && docker compose restart app`, wait ~30s, refresh.

## If stuck

`solutions/scripts/` has every completed tool. Themes need GDS - your local
sandbox has it. A crashed themes run leaves no debris (the script drops its
projection).
