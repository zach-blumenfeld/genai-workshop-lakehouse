---
id: man-lumen-steering
title: Lumen Steering Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Lumen steering system. Always disable the supplemental restraint system and disconnect the battery negative terminal before servicing any steering column component. Wear eye protection when working near the steering rack hydraulic and electrical connections. For related cooling-circuit interactions during high-load steering assist, refer to the [Lumen Cooling Service Manual](doc://man-lumen-cooling).

# Steering System Overview

The Lumen steering system integrates the tie rod assembly TROD-8700, the steering rack RACK-8720, the electric power steering motor EPS-8740, and the steering angle sensor SAS-8760. These components work together to translate driver input at the wheel into precise road-wheel movement with electronic assist. The architecture is broadly similar to the Osprey platform; see the [Osprey Steering Service Manual](doc://man-osprey-steering) for cross-platform comparison.

## Steering Rack and Tie Rods

The steering rack RACK-8720 converts rotary steering input into linear motion transferred through the tie rods TROD-8700 to the steering knuckles. Inspect the rack boots for tearing and the tie rod ends TROD-8700 for excessive play before any alignment work. Worn tie rod ends are the most common cause of inner-edge tire wear on the Lumen.

## Electric Power Steering Motor

The electric power steering motor EPS-8740 provides variable assist based on vehicle speed and torque sensor input. The motor draws high current under low-speed maneuvering, so verify the charging system voltage before condemning EPS-8740. A failed EPS-8740 torque sensor will set fault codes and disable assist.

## Steering Angle Sensor

The steering angle sensor SAS-8760 reports absolute wheel position to the EPS and stability control modules. SAS-8760 must be calibrated after any alignment or rack replacement. An uncalibrated SAS-8760 will produce centering and stability-control faults.

# Diagnostic Trouble Codes

This section lists the steering-related diagnostic trouble codes for the Lumen, including C1234 and C1556. Always clear codes and road test after repair to confirm the fault does not return. The Osprey platform shares these code definitions; see the [Osprey Steering Service Manual :: Diagnostic Trouble Codes](doc://man-osprey-steering#diagnostic-trouble-codes).

## Steering Angle Sensor Fault

DTC C1234 indicates a steering angle sensor fault originating in SAS-8760. This code commonly sets when the sensor loses calibration or its signal circuit is interrupted. Inspect the SAS-8760 connector and harness before replacement. Compare against the [Osprey Steering Service Manual :: C1234 Steering Angle Sensor Fault](doc://man-osprey-steering#diagnostic-trouble-codes/c1234-steering-angle-sensor-fault).

## EPS Torque Sensor Fault

DTC C1556 indicates an EPS torque sensor fault within the EPS-8740 motor assembly. When C1556 is active, power steering assist is reduced or disabled. The torque sensor is integral to EPS-8740 and is not serviced separately. Refer to the [Osprey Steering Service Manual :: C1556 EPS Torque Sensor Fault](doc://man-osprey-steering#diagnostic-trouble-codes/c1556-eps-torque-sensor-fault) for the equivalent Osprey procedure.

# Tie Rod Sub-System Service

This sub-system covers service of the tie rod assembly TROD-8700. Inspect both inner and outer tie rod ends for play and boot integrity. Replace TROD-8700 components in pairs where wear is suspected. The Osprey equivalent is documented in the [Osprey Steering Service Manual :: Tie Rod and Linkage Sub-System](doc://man-osprey-steering#tie-rod-and-linkage-sub-system).

## Tie Rod End Replacement Procedure

Procedure PROC-TIE-ROD covers replacement of the outer tie rod end on the TROD-8700 assembly. Mark the thread position before removal to preserve approximate toe and minimize realignment. After installing the new TROD-8700 end, a four-wheel alignment is mandatory. See the [Osprey Steering Service Manual :: Tie Rod End Replacement](doc://man-osprey-steering#tie-rod-and-linkage-sub-system/tie-rod-end-replacement) for torque values on the locknut.

# Electric Power Steering Sub-System Service

This sub-system covers service of the EPS-8740 motor and the SAS-8760 steering angle sensor, including diagnosis of codes C1234 and C1556. Always verify battery and charging system health before diagnosing EPS faults. Both C1234 and C1556 require a SAS-8760 calibration after any repair.

## Electric Power Steering Diagnosis Procedure

Procedure PROC-EPS-DIAG guides diagnosis of the EPS-8740 motor and SAS-8760 sensor when C1234 or C1556 is stored. Begin by checking supply voltage and ground integrity at the EPS-8740 connector, then verify SAS-8760 calibration status with a scan tool. If C1556 persists with good power and ground, replace the EPS-8740 assembly. The parallel Osprey routine is the [Osprey Steering Service Manual :: Electric Power Steering Diagnosis](doc://man-osprey-steering#electric-power-steering-sub-system/electric-power-steering-diagnosis).

# Wheel Alignment Sub-System Service

Wheel alignment service ties together the tie rods TROD-8700, the steering rack RACK-8720, and the steering angle sensor SAS-8760. Alignment must be performed whenever TROD-8700 or RACK-8720 is disturbed. After alignment, recalibrate SAS-8760 to restore correct steering-center reporting.

## Four-Wheel Alignment Procedure

Procedure PROC-ALIGN sets caster, camber, and toe across all four wheels, adjusting toe through the TROD-8700 tie rods. On completion, perform a SAS-8760 zero-point calibration so the angle sensor agrees with the new mechanical center. Refer to the [Osprey Steering Service Manual :: Wheel Alignment](doc://man-osprey-steering#wheel-alignment) for platform-specific specifications.

# Torque Specifications and Reference

This section consolidates fastener torque values and reference data for the Lumen steering system. Always use the listed values and replace any single-use fasteners during reassembly. Apply thread-locking compound only where specified.
