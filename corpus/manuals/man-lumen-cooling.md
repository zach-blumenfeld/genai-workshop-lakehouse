---
id: man-lumen-cooling
title: Lumen Cooling Service Manual
area: manuals
---

# Cooling System Overview

The Lumen cooling system regulates engine temperature by circulating coolant through the block, radiator, and heater core. Core components include the thermostat TSTAT-6100, water pump WP-6120, radiator RAD-6140, cooling fan module FAN-6160, and the upper radiator hose RHOSE-6180. Proper operation depends on correct coolant level, flow, and fan control across all load conditions. The comparable platform architecture is documented in the [Harrier Cooling Service Manual](doc://man-harrier-cooling).

# Safety and Service Precautions

Never open the cooling system while hot, as pressurized coolant can cause severe burns. Allow the engine to cool, then relieve pressure slowly before removing the cap. Use only the specified coolant type and dispose of used coolant according to local regulations. Keep the cooling fan FAN-6160 disabled during hands-on service to prevent unexpected activation.

# Diagnostic Trouble Codes

Cooling faults are commonly indicated by stored diagnostic trouble codes confirmed with live temperature and fan data. The codes addressed in this manual are P0128, P0480, and P0217. Capture freeze-frame data and verify coolant level before beginning component diagnosis. Each code is detailed in the subsections below.

## P0128 Coolant Thermostat Below Regulating Temperature

P0128 sets when the engine fails to reach the calibrated operating temperature within the expected time, usually due to a thermostat TSTAT-6100 stuck open. Verify actual coolant temperature against the model's regulating value using a scan tool. Confirm the coolant temperature sensor reads accurately before condemning TSTAT-6100. The equivalent regulation diagnosis appears in [Harrier Cooling Service Manual :: Temperature Regulation](doc://man-harrier-cooling#temperature-regulation).

## P0480 Cooling Fan Control Circuit

P0480 indicates a fault in the cooling fan control circuit affecting the fan module FAN-6160. Inspect the fan relay, control driver, and harness for open or shorted conditions. Command the fan with a scan tool and verify FAN-6160 responds at the expected speeds. The comparable fan circuit guidance is in [Harrier Cooling Service Manual :: Cooling Fan Module Service](doc://man-harrier-cooling#heat-rejection/cooling-fan-module-service).

## P0217 Engine Over-Temperature Condition

P0217 sets when the engine exceeds its maximum safe temperature, often due to low coolant, a failed water pump, or a restricted radiator RAD-6140. Inspect for leaks, verify fan operation, and check radiator airflow and flow restriction. Address the over-temperature root cause before clearing the code to prevent engine damage. See [Harrier Cooling Service Manual :: Heat Rejection](doc://man-harrier-cooling#heat-rejection) for the related diagnosis.

# Coolant Circuit and Flush Service

The coolant circuit must be kept clean and at the correct concentration to prevent corrosion and overheating. Use PROC-COOLANT to drain, flush, and refill the system at the specified interval or whenever contamination is found. Bleed all air from the system to avoid hot spots and false temperature readings. The comparable service is in [Harrier Cooling Service Manual :: Coolant Service](doc://man-harrier-cooling#coolant-service).

## Coolant Flush and Refill Procedure

Follow PROC-COOLANT to drain the system at the radiator and block drains, flush with clean water, then refill with the specified coolant mixture. Open the bleed valves and run the engine through warm-up cycles to purge trapped air. Confirm the level stabilizes and no air pockets remain before returning the vehicle to service. The equivalent steps are in [Harrier Cooling Service Manual :: Coolant Flush and Refill Procedure](doc://man-harrier-cooling#coolant-service/coolant-flush-and-refill-procedure).

# Thermostat Sub-System

The thermostat sub-system uses TSTAT-6100 to regulate coolant flow and bring the engine to operating temperature quickly. A thermostat stuck open causes slow warm-up and sets P0128, while a stuck-closed unit can cause overheating. Verify opening temperature and seating during diagnosis.

## Thermostat Replacement Procedure

Use PROC-THERMOSTAT to replace the thermostat TSTAT-6100 after draining coolant below the housing level. Install a new gasket or O-ring, observe the correct orientation of the jiggle valve, and torque the housing to specification. Refill and bleed the system, then confirm the engine reaches regulating temperature to clear P0128. The comparable procedure is in [Harrier Cooling Service Manual :: Thermostat Replacement Procedure](doc://man-harrier-cooling#temperature-regulation/thermostat-replacement-procedure).

# Water Pump Sub-System

The water pump sub-system circulates coolant through the engine and radiator. The original pump WP-6120 has been superseded by the revised unit WP-6122, which incorporates an improved seal design. Always verify the correct part number before ordering, as WP-6120 and WP-6122 differ in seal and impeller specification. See [Harrier Cooling Service Manual :: Water Pump Identification and Supersession](doc://man-harrier-cooling#coolant-circulation/water-pump-identification-and-supersession).

## Water Pump Replacement Procedure

Follow PROC-WATER-PUMP to replace the water pump, installing the current WP-6122 in place of the superseded WP-6120. Remove the drive belt and any timing components required for access, then clean the mounting surface before fitting a new gasket. Torque fasteners in sequence to specification and verify there are no leaks after refill. The equivalent steps are in [Harrier Cooling Service Manual :: Water Pump Replacement Procedure](doc://man-harrier-cooling#coolant-circulation/water-pump-replacement-procedure).

# Radiator and Hose Sub-System

The radiator and hose sub-system rejects heat through the radiator RAD-6140 and routes coolant via the upper radiator hose RHOSE-6180. A restricted or damaged RAD-6140 reduces heat rejection and can contribute to over-temperature conditions. Inspect RHOSE-6180 for swelling, cracking, or soft spots during service. See [Harrier Cooling Service Manual :: Heat Rejection](doc://man-harrier-cooling#heat-rejection) for the related overview.

## Radiator Replacement Procedure

Use PROC-RAD to replace the radiator RAD-6140 after draining the system and removing the fan shroud and hoses. Transfer any brackets and insulators to the new unit and ensure the lower mounts seat correctly. Refill, bleed, and verify there are no leaks and that operating temperature stabilizes. The comparable procedure is in [Harrier Cooling Service Manual :: Radiator Replacement Procedure](doc://man-harrier-cooling#heat-rejection/radiator-replacement-procedure).

## Upper Radiator Hose Replacement

Replace the upper radiator hose RHOSE-6180 whenever it shows signs of age, swelling, or leakage. Drain coolant below the hose level, release the clamps, and remove the hose without twisting the radiator or thermostat housing necks. Install the new RHOSE-6180 with fresh clamps positioned clear of the bead. See [Harrier Cooling Service Manual :: Radiator Hose Replacement](doc://man-harrier-cooling#heat-rejection/radiator-hose-replacement) for the equivalent steps.

# Cooling Fan Sub-System

The cooling fan sub-system uses the electric fan module FAN-6160 to draw air through the radiator at low vehicle speeds. A control circuit fault sets P0480 and can lead to overheating in traffic. Verify commanded operation and current draw during diagnosis.

## Cooling Fan Module Service

Service the cooling fan module FAN-6160 when P0480 is confirmed and the fan fails to respond to commands. Inspect the connector, relay, and control driver before replacing the module. After installing FAN-6160, command the fan through all speeds and verify correct rotation and airflow direction. The comparable guidance is in [Harrier Cooling Service Manual :: Cooling Fan Module Service](doc://man-harrier-cooling#heat-rejection/cooling-fan-module-service).
