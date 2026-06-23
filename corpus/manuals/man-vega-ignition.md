---
id: man-vega-ignition
title: Vega Ignition Service Manual
area: manuals
---

# Ignition System Overview

The Vega ignition system uses a coil-on-plug architecture with individual coils for each cylinder, supporting both gasoline spark-ignition and diesel glow-plug variants. This manual covers coil, spark plug, and glow plug service along with circuit diagnosis. For the closely related platform sharing many coil applications, cross-reference the [Heron Ignition Service Manual](doc://man-heron-ignition). Disconnect the battery negative terminal before servicing any ignition component.

# Ignition System Diagnosis

Ignition faults on the Vega typically present as misfires, hard starts, or illuminated MIL with stored coil-circuit codes. Fault codes P0351 and P0352 point directly to the primary control circuits for the cylinder one and cylinder two coils. Swap suspect coils between cylinders to confirm whether a fault follows the component or stays with the circuit, as detailed in the [Heron Ignition Service Manual :: Ignition Circuit Diagnosis](doc://man-heron-ignition#ignition-circuit-diagnosis).

## Ignition Coil Circuit Fault Codes

Code P0351 indicates an ignition coil A primary or secondary circuit malfunction, and P0352 indicates the same condition for coil B. Back-probe the coil connector to verify supply voltage, ground, and the ECM drive signal before condemning the coil. Persistent P0351 or P0352 codes with good wiring confirm a failed coil, and the wiring tests are expanded in the [Heron Ignition Service Manual :: Coil Primary and Secondary Circuit Faults](doc://man-heron-ignition#ignition-circuit-diagnosis/coil-primary-and-secondary-circuit-faults).

# Ignition Coil Sub-System

The Vega coil sub-system spans several part numbers across engine variants, including IC-2042-A, IC-2042-B, IC-2044-A, and IC-2050-A. Coil selection depends on engine displacement and model year, and superseded numbers must be matched carefully. The [Heron Ignition Service Manual :: Ignition Coils](doc://man-heron-ignition#ignition-coils) section lists equivalent applications.

## Ignition Coil Identification and Supersession

Coil IC-2042-A was the original-fit unit and has been superseded by IC-2042-B, which adds an improved connector seal and is fully backward compatible. When IC-2042-A is no longer available, install IC-2042-B in a complete set on that engine. Supersession history is mirrored in the [Heron Ignition Service Manual :: Coil Identification and Supersession](doc://man-heron-ignition#ignition-coils/coil-identification-and-supersession).

## Coil Applications Across Engine Variants

The turbocharged Vega variant uses coil IC-2044-A, while the high-output performance engine requires the higher-energy IC-2050-A. These coils are not interchangeable with the base IC-2042 series due to differences in primary resistance and dwell calibration. Confirm the correct application against the [Heron Ignition Service Manual :: Application-Specific Coils](doc://man-heron-ignition#ignition-coils/application-specific-coils).

### Ignition Coil Replacement Procedure

Follow procedure PROC-IGN-COIL: release the connector lock, remove the hold-down bolt, and pull the coil straight up from the spark-plug well. When replacing IC-2042-A with the superseded IC-2042-B, apply dielectric grease to the boot to prevent moisture-induced P0351 and P0352 faults. Torque the hold-down bolt to specification and clear codes, then road-test to confirm no recurrence; the equivalent steps appear in the [Heron Ignition Service Manual :: Ignition Coil Replacement Procedure](doc://man-heron-ignition#ignition-coils/ignition-coil-replacement-procedure).

# Spark Plug Sub-System

The Vega spark plug sub-system uses iridium plugs selected by engine variant: SP-1108, SP-1110, and SP-1112. Heat range and reach differ between these part numbers, so verify the application before installation. See the [Heron Ignition Service Manual :: Spark Plugs](doc://man-heron-ignition#spark-plugs) for cross-reference data.

## Spark Plug Specifications and Applications

Spark plug SP-1108 fits the naturally aspirated base engine with a 0.044-inch gap, SP-1110 fits the turbocharged engine with a colder heat range, and SP-1112 is the long-reach plug for the high-output variant. Never install a hotter plug in a boosted application, as pre-ignition can result. Gap and torque specifications are tabulated in the [Heron Ignition Service Manual :: Spark Plug Selection and Specifications](doc://man-heron-ignition#spark-plugs/spark-plug-selection-and-specifications).

### Spark Plug Replacement Procedure

Follow procedure PROC-SPARK-PLUG: remove the coils, blow debris from the wells, and back out each plug only when the engine is cool to protect the aluminum threads. Gap-check each new SP-1108, SP-1110, or SP-1112 even though they ship pre-gapped, and apply a light anti-seize per the specification. Torque to value and reinstall the coils, referencing the [Heron Ignition Service Manual :: Spark Plug Replacement Procedure](doc://man-heron-ignition#spark-plugs/spark-plug-replacement-procedure).

# Glow Plug Sub-System

Diesel Vega variants rely on glow plugs to aid cold starting and reduce cold-start emissions. The glow plug sub-system is controlled by a dedicated relay module that monitors plug resistance.

## Diesel Glow Plug Service

Glow plug GP-1304 is the service part for all diesel Vega engines and must be torqued carefully to avoid cracking the ceramic tip. Test each plug for correct resistance and inspect for tip swelling before reuse. Detailed diesel-specific steps are provided in the [Heron Ignition Service Manual :: Glow Plug Service](doc://man-heron-ignition#glow-plug-system-diesel/glow-plug-service), part of the broader [Heron Ignition Service Manual :: Glow Plug System (Diesel)](doc://man-heron-ignition#glow-plug-system-diesel) coverage.
