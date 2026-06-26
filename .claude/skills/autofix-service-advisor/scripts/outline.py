"""outline - render the technical library as a table of contents.

Usage: python skill/scripts/outline.py [<root-uri>] [--depth N]

The shape: a ToC the agent can navigate - display names on the left, full
copy-pasteable URIs on the right, `→` rows for outbound links. Spec:
docs/outline-format.md. Re-run rooted at any URI from the output to drill.
"""
import argparse

from db import query

INDENT = 2
NAME_COL_CAP = 52
TYPE_LETTER = {"Library": "L", "Folder": "F", "Document": "D", "Section": "S"}

# The wire query: one variable-length HAS walk from the root emits a flat
# row per node - the renderer assembles the tree client-side.
WIRE = """
// ================================================== BUILD FROM SPEC =====
// docs/outline-format.md "The wire contract": one variable-length HAS walk
// from the root (all :Library nodes when $root IS NULL, else the node with
// uri = $root) emits one row per reachable node:
//   depth, label, name, displayName, uri, parent_uri, sort_pos
// Hints: MATCH path = (root)-[:HAS*0..%d]->(n); depth = length(path);
//        parent_uri = nodes(path)[-2].uri (NULL at depth 0);
//        sort_pos = n.sortPos
RETURN 0 AS depth, 'Library' AS label, '' AS name, '' AS displayName,
       '' AS uri, NULL AS parent_uri, NULL AS sort_pos   // <-- replace
// =========================================================================
"""

LINKS = """
UNWIND $uris AS u
MATCH ({uri: u})-[:LINKS_TO]->(tgt)
RETURN u AS parent_uri,
       CASE WHEN tgt:Document THEN 'Document' ELSE 'Section' END AS label,
       tgt.name AS name, tgt.displayName AS displayName, tgt.uri AS uri
"""


def collect(root_uri, depth):
    rows = [dict(r, inrel=("HAS" if r["parent_uri"] else None))
            for r in query(WIRE % depth, root=root_uri)]
    if not rows:
        return []
    uris = [r["uri"] for r in rows if r["label"] in ("Document", "Section")]
    depth_by_uri = {r["uri"]: r["depth"] for r in rows}
    for lr in query(LINKS, uris=uris):
        if lr["parent_uri"] in depth_by_uri:
            rows.append(dict(lr, depth=depth_by_uri[lr["parent_uri"]] + 1,
                             inrel="LINKS_TO", sort_pos=None))
    return rows


def order(rows):
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent_uri"], []).append(r)
    for parent, kids in by_parent.items():
        if parent is None:
            kids.sort(key=lambda k: k["name"] or "")
            continue
        others = sorted([k for k in kids if k["inrel"] == "HAS" and k["label"] != "Section"],
                        key=lambda k: k["name"] or "")
        sections = sorted([k for k in kids if k["inrel"] == "HAS" and k["label"] == "Section"],
                          key=lambda k: k["sort_pos"] or 0)
        links = sorted([k for k in kids if k["inrel"] == "LINKS_TO"],
                       key=lambda k: k["uri"] or "")
        by_parent[parent] = others + sections + links

    output, visited = [], set()

    def emit(uri):
        if uri in visited:
            return
        visited.add(uri)
        for child in by_parent.get(uri, []):
            output.append(child)
            # A → row is visible but never extends the tree - to follow a
            # link, re-run outline rooted at its URI (spec: LINKS_TO rendering).
            if child["inrel"] != "LINKS_TO":
                emit(child["uri"])

    for root in by_parent.get(None, []):
        output.append(root)
        emit(root["uri"])
    return output


def left_string(r):
    pad = " " * (r["depth"] * INDENT)
    if r["inrel"] == "LINKS_TO":
        return f"{pad}→ {r['displayName'] or 'links_to'}"
    if r["label"] == "Folder":
        return f"{pad}{r['name']}/"
    return f"{pad}{r['displayName'] or r['name']}"


def render(rows):
    name_col = min(NAME_COL_CAP, max(len(left_string(r)) for r in rows) + 3)
    out = ["Key:  L Library   F Folder   D Document   S Section   → Links-to", "",
           f"{'NAME':<{name_col}} T   URI"]
    for r in rows:
        left = left_string(r)
        letter = "→" if r["inrel"] == "LINKS_TO" else TYPE_LETTER[r["label"]]
        if len(left) >= name_col:
            name_part = (left[: name_col - 1] + "…").ljust(name_col)
        else:
            name_part = f"{left} " + "." * (name_col - len(left) - 1)
        out.append(f"{name_part} {letter}   {r['uri']}")
    return "\n".join(out)


def main():
    p = argparse.ArgumentParser(description="Render the technical library as a table of contents.")
    p.add_argument("root", nargs="?", default=None,
                   help="root URI to drill into (default: the whole library)")
    p.add_argument("--depth", type=int, default=25, help="max HAS-tree depth to render")
    a = p.parse_args()
    rows = order(collect(a.root, a.depth))
    print(render(rows) if rows else f"(nothing found at {a.root or 'any library'})")


if __name__ == "__main__":
    main()
