---
id: man-osprey-transmission
title: Osprey Transmission Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis, service, and component replacement for the Osprey automatic transmission. Always observe lift safety, allow the transmission to cool before draining fluid, and disconnect the battery negative terminal before any electrical work on the transmission control system. Related driveline interactions affecting steering geometry are documented in the [Osprey Steering Service Manual](doc://man-osprey-steering), and fuel-system interlocks are covered in the [Osprey Fuel Service Manual](doc://man-osprey-fuel). Read each procedure fully before beginning work.

# Transmission System Overview

The Osprey transmission integrates the fluid and filter assembly TFLT-9500, the shift solenoid pack TSOL-9520, the transmission mount TMNT-9540, and the friction clutch assembly CLU-9560. These four sub-systems work together to manage line pressure, gear selection, isolation, and torque transfer. The architecture closely parallels the platform-shared design described in the [Summit Transmission Service Manual](doc://man-summit-transmission), which uses equivalent solenoid and filter components. Use this overview to identify which sub-system section applies to the symptom you are diagnosing.

# Diagnosis

Begin transmission diagnosis by retrieving stored trouble codes, which commonly include P0700, P0741, and P0868. Follow the structured workflow defined in procedure PROC-TRANS-DIAG to avoid replacing parts unnecessarily. The diagnostic sequence and code definitions align with the corresponding section in the [Summit Transmission Service Manual :: Transmission Diagnosis](doc://man-summit-transmission#transmission-diagnosis). Confirm the customer concern before clearing any codes.

## Diagnostic Trouble Code Reference

Code P0700 indicates a transmission control system malfunction request and is typically accompanied by a more specific code. Code P0741 identifies torque converter clutch circuit performance or stuck-off condition, while P0868 reports transmission fluid pressure low. For cross-platform code definitions and bit-level descriptions, refer to the [Summit Transmission Service Manual :: Transmission Control System Fault Codes](doc://man-summit-transmission#transmission-diagnosis/transmission-control-system-fault-codes). Record all freeze-frame data before proceeding.

## Transmission Fault Diagnosis Procedure

Procedure PROC-TRANS-DIAG directs the technician through a sequential check of harness continuity, control module inputs, and mechanical pressure before component replacement. When P0700 is the only code present, scan associated modules for the underlying fault that triggered the request. The equivalent step-by-step flow is mirrored in the [Summit Transmission Service Manual :: Transmission Fault Diagnostic Procedure](doc://man-summit-transmission#transmission-diagnosis/transmission-fault-diagnostic-procedure). Do not skip the continuity verification step.

## Fluid Pressure Diagnosis

A P0868 low-pressure code requires connecting a mechanical gauge to the line pressure tap and comparing readings against specification. Low pressure combined with P0741 often points to internal leakage or a degraded torque converter clutch apply circuit. Compare your measured values against the platform baseline in the [Summit Transmission Service Manual :: Fluid Pressure Diagnosis](doc://man-summit-transmission#transmission-diagnosis/fluid-pressure-diagnosis). Verify fluid level and condition before concluding a pressure fault.

# Fluid and Filter Sub-System

The fluid and filter assembly TFLT-9500 maintains hydraulic cleanliness and correct fluid volume for proper line pressure. Service this sub-system using procedure PROC-TRANS-SERVICE at the specified interval or whenever contamination is suspected. Component interchange and capacity data are shared with the [Summit Transmission Service Manual :: Fluid and Filter Sub-System](doc://man-summit-transmission#fluid-and-filter-sub-system). Always use the specified fluid type.

## Transmission Fluid and Filter Service Procedure

Procedure PROC-TRANS-SERVICE describes draining, dropping the pan, replacing the TFLT-9500 filter element, and refilling to the correct level. Torque the pan bolts in the sequence given in the specifications section to prevent leaks. The detailed fill-and-check steps match those in the [Summit Transmission Service Manual :: Transmission Fluid and Filter Service Procedure](doc://man-summit-transmission#fluid-and-filter-sub-system/fluid-and-filter-specifications/transmission-fluid-and-filter-service-procedure). Dispose of used fluid according to local regulations.

## Fluid Level and Condition Inspection

Inspect TFLT-9500 fluid for color, odor, and metallic particulate at every service. Dark or burnt fluid combined with a stored P0868 may indicate pump wear or internal pressure loss. Refer to the shared filter and capacity specifications in the [Summit Transmission Service Manual :: Fluid and Filter Specifications](doc://man-summit-transmission#fluid-and-filter-sub-system/fluid-and-filter-specifications). Correct fluid level before any further diagnosis.

# Shift Control Sub-System

The shift solenoid pack TSOL-9520 controls gear selection and torque converter clutch apply through pulse-width modulated signals. Electrical faults in this circuit frequently set P0741. Replace the pack using procedure PROC-SHIFT-SOL when commanded states do not match observed gear engagement. The control strategy parallels the [Summit Transmission Service Manual :: Shift Solenoid Sub-System](doc://man-summit-transmission#shift-solenoid-sub-system).

## Shift Solenoid Pack Replacement Procedure

Procedure PROC-SHIFT-SOL covers lowering the pan, disconnecting the internal harness, and removing the TSOL-9520 solenoid pack. Verify connector pin condition before installing the replacement and recheck resistance against specification. Always relearn adaptive shift values after installation. Refer to the platform torque values in the specifications section.

## Torque Converter Clutch Diagnosis

A P0741 code reflects torque converter clutch slip or circuit performance, often traced to the TSOL-9520 apply solenoid. Verify electrical command, line pressure, and converter condition before condemning the converter. Use the combined solenoid and converter checks in the [Summit Transmission Service Manual :: Solenoid and Torque Converter Clutch Diagnosis](doc://man-summit-transmission#shift-solenoid-sub-system/solenoid-and-torque-converter-clutch-diagnosis). Confirm fluid pressure is within spec first.

# Clutch Sub-System

The friction clutch assembly CLU-9560 transfers engine torque within the transmission and is subject to wear over the vehicle's service life. Symptoms of a failing CLU-9560 include slipping under load, harsh engagement, and elevated operating temperature. Inspect this assembly whenever internal contamination is found during fluid service.

## Clutch Inspection and Replacement

Inspect the CLU-9560 friction surfaces for glazing, scoring, and material transfer during teardown. Replace the assembly if friction material thickness falls below the minimum listed in the specifications section. Always replace the clutch as a matched set and clean all hydraulic passages before reassembly.

# Transmission Mount Sub-System

The transmission mount TMNT-9540 isolates driveline vibration and maintains correct powertrain alignment. A collapsed or cracked TMNT-9540 mount causes clunking on shifts and excessive driveline movement. Inspect the mount during any major transmission service.

# Transmission Mount Replacement

Support the transmission with a jack before removing the TMNT-9540 mount fasteners. Replace the mount, then torque the fasteners to the values listed in the specifications section. Verify driveline alignment and clearance after installation.

# Specifications and Torque Values

This section lists fastener torque sequences, fluid capacities, and clearance tolerances for all Osprey transmission sub-systems. Always use a calibrated torque wrench and follow the specified tightening sequence. Refer back to the relevant procedure section for component-specific values.
