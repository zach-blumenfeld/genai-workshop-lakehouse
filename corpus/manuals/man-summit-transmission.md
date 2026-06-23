---
id: man-summit-transmission
title: Summit Transmission Service Manual
area: manuals
---

# Transmission System Overview

The Summit transmission system transfers engine torque to the driveline through a hydraulically controlled gearset managed by the transmission control module. The system comprises the fluid and filter circuit, the shift solenoid pack, the manual clutch, and the transmission mounts. For a comparable architecture on a related platform, refer to the [Osprey Transmission Service Manual :: Transmission System Overview](doc://man-osprey-transmission#transmission-system-overview). Brake interaction during downshifts is addressed in the [Summit Abs Service Manual](doc://man-summit-abs).

# Transmission Diagnosis

Diagnosis begins by retrieving stored codes and verifying fluid level and condition before any hydraulic testing. The most common codes are P0700 (Transmission Control System Malfunction), P0741 (Torque Converter Clutch Circuit Performance), and P0868 (Transmission Fluid Pressure Low). Always complete procedure PROC-TRANS-DIAG before disassembly. A parallel code reference is available in the [Osprey Transmission Service Manual :: Diagnostic Trouble Code Reference](doc://man-osprey-transmission#diagnosis/diagnostic-trouble-code-reference).

## Transmission Control System Fault Codes

Code P0700 is a general indicator that the transmission control module has set a fault and requests the malfunction indicator be illuminated; always read the accompanying subcodes. Code P0741 indicates the torque converter clutch is not achieving commanded slip, often from a worn clutch or solenoid fault. Code P0868 indicates measured line pressure below the calibrated threshold. Record freeze-frame data for all three before clearing.

## Transmission Fault Diagnostic Procedure

Procedure PROC-TRANS-DIAG verifies fluid condition, line pressure, solenoid resistance, and control circuit integrity in sequence. Because P0700 is a companion code, always retrieve and address the specific subcodes it points to rather than treating it alone. Perform a pressure test at the designated tap and compare to specification across gear ranges. The equivalent flow is the [Osprey Transmission Service Manual :: Transmission Fault Diagnosis Procedure](doc://man-osprey-transmission#diagnosis/transmission-fault-diagnosis-procedure).

## Fluid Pressure Diagnosis

When P0868 is active, low line pressure may result from low fluid level, a clogged filter, or a worn pump rather than an electronic fault. Inspect and verify the condition of fluid and filter assembly part number TFLT-9500 before condemning the pump. Connect a calibrated pressure gauge and record readings in each range. Refer to the [Osprey Transmission Service Manual :: Fluid Pressure Diagnosis](doc://man-osprey-transmission#diagnosis/fluid-pressure-diagnosis) for the analogous procedure.

# Fluid and Filter Sub-System

The fluid and filter sub-system supplies clean, properly leveled fluid to the hydraulic control circuit and lubricates the gearset. Degraded fluid or a restricted filter is a primary cause of pressure and shift-quality complaints. Refer to the [Osprey Transmission Service Manual :: Fluid and Filter Sub-System](doc://man-osprey-transmission#fluid-and-filter-sub-system) for the comparable system.

## Fluid and Filter Specifications

The service fluid and filter kit is part number TFLT-9500, which includes the filter element and pan gasket matched to the Summit transmission. Use only the specified fluid type and fill volume listed on the service label. Inspect the magnet in the pan for excessive ferrous debris during service. Confirm the correct kit by transmission family before ordering.

### Transmission Fluid and Filter Service Procedure

Procedure PROC-TRANS-SERVICE covers draining the fluid, removing the pan, and replacing filter kit TFLT-9500. A neglected filter is a frequent root cause of P0868, so always replace the element rather than reusing it. Install a new gasket, torque the pan bolts to specification, and refill to the correct level at operating temperature. Compare to the [Osprey Transmission Service Manual :: Transmission Fluid and Filter Service Procedure](doc://man-osprey-transmission#fluid-and-filter-sub-system/transmission-fluid-and-filter-service-procedure), then verify level per the [Osprey Transmission Service Manual :: Fluid Level and Condition Inspection](doc://man-osprey-transmission#fluid-and-filter-sub-system/fluid-level-and-condition-inspection).

# Shift Solenoid Sub-System

The shift solenoid sub-system directs hydraulic pressure to the appropriate clutches and bands to execute commanded gear changes. Solenoid faults commonly produce harsh shifts, slipping, or torque converter clutch codes. Refer to the [Osprey Transmission Service Manual :: Shift Control Sub-System](doc://man-osprey-transmission#shift-control-sub-system) for the comparable system.

## Solenoid and Torque Converter Clutch Diagnosis

When P0741 is active, the torque converter clutch is failing to lock or hold within commanded slip limits, often traced to the apply solenoid within shift solenoid pack part number TSOL-9520. Measure solenoid resistance and command the clutch apply with the scan tool while monitoring slip RPM. Verify line pressure is adequate, since a low-pressure condition can also produce slip. Replace the solenoid pack if it is out of specification.

### Shift Solenoid Pack Replacement Procedure

Procedure PROC-SHIFT-SOL directs draining the fluid, removing the pan, and detaching the wiring harness from solenoid pack TSOL-9520. Remove the retaining bolts and lower the pack, taking care not to damage the valve body mating surface. Install the replacement, torque the bolts to specification, and reconnect the harness. Clear codes and verify P0741 does not return after a road test, following the [Osprey Transmission Service Manual :: Shift Solenoid Pack Replacement Procedure](doc://man-osprey-transmission#shift-control-sub-system/shift-solenoid-pack-replacement-procedure).

# Clutch Sub-System

The clutch sub-system on manual-equipped Summit models couples and decouples engine torque from the transmission input shaft. Clutch wear produces slipping under load and difficulty engaging gears. The Osprey diagnosis flow in the [Osprey Transmission Service Manual :: Diagnosis](doc://man-osprey-transmission#diagnosis) covers comparable symptoms.

## Manual Clutch Specifications and Service

The service clutch kit is part number CLU-9560, which includes the disc, pressure plate, and release bearing. Inspect the flywheel surface for scoring and heat checking before installation. Measure free play and adjust the release mechanism to specification after installation. Confirm the correct kit by engine and transmission application before ordering.

# Transmission Mounting Sub-System

The transmission mounting sub-system isolates driveline vibration and locates the transmission relative to the engine and chassis. Worn mounts produce clunking on shifts and excessive driveline movement.

## Transmission Mount Inspection and Replacement

Inspect transmission mount part number TMNT-9540 for cracked, separated, or collapsed rubber and for fluid contamination that accelerates degradation. Support the transmission before removing the mount bolts, then replace TMNT-9540 with the correct unit for the application. Torque the through-bolts and bracket fasteners to specification. Verify driveline movement is within limits after installation.
