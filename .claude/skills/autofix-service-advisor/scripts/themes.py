"""themes - surface the technical library's repair themes.

Usage: python skill/scripts/themes.py [--gamma G] [--min-docs N]

The shape (spec: docs/theme-format.md): a header that reconciles
(N docs / grouped / ungrouped), then one evidence block per theme - cohesion
word, the shared link targets the members converge on, the most-linked
member documents as outline rows, and crossover documents into other themes.
The tool never names a theme; it ships the evidence and the agent names it.

Reasoning (domain-agnostic): the library has no Part/DTC entity nodes -
documents are tied together purely by their cross-reference links (LINKS_TO).
Two documents land in the same theme because they link to each other or
converge on the same targets. Pipeline: project a doc-level graph (Section
links collapsed to owning documents, undirected, weighted) -> Leiden mutate
themeId -> per-community conductance (cohesion) -> write themeId -> renderer
queries -> drop projection. themeId is producer-owned and regenerated per run;
theme numbers are stable only within a run - store URIs, never T<id>.
"""

import sys

from db import query

GRAPH = "autofix-themes"

PROJECT = """
// ================================================== BUILD FROM SPEC =====
// docs/theme-format.md "The reasoning to derive": project a doc-level graph
// from the cross-reference links (no Part/DTC glue nodes - they do not exist).
//   - match (s:Section)-[:LINKS_TO]->(tgt)
//   - collapse BOTH ends to their owning Document via split(uri, '#')[0]
//   - drop self-pairs, count(*) per pair AS weight
//   - RETURN gds.graph.project($graph, d, t,
//       { relationshipProperties: { weight: weight } },
//       { undirectedRelationshipTypes: ['*'] })
RETURN 0   // <-- replace
// =========================================================================
"""

LEIDEN = """
CALL gds.leiden.mutate($graph, {
  mutateProperty: 'themeId', relationshipWeightProperty: 'weight',
  gamma: $gamma, randomSeed: 42, concurrency: 1
}) YIELD communityCount RETURN communityCount
"""

CONDUCTANCE = """
CALL gds.conductance.stream($graph, {
  communityProperty: 'themeId', relationshipWeightProperty: 'weight'
}) YIELD community, conductance RETURN community, conductance
"""

CLEAR = "MATCH (n) WHERE n.themeId IS NOT NULL REMOVE n.themeId"
WRITE = "CALL gds.graph.nodeProperties.write($graph, ['themeId']) YIELD propertiesWritten RETURN propertiesWritten"
DROP = "CALL gds.graph.drop($graph, false)"

FOLD = """
MATCH (m:Document) WHERE m.themeId IS NOT NULL
WITH m.themeId AS theme, count(m) AS docCount
WHERE docCount < $minDocs
WITH collect(theme) AS small
MATCH (n) WHERE n.themeId IN small
REMOVE n.themeId
"""

MEMBERS = """
MATCH (s:Section)-[:LINKS_TO]->(tgt)
MATCH (d:Document {uri: split(s.uri, '#')[0]})
MATCH (t:Document {uri: split(tgt.uri, '#')[0]})
WHERE d <> t AND d.themeId IS NOT NULL AND d.themeId = t.themeId
WITH d, count(*) AS withinThemeLinks
RETURN d.themeId AS theme, d.uri AS uri, d.displayName AS displayName,
       withinThemeLinks
ORDER BY theme, withinThemeLinks DESC, uri
"""

# What holds a theme together: the link targets the most member documents
# converge on (the sections/documents they cite in common).
TOP_TARGETS = """
MATCH (src:Section)-[:LINKS_TO]->(tgt)
MATCH (d:Document {uri: split(src.uri, '#')[0]})
WHERE d.themeId IS NOT NULL
WITH d.themeId AS theme, tgt,
     coalesce(tgt.displayName, tgt.uri) AS key, count(DISTINCT d) AS docs
WHERE docs > 1
ORDER BY theme, docs DESC, key
WITH theme, collect({key: key, docs: docs})[..5] AS targets
RETURN theme, targets
"""

CROSSOVERS = """
MATCH (src:Section)-[:LINKS_TO]->(tgt)
MATCH (s:Document {uri: split(src.uri, '#')[0]})
MATCH (t:Document {uri: split(tgt.uri, '#')[0]})
WHERE s.themeId IS NOT NULL AND t.themeId IS NOT NULL
  AND s.themeId <> t.themeId
WITH s.themeId AS theme, t.themeId AS otherTheme, s, count(*) AS crossLinks
ORDER BY theme, otherTheme, crossLinks DESC, s.uri
WITH theme, otherTheme,
     collect({uri: s.uri, displayName: s.displayName})[0] AS via
RETURN theme, otherTheme, via
"""

HEADER = """
MATCH (d:Document)
RETURN count(d) AS totalDocs, count(d.themeId) AS groupedDocs
"""


def cohesion(c):
    return "tightly interlinked" if c <= 0.2 else \
           "loosely interlinked" if c >= 0.5 else "moderately interlinked"


def dotted(display, uri, width=44):
    left = display if len(display) < width else display[: width - 1] + "…"
    return f"{left} " + "." * max(2, width - len(left) - 1) + f" D   {uri}"


def main():
    args = sys.argv[1:]
    gamma = float(args[args.index("--gamma") + 1]) if "--gamma" in args else 1.0
    min_docs = int(args[args.index("--min-docs") + 1]) if "--min-docs" in args else 2

    query(DROP, graph=GRAPH)
    query(PROJECT, graph=GRAPH)
    try:
        query(LEIDEN, graph=GRAPH, gamma=gamma)
        coh = {r["community"]: cohesion(r["conductance"])
               for r in query(CONDUCTANCE, graph=GRAPH)}
        query(CLEAR)
        query(WRITE, graph=GRAPH)
    finally:
        query(DROP, graph=GRAPH)
    query(FOLD, minDocs=min_docs)

    members = query(MEMBERS)
    targets = {r["theme"]: r["targets"] for r in query(TOP_TARGETS)}
    crossovers = query(CROSSOVERS)
    header = query(HEADER)[0]

    by_theme = {}
    for m in members:
        by_theme.setdefault(m["theme"], []).append(m)
    ordered = sorted(by_theme.items(), key=lambda kv: (-len(kv[1]), kv[1][0]["uri"]))
    tid = {theme: f"T{i}" for i, (theme, _) in enumerate(ordered, 1)}

    total, grouped = header["totalDocs"], header["groupedDocs"]
    print(f"THEMES  AutoFix Technical Library   {total} docs · {grouped} grouped "
          f"into {len(ordered)} themes by shared cross-references · {total - grouped} ungrouped")
    for theme, docs in ordered:
        pct = round(100 * len(docs) / total)
        print(f"\n{tid[theme]}  {len(docs)} docs ({pct}%) · {coh.get(theme, 'loosely interlinked')}")
        tgt_line = " · ".join(f"[{t['key']}] in {t['docs']} docs" for t in targets.get(theme, [])[:3])
        print(f"    top shared targets   {tgt_line or '(none)'}")
        label = "most-linked docs     "
        for d in docs[:3]:
            print(f"    {label}{dotted(d['displayName'], d['uri'])}")
            label = "                     "
        if len(docs) > 3:
            print(f"                         (+{len(docs) - 3} more docs)")
        for c in crossovers:
            if c["theme"] == theme and c["otherTheme"] in tid:
                print(f"    links into {tid[c['otherTheme']]} via    "
                      f"{dotted(c['via']['displayName'], c['via']['uri'])}")


if __name__ == "__main__":
    main()
