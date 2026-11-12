You're my ideation partner for the third project I'll exhibit at **Bengaluru Tech Summit 2026**
(17–19 November 2026, BIEC, Bengaluru; theme "AI & Beyond"; there is a dedicated **AI & Robotics
Pavilion**). Today is 11 November 2026, so I have **about 6 days** to design, print, wire and test
whatever we pick. Help me think, don't build yet.

## Read these first (all in this workspace)

1. `third-project/video-notes.md` — my notes on a YouTube video ("Build your own 3D printable BLDC
   servo actuator for robotics!") that inspired this. Contact sheets of the video are in
   `third-project/frames/`, take a look at them.
2. `3d-printable-planetary-gearbox/README.md` and `electronics-brief.md`: project 1, a two-stage
   16:1 planetary gearbox on a NEMA 17. Measured: ≈2 N·m output, ≈50 % efficiency, ≈18 arcmin backlash.
   The electronics brief specs an AS5600 encoder, homing, backlash handling and stall detection.
3. `cycloidal-drive-print-ready/README.md`, `BOM.md` and `ASSEMBLY.md`: project 2, a 15:1 cycloidal
   drive on a NEMA 17, 106 printed parts, Bambu P1S/H2D 3MF projects ready.

Both existing projects are rebuilds of **HowToMechatronics** designs. I'm also refining them for
the summit, but this session is about the **third** project.

## What I want from the third project

- Something I can honestly call **my own design or my own contribution**, not another rebuild.
- It should tie my stand together: ideally projects 1 and 2 plus the new one tell one story.
  (Note from the video: its actuator is a planetary stage feeding a cycloidal stage, i.e. my two
  projects stacked. The video skips electronics, control, torque sensing and any measured numbers.)
- It has to **run live at a booth** for 3 days: robust, safe for visitors to touch or interact with,
  and understandable in 30 seconds.
- It should fit the "AI & Beyond" / AI & Robotics framing without being AI-washed.

## How I want to work

1. Read the files above, then ask me what you need to know before proposing anything: what
   printers, motors, drivers, microcontrollers, encoders and bearings I have; what I can order and
   receive by ~14 Nov; budget; my electronics and firmware experience; whether I'm working alone.
   Ask a few questions at a time, not a wall of them.
2. Then propose **4–6 distinct concepts**, ranging from safe to ambitious. For each: a one-line pitch,
   what a visitor sees and does at the booth, how it connects to projects 1 and 2, what's original
   about it, the key parts, and the biggest risk.
3. Score them in a table against: buildable in 6 days with my resources, originality, booth impact,
   connection to the other two projects, and fit with the theme. Be blunt about which ones are
   unrealistic for the timeline.
4. Once we've converged on one, help me cut it into a day-by-day plan (design → print → assemble →
   electronics → firmware → test → booth prep), with a **fallback "minimum demo"** I can still show
   if day 5 goes badly, and the measurements I should take so I have real numbers on the poster.

## Ground rules

- Don't invent specs, prices or performance figures. If a number isn't in my files or from me, say
  it's an estimate and how you got it.
- The video's designs (RoboBiceps' paid Cults3D actuator, Mishin Machine's cycloidal drive) belong to
  their authors. Don't propose copying them; if a concept builds on one, say what credit or
  licence it needs.
- Push back when I'm over-scoping. A finished, working, well-explained demo beats an ambitious one
  that's half-built on the 17th.
