---
id: man-heron-hvac
title: Heron Hvac Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Heron HVAC system. Only certified technicians may recover and recharge refrigerant, and approved recovery equipment must be used at all times. Wear eye protection and gloves when working near pressurized refrigerant lines. For ignition-side interactions affecting blower power, refer to the [Heron Ignition Service Manual](doc://man-heron-ignition).

# HVAC System Overview

The Heron HVAC system comprises the blower motor BLW-7200, the A/C compressor ACMP-7220, the condenser ACND-7240, the heater core HCOR-7260, and the cabin air filter CABF-7280. These components manage cabin temperature, airflow, and air quality across heating and cooling modes. The system shares many components with the Marlin EV platform; see the [Marlin EV Hvac Service Manual](doc://man-marlin-ev-hvac).

## Blower Motor and Cabin Air Filter

The blower motor BLW-7200 drives cabin airflow through the duct system, drawing intake air through the cabin air filter CABF-7280. A clogged CABF-7280 restricts airflow and increases load on BLW-7200. Inspect and replace CABF-7280 at the recommended interval to protect the blower motor. For suspension-noise complaints often confused with blower noise, see the [Heron Suspension Service Manual](doc://man-heron-suspension).

## A/C Compressor and Condenser

The A/C compressor ACMP-7220 pressurizes refrigerant and circulates it to the condenser ACND-7240, where heat is rejected to ambient air. Verify ACMP-7220 clutch engagement and ACND-7240 airflow before condemning either component. A blocked ACND-7240 will cause high-side pressure faults. Refer to the [Marlin EV Hvac Service Manual :: A/C Component Identification](doc://man-marlin-ev-hvac#air-conditioning-sub-system/a-c-component-identification).

## Heater Core

The heater core HCOR-7260 transfers engine coolant heat to cabin air during heating mode. Inspect HCOR-7260 for coolant leaks and a sweet odor in the cabin. A plugged HCOR-7260 produces insufficient heat output. See the [Marlin EV Hvac Service Manual :: Heater Core Specifications](doc://man-marlin-ev-hvac#heating-sub-system/heater-core-specifications).

# Diagnostic Trouble Codes

This section covers the Heron HVAC codes B1352 and P0533. These codes identify blower circuit and refrigerant pressure sensor faults respectively. The Marlin EV platform shares these definitions; see the [Marlin EV Hvac Service Manual :: HVAC System Diagnosis](doc://man-marlin-ev-hvac#hvac-system-diagnosis).

## Blower Motor Circuit Code

DTC B1352 indicates a blower motor circuit fault in the BLW-7200 circuit. This code commonly sets from a failed blower motor, a damaged power module, or a corroded connector. Inspect the BLW-7200 connector and supply circuit before replacement. Refer to the [Marlin EV Hvac Service Manual :: Blower Motor Circuit Fault Diagnosis](doc://man-marlin-ev-hvac#hvac-system-diagnosis/blower-motor-circuit-fault-diagnosis).

## Refrigerant Pressure Sensor Code

DTC P0533 indicates an A/C refrigerant pressure sensor circuit high input near the ACMP-7220 high-side line. This code often results from a sensor fault or an overcharged system. Verify actual system pressures with manifold gauges before replacing the sensor. See the [Marlin EV Hvac Service Manual :: Refrigerant Pressure Sensor Diagnosis](doc://man-marlin-ev-hvac#hvac-system-diagnosis/refrigerant-pressure-sensor-diagnosis).

# Refrigerant Sub-System Service

This sub-system covers service of the A/C compressor ACMP-7220 and condenser ACND-7240, including diagnosis of code P0533. Always recover refrigerant before opening the sealed system. Confirm correct charge weight, as an overcharge will set P0533. The Marlin EV equivalent is the [Marlin EV Hvac Service Manual :: Air Conditioning Sub-System](doc://man-marlin-ev-hvac#air-conditioning-sub-system).

## A/C Evacuate and Recharge Procedure

Procedure PROC-AC-RECHARGE covers evacuating and recharging the system feeding ACMP-7220 and ACND-7240. Pull a deep vacuum and verify it holds before introducing the specified refrigerant charge. An incorrect charge will trigger P0533 and reduce cooling performance. Refer to the [Marlin EV Hvac Service Manual :: A/C Evacuate and Recharge Procedure](doc://man-marlin-ev-hvac#air-conditioning-sub-system/a-c-component-identification/a-c-evacuate-and-recharge-procedure).

## A/C Compressor Replacement Procedure

Procedure PROC-AC-COMP covers removal and installation of the A/C compressor ACMP-7220. Recover refrigerant and add the specified oil charge to the new ACMP-7220 before installation. Flush the system if the previous compressor failed internally. See the [Marlin EV Hvac Service Manual :: A/C Compressor Replacement Procedure](doc://man-marlin-ev-hvac#air-conditioning-sub-system/a-c-component-identification/a-c-compressor-replacement-procedure).

# Air Distribution Sub-System Service

This sub-system covers the blower motor BLW-7200 and cabin air filter CABF-7280, including diagnosis of code B1352. A restricted CABF-7280 increases blower load and can contribute to B1352 setting. Confirm filter condition before condemning the blower.

## HVAC Blower Motor Replacement Procedure

Procedure PROC-BLOWER covers removal and installation of the blower motor BLW-7200 when B1352 is confirmed. Disconnect the BLW-7200 connector and inspect for heat damage before fitting the new motor. Verify smooth operation across all speeds after replacement.

## Cabin Air Filter Replacement Procedure

Procedure PROC-CABIN-FILTER covers replacement of the cabin air filter CABF-7280. Note the airflow direction arrow on CABF-7280 during installation. Replacing CABF-7280 at the recommended interval protects the blower motor and maintains airflow.

# Heater Core Sub-System Service

This sub-system covers service of the heater core HCOR-7260. Drain the cooling system before disconnecting the HCOR-7260 hoses. Pressure-test HCOR-7260 after installation to confirm there are no coolant leaks into the cabin.

# Torque Specifications and Reference

This section consolidates fastener torque values and reference data for the Heron HVAC system. Use the listed values for compressor mounts, blower housing fasteners, and heater core retainers. Replace seals and O-rings during reassembly.
