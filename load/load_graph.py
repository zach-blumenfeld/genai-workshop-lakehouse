"""Load the AutoFix lakehouse into Neo4j.

One command builds the workshop's starting graph:

    python load/load_graph.py

1. Parses the PDF library (sources/pdfs/) into document trees with
   part-number and trouble-code references.
2. Reads the warehouse tables (CSV exports today, Databricks tomorrow -
   see warehouse_source.py) and merges them onto the same Part and DTC
   nodes the documents reference.
3. Derives LINKS_TO between sections in different documents that share
   a key.

Connection comes from .env / environment: NEO4J_URI, NEO4J_USERNAME,
NEO4J_PASSWORD. Leiden is NOT run here - surfacing themes is Module 3.

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
    "CREATE CONSTRAINT document_id IF NOT EXISTS FOR (d:Document) REQUIRE d.id IS UNIQUE",
    "CREATE CONSTRAINT section_id IF NOT EXISTS FOR (s:Section) REQUIRE s.id IS UNIQUE",
    "CREATE CONSTRAINT part_number IF NOT EXISTS FOR (p:Part) REQUIRE p.partNumber IS UNIQUE",
    "CREATE CONSTRAINT dtc_code IF NOT EXISTS FOR (c:DTC) REQUIRE c.code IS UNIQUE",
    "CREATE CONSTRAINT vehicle_vin IF NOT EXISTS FOR (v:Vehicle) REQUIRE v.vin IS UNIQUE",
    "CREATE CONSTRAINT work_order_id IF NOT EXISTS FOR (w:WorkOrder) REQUIRE w.id IS UNIQUE",
    "CREATE CONSTRAINT procedure_id IF NOT EXISTS FOR (p:Procedure) REQUIRE p.id IS UNIQUE",
]

LOAD_DOCUMENTS = """
UNWIND $documents AS row
MERGE (d:Document {id: row.id})
SET d.docType = row.doc_type, d.title = row.title,
    d.model = row.model, d.published = date(row.published)
"""

LABEL_DOCUMENTS = [
    "MATCH (d:Document {docType: 'Manual'}) SET d:Manual",
    "MATCH (d:Document {docType: 'Bulletin'}) SET d:Bulletin",
    "MATCH (d:Document {docType: 'RecallNotice'}) SET d:RecallNotice",
]

LOAD_SECTIONS = """
UNWIND $sections AS row
MERGE (s:Section {id: row.id})
SET s.seq = toInteger(row.seq), s.title = row.title, s.text = row.text
"""

LINK_TOP_SECTIONS = """
UNWIND [r IN $sections WHERE r.parent_id = ''] AS row
MATCH (d:Document {id: row.doc_id})
MATCH (s:Section {id: row.id})
MERGE (d)-[:HAS_SECTION]->(s)
"""

LINK_SUB_SECTIONS = """
UNWIND [r IN $sections WHERE r.parent_id <> ''] AS row
MATCH (parent:Section {id: row.parent_id})
MATCH (s:Section {id: row.id})
MERGE (parent)-[:HAS_SECTION]->(s)
"""

LOAD_PART_REFS = """
UNWIND [r IN $refs WHERE r.ref_type = 'PART'] AS row
MATCH (s:Section {id: row.section_id})
MERGE (p:Part {partNumber: row.ref_value})
MERGE (s)-[:REFERENCES_PART]->(p)
"""

LOAD_CODE_REFS = """
UNWIND [r IN $refs WHERE r.ref_type = 'CODE'] AS row
MATCH (s:Section {id: row.section_id})
MERGE (c:DTC {code: row.ref_value})
MERGE (s)-[:REFERENCES_CODE]->(c)
"""

DERIVE_LINKS = """
MATCH (s1:Section)-[:REFERENCES_PART|REFERENCES_CODE]->(key)
      <-[:REFERENCES_PART|REFERENCES_CODE]-(s2:Section)
