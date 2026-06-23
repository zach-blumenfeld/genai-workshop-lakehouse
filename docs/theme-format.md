# Theme format — the themes shape

**This is the spec you build `skill/scripts/themes.py` against.** It defines
the evidence view an agent reasons over. The tool **never names a theme** —
it ships evidence (shared targets, member titles); the agent does the naming.

## The shape

```
THEMES  AutoFix Technical Library   183 docs · 183 grouped into 13 themes by shared cross-references · 0 ungrouped

T1  20 docs (11%) · moderately interlinked
    top shared targets   [CAN Bus Communication Diagnosis Procedure] in 11 docs · [Lost Communication with BCM and Cluster] in 11 docs
    most-linked docs     Falcon Service Manual (3rd Edition) ........ D   technical-library/manuals/man-falcon-electrical.pdf
                         Body Control Module Communication Faults ... D   technical-library/bulletins/tsb-23-118.pdf
                         (+18 more docs)
    links into T2 via    Falcon Service Manual (3rd Edition) ........ D   technical-library/manuals/man-falcon-electrical.pdf
```

Rules (self-explanatory like outline — every count carries its unit):

- **Header always reconciles:** `N docs · G grouped into K themes by shared cross-references · U ungrouped`,
  with `N = G + U`. Ungrouped always prints, even at 0 — it stops the agent
  overclaiming coverage.
- **Theme line:** `T<id>  <docs> docs (<pct>%) · <cohesion>`. Theme ids are
  assigned by size order at render time and are stable **only within one
  run** — store URIs, never `T<id>`.
- **Cohesion is a word, not a number:** `tightly / moderately / loosely
  interlinked`. Backed by per-community conductance; the thresholds live in
  the producer, only the three phrases are the contract.
- **`top shared targets`** — the link targets (sections/documents) the
  theme's documents most converge on (`[Front Brake Pad and Rotor Service
  Procedure] in 8 docs`). These are the naming evidence.
- **`most-linked docs`** — member documents by within-theme link count, in
  outline row shape (dots, `D`, full URI), followed by `(+N more docs)`
  whenever membership exceeds the rows shown — counts always reconcile.
- **`links into T<j> via`** — one crossover document per connected theme:
  the drill handle for "how do these themes connect".

## The reasoning to derive

The library has no Part/DTC entity nodes — documents are tied together
purely by their **cross-reference links** (`LINKS_TO`). Two documents land
in the same theme because they link to each other or converge on the same
targets. Project a document-level graph: take every `MATCH (s:Section)-[:LINKS_TO]->(tgt)`,
collapse **both** ends to their owning document (`split(uri,'#')[0]` — no
tree walk needed), undirected, weight = link count. Then:

1. **Leiden (mutate)** assigns `themeId` in the in-memory projection —
   `gamma` is the granularity dial (higher = more, finer themes)
2. **Conductance per community** (read from the mutated property — the
   projection never sees DB writes, so mutate must precede write) maps to
   the cohesion word
3. **Write `themeId` back**, fold sub-floor themes into ungrouped
4. Renderer queries aggregate members, targets, and crossovers per theme
5. Drop the projection

Community detection on arbitrary links gives arbitrary clusters. Here every
edge exists because two documents cross-reference the same sections and
documents — so dense clusters are real repair themes, found without anyone
naming them. What holds a theme together is its **shared link targets**:
the sections and documents its members most often cite in common.
