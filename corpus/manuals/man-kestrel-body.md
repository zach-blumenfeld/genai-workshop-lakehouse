---
id: man-kestrel-body
title: Kestrel Body Service Manual
area: manuals
---

# Introduction and Safety

This manual covers the Kestrel body electrical sub-systems, including diagnosis and component replacement. Before servicing any module, disconnect the battery negative terminal and wait for capacitors to discharge to avoid airbag or module damage. Emissions-related body interlocks are documented in the [Kestrel Emissions Service Manual](doc://man-kestrel-emissions), and powertrain wiring shared with the body controller is covered in the [Kestrel Electrical Service Manual](doc://man-kestrel-electrical). Read each procedure completely before beginning.

# Body Electrical System Overview

The Kestrel body electrical system comprises the wiper motor WIPM-7000, the headlamp assembly HLMP-7020, the door mirror assembly DRMR-7040, and the windshield washer pump WSHLD-7060. These components are managed by the body control module across a multiplexed network. The architecture mirrors the heavy-duty platform described in the [Ridgeline HD Body Service Manual](doc://man-ridgeline-hd-body), which shares connector and module configuration conventions. Identify the affected sub-system before beginning diagnosis.

# Diagnosis

Begin body electrical diagnosis by retrieving stored codes, most commonly B1318 and B2477. Verify the customer concern and confirm battery state of charge before interpreting any module configuration faults. Code definitions and the diagnostic flow align with the [Ridgeline HD Body Service Manual :: Body System Diagnosis](doc://man-ridgeline-hd-body#body-system-diagnosis). Record freeze-frame data before clearing codes.

## Body Diagnostic Trouble Code Reference

Code B1318 indicates low battery voltage detected by the body control module, which can cause erratic module behavior and false faults. Code B2477 reports a module configuration failure, typically following a module replacement without proper programming. For cross-platform definitions of both codes, refer to the [Ridgeline HD Body Service Manual :: Body System Diagnosis](doc://man-ridgeline-hd-body#body-system-diagnosis). Always resolve B1318 before pursuing other codes.

## Low Battery Voltage Diagnosis

A B1318 code requires verifying battery state of health, charging system output, and ground integrity at the body control module. Low system voltage can latch additional codes that clear once supply is restored, so address B1318 first. The equivalent voltage-drop test sequence is detailed in the [Ridgeline HD Body Service Manual :: Low Battery Voltage Body Control Diagnosis](doc://man-ridgeline-hd-body#body-system-diagnosis/low-battery-voltage-body-control-diagnosis). Load-test the battery before condemning the module.

## Module Configuration Failure Diagnosis

A B2477 code points to a configuration or programming mismatch in the body control module. Confirm the correct calibration file and vehicle option content before reprogramming. The reconfiguration procedure parallels the [Ridgeline HD Body Service Manual :: Module Configuration Failure Diagnosis](doc://man-ridgeline-hd-body#body-system-diagnosis/module-configuration-failure-diagnosis). Verify a stable supply voltage before initiating any programming event.

# Lighting Sub-System

The headlamp assembly HLMP-7020 provides forward illumination and integrates with the body control module for automatic lighting functions. Replace the assembly using procedure PROC-HEADLAMP when lens damage, moisture intrusion, or internal failure is confirmed. Assembly identification and trim variants are cross-referenced in the [Ridgeline HD Body Service Manual :: Exterior Lighting Sub-System](doc://man-ridgeline-hd-body#exterior-lighting-sub-system). Confirm the correct part number for the vehicle's option package.

## Headlamp Assembly Replacement Procedure

Procedure PROC-HEADLAMP covers removing the fascia fasteners, disconnecting the HLMP-7020 connector, and extracting the assembly. Verify aim after installation and recheck automatic lighting operation. For headlamp variant identification before ordering, see the [Ridgeline HD Body Service Manual :: Headlamp Assembly Identification](doc://man-ridgeline-hd-body#exterior-lighting-sub-system/headlamp-assembly-identification). Torque all fasteners to the values in the specifications section.

# Wiper and Washer Sub-System

The wiper motor WIPM-7000 and the windshield washer pump WSHLD-7060 together provide glass clearing and washing functions. Service the wiper motor using procedure PROC-WIPER when intermittent or no-park operation is observed. The shared mechanism layout is documented in the [Ridgeline HD Body Service Manual :: Wiper and Washer Sub-System](doc://man-ridgeline-hd-body#wiper-and-washer-sub-system). Verify the park switch before replacing any component.

## Wiper Motor Replacement Procedure

Procedure PROC-WIPER covers removing the cowl, disconnecting the WIPM-7000 connector, and detaching the linkage. Index the motor to the park position before reconnecting the linkage to ensure correct blade sweep. The detailed steps match the [Ridgeline HD Body Service Manual :: Wiper Motor Replacement Procedure](doc://man-ridgeline-hd-body#wiper-and-washer-sub-system/wiper-motor-specifications/wiper-motor-replacement-procedure). Confirm motor specifications against the [Ridgeline HD Body Service Manual :: Wiper Motor Specifications](doc://man-ridgeline-hd-body#wiper-and-washer-sub-system/wiper-motor-specifications).

## Windshield Washer Pump Service

The washer pump WSHLD-7060 mounts to the reservoir and supplies fluid to the spray nozzles. Inspect for cracked seals and clogged inlet screens when flow is weak or absent. Prime the system after replacement and verify spray pattern at the windshield. Use the correct washer fluid for ambient conditions.

# Exterior Mirror Sub-System

The door mirror assembly DRMR-7040 houses the glass, actuator, and any integrated signal or camera modules. Inspect the DRMR-7040 wiring harness for chafing when power fold or heat functions fail. Confirm the correct variant before ordering a replacement.

# Door Mirror Assembly Replacement

Remove the interior door trim panel to access the DRMR-7040 mounting fasteners and connector. Transfer any integrated modules to the replacement assembly if not supplied. Calibrate power-fold and auto-dimming features after installation and torque fasteners to specification.

# Specifications and Torque Values

This section lists fastener torque values, electrical resistance ranges, and fluid specifications for all Kestrel body sub-systems. Always use a calibrated torque wrench and verify connector seating after any repair. Refer to the relevant procedure section for component-specific values.
