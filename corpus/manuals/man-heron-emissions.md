---
id: man-heron-emissions
title: Heron Emissions Service Manual
area: manuals
---

# Introduction and Safety Precautions

This manual covers the Heron emissions control systems, including catalytic conversion, oxygen sensing, exhaust gas recirculation, evaporative emissions, and diesel particulate filtration. Exhaust components reach extreme temperatures, so allow the system to cool before service and never run the engine in an enclosed space. Ignition-side interactions are documented in the [Heron Ignition Service Manual](doc://man-heron-ignition). For the comparable platform, cross-reference the [Kestrel Emissions Service Manual](doc://man-kestrel-emissions).

# Emissions System Overview

The Heron emissions architecture combines a primary catalytic converter (CAT-5500) and secondary converter (CAT-5520) with upstream and downstream oxygen sensors (O2U-5100 and O2D-5120), an EGR valve (EGR-5140), an evaporative purge valve (EVP-5160), and a diesel particulate filter (DPF-5180) on compression-ignition variants. These subsystems work together to meet tailpipe standards across operating conditions. Component layout closely follows the [Kestrel Emissions Service Manual](doc://man-kestrel-emissions).

# Catalytic Converter Subsystem

The catalytic converter subsystem uses CAT-5500 on bank 1 and CAT-5520 on bank 2 to oxidize hydrocarbons and reduce NOx. Reduced catalyst efficiency commonly sets P0420 on bank 1 or P0430 on bank 2. Always rule out exhaust leaks and faulty oxygen sensors before condemning a converter, and see the [Kestrel Emissions Service Manual :: Catalytic Conversion](doc://man-kestrel-emissions#catalytic-conversion).

## Catalyst Efficiency Faults

Code P0420 indicates catalyst efficiency below threshold on bank 1, and P0430 indicates the same on bank 2. These codes are triggered when the downstream sensor signal begins to mirror the upstream sensor, indicating a depleted catalyst. Verify that the downstream O2D-5120 sensor is healthy before replacing CAT-5500 or CAT-5520, referencing the [Kestrel Emissions Service Manual :: Catalytic Converter (Bank 1 and Bank 2)](doc://man-kestrel-emissions#catalytic-conversion/catalytic-converter-bank-1-and-bank-2).

### Catalytic Converter Replacement Procedure

Follow procedure PROC-CAT: support the exhaust, remove the upstream and downstream sensors, and unbolt the converter at its flanges. Replace CAT-5500 or CAT-5520 with the correct bank-specific unit and renew the flange gaskets to prevent leaks that would skew sensor readings. The equivalent steps are in the [Kestrel Emissions Service Manual :: Catalytic Converter Replacement Procedure](doc://man-kestrel-emissions#catalytic-conversion/catalytic-converter-replacement-procedure).

# Oxygen Sensor Subsystem

The oxygen sensor subsystem provides the ECM with closed-loop feedback using the upstream sensor O2U-5100 and downstream sensor O2D-5120. The upstream sensor controls fuel trim while the downstream sensor monitors catalyst efficiency. Cross-reference the [Kestrel Emissions Service Manual :: Oxygen Sensing](doc://man-kestrel-emissions#oxygen-sensing).

## Upstream and Downstream Sensors

Upstream sensor O2U-5100 is a wideband air-fuel sensor mounted before the catalyst, while downstream sensor O2D-5120 is a narrowband sensor mounted after it. A lazy or biased O2U-5100 corrupts fuel trim, and a degraded O2D-5120 can falsely trigger catalyst codes. Sensor function and testing are detailed in the [Kestrel Emissions Service Manual :: Upstream and Downstream Oxygen Sensors](doc://man-kestrel-emissions#oxygen-sensing/upstream-and-downstream-oxygen-sensors).

### Oxygen Sensor Replacement Procedure

Follow procedure PROC-O2-SENSOR: allow the exhaust to cool, apply penetrating oil to the sensor threads, and use a slotted socket to avoid damaging the harness on O2U-5100 or O2D-5120. Apply anti-seize sparingly to the threads only, never to the sensor tip, and route the harness away from hot surfaces. The full sequence appears in the [Kestrel Emissions Service Manual :: Oxygen Sensor Replacement Procedure](doc://man-kestrel-emissions#oxygen-sensing/oxygen-sensor-replacement-procedure).

# Exhaust Gas Recirculation Subsystem

The EGR subsystem reduces combustion temperatures and NOx by recirculating measured exhaust gas through the EGR valve EGR-5140. Insufficient flow commonly sets P0401. Carbon buildup is the most frequent cause of EGR complaints on the Heron platform.

## EGR Flow Faults

Code P0401 indicates insufficient exhaust gas recirculation flow detected by the ECM. This is usually caused by carbon clogging the EGR-5140 passages or a sticking valve pintle. Inspect and clean the passages before replacing the valve, referencing the [Kestrel Emissions Service Manual :: Exhaust Gas Recirculation](doc://man-kestrel-emissions#exhaust-gas-recirculation).

### EGR Valve Service Procedure

Follow procedure PROC-EGR: disconnect the connector and vacuum or electrical actuation, then remove EGR-5140 and decarbon the mating passages. Test valve operation and verify the P0401 code clears after cleaning or replacement. Detailed steps are in the [Kestrel Emissions Service Manual :: EGR Valve Service Procedure](doc://man-kestrel-emissions#exhaust-gas-recirculation/egr-valve-service-procedure).

# Evaporative Emissions Subsystem

The evaporative emissions subsystem captures fuel vapor in the charcoal canister and meters it to the intake through the purge valve EVP-5160. Leaks in this sealed system set EVAP codes. Most failures trace to the purge valve, vent valve, or fuel cap.

## EVAP Leak Faults

Code P0455 indicates a large evaporative system leak, while P0442 indicates a small leak. Begin diagnosis with a smoke test of the sealed system and confirm the EVP-5160 purge valve holds vacuum. Purge valve service is documented in the [Kestrel Emissions Service Manual :: EVAP Purge Valve Service](doc://man-kestrel-emissions#evaporative-emission-control/evap-purge-valve-service), part of the [Kestrel Emissions Service Manual :: Evaporative Emission Control](doc://man-kestrel-emissions#evaporative-emission-control) coverage.

# Diesel Particulate Filter Subsystem

The diesel particulate filter subsystem traps soot in the DPF-5180 and periodically regenerates to burn off accumulated particulate. Restricted or failed regeneration sets DPF efficiency codes. Frequent short trips prevent passive regeneration and accelerate clogging.

## DPF Efficiency Faults

Code P2002 indicates diesel particulate filter efficiency below threshold for the DPF-5180. Measure the differential pressure across the filter and attempt a forced regeneration before replacement. A DPF-5180 contaminated by engine oil or coolant cannot be regenerated and must be replaced.
