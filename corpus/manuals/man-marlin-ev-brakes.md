---
id: man-marlin-ev-brakes
title: Marlin EV Brakes Service Manual
area: manuals
---

# Introduction and EV Brake System Overview

This manual covers the friction and hydraulic brake system of the Marlin EV, which operates alongside regenerative braking through the drive motors. Because regeneration handles much of the deceleration, friction components see reduced duty but require correct service to ensure full braking authority when blended braking transitions to hydraulic. Technicians should consult the [Marlin EV Ignition Service Manual](doc://man-marlin-ev-ignition) before disabling the high-voltage system for any brake work. The hydraulic architecture mirrors the conventional platform documented in the [Vega Brakes Service Manual](doc://man-vega-brakes).

# Safety Precautions and High-Voltage Handling

Before servicing any brake component, follow the high-voltage shutdown sequence and confirm the service disconnect is removed and locked out. Regenerative braking can apply motor torque unexpectedly if the high-voltage system remains live, so verify zero potential at the designated test points. Wear Class 0 insulated gloves until the system is confirmed de-energized. Brake fluid is corrosive to paint and skin; flush any contact immediately with water.

# Front Brakes

The Marlin EV front axle carries the majority of friction braking load during hard stops. Front service involves brake pad set BP-7720 and brake rotor BR-7731, which must be inspected together at every service interval. Equivalent front-axle guidance is provided in the [Vega Brakes Service Manual :: Front Brake Sub-System](doc://man-vega-brakes#front-brake-sub-system).

## Front Pad and Rotor Specifications

Front pad set BP-7720 has a minimum friction-material thickness of 3 mm; replace below this limit. Front rotor BR-7731 has a minimum machining thickness stamped on the hat and must be replaced rather than turned if below specification. Always replace BP-7720 and BR-7731 as an axle set to maintain even braking. Measure rotor runout and thickness variation before reusing any BR-7731.

## Front Brake Pad Replacement Procedure

Follow PROC-BRAKE-PAD to retract the caliper piston, remove the caliper bracket bolts, and lift the caliper clear without straining the brake hose. Install new BP-7720 pads with fresh hardware and anti-squeal shims, then seat the caliper and torque the guide bolts. Pump the pedal to seat the pads before moving the vehicle. The corresponding pad-only steps appear in the [Vega Brakes Service Manual :: Front Brake Pad Replacement](doc://man-vega-brakes#front-brake-sub-system/front-brake-pad-replacement).

## Front Brake Pad and Rotor Service Procedure

When the rotor is also out of specification, follow PROC-BRAKE-FR to replace both BP-7720 and BR-7731 together. Remove the caliper and bracket, slide off the old BR-7731 rotor, and clean the hub face of all rust and debris. Install the new rotor and pads, torque all fasteners, and bed the brakes per the break-in schedule. See the [Vega Brakes Service Manual :: Front Brake Pad and Rotor Service](doc://man-vega-brakes#front-brake-sub-system/front-brake-pad-and-rotor-service).

# Rear Brakes

The rear axle uses smaller friction components because regeneration biases toward the rear on the Marlin EV. Rear service covers brake pad set BP-7722 and brake rotor BR-7733. Refer to the [Vega Brakes Service Manual :: Rear Brake Sub-System](doc://man-vega-brakes#rear-brake-sub-system) for shared rear-axle guidance.

## Rear Pad and Rotor Specifications

Rear pad set BP-7722 carries a 2 mm minimum friction-material limit; replace below this thickness. Rear rotor BR-7733 must meet its stamped minimum thickness and show runout within tolerance. Replace BP-7722 and BR-7733 together as an axle set. Inspect the integrated parking-brake function whenever the rear rotors are serviced.

## Rear Brake Pad and Rotor Service Procedure

Follow PROC-BRAKE-RR to release the electronic parking brake into service mode before retracting the rear caliper pistons. Replace BP-7722 and BR-7733, clean the hub, and torque the caliper and bracket fasteners to specification. Exit service mode and cycle the parking brake to confirm operation. The parallel rear procedure is the [Vega Brakes Service Manual :: Rear Brake Pad and Rotor Service](doc://man-vega-brakes#rear-brake-sub-system/rear-brake-pad-and-rotor-service).

# Hydraulic Actuation

Hydraulic actuation converts pedal and electronic brake-boost demand into clamping force at the calipers. The primary components are brake caliper BCAL-7760 and brake master cylinder BMC-7780. Related guidance is provided in the [Vega Brakes Service Manual :: Caliper Sub-System](doc://man-vega-brakes#caliper-sub-system).

## Brake Caliper Replacement Procedure

Replace caliper BCAL-7760 per PROC-CALIPER by clamping the flexible hose, disconnecting the hydraulic line, and capturing residual fluid. Remove the bracket bolts, transfer the pads, and install the new BCAL-7760 with a fresh banjo washer set. Torque the line fitting and bracket bolts, then bleed the caliper. Detailed steps are in the [Vega Brakes Service Manual :: Brake Caliper Replacement](doc://man-vega-brakes#caliper-sub-system/brake-caliper-replacement).

## Brake Master Cylinder Service

Master cylinder BMC-7780 supplies hydraulic pressure to all four corners and interfaces with the EV brake-boost actuator. Inspect BMC-7780 for external leaks and a sinking pedal that indicates internal seal bypass. Replace BMC-7780 as a unit; do not attempt to rebuild the bore. Bench-bleed the new BMC-7780 before installation, then bleed the full system. See the [Vega Brakes Service Manual :: Master Cylinder Service](doc://man-vega-brakes#hydraulic-sub-system/master-cylinder-service).

# Hydraulic Lines and Fluid

The hydraulic circuit is completed by brake hose BH-7745 and brake fluid BF-7790. Inspect flexible hoses for bulging, cracking, and chafing, and verify fluid condition with moisture-content testing. Reference the [Vega Brakes Service Manual :: Hydraulic Sub-System](doc://man-vega-brakes#hydraulic-sub-system) for the matching circuit overview.

## Brake Hose Replacement Procedure

Replace flexible hose BH-7745 per PROC-BRAKE-HOSE by loosening the hard-line fitting first, then the caliper-end banjo or threaded connection. Support the new BH-7745 free of suspension travel and steering sweep to prevent chafing, and use new sealing washers. Torque both fittings, then bleed the affected corner. Confirm no contact at full lock and full droop.

## Brake Fluid Flush and Bleed Procedure

Flush and bleed using fluid BF-7790 per PROC-BRAKE-FLUID, working from the corner farthest from the master cylinder inward. With the high-voltage system safely disabled, use a pressure bleeder and continue until clean BF-7790 free of air and moisture flows from each bleeder. Top off the reservoir to the full mark and verify firm pedal travel. Record the fluid moisture reading on the repair order.
