---
name: cadquery-family
description: "Build or edit CadQuery family scripts from parameters.yaml. Use when parameters are locked and STEP/STL must be produced. Not for mesh-diffusion or OpenSCAD-first generator assemblies."
type: workflow
lifecycle: active
---

# CadQuery family build

1. Import parameters. No numeric literals in part modules except documented constants (e.g. 608 bearing OD).
2. One module per printable part. Shaft axis = origin. Units mm.
3. Export STEP and STL. STL is disposable.
4. If OCC fails, simplify the failing op (drop fillet, split boolean). Do not switch to a mesh library.
5. Coils: model the former / window, not the copper helix.
6. Hand artifacts to print-gate.
