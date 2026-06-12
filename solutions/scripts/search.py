"""search - hierarchical full-text search over the technical library.

Usage: python skill/scripts/search.py "<query>" [--under <uri-prefix>] [-k N]

Hybrid Lucene query against the content_search index:
- a structural subtree scope: URIs sort hierarchically, so --under is a
  STARTS WITH prefix filter applied after ranking (Lucene's analyzer
  tokenizes the uri field, so the scope lives in Cypher, not the query)
- the user's free-text query passed through verbatim per field, so OR/AND
  operators survive: search.py 'misfire OR "rough idle"' --under technical-library/bulletins

Lexical only - synonyms are the agent's job (semantic expansion, see
SKILL.md): rewrite thin queries with OR-alternates you know.
"""

import re
import sys

from db import query

# Escape Lucene specials - used ONLY for the uri prefix (must be literal).
# The user query is deliberately NOT escaped, preserving its operators.
_LUCENE_SPECIAL = re.compile(r'([+\-!(){}\[\]^"~*?:\\/]|&&|\|\|)')

SEARCH_FIELDS = ("displayName", "content")

CYPHER = """
CALL db.index.fulltext.queryNodes('content_search', $lucene)
YIELD node, score
WHERE $under IS NULL OR node.uri STARTS WITH $under
RETURN [l IN labels(node) WHERE l IN ['Document', 'Section']][0] AS label,
       node.uri AS uri, node.displayName AS displayName,
       left(coalesce(node.content, ''), 140) AS preview, score
ORDER BY score DESC
LIMIT toInteger($k)
"""


def escape_lucene(value):
    return _LUCENE_SPECIAL.sub(r"\\\1", value)


def build_lucene(user_query):
    per_field = " OR ".join(f"{f}:({user_query.strip()})" for f in SEARCH_FIELDS)
    return f"+({per_field})"


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit('usage: search.py "<query>" [--under <uri-prefix>] [-k N]')
    user_query = args[0]
    under = args[args.index("--under") + 1] if "--under" in args else None
    k = int(args[args.index("-k") + 1]) if "-k" in args else 10

    rows = query(CYPHER, lucene=build_lucene(user_query), under=under, k=k)
    if not rows:
        print("(no hits - consider semantic expansion: rewrite with OR-alternates)")
        return
    for r in rows:
        preview = (r["preview"] or "").split("\nuri:")[0].replace("\n", " ")
        print(f"{r['score']:6.3f}  {r['label'][0]}  {r['uri']}")
        print(f"        {r['displayName']}: {preview[:110]}")


if __name__ == "__main__":
    main()
