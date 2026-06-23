---
id: man-summit-fuel
title: Summit Fuel Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Summit fuel system. Always relieve fuel system pressure before opening any line, disconnect the battery negative terminal, and work in a well-ventilated area away from open flame. Wear eye protection and keep a Class B fire extinguisher within reach during all fuel service operations. For platform-equivalent procedures on the related architecture, refer to the [Osprey Fuel Service Manual](doc://man-osprey-fuel).

# Fuel System Overview

The Summit fuel system delivers metered fuel from the tank to the combustion chambers through a coordinated set of components. The low-pressure fuel pump FP-4100 supplies the high-pressure fuel pump HPFP-4120, which feeds the fuel injectors INJ-4140 through the rail. The fuel filter FF-4160 protects downstream components from contamination, while the fuel rail pressure sensor FRS-4180 provides closed-loop pressure feedback to the powertrain control module. The overall layout closely mirrors the architecture documented in [Osprey Fuel Service Manual :: Fuel Delivery](doc://man-osprey-fuel#fuel-delivery).

# Diagnosis

Fuel system faults typically surface as drivability complaints accompanied by stored diagnostic trouble codes. Begin with a full scan-tool sweep and capture freeze-frame data before clearing any codes. The most common codes seen on this platform are P0171, P0172, P0087, P0190, and P0201, each of which is detailed below. Follow the structured workflow in PROC-FUEL-DIAG to isolate root cause rather than replacing parts speculatively. The equivalent diagnostic tree appears in [Osprey Fuel Service Manual :: Fuel System Diagnosis](doc://man-osprey-fuel#fuel-system-diagnosis).

## Fuel Diagnostic Trouble Code Reference

P0171 indicates System Too Lean (Bank 1) and P0172 indicates System Too Rich (Bank 1); both reflect fuel trim corrections exceeding calibrated limits. P0087 sets when Fuel Rail/System Pressure is too low, commonly tied to a weak FP-4100 or a clogged FF-4160. P0190 reports a Fuel Rail Pressure Sensor circuit malfunction associated with FRS-4180, while P0201 flags an injector circuit fault for cylinder 1 affecting INJ-4140. Record all codes with their freeze-frame fuel trim values before proceeding.

## Fuel Trim and Pressure Diagnosis Procedure

Execute PROC-FUEL-DIAG by first observing live short- and long-term fuel trims while monitoring rail pressure against the desired value. A lean code such as P0171 with low measured pressure points toward delivery faults, whereas P0172 with normal pressure suggests a contributing sensor or injector concern. If P0087 is present, perform a static and running pressure test to determine whether the deficiency originates at the low-pressure or high-pressure stage. When P0190 appears, verify FRS-4180 reference voltage and signal return before condemning the sensor. The cross-platform analog of this routine is documented in [Osprey Fuel Service Manual :: Fuel System Diagnosis](doc://man-osprey-fuel#fuel-system-diagnosis).

# Fuel Delivery Sub-System

The delivery sub-system moves fuel from the tank through the filter to the high-pressure stage. The in-tank pump FP-4100 establishes lift pressure, the filter FF-4160 removes particulates, and the high-pressure fuel pump HPFP-4120 raises pressure to injection levels. A degraded pump or restricted filter commonly produces P0087. Refer to PROC-FUEL-PUMP for removal and installation steps; the corresponding low-pressure procedure is in [Osprey Fuel Service Manual :: Low-Pressure Fuel Pump](doc://man-osprey-fuel#fuel-delivery/low-pressure-fuel-pump).

## Fuel Pump Replacement Procedure

Follow PROC-FUEL-PUMP to replace the low-pressure pump FP-4100 after relieving system pressure and draining the tank as needed. Disconnect the electrical connector and supply line, remove the lock ring, and extract the module taking care not to damage the level sender. When servicing the high-pressure stage, the HPFP-4120 is accessed at the cylinder head and requires camshaft timing verification on reinstallation. The platform-equivalent steps are described in [Osprey Fuel Service Manual :: Fuel Pump Replacement Procedure](doc://man-osprey-fuel#fuel-delivery/fuel-pump-replacement-procedure).

## Fuel Filter Service

Replace the fuel filter FF-4160 at the specified interval or whenever a delivery restriction is suspected. Relieve pressure, capture residual fuel in an approved container, and note the directional flow arrow during installation. A neglected FF-4160 is a frequent contributor to low-pressure faults and should be inspected during any delivery diagnosis. See [Osprey Fuel Service Manual :: Fuel Filter Service](doc://man-osprey-fuel#fuel-delivery/fuel-filter-service) for the comparable interval and orientation notes.

## High-Pressure Fuel Pump Service

The high-pressure fuel pump HPFP-4120 is mechanically driven and must be timed to the camshaft lobe during installation. A worn pump tappet or internal leakage frequently sets P0087 under high-demand conditions. Always replace the pump follower and seal when servicing HPFP-4120 and pre-lubricate the contact surfaces before torquing the mounting bolts. The GDI-specific guidance is provided in [Osprey Fuel Service Manual :: High-Pressure Fuel Pump (GDI)](doc://man-osprey-fuel#fuel-delivery/high-pressure-fuel-pump-gdi).

# Fuel Injection Sub-System

The injection sub-system atomizes pressurized fuel into each cylinder via the injectors INJ-4140. An open, shorted, or fouled injector circuit on cylinder 1 sets P0201 and produces a misfire or rough idle. Use PROC-INJECTOR to test resistance and spray pattern before replacement. The corresponding cross-platform overview is in [Osprey Fuel Service Manual :: Fuel Injection](doc://man-osprey-fuel#fuel-injection).

## Fuel Injector Replacement Procedure

PROC-INJECTOR details removal of the injectors INJ-4140 after rail depressurization and rail removal. Always replace the injector seals and combustion gaskets, and code any new injector trim values into the PCM where applicable. A confirmed P0201 with verified wiring integrity justifies replacing the cylinder 1 injector. Comparable steps appear in [Osprey Fuel Service Manual :: Fuel Injector Replacement Procedure](doc://man-osprey-fuel#fuel-injection/fuel-injector-replacement-procedure).

# Fuel Rail Pressure Sub-System

The fuel rail pressure sub-system uses sensor FRS-4180 to report actual rail pressure for closed-loop control. A faulty sensor or circuit sets P0190 and may cause erratic pressure regulation or a no-start. Verify connector integrity and reference voltage before condemning FRS-4180.

## Fuel Rail Pressure Sensor Replacement

Replace the fuel rail pressure sensor FRS-4180 only after confirming wiring and connector integrity for a stored P0190. Relieve rail pressure, remove the sensor, and torque the replacement to specification using a new seal. Clear codes and verify rail pressure tracks the desired value across the operating range. See [Osprey Fuel Service Manual :: Fuel Rail Pressure Sensor Replacement](doc://man-osprey-fuel#fuel-rail-and-pressure-sensing/fuel-rail-pressure-sensor-replacement) for the equivalent procedure.

# Specifications and Torque Values

All fasteners must be torqued to the values listed in this section using a calibrated torque wrench. Observe specified fuel pressure ranges, sensor reference voltages, and seal replacement requirements for every component. Always reference the latest revision of this section, as torque values may be superseded by service bulletins.
