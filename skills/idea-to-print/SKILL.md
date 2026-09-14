---
name: idea-to-print
description: "Turn voice or chat into gated, parametric OpenSCAD STLs for FDM printing. Use when the user describes a physical part, generator, coupon, magnet pocket, coil former, or asks to go from idea to print. Not for organic mesh generators, Meshy/Tripo, or hand-edited STLs."
type: workflow
lifecycle: active
---

# Idea → Print

Convert spoken or typed intent into print-ready STLs. Edit parameters, never meshes. One kernel. One param file. Coupon before rotors.

## Repos

| Role | Repo | Branch |
|---|---|---|
| Live geometry | `lucidlooney2030/serpentine-pm-generator` | `serpentine-v1` |
| This skill + contract | `lucidlooney2030/idea-to-print-pipeline` | `serpentine-v1` |

Do not create new repos or PROCESS.md files. Work in the generator repo clone.

## Fast path

1. Intent in ≤3 sentences. Ask ≤3 questions only if a purchased part, printer constraint, or mating fit is missing.
2. Propose a param table. Wait for approval. Source of truth: generator `params.yaml`.
3. After approval, change **only** `params.yaml` (including `derived:` when magnet size or clearance changes — `generate_params.py` copies derived, it does not recompute). Run:
   ```bash
   python3 generate_params.py
   make coupon
   ```
4. Read `SIM_REPORT.md`. If Overall is PASS, stop. Tell the user to print `out/coupon.stl` first.
5. After coupon measurements land in `DEBRIEF.md`, run `make all` and commit.

Full parts (`outer` `inner` `coil` `stand`) only after coupon deltas are logged.

## Commands

Work in `serpentine-pm-generator` on `serpentine-v1`.

| Goal | Command |
|---|---|
| Emit params | `python3 generate_params.py` |
| Coupon only | `make coupon` |
| All STLs + gate | `make all` |
| Clean | `make clean` |

OpenSCAD must be on PATH. Python needs `pyyaml trimesh numpy`.

## Hard rules

- No hand-edited STLs. Failures → fix `.scad` or `params.yaml`, rebuild.
- Numbers live in `params.yaml` only. `parameters.py` / `parameters.scad` are generated. Do not edit them.
- Kernel: OpenSCAD. CadQuery is optional later, not the default.
- EMF in `simulate.py` is ESTIMATE only. Never a PASS/FAIL gate.
- If gate FAILs, do not tell the user to print.
- Do not invent a third repo. Do not restart PROCESS.md.

## Coupon-gate gotcha

`simulate.py` currently loops `coupon outer inner coil stand` and FAILs any missing STL. After a clean `make coupon` the report will FAIL on the four unbuilt parts even if the coupon is good.

When the user asked for coupon only:

1. Treat missing full-part STLs as expected, not as a print block.
2. PASS/FAIL the coupon checks plus param checks (`outer_pocket_clears`, `inner_pocket_clears`, `min_wall`, `assembly_no_collision`, `winding_even_odd_aligned`).
3. Do not tell the user to print if **coupon** watertight/manifold/nonempty failed.
4. Optional durable fix (only if the user wants a pipeline patch): skip missing STLs unless the target is `all`. Keep that change in the generator repo.

## Commit

```
feat(part): short description [param-sha]
```

Include `params.yaml`, `SIM_REPORT.md`, and `DEBRIEF.md` when measurements exist. Prefer gitignoring `out/` and regenerating. Do not commit generated `parameters.py` / `parameters.scad` unless repo policy already tracks them.

## Output to the user

Do not restate this workflow. Return only:

1. **Param table** — name, value, unit, role (`purchased` / `derived` / `printer`).
2. **Gate result** — PASS or FAIL + failing checks (coupon-scoped if that is all that was built).
3. **Next STL** — `out/coupon.stl` until `DEBRIEF.md` has measured deltas; then the requested full part.

## Load on demand

Start at `references/INDEX.md`. Then:

- Printer / FDM rules: `references/fdm-rules.md`
- Geometry + gate: `references/geometry-gate.md`
- Serpentine generator specifics: `references/serpentine.md`

## Knowledge Graph

- [[fdm-rules]] — walls, clearances, coupon-first print
- [[geometry-gate]] — OpenSCAD selector, SIM_REPORT checks, FAIL loop
- [[serpentine]] — magnets, weave, part map, DEBRIEF
