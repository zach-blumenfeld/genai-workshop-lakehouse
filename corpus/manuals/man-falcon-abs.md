---
id: man-falcon-abs
title: Falcon Abs Service Manual
area: manuals
---

# ABS System Overview

The Falcon anti-lock braking system prevents wheel lockup during hard braking by modulating hydraulic pressure at each corner. Core components include four wheel speed sensors, the Electronic Brake Control Module (EBCM-8100), and the ABS hydraulic pump assembly (ABSP-8120). The architecture closely parallels the platform-shared design documented in the [Summit Abs Service Manual :: ABS System Overview](doc://man-summit-abs#abs-system-overview). Brake fluid pressure and electrical control are tightly coupled, so accurate diagnosis depends on reading live sensor data before any component is replaced.

# Safety and Service Precautions

Always depressurize the hydraulic accumulator and disconnect the 12V battery before opening any ABS hydraulic line. Brake fluid is corrosive to paint and damages electrical connectors, so cap all open ports immediately. Engine bay routing of brake and electrical lines is shared with components covered in the [Falcon Engine Service Manual](doc://man-falcon-engine), so verify clearances after reassembly. Never road-test a vehicle until the EBCM has completed its self-test and the ABS warning lamp has extinguished.

# Diagnostic Trouble Codes

The Falcon EBCM stores faults that fall into wheel speed, pump and relay, and configuration or communication categories. Wheel speed sensor circuit faults are reported as C0035, C0040, C0045, and C0050, one per corner. Pump and relay faults appear as C0110 and C0265, while configuration and network faults are stored as C0561 and U0121. Cross-reference equivalent platform codes in the [Summit Abs Service Manual :: Diagnostic Trouble Codes](doc://man-summit-abs#diagnostic-trouble-codes) when diagnosing a shared chassis.

## Wheel Speed Sensor Codes

Codes C0035, C0040, C0045, and C0050 map to the left front, right front, left rear, and right rear wheel speed sensor circuits respectively. An open or shorted sensor circuit, excessive air gap, or a damaged tone ring will set one of these codes and disable ABS function. Compare the diagnostic flow against the [Summit Abs Service Manual :: Wheel Speed Sensor Circuit Codes](doc://man-summit-abs#diagnostic-trouble-codes/wheel-speed-sensor-circuit-codes) before condemning a sensor. Always inspect the harness and connector for corrosion before replacing the sensor itself.

## Pump and Relay Codes

Code C0110 indicates a pump motor circuit malfunction in the ABS hydraulic pump assembly ABSP-8120, while C0265 indicates an EBCM relay or motor control fault. A seized pump motor or a failed relay driver inside the EBCM is the most common cause. Refer to the [Summit Abs Service Manual :: Pump and Relay Circuit Codes](doc://man-summit-abs#diagnostic-trouble-codes/pump-and-relay-circuit-codes) for the comparable test sequence. Verify pump motor current draw before replacing ABSP-8120.

## Configuration and Communication Codes

Code C0561 indicates the system is disabled due to an invalid configuration or a fault reported by another module, and U0121 indicates lost communication with the ABS/EBCM over the network. These codes frequently appear together after a module replacement that was not properly programmed. Consult the [Summit Abs Service Manual :: System Configuration and Communication Codes](doc://man-summit-abs#diagnostic-trouble-codes/system-configuration-and-communication-codes) for the matching reconfiguration steps. Clear all related modules and re-run the network self-test after correcting the root cause.

# Wheel Speed Sensor Sub-System

The Falcon uses active Hall-effect wheel speed sensors carrying part numbers WSS-3300 for the front axle and WSS-3302 for the rear axle. Each sensor reads a toothed reluctor ring pressed onto the hub and reports rotational speed to the EBCM. The front WSS-3300 and rear WSS-3302 are not interchangeable due to differing connector keying and cable lengths. Refer to the [Summit Abs Service Manual :: Wheel Speed Sensors](doc://man-summit-abs#abs-system-overview/wheel-speed-sensors) for platform sensor specifications.

## Wheel Speed Sensor Replacement

Follow procedure PROC-WSS to replace a faulty sensor after confirming a C0035 through C0050 code is current. Install the front WSS-3300 or rear WSS-3302 with a new mounting bolt torqued to specification and verify the air gap. The replacement sequence mirrors the [Summit Abs Service Manual :: Wheel Speed Sensor Replacement Procedure](doc://man-summit-abs#wheel-speed-sensor-sub-system-service/wheel-speed-sensor-replacement-procedure). After installation, clear codes and confirm a clean wheel speed signal at all four corners during a low-speed road test.

# EBCM Control Module Sub-System

The Electronic Brake Control Module EBCM-8100 is the central processor for the Falcon ABS, governing pump operation and valve actuation. A failed EBCM-8100 commonly sets C0265 for internal relay faults and C0561 when its stored configuration becomes invalid. The module shares its calibration architecture with the [Summit Abs Service Manual :: Electronic Brake Control Module (EBCM)](doc://man-summit-abs#abs-system-overview/electronic-brake-control-module-ebcm). Always document the existing configuration before replacing the module.

## ABS Module Diagnosis

Use procedure PROC-ABS-DIAG to confirm an EBCM-8100 fault, which begins by verifying power, ground, and network communication. A U0121 lost-communication code points to wiring or connector problems rather than the module itself, so test the network harness first. Only condemn EBCM-8100 after power, ground, and CAN integrity have all been confirmed good. Reprogram and reconfigure any replacement module before returning the vehicle to service.

# Hydraulic Pump Sub-System

The ABS hydraulic pump assembly ABSP-8120 generates the pressure used to modulate brake apply during an ABS event. A pump motor circuit fault stores C0110 and renders the system inoperative. The pump assembly shares servicing characteristics with the unit described in the [Summit Abs Service Manual :: ABS Hydraulic Pump Assembly](doc://man-summit-abs#abs-system-overview/abs-hydraulic-pump-assembly). Internal pump damage from contaminated brake fluid is a frequent cause of C0110.

## ABS Hydraulic Pump Service

Service of ABSP-8120 requires full depressurization and a clean work area to prevent fluid contamination. After installing a replacement ABSP-8120, bleed the system thoroughly and run the automated ABS bleed routine to purge air from the modulator. Internal pump faults are flagged with bulletin reference ABSP-8120 and a C0110 code. Confirm correct pump operation with a commanded self-test before releasing the vehicle.
