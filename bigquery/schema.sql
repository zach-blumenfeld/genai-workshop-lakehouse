-- AutoFix warehouse — BigQuery DDL with PRIMARY KEY / FOREIGN KEY constraints.
--
-- The constraints are NOT ENFORCED (BigQuery does not validate them) but they
-- ARE surfaced in INFORMATION_SCHEMA — which is exactly what neocarta reads to
-- materialize the Column-[:REFERENCES]->Column graph (the connections shape).
-- Without declared keys, the metadata graph has no join paths.
--
-- Placeholders ${PROJECT} and ${DATASET} are filled by setup.sh (envsubst).
-- Run order matters: tables first, then foreign keys.

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.vehicles` (
  vin STRING NOT NULL,
  make STRING,
  model STRING,
  year INT64,
  engine STRING,
  PRIMARY KEY (vin) NOT ENFORCED
) OPTIONS (description = 'One row per serviced vehicle.');

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.dtc_codes` (
  code STRING NOT NULL,
  description STRING,
  PRIMARY KEY (code) NOT ENFORCED
) OPTIONS (description = 'Diagnostic trouble code reference (OBD-II).');

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.procedures` (
  procedure_id STRING NOT NULL,
  name STRING,
  labor_hours FLOAT64,
  PRIMARY KEY (procedure_id) NOT ENFORCED
) OPTIONS (description = 'Labor procedures performed on work orders.');

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.parts` (
  part_number STRING NOT NULL,
  name STRING,
  superseded_by STRING,
  PRIMARY KEY (part_number) NOT ENFORCED
) OPTIONS (description = 'Parts catalog; superseded_by points to the replacement part.');

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.work_orders` (
  wo_id STRING NOT NULL,
  vin STRING,
  opened DATE,
  odometer INT64,
  complaint STRING,
  dtc_code STRING,
  procedure_id STRING,
  comeback BOOL,
  PRIMARY KEY (wo_id) NOT ENFORCED
) OPTIONS (description = 'A repair visit; comeback = true means the vehicle returned with the same problem.');

CREATE TABLE IF NOT EXISTS `${PROJECT}.${DATASET}.work_order_parts` (
  wo_id STRING NOT NULL,
  part_number STRING NOT NULL,
  qty INT64,
  PRIMARY KEY (wo_id, part_number) NOT ENFORCED
) OPTIONS (description = 'Parts replaced on a work order (bridge: work_orders <-> parts).');

-- Foreign keys = the join paths neocarta turns into REFERENCES edges.
-- NOTE: parts.superseded_by is a self-reference (part -> replacement part), but
-- BigQuery rejects foreign keys that reference their own table. So supersession
-- stays a queryable column (the agent reads it via SQL; the parts API also
-- enforces it with a 409). To model it as a join-path edge you'd add a
-- part_supersession(old, new) bridge table — deferred; not needed for the workshop.

ALTER TABLE `${PROJECT}.${DATASET}.work_orders`
  ADD CONSTRAINT IF NOT EXISTS fk_wo_vehicle
  FOREIGN KEY (vin) REFERENCES `${PROJECT}.${DATASET}.vehicles`(vin) NOT ENFORCED;

ALTER TABLE `${PROJECT}.${DATASET}.work_orders`
  ADD CONSTRAINT IF NOT EXISTS fk_wo_dtc
  FOREIGN KEY (dtc_code) REFERENCES `${PROJECT}.${DATASET}.dtc_codes`(code) NOT ENFORCED;

ALTER TABLE `${PROJECT}.${DATASET}.work_orders`
  ADD CONSTRAINT IF NOT EXISTS fk_wo_procedure
  FOREIGN KEY (procedure_id) REFERENCES `${PROJECT}.${DATASET}.procedures`(procedure_id) NOT ENFORCED;

ALTER TABLE `${PROJECT}.${DATASET}.work_order_parts`
  ADD CONSTRAINT IF NOT EXISTS fk_wop_workorder
  FOREIGN KEY (wo_id) REFERENCES `${PROJECT}.${DATASET}.work_orders`(wo_id) NOT ENFORCED;

ALTER TABLE `${PROJECT}.${DATASET}.work_order_parts`
  ADD CONSTRAINT IF NOT EXISTS fk_wop_part
  FOREIGN KEY (part_number) REFERENCES `${PROJECT}.${DATASET}.parts`(part_number) NOT ENFORCED;
