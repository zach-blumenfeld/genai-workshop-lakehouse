---
id: man-fal-3
title: Falcon Service Manual (3rd Edition)
area: manuals
---

# Engine

Service coverage for the Cascadia Falcon 2.0T and 1.6 engines: driveability
diagnosis, ignition service, and related emissions interactions.

## Misfire Diagnosis

Misfire codes P0300 (random/multiple) and P0301 (cylinder 1) on the 2.0T are
most often ignition-related. Confirm fuel trims and compression are within range
before condemning a coil. Begin with the
[Ignition System](doc://man-fal-3#engine/ignition-system) checks. If a coil has
already been replaced and the misfire returns, the original part may be at
fault — see [Revised Ignition Coil for Repeated Misfire](doc://tsb-21-114). A
persistent misfire can also set catalyst code P0420 downstream; see
[Catalyst Efficiency](doc://man-fal-3#emissions/catalyst-efficiency).

## Ignition System

The 2.0T uses a coil-on-plug ignition system. Inspect coil boots and connectors
for heat damage before parts replacement.

### Ignition Coil Replacement

Replace the ignition coil IC-2042-A as a complete set; mixing old and new coils
masks a weak cylinder. Torque the hold-down bolts to 9 Nm. On early-production
vehicles the connector can overheat — refer to
[Safety Recall RC-2021-04](doc://rc-2021-04#defect-description) and install the
revised coil IC-2042-B. Always replace the spark plug set when servicing coils
(see [Spark Plug Service](doc://man-fal-3#engine/ignition-system/spark-plug-service)).

### Spark Plug Service

Replace spark plug set SP-1108 at the specified interval or whenever the coils
are serviced. Gap to 0.7 mm. Worn plugs are a common contributor to P0301.

# Emissions

Catalyst monitoring and engine-control software for the Falcon platform.

## Catalyst Efficiency

Code P0420 indicates catalyst efficiency below threshold. Rule out upstream
misfire (see [Misfire Diagnosis](doc://man-fal-3#engine/misfire-diagnosis))
before replacing the catalytic converter CAT-5500, as raw fuel from a misfire
damages the catalyst.

## ECM Software Updates

Some driveability and emissions complaints are resolved by an ECM-9901 software
update rather than hardware. See
[Updated Catalyst Monitor Calibration](doc://tsb-20-087).

# Brakes

Front brake service and hydraulic system for the Falcon platform.

## Front Brake Service

Service the front brake pad kit BP-7720 and rotor pair BR-7731 as a set.
Machining is not approved on this rotor. For brake judder after a pad change,
see [Brake Judder After Front Pad Replacement](doc://tsb-22-031).

## Brake Hose Replacement

Replace the front brake hose BH-7745 if cracked or swollen. Bleed the system in
the specified sequence after service.

# ABS

Wheel-speed and anti-lock control diagnosis.

## Wheel Speed Sensors

Code C0035 indicates a left front wheel speed sensor circuit fault. Inspect the
sensor WSS-3300 and its harness routing near the brake hose. Sensor faults can
cascade to ABS communication loss; see
[ABS Module Diagnosis](doc://man-fal-3#abs/abs-module-diagnosis).

## ABS Module Diagnosis

Code U0121 indicates lost communication with the ABS control module. Check power,
ground, and CAN continuity before module replacement. A recall applies to certain
harness routings — see [Wheel Speed Sensor Harness Chafing](doc://rc-2022-09).

# Electrical

Charging and starting system service.

## Charging System

A no-charge condition sets P0562 (system voltage low). Test the alternator
ALT-8810 output before replacement and confirm the battery is healthy (see
[Battery Service](doc://man-fal-3#electrical/battery-service)).

## Battery Service

Replace the AGM battery BAT-1200 with the same chemistry; register the new
battery to the charging system where required.
