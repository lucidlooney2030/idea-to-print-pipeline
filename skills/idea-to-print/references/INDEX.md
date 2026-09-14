---
description: "Knowledge graph index for idea-to-print. Start here when loading references."
connections: [fdm-rules, geometry-gate, generator-contract, examples/serpentine]
---

# Idea-to-Print Knowledge Graph

Load only the node needed for the current step. The process is generator-agnostic; domain specifics live in the selected generator's own docs or an example entry.

## Core nodes

- [[fdm-rules]] — FDM walls, fits, materials, coupon-first. Read before proposing clearances.
- [[geometry-gate]] — OpenSCAD part selector, SIM_REPORT checks, FAIL loop, coupon-gate gotcha. Read when building or when a gate fails.
- [[generator-contract]] — Registry fields, how a new project plugs in, param-file rules. Read when the active generator is unknown or new.
- [[examples/serpentine]] — One concrete registry entry (dual-magnet axial). Read only as a worked example, never as the default.

## Traversal

Intent / purchased hardware → [[generator-contract]] + [[fdm-rules]]
Param approval → stay in SKILL.md + the generator's param file
`coupon` / `all` / SIM_REPORT → [[geometry-gate]]
Print measurements → the generator's DEBRIEF (shape defined by its own contract)
