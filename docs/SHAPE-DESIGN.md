# Shape-first design — AutoFix technical library on the lakehouse

The workshop's thesis applied to its own build: **start from the shape the
agent's context needs, spec it, then derive the graph reasoning, and only
then write the query logic.** Modeled on knowledge-index (ki); adapted from
local markdown vaults to PDFs in cloud buckets.

## Data model

Containment is one relationship type, `HAS`, exactly as in ki — every child
has one incoming `HAS`; tree walks are `[:HAS*]`.

```
(:Library {uri, name, displayName})                       // bucket root: technical-library
  -[:HAS]-> (:Folder {uri, name, displayName})            // gcs prefixes: manuals/ bulletins/ recalls/
    -[:HAS]-> (:Document {uri, id, name, displayName,     // one PDF; id = printed doc code (TSB-21-114)
                          docType, model, published}      //   + secondary label :Manual|:Bulletin|:RecallNotice
      -[:HAS]-> (:Section {uri, name, displayName,
                           headingLevel, content})        // content = Rule 1: own body + `uri:` child pointers
        -[:HAS]-> (:Section ...)                          // nested headings

(:Section)-[:NEXT_SECTION]->(:Section)                    // DFS reading order per document
(:Section)-[:REFERENCES_PART]->(:Part {partNumber})       // extracted against the parts catalog
(:Section)-[:REFERENCES_CODE]->(:DTC {code})              // OBD-II regex
(:Section)-[:LINKS_TO {citation:true}]->(:Document)       // explicit: "per recall RC-2021-04"
(:Section)-[:LINKS_TO {derived:true,                      // derived: sections in different docs
            sharedKeys, strength}]->(:Section)            //   sharing a part or code
```

URIs are hierarchical and slugified, so prefix matching scopes any subtree:

```
technical-library
technical-library/bulletins
technical-library/bulletins/tsb-21-114.pdf
technical-library/bulletins/tsb-21-114.pdf#condition
technical-library/manuals/man-fal-3.pdf#engine/ignition-coil-replacement
```

Section URI fragments are the **full heading path** (ki rule), with `-1`/`-2`
disambiguation for duplicate headings under one parent. `Document.id` keeps
the printed document code (`TSB-21-114`) because the warehouse and the
judgment tools key on it; `uri` is the containment identity.

The warehouse half (Vehicle / WorkOrder / Part / Procedure / DTC) is
unchanged — it still merges onto Part/DTC by shared key.

## The three shapes (spec → reasoning → query)

### 1. Outline (ToC) — `skill/scripts/outline.py`

- **Spec:** `docs/outline-format.md` — dotted-leader rows, type letters,
  full URIs always, `→` rows for outbound links, NEXT_SECTION sibling order.
- **Reasoning:** one variable-length `HAS` walk from any root URI emits flat
  wire rows (depth, label, names, uri, parent_uri, sort_pos); a second query
  fetches outbound LINKS_TO for the visible Document/Section rows; the
  renderer (Python — assembling a tree is application logic, not query
  logic) groups by parent, sorts per sibling-kind, DFS-emits.
- **Why Python stays:** sibling-sort rules differ per group and the
  LINKS_TO rows are synthesized client-side at parent-depth+1 — exactly as
  in ki's `outline.py`.

### 2. Search — `skill/scripts/search.py` + index

```cypher
CREATE FULLTEXT INDEX content_search IF NOT EXISTS
FOR (n:Document|Section) ON EACH [n.displayName, n.content, n.uri]
```

- **Spec:** ranked rows of (score, label, uri, displayName, content head).
- **Reasoning:** hierarchical hybrid — a hard `+uri:<escaped-prefix>*` MUST
  clause (structural, ours) AND'd with the user's free-text query passed
  through verbatim per field (their operators preserved). Works because
  URIs sort hierarchically.
- **Semantic expansion lives in the skill, not the index:** lexical search
  misses synonyms ("rough idle" vs "misfire"), so SKILL.md instructs the
  agent to rewrite thin queries with OR-alternates it knows
  (`misfire OR "rough idle" OR P0301`) — ki's pattern verbatim.

### 3. Themes — `skill/scripts/themes.py`

- **Spec:** `docs/theme-format.md` — header that reconciles
  (`N docs · G grouped into K themes by shared parts and codes · U ungrouped`),
  one block per theme: cohesion word, top shared targets
  (`[IC-2042-A] in 4 docs`), most-linked docs as outline rows,
  `links into T<j> via` crossover rows. ki rule kept: **the tool never
  names a theme** — it ships the evidence; the agent names it.
- **Reasoning (ki's glue-node insight, mapped):** Part and DTC nodes are
  the glue — two documents that both reference `IC-2042-A` should cluster
  even if neither cites the other (co-citation). Project a doc-level
  graph: collapse section-level REFERENCES and LINKS_TO to owning
  documents (`split(uri,'#')[0]`), docs + glue nodes, undirected,
  weight = mention count. Leiden **mutate** → per-community conductance
  (cohesion word) → write `themeId` to Documents → renderer queries →
  drop projection. Pure driver + Cypher `CALL gds.*` — no extra client
  dependency.
- `themeId` lives on `Document` (doc-level themes), is producer-owned,
  regenerated per run; theme numbers are stable only within a run —
  store URIs, never `T<id>`.

## Sources

- PDFs live in GCS: `gs://<bucket>/technical-library/{manuals,bulletins,recalls}/*.pdf`
  (prefixes materialize the Folder nodes). `load/parse_pdfs.py` reads local
  `sources/pdfs/` by default; `PDF_SOURCE=gcs` + `GCS_BUCKET` reads the
  bucket (lazy google-cloud-storage import).
- PDFs carry printed numbered headings (no synthetic ref codes) and real
  citation sentences ("as described in safety recall RC-2021-04") — the
  parser extracts citations against the document-id vocabulary the same way
  parts are extracted against the catalog.
- Warehouse stays CSV → `WAREHOUSE_SOURCE=databricks` later, unchanged.

## Course mapping (shape-first pedagogy)

| Module | Spec lesson (the shape) | Build challenge (from spec, with agent) |
|---|---|---|
| 2 | outline-format + search shape | `outline.py` + `search.py` |
| 3 | theme-format | `themes.py` |
| 4 | judgment specs (already spec-first) | unchanged |

Per module: read the spec → discuss what the context must include → derive
the traversal → hand spec to the agent → verify against the rendered shape.
