# Video notes — "Build your own 3D printable BLDC servo actuator for robotics!"

Source: local file `Downloads/vidssave.com Build your own 3D printable BLDC servo actuator for robotics! 720P.mp4`
(8 min 46 s, 720p). Notes are from a Whisper transcript of the narration plus frames sampled every
15 s. Contact sheets are in [`frames/`](frames/) — each sheet is 6 frames, 15 s apart, read left→right,
top→bottom (sheet 1 = 0:00–1:15, sheet 2 = 1:30–2:45, … sheet 6 = 7:30–8:45).

Creator: published on Cults3D as **"BLDC SERVO CO-BOT ACTUATOR"** by **RoboBiceps** (design #4717286,
AU$12, 21 files — 3MF/GCODE/STL, licence "Cults CU", tagged *Made with AI*, published 28 Jul 2026).
The cycloidal stage credits **Mishin Machine**'s open-source "Three Phase Cycloidal Drive" (Onshape
document "TRICY | MSHN"). The transcript renders the name as "Mission Machine" — the YouTube frame at
~7:30 shows the correct spelling.

---

## 1. The point of the video

- Goal of the series: a **fully 3D-printable collaborative robot (cobot)** built from scratch.
- What makes a cobot a cobot: it **monitors torque at every joint** and stops when it sees an
  unexpected load (hitting a person or object), so it can work beside people without safety fences.
- That needs **high-torque servo actuators**. Industrial ones cost hundreds to thousands of dollars;
  hobby servos are too weak. So: build a cheap, modular, printable **BLDC servo actuator**.
- Argument for BLDC over NEMA 17 steppers: steppers built the hobby-robot era (cheap, simple), but
  arms that behave like industrial ones need brushless servos.
- The author previously tried an **axial-flux motor**; it needed a steel core and they're limited to
  printing in plastic, so they switched to an off-the-shelf drone motor.

## 2. Architecture — two stages, 100:1

| Stage | Type | Ratio | Status in this video |
| --- | --- | --- | --- |
| 1 | Planetary, helical ring gear | 4:1 | **Built** |
| 2 | Cycloidal (Mishin Machine "TRICY", three-phase) | 25:1 | Shown printed + in CAD, not assembled |
| Total | | **100:1** | Future video |

**Why planetary first, cycloidal second (5:44–6:36):** planetary gears cope far better with a BLDC's
very high input RPM. Reducing 4:1 first means the cycloidal stage sees lower input speed — less
vibration, lower bearing loads, better efficiency — and already-multiplied torque. "Each stage does
what it does best": planetary = efficient first reduction, cycloidal = the big final reduction for a
robot joint.

Claim at 8:00: 100:1 puts it "in the same ballpark" as many industrial cobot joints for output torque.
**No torque, backlash, efficiency or speed figures are measured or stated anywhere in the video.**

## 3. Stage 1 hardware (as narrated)

| Item | Spec | Notes |
| --- | --- | --- |
| Motor | **5010 outrunner BLDC**, 360 KV or 750 KV | Drone motor; 50 × 10 mm stator, 4 mm shaft, 80 g, 2–6S, 20–40 A ESC rated. "Under AU$15" on Temu/AliExpress |
| Centre bearing | 10 × 22 × 6 mm (6900 size) | In the bearing carrier, supports planet carrier |
| Planet bearings | 4 × 10 × 4 mm (MR104 size), **4 per planet** | Press-fit, printed spacers between bearings and gear |
| Output bearing | 45 × 58 × 7 mm (6809 size) | Pressed into top of planet carrier |
| Motor → mount | 4 × M3 × 10 | Supplied with the motor |
| Sun gear → motor rotor | 4 × M3 × 12 | Sun gear bolts to the rotor bell, not a shaft coupling |
| Motor mount → ring gear | 4 × M4 × 40 | Ring-gear teeth face away from the motor (clearance for carrier screw heads) |

Printed parts: motor mount, helical ring gear, planet gears, planet carrier, bearing carrier, end cap.

**Build tips given:**
- Route the motor wires out through the housing opening first — keeps wiring tidy and the rotor clear.
- Do **not** power-drive the sun-gear screws — the rotor magnets grab the driver and the rotor edges
  are sharp.
- Check every planet spins with almost no resistance before closing up.
- For printed threads, the author prefers a **tight-tolerance hole that the screw self-taps** over
  heat-set inserts: "quicker, lighter, and works surprisingly well."
- Hand-turn the whole train before sealing; fix tightness then, not later.

## 4. Stage 2 (glimpsed, ~6:00–8:00)

- Printed cycloidal disk with ~6 output-pin holes and a central bearing (6:00–6:15).
- Onshape configuration panel for "TRICY | MSHN" (7:45): pin Ø 5 mm, pin-centre Ø 67 mm,
  **25 pins**, eccentricity 0.8 mm, cam bearing 10 × 22 × 7 mm, ring height 5 mm, BB Ø 5 mm
  (rolling elements instead of pins appear to be an option). It is a *configurable* parametric model.
- Joint CAD (6:30, 7:15): motor + planetary + cycloidal stacked coaxially inside a red/black joint
  housing, with what looks like a **PCB on the back face** (green board, 6:45) — likely driver/encoder.
- A full 6-axis cobot arm in CAD (sheets 1, 6) — the end goal.

## 5. What is *not* in the video (gaps)

- **No electronics or control at all.** No driver (FOC controller, ODrive, SimpleFOC, MKS etc.),
  no encoder, no current sensing — yet the whole cobot premise rests on torque monitoring.
- No test: no load, torque, backlash, speed, heat, or efficiency numbers.
- No stage-2 assembly, no 100:1 test.
- The motor was chosen with ChatGPT's help (8:12) — no derivation shown.
- Several opening b-roll shots (stator coil grid, "MASON-BOT 100" bricklaying robot, factory cobot)
  look AI-generated/stock — not the author's hardware.

## 6. Why this matters for *your* summit stand

The video's actuator is **literally your two existing projects stacked together**: a planetary first
stage feeding a cycloidal second stage. You already have:

- a working 16:1 planetary (measured ≈2 N·m, ≈50 % η, ≈18 arcmin) — `3d-printable-planetary-gearbox/`
- a print-ready 15:1 cycloidal (author-measured ≈10× torque, ≈66 % η, back-drivable) — `cycloidal-drive-print-ready/`
- an electronics brief that already asks for an **AS5600 encoder, homing, backlash handling and
  stall detection** — i.e. half the cobot safety story — plus an AS5600 mount in CAD.

What the video skips — closed-loop control, torque sensing, collision stop, and real measured
numbers — is exactly what would make a third project *yours* rather than another rebuild, and it is
squarely on-theme for the BTS 2026 **AI & Robotics Pavilion**.

Things to keep in mind: RoboBiceps' files are paid, licensed (Cults CU) designs, and the cycloidal
stage is Mishin Machine's. Anything you derive from them needs credit and a licence check; an
original design of your own avoids the question entirely.
