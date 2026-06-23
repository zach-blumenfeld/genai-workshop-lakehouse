---
id: man-harrier-abs
title: Harrier Abs Service Manual
area: manuals
---

# Introduction and Safety Precautions

This manual covers diagnosis and service of the Harrier anti-lock brake system. Always disconnect battery power before handling EBCM connectors and follow the prescribed depressurization steps when opening the hydraulic circuit. Use a factory-capable scan tool, as several procedures require module relearn after service. Related cooling-system cautions for shared underhood work are noted in the [Harrier Cooling Service Manual](doc://man-harrier-cooling), and the comparable architecture is documented in the [Summit Abs Service Manual](doc://man-summit-abs).

# ABS System Overview

The Harrier ABS uses front wheel speed sensors WSS-3300 and rear sensors WSS-3302 feeding the electronic brake control module EBCM-8100, which commands hydraulic pump assembly ABSP-8120 during an anti-lock event. The module monitors wheel behavior and modulates pressure to prevent lockup. The equivalent system layout is summarized in [Summit Abs Service Manual :: ABS System Overview](doc://man-summit-abs#abs-system-overview), with module detail in [Summit Abs Service Manual :: Electronic Brake Control Module (EBCM)](doc://man-summit-abs#abs-system-overview/electronic-brake-control-module-ebcm).

# Wheel Speed Sensor Subsystem

Front sensors WSS-3300 and rear sensors WSS-3302 report individual wheel rotation to the EBCM. Open or shorted sensor circuits set the corner-specific codes C0035, C0040, C0045, and C0050. Sensor architecture and supersession on the related platform is described in [Summit Abs Service Manual :: Wheel Speed Sensors](doc://man-summit-abs#abs-system-overview/wheel-speed-sensors).

## Front Wheel Speed Sensor Faults

DTC C0035 indicates a fault in the left front WSS-3300 circuit, while C0040 indicates the right front WSS-3300 circuit. Inspect the sensor connector, harness routing, and tone ring for debris before condemning the sensor. Air gap and signal integrity should be verified with a scope where available. The circuit-code reference for the related platform is [Summit Abs Service Manual :: Wheel Speed Sensor Circuit Codes](doc://man-summit-abs#diagnostic-trouble-codes/wheel-speed-sensor-circuit-codes).

## Rear Wheel Speed Sensor Faults

DTC C0045 indicates a fault in the left rear WSS-3302 circuit, and C0050 indicates the right rear WSS-3302 circuit. As with the front, inspect wiring and the tone ring before replacement, since corrosion at the connector is a frequent cause. Confirm the fault follows the sensor by swapping or back-probing. Diagnostic trouble codes for the comparable system are catalogued in [Summit Abs Service Manual :: Diagnostic Trouble Codes](doc://man-summit-abs#diagnostic-trouble-codes).

### Wheel Speed Sensor Replacement Procedure

Procedure PROC-WSS covers replacement of front sensor WSS-3300 or rear sensor WSS-3302. Remove the sensor mounting bolt, withdraw the sensor without prying on the tip, and clean the mounting bore of corrosion before fitting the new unit. Route the harness exactly as original to prevent chafing, then clear codes and verify a clean wheel speed signal on a road test. The platform-equivalent steps are in [Summit Abs Service Manual :: Wheel Speed Sensor Replacement Procedure](doc://man-summit-abs#wheel-speed-sensor-sub-system-service/wheel-speed-sensor-replacement-procedure).

# EBCM and Hydraulic Subsystem

Module EBCM-8100 controls pump assembly ABSP-8120 to modulate brake pressure during ABS activation. Pump motor faults set C0110, while EBCM relay faults set C0265. Pump and relay coverage for the related platform is in [Summit Abs Service Manual :: Pump and Relay Circuit Codes](doc://man-summit-abs#diagnostic-trouble-codes/pump-and-relay-circuit-codes).

## ABS Pump Motor Faults

DTC C0110 indicates a pump motor circuit fault in assembly ABSP-8120. Verify motor supply voltage, ground integrity, and EBCM-8100 motor drive before replacing the pump. A seized or high-resistance motor will commonly trigger C0110 during the self-test. Hydraulic pump detail for the comparable system is in [Summit Abs Service Manual :: ABS Hydraulic Pump Assembly](doc://man-summit-abs#abs-system-overview/abs-hydraulic-pump-assembly).

## EBCM Relay Faults

DTC C0265 indicates an EBCM-8100 relay circuit fault, often the internal valve relay or its supply. Check the module power and ground circuits and inspect for corrosion at the EBCM connector. C0265 frequently accompanies low system voltage, so confirm charging system health first.

# System Configuration and Communication

The EBCM relies on stored configuration and on the vehicle communication bus to coordinate with other modules. Configuration mismatches set C0561, while loss of communication sets U0121. Configuration and communication codes for the related platform are catalogued in [Summit Abs Service Manual :: System Configuration and Communication Codes](doc://man-summit-abs#diagnostic-trouble-codes/system-configuration-and-communication-codes).

## Configuration and ESP Faults

DTC C0561 indicates the EBCM has detected a system configuration fault or an inhibited ESP function. This commonly appears after module replacement without the required programming or after a related module reports a disabling condition. Resolve all other active faults, then perform the configuration relearn.

## Module Communication Loss

DTC U0121 indicates lost communication with the ABS/EBCM over the bus. Inspect the network wiring, connector pins, and module power before assuming a failed EBCM-8100. Confirm whether the fault is current or historic, as intermittent U0121 events often trace to a wiring or connector problem.

# ABS Module Diagnostics

Effective ABS diagnosis correlates the stored codes - C0035, C0040, C0045, C0050, C0110, C0265, C0561, and U0121 - with circuit testing rather than parts swapping. Start by confirming battery and ground integrity, since low voltage can produce several of these codes simultaneously. The platform-equivalent diagnostic flow is summarized in [Summit Abs Service Manual :: ABS System Overview](doc://man-summit-abs#abs-system-overview).

## ABS Module Diagnostic Procedure

Procedure PROC-ABS-DIAG sequences the technician through verifying power and ground, then addressing communication code U0121 and configuration code C0561 before chasing component codes such as pump fault C0110 or relay fault C0265. Resolve communication and configuration faults first, because they can mask or mimic downstream sensor and actuator codes. Document freeze-frame data, repair the identified circuit, and confirm all codes clear after a functional self-test.
