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
    -[:HAS]-> (:Document {uri, id, name, displayName,     // one PDF; id = doc slug (tsb-21-114); area = folder
                          area})
      -[:HAS]-> (:Section {uri, name, displayName,
                           headingLevel, content})        // content = Rule 1: own body + `uri:` child pointers
        -[:HAS]-> (:Section ...)                          // nested headings

(:Section)-[:NEXT_SECTION]->(:Section)                    // DFS reading order per document
(:Section)-[:LINKS_TO]->(:Document|:Section)              // real cross-references the author wrote
(:Section)-[:LINKS_TO {external:true}]->(:Document)       //   outbound URLs become stub Documents
```

**Domain-agnostic by design.** There are no `Part`/`DTC` entity nodes, no
`REFERENCES_*`, and no shared-key derivation — the same loader works on any
document estate. Part numbers and trouble codes live only in the warehouse
(BigQuery) and in the section *text*; the finale federates by full-text search
plus reading identifiers from the prose. `LINKS_TO` edges are the document
author's actual cross-references (rendered into the PDF as link annotations and
read back by the parser), not links inferred from shared keys.

URIs are hierarchical and slugified, so prefix matching scopes any subtree:

```
technical-library
technical-library/bulletins
technical-library/bulletins/tsb-21-114.pdf
technical-library/bulletins/tsb-21-114.pdf#condition
technical-library/manuals/man-fal-3.pdf#engine/ignition-coil-replacement
```

Section URI fragments are the **full heading path** (ki rule), with `-1`/`-2`
disambiguation for duplicate headings under one parent. `Document.id` is the
document slug (`tsb-21-114`); `uri` is the containment identity.

The warehouse half (vehicles / work_orders / parts / procedures / dtc_codes)
lives in **BigQuery** and is never migrated — the finale federates against it
with live SQL, joining on identifiers (part numbers, codes) that appear in both
the warehouse rows and the document text.

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
  (`N docs · G grouped into K themes by shared cross-references · U ungrouped`),
  one block per theme: cohesion word, top shared targets
  (`[Ignition Coil Replacement] in 4 docs`), most-linked docs as outline rows,
  `links into T<j> via` crossover rows. ki rule kept: **the tool never
  names a theme** — it ships the evidence; the agent names it.
- **Reasoning:** with no glue nodes, documents cluster purely by their
  cross-reference links. Project a doc-level graph: collapse both ends of every
  `(:Section)-[:LINKS_TO]->` to their owning documents (`split(uri,'#')[0]`),
  undirected, weight = link count. Leiden **mutate** → per-community conductance
  (cohesion word) → write `themeId` to Documents → renderer queries → drop
  projection. "What holds a theme together" is the set of link targets the most
  members converge on. Pure driver + Cypher `CALL gds.*` — no extra client
  dependency.
- `themeId` lives on `Document` (doc-level themes), is producer-owned,
  regenerated per run; theme numbers are stable only within a run —
  store URIs, never `T<id>`.

## Sources

- The corpus is authored as markdown in `corpus/<area>/<id>.md` and rendered to
  PDFs by `tools/render_corpus.py` (numbered headings for parse-time heading
  detection; cross-references embedded as real PDF link annotations).
- PDFs live in GCS: `gs://<bucket>/technical-library/{manuals,bulletins,recalls}/*.pdf`
  (prefixes materialize the Folder nodes). `load/parse_corpus.py` reads local
  `sources/pdfs/` by default; `PDF_SOURCE=gcs` + `GCS_BUCKET` reads the bucket
  (lazy google-cloud-storage import).
- The parser reads structure from the numbered headings and cross-reference
  edges from the PDFs' own link annotations (`doc://<id>#<frag>` portable refs →
  `LINKS_TO`; external URLs → stub Documents). No text-scraped citations, no
  shared-key derivation.
- Warehouse rows live in BigQuery (CSV exports in `sources/warehouse/` regenerated
  by `tools/generate_warehouse.py` from `tools/catalog.frozen.json`).

## Course mapping (shape-first pedagogy)

| Module | Spec lesson (the shape) | Build challenge (from spec, with agent) |
|---|---|---|
| 2 | outline-format + search shape | `outline.py` + `search.py` |
| 3 | theme-format | `themes.py` |
| 4 | judgment specs (already spec-first) | unchanged |

Per module: read the spec → discuss what the context must include → derive
the traversal → hand spec to the agent → verify against the rendered shape.
