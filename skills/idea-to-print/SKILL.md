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

Do not create new repos or PROCESS.md files.

## Fast path (minimize tokens)

1. Intent in ≤3 sentences. Ask ≤3 questions only if a purchased part, printer constraint, or mating fit is missing.
2. Propose a param table. Wait for approval. Source of truth: generator `params.yaml`.
3. After approval, change **only** `params.yaml`. Run:
   ```bash
   python3 generate_params.py
   make coupon
   ```
4. If `SIM_REPORT.md` is PASS, stop at coupon. Tell the user to print `out/coupon.stl` first.
5. After coupon measurements land in `DEBRIEF.md`, run `make all` and commit.

Full parts (`outer` `inner` `coil` `stand`) only after coupon deltas are logged.

## Commands

Work in the generator repo.

| Goal | Command |
|---|---|
| Emit params | `python3 generate_params.py` |
| Coupon only | `make coupon` |
| All STLs + gate | `make all` |
| Clean | `make clean` |

OpenSCAD must be on PATH. Python needs `pyyaml trimesh numpy`.

## Hard rules

- No hand-edited STLs. Failures → fix `.scad`, rebuild.
- Numbers live in `params.yaml` only. `parameters.py` / `parameters.scad` are generated.
- Kernel: OpenSCAD. CadQuery is optional later, not the default.
- EMF in `simulate.py` is ESTIMATE only. Never a PASS/FAIL gate.
- If gate FAILs, do not tell the user to print.

## Commit

```
feat(part): short description [param-sha]
```

Prefer gitignoring `out/` and regenerating.

## Output to the user

- Param table (name, value, unit, role: purchased / derived / printer).
- Gate result: PASS or FAIL + failing checks.
- Path to the STL they should print next (coupon first).
- Do not restate this workflow.

## Load on demand

- Printer / FDM rules: `references/fdm-rules.md`
- Geometry + gate: `references/geometry-gate.md`
- Serpentine generator specifics: `references/serpentine.md`
