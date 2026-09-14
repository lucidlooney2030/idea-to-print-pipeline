---
name: print-gate
description: "Geometry and printability checks before export is trusted. Use after CAD export. Not a substitute for electromagnetic FEM."
type: workflow
lifecycle: active
---

# Print gate

Fail the build if any of:
- non-manifold mesh
- wall < 3*nozzle on load parts
- pocket smaller than magnet + slide clearance
- coil window area * fill_factor < copper area for target turns
- interference between rotor and stator at nominal gap
- part larger than bed
- winding layout marked `zigzag` on an even-pole single-phase family

Write `templates/SIM_REPORT.md` with numbers. Label the EM section ESTIMATE if present.
