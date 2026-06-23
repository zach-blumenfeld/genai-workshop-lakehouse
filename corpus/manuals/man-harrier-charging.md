---
id: man-harrier-charging
title: Harrier Charging Service Manual
area: manuals
---

# Charging System Overview

The Harrier charging system maintains battery state of charge and supplies regulated voltage to the vehicle electrical loads during all operating conditions. The system comprises the battery, the alternator with integrated generator control, and the starter motor, each managed by the powertrain control module over the serial data bus. For comparable architecture on a related platform, refer to the [Falcon Charging Service Manual :: Charging System Overview](doc://man-falcon-charging#charging-system-overview). Thermal management of the engine bay affects charging component longevity, as covered in the [Harrier Cooling Service Manual](doc://man-harrier-cooling).

# System Diagnosis

System diagnosis begins with retrieving stored diagnostic trouble codes and verifying the condition with a calibrated charging system analyzer. The most common codes are P0562 (System Voltage Low), P0563 (System Voltage High), and P0620 (Generator Control Circuit). Always complete the full diagnostic flow defined in procedure PROC-CHG-DIAG before condemning any component. A parallel code reference is available in the [Falcon Charging Service Manual :: Diagnostic Trouble Codes](doc://man-falcon-charging#diagnostic-trouble-codes).

## Reading Charging System Fault Codes

Connect the scan tool to the data link connector and record all freeze-frame data before clearing any code. P0562 indicates measured system voltage below the calibrated threshold for the engine-running condition, while P0563 indicates voltage above the upper threshold. P0620 is set when the control module detects an electrical fault in the generator control circuit itself. For cross-platform interpretation of these voltage codes, see the [Falcon Charging Service Manual :: System Voltage Codes](doc://man-falcon-charging#diagnostic-trouble-codes/system-voltage-codes).

## Charging System Diagnostic Procedure

Procedure PROC-CHG-DIAG verifies battery state, drive belt tension, charging output, and generator control circuit integrity in sequence. Confirm that P0620 is not caused by an open or shorted control wire before replacing the alternator, as a circuit fault will mimic a failed generator. Measure voltage drop across the main charging cable under load and compare against specification. The equivalent flow for the related platform is the [Falcon Charging Service Manual :: Charging System Diagnosis Procedure](doc://man-falcon-charging#charging-system-diagnosis-sub-system/charging-system-diagnosis-procedure).

# Battery Sub-System

The battery sub-system stores electrical energy and provides cranking current to the starter motor. The Harrier uses an absorbed glass mat battery sized to the vehicle electrical load profile. Refer to the [Falcon Charging Service Manual :: Battery](doc://man-falcon-charging#charging-system-overview/battery) for the comparable component on the Falcon platform.

## Battery Specifications and Identification

The standard service battery is part number BAT-1200, an 80 Ah AGM unit rated at 760 cold cranking amps. The heavy-duty option is part number BAT-1210, a 95 Ah AGM unit rated at 850 cold cranking amps used on vehicles with extended electrical loads. Always match replacement capacity to the original equipment specification stamped on the case label. Confirm group size and terminal orientation before ordering.

## Low System Voltage Diagnosis

When P0562 is active, first load-test the battery to confirm it can hold charge under cranking demand. A weak or sulfated BAT-1200 will pull system voltage below threshold even with a functioning alternator, so verify open-circuit voltage and conductance before proceeding upstream. Inspect terminal corrosion and ground strap resistance, which commonly cause low-voltage faults. Recharge and retest before final diagnosis.

### Battery Replacement Procedure

Procedure PROC-BATT covers safe removal and installation of the battery with the ignition off and negative cable disconnected first. Install the correct unit, either BAT-1200 for standard applications or BAT-1210 for heavy-duty applications, and torque the terminal clamps to specification. Perform a battery state-of-charge registration with the scan tool so the charging strategy adapts to the new battery. Document the replacement and verify no codes return after a test drive.

# Alternator Sub-System

The alternator sub-system generates regulated AC current rectified to DC to power loads and recharge the battery. Generator control is managed by the control module through a dedicated circuit monitored for the P0620 fault. See the [Falcon Charging Service Manual :: Alternator](doc://man-falcon-charging#charging-system-overview/alternator) for the analogous component.

## Alternator Specifications and Application

The base alternator is part number ALT-8810, rated at 150 amps for standard electrical loads. The high-output alternator is part number ALT-8812, rated at 220 amps and fitted to vehicles equipped with towing or auxiliary power packages. Verify the application by the broadcast code before ordering a replacement. Both units share the same mounting interface but differ in pulley ratio.

## High System Voltage and Generator Control Diagnosis

When P0563 is active, the regulator within ALT-8810 or the generator control command may be driving output above the upper voltage threshold. Confirm the control module is commanding the correct setpoint and that P0620 is not also present, which would indicate a control circuit fault rather than a regulator failure. Measure regulated output at the battery with all accessories on and compare to specification. Refer to the [Falcon Charging Service Manual :: Generator Control Circuit Code](doc://man-falcon-charging#diagnostic-trouble-codes/generator-control-circuit-code) for related diagnosis.

### Alternator Replacement Procedure

Procedure PROC-ALT directs removal of the drive belt, electrical connectors, and mounting bolts to free the unit. Install the correct alternator, ALT-8810 for standard or ALT-8812 for high-output applications, and route the field and sense wiring to prevent chafing. Re-tension the drive belt to specification and verify charging output under load. Clear codes and confirm no recurrence after the repair.

# Starter Sub-System

The starter sub-system provides the cranking torque required to start the engine and draws its current directly from the battery. Proper battery condition is a prerequisite for reliable starter operation. The comparable component is documented in the [Falcon Charging Service Manual :: Starter Motor](doc://man-falcon-charging#charging-system-overview/starter-motor).

## Starter Motor Specifications

The service starter motor is part number STM-9300, a gear-reduction unit with an integrated solenoid sized for the engine displacement. Verify the engagement geometry and mounting flange match the original before installation. Inspect the ring gear teeth for damage whenever the starter is removed. Confirm the unit draws within the specified current range during a cranking test.

### Starter Motor Replacement Procedure

Procedure PROC-STARTER covers disconnecting the battery negative cable, removing the heat shield, and detaching the solenoid feed and control wires. Remove the mounting bolts and lower the STM-9300 from the bell housing, taking care not to damage adjacent wiring. Install the replacement, torque the mounting bolts to specification, and reconnect the wiring in the correct order. Perform a cranking test and verify smooth engagement before returning the vehicle.
