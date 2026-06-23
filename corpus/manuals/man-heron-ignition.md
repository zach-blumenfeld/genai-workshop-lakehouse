---
id: man-heron-ignition
title: Heron Ignition Service Manual
area: manuals
---

# Introduction and Ignition System Overview

This manual describes the ignition system for the Heron platform, covering coil-on-plug gasoline ignition and diesel glow-plug preheating. The Heron ignition architecture closely parallels the Marlin EV platform; consult the [Marlin EV Ignition Service Manual :: Ignition System Overview](doc://man-marlin-ev-ignition#ignition-system-overview) where shared components apply. Read this overview before servicing any coil or plug to understand the firing-order and circuit layout.

# Safety Precautions and Diagnostic Tools

Disconnect the battery and allow the ignition coils to discharge before handling primary or secondary circuits. Use an insulated spark tester and a calibrated torque wrench when servicing coils and plugs. When ignition diagnosis overlaps with cabin electrical work, reference the [Heron Hvac Service Manual](doc://man-heron-hvac) for shared connector locations.

# Ignition Coils

The Heron uses coil-on-plug ignition with several application-specific part numbers, including IC-2042-A, IC-2042-B, IC-2044-A, and IC-2050-A. Coil selection depends on engine variant and model year, and supersession rules must be observed. A weak or shorted coil is a leading cause of misfire codes.

## Coil Identification and Supersession

The original coil IC-2042-A has been superseded by the revised IC-2042-B, which features an updated potting compound and connector. When replacing one coil in a bank, inspect the remaining coils for the same revision level. Supersession history for the equivalent part is documented in the [Marlin EV Ignition Service Manual :: Coil Part Supersession Notes](doc://man-marlin-ev-ignition#ignition-coil-sub-system/coil-part-supersession-notes).

## Application-Specific Coils

Higher-output Heron variants use coil IC-2044-A, while the turbocharged application requires the high-energy IC-2050-A coil. Do not interchange these across applications, as the primary resistance and dwell calibration differ. See the [Marlin EV Ignition Service Manual :: Ignition Coil Sub-System](doc://man-marlin-ev-ignition#ignition-coil-sub-system) for the cross-reference table.

## Ignition Coil Replacement Procedure

Follow procedure PROC-IGN-COIL to replace any coil-on-plug unit, releasing the connector lock before lifting the coil to avoid damaging the boot. Apply dielectric grease to the boot and torque the hold-down fastener to specification. The equivalent step list is provided in the [Marlin EV Ignition Service Manual :: Ignition Coil Replacement Procedure](doc://man-marlin-ev-ignition#ignition-coil-sub-system/ignition-coil-replacement-procedure).

# Spark Plugs

The Heron uses iridium spark plugs cataloged as SP-1108, SP-1110, and SP-1112 depending on engine variant. Correct heat range and gap are essential for reliable combustion and emissions compliance. Always verify the application before installation.

## Spark Plug Selection and Specifications

Plug SP-1108 is specified for the base engine, SP-1110 for the high-output variant, and SP-1112 for the turbocharged application. Gap the plugs only if the manufacturer permits, as pre-gapped iridium plugs are easily damaged. Match the plug to the engine code stamped on the cylinder head.

## Spark Plug Replacement Procedure

Procedure PROC-SPARK-PLUG requires removing the coils first and blowing debris from the plug wells before extraction. Apply anti-seize sparingly to the threads only where specified and torque to the published value to protect the aluminum head. A parallel procedure appears in the [Marlin EV Ignition Service Manual :: Spark Plug Replacement Procedure](doc://man-marlin-ev-ignition#spark-plug-sub-system/spark-plug-replacement-procedure).

# Glow Plug System (Diesel)

Diesel Heron variants use glow plug GP-1304 to preheat the combustion chamber for cold starts. A failed glow plug causes hard starting and white exhaust smoke until the engine reaches operating temperature. Glow plug control is monitored by the engine control module.

## Glow Plug Service

Test glow plug GP-1304 for resistance and current draw before replacement, and never force a seized plug, which can damage the cylinder head threads. Cycle the glow plug relay and confirm preheat function after installation. Additional diesel-specific notes are in the [Marlin EV Ignition Service Manual :: Glow Plug Sub-System](doc://man-marlin-ev-ignition#glow-plug-sub-system).

# Ignition Circuit Diagnosis

Ignition circuit faults set diagnostic trouble codes P0351 and P0352 among the coil-related range. Begin by checking power and ground at the coil connector and the integrity of the driver circuit from the control module. The complete DTC reference is mirrored in the [Marlin EV Ignition Service Manual :: Ignition Diagnostic Trouble Code Reference](doc://man-marlin-ev-ignition#diagnosis/ignition-diagnostic-trouble-code-reference).

## Coil Primary and Secondary Circuit Faults

Code P0351 indicates a fault in the ignition coil A primary or secondary circuit, while P0352 indicates the same fault on coil B. Swap a suspect coil to a known-good cylinder to determine whether the fault follows the coil or stays with the circuit. The full circuit test sequence is documented in the [Marlin EV Ignition Service Manual :: Ignition Coil Circuit Diagnosis](doc://man-marlin-ev-ignition#diagnosis/ignition-coil-circuit-diagnosis).
