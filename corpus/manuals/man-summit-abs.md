---
id: man-summit-abs
title: Summit Abs Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and service of the Summit anti-lock braking system, including the control module, hydraulic pump, and wheel speed sensors. Always discharge any stored hydraulic pressure and disconnect the battery before opening the ABS hydraulic circuit. The base brake system must be confirmed sound before diagnosing ABS faults. Technicians may also reference the [Summit Fuel Service Manual](doc://man-summit-fuel) for shared electrical and grounding information.

# ABS System Overview

The Summit ABS comprises electronic brake control module EBCM-8100, ABS hydraulic pump assembly ABSP-8120, and front wheel speed sensors WSS-3300 and rear sensors WSS-3302. The EBCM monitors wheel speed inputs and modulates hydraulic pressure through the pump to prevent wheel lock. This architecture parallels the platform documented in the [Falcon Abs Service Manual](doc://man-falcon-abs). Verify all four sensor signals before suspecting the module or pump.

## Electronic Brake Control Module (EBCM)

Module EBCM-8100 processes wheel speed data and commands the hydraulic actuator during ABS events. An internal module fault typically sets C0265, indicating an EBCM relay or internal control circuit failure. Do not replace EBCM-8100 before confirming power, ground, and communication integrity. Configuration data must be programmed after any EBCM-8100 replacement.

## ABS Hydraulic Pump Assembly

Pump assembly ABSP-8120 generates the pressure used to modulate the brakes during ABS activation. A pump motor circuit fault sets C0110 and disables ABS function while leaving base brakes operational. Inspect the pump motor connector and high-current feed before condemning ABSP-8120. Detailed pump service appears in the [Falcon Abs Service Manual :: ABS Hydraulic Pump Service](doc://man-falcon-abs#hydraulic-pump-sub-system/abs-hydraulic-pump-service).

## Wheel Speed Sensors

The Summit uses front sensors WSS-3300 and rear sensors WSS-3302, each reporting wheel speed to EBCM-8100. Open, shorted, or erratic signals set corner-specific codes C0035, C0040, C0045, and C0050. Inspect the sensor tip, tone ring, and connector for debris and corrosion. Related sensor guidance is provided in the [Falcon Abs Service Manual :: Wheel Speed Sensor Sub-System](doc://man-falcon-abs#wheel-speed-sensor-sub-system).

# Diagnostic Trouble Codes

The Summit ABS reports faults through chassis codes read with a compatible scan tool. The complete set spans wheel speed sensor codes C0035, C0040, C0045, and C0050, pump and relay codes C0110 and C0265, and configuration and communication codes C0561 and U0121. Always record freeze-frame data before clearing any code. The full definitions are mirrored in the [Falcon Abs Service Manual :: Diagnostic Trouble Codes](doc://man-falcon-abs#diagnostic-trouble-codes).

## Wheel Speed Sensor Circuit Codes

Codes C0035, C0040, C0045, and C0050 correspond to the left front, right front, left rear, and right rear wheel speed sensor circuits respectively. Diagnose each by inspecting the WSS-3300 or WSS-3302 sensor, harness, and tone ring for the affected corner. Compare live wheel speed data across all four sensors during a road test. Cross-reference the [Falcon Abs Service Manual :: Wheel Speed Sensor Codes](doc://man-falcon-abs#diagnostic-trouble-codes/wheel-speed-sensor-codes).

## Pump and Relay Circuit Codes

Code C0110 indicates an ABSP-8120 pump motor circuit fault, while C0265 indicates an EBCM-8100 relay or control circuit fault. Both codes disable ABS modulation until repaired. Verify the high-current supply and ground paths before replacing either component. See the [Falcon Abs Service Manual :: Pump and Relay Codes](doc://man-falcon-abs#diagnostic-trouble-codes/pump-and-relay-codes).

## System Configuration and Communication Codes

Code C0561 indicates the system is disabled pending valid configuration, commonly after an EBCM-8100 replacement without programming. Code U0121 indicates lost communication with the EBCM-8100 on the vehicle data bus. Check bus wiring and module power before suspecting an internal fault. Refer to the [Falcon Abs Service Manual :: Configuration and Communication Codes](doc://man-falcon-abs#diagnostic-trouble-codes/configuration-and-communication-codes).

# Wheel Speed Sensor Sub-System Service

Service of the wheel speed sensors covers front sensors WSS-3300 and rear sensors WSS-3302 and addresses codes C0035, C0040, C0045, and C0050. Each sensor reads the tone ring and must be mounted with the correct air gap and clean mating surface. Replace any sensor with damaged wiring or a cracked body. See the [Falcon Abs Service Manual :: Wheel Speed Sensor Sub-System](doc://man-falcon-abs#wheel-speed-sensor-sub-system) for shared service detail.

## Wheel Speed Sensor Replacement Procedure

Follow PROC-WSS to remove the affected sensor by disconnecting the harness, releasing the retaining bolt, and withdrawing WSS-3300 or WSS-3302 from its bore. Clean the mounting bore and tone ring of all debris before seating the new sensor fully. Torque the retainer and route the harness clear of rotating components, then clear codes and road test. The matching procedure is the [Falcon Abs Service Manual :: Wheel Speed Sensor Replacement](doc://man-falcon-abs#wheel-speed-sensor-sub-system/wheel-speed-sensor-replacement).

# EBCM and Hydraulic Sub-System Service

This sub-system covers module EBCM-8100 and pump ABSP-8120 and addresses codes C0110, C0265, and C0561. Both components form an integrated assembly on the Summit and are serviced together when internal faults are confirmed. Programming is mandatory after replacement. Related guidance appears in the [Falcon Abs Service Manual :: EBCM Control Module Sub-System](doc://man-falcon-abs#ebcm-control-module-sub-system).

## ABS Module Diagnosis Procedure

Follow PROC-ABS-DIAG to verify power and ground to EBCM-8100, confirm data-bus communication to resolve U0121, and test the pump circuit associated with C0110. Confirm C0265 by checking the EBCM relay supply, and resolve C0561 by completing configuration programming after any module replacement. Document all readings before and after repair. See the [Falcon Abs Service Manual :: ABS Module Diagnosis](doc://man-falcon-abs#ebcm-control-module-sub-system/abs-module-diagnosis).

# Torque Specifications and Reference

Torque all wheel speed sensor retainers, EBCM-8100 mounting fasteners, and ABSP-8120 hydraulic fittings to the values listed in the specification table. Use a calibrated torque wrench and replace any single-use fasteners. Always bleed the ABS hydraulic circuit after opening any line per the base brake bleeding sequence. Verify the brake warning lamps extinguish after a successful repair.
