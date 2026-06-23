---
id: man-ridgeline-hd-emissions
title: Ridgeline HD Emissions Service Manual
area: manuals
---

# Introduction and Safety

This manual covers diagnosis and repair of the Ridgeline HD emissions control system. Exhaust components operate at extreme temperatures, so allow the system to cool fully before service and wear heat-resistant gloves. Use approved exhaust gas analyzers in ventilated bays and never run the engine in an enclosed space. For the comparable light-duty architecture, refer to the [Kestrel Emissions Service Manual](doc://man-kestrel-emissions).

# Emissions System Overview

The Ridgeline HD emissions system reduces tailpipe pollutants through catalytic conversion, oxygen sensing, recirculation, evaporative control, and particulate filtration. The primary catalytic converter CAT-5500 and secondary converter CAT-5520 oxidize hydrocarbons, monitored by upstream sensor O2U-5100 and downstream sensor O2D-5120. The EGR valve EGR-5140 meters recirculated exhaust to lower combustion temperatures, while the evaporative purge valve EVP-5160 manages fuel vapor. On diesel variants the particulate filter DPF-5180 traps soot for periodic regeneration. The catalytic stage parallels [Kestrel Emissions Service Manual :: Catalytic Conversion](doc://man-kestrel-emissions#catalytic-conversion).

# Diagnosis

Emissions faults are usually identified by stored diagnostic trouble codes and confirmed with live sensor data. Capture freeze-frame data and verify there are no active fuel or ignition codes that could skew emissions readings. The codes addressed in this manual are P0420, P0430, P0401, P0455, P0442, and P2002. Begin with the most upstream contributing fault before condemning catalysts or filters.

## Emissions Diagnostic Trouble Code Reference

P0420 indicates Catalyst System Efficiency Below Threshold (Bank 1) and P0430 the same condition for Bank 2. P0401 sets when Exhaust Gas Recirculation flow is insufficient at the EGR-5140 valve. P0455 reports a large evaporative system leak and P0442 a small leak, both involving EVP-5160. P2002 indicates Diesel Particulate Filter efficiency below threshold for DPF-5180. Record all codes before clearing.

## Catalyst Efficiency Diagnosis

A P0420 or P0430 is set when the downstream sensor O2D-5120 mirrors the upstream sensor O2U-5100, indicating the catalyst is no longer storing oxygen effectively. Before condemning CAT-5500 or CAT-5520, confirm both oxygen sensors switch normally and rule out exhaust leaks or fuel trim faults. Compare upstream and downstream waveforms under steady-state and acceleration. The equivalent efficiency workflow is documented in [Kestrel Emissions Service Manual :: Oxygen Sensing](doc://man-kestrel-emissions#oxygen-sensing).

## EVAP Leak Diagnosis

P0455 and P0442 are diagnosed by pressurizing or evacuating the evaporative system and locating the leak source. Inspect the purge valve EVP-5160, fuel cap seal, and all vapor lines for cracking or loose connections. A small leak setting P0442 is often a degraded seal, while a large leak setting P0455 frequently traces to a stuck-open EVP-5160 or disconnected line. See [Kestrel Emissions Service Manual :: Evaporative Emission Control](doc://man-kestrel-emissions#evaporative-emission-control) for the comparable leak test.

# Catalytic Converter Sub-System

The catalytic converter sub-system comprises the primary CAT-5500 and secondary CAT-5520 units that oxidize and reduce tailpipe pollutants. Efficiency loss from contamination, overheating, or substrate breakdown sets P0420 or P0430. Use PROC-CAT for removal and installation after confirming sensors and fuel trim are within specification. The cross-platform overview is in [Kestrel Emissions Service Manual :: Catalytic Converter (Bank 1 and Bank 2)](doc://man-kestrel-emissions#catalytic-conversion/catalytic-converter-bank-1-and-bank-2).

## Catalytic Converter Replacement Procedure

Follow PROC-CAT to replace the catalytic converters CAT-5500 and CAT-5520 after the assembly has fully cooled. Penetrate and remove fasteners carefully, replace all gaskets, and avoid impacting the substrate during handling. After installing CAT-5500 or CAT-5520, clear codes and complete a catalyst monitor drive cycle to confirm the repair. The equivalent steps are in [Kestrel Emissions Service Manual :: Catalytic Converter Replacement Procedure](doc://man-kestrel-emissions#catalytic-conversion/catalytic-converter-replacement-procedure).

# Oxygen Sensor Sub-System

The oxygen sensor sub-system uses upstream sensor O2U-5100 for fuel control and downstream sensor O2D-5120 for catalyst monitoring. A lazy or biased sensor can falsely set P0420 or P0430, so always validate sensor response before replacing a converter. Inspect the harness and connector for heat damage. The comparable description appears in [Kestrel Emissions Service Manual :: Upstream and Downstream Oxygen Sensors](doc://man-kestrel-emissions#oxygen-sensing/upstream-and-downstream-oxygen-sensors).

## Oxygen Sensor Replacement Procedure

Use PROC-O2-SENSOR to replace the oxygen sensors O2U-5100 and O2D-5120 after the exhaust has cooled. Apply anti-seize sparingly to the threads only, avoiding the sensor tip, and torque to specification. Confirm the new O2U-5100 switches rapidly and the downstream O2D-5120 remains stable once the catalyst is hot. Equivalent guidance is in [Kestrel Emissions Service Manual :: Oxygen Sensor Replacement Procedure](doc://man-kestrel-emissions#oxygen-sensing/oxygen-sensor-replacement-procedure).

# Exhaust Gas Recirculation Sub-System

The exhaust gas recirculation sub-system routes metered exhaust back into the intake through valve EGR-5140 to reduce combustion temperature and NOx. Carbon buildup or a stuck valve restricts flow and sets P0401. Inspect the valve and passages for deposits during diagnosis. The cross-platform overview is in [Kestrel Emissions Service Manual :: Exhaust Gas Recirculation](doc://man-kestrel-emissions#exhaust-gas-recirculation).

## EGR Valve Service Procedure

Follow PROC-EGR to clean or replace the EGR valve EGR-5140 when P0401 indicates insufficient flow. Remove the valve, inspect the pintle and seat for carbon, and clear obstructed passages with approved solvent. Replace the gasket on reinstallation and verify commanded versus actual flow with a scan tool. See [Kestrel Emissions Service Manual :: EGR Valve Service Procedure](doc://man-kestrel-emissions#exhaust-gas-recirculation/egr-valve-service-procedure) for comparable steps.

# Evaporative Emissions Sub-System

The evaporative emissions sub-system captures and purges fuel vapor through the purge valve EVP-5160 and associated lines. A stuck or leaking EVP-5160 commonly sets P0455 for large leaks or P0442 for small leaks. Inspect the valve operation and all vapor line connections during service. See [Kestrel Emissions Service Manual :: Evaporative Emission Control](doc://man-kestrel-emissions#evaporative-emission-control) for the equivalent overview.

## EVAP Purge Valve Service

Service the purge valve EVP-5160 when leak codes P0455 or P0442 are confirmed and the valve is implicated. Verify the valve holds vacuum when commanded closed and opens fully when commanded open. Replace EVP-5160 if it fails to seal, then re-run the evaporative monitor to confirm the leak is resolved. The comparable procedure is in [Kestrel Emissions Service Manual :: EVAP Purge Valve Service](doc://man-kestrel-emissions#evaporative-emission-control/evap-purge-valve-service).

# Diesel Particulate Filter Sub-System

On diesel variants the particulate filter DPF-5180 traps soot and is periodically cleaned through regeneration. Excessive ash loading or a degraded substrate sets P2002 for filter efficiency below threshold. Monitor differential pressure and soot load before condemning the filter. See [Kestrel Emissions Service Manual :: Diesel Particulate Filter](doc://man-kestrel-emissions#diesel-particulate-filter) for the related description.

## Diesel Particulate Filter Service and Forced Regeneration

When P2002 is active, first attempt a scan-tool commanded forced regeneration of DPF-5180 to burn off accumulated soot. Ensure exhaust temperatures reach the required regeneration threshold and that no active EGR or sensor faults interrupt the cycle. If regeneration fails to restore differential pressure, the DPF-5180 must be cleaned or replaced. Always observe exhaust temperature warnings during forced regeneration.

# Specifications and Torque Values

All exhaust and emissions fasteners must be torqued to the values listed using a calibrated torque wrench. Observe specified sensor torque, gasket replacement requirements, and regeneration temperature thresholds. Reference the latest revision, as values may be superseded by service bulletins.
