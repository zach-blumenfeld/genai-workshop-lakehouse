---
id: man-ridgeline-hd-body
title: Ridgeline HD Body Service Manual
area: manuals
---

# Body Electrical System Overview

The Ridgeline HD body electrical system manages exterior lighting, wiper and washer functions, and heated mirrors through the body control module over the serial data network. The module monitors supply voltage and stored configuration to ensure correct feature operation across trim levels. For a comparable architecture on a related platform, refer to the [Kestrel Body Service Manual :: Body Electrical System Overview](doc://man-kestrel-body#body-electrical-system-overview). Suspension-related ride-height inputs that affect headlamp leveling are documented in the [Ridgeline HD Suspension Service Manual](doc://man-ridgeline-hd-suspension).

# Body System Diagnosis

Diagnosis begins by retrieving stored body codes and confirming supply voltage and module configuration before component testing. The two most common faults are B1318 (Battery Voltage Low) and B2477 (Module Configuration Failure). Always verify the underlying condition, since a low-voltage fault can cascade into apparent feature failures. A parallel code reference is available in the [Kestrel Body Service Manual :: Body Diagnostic Trouble Code Reference](doc://man-kestrel-body#diagnosis/body-diagnostic-trouble-code-reference).

## Low Battery Voltage Body Control Diagnosis

Code B1318 indicates the body control module detected supply voltage below the operating threshold, which can disable or impair lighting, wiper, and mirror functions. Inspect the module power and ground circuits, charging output, and battery condition before replacing any actuator. Measure voltage at the module connector under load and compare to specification. Refer to the [Kestrel Body Service Manual :: Low Battery Voltage Diagnosis](doc://man-kestrel-body#diagnosis/low-battery-voltage-diagnosis) for the analogous procedure.

## Module Configuration Failure Diagnosis

Code B2477 is set when the module configuration does not match the expected vehicle build or when programming is incomplete. Verify the vehicle configuration data and reprogram the module with the latest calibration before condemning hardware. A B2477 frequently follows module replacement performed without the required configuration step. See the [Kestrel Body Service Manual :: Module Configuration Failure Diagnosis](doc://man-kestrel-body#diagnosis/module-configuration-failure-diagnosis) for related steps.

# Exterior Lighting Sub-System

The exterior lighting sub-system provides headlamp, marker, and signal illumination controlled by the body control module. Lighting faults are commonly traced to module configuration, supply voltage, or the lamp assembly itself. Refer to the [Kestrel Body Service Manual :: Lighting Sub-System](doc://man-kestrel-body#lighting-sub-system) for the comparable system.

## Headlamp Assembly Identification

The service headlamp assembly is part number HLMP-7020, an LED projector unit matched to the Ridgeline HD front fascia. Verify the part number against the trim level, since lower trims use a different reflector assembly. Inspect the connector and mounting tabs for damage during service. Confirm beam pattern and aim after any replacement.

### Headlamp Assembly Replacement Procedure

Procedure PROC-HEADLAMP directs removal of the front fascia fasteners to access the lamp mounting points. Disconnect the connector and remove the retaining bolts to free HLMP-7020 from the body. After installing the replacement, a B2477 may require the module be reconfigured to recognize the lamp's adaptive features. Verify operation and aim, then compare to the [Kestrel Body Service Manual :: Headlamp Assembly Replacement Procedure](doc://man-kestrel-body#lighting-sub-system/headlamp-assembly-replacement-procedure).

# Wiper and Washer Sub-System

The wiper and washer sub-system clears the windshield using a reversible wiper motor and an electric washer pump. Intermittent wiper operation is frequently caused by low supply voltage or a worn motor. Refer to the [Kestrel Body Service Manual :: Wiper and Washer Sub-System](doc://man-kestrel-body#wiper-and-washer-sub-system) for the comparable system.

## Wiper Motor Specifications

The service wiper motor is part number WIPM-7000, a reversible unit with an integrated park switch and module communication. Verify the linkage geometry and mounting pattern match the original before installation. Inspect the linkage pivots for binding whenever the motor is serviced. Confirm park position and sweep range after installation.

### Wiper Motor Replacement Procedure

Procedure PROC-WIPER covers removing the cowl panel and wiper arms to access the motor and linkage. A B1318 low-voltage condition can cause the motor to stall or park incorrectly, so confirm supply voltage before replacing WIPM-7000. Disconnect the connector, remove the linkage and mounting bolts, and install the replacement. Verify park and sweep operation, then compare to the [Kestrel Body Service Manual :: Wiper Motor Replacement Procedure](doc://man-kestrel-body#wiper-and-washer-sub-system/wiper-motor-replacement-procedure).

## Windshield Washer Pump Service

The windshield washer pump delivers fluid from the reservoir to the nozzles on demand. A pump that runs without spraying usually indicates a clogged nozzle or a failed pump impeller. Inspect washer pump part number WSHLD-7060 and its grommet seal for leaks during service. Replace the pump if it fails to prime or is noisy, referring to the [Kestrel Body Service Manual :: Windshield Washer Pump Service](doc://man-kestrel-body#wiper-and-washer-sub-system/windshield-washer-pump-service).

# Mirror Sub-System

The mirror sub-system provides power adjustment and heating of the exterior mirrors controlled by the body control module. Mirror heater faults are commonly related to supply voltage or a broken heater element. The Kestrel diagnosis flow in the [Kestrel Body Service Manual :: Diagnosis](doc://man-kestrel-body#diagnosis) covers comparable symptoms.

## Heated Door Mirror Service

The service heated door mirror is part number DRMR-7040, which integrates the glass, heater element, and adjustment actuator. A B1318 low-voltage condition can prevent the heater from reaching temperature, so verify supply voltage before replacing the mirror. Test the heater element resistance and actuator operation against specification. Replace DRMR-7040 as an assembly if either function is out of range.
