---
id: man-falcon-fuel
title: Falcon Fuel Service Manual
area: manuals
---

# Introduction and Safety Precautions

This manual covers the Falcon fuel system, including delivery, injection, pressure sensing, and diagnostics. Because the system operates at high pressure, always relieve fuel pressure and disconnect the battery before opening any line. Wear eye protection and keep a Class B extinguisher nearby. Engine-side interactions are documented in the [Falcon Engine Service Manual](doc://man-falcon-engine).

# Fuel System Overview

The Falcon fuel system comprises an in-tank low-pressure pump (FP-4100), a camshaft-driven high-pressure GDI pump (HPFP-4120), four direct injectors (INJ-4140), an inline fuel filter (FF-4160), and a fuel rail pressure sensor (FRS-4180). These components together maintain rail pressure across the full load range. For the comparable transverse layout, cross-reference the [Osprey Fuel Service Manual](doc://man-osprey-fuel).

# Fuel Delivery Subsystem

The delivery subsystem moves fuel from the tank to the high-pressure circuit using the in-tank pump FP-4100, the high-pressure pump HPFP-4120, and the inline filter FF-4160. Adequate low-side supply is a prerequisite for stable high-side pressure. See the [Osprey Fuel Service Manual :: Fuel Delivery](doc://man-osprey-fuel#fuel-delivery) for the analogous architecture.

## In-Tank Fuel Pump

The in-tank fuel pump FP-4100 is a module-mounted unit that supplies the HPFP at roughly 60 psi. A weak FP-4100 starves the high-pressure circuit and is a common root cause of low rail pressure. Verify low-side pressure and volume before condemning any high-side component, as covered in the [Osprey Fuel Service Manual :: Low-Pressure Fuel Pump](doc://man-osprey-fuel#fuel-delivery/low-pressure-fuel-pump).

### Fuel Pump Replacement Procedure

Follow procedure PROC-FUEL-PUMP: relieve pressure, drop or access the tank, and replace the FP-4100 module as a complete assembly including the strainer. Always renew the lock ring seal and prime the system before cranking. The equivalent steps are documented in the [Osprey Fuel Service Manual :: Fuel Pump Replacement Procedure](doc://man-osprey-fuel#fuel-delivery/fuel-pump-replacement-procedure).

## High-Pressure Fuel Pump (GDI)

The high-pressure pump HPFP-4120 is driven by a dedicated cam lobe and raises pressure to over 2,000 psi for direct injection. A worn cam follower or failing HPFP-4120 commonly sets P0087 (fuel rail pressure too low). Inspect the follower whenever the pump is removed, and see the [Osprey Fuel Service Manual :: High-Pressure Fuel Pump (GDI)](doc://man-osprey-fuel#fuel-delivery/high-pressure-fuel-pump-gdi).

## Fuel Filter Service

The inline fuel filter FF-4160 protects the injectors and HPFP from particulate contamination and should be replaced at the specified interval. A clogged FF-4160 restricts flow and can mimic a failing pump. Replacement detail appears in the [Osprey Fuel Service Manual :: Fuel Filter Service](doc://man-osprey-fuel#fuel-delivery/fuel-filter-service).

# Fuel Injection Subsystem

The injection subsystem delivers metered fuel through the direct injectors INJ-4140 under ECM control. A clogged or electrically open injector commonly sets P0201 (injector circuit, cylinder 1). Injector balance and leak-down testing are the primary diagnostics here.

## Fuel Injectors

Direct injectors INJ-4140 are matched to the engine by flow code, and replacement units must be coded into the ECM after installation. A leaking INJ-4140 causes hard starts and fuel dilution of the oil. Cross-reference injector service in the [Osprey Fuel Service Manual :: Injector Service](doc://man-osprey-fuel#fuel-injection/injector-service).

### Fuel Injector Replacement Procedure

Follow procedure PROC-INJECTOR: remove the fuel rail, extract the injector with the proper puller, and always fit new Teflon sealing rings and combustion seals on each INJ-4140. After installation, code the new injector flow values and clear P0201, then verify with a balance test. The full sequence mirrors the [Osprey Fuel Service Manual :: Fuel Injector Replacement Procedure](doc://man-osprey-fuel#fuel-injection/fuel-injector-replacement-procedure).

# Fuel Rail and Pressure Sensing Subsystem

The fuel rail houses the pressure sensor FRS-4180, which closes the loop on the ECM's pressure-control strategy. A faulty FRS-4180 frequently sets P0190 (fuel rail pressure sensor circuit). Accurate sensing is essential for both startup and high-load fueling.

## Fuel Rail Pressure Sensor

The fuel rail pressure sensor FRS-4180 threads into the rail and provides a voltage proportional to pressure. An out-of-range signal sets P0190 and may force the ECM into a limp-home pressure limit. Replacement and recalibration are described in the [Osprey Fuel Service Manual :: Fuel Rail Pressure Sensor Replacement](doc://man-osprey-fuel#fuel-rail-and-pressure-sensing/fuel-rail-pressure-sensor-replacement), part of the [Osprey Fuel Service Manual :: Fuel Rail and Pressure Sensing](doc://man-osprey-fuel#fuel-rail-and-pressure-sensing) coverage.

# Fuel System Diagnostics

Fuel diagnostics on the Falcon combine fuel-trim analysis with direct pressure measurement. The relevant codes are P0171 and P0172 for trim, P0087 and P0190 for pressure, and P0201 for the injector circuit. Always begin with a visual inspection and a low-side pressure check.

## Fuel Trim Diagnosis (Lean/Rich)

Code P0171 indicates a lean condition while P0172 indicates a rich condition, each reflecting the ECM's long-term correction exceeding threshold. Lean P0171 commonly stems from vacuum leaks or low fuel supply, while rich P0172 points to leaking injectors or high rail pressure. Review live fuel-trim data across load ranges before replacing parts.

## Fuel Pressure Diagnosis

Code P0087 means rail pressure is too low and P0190 indicates a rail-pressure-sensor circuit fault. Confirm P0087 with a direct mechanical pressure reading before trusting the sensor, since a faulty FRS-4180 setting P0190 can corrupt the ECM's view of actual pressure. Distinguish a delivery shortfall from a sensing fault early in the diagnosis.

### Fuel Trim and Pressure Diagnostic Procedure

Follow procedure PROC-FUEL-DIAG: record fuel trims, then measure both low-side and high-side pressure with a gauge and scan tool. Lean codes P0171 with low pressure point to FP-4100 or HPFP-4120 supply faults, while P0087 with normal low-side pressure isolates the high-pressure circuit; a P0190 reading inconsistent with the gauge confirms the sensor. Document each reading before parts replacement to avoid misdiagnosis.
