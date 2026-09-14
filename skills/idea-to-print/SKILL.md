---
name: idea-to-print
description: "Turn any voice or chat description of a physical part into gated, parametric OpenSCAD STLs for FDM printing. Use when the user describes a bracket, housing, gear, magnet pocket, coil former, coupon, generator, or says 'make this printable' / 'idea to print' / 'voice to STL'. Not for organic mesh generators (Meshy/Tripo/Rodin), hand-edited STLs, or non-parametric CAD. Works across any OpenSCAD generator repo that follows the params.yaml contract."
type: workflow
lifecycle: active
---

# Idea → Print (generator-agnostic)

Convert spoken or typed intent into print-ready STLs. Edit parameters, never meshes. One kernel per project. One param file per project. Coupon before full parts.

This skill is the **process**, not a specific part. Serpentine, brackets, housings, gears — any parametric OpenSCAD generator plugs in via a registry entry. The workflow never changes; only the generator config does.

## Generator registry

Each project lives in its own repo and declares itself in `generators/<id>.yaml` (see `references/generator-contract.md`). The active generator is selected by the user's intent or an explicit `generator:` field.

| Field | Meaning |
|---|---|
| `id` | Short name (e.g. `serpentine`, `bracket-v2`) |
| `repo` | `owner/name` |
| `branch` | Working branch |
| `kernel` | `openscad` (default) or `cadquery` |
| `param_file` | Path to params (default `params.yaml`) |
| `emit` | Command to emit generated params |
| `coupon_target` | Make target or OpenSCAD part name for the fit coupon |
| `all_target` | Make target for full set |
| `parts` | List of full-part names |
| `gate` | Script that writes `SIM_REPORT.md` |

If no registry entry matches, ask the user for the repo + branch (or create a minimal one) before proceeding. Do not hard-code a single generator.

## Fast path

1. **Intent** in ≤3 sentences. Ask ≤3 questions only if a purchased part, printer constraint, or mating fit is missing.
2. **Resolve generator** from registry (or prompt). Load its contract.
3. **Propose a param table** (name, value, unit, role: `purchased` / `derived` / `printer`). Wait for approval. Source of truth: that generator's `param_file`.
4. After approval, change **only** the param file (including any `derived:` block — emitters copy derived, they do not recompute it). Run the generator's `emit`, then its `coupon_target`.
5. Read `SIM_REPORT.md`. Scope the gate to what was actually built (coupon-only builds must not be failed by missing full parts). If scoped result is PASS, stop. Tell the user to print the coupon STL first.
6. After coupon measurements land in `DEBRIEF.md`, run `all_target` and commit.

Full parts only after coupon deltas are logged.

## Hard rules

- No hand-edited STLs. Failures → fix `.scad` / source or `params.yaml`, rebuild.
- Numbers live in the generator's param file only. Generated `parameters.py` / `parameters.scad` are never hand-edited.
- Default kernel: OpenSCAD. CadQuery is optional later, not the default.
- Any EMF / physics number from the gate is ESTIMATE only. Never a PASS/FAIL gate.
- If the scoped gate FAILs, do not tell the user to print.
- Do not create new repos or PROCESS.md files. Work inside the selected generator repo.
- One param file per generator. Do not scatter numbers across scripts.

## Coupon-gate gotcha

Many gates loop over *all* declared parts and FAIL any missing STL. A coupon-only build will therefore report FAILs for the unbuilt full parts even when the coupon is perfect.

When the user asked for coupon only:

1. Treat missing full-part STLs as expected, not a print block.
2. PASS/FAIL the coupon mesh checks (nonempty / watertight / manifold) plus param checks (clearances, min wall, assembly).
3. Do not tell the user to print if the **coupon** itself failed.
4. Optional durable fix (only if the user wants a pipeline patch): make the gate skip missing STLs unless the target is `all`. Keep that change in the generator repo.

## Commit

```
feat(part): short description [param-sha]
```

Include the param file, `SIM_REPORT.md`, and `DEBRIEF.md` when measurements exist. Prefer gitignoring `out/` and regenerating. Do not commit generated param modules unless repo policy already tracks them.

## Output to the user

Do not restate this workflow. Return only:

1. **Param table** — name, value, unit, role.
2. **Gate result** — PASS or FAIL + failing checks (scoped to what was built).
3. **Next STL** — the coupon STL until `DEBRIEF.md` has measured deltas; then the requested full part.

## Load on demand

Start at `references/INDEX.md`. Then:

- Printer / FDM rules: `references/fdm-rules.md`
- Geometry + gate: `references/geometry-gate.md`
- Generator contract + registry: `references/generator-contract.md`
- Example registry entry (serpentine): `references/examples/serpentine.yaml`

## Knowledge Graph

- [[fdm-rules]] — walls, clearances, coupon-first print
- [[geometry-gate]] — OpenSCAD selector, SIM_REPORT checks, FAIL loop, coupon-gate gotcha
- [[generator-contract]] — how any project plugs in; registry fields
- [[examples/serpentine]] — one concrete registry entry (magnets, weave, part map)
