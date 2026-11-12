# BOM — QDD planetary actuator v1.0

One actuator, plus the bench stand and test arm. Quantities come from the CAD
(`cad/qdd_actuator_v1.0.FCStd`). Prices are only given where they were actually checked;
everything else says "not checked" rather than a guess.

## 1. Printed parts (PLA)

| Qty | File (`cad/stl/`) | Size as printed (mm) | Solid volume (cm³) | Notes |
| ---: | --- | --- | ---: | --- |
| 1 | `x1_Housing_RingGear.stl` | 78 × 78 × 53 | 126.4 | Base, motor cavity and 60T ring gear in one piece. Print base down, no supports. |
| 1 | `x1_Sun_Gear.stl` | 34 × 34 × 22.5 | 5.4 | 12T. **Do not print until the rotor bolt circle is measured** (see README). 100 % infill. |
| 3 | `x3_Planet.stl` | 25.1 × 25.1 × 12 | 3.4 each | 24T, two 686 bearing seats. 100 % infill. |
| 1 | `x1_Carrier_Rear.stl` | 54 × 54 × 4.5 | 7.9 | Flat side down. |
| 1 | `x1_Carrier_Front_Output.stl` | 54 × 54 × 27.3 | 25.1 | Exported hub-down. **Needs supports** under the Ø54 plate. |
| 1 | `x1_Front_Cover.stl` | 78 × 78 × 16 | 40.7 | Exported outer face down, no supports. |
| 1 | `x1_Output_Flange.stl` | 41 × 41 × 6 | 7.0 | |
| 1 | `x1_Rear_Cap_Encoder.stl` | 78 × 78 × 11.8 | 37.8 | Holds the AS5600 board. |
| 1 | `x1_Magnet_Cup.stl` | 9 × 9 × 6 | 0.3 | Presses on the 4 mm shaft, holds the magnet. |
| | **Actuator subtotal** | | **260.8** | ≈ 323 g if printed solid (1.24 g/cm³); expect roughly 180–220 g with normal walls and infill (estimate). |
| 1 | `x1_Test_Arm.stl` | 127.5 × 41 × 5 | 11.4 | Load holes at 50 mm and 100 mm from the axis. |
| 1 | `x1_Stand_Lower.stl` | 140 × 49.8 × 24 | 67.2 | Saddle with feet. |
| 1 | `x1_Stand_Upper.stl` | 100 × 44.8 × 24 | 22.7 | Clamp strap. |
| 1 | `TEST_ring_slice.stl` | 70 × 70 × 13 | 13.8 | Fit test only — print with one sun and one planet first. |

## 2. Motor, bearings, pins

| Qty | Item | Spec | Price | Source / status |
| ---: | --- | --- | --- | --- |
| 1 | 5010 360 KV outrunner | Ø50 × 26 mm, 12N14P, 4 mm shaft, 67 mΩ, 20 A max | ₹2,239 | robu.in SKU 45571, listed in stock 11 Nov 2026 |
| 6 | 686 ZZ bearing | 6 × 13 × 5 mm | ₹26 each | onlyscrews.in price from the cycloidal BOM (Sep 2026) |
| 1 | 6807 bearing | 35 × 47 × 7 mm | ₹98 | IndiaMART price from the cycloidal BOM (Sep 2026) |
| 3 | Steel pin | Ø6 × 22 mm | not checked | Same size as the planet pins in the 16:1 planetary |
| 1 | Diametric magnet | Ø6 × 2.5 mm | — | Supplied with the AS5600 module |

## 3. Fasteners (all M3)

| Qty | Fastener | Where | How the length was set |
| ---: | --- | --- | --- |
| 25 | Heat-set insert M3 × 5 (OD ≈ 4.4) | 6 housing front, 4 housing rear, 3 carrier posts, 4 output hub, 6 output flange, 2 stand | Pockets are Ø4.2, 5.5–7 mm deep |
| 6 | Socket head M3 × 16 | Front cover → housing | 10 mm under the head + insert |
| 4 | Socket head M3 × 14 | Rear cap → housing | 8.65 mm under the head + insert |
| 4 | Socket head M3 × 8 | Output flange → carrier hub | 2.8 mm under the head + insert |
| 3 | Countersunk M3 × 8 | Rear carrier plate → posts | 4 mm plate + insert |
| 4 | Socket head M3 × 6 | Sun gear → rotor | 1.8 mm under the head; **check the rotor's thread depth** |
| 4 | M3 screws | Motor base → housing | Use the 4 screws supplied with the motor; 2.4 mm under the head |
| 4 | Socket/pan head M3 × 5 | AS5600 board → rear cap | Self-taps into Ø2.6 holes, 3.7 mm deep |
| 6 | Socket head M3 × 10 | Test arm → output flange | 5 mm arm + insert |
| 2 | Socket head M3 × 20 | Stand strap → saddle | 16 mm strap + insert |

Insert price in the cycloidal BOM was ₹4.60 each and M3 socket heads about ₹3.20 each
(onlyscrews.in, Sep 2026). On those prices the fasteners come to roughly ₹250.

## 4. Electronics — home-built FOC controller

| Qty | Item | Purpose | Price | Status |
| ---: | --- | --- | --- | --- |
| 1 | ESP32 dev board | Runs SimpleFOC | — | In hand |
| 1 | AS5600 breakout | Rotor angle | — | In hand |
| 3 | BTS7960 (IBT-2) module | Three half-bridges (2 needed, 1 spare) | not checked | Buy |
| 2 | ACS712 20 A module | Phase current sensing | not checked | Buy |
| 1 | SimpleFOCmini | Low-current fallback driver | ₹729 | robu.in SKU R261566, listed in stock 11 Nov 2026 |
| 1 | Fuse holder + 10 A fuses | Protects motor and battery | not checked | Buy |
| 1 | Electrolytic capacitor ≥ 1000 µF, ≥ 25 V | Bus capacitor at the bridge supply | not checked | Buy |
| 1 | Proto board, 16 AWG silicone wire, XT60 or similar | Power wiring (soldered, not breadboard) | not checked | Buy |
| 1 | 12 V supply ≥ 10 A, or the LiPo with the fuse | Power | — | LiPo in hand |

## 5. Known cost

| | ₹ |
| --- | ---: |
| Motor | 2,239 |
| 6 × 686 + 1 × 6807 | 254 |
| Fasteners and inserts (approx.) | 250 |
| SimpleFOCmini fallback | 729 |
| **Checked subtotal** | **≈ 3,470** |

Not included because the prices were not checked: steel pins, BTS7960 modules, ACS712 modules,
fuse, capacitor, wire, power supply, filament.
