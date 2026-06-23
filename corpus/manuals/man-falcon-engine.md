---
id: man-falcon-engine
title: Falcon Engine Service Manual
area: manuals
---

# Introduction and Engine Overview

This manual covers service and diagnostic procedures for the Falcon engine family, including naturally aspirated and turbocharged variants. The Falcon shares much of its architecture with the Harrier platform; where procedures are equivalent, refer to the [Harrier Engine Service Manual :: Engine System Overview](doc://man-harrier-engine#engine-system-overview) for supplemental detail. Technicians should read this overview in full before attempting any sub-system repair to understand torque sequences and component interdependencies.

# Safety Precautions and Special Tools

Always disconnect the negative battery terminal and allow the engine to cool before beginning service. Several timing and position-sensor procedures require dedicated alignment fixtures and a calibrated torque wrench. When servicing charging-related components in conjunction with engine work, observe the precautions in the [Falcon Charging Service Manual](doc://man-falcon-charging).

# Timing System

The Falcon timing system uses either a belt-driven (TB-3320, TB-3322) or chain-driven (TC-3340) configuration depending on model year. Belt-equipped engines require periodic replacement at the published service interval, while chain-equipped engines are designed for the life of the engine barring tensioner failure. Correct timing alignment is critical to prevent valve-to-piston contact on this interference design.

## Timing Belt and Tensioner Service

The timing belt kit TB-3320 includes the belt, idler, and a hydraulic tensioner, while the standalone tensioner assembly is cataloged as TB-3322. Always replace the tensioner when replacing the belt, and rotate the crankshaft two full revolutions by hand to verify alignment before starting the engine. For the equivalent procedure on the sister platform, see the [Harrier Engine Service Manual :: Timing Belt and Tensioner Replacement](doc://man-harrier-engine#timing-sub-system/timing-belt-and-tensioner-replacement).

## Timing Chain Service

Chain-driven Falcon engines use timing chain kit TC-3340, which bundles the chain, guides, and tensioner. Inspect the guides for scoring and the tensioner for hydraulic bleed-down whenever the front cover is removed. Detailed chain routing diagrams are provided in the [Harrier Engine Service Manual :: Timing Chain Service](doc://man-harrier-engine#timing-sub-system/timing-chain-service).

# Variable Valve Timing System

The variable valve timing (VVT) system advances and retards cam timing using an oil-control solenoid, part number VVT-3360. Faults in this circuit commonly present as rough idle, reduced power, or correlation diagnostic trouble codes. Adequate oil pressure and clean oil are prerequisites for correct VVT operation.

## VVT Solenoid Replacement

Replace the VVT-3360 solenoid when oil-control faults persist after confirming oil pressure and screen cleanliness. Torque the solenoid to specification and reset adaptive values after installation. The analogous solenoid procedure is documented in the [Harrier Engine Service Manual :: Variable Valve Timing Solenoid Replacement](doc://man-harrier-engine#timing-sub-system/variable-valve-timing-solenoid-replacement).

# Position Sensors

The Falcon engine relies on a crankshaft position sensor (CPS-3380) and a camshaft position sensor (CMP-3382) to establish synchronization for fuel and spark. Signal loss from either sensor will trigger a no-start or stalling condition. Inspect the reluctor rings and connector pins before condemning either sensor.

## Crankshaft Position Sensor Replacement

The crankshaft position sensor CPS-3380 is mounted at the front of the block adjacent to the reluctor wheel. Clear the air gap of debris and verify the resistance value against specification before installation. Cross-platform guidance is available in the [Harrier Engine Service Manual :: Crankshaft and Camshaft Position Sensor Replacement](doc://man-harrier-engine#position-sensor-sub-system/crankshaft-and-camshaft-position-sensor-replacement).

## Camshaft Position Sensor Replacement

The camshaft position sensor CMP-3382 is located in the cylinder head near the cam phaser. After replacement, perform a crank-cam correlation relearn so the control module can re-establish synchronization. See the [Harrier Engine Service Manual :: Position Sensor Sub-System](doc://man-harrier-engine#position-sensor-sub-system) for the shared wiring schematic.

# Lubrication and Crankcase Ventilation

Proper lubrication and crankcase ventilation protect the timing and VVT systems from sludge and pressure-related seal failures. The oil and filter kit OFK-3420 and the PCV valve PCV-3490 are the primary serviceable components in this group. Use only the specified oil viscosity to maintain VVT response.

## Oil and Filter Service

Use oil and filter kit OFK-3420 at every service interval, draining the oil while warm to carry away suspended contaminants. Always replace the drain plug crush washer and torque the filter housing to specification. Refer to the [Harrier Engine Service Manual](doc://man-harrier-engine) for capacity charts on related applications.

## PCV Valve Replacement

A failed PCV valve PCV-3490 can cause oil consumption, rough idle, and intake leaks. Inspect the valve for rattle and the hoses for collapse, then replace as an assembly if either is suspect. Verify there are no stored vacuum-related codes after replacement.

# Forced Induction (Turbocharger)

Turbocharged Falcon engines use turbocharger assembly TBO-3470, which is oil- and coolant-cooled. Always inspect the oil feed and drain lines for restriction when diagnosing turbo failures, as oil starvation is the leading cause of bearing failure.

## Turbocharger Replacement

Before installing turbocharger TBO-3470, prime the bearing housing with clean oil and replace all gaskets and the oil feed line. Allow the engine to idle after the initial start to establish oil flow before applying load. Confirm there are no boost-control or overboost codes after the repair.

# Engine Sealing and Mounting

The valve cover gasket VCG-3401 and engine mount ENM-3450 are common service items that affect oil sealing and NVH respectively. A leaking valve cover gasket can contaminate spark plug wells and ignition components.

## Valve Cover Gasket Replacement

Replace the valve cover gasket VCG-3401 whenever oil seepage is found at the cylinder head mating surface. Clean the sealing surface thoroughly and torque the cover fasteners in the specified cross pattern to avoid distortion. Inspect the spark plug tube seals at the same time.

## Engine Mount Replacement

A collapsed or fluid-filled engine mount ENM-3450 causes excessive vibration and driveline clunk. Support the engine before removing the mount and torque the fasteners to specification with the powertrain at rest. Verify clearance to surrounding components after installation.

# Misfire Diagnosis

Misfire diagnostic trouble codes include the general misfire P0300 and cylinder-specific codes P0301, P0302, P0303, and P0304. Begin diagnosis by reviewing freeze-frame data and fuel trims, then isolate ignition, fuel, and mechanical causes. The full diagnostic decision tree and DTC definitions are mirrored in the [Harrier Engine Service Manual :: Misfire Diagnostic Trouble Code Reference](doc://man-harrier-engine#diagnosis/misfire-diagnostic-trouble-code-reference) and the step-by-step [Harrier Engine Service Manual :: Misfire Diagnosis Procedure](doc://man-harrier-engine#diagnosis/misfire-diagnosis-procedure).
