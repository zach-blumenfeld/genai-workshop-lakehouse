---
id: man-falcon-charging
title: Falcon Charging Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Falcon charging and starting systems. Disconnect the battery negative terminal before servicing the alternator or starter to prevent arcing and short circuits. Wear eye and hand protection when handling battery electrolyte. For engine-driven accessory belt routing, refer to the [Falcon Engine Service Manual](doc://man-falcon-engine).

# Charging System Overview

The Falcon charging system comprises the battery BAT-1200 and its high-capacity variant BAT-1210, the alternator ALT-8810 and its heavy-duty variant ALT-8812, and the starter motor STM-9300. The alternator maintains system voltage and recharges the battery while the engine runs, and the starter draws from the battery to crank the engine. This architecture parallels the Harrier platform; see the [Harrier Charging Service Manual](doc://man-harrier-charging).

## Battery

The standard battery BAT-1200 and the high-capacity BAT-1210 supply cranking current and stabilize system voltage. Always match the replacement to the original part number, as BAT-1210 has higher reserve capacity than BAT-1200. Perform a conductance test before condemning either battery. Refer to the [Harrier Charging Service Manual :: Battery Specifications and Identification](doc://man-harrier-charging#battery-sub-system/battery-specifications-and-identification).

## Alternator

The alternator ALT-8810 and the heavy-duty ALT-8812 generate charging current under ECM regulation. ALT-8812 is fitted to vehicles with higher electrical loads and is not interchangeable with ALT-8810 without a connector adapter. Verify belt tension and the field control circuit before replacement. See the [Harrier Charging Service Manual :: Alternator Specifications and Application](doc://man-harrier-charging#alternator-sub-system/alternator-specifications-and-application).

## Starter Motor

The starter motor STM-9300 engages the flywheel ring gear to crank the engine on key-on. Inspect STM-9300 mounting bolts and the solenoid trigger circuit when diagnosing no-crank conditions. A weak BAT-1200 will mimic STM-9300 failure, so always confirm battery state first.

# Diagnostic Trouble Codes

This section covers the Falcon charging system codes P0562, P0563, and P0620. These codes report abnormal system voltage or a fault in the generator control circuit. Reading and interpreting these codes is the starting point for charging diagnosis; see the [Harrier Charging Service Manual :: Reading Charging System Fault Codes](doc://man-harrier-charging#system-diagnosis/reading-charging-system-fault-codes).

## System Voltage Codes

DTC P0562 indicates system voltage low and DTC P0563 indicates system voltage high. P0562 commonly results from a failing alternator or a discharged battery, while P0563 points to an overcharging condition or a regulator fault. Confirm the actual charging voltage at the battery posts before proceeding.

## Generator Control Circuit Code

DTC P0620 indicates a fault in the generator control circuit governing the alternator ALT-8810 or ALT-8812. Inspect the field control wiring and connector at the alternator before replacement. A P0620 with good wiring usually means the regulator inside ALT-8810 or ALT-8812 has failed.

# Charging System Diagnosis Sub-System

This sub-system integrates diagnosis of the battery BAT-1200 and BAT-1210, the alternator ALT-8810 and ALT-8812, and codes P0562, P0563, and P0620. Begin every charging complaint with a battery state-of-charge and conductance test. Then evaluate alternator output under load. The Harrier equivalent is the [Harrier Charging Service Manual :: System Diagnosis](doc://man-harrier-charging#system-diagnosis).

## Charging System Diagnosis Procedure

Procedure PROC-CHG-DIAG guides charging diagnosis when P0562, P0563, or P0620 is stored. Measure resting voltage at BAT-1200, then start the engine and confirm ALT-8810 raises system voltage into the regulated range. If P0620 persists with good wiring, replace the alternator. See the [Harrier Charging Service Manual :: Charging System Diagnostic Procedure](doc://man-harrier-charging#system-diagnosis/charging-system-diagnostic-procedure).

# Battery Sub-System Service

This sub-system covers service of the battery BAT-1200 and the high-capacity BAT-1210. Always verify the application before fitting BAT-1210 in place of BAT-1200. Reset memory functions after disconnecting the battery. Low-voltage diagnosis is detailed in the [Harrier Charging Service Manual :: Low System Voltage Diagnosis](doc://man-harrier-charging#battery-sub-system/low-system-voltage-diagnosis).

## Battery Replacement Procedure

Procedure PROC-BATT covers removal and installation of BAT-1200 or BAT-1210. Disconnect the negative terminal first and reconnect it last to avoid shorting. Clean the terminals and apply protective grease before torquing the clamps. Refer to the [Harrier Charging Service Manual :: Battery Replacement Procedure](doc://man-harrier-charging#battery-sub-system/low-system-voltage-diagnosis/battery-replacement-procedure).

# Alternator Sub-System Service

This sub-system covers service of the alternator ALT-8810 and ALT-8812, including diagnosis of code P0620. Confirm belt condition and field control wiring before removing the alternator. ALT-8812 requires verifying the higher-rated charging circuit on equipped vehicles.

## Alternator Replacement Procedure

Procedure PROC-ALT covers removal and installation of ALT-8810 or ALT-8812. Relieve belt tension with the automatic tensioner before slipping the belt off the pulley. After installing ALT-8810 or ALT-8812, verify regulated output voltage at idle and under load.

# Starter Sub-System Service

This sub-system covers service of the starter motor STM-9300. Verify battery state of charge and cable integrity before diagnosing STM-9300. A high-resistance ground will cause slow cranking that mimics a worn starter.

## Starter Motor Replacement Procedure

Procedure PROC-STARTER covers removal and installation of STM-9300. Disconnect the battery and the starter solenoid B+ lead before removing the mounting bolts. Torque the STM-9300 mounting bolts to specification and confirm reliable engagement after installation.

# Torque Specifications and Reference

This section consolidates fastener torque values and reference data for the Falcon charging and starting systems. Use the listed values for battery clamps, alternator mounts, and starter bolts. Replace single-use fasteners during reassembly.
