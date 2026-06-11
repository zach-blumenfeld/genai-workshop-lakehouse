"""Detect document themes with Leiden community detection.

Usage: python skill/scripts/run_leiden.py [gamma]   (default 0.5)

Projects the section-link graph, runs Leiden weighted by how many keys two
sections share, and writes each section's communityId back to the graph.
Re-runnable: drops any existing projection first.
"""

import sys

from db import query

gamma = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5

query("CALL gds.graph.drop('doc-links', false)")

# ============================================================ FILL IN ======
# Project 'doc-links': Section nodes and LINKS_TO relationships with
# orientation UNDIRECTED, carrying the strength property as a weight.
PROJECT = """
CALL gds.graph.project(
  'doc-links',
  'Section',
  { }   // <-- complete the relationship projection
)
"""
# ===========================================================================

WRITE = """
CALL gds.leiden.write('doc-links', {
  writeProperty: 'communityId',
  relationshipWeightProperty: 'strength',
  gamma: $gamma
})
YIELD communityCount, nodeCount
RETURN communityCount, nodeCount
"""

query(PROJECT)
result = query(WRITE, gamma=gamma)
print(f"gamma={gamma}: {result[0]['communityCount']} communities over {result[0]['nodeCount']} sections")
print("communityId written to every Section - run theme_cards.py to see the themes")