WHERE s1.id < s2.id
MATCH (d1:Document)-[:HAS_SECTION*]->(s1)
MATCH (d2:Document)-[:HAS_SECTION*]->(s2)
WHERE d1 <> d2
WITH s1, s2, collect(DISTINCT coalesce(key.partNumber, key.code)) AS sharedKeys
MERGE (s1)-[l:LINKS_TO]->(s2)
SET l.sharedKeys = sharedKeys, l.strength = size(sharedKeys)
"""

WAREHOUSE = {
    "parts": """
        UNWIND $rows AS row
        MERGE (p:Part {partNumber: row.part_number})
        SET p.name = row.name
        WITH p, row WHERE row.superseded_by <> ''
        MERGE (new:Part {partNumber: row.superseded_by})
        MERGE (p)-[:SUPERSEDED_BY]->(new)
    """,
    "dtc_codes": """
        UNWIND $rows AS row
        MERGE (c:DTC {code: row.code})
        SET c.description = row.description
    """,
    "procedures": """
        UNWIND $rows AS row
        MERGE (p:Procedure {id: row.procedure_id})
        SET p.name = row.name, p.laborHours = toFloat(row.labor_hours)
    """,
    "vehicles": """
        UNWIND $rows AS row
        MERGE (v:Vehicle {vin: row.vin})
        SET v.make = row.make, v.model = row.model,
            v.year = toInteger(row.year), v.engine = row.engine
    """,
    "work_orders": """
        UNWIND $rows AS row
        MERGE (w:WorkOrder {id: row.wo_id})
        SET w.opened = date(row.opened), w.odometer = toInteger(row.odometer),
            w.complaint = row.complaint, w.comeback = (row.comeback = 'true')
        WITH w, row
        MATCH (v:Vehicle {vin: row.vin})
        MERGE (v)-[:HAS_WORK_ORDER]->(w)
        WITH w, row
        MATCH (p:Procedure {id: row.procedure_id})
        MERGE (w)-[:PERFORMED]->(p)
        WITH w, row WHERE row.dtc_code <> ''
        MATCH (c:DTC {code: row.dtc_code})
        MERGE (w)-[:DIAGNOSED]->(c)
    """,
    "work_order_parts": """
        UNWIND $rows AS row
        MATCH (w:WorkOrder {id: row.wo_id})
        MATCH (p:Part {partNumber: row.part_number})
        MERGE (w)-[r:REPLACED]->(p)
        SET r.qty = toInteger(row.qty)
    """,
}


def main():
    load_dotenv()
    driver = GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
    )
    source = get_source()
    part_vocabulary = [r["part_number"] for r in source.rows("parts")]
    documents, sections, refs = parse_all(part_vocabulary)
    print(f"Parsed {len(documents)} PDFs -> {len(sections)} sections, {len(refs)} references")

    with driver.session() as session:
        for stmt in CONSTRAINTS:
            session.run(stmt)
        session.run(LOAD_DOCUMENTS, documents=documents)
        for stmt in LABEL_DOCUMENTS:
            session.run(stmt)
        session.run(LOAD_SECTIONS, sections=sections)
        session.run(LINK_TOP_SECTIONS, sections=sections)
        session.run(LINK_SUB_SECTIONS, sections=sections)
        session.run(LOAD_PART_REFS, refs=refs)
        session.run(LOAD_CODE_REFS, refs=refs)
        links = session.run(DERIVE_LINKS + " RETURN count(*) AS n").single()["n"]
        for table, stmt in WAREHOUSE.items():
            rows = list(source.rows(table))
            session.run(stmt, rows=rows)
            print(f"warehouse.{table}: {len(rows)} rows merged")
        counts = session.run(
            "RETURN COUNT {(:Document)} AS docs, COUNT {(:Section)} AS sections, "
            "COUNT {()-[:LINKS_TO]->()} AS links, COUNT {(:Vehicle)} AS vehicles, "
            "COUNT {(:WorkOrder)} AS workOrders, COUNT {(:Part)} AS parts"
        ).single()
        print(
            f"Graph ready: {counts['docs']} documents, {counts['sections']} sections, "
            f"{counts['links']} links, {counts['vehicles']} vehicles, "
            f"{counts['workOrders']} work orders, {counts['parts']} parts"
        )
    driver.close()


if __name__ == "__main__":
    main()
