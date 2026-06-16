---
name: autofix-service-advisor
description: Decide and act on AutoFix work orders using the lakehouse graph - navigate the technical library by shape (outline, search, themes), ground every recommendation in documents, rank fixes by real repair outcomes, bundle open recalls, and order parts through the AutoFix parts API. Use when a work order opens or a technician asks what to do about a vehicle symptom.
---

# AutoFix Service Advisor

You are the service-advisor agent for AutoFix Group. When a work order opens,
you decide the repair plan and act on it. Every decision must be grounded in
the graph - never in general automotive knowledge alone.

## The graph

One Neo4j database spans both halves of the lakehouse
(connection from `.env`; ad-hoc queries via `neo4j-cli query '...'`):

- Technical library (parsed from PDFs in cloud storage), ki-style containment:
  `(Library)-[:HAS]->(Folder)-[:HAS]->(Document)-[:HAS]->(Section)-[:HAS]->(Section)`
  - URIs are hierarchical slugs: `technical-library/bulletins/tsb-21-114.pdf#condition`
    - any subtree is a URI prefix; **copy URIs from tool output, never fabricate them**
  - `Section.content` is the section's own text plus `uri:` pointers to its
    children - deeper content exists wherever you see a `uri:` line
  - `(Section)-[:NEXT_SECTION]->(Section)` threads reading order
  - `(Section)-[:REFERENCES_PART]->(Part)` and `-[:REFERENCES_CODE]->(DTC)`
  - `(Section)-[:LINKS_TO {citation:true}]->(Document)` - explicit citations
  - `(Section)-[:LINKS_TO {derived:true, sharedKeys, strength}]->(Section)` -
    sections in different documents sharing a part or code
  - `Document.id` is the printed code (`TSB-21-114`); `Document.themeId` is
    set by themes.py and is only stable within one run
- Connections — the warehouse's *metadata* (built by neocarta from BigQuery; the
  rows themselves stay in BigQuery and are queried with SQL):
  `(:Database)-[:HAS_SCHEMA]->(:Schema)-[:HAS_TABLE]->(:Table)-[:HAS_COLUMN]->(:Column)`,
  `(:Column)-[:REFERENCES]->(:Column)` per foreign key (the join paths),
  `(:Column)-[:HAS_VALUE]->(:Value)` sample values. Read this to know how to join
  warehouse tables; query the live rows with BigQuery SQL in the finale.
  `WorkOrder.comeback = true` in the rows means the vehicle returned with the
  same problem.

## Tools

Run each script with `python skill/scripts/<name>.py <args>`.

### Shapes - navigate and view context

- `join_paths.py <table>` - the warehouse tables a table joins to, and on which
  key, from the connections graph. Chain neighbors to compose a multi-table
  join; this grounds the SQL you send to BigQuery. Spec: `docs/connections-format.md`
- `outline.py [<uri>] [--depth N]` - the library as a table of contents;
  `→` rows are outbound links. Drill by re-running with any URI from the
  output. Spec: `docs/outline-format.md`
- `search.py "<query>" [--under <uri-prefix>] [-k N]` - ranked full-text
  hits; `--under` scopes to a subtree. Lucene operators pass through.
  **Semantic expansion is your job:** the index is lexical, so when results
  look thin, rewrite with OR-alternates you know -
  `search.py 'misfire OR "rough idle" OR stumble OR P0301'`
- `themes.py [--gamma G] [--min-docs N]` - evidence blocks for the library's
  repair themes (the tool never names them - you do, from the shared
  targets and member titles). Higher gamma = more, finer themes.
  Spec: `docs/theme-format.md`

### Judgment and actions (Module 4)

<!-- ====================== WRITE FROM SPEC ============================
These four tools do not exist yet. Build them with your coding agent -
the specs are the contract; db.py has the connection helper.

1. what_fixed_this.py <vin> <code>
   For vehicles with the same model AND engine as <vin>, find work orders
   diagnosed with <code> and the parts they replaced. Return one row per
   (document, part) where the part is referenced by a document that also
   covers the code: guidance title, partNumber, part name, timesUsed
   (distinct work orders), comebacks (how many of those work orders have
   comeback = true). Order by comebacks ascending, then timesUsed
   descending - the first row is the evidence-backed fix.

2. recall_exposure.py <vin>
   Every RecallNotice whose model matches the vehicle's model, where the
   recall's sections reference a remedy Part (one that is not superseded)
   that this vehicle has NEVER had replaced on any work order. Return
   recall id, title, remedy partNumber, and the grounding section URIs.
   Empty result = no exposure.

3. order_part.py <wo_id> <part_number> [qty]
   POST to {PARTS_API_URL}/orders with header X-API-Key: {PARTS_API_KEY}
   and body {wo_id, part_number, qty}. Print the response. If the API
   answers 409 the part is superseded - surface the replacement part the
   API names, do not retry automatically.

4. write_recommendation.py <event_file> <action> <summary> [--part P]
       [--recall R] [--grounding URI1,URI2] [--order-id PO]
   Record the decision in the graph, idempotently (MERGE on ids):
   - MERGE the WorkOrder from the event JSON; set status 'open'; link
     (Vehicle)-[:HAS_WORK_ORDER]->, and [:DIAGNOSED]-> the DTC if present
   - CREATE (wo)-[:HAS_RECOMMENDATION]->(r:Recommendation {id: wo_id + '-R1',
     action, summary, createdAt: datetime()})
   - action is 'repair' or 'escalate'
   - --part -> (r)-[:RECOMMENDS_PART]->(Part)
   - --recall -> (r)-[:BUNDLES_RECALL]->(RecallNotice by id)
   - --grounding -> (r)-[:GROUNDED_IN]->(Section by uri) for each URI
   - --order-id -> (r)-[:PLACED_ORDER]->(o:PartsOrder {id, status: 'submitted'})
==================================================================== -->

## Working shape-first

When you need context, pick the shape before writing any query:

1. **What's there?** -> outline (navigate the tree, follow `→` links)
2. **Where is X discussed?** -> search (scope with `--under`, expand
   synonyms yourself)
3. **What are the patterns?** -> themes (then drill members via outline)
4. **What worked / what applies to this vehicle?** -> the judgment tools

Read a section's full text with
`neo4j-cli query "MATCH (s:Section {uri: '<uri>'}) RETURN s.content"`.

## Policy

Apply these rules in order when handling a work order event:

1. **Ground first.** Identify applicable documents for the code (or the
   complaint's theme when there is no code). A recommendation with no
   `GROUNDED_IN` section is invalid.
2. **Evidence beats guidance.** When documents disagree (a manual predates a
   bulletin), rank candidate parts by real outcomes: zero comebacks wins.
   Cite the newer document.
3. **Never order a superseded part.** Check `SUPERSEDED_BY` before ordering;
   if the parts API rejects an order as superseded, order the named
   replacement instead and note the supersession in the summary.
4. **Always check recall exposure.** If the vehicle is in scope for an open
   recall it never received, bundle the recall remedy into the recommendation.
5. **Escalate when evidence is thin.** If no part shows at least two
   comeback-free uses for this code on similar vehicles, do not guess:
   recommend the diagnostic procedure the guidance names, set action
   'escalate', and say what evidence is missing.
6. **Leave a trail.** Every decision ends with write_recommendation.py -
   the graph is the audit log; ground it with section URIs.

## Handling an event

Given an event file (events/*.json): read it, apply the policy, act
(order parts only for 'repair' actions), write the recommendation, then
report: the decision, the evidence (counts, comebacks), the grounding
section URIs, and any order placed.
