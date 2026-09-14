---
description: "How geometry is built and gated. Read when SIM_REPORT fails or when adding a part."
connections: [fdm-rules, generator-contract]
---

# Geometry and gate

## Build

The generator's kernel (usually an `.scad` file) is selected by a part name. Typical pattern:

```
openscad -o out/NAME.stl -D part="NAME" <kernel>.scad
```

Exact part names and the emit/coupon/all commands come from the generator's registry entry — see [[generator-contract]].

Generated param modules (`parameters.scad`, `parameters.py`) are written by the emit step. Never edit them by hand.

If the param file has a `derived:` block, it is copied, not computed. When a purchased dimension or clearance changes, recompute derived values before emit.

## Gate

The gate script (from the registry) must PASS for every STL that was actually built:

| Check | Meaning |
|---|---|
| STL exists and nonempty | Build actually ran |
| watertight | `mesh.is_watertight` |
| manifold / volume | `mesh.is_volume` |
| fit clearance | slide/press gap from params |
| min wall ≥ 3× nozzle | printer rule in [[fdm-rules]] |
| assembly clearance | mating parts do not collide |

Any physics / EMF / flux estimate is logged only. Do not fail the job on it.

## Coupon-gate gotcha

Many gates loop over *all* declared parts and FAIL any missing STL. A coupon-only build will report FAILs for the unbuilt full parts. Do not treat that as a coupon geometry failure. Block print only when the **coupon** mesh or a param check fails. See SKILL.md for the scoped PASS rule.

## On FAIL

1. Read the failing check name.
2. Patch the `.scad` / source or the param file (not the STL).
3. Re-run coupon or all.
4. Commit only when the scoped gate is PASS.
