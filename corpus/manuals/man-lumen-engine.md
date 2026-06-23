---
id: man-lumen-engine
title: Lumen Engine Service Manual
area: manuals
---

# Engine System Overview

The Lumen engine platform is a transversely mounted inline-four available in both naturally aspirated and turbocharged forms. This manual covers diagnosis and repair of the valve timing, position sensing, induction, lubrication, and mounting sub-systems. For the longitudinally mounted variant used in rear-drive applications, cross-reference the [Falcon Engine Service Manual](doc://man-falcon-engine), which shares many torque specifications and diagnostic flows. Always observe the safety precautions in the relevant section before beginning any teardown.

# Misfire Diagnosis

Misfires on the Lumen engine are most often traced to ignition, fuel delivery, or mechanical compression faults. Stored fault codes P0300, P0301, P0302, P0303, and P0304 should be the starting point for any misfire complaint. Confirm fuel trim and compression before condemning ignition components, and inspect the PCV system as described in the PCV Valve Service section, since vacuum leaks frequently set P0300.

## Reading Misfire Fault Codes

Code P0300 indicates a random or multiple-cylinder misfire, while P0301, P0302, P0303, and P0304 identify a misfire isolated to cylinders one through four respectively. Use a scan tool to capture freeze-frame data and the misfire counter per cylinder before clearing codes. A single-cylinder code such as P0302 paired with low compression on that cylinder points to a mechanical fault rather than an ignition or fuel issue.

# Valve Timing Sub-System

The Lumen valve timing sub-system uses either a timing belt (parts TB-3320 and TB-3322) or a timing chain (TC-3340) depending on engine build year, plus a variable valve timing solenoid (VVT-3360). Correct timing is critical to prevent piston-to-valve contact on this interference engine. For the comparable rear-drive layout, see the [Falcon Engine Service Manual :: Timing System](doc://man-falcon-engine#timing-system).

## Timing Belt Specifications and Identification

Early Lumen builds use timing belt TB-3320 (124-tooth) for naturally aspirated engines and TB-3322 (126-tooth) for turbocharged engines; the two are not interchangeable. Verify the part number stamped on the belt spine against the build sheet before ordering. Belt replacement interval is 90,000 miles or 7 years, whichever comes first.

### Timing Belt and Tensioner Replacement Procedure

Remove the accessory drive belt, crankshaft pulley, and upper timing cover, then align the crankshaft and camshaft timing marks before loosening the tensioner. Install the new belt (TB-3320 or TB-3322 as applicable) and a fresh tensioner, rotating the engine two full revolutions by hand to confirm mark alignment. The procedure mirrors the [Falcon Engine Service Manual :: Timing Belt and Tensioner Service](doc://man-falcon-engine#timing-system/timing-belt-and-tensioner-service), though tensioner torque differs.

## Timing Chain Service

Later Lumen engines use a maintenance-free timing chain, part TC-3340, with a hydraulic tensioner that pressurizes on oil flow. A stretched chain or worn guides will retard cam timing and may set position-sensor correlation codes. Replacement requires removing the front cover and is documented further in the [Falcon Engine Service Manual :: Timing Chain Service](doc://man-falcon-engine#timing-system/timing-chain-service).

## Variable Valve Timing Solenoid Service

The variable valve timing solenoid VVT-3360 controls oil flow to the cam phaser and is a common cause of cold-start rattle and rough idle. Inspect the solenoid screen for sludge before replacement, as a restricted screen mimics a failed solenoid. See the [Falcon Engine Service Manual :: VVT Solenoid Replacement](doc://man-falcon-engine#variable-valve-timing-system/vvt-solenoid-replacement) for the analogous removal sequence.

# Position Sensor Sub-System

Accurate engine timing depends on the crankshaft position sensor (CPS-3380) and camshaft position sensor (CMP-3382), which the ECM compares for correlation. A fault in either sensor can cause no-start, stalling, or misfire complaints. The Lumen sensor layout closely follows the [Falcon Engine Service Manual :: Position Sensors](doc://man-falcon-engine#position-sensors).

## Crankshaft and Camshaft Position Sensor Service

The crankshaft position sensor CPS-3380 mounts at the bellhousing and reads the reluctor ring, while the camshaft position sensor CMP-3382 mounts in the cylinder head near the phaser. Check the air gap and connector for oil intrusion before replacing either unit. Detailed removal steps are provided in the [Falcon Engine Service Manual :: Crankshaft Position Sensor Replacement](doc://man-falcon-engine#position-sensors/crankshaft-position-sensor-replacement) and the [Falcon Engine Service Manual :: Camshaft Position Sensor Replacement](doc://man-falcon-engine#position-sensors/camshaft-position-sensor-replacement).

# Air Induction and Forced Induction Sub-System

Turbocharged Lumen engines route intake air through the turbocharger (TBO-3470) and recirculate crankcase vapors via the PCV valve (PCV-3490). Both components affect intake pressure and can influence misfire and fuel-trim behavior. Inspect all charge-air piping clamps when servicing either part.

## Turbocharger Service

The turbocharger assembly TBO-3470 is oil- and coolant-cooled; always prime the oil feed before initial start to prevent bearing damage. Inspect the wastegate actuator and shaft play during diagnosis of low-boost complaints. Allow the engine to idle before shutdown to avoid coking the center bearing.

## PCV Valve Service

A stuck-open PCV valve PCV-3490 creates a metered vacuum leak that commonly sets P0300 along with lean fuel trims. Test the valve by checking for rattle and verifying it seals under engine vacuum. Replacement is straightforward and parallels the [Falcon Engine Service Manual :: PCV Valve Replacement](doc://man-falcon-engine#lubrication-and-crankcase-ventilation/pcv-valve-replacement).

# Lubrication and Sealing Sub-System

The lubrication and sealing sub-system covers the oil and filter service kit (OFK-3420) and the valve cover gasket (VCG-3401). Maintaining clean oil at the correct level is essential for VVT and timing-chain tensioner operation. See the [Falcon Engine Service Manual :: Lubrication and Crankcase Ventilation](doc://man-falcon-engine#lubrication-and-crankcase-ventilation) for shared fluid specifications.

## Oil and Filter Service

Use oil and filter kit OFK-3420, which includes the cartridge filter, drain plug crush washer, and the correct 5W-30 full-synthetic capacity for the Lumen sump. Replace oil every 7,500 miles under normal duty or 5,000 miles under severe duty. The service interval and fill procedure match the [Falcon Engine Service Manual :: Oil and Filter Service](doc://man-falcon-engine#lubrication-and-crankcase-ventilation/oil-and-filter-service).

## Valve Cover Gasket Replacement

Valve cover gasket VCG-3401 hardens with age and is a frequent source of oil leaks onto the exhaust manifold and ignition components. Replace the gasket and spark-plug tube seals together, torquing the cover bolts in sequence to avoid warping. Clean all sealing surfaces and inspect the PCV grommet during reassembly.

# Engine Mounting Sub-System

The engine mounting sub-system secures the powertrain and damps vibration through three hydraulic mounts. Worn mounts transmit excess vibration into the cabin and can allow the engine to shift under load. The primary serviceable component is the right-hand hydraulic mount.

## Engine Mount Inspection and Replacement

Inspect engine mount ENM-3450 for fluid leakage, separation of the rubber isolator, and excessive movement during a torque-load test. Support the engine with a jack and wood block before removing the mount fasteners. Torque the new ENM-3450 to specification and recheck driveline alignment after installation.
