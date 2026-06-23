---
id: man-kestrel-electrical
title: Kestrel Electrical Service Manual
area: manuals
---

# Electrical System Overview

The Kestrel electrical system links the Engine Control Module ECM-9901, Body Control Module BCM-9920, and Transmission Control Module TCM-9940 over a CAN bus network. Power distribution flows through the underhood fuse box FUSE-9980 and the engine wiring harness HARN-9960. The overall architecture parallels the platform-shared design in the [Vega Electrical Service Manual :: Electrical System Overview](doc://man-vega-electrical#electrical-system-overview). A single network or power fault can affect multiple modules, so always diagnose the system as a whole.

# Safety and Service Precautions

Disconnect the 12V battery and wait for capacitors to discharge before opening the underhood fuse box FUSE-9980 or any module connector. Static-sensitive control modules require an ESD strap during handling to prevent damage. Emissions-related electrical components share routing documented in the [Kestrel Emissions Service Manual](doc://man-kestrel-emissions), so verify connector seating after service. Never probe a CAN bus circuit with a test light, as this can corrupt network communication.

# Diagnostic Trouble Codes

The Kestrel network stores lost-communication codes when a module stops responding on the CAN bus. The primary codes are U0100 for lost communication with the ECM/PCM, U0140 for lost communication with the BCM, and U0155 for lost communication with the instrument cluster. These codes typically point to wiring, connector, or power faults rather than the modules themselves. Cross-reference the platform equivalents in the [Vega Electrical Service Manual :: Network Communication Diagnostic Codes](doc://man-vega-electrical#network-communication-diagnostic-codes).

## U0100 Lost Communication with ECM/PCM

Code U0100 indicates that other modules have lost communication with the Engine Control Module ECM-9901 over the CAN bus. Causes include a loss of power or ground to ECM-9901, an open bus wire, or a failed module. Verify power and ground at ECM-9901 before condemning the module, and compare the flow against the [Vega Electrical Service Manual :: Lost Communication with ECM/PCM](doc://man-vega-electrical#network-communication-diagnostic-codes/lost-communication-with-ecm-pcm). A U0100 will often set companion codes in other modules.

## U0140 Lost Communication with BCM

Code U0140 indicates lost communication with the Body Control Module BCM-9920. The BCM is a gateway for many body and network functions, so a fault here can cascade across the vehicle. Check power, ground, and bus continuity at BCM-9920, then refer to the [Vega Electrical Service Manual :: Lost Communication with BCM and Cluster](doc://man-vega-electrical#network-communication-diagnostic-codes/lost-communication-with-bcm-and-cluster). A failed BCM-9920 should only be replaced after wiring is confirmed good.

## U0155 Lost Communication with Instrument Cluster

Code U0155 indicates lost communication with the instrument cluster over the CAN bus. Because the cluster shares the bus with the BCM, a U0155 frequently appears alongside U0140 when a common gateway fault exists. Inspect the cluster connector and the bus segment feeding it before replacing the cluster. The companion diagnosis is documented in the [Vega Electrical Service Manual :: Lost Communication with BCM and Cluster](doc://man-vega-electrical#network-communication-diagnostic-codes/lost-communication-with-bcm-and-cluster).

# Engine Control Module Sub-System

The Engine Control Module ECM-9901 manages fuel, ignition, and emissions and is a primary node on the CAN bus. A loss of communication with ECM-9901 sets U0100 and can disable engine operation. The module corresponds to the unit in the [Vega Electrical Service Manual :: Engine Control Module](doc://man-vega-electrical#electrical-system-overview/engine-control-module). Always verify power and ground integrity before condemning ECM-9901.

## ECM Software Flash Procedure

Use procedure PROC-ECM-FLASH to update or reprogram the ECM-9901 software after a confirmed calibration fault or module replacement. Maintain a stable battery voltage with a programming support power supply throughout the flash. An interrupted flash can brick ECM-9901, so never disconnect during programming. The procedure parallels the [Vega Electrical Service Manual :: ECM Software Update Procedure](doc://man-vega-electrical#ecm-sub-system-service/ecm-software-update-procedure).

# Body Control Module Sub-System

The Body Control Module BCM-9920 manages lighting, locks, and acts as a CAN gateway between network segments. A failed or unpowered BCM-9920 sets U0140 and can disrupt communication across the entire vehicle. The module corresponds to the unit in the [Vega Electrical Service Manual :: Body Control Module](doc://man-vega-electrical#electrical-system-overview/body-control-module). Confirm wiring and power before replacing BCM-9920.

## BCM Configuration Procedure

Use procedure PROC-BCM-CONFIG to program vehicle options and calibration into a replacement BCM-9920. The new BCM-9920 must be configured to match the vehicle build before body functions and network gateway operation will work correctly. Verify all body functions after configuration is complete. Clear any U0140 codes and re-run the network self-test after the procedure.

# Transmission Control Module Sub-System

The Transmission Control Module TCM-9940 governs shift scheduling and torque converter control and communicates over the CAN bus. The module corresponds to the unit in the [Vega Electrical Service Manual :: Transmission Control Module](doc://man-vega-electrical#electrical-system-overview/transmission-control-module). A loss of power or network communication to TCM-9940 can place the transmission in a limp-home mode. Verify power, ground, and bus integrity before condemning TCM-9940.

## TCM Service Notes

A replacement TCM-9940 generally requires a relearn of adaptive shift values after installation. Always perform the adaptive relearn on a road test so the TCM-9940 can recalibrate clutch fill and shift timing. Confirm there are no active network codes before beginning the relearn. Verify smooth shifting across all gears before returning the vehicle to service.

# Wiring, Fuse, and Network Sub-System

The Kestrel power and signal distribution relies on the engine wiring harness HARN-9960 and the underhood fuse box FUSE-9980. Chafed wiring or a corroded fuse box terminal is a frequent root cause of intermittent module faults. These components correspond to the assemblies in the [Vega Electrical Service Manual :: Wiring Harness and Fuse Box](doc://man-vega-electrical#electrical-system-overview/wiring-harness-and-fuse-box). Inspect both HARN-9960 and FUSE-9980 before condemning any control module.

## Engine Wiring Harness Service

Service of the engine wiring harness HARN-9960 requires careful inspection of every connector for backed-out terminals, corrosion, and chafe points. Repair damaged circuits with sealed splices and protect the repair with proper loom. A wiring fault in HARN-9960 can mimic a failed module by causing intermittent communication loss. Always perform a wiggle test on HARN-9960 while monitoring live data.

## Underhood Fuse Box Service

The underhood fuse box FUSE-9980 distributes battery power to modules, relays, and high-current circuits. Inspect FUSE-9980 for blown fuses, melted terminals, and water intrusion that can cause module power loss. A corroded power feed in FUSE-9980 can set multiple lost-communication codes simultaneously. Replace damaged fuse box terminals rather than over-crimping existing ones.

## CAN Bus Network Communication Diagnosis

Use procedure PROC-COMMS-DIAG to isolate network faults when U0100, U0140, or U0155 are stored together. The procedure measures bus voltage and resistance to locate opens, shorts, or a module that is dragging down the network. Identify which module dropped off the bus first to find the root cause. Confirm all modules report present on the network after repairs and clear all communication codes.
