"""Load the document corpus into Neo4j - domain-agnostic containment + links.

Reads the rendered PDFs (load/parse_corpus.py) and builds the generic graph:

    (Library)-[:HAS]->(Folder)-[:HAS]->(Document)-[:HAS]->(Section)-[:HAS]->(Section)
    (Section)-[:NEXT_SECTION]->(Section)        reading order
    (Section)-[:LINKS_TO]->(Document|Section)   real cross-references (PDF links)

No domain entities (no Part/DTC, no per-type Document labels, no REFERENCES_*,
no shared-key derivation). The same loader works on any document estate. The
finale federates to BigQuery on identifiers that appear in section *text*, found
by full-text search - not by graph entities.

External link targets (URLs) become stub :Document nodes (metadata only).

Run: .venv/bin/python load/load_documents.py
Wipes and rebuilds only the document half (Library/Folder/Document/Section and
their indexes); any connections graph (:Table/:Column from build_connections.py)
is left untouched, so the two loaders can run in either order.
"""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

from parse_corpus import parse_all

CONSTRAINTS = [
    "CREATE CONSTRAINT document_uri IF NOT EXISTS FOR (d:Document) REQUIRE d.uri IS UNIQUE",
    "CREATE CONSTRAINT section_uri IF NOT EXISTS FOR (s:Section) REQUIRE s.uri IS UNIQUE",
]

FULLTEXT_INDEX = """
CREATE FULLTEXT INDEX content_search IF NOT EXISTS
FOR (n:Document|Section) ON EACH [n.displayName, n.content, n.uri]
"""

LOAD_LIBRARY = """
MERGE (l:Library {uri: $library.uri})
SET l.name = $library.name, l.displayName = $library.displayName
"""

LOAD_FOLDERS = """
UNWIND $folders AS row
MERGE (f:Folder {uri: row.uri})
SET f.name = row.name, f.displayName = row.displayName
WITH f, row
MATCH (l:Library {uri: row.parent_uri})
MERGE (l)-[:HAS]->(f)
"""

LOAD_DOCUMENTS = """
UNWIND $documents AS row
MERGE (d:Document {uri: row.uri})
SET d.id = row.id, d.title = row.title, d.area = row.area,
    d.displayName = row.displayName, d.name = row.name, d.stub = false
WITH d, row
MATCH (f:Folder {uri: row.parent_uri})
MERGE (f)-[:HAS]->(d)
"""

LOAD_SECTIONS = """
UNWIND $sections AS row
MERGE (s:Section {uri: row.uri})
SET s.name = row.name, s.displayName = row.displayName,
    s.headingLevel = row.headingLevel, s.content = row.content, s.sort_pos = row.sort_pos
"""

LINK_SECTION_PARENTS = """
UNWIND $sections AS row
MATCH (s:Section {uri: row.uri})
MATCH (parent {uri: row.parent_uri})
WHERE parent:Document OR parent:Section
MERGE (parent)-[:HAS]->(s)
"""

NEXT_SECTIONS = """
UNWIND $sections AS row
WITH row.doc_uri AS doc, row ORDER BY row.sort_pos
WITH doc, collect(row.uri) AS uris
UNWIND range(0, size(uris) - 2) AS i
MATCH (a:Section {uri: uris[i]}), (b:Section {uri: uris[i + 1]})
MERGE (a)-[:NEXT_SECTION]->(b)
"""

# In-corpus links: source Section -> resolved Document/Section.
LOAD_LINKS = """
UNWIND $links AS row
MATCH (src:Section {uri: row.source_uri})
MATCH (tgt {uri: row.target_uri})
MERGE (src)-[r:LINKS_TO]->(tgt)
SET r.embed = row.embed
"""

# External links: source Section -> stub Document (the URL itself).
LOAD_EXTERNAL_LINKS = """
UNWIND $externals AS row
MATCH (src:Section {uri: row.source_uri})
MERGE (d:Document {uri: row.external})
SET d.stub = true, d.displayName = coalesce(d.displayName, row.external),
    d.name = coalesce(d.name, row.external)
MERGE (src)-[r:LINKS_TO]->(d)
SET r.external = true, r.embed = row.embed
"""


def wipe(session):
    """Clear only the document half - Library/Folder/Document/Section nodes
    (and, by DETACH, their HAS/NEXT_SECTION/LINKS_TO edges) plus the doc-specific
    constraints and full-text index. The connections graph (:Table/:Column) is a
    disjoint set of labels, so it survives - load_documents.py and
    build_connections.py write into the same sandbox without clobbering."""
    for name in ("document_uri", "section_uri"):
        session.run(f"DROP CONSTRAINT {name} IF EXISTS")
    session.run("DROP INDEX content_search IF EXISTS")
    # Batch the delete with CALL { ... } IN TRANSACTIONS so each chunk commits
    # separately - a single DETACH DELETE of a large library holds every change
    # in one transaction and can OOM. See:
    # https://neo4j.com/docs/cypher-manual/current/subqueries/subqueries-in-transactions/#delete-with-call-in-transactions
    # (Requires an auto-commit transaction, which session.run provides.)
    session.run(
        "MATCH (n) WHERE n:Library OR n:Folder OR n:Document OR n:Section "
        "CALL (n) { DETACH DELETE n } IN TRANSACTIONS OF 10000 ROWS"
    ).consume()


def main():
    load_dotenv(override=True)
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
        notifications_min_severity="OFF",
    )
    database = os.environ.get("NEO4J_DATABASE", "neo4j")

    library, folders, documents, sections, links = parse_all()
    in_corpus = [lk for lk in links if lk["target_uri"]]
    externals = [lk for lk in links if lk["external"]]
    print(f"Parsed {len(documents)} PDFs -> {len(folders)} folders, {len(sections)} "
          f"sections, {len(in_corpus)} in-corpus links, {len(externals)} external links")

    with driver.session(database=database) as session:
        wipe(session)
        for stmt in CONSTRAINTS:
            session.run(stmt)
        session.run(FULLTEXT_INDEX)
        session.run(LOAD_LIBRARY, library=library)
        session.run(LOAD_FOLDERS, folders=folders)
        session.run(LOAD_DOCUMENTS, documents=documents)
        session.run(LOAD_SECTIONS, sections=sections)
        session.run(LINK_SECTION_PARENTS, sections=sections)
        session.run(NEXT_SECTIONS, sections=sections)
        session.run(LOAD_LINKS, links=in_corpus)
        session.run(LOAD_EXTERNAL_LINKS, externals=externals)
        c = session.run(
            "RETURN COUNT {(:Library)} AS lib, COUNT {(:Folder)} AS folders, "
            "COUNT {(:Document)} AS docs, COUNT {(:Document {stub:true})} AS stubs, "
            "COUNT {(:Section)} AS sections, COUNT {()-[:HAS]->()} AS has, "
            "COUNT {()-[:NEXT_SECTION]->()} AS next, COUNT {()-[:LINKS_TO]->()} AS links"
        ).single()
        print(f"Graph ready: {c['lib']} library, {c['folders']} folders, "
              f"{c['docs']} documents ({c['stubs']} stub), {c['sections']} sections | "
              f"HAS {c['has']}, NEXT_SECTION {c['next']}, LINKS_TO {c['links']}")
    driver.close()


if __name__ == "__main__":
    main()
