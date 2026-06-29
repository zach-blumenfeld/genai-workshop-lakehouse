# CLAUDE.md

Guidance for Claude Code (and any coding agent) working in this repo.

## What this is

The companion environment for the GraphAcademy workshop **AI on Your Lakehouse:
Context Comes in Shapes, Not Queries**. You build a **service-advisor skill** that
answers questions over the AutoFix lakehouse — a document library (PDF manuals,
service bulletins, recall notices) and a warehouse (vehicles, work orders, parts) —
by giving the agent three reusable graph **shapes**.

## Architecture

- **Documents** (`corpus/` → rendered to `sources/pdfs/`) are parsed into a Neo4j
  **document graph**: a containment tree (table of contents) plus Leiden **themes**
  (communities over the documents' cross-references).
- **Warehouse** rows live in **BigQuery** and are never migrated. **neocarta** reads
  the warehouse's metadata (the foreign-key join paths) into a Neo4j **connections**
  graph; the agent writes Text2SQL grounded by those join paths and runs it live.
- The agent **federates**: ground a question in the document graph, then read the
  warehouse facts with SQL, joining on the identifiers both halves share (part
  numbers, trouble codes).

## The skill you build

`skill/SKILL.md` is the playbook; `skill/scripts/` are its tools:

- `outline.py` — the library as a navigable table of contents (the tree shape)
- `search.py` — full-text search over sections
- `themes.py` — Leiden community detection over document cross-references
- `run_sql.py` — run BigQuery SQL for warehouse facts, grounded by the `connections` MCP

## Common commands

```bash
python load/build_connections.py    # neocarta: warehouse metadata -> connections graph
python load/load_documents.py       # parse PDFs -> document graph (trees + themes)
python skill/scripts/outline.py
python skill/scripts/search.py "<query>"
python skill/scripts/themes.py
python skill/scripts/run_sql.py "<SQL>"
```

## Answer from the graph, not the source files

When acting as the workshop agent, ground every answer in the graph and the
warehouse — do **not** read `corpus/`, `sources/`, `solutions/`, or `databricks/`
to shortcut to an answer. The point is to reach the answer through the shapes. See
`skill/SKILL.md` for the full policy.
