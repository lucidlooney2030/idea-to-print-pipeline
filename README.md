# Idea-to-Print Pipeline — contract only

This repo is the **process contract**, not a second codebase.

## The loop (silent — do not restate)
1. Capture intent (plain words).
2. Lock params in the **generator repo** `params.yaml`. Approve the table.
3. Geometry rebuilds from params only (OpenSCAD kernel).
4. Gate must PASS: manifold, fit, walls, assembly, winding rule.
5. Commit with `SIM_REPORT.md`.
6. Print fit coupon first. Log in `DEBRIEF.md`.

## Where the work lives
- **Live generator:** `lucidlooney2030/serpentine-pm-generator` (branch `serpentine-v1`)
- **This repo:** contract + agent skill + templates only.
- Frozen: `parametric-cad-pipeline`, `cad-process-docs` (historical).

## Agent skill
See `SKILL.md`. Follow it without asking the user to restate the mission.

## Templates
- `templates/IDEA.md.template`
- `templates/DEBRIEF.md.template`
