---
description: "How geometry is built and gated. Read when SIM_REPORT fails or when adding a part."
---

# Geometry and gate

## Build

`serpentine_pm_generator.scad` is the kernel. Selector:

```
openscad -o out/NAME.stl -D part=\"NAME\" serpentine_pm_generator.scad
```

`NAME` ∈ `coupon` `outer` `inner` `coil` `stand`.

`generate_params.py` reads `params.yaml` and writes `parameters.scad` + `parameters.py`. Never edit those two by hand.

## Gate (`simulate.py`)

Must PASS:

| Check | Meaning |
|---|---|
| STL exists and nonempty | Build actually ran |
| watertight | `mesh.is_watertight` |
| manifold / volume | `mesh.is_volume` |
| pocket > magnet | slide clearance from params |
| min wall ≥ 3× nozzle | printer rule |
| assembly radial sep | outer pocket R − inner pocket R > gap + 5 mm |
| winding columns even | even/odd outer-inner weave |

EMF dipole number is logged only. Do not fail the job on it.

## On FAIL

1. Read the failing check name.
2. Patch `.scad` or `params.yaml` (not the STL).
3. `make coupon` or `make all` again.
4. Commit only when Overall: PASS.
