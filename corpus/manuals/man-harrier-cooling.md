---
id: man-harrier-cooling
title: Harrier Cooling Service Manual
area: manuals
---

# Introduction and Cooling System Overview

This manual covers diagnosis and service of the Harrier engine cooling system, including the coolant circuit, thermostat, water pump, radiator, and cooling fan module. The system maintains regulated operating temperature under all load conditions and protects the engine from over-temperature damage. Technicians should reference the [Harrier Engine Service Manual](doc://man-harrier-engine) for related powertrain torque values and component access. The architecture closely parallels the platform documented in the [Lumen Cooling Service Manual](doc://man-lumen-cooling), which shares the same regulating strategy.

# Safety Precautions and Coolant Handling

Never open the cooling system while the engine is hot, as pressurized coolant can cause severe burns. Allow the system to cool below 50 C before removing the pressure cap or disconnecting any hose. Used coolant is toxic and must be captured and disposed of in accordance with local hazardous-waste regulations. Wear chemical-resistant gloves and eye protection throughout all coolant handling operations.

# Coolant Service

Routine coolant service preserves corrosion protection and heat-transfer performance across the circuit. The PROC-COOLANT procedure governs the recommended drain, flush, and refill interval for the Harrier platform. Use only the specified ethylene-glycol formulation to avoid seal degradation. The equivalent coolant circuit work is described in the [Lumen Cooling Service Manual :: Coolant Circuit and Flush Service](doc://man-lumen-cooling#coolant-circuit-and-flush-service).

## Coolant Flush and Refill Procedure

Follow PROC-COOLANT to drain the system at the radiator petcock and lower hose, then back-flush the block and heater core with clean water. Refill with a 50/50 coolant mixture and bleed air from the high-point bleeder until a steady stream is observed. Run the engine to operating temperature with the cap off to purge trapped air, then top off and verify level when cool. The analogous step-by-step is documented in the [Lumen Cooling Service Manual :: Coolant Flush and Refill Procedure](doc://man-lumen-cooling#coolant-circuit-and-flush-service/coolant-flush-and-refill-procedure).

# Temperature Regulation

The thermostat regulates coolant flow to the radiator to maintain target operating temperature. The Harrier uses thermostat assembly TSTAT-6100, which begins to open at approximately 88 C and is fully open by 102 C. A stuck-open thermostat causes slow warm-up and may set diagnostic code P0128. Inspect the TSTAT-6100 seal and housing for cracks whenever the system is opened.

## Thermostat Replacement Procedure

Replace TSTAT-6100 per PROC-THERMOSTAT by draining coolant below the housing, removing the outlet housing bolts, and extracting the old thermostat and seal. Install the new TSTAT-6100 with the jiggle valve oriented to the top to aid bleeding, then torque the housing fasteners to specification. Refill and bleed the system following the coolant procedure above. Comparable instructions appear in the [Lumen Cooling Service Manual :: Thermostat Replacement Procedure](doc://man-lumen-cooling#thermostat-sub-system/thermostat-replacement-procedure).

# Coolant Circulation

The water pump drives coolant through the block, head, and radiator circuit whenever the engine is running. Inspect the pump for shaft play, weep-hole seepage, and bearing noise during any cooling service. A failing pump reduces flow and can trigger an over-temperature condition. See the [Lumen Cooling Service Manual :: Water Pump Sub-System](doc://man-lumen-cooling#water-pump-sub-system) for shared diagnostic guidance.

## Water Pump Identification and Supersession

Early Harrier units shipped with water pump WP-6120, which has been superseded by WP-6122 featuring an upgraded ceramic seal and revised impeller. When servicing a vehicle still equipped with WP-6120, always install the superseding WP-6122, as the earlier part is no longer stocked. Both pumps share the same mounting pattern and gasket, so no bracket changes are required. Record the supersession on the repair order.

## Water Pump Replacement Procedure

Perform PROC-WATER-PUMP by draining coolant, removing the accessory drive belt, and unbolting the pump from the timing cover. Clean the sealing surface completely before installing the new WP-6122 with a fresh gasket, and torque fasteners in a crossing pattern to specification. Refill, bleed, and pressure-test the system before returning the vehicle to service. The parallel procedure is the [Lumen Cooling Service Manual :: Water Pump Replacement Procedure](doc://man-lumen-cooling#water-pump-sub-system/water-pump-replacement-procedure).

# Heat Rejection

Heat rejection components transfer engine heat to ambient air and include radiator RAD-6140, cooling fan module FAN-6160, and upper radiator hose RHOSE-6180. Inspect the radiator core for blockage, the fan module for cracked blades or seized motor, and RHOSE-6180 for swelling or soft spots. Restricted airflow or a degraded hose can lead to over-temperature faults. Replace any component showing damage during cooling service.

## Radiator Replacement Procedure

Replace radiator RAD-6140 per PROC-RAD by draining the system, disconnecting the inlet and outlet hoses, and removing the transmission cooler lines where fitted. Detach the fan shroud, unbolt the radiator from its mounts, and lift the assembly clear. Install the new RAD-6140 with intact rubber isolators, reconnect all lines, then refill and bleed.

## Cooling Fan Module Service

The cooling fan module FAN-6160 is controlled by the engine control module through a relay and pulls air across RAD-6140 at low vehicle speed. Test FAN-6160 by commanding the fan with a scan tool and confirming current draw within specification. A fan circuit failure commonly sets P0480. Replace the FAN-6160 assembly as a unit; individual motors are not serviced separately.

## Radiator Hose Replacement

Replace upper radiator hose RHOSE-6180 whenever it shows cracking, swelling, or chafing. Drain coolant below the hose level, release the spring or worm clamps, and twist the hose free of the radiator and thermostat housing necks. Seat the new RHOSE-6180 fully on both necks and secure with new clamps positioned clear of the bead. Refill and inspect for leaks under pressure.

# Cooling System Diagnosis

Cooling system faults are diagnosed using stored diagnostic trouble codes and live data. The Harrier may set P0128 for thermostat below regulating temperature, P0480 for a cooling fan control circuit fault, and P0217 for an engine over-temperature condition. Always confirm coolant level and concentration before pursuing a code. The shared code definitions are listed in the [Lumen Cooling Service Manual :: Diagnostic Trouble Codes](doc://man-lumen-cooling#diagnostic-trouble-codes).

## Thermostat and Temperature Faults

Code P0128 indicates the coolant did not reach regulating temperature within the expected time and most often points to a stuck-open TSTAT-6100. Code P0217 indicates an over-temperature condition and requires inspection of the water pump, coolant level, and fan operation before clearing. Verify the coolant temperature sensor reading against an infrared thermometer when diagnosing either code. Refer to the [Lumen Cooling Service Manual :: P0128 Coolant Thermostat Below Regulating Temperature](doc://man-lumen-cooling#diagnostic-trouble-codes/p0128-coolant-thermostat-below-regulating-temperature) and the [Lumen Cooling Service Manual :: P0217 Engine Over-Temperature Condition](doc://man-lumen-cooling#diagnostic-trouble-codes/p0217-engine-over-temperature-condition).

## Cooling Fan Circuit Faults

Code P0480 is set when the control module detects a fault in the cooling fan control circuit feeding FAN-6160. Inspect the fan relay, connector, and harness for corrosion or open circuits before condemning the fan module. Command the fan on with a scan tool and back-probe the supply and ground to isolate the fault. Cross-reference the [Lumen Cooling Service Manual :: P0480 Cooling Fan Control Circuit](doc://man-lumen-cooling#diagnostic-trouble-codes/p0480-cooling-fan-control-circuit) for the matching test sequence.
