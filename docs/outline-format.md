# Outline format — the ToC shape

**This is the spec you build `skill/scripts/outline.py` against.** It defines
the *shape* the agent's navigation context must take. Derive the graph
reasoning from the shape; write the Cypher last.

## The shape

```
Key:  L Library   F Folder   D Document   S Section   → Links-to

NAME                                                 T   URI
AutoFix Technical Library .......................... L   technical-library
  bulletins/ ....................................... F   technical-library/bulletins
    Revised Ignition Coil for Repeated Misfire ..... D   technical-library/bulletins/tsb-21-114.pdf
      Condition .................................... S   technical-library/bulletins/tsb-21-114.pdf#condition
        → Misfire Diagnosis ........................ →   technical-library/manuals/man-fal-3.pdf#engine/misfire-diagnosis
      Cause ........................................ S   technical-library/bulletins/tsb-21-114.pdf#cause
```

Readable by humans (names left) and agents (URIs right). Rules:

- **Row** = `<indent><name> <dots> <T>   <URI>`; two spaces of indent per
  containment step; dotted leader aligns the type column.
- **URIs are full and verbatim, never truncated** — every URI round-trips
  into `outline.py <uri>` (drill) and `search.py --under <uri>` (scope).
  Names truncate with `…` at the column cap; URIs never do.
- **Folders render with a trailing `/`**; Documents and Sections render
  `displayName` (title / heading text), not the slug.
- **`→` rows** are outbound `LINKS_TO` edges (citations and derived
  shared-key links), rendered as children of their source, one extra
  indent. A `→` row **never expands its target's subtree** — to follow a
  link, re-run outline rooted at its URI.
- **Sibling order:** Folders and Documents alphabetical by name; Sections
  in `NEXT_SECTION` reading order (never alphabetical); `→` rows last,
  alphabetical by target URI.
- Header (key line + column line) always prints.

## The wire contract (query → renderer)

The renderer (given) assembles the tree client-side from flat rows. The
query you write must emit, for every node reachable from the root by `HAS`:

| field | meaning |
|---|---|
| `depth` | 0 at the root, +1 per HAS step |
| `label` | Library / Folder / Document / Section |
| `name`, `displayName`, `uri` | the node's properties, verbatim |
| `parent_uri` | URI of the HAS-parent (null at the root) |
| `sort_pos` | reading-order position for Sections (drives sibling sort) |

A second given query fetches outbound `LINKS_TO` for the visible Document
and Section rows; the renderer synthesizes `→` rows at parent depth + 1.

## The reasoning to derive

One variable-length walk materializes the whole shape: from the root
(`Library`, or any node by URI), `-[:HAS*0..N]->` reaches every descendant;
the path length is the depth; the second-to-last node on the path is the
parent. That single traversal — impossible to express as a fixed number of
joins — is why the tree lives in a graph.
