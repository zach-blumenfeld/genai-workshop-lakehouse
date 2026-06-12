"""SOLUTION: Record a decision in the graph - the audit trail.

Usage:
  python solutions/scripts/write_recommendation.py events/wo-2026-0117.json \
      repair "Replace all coils with IC-2042-B per TSB-21-114; bundle recall RC-2021-04" \
      --part IC-2042-B --recall RC-2021-04 \
      --grounding 'technical-library/bulletins/tsb-21-114.pdf#repair-procedure,technical-library/recalls/rc-2021-04.pdf#remedy' --order-id PO-0001
"""

import argparse
import json

from db import query

parser = argparse.ArgumentParser()
parser.add_argument("event_file")
parser.add_argument("action", choices=["repair", "escalate"])
parser.add_argument("summary")
parser.add_argument("--part")
parser.add_argument("--recall")
parser.add_argument("--grounding", help="comma-separated Section URIs")
parser.add_argument("--order-id")
args = parser.parse_args()

event = json.load(open(args.event_file))

query(
    """
    MERGE (w:WorkOrder {id: $e.wo_id})
    SET w.opened = date($e.opened), w.odometer = toInteger($e.odometer),
        w.complaint = $e.complaint, w.status = 'open'
    WITH w
    MATCH (v:Vehicle {vin: $e.vin})
    MERGE (v)-[:HAS_WORK_ORDER]->(w)
    """,
    e=event,
)
if event.get("dtc_code"):
    query(
        """
        MATCH (w:WorkOrder {id: $wo}), (c:DTC {code: $code})
        MERGE (w)-[:DIAGNOSED]->(c)
        """,
        wo=event["wo_id"],
        code=event["dtc_code"],
    )

rec_id = f"{event['wo_id']}-R1"
query(
    """
    MATCH (w:WorkOrder {id: $wo})
    MERGE (w)-[:HAS_RECOMMENDATION]->(r:Recommendation {id: $rec})
    SET r.action = $action, r.summary = $summary, r.createdAt = datetime()
    """,
    wo=event["wo_id"],
    rec=rec_id,
    action=args.action,
    summary=args.summary,
)
if args.part:
    query(
        "MATCH (r:Recommendation {id: $rec}), (p:Part {partNumber: $part}) "
        "MERGE (r)-[:RECOMMENDS_PART]->(p)",
        rec=rec_id, part=args.part,
    )
if args.recall:
    query(
        "MATCH (r:Recommendation {id: $rec}), (rc:RecallNotice {id: $recall}) "
        "MERGE (r)-[:BUNDLES_RECALL]->(rc)",
        rec=rec_id, recall=args.recall,
    )
if args.grounding:
    query(
        "MATCH (r:Recommendation {id: $rec}) "
        "UNWIND $ids AS sid MATCH (s:Section {uri: sid}) "
        "MERGE (r)-[:GROUNDED_IN]->(s)",
        rec=rec_id, ids=args.grounding.split(","),
    )
if args.order_id:
    query(
        "MATCH (r:Recommendation {id: $rec}) "
        "MERGE (o:PartsOrder {id: $oid}) SET o.status = 'submitted' "
        "MERGE (r)-[:PLACED_ORDER]->(o)",
        rec=rec_id, oid=args.order_id,
    )

trail = query(
    """
    MATCH (v:Vehicle)-[:HAS_WORK_ORDER]->(w:WorkOrder {id: $wo})
          -[:HAS_RECOMMENDATION]->(r:Recommendation)
    OPTIONAL MATCH (r)-[:RECOMMENDS_PART]->(p:Part)
    OPTIONAL MATCH (r)-[:BUNDLES_RECALL]->(rc:RecallNotice)
    OPTIONAL MATCH (r)-[:GROUNDED_IN]->(s:Section)
    OPTIONAL MATCH (r)-[:PLACED_ORDER]->(o:PartsOrder)
    RETURN v.vin AS vin, r.action AS action, r.summary AS summary,
           p.partNumber AS part, rc.id AS recall,
           collect(DISTINCT s.uri) AS grounding, o.id AS order
    """,
    wo=event["wo_id"],
)
print(json.dumps(trail, indent=2, default=str))
