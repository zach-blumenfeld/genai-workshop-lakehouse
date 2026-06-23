---
id: man-marlin-ev-ignition
title: Marlin EV Ignition Service Manual
area: manuals
---

# Introduction and Safety

This manual covers the Marlin EV range-extender ignition system, including ignition coils, spark plugs, and the diesel-cycle glow plug sub-system. De-energize the high-voltage system and verify zero potential before servicing any ignition component near the traction battery. Disconnect the 12-volt battery negative terminal before removing coils or sensors. Read each procedure completely and observe all torque specifications.

# Ignition System Overview

The Marlin EV ignition system uses primary ignition coils IC-2042-A and its supersession IC-2042-B, the application-specific coils IC-2044-A and IC-2050-A, and spark plugs SP-1108, SP-1110, and SP-1112. The diesel-cycle range extender additionally uses glow plug GP-1304 for cold-start assistance. The coil and plug conventions parallel those in the [Heron Ignition Service Manual](doc://man-heron-ignition). Confirm the correct part number for the engine variant before ordering.

# Diagnosis

Begin ignition diagnosis by retrieving stored codes, most commonly P0351 and P0352. Confirm the customer concern and inspect connector condition before testing the coils. The diagnostic flow parallels the [Heron Ignition Service Manual :: Ignition Circuit Diagnosis](doc://man-heron-ignition#ignition-circuit-diagnosis). Record freeze-frame data before clearing any codes.

## Ignition Diagnostic Trouble Code Reference

Code P0351 indicates an ignition coil A primary or secondary circuit malfunction, while P0352 reports the same fault for ignition coil B. These codes commonly accompany a misfire and may point to a failed coil, harness, or driver circuit. For cross-platform definitions, refer to the [Heron Ignition Service Manual :: Coil Primary and Secondary Circuit Faults](doc://man-heron-ignition#ignition-circuit-diagnosis/coil-primary-and-secondary-circuit-faults). Record all stored codes before testing.

## Ignition Coil Circuit Diagnosis

When diagnosing P0351 or P0352, verify coil supply voltage, ground, and driver command before condemning the coil IC-2042-A or its replacement IC-2042-B. Swap the suspect coil to an adjacent cylinder to confirm whether the fault follows the coil. The test sequence aligns with the [Heron Ignition Service Manual :: Coil Primary and Secondary Circuit Faults](doc://man-heron-ignition#ignition-circuit-diagnosis/coil-primary-and-secondary-circuit-faults). Inspect the connector for corrosion before replacement.

# Ignition Coil Sub-System

The ignition coil sub-system covers the primary coil IC-2042-A and superseding IC-2042-B, plus the application-specific coils IC-2044-A and IC-2050-A. Replace coils using procedure PROC-IGN-COIL when a circuit fault or misfire is confirmed. Coil identification conventions match the [Heron Ignition Service Manual :: Ignition Coils](doc://man-heron-ignition#ignition-coils). Always confirm the correct application before ordering.

## Ignition Coil Replacement Procedure

Procedure PROC-IGN-COIL covers disconnecting the coil connector, removing the hold-down fastener, and extracting coil IC-2042-A, IC-2042-B, IC-2044-A, or IC-2050-A. Apply dielectric grease to the boot and seat the coil fully before securing. The detailed steps match the [Heron Ignition Service Manual :: Ignition Coil Replacement Procedure](doc://man-heron-ignition#ignition-coils/ignition-coil-replacement-procedure). Torque the hold-down to the value in the specifications section.

## Coil Part Supersession Notes

Coil IC-2042-A has been superseded by IC-2042-B, which carries an improved insulation jacket and is fully backward compatible. Always install IC-2042-B when servicing applications that originally specified IC-2042-A. Supersession and identification details are documented in the [Heron Ignition Service Manual :: Coil Identification and Supersession](doc://man-heron-ignition#ignition-coils/coil-identification-and-supersession). Application-specific variants are covered under [Heron Ignition Service Manual :: Application-Specific Coils](doc://man-heron-ignition#ignition-coils/application-specific-coils).

# Spark Plug Sub-System

The spark plug sub-system uses SP-1108, SP-1110, and SP-1112 depending on engine variant and heat range. Replace plugs using procedure PROC-SPARK-PLUG at the specified interval or when fouling is found. Plug selection conventions match the [Heron Ignition Service Manual :: Spark Plugs](doc://man-heron-ignition#spark-plugs). Confirm the correct heat range before installation.

## Spark Plug Replacement Procedure

Procedure PROC-SPARK-PLUG covers removing the coils, blowing out the plug wells, and extracting plugs SP-1108, SP-1110, or SP-1112. Gap each plug to specification and apply anti-seize sparingly to the threads. The steps and gap values align with the [Heron Ignition Service Manual :: Spark Plug Selection and Specifications](doc://man-heron-ignition#spark-plugs/spark-plug-selection-and-specifications) and the [Heron Ignition Service Manual :: Spark Plug Replacement Procedure](doc://man-heron-ignition#spark-plugs/spark-plug-replacement-procedure). Torque each plug to the specified value.

# Glow Plug Sub-System

The glow plug GP-1304 preheats the combustion chamber for reliable cold starting of the diesel-cycle range extender. A failed GP-1304 causes hard starting and white exhaust smoke when cold. Test glow plug resistance before replacement.

# Glow Plug Service

Replace the glow plug GP-1304 when resistance is out of specification or the plug fails to heat. Use the correct tool to avoid breaking the plug in the cylinder head. The service procedure parallels the [Heron Ignition Service Manual :: Glow Plug Service](doc://man-heron-ignition#glow-plug-system-diesel/glow-plug-service). Torque the GP-1304 to specification to prevent seizing.

# Specifications and Torque Values

This section lists coil hold-down torque, spark plug torque and gap, and glow plug torque values for the Marlin EV ignition system. Always use a calibrated torque wrench and confirm gap with a feeler gauge. Refer to the relevant procedure section for component-specific values.
