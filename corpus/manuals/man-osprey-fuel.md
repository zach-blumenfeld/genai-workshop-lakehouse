---
id: man-osprey-fuel
title: Osprey Fuel Service Manual
area: manuals
---

# Introduction and Fuel System Overview

This manual covers the Osprey fuel system, including low-pressure delivery, high-pressure GDI delivery, injection, and pressure sensing. The Osprey fuel architecture is closely related to the Summit platform; refer to the [Summit Fuel Service Manual :: Fuel System Overview](doc://man-summit-fuel#fuel-system-overview) for shared component detail. Understanding the two-stage pressure system is essential before performing any fuel repair.

# Safety Precautions and Pressure Relief

The Osprey GDI system operates at high pressure, so always perform the documented pressure-relief procedure and allow residual pressure to bleed down before opening any fuel connection. Wear eye protection and keep an extinguisher nearby. When fuel work coincides with driveline service, see the [Osprey Transmission Service Manual](doc://man-osprey-transmission) for component clearances.

# Fuel Delivery

The Osprey uses an in-tank low-pressure pump FP-4100 feeding a cam-driven high-pressure pump HPFP-4120 on GDI applications, with fuel filtration provided by FF-4160. Adequate low-side pressure is a prerequisite for correct high-side operation. Always confirm low-pressure supply before condemning the high-pressure pump.

## Low-Pressure Fuel Pump

The low-pressure fuel pump FP-4100 is mounted in the fuel tank as part of the sending-unit assembly. Verify supply voltage and ground at the pump connector and measure static pressure before removal. Equivalent delivery testing is described in the [Summit Fuel Service Manual :: Fuel Delivery Sub-System](doc://man-summit-fuel#fuel-delivery-sub-system).

## High-Pressure Fuel Pump (GDI)

The high-pressure fuel pump HPFP-4120 is driven by a dedicated lobe on the camshaft and is sensitive to oil cleanliness at the follower. Always replace the cam follower and bucket when servicing the pump, and prime the low-pressure side before cranking. See the [Summit Fuel Service Manual :: High-Pressure Fuel Pump Service](doc://man-summit-fuel#fuel-delivery-sub-system/high-pressure-fuel-pump-service) for the torque sequence.

## Fuel Filter Service

The fuel filter FF-4160 should be replaced at the published interval or whenever fuel contamination is suspected. Relieve pressure before disconnecting the filter lines and observe the flow-direction arrow on installation. A parallel procedure is provided in the [Summit Fuel Service Manual :: Fuel Filter Service](doc://man-summit-fuel#fuel-delivery-sub-system/fuel-filter-service).

## Fuel Pump Replacement Procedure

Procedure PROC-FUEL-PUMP covers removal of both the low-pressure module and the high-pressure pump, beginning with system depressurization. Replace all sealing rings and confirm there are no leaks under operating pressure before returning the vehicle to service. The equivalent step list appears in the [Summit Fuel Service Manual :: Fuel Pump Replacement Procedure](doc://man-summit-fuel#fuel-delivery-sub-system/fuel-pump-replacement-procedure).

# Fuel Injection

The Osprey GDI system uses high-pressure injectors cataloged as INJ-4140, which are calibrated and coded to the engine control module. Carbon buildup and electrical faults are the most common injector failure modes. Injector coding must be updated after replacement.

## Injector Service

Inspect injector INJ-4140 for external leaks and measure resistance before condemning the unit. Always replace the combustion seal and Teflon tip seal when an injector is removed. Refer to the [Summit Fuel Service Manual :: Fuel Injection Sub-System](doc://man-summit-fuel#fuel-injection-sub-system) for spray-pattern criteria.

## Fuel Injector Replacement Procedure

Procedure PROC-INJECTOR requires depressurizing the rail and carefully extracting the injector to avoid damaging the bore. After installation, program the injector trim codes and verify smooth idle. The equivalent procedure is documented in the [Summit Fuel Service Manual :: Fuel Injector Replacement Procedure](doc://man-summit-fuel#fuel-injection-sub-system/fuel-injector-replacement-procedure).

# Fuel Rail and Pressure Sensing

The fuel rail pressure sensor FRS-4180 provides high-side pressure feedback to the control module for closed-loop pressure regulation. Inaccurate readings cause poor starting, hesitation, and pressure-related codes.

## Fuel Rail Pressure Sensor Replacement

Replace the fuel rail pressure sensor FRS-4180 when readings deviate from commanded pressure after confirming pump output. Relieve pressure before removal and torque the sensor to the specified value to ensure a leak-free seal. Clear codes and verify the live data stream after installation.

# Fuel System Diagnosis

Fuel system diagnosis addresses lean and rich codes (P0171, P0172), pressure and sensor codes (P0087, P0190), and injector circuit code P0201. Begin with fuel trims, then verify low- and high-side pressure against specification. The complete DTC table is mirrored in the [Summit Fuel Service Manual :: Fuel Diagnostic Trouble Code Reference](doc://man-summit-fuel#diagnosis/fuel-diagnostic-trouble-code-reference).

## Fuel Trim Faults (Lean/Rich)

Code P0171 indicates a system-too-lean condition while P0172 indicates system-too-rich; both require evaluation of fuel pressure, injector function, and intake integrity. Review long-term fuel trim across load ranges to distinguish a vacuum leak from a fuel-supply problem. Follow the [Summit Fuel Service Manual :: Fuel Trim and Pressure Diagnosis Procedure](doc://man-summit-fuel#diagnosis/fuel-trim-and-pressure-diagnosis-procedure) for the structured tree.

## Fuel Pressure and Sensor Faults

Code P0087 indicates fuel rail pressure too low, and P0190 indicates a fuel rail pressure sensor circuit fault. Confirm actual pressure with a mechanical gauge before deciding between a pump, regulator, or sensor cause. Inspect the sensor connector and wiring for corrosion.

## Injector Circuit Faults

Code P0201 indicates a fault in the cylinder 1 injector control circuit. Check the driver circuit continuity from the control module and the injector coil resistance. Swap connectors with an adjacent injector to determine whether the fault follows the injector or the harness.

## Fuel Trim and Pressure Diagnosis Procedure

Procedure PROC-FUEL-DIAG provides the master sequence for combining fuel-trim analysis with low- and high-side pressure testing. Record commanded versus actual rail pressure under load and compare against the published thresholds. Document all readings before parts replacement to avoid misdiagnosis.
