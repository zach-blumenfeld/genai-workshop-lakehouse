---
id: man-osprey-steering
title: Osprey Steering Service Manual
area: manuals
---

# Steering System Overview

The Osprey steering system combines a rack-and-pinion gear, electric power steering, and a steering angle sensor to deliver assisted, geometry-correct steering. The steering rack RACK-8720, tie rod ends TROD-8700, EPS motor EPS-8740, and steering angle sensor SAS-8760 work together as an integrated assembly. The architecture parallels the platform-shared design in the [Lumen Steering Service Manual :: Steering System Overview](doc://man-lumen-steering#steering-system-overview). Faults in any one component can disable or degrade power assist, so diagnose the system as a whole.

# Safety and Service Precautions

Disable the EPS system and disconnect the 12V battery before working on any steering electrical component. The steering angle sensor SAS-8760 and EPS torque sensor must be recalibrated after any service that disturbs the steering position. Electrical and fuel routing near the steering column is documented in the [Osprey Fuel Service Manual](doc://man-osprey-fuel), so verify clearances after reassembly. Never road-test the vehicle until the EPS warning lamp has extinguished and the steering angle is centered.

# Diagnostic Trouble Codes

The Osprey EPS module stores faults related to the steering angle sensor and the EPS torque sensor circuit. The two primary codes are C1234 for steering angle sensor faults and C1556 for EPS torque sensor faults. Both codes will reduce or disable power assist until the underlying fault is corrected. Cross-reference equivalent platform codes in the [Lumen Steering Service Manual :: Diagnostic Trouble Codes](doc://man-lumen-steering#diagnostic-trouble-codes).

## C1234 Steering Angle Sensor Fault

Code C1234 indicates an implausible or missing signal from the steering angle sensor SAS-8760. Causes include a failed sensor, a disturbed sensor calibration, or a wiring fault in the sensor circuit. Always perform the SAS-8760 calibration before condemning the sensor, and compare the diagnostic flow against the [Lumen Steering Service Manual :: Steering Angle Sensor Fault](doc://man-lumen-steering#diagnostic-trouble-codes/steering-angle-sensor-fault). A C1234 will commonly accompany ABS and stability faults due to the shared signal.

## C1556 EPS Torque Sensor Fault

Code C1556 indicates a fault in the EPS torque sensor integrated into the EPS-8740 assembly. A failed torque sensor causes loss of power assist and heavy steering effort. The torque sensor is not separately serviceable, so a confirmed C1556 requires replacement of the EPS-8740 unit. Refer to the [Lumen Steering Service Manual :: EPS Torque Sensor Fault](doc://man-lumen-steering#diagnostic-trouble-codes/eps-torque-sensor-fault) for the matching test sequence.

# Tie Rod and Linkage Sub-System

The Osprey tie rod end TROD-8700 connects the steering rack to the steering knuckle and sets the toe angle. A worn TROD-8700 produces play in the steering and uneven tire wear. The tie rod design corresponds to the unit in the [Lumen Steering Service Manual :: Steering Rack and Tie Rods](doc://man-lumen-steering#steering-system-overview/steering-rack-and-tie-rods). Inspect the ball joint and boot for play and damage before replacement.

## Tie Rod End Replacement

Use procedure PROC-TIE-ROD to replace the TROD-8700 after counting the threads to preserve the approximate toe setting. Separate the tie rod from the knuckle with a puller, then thread on the new TROD-8700 to the marked position. The procedure mirrors the [Lumen Steering Service Manual :: Tie Rod End Replacement Procedure](doc://man-lumen-steering#tie-rod-sub-system-service/tie-rod-end-replacement-procedure). A four-wheel alignment is mandatory after any tie rod replacement.

# Steering Rack Sub-System

The Osprey steering rack RACK-8720 converts the rotational input from the steering column into linear motion at the tie rods. A worn or leaking RACK-8720 causes steering play, fluid loss, or knocking over bumps. The rack assembly corresponds to the unit described in the [Lumen Steering Service Manual :: Steering Rack and Tie Rods](doc://man-lumen-steering#steering-system-overview/steering-rack-and-tie-rods). Inspect the rack boots for tears that allow contamination.

## Steering Rack Service

Service of RACK-8720 requires removing the tie rods and supporting the subframe before unbolting the rack. Install the replacement RACK-8720 and center it before connecting the steering column to preserve sensor calibration. Reconnect the tie rods to their marked positions to approximate the prior toe setting. A four-wheel alignment is required after any RACK-8720 replacement.

# Electric Power Steering Sub-System

The Osprey electric power steering relies on the EPS motor EPS-8740 and the steering angle sensor SAS-8760 to provide variable assist. A C1556 torque sensor fault or a C1234 steering angle fault will reduce or eliminate assist from the EPS-8740. The system architecture corresponds to the [Lumen Steering Service Manual :: Electric Power Steering Motor](doc://man-lumen-steering#steering-system-overview/electric-power-steering-motor). Both SAS-8760 calibration and EPS-8740 initialization are required after service.

## Electric Power Steering Diagnosis

Use procedure PROC-EPS-DIAG to diagnose EPS faults, beginning with power, ground, and network communication to the EPS-8740. Verify the SAS-8760 signal and calibration before condemning the motor assembly. The diagnostic flow parallels the [Lumen Steering Service Manual :: Electric Power Steering Sub-System Service](doc://man-lumen-steering#electric-power-steering-sub-system-service). Recalibrate the steering angle sensor and clear all codes after any EPS-8740 replacement.

# Wheel Alignment

Proper wheel alignment is essential after any steering or suspension service that affects toe, camber, or caster. Procedure PROC-ALIGN defines the full four-wheel alignment sequence for the Osprey platform. An out-of-spec alignment causes uneven tire wear and a steering pull. Verify ride height and tire condition before beginning PROC-ALIGN.

## Four-Wheel Alignment Procedure

Procedure PROC-ALIGN requires that all tie rod ends TROD-8700 and suspension bushings be in good condition before measurements are taken. Adjust toe at the tie rod sleeves and reset the steering angle sensor zero after the alignment is complete. Worn TROD-8700 components must be replaced before a meaningful alignment can be performed. Record the final alignment values and confirm the steering wheel is centered on a road test.
