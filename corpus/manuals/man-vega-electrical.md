---
id: man-vega-electrical
title: Vega Electrical Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Vega electrical and network systems. Disconnect the battery negative terminal and wait for capacitor discharge before probing any control module connector. Never back-probe live CAN circuits with unprotected pins, as this can corrupt module communication. For brake-related electrical interactions, consult the [Vega Brakes Service Manual](doc://man-vega-brakes).

# Electrical System Overview

The Vega electrical system comprises the engine control module ECM-9901, the body control module BCM-9920, the transmission control module TCM-9940, the wiring harness HARN-9960, and the fuse box FUSE-9980. These modules communicate over a high-speed CAN bus carried through HARN-9960 and protected by FUSE-9980. The architecture mirrors the Kestrel platform documented in the [Kestrel Electrical Service Manual](doc://man-kestrel-electrical).

## Engine Control Module

The engine control module ECM-9901 governs fuel, ignition, and emissions and is the primary node on the powertrain CAN bus. ECM-9901 requires a software flash after replacement to match the vehicle calibration. A non-communicating ECM-9901 will set lost-communication codes across the network.

## Body Control Module

The body control module BCM-9920 manages lighting, locks, and the instrument cluster gateway. BCM-9920 must be configured to the vehicle option content after replacement. A failed BCM-9920 commonly disrupts cluster and comfort functions.

## Transmission Control Module

The transmission control module TCM-9940 controls shift scheduling and torque-converter clutch engagement. TCM-9940 shares wheel-speed and torque data with ECM-9901 over CAN. Adaptive shift values stored in TCM-9940 should be reset after major driveline repair. See the [Kestrel Electrical Service Manual :: TCM Service Notes](doc://man-kestrel-electrical#transmission-control-module-sub-system/tcm-service-notes) for the equivalent Kestrel guidance.

## Wiring Harness and Fuse Box

The main wiring harness HARN-9960 routes power, ground, and CAN circuits throughout the vehicle, with circuit protection in the fuse box FUSE-9980. Inspect HARN-9960 for chafing at body pass-throughs and verify FUSE-9980 fuse integrity before condemning any module. Most intermittent network faults trace to damaged HARN-9960 connectors or corroded FUSE-9980 terminals.

# Network Communication Diagnostic Codes

This section covers the Vega CAN network communication codes U0100, U0140, and U0155. These U-codes indicate lost communication between modules and are frequently caused by harness or power-supply faults rather than module failure. The Kestrel platform shares these definitions; see the [Kestrel Electrical Service Manual :: Diagnostic Trouble Codes](doc://man-kestrel-electrical#diagnostic-trouble-codes).

## Lost Communication with ECM/PCM

DTC U0100 indicates lost communication with the ECM/PCM, meaning other modules can no longer reach ECM-9901 on the bus. Check ECM-9901 power, ground, and CAN termination before replacing the module. Compare with the [Kestrel Electrical Service Manual :: U0100 Lost Communication with ECM/PCM](doc://man-kestrel-electrical#diagnostic-trouble-codes/u0100-lost-communication-with-ecm-pcm).

## Lost Communication with BCM and Cluster

DTC U0140 indicates lost communication with the body control module BCM-9920, while U0155 indicates lost communication with the instrument cluster. Both codes often set together when BCM-9920, acting as the cluster gateway, drops off the bus. Inspect BCM-9920 connectors and gateway power first. Refer to the [Kestrel Electrical Service Manual :: U0140 Lost Communication with BCM](doc://man-kestrel-electrical#diagnostic-trouble-codes/u0140-lost-communication-with-bcm) and the [Kestrel Electrical Service Manual :: U0155 Lost Communication with Instrument Cluster](doc://man-kestrel-electrical#diagnostic-trouble-codes/u0155-lost-communication-with-instrument-cluster).

# ECM Sub-System Service

This sub-system covers service of the engine control module ECM-9901 and diagnosis of code U0100. Always confirm power, ground, and CAN integrity at ECM-9901 before replacement. A stored U0100 with good supply circuits points to the module itself. The Kestrel equivalent is the [Kestrel Electrical Service Manual :: Engine Control Module Sub-System](doc://man-kestrel-electrical#engine-control-module-sub-system).

## ECM Software Update Procedure

Procedure PROC-ECM-FLASH covers reprogramming the ECM-9901 with current calibration software. Maintain a stable battery support voltage throughout the flash to avoid corrupting ECM-9901 memory. Verify the calibration ID after flashing. See the [Kestrel Electrical Service Manual :: ECM Software Flash Procedure](doc://man-kestrel-electrical#engine-control-module-sub-system/ecm-software-flash-procedure) for the comparable Kestrel routine.

# BCM Sub-System Service

This sub-system covers service of the body control module BCM-9920 and diagnosis of codes U0140 and U0155. Confirm BCM-9920 power and ground before suspecting the gateway. Both U0140 and U0155 require verifying the cluster CAN branch.

## Body Control Module Configuration Procedure

Procedure PROC-BCM-CONFIG configures a replacement BCM-9920 to the vehicle option content and VIN. The module will not exit limp behavior until configuration completes. After configuring BCM-9920, clear codes and confirm cluster communication. Refer to the [Kestrel Electrical Service Manual :: BCM Configuration Procedure](doc://man-kestrel-electrical#body-control-module-sub-system/bcm-configuration-procedure).

# Network and Harness Sub-System Service

This sub-system addresses the wiring harness HARN-9960 and fuse box FUSE-9980 in relation to communication codes U0100, U0140, and U0155. Most multi-module U-codes are caused by a shared open or short in HARN-9960 or a blown circuit in FUSE-9980. Inspect splice packs and grounds before condemning any module. The Kestrel BCM context is documented in the [Kestrel Electrical Service Manual :: Body Control Module Sub-System](doc://man-kestrel-electrical#body-control-module-sub-system).

## CAN Bus Communication Diagnosis Procedure

Procedure PROC-COMMS-DIAG isolates CAN bus faults in HARN-9960 when U0100, U0140, or U0155 is present. Measure bus resistance across the twisted pair and confirm both termination resistors are intact. Wiggle-test HARN-9960 connectors while monitoring for intermittent dropouts. The Kestrel TCM node is covered in the [Kestrel Electrical Service Manual :: Transmission Control Module Sub-System](doc://man-kestrel-electrical#transmission-control-module-sub-system).

# Wiring Diagrams and Reference

This section provides wiring diagrams and reference data for HARN-9960 and the fuse box FUSE-9980. Use the circuit identifiers to trace power, ground, and CAN paths. Confirm FUSE-9980 ratings before installing replacement fuses.
