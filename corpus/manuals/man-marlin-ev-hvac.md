---
id: man-marlin-ev-hvac
title: Marlin EV Hvac Service Manual
area: manuals
---

# HVAC System Overview

The Marlin EV HVAC system provides cabin heating, cooling, and air distribution using an electrically driven compressor and a high-voltage heater core rather than engine waste heat. The system integrates the blower motor, refrigerant circuit, heater core, and cabin air filter under the control of the climate control module. For a comparable conventional architecture, refer to the [Heron Hvac Service Manual :: HVAC System Overview](doc://man-heron-hvac#hvac-system-overview). Brake-related thermal interactions are documented separately in the [Marlin EV Brakes Service Manual](doc://man-marlin-ev-brakes).

# HVAC System Diagnosis

Diagnosis begins by retrieving stored codes and confirming the customer concern with the climate control module live data. The two most common faults are B1352 (Blower Motor Circuit) and P0533 (A/C Refrigerant Pressure Sensor Circuit High). Always verify the condition before replacing a component, since wiring and connector faults frequently mimic component failures. A parallel code reference is available in the [Heron Hvac Service Manual :: Diagnostic Trouble Codes](doc://man-heron-hvac#diagnostic-trouble-codes).

## Blower Motor Circuit Fault Diagnosis

Code B1352 indicates the climate control module has detected an open, short, or out-of-range condition in the blower motor circuit. Inspect the connector at blower motor part number BLW-7200 for corrosion and backed-out terminals before condemning the motor itself. Command the blower through its full speed range with the scan tool and monitor current draw against specification. For the analogous diagnosis on the Heron platform, see the [Heron Hvac Service Manual :: Blower Motor Circuit Code](doc://man-heron-hvac#diagnostic-trouble-codes/blower-motor-circuit-code).

## Refrigerant Pressure Sensor Diagnosis

Code P0533 is set when the refrigerant pressure sensor signal reads higher than the expected range, often due to an overcharged system, sensor fault, or wiring issue. Verify static and operating pressures with manifold gauges before replacing the sensor mounted near A/C compressor part number ACMP-7220. Confirm the signal and reference voltages at the sensor connector. Refer to the [Heron Hvac Service Manual :: Refrigerant Pressure Sensor Code](doc://man-heron-hvac#diagnostic-trouble-codes/refrigerant-pressure-sensor-code) for related diagnosis.

# Air Conditioning Sub-System

The air conditioning sub-system circulates refrigerant through the compressor, condenser, expansion device, and evaporator to remove heat from the cabin. On the Marlin EV the compressor is electrically driven from the high-voltage bus and requires proper high-voltage safety procedures during service. Refer to the [Heron Hvac Service Manual :: A/C Compressor and Condenser](doc://man-heron-hvac#hvac-system-overview/a-c-compressor-and-condenser) for the comparable components.

## A/C Component Identification

The electric A/C compressor is part number ACMP-7220, a high-voltage scroll unit with an integrated inverter. The condenser is part number ACND-7240, a parallel-flow design mounted ahead of the cooling package. Verify both part numbers against the vehicle build before ordering, as the high-voltage compressor differs from conventional belt-driven units. Confirm refrigerant type and oil specification on the underhood label.

### A/C Evacuate and Recharge Procedure

Procedure PROC-AC-RECHARGE covers recovery, evacuation, and recharge of the refrigerant circuit using approved equipment. An overcharge condition is a frequent cause of P0533, so charge precisely to the specified mass and verify with calibrated scales. Hold vacuum to confirm the system is leak-free before introducing refrigerant. Compare to the [Heron Hvac Service Manual :: A/C Evacuate and Recharge Procedure](doc://man-heron-hvac#refrigerant-sub-system-service/a-c-evacuate-and-recharge-procedure) for the analogous flow.

### A/C Compressor Replacement Procedure

Procedure PROC-AC-COMP requires de-energizing and verifying the absence of high voltage before disconnecting compressor ACMP-7220. Recover refrigerant, disconnect the high-voltage connector and refrigerant lines, then remove the mounting bolts. Install the replacement with new sealing washers and the specified compressor oil charge. See the [Heron Hvac Service Manual :: A/C Compressor Replacement Procedure](doc://man-heron-hvac#refrigerant-sub-system-service/a-c-compressor-replacement-procedure) for comparable steps, then evacuate and recharge.

# Heating Sub-System

The heating sub-system delivers warm air to the cabin using a coolant loop heated by the high-voltage heater rather than engine heat. Proper bleeding of the coolant circuit is essential to avoid air pockets that reduce heater performance. Refer to the [Heron Hvac Service Manual :: Heater Core](doc://man-heron-hvac#hvac-system-overview/heater-core) for the comparable component.

## Heater Core Specifications

The service heater core is part number HCOR-7260, an aluminum core matched to the Marlin EV coolant loop and ducting. Inspect for coolant staining at the case seams and check inlet and outlet hose condition during service. Pressure-test the core when a leak is suspected before replacement. Confirm coolant specification and fill the loop following the bleed procedure.

# Air Distribution Sub-System

The air distribution sub-system moves conditioned air through the cabin using the blower motor and routes intake air through the cabin air filter. Restricted airflow is frequently traced to a clogged filter or a degraded blower motor. The comparable components appear in the [Heron Hvac Service Manual :: Blower Motor and Cabin Air Filter](doc://man-heron-hvac#hvac-system-overview/blower-motor-and-cabin-air-filter).

## Blower Motor Service

Service of blower motor part number BLW-7200 includes inspecting the wheel for debris and verifying smooth bearing rotation. A B1352 code accompanied by intermittent operation often points to a failing motor brush set or a high-resistance connector. Measure current draw across the speed range and compare to specification. Replace the motor if it is out of range or noisy.

### HVAC Blower Motor Replacement Procedure

Procedure PROC-BLOWER directs removal of the lower dash panel to access the blower motor housing. Disconnect the connector, release the retaining screws, and lower BLW-7200 from the housing without damaging the wheel. Install the replacement, reconnect the wiring, and verify operation at all speeds before reassembly. Confirm no B1352 code returns after the repair.

## Cabin Air Filter Service

The cabin air filter traps dust, pollen, and debris before air reaches the blower and evaporator. A restricted filter reduces airflow and can cause musty odors and reduced cooling capacity. Inspect filter part number CABF-7280 at the recommended service interval. Replace whenever airflow is reduced or the element is visibly soiled.

### Cabin Air Filter Replacement Procedure

Procedure PROC-CABIN-FILTER covers opening the glove box or access door to reach the filter housing. Note the airflow direction arrow on CABF-7280 and install the replacement in the correct orientation. Reseat the housing cover fully to prevent unfiltered air bypass. Verify restored airflow at the dash vents after installation.
