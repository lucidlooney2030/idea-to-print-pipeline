---
description: "Knowledge graph index for idea-to-print. Start here when loading references."
connections: [fdm-rules, geometry-gate, serpentine]
---

# Idea-to-Print Knowledge Graph

Load only the node needed for the current step.

## Core nodes

- [[fdm-rules]] — Kobra-class FDM walls, fits, materials. Read before proposing clearances or coupon features.
- [[geometry-gate]] — OpenSCAD part selector, SIM_REPORT checks, FAIL loop, coupon-gate gotcha. Read when building or when a gate fails.
- [[serpentine]] — Dual-magnet axial baseline: magnets, weave, part map, DEBRIEF. Read when the user talks poles, weave, EMF, or named parts.

## Traversal

Intent / purchased hardware → [[serpentine]] + [[fdm-rules]]
Param approval → stay in SKILL.md + `params.yaml`
`make coupon` / `make all` / SIM_REPORT → [[geometry-gate]]
Print measurements → [[serpentine]] DEBRIEF section
