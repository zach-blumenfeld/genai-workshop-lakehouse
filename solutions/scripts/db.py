"""Shared Neo4j connection for the AutoFix skill scripts.

Reads NEO4J_URI / NEO4J_USERNAME / NEO4J_PASSWORD from the environment
(.env is loaded automatically).
"""

import os

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

_driver = None


def driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(
            os.environ["NEO4J_URI"],
            auth=(os.environ["NEO4J_USERNAME"], os.environ["NEO4J_PASSWORD"]),
            notifications_min_severity="OFF",
        )
    return _driver


def query(cypher, **params):
    """Run a query and return a list of dict records."""
    with driver().session() as session:
        return [r.data() for r in session.run(cypher, **params)]
