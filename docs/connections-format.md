# Connections format — the join-path shape

**This is the spec you build `skill/scripts/join_paths.py` against.** It defines
how an agent reads the warehouse's *structure* — without the warehouse rows ever
leaving BigQuery.

## Where this shape comes from

neocarta reads the BigQuery Information Schema (the PK/FK constraints you
declared in `bigquery/schema.sql`) and writes a **metadata graph** into Neo4j:

```
(:Database)-[:HAS_SCHEMA]->(:Schema)-[:HAS_TABLE]->(:Table)-[:HAS_COLUMN]->(:Column)
(:Column)-[:REFERENCES]->(:Column)        // one per foreign key — the join paths
(:Column)-[:HAS_VALUE]->(:Value)          // sample distinct values (the security knob)
```

Only this metadata crosses into Neo4j. The warehouse **rows** stay in BigQuery
(see `docs/COURSE-PLAN.md` → Architecture). The `REFERENCES` edges are the point:
they are the foreign keys, i.e. the legal joins.

## The shape

`join_paths.py <table>` returns one row per table that `<table>` joins to, with
the key:

```
work_orders joins:
  out  procedure_id -> procedures
  out  dtc_code     -> dtc_codes
  out  vin          -> vehicles
  in   wo_id        <- work_order_parts
```

- **`out`** — a key on this table references another table's primary key
- **`in`** — another table's key references this table

Chaining neighbors composes a multi-table join. To get from `work_order_parts`
to `vehicles`: `work_order_parts.wo_id → work_orders.wo_id`, then
`work_orders.vin → vehicles.vin`. That chain is what the agent turns into a
correct SQL `JOIN` in the finale — instead of guessing the keys (Text2SQL's
quiet failure).

## The reasoning to derive

A foreign key in the metadata graph is the path
`(Table)-[:HAS_COLUMN]->(Column)-[:REFERENCES]->(Column)<-[:HAS_COLUMN]-(Table)`.
A table's join neighbors are that pattern in **both** directions:

- outbound: `(t)-[:HAS_COLUMN]->(c)-[:REFERENCES]->(c2)<-[:HAS_COLUMN]-(other)`
- inbound:  `(t)-[:HAS_COLUMN]->(c)<-[:REFERENCES]-(c2)<-[:HAS_COLUMN]-(other)`

A `UNION` of the two is the tool. Why a graph and not a `SELECT` over
`INFORMATION_SCHEMA`? Because the next question — *how do I join two tables that
aren't directly related* — is a variable-length walk over `REFERENCES`, which is
a traversal, not a join. The connections live in a graph for the same reason the
document tree does.

## The security knob

neocarta pulls sample column values into `(:Value)` nodes by default (179 for
AutoFix: part numbers, VINs, `Falcon`/`Heron`/`Osprey`). They help the agent
route ("model is one of these three"), but a security-conscious team weighs
whether live values belong in the metadata graph. Naming that trade-off is part
of the lesson — it is the fourth pain (security) made concrete.
