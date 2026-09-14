---
description: "How geometry is built and gated. Read when SIM_REPORT fails or when adding a part."
connections: [fdm-rules, serpentine]
---

# Geometry and gate

## Build

`serpentine_pm_generator.scad` is the kernel. Selector:

```
openscad -o out/NAME.stl -D part=\"NAME\" serpentine_pm_generator.scad
```

`NAME` ∈ `coupon` `outer` `inner` `coil` `stand`.

`generate_params.py` reads `params.yaml` and writes `parameters.scad` + `parameters.py`. Never edit those two by hand.

`derived:` in `params.yaml` is copied, not computed. If magnet diameter, thickness, or slide clearance changes, recompute before emit:

- pocket_dia = magnet_dia + 2 × slide_mm
- pocket_depth = magnet_thk + 0.35

## Gate (`simulate.py`)

Must PASS (when that STL exists):

| Check | Meaning |
|---|---|
| STL exists and nonempty | Build actually ran |
| watertight | `mesh.is_watertight` |
| manifold / volume | `mesh.is_volume` |
| pocket > magnet | slide clearance from params |
| min wall ≥ 3× nozzle | printer rule in [[fdm-rules]] |
| assembly radial sep | outer pocket R − inner pocket R > gap + 5 mm |
| winding columns even | even/odd outer-inner weave |

EMF dipole number is logged only. Do not fail the job on it.

## Coupon-gate gotcha

`make coupon` builds only `out/coupon.stl`, then runs the same `simulate.py` that demands `outer inner coil stand`. Those four will FAIL as missing on a clean tree. Do not treat that as a coupon geometry failure. Block print only when **coupon** nonempty/watertight/manifold or a param check fails.

## On FAIL

1. Read the failing check name.
2. Patch `.scad` or `params.yaml` (not the STL).
3. `make coupon` or `make all` again.
4. Commit only when the scoped gate is PASS.

Part names and DEBRIEF columns live in [[serpentine]].
