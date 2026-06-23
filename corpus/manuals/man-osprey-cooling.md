---
id: man-osprey-cooling
title: Osprey Cooling Service Manual
area: manuals
---

# Introduction and Safety Precautions

This manual covers diagnosis and service of the Osprey engine cooling system. Always allow the engine to cool fully before opening the cooling circuit, as pressurized coolant can cause severe scald injuries. Wear eye protection and dispose of used coolant in accordance with local environmental regulations. Sections in this manual share structure with the [Osprey Fuel Service Manual](doc://man-osprey-fuel) and the platform-equivalent [Harrier Cooling Service Manual](doc://man-harrier-cooling).

# Cooling System Overview

The Osprey cooling system circulates coolant through the engine block and cylinder head, regulating flow with thermostat TSTAT-6100 and driving circulation with water pump WP-6120, superseded on later builds by WP-6122. Heat is rejected through radiator RAD-6140, assisted by electric cooling fan FAN-6160 under PCM control. Upper and lower radiator hoses are serviced as kit RHOSE-6180. The corresponding architecture on the sister platform is documented in the [Harrier Cooling Service Manual](doc://man-harrier-cooling).

# Coolant Circuit and Service

Coolant enters the pump inlet, passes through the block and head, and returns through the radiator core via hose kit RHOSE-6180. The complete drain, flush, and refill sequence is captured in procedure PROC-COOLANT and must be followed to avoid trapped air pockets. Cross-platform technicians should compare this circuit against [Harrier Cooling Service Manual :: Coolant Service](doc://man-harrier-cooling#coolant-service).

## Coolant Flush and Refill Procedure

Procedure PROC-COOLANT begins by draining the radiator at the petcock, then back-flushing the block until effluent runs clear. Inspect hose kit RHOSE-6180 for cracking or swelling and replace any degraded section before refilling. Fill with the specified coolant blend, run the engine with the cap off to purge air, and top off as the level drops. The equivalent fill-and-bleed steps are mirrored in [Harrier Cooling Service Manual :: Coolant Flush and Refill Procedure](doc://man-harrier-cooling#coolant-service/coolant-flush-and-refill-procedure).

# Thermostat Subsystem

Thermostat TSTAT-6100 governs coolant flow to bring the engine to operating temperature quickly and hold it within range. A stuck-open thermostat prevents the engine from reaching closed-loop temperature and commonly sets DTC P0128. Temperature regulation on the related chassis is covered in [Harrier Cooling Service Manual :: Temperature Regulation](doc://man-harrier-cooling#temperature-regulation).

## Thermostat Faults

DTC P0128 (Coolant Thermostat Below Regulating Temperature) typically indicates a thermostat TSTAT-6100 that is stuck open or slow to close. Before condemning the thermostat, verify the coolant temperature sensor reading and confirm the engine actually fails to reach the regulation threshold within the expected warm-up window. A faulty thermostat is the most frequent root cause of P0128.

### Thermostat Replacement Procedure

Procedure PROC-THERMOSTAT directs the technician to drain coolant below the housing, remove the housing bolts, and extract thermostat TSTAT-6100 with its gasket. Install the new thermostat with the jiggle valve oriented upward, torque the housing to spec, and refill per the coolant procedure. Clear DTC P0128 and verify the engine reaches regulating temperature on a road test. The platform-equivalent steps are documented in [Harrier Cooling Service Manual :: Thermostat Replacement Procedure](doc://man-harrier-cooling#temperature-regulation/thermostat-replacement-procedure).

# Water Pump Subsystem

The water pump drives coolant circulation throughout the engine and radiator. Early Osprey builds use pump WP-6120, which was superseded by WP-6122 following a seal revision. Coolant circulation on the sister platform is described in [Harrier Cooling Service Manual :: Coolant Circulation](doc://man-harrier-cooling#coolant-circulation).

## Water Pump Variants and Seal Revision

Pump WP-6120 was the original-fitment unit; field reports of weep-hole seepage led to the revised WP-6122, which carries an upgraded mechanical seal. WP-6122 fully supersedes WP-6120 and should be used for all replacements regardless of original fitment. Confirm the impeller vane count matches the application before installation. Supersession handling is mirrored in [Harrier Cooling Service Manual :: Water Pump Identification and Supersession](doc://man-harrier-cooling#coolant-circulation/water-pump-identification-and-supersession).

### Water Pump Replacement Procedure

Procedure PROC-WATER-PUMP requires removing the accessory drive belt and pump pulley before unbolting the pump body. Discard pump WP-6120 and install the superseding WP-6122 with a new gasket and a thin bead of sealant where specified. Torque the bolts in a crossing pattern, refill the cooling system, and check for leaks at operating temperature. See [Harrier Cooling Service Manual :: Water Pump Replacement Procedure](doc://man-harrier-cooling#coolant-circulation/water-pump-replacement-procedure) for the equivalent platform steps.

# Radiator and Cooling Fan Subsystem

Radiator RAD-6140 transfers engine heat to ambient air, with electric fan FAN-6160 providing forced airflow at low vehicle speeds. A fan control circuit fault sets DTC P0480, while a genuine loss of cooling capacity can escalate to engine over-temperature DTC P0217. Heat rejection on the related chassis is detailed in [Harrier Cooling Service Manual :: Heat Rejection](doc://man-harrier-cooling#heat-rejection).

## Cooling Fan Control Faults

DTC P0480 (Cooling Fan 1 Control Circuit) points to a fault in the FAN-6160 control circuit, relay, or fan motor. Inspect the fan relay, connector, and motor draw before replacing the fan assembly. Confirm the PCM commands the fan on at the calibrated temperature threshold. Module-level fan service is covered in [Harrier Cooling Service Manual :: Cooling Fan Module Service](doc://man-harrier-cooling#heat-rejection/cooling-fan-module-service).

## Engine Over-Temperature Condition

DTC P0217 (Engine Over-Temperature Condition) indicates the coolant temperature exceeded the safe operating ceiling. Investigate low coolant level, a failed water pump, a stuck thermostat, or inadequate airflow through radiator RAD-6140 before clearing the code. Continued operation with P0217 active risks head gasket and cylinder head damage.

### Radiator Replacement Procedure

Procedure PROC-RAD begins by draining the system and disconnecting the upper and lower hoses, transmission cooler lines, and the FAN-6160 shroud assembly. Lift radiator RAD-6140 from its lower mounts, transfer the fan shroud to the replacement core, and reinstall with new isolators. Refill, bleed, and confirm there is no DTC P0217 recurrence under load. The platform-equivalent steps appear in [Harrier Cooling Service Manual :: Radiator Replacement Procedure](doc://man-harrier-cooling#heat-rejection/radiator-replacement-procedure).
