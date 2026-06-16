"""Load the AutoFix lakehouse into Neo4j - ki-style containment model.

One command builds the workshop's starting graph:

    python load/load_graph.py

1. Parses the PDF library into Library -> Folder -> Document -> Section
   containment (single HAS relationship type), with hierarchical URIs,
   Rule-1 section content, NEXT_SECTION reading order, part/code
   references, and explicit citation links.
2. Derives LINKS_TO {derived:true} between sections in different documents
   that share a part or code; citations land as LINKS_TO {citation:true}.
3. Creates the content_search fulltext index for hierarchical search.

Part and DTC nodes come only from document references; the warehouse rows
live in BigQuery (the finale federates against them). The parts catalog is
still read as the vocabulary for extracting part numbers from PDF text.

Connection from .env: NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD.
Themes are NOT computed here - surfacing them is Module 3 (themes.py).
Idempotent: every write is MERGE; safe to re-run.
"""

import os
import sys

from dotenv import load_dotenv
from neo4j import GraphDatabase

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_pdfs import parse_all
from warehouse_source import get_source

CONSTRAINTS = [
    "CREATE CONSTRAINT library_uri IF NOT EXISTS FOR (l:Library) REQUIRE l.uri IS UNIQUE",
    "CREATE CONSTRAINT folder_uri IF NOT EXISTS FOR (f:Folder) REQUIRE f.uri IS UNIQUE",
    "CREATE CONSTRAINT document_uri IF NOT EXISTS FOR (d:Document) REQUIRE d.uri IS UNIQUE",
    "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
    "CREATE CONSTRAINT section_uri IF NOT EXISTS FOR (s:Section) REQUIRE s.uri IS UNIQUE",
    "CREATE CONSTRAINT part_number IF NOT EXISTS FOR (p:Part) REQUIRE p.partNumber IS UNIQUE",
    "CREATE CONSTRAINT dtc_code IF NOT EXISTS FOR (c:DTC) REQUIRE c.code IS UNIQUE",
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
SET d.id = row.id, d.docType = row.doc_type, d.title = row.title,
    d.displayName = row.displayName, d.name = row.name,
    d.model = row.model, d.published = date(row.published)
WITH d, row
MATCH (f:Folder {uri: row.parent_uri})
MERGE (f)-[:HAS]->(d)
"""

LABEL_DOCUMENTS = [
    "MATCH (d:Document {docType: 'Manual'}) SET d:Manual",
    "MATCH (d:Document {docType: 'Bulletin'}) SET d:Bulletin",
    "MATCH (d:Document {docType: 'RecallNotice'}) SET d:RecallNotice",
]

LOAD_SECTIONS = """
UNWIND $sections AS row
MERGE (s:Section {uri: row.uri})
SET s.name = row.name, s.displayName = row.displayName,
    s.headingLevel = row.headingLevel, s.content = row.content,
    s.sortPos = row.sort_pos
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
MATCH (s:Section {uri: row.uri})
WITH row.doc_uri AS doc, s ORDER BY s.sortPos
WITH doc, collect(s) AS ordered
UNWIND range(0, size(ordered) - 2) AS i
WITH ordered[i] AS a, ordered[i + 1] AS b
MERGE (a)-[:NEXT_SECTION]->(b)
"""

LOAD_PART_REFS = """
UNWIND [r IN $refs WHERE r.ref_type = 'PART'] AS row
MATCH (s:Section {uri: row.section_uri})
MERGE (p:Part {partNumber: row.ref_value})
MERGE (s)-[:REFERENCES_PART]->(p)
"""

LOAD_CODE_REFS = """
UNWIND [r IN $refs WHERE r.ref_type = 'CODE'] AS row
MATCH (s:Section {uri: row.section_uri})
MERGE (c:DTC {code: row.ref_value})
MERGE (s)-[:REFERENCES_CODE]->(c)
"""

LOAD_CITATIONS = """
UNWIND $citations AS row
MATCH (s:Section {uri: row.section_uri})
MATCH (d:Document {id: row.doc_id})
MERGE (s)-[l:LINKS_TO]->(d)
SET l.citation = true
"""

DERIVE_LINKS = """
MATCH (s1:Section)-[:REFERENCES_PART|REFERENCES_CODE]->(key)
      <-[:REFERENCES_PART|REFERENCES_CODE]-(s2:Section)
WHERE s1.uri < s2.uri
  AND split(s1.uri, '#')[0] <> split(s2.uri, '#')[0]
WITH s1, s2, collect(DISTINCT coalesce(key.partNumber, key.code)) AS sharedKeys
MERGE (s1)-[l:LINKS_TO]->(s2)
SET l.derived = true, l.sharedKeys = sharedKeys, l.strength = size(sharedKeys)
"""



def main():
    load_dotenv(override=True)  # .env is the source of truth, even over exported vars
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
        notifications_min_severity="OFF",
    )
    source = get_source()
    part_vocabulary = [r["part_number"] for r in source.rows("parts")]
    library, folders, documents, sections, refs, citations = parse_all(part_vocabulary)
    print(
        f"Parsed {len(documents)} PDFs -> {len(folders)} folders, "
        f"{len(sections)} sections, {len(refs)} references, {len(citations)} citations"
    )

    with driver.session() as session:
        for stmt in CONSTRAINTS:
            session.run(stmt)
        session.run(FULLTEXT_INDEX)
        session.run(LOAD_LIBRARY, library=library)
        session.run(LOAD_FOLDERS, folders=folders)
        session.run(LOAD_DOCUMENTS, documents=documents)
        for stmt in LABEL_DOCUMENTS:
            session.run(stmt)
        session.run(LOAD_SECTIONS, sections=sections)
        session.run(LINK_SECTION_PARENTS, sections=sections)
        session.run(NEXT_SECTIONS, sections=sections)
        session.run(LOAD_PART_REFS, refs=refs)
        session.run(LOAD_CODE_REFS, refs=refs)
        session.run(LOAD_CITATIONS, citations=citations)
        session.run(DERIVE_LINKS)
        counts = session.run(
            "RETURN COUNT {(:Library)} AS lib, COUNT {(:Folder)} AS folders, "
            "COUNT {(:Document)} AS docs, COUNT {(:Section)} AS sections, "
            "COUNT {()-[:HAS]->()} AS has, COUNT {()-[:NEXT_SECTION]->()} AS next, "
            "COUNT {()-[:LINKS_TO {citation: true}]->()} AS citations, "
            "COUNT {()-[:LINKS_TO {derived: true}]->()} AS derived, "
            "COUNT {(:Part)} AS parts, COUNT {(:DTC)} AS codes"
        ).single()
        print(
            f"Graph ready: {counts['lib']} library, {counts['folders']} folders, "
            f"{counts['docs']} documents, {counts['sections']} sections | "
            f"HAS {counts['has']}, NEXT_SECTION {counts['next']}, "
            f"citations {counts['citations']}, derived links {counts['derived']} | "
            f"{counts['parts']} parts, {counts['codes']} codes referenced "
            f"(warehouse rows stay in BigQuery)"
        )
    driver.close()


if __name__ == "__main__":
    main()
