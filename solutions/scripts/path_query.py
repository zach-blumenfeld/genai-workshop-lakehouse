"""SOLUTION: a question becomes a join along the connections graph.

Give it two warehouse tables. It walks the connections graph (the foreign-key
metadata neocarta built) to find the join PATH between them, generates the SQL
that joins along that path, runs it on BigQuery, and shows the rows.

This is the connections shape doing its job: it hands over the exact path and
join keys, so the SQL is correct by construction instead of guessed. The
warehouse rows never moved - only the path map did.

Usage:
  python solutions/scripts/path_query.py parts vehicles \
      --where "parts.part_number = 'IC-2042-B'" \
      --select "DISTINCT vehicles.vin, vehicles.model, vehicles.engine, work_orders.wo_id, work_orders.dtc_code"
"""

import argparse
from collections import deque

from db import query
from bq import bq_query, table


def fk_edges():
    """Every foreign key as (ta, ca, tb, cb): ta.ca REFERENCES tb.cb."""
    return query("""
        MATCH (ta:Table)-[:HAS_COLUMN]->(ca:Column)-[:REFERENCES]->(cb:Column)
              <-[:HAS_COLUMN]-(tb:Table)
        RETURN ta.name AS ta, ca.name AS ca, tb.name AS tb, cb.name AS cb
    """)


def find_path(frm, to, edges):
    """Undirected BFS over the FK edges. Returns (ordered_tables, join_steps)."""
    adj = {}
    for e in edges:
        step = (e["ta"], e["ca"], e["tb"], e["cb"])
        adj.setdefault(e["ta"], []).append((e["tb"], step))
        adj.setdefault(e["tb"], []).append((e["ta"], step))

    prev = {frm: None}
    q = deque([frm])
    while q:
        cur = q.popleft()
        if cur == to:
            break
        for nxt, step in adj.get(cur, []):
            if nxt not in prev:
                prev[nxt] = (cur, step)
                q.append(nxt)
    if to not in prev:
        raise SystemExit(f"No join path between {frm} and {to}")

    steps = []
    node = to
    while prev[node] is not None:
        cur, step = prev[node]
        steps.append(step)
        node = cur
    steps.reverse()

    tables = [frm]
    for ta, ca, tb, cb in steps:
        tables.append(tb if tables[-1] == ta else ta)
    return tables, steps


def build_sql(tables, steps, select, where):
    sql = [f"SELECT {select}", f"FROM {table(tables[0])} AS {tables[0]}"]
    joined = {tables[0]}
    for ta, ca, tb, cb in steps:
        newt = tb if ta in joined else ta
        sql.append(f"JOIN {table(newt)} AS {newt} ON {ta}.{ca} = {tb}.{cb}")
        joined.add(newt)
    if where:
        sql.append(f"WHERE {where}")
    sql.append("LIMIT 20")
    return "\n".join(sql)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("from_table")
    ap.add_argument("to_table")
    ap.add_argument("--select", default=None, help="SELECT list (default: <to>.*)")
    ap.add_argument("--where", default=None)
    args = ap.parse_args()

    tables, steps = find_path(args.from_table, args.to_table, fk_edges())
    select = args.select or f"{args.to_table}.*"
    sql = build_sql(tables, steps, select, args.where)

    print("PATH :", " -> ".join(tables))
    print("\nSQL  :\n" + sql + "\n")
    rows = bq_query(sql)
    print(f"RESULT: {len(rows)} rows")
    for r in rows:
        print(" ", {k: v for k, v in r.items()})


if __name__ == "__main__":
    main()
