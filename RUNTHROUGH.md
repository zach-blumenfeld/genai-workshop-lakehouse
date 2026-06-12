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

- **Module 1:** `python load/load_graph.py` parses the PDFs into the
  Library tree (folders, citations, fulltext index) and merges the
  warehouse. Start the API: `uvicorn api.parts_api:app --port 8800`.
  Smoke test in `claude`.
- **Module 2 (shape-first):** read `docs/outline-format.md` FIRST — it is
  the spec. Then fill the `BUILD FROM SPEC` blocks in
  `skill/scripts/outline.py` and `search.py` with Claude. Test:
  `python skill/scripts/outline.py` and
  `python skill/scripts/search.py 'misfire OR "rough idle"'`.
- **Module 3:** read `docs/theme-format.md`, build the projection block in
  `skill/scripts/themes.py`, run it, then `--gamma 2.0` for the dial moment.
- **Module 4:** build the four judgment/action tools from the specs in
  `skill/SKILL.md`, then: `Work order event: events/wo-2026-0117.json.
  Handle it per the skill.` Grounding now uses **section URIs** (copy from
  outline output). Second event must escalate.
- Check Database buttons verify your local sandbox throughout.

## If a lesson page 404s
The local app caches its route map - `cd ~/dev/courses && docker compose restart app`, wait ~30s, refresh.

## If stuck

`solutions/scripts/` has every completed tool. Themes need GDS - your local
sandbox has it. A crashed themes run leaves no debris (the script drops its
projection).
