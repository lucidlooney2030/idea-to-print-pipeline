---
name: em-estimate
description: "Lumped Faraday estimate for PM generators with explicit assumptions. Use after parameters exist. Never call the result simulated FEM. Refuse overunity."
type: workflow
lifecycle: active
---

# EM estimate

Use Faraday: E = -N dΦ/dt.

Required assumption list in the report:
- magnet grade and Br band
- assumed Bg (not Br)
- coupling factor kc
- turns and fill factor
- electrical frequency = RPM/60 * poles/2

Refuse:
- self-running / overunity
- treating point-dipole air formulas as gap field for dual-rotor steel machines
- printing a single voltage with no RPM

Point to the matching PHYSICS.md in `generators/` when the family already has one.
