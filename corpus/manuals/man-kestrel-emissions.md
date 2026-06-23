---
id: man-kestrel-emissions
title: Kestrel Emissions Service Manual
area: manuals
---

# Introduction and Emissions System Overview

This manual covers the Kestrel emissions system, including catalytic conversion, oxygen sensing, exhaust gas recirculation, evaporative control, and diesel particulate filtration. The Kestrel emissions architecture parallels the heavy-duty Ridgeline platform; refer to the [Ridgeline HD Emissions Service Manual :: Emissions System Overview](doc://man-ridgeline-hd-emissions#emissions-system-overview) for related component detail. Read this overview before servicing any emissions sub-system.

# Safety Precautions and Diagnostic Tools

Exhaust components remain hot long after shutdown, so allow adequate cooling before servicing catalytic converters or oxygen sensors. Use a scan tool capable of reading mode-6 emissions data and a dedicated oxygen-sensor socket. When emissions work overlaps with body or undercarriage repair, consult the [Kestrel Body Service Manual](doc://man-kestrel-body) for shield removal.

# Catalytic Conversion

The Kestrel uses bank-specific catalytic converters, with CAT-5500 serving Bank 1 and CAT-5520 serving Bank 2 on V-configuration engines. Converter efficiency is monitored by the downstream oxygen sensors. Always diagnose the root cause of a failed converter, such as a misfire or rich condition, before replacement.

## Catalytic Converter (Bank 1 and Bank 2)

Install converter CAT-5500 on Bank 1 and CAT-5520 on Bank 2, observing the correct flow direction and using new gaskets at every flange. Do not reuse exhaust fasteners that show heat damage. Cross-platform fitment data is in the [Ridgeline HD Emissions Service Manual :: Catalytic Converter Sub-System](doc://man-ridgeline-hd-emissions#catalytic-converter-sub-system).

## Catalytic Converter Replacement Procedure

Procedure PROC-CAT covers removal of the converter and the associated oxygen sensors, applying penetrating oil to seized fasteners well in advance. After installation, clear codes and complete a catalyst monitor drive cycle to confirm the repair. The equivalent step list is provided in the [Ridgeline HD Emissions Service Manual :: Catalytic Converter Replacement Procedure](doc://man-ridgeline-hd-emissions#catalytic-converter-sub-system/catalytic-converter-replacement-procedure).

# Oxygen Sensing

The Kestrel uses an upstream wide-band oxygen sensor O2U-5100 for fuel control and a downstream sensor O2D-5120 for catalyst monitoring. Contamination from coolant or oil will skew sensor readings and set efficiency codes. Verify sensor heater operation during diagnosis.

## Upstream and Downstream Oxygen Sensors

The upstream sensor O2U-5100 provides the primary feedback signal for closed-loop fueling, while the downstream sensor O2D-5120 compares post-catalyst oxygen content. Do not interchange the two, as the connector keying and calibration differ. Refer to the [Ridgeline HD Emissions Service Manual :: Oxygen Sensor Sub-System](doc://man-ridgeline-hd-emissions#oxygen-sensor-sub-system) for the wiring schematic.

## Oxygen Sensor Replacement Procedure

Procedure PROC-O2-SENSOR requires the engine to be cool and the use of anti-seize on the sensor threads only where specified. Torque the sensor to the published value and route the harness away from the exhaust to prevent melting. The parallel procedure appears in the [Ridgeline HD Emissions Service Manual :: Oxygen Sensor Replacement Procedure](doc://man-ridgeline-hd-emissions#oxygen-sensor-sub-system/oxygen-sensor-replacement-procedure).

# Exhaust Gas Recirculation

The exhaust gas recirculation system uses EGR valve EGR-5140 to route metered exhaust back into the intake, reducing combustion temperatures and NOx. Carbon accumulation is the most common cause of EGR faults. Inspect the passages whenever the valve is removed.

## EGR Valve Service Procedure

Procedure PROC-EGR covers cleaning and replacement of the EGR valve EGR-5140, including decarboning the intake passages with an approved solvent. Replace the valve gasket and verify smooth actuation before reinstallation. Additional guidance is in the [Ridgeline HD Emissions Service Manual :: Exhaust Gas Recirculation Sub-System](doc://man-ridgeline-hd-emissions#exhaust-gas-recirculation-sub-system).

# Evaporative Emission Control

The evaporative emission control system uses purge valve EVP-5160 to draw stored fuel vapor from the canister into the intake. A stuck or leaking purge valve causes fuel-trim drift and leak-detection faults. Inspect the valve and hoses for cracks during diagnosis.

## EVAP Purge Valve Service

Replace the EVAP purge valve EVP-5160 when it fails to hold vacuum or chatters during a commanded test. Verify the canister and vent valve function as part of a complete EVAP inspection. Confirm the monitor runs to completion after the repair.

# Diesel Particulate Filter

Diesel Kestrel variants use a diesel particulate filter DPF-5180 to trap soot, which is periodically burned off during regeneration. Frequent short trips can prevent regeneration and lead to clogging. Monitor differential pressure to assess filter loading.

## DPF Service and Regeneration

Service the diesel particulate filter DPF-5180 by first attempting a forced regeneration with the scan tool when soot loading is high but within limits. Replace the filter only when ash loading exceeds the published threshold or regeneration repeatedly fails. Record pre- and post-service differential pressure values.

# Emissions System Diagnosis

Emissions diagnosis addresses catalyst codes (P0420, P0430), EGR flow code P0401, EVAP leak codes (P0455, P0442), and DPF efficiency code P2002. Always identify and correct upstream faults before condemning an emissions component. The complete DTC table is mirrored in the [Ridgeline HD Emissions Service Manual :: Emissions Diagnostic Trouble Code Reference](doc://man-ridgeline-hd-emissions#diagnosis/emissions-diagnostic-trouble-code-reference).

## Catalyst Efficiency Faults

Code P0420 indicates catalyst efficiency below threshold on Bank 1, and P0430 indicates the same on Bank 2. Confirm the downstream oxygen sensor is healthy and that no exhaust leaks exist before replacing the converter. The structured tree is provided in the [Ridgeline HD Emissions Service Manual :: Catalyst Efficiency Diagnosis](doc://man-ridgeline-hd-emissions#diagnosis/catalyst-efficiency-diagnosis).

## EGR Flow Faults

Code P0401 indicates insufficient EGR flow, commonly caused by carbon-clogged passages or a stuck valve. Inspect and clean the EGR-5140 valve and intake passages before considering replacement. Verify commanded versus actual flow with the scan tool.

## EVAP Leak Faults

Code P0455 indicates a large evaporative leak while P0442 indicates a small leak. Use a smoke machine to pinpoint the leak source, paying close attention to the fuel cap, hoses, and purge valve EVP-5160. See the [Ridgeline HD Emissions Service Manual :: EVAP Leak Diagnosis](doc://man-ridgeline-hd-emissions#diagnosis/evap-leak-diagnosis) for the leak-isolation sequence.

## DPF Efficiency Faults

Code P2002 indicates diesel particulate filter efficiency below threshold on Bank 1. Confirm the differential pressure sensor and its hoses are accurate before condemning the filter DPF-5180. Attempt a forced regeneration and re-evaluate before replacement.
