# Theme format — the themes shape

**This is the spec you build `skill/scripts/themes.py` against.** It defines
the evidence view an agent reasons over. The tool **never names a theme** —
it ships evidence (shared targets, member titles); the agent does the naming.

## The shape

```
THEMES  AutoFix Technical Library   10 docs · 9 grouped into 4 themes by shared parts and codes · 1 ungrouped

T1  3 docs (30%) · moderately interlinked
    top shared targets   [WSS-3300] in 3 docs · [C0035] in 2 docs · [U0121] in 2 docs
    most-linked docs     Intermittent Wheel Speed Sensor Faults ..... D   technical-library/bulletins/tsb-20-087.pdf
                         Heron Service Manual (2nd Edition) ......... D   technical-library/manuals/man-her-2.pdf
                         (+1 more docs)
    links into T2 via    Heron Service Manual (2nd Edition) ......... D   technical-library/manuals/man-her-2.pdf
```

Rules (self-explanatory like outline — every count carries its unit):

- **Header always reconciles:** `N docs · G grouped into K themes by <method> · U ungrouped`,
  with `N = G + U`. Ungrouped always prints, even at 0 — it stops the agent
  overclaiming coverage.
- **Theme line:** `T<id>  <docs> docs (<pct>%) · <cohesion>`. Theme ids are
  assigned by size order at render time and are stable **only within one
  run** — store URIs, never `T<id>`.
- **Cohesion is a word, not a number:** `tightly / moderately / loosely
  interlinked`. Backed by per-community conductance; the thresholds live in
  the producer, only the three phrases are the contract.
- **`top shared targets`** — the parts and codes most referenced by the
  theme's documents (`[IC-2042-A] in 3 docs`). These are the naming
  evidence.
- **`most-linked docs`** — member documents by within-theme link count, in
  outline row shape (dots, `D`, full URI), followed by `(+N more docs)`
  whenever membership exceeds the rows shown — counts always reconcile.
- **`links into T<j> via`** — one crossover document per connected theme:
  the drill handle for "how do these themes connect".

## The reasoning to derive

Documents rarely link each other directly — but two documents that both
reference `IC-2042-A` are about the same thing. Parts and codes are **glue
nodes**: project a document-level graph where section-level references and
links are collapsed to their owning documents (`split(uri,'#')[0]` — no
tree walk needed), documents and glue nodes together, undirected, weight =
mention count. Then:

1. **Leiden (mutate)** assigns `themeId` in the in-memory projection —
   `gamma` is the granularity dial (higher = more, finer themes)
2. **Conductance per community** (read from the mutated property — the
   projection never sees DB writes, so mutate must precede write) maps to
   the cohesion word
3. **Write `themeId` back**, fold sub-floor themes into ungrouped
4. Renderer queries aggregate members, targets, and crossovers per theme
5. Drop the projection

Community detection on arbitrary links gives arbitrary clusters. Here every
edge exists because two documents touch the same physical part or fault
code — so dense clusters are real repair themes, found without anyone
naming them.
