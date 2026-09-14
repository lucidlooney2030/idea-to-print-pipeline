# Idea-to-Print Pipeline — process contract

This repo is the **process contract**, not a second codebase. The skill turns any voice or chat description of a physical part into gated, parametric OpenSCAD STLs for FDM printing.

## The loop (silent — do not restate)
1. Capture intent (plain words).
2. Resolve the **generator** from the registry (`generators/<id>.yaml`).
3. Lock params in that generator's param file. Approve the table.
4. Geometry rebuilds from params only (OpenSCAD kernel).
5. Gate must PASS (scoped to what was built): manifold, fit, walls, assembly.
6. Commit with `SIM_REPORT.md`.
7. Print fit coupon first. Log in `DEBRIEF.md`.
8. Full parts only after coupon deltas are logged.

## Where the work lives
- **Live generators:** any repo that follows `references/generator-contract.md` (see `generators/` and `references/examples/`).
- **This repo:** contract + agent skill + templates only. Serpentine is one example, not the default.
- Frozen: `parametric-cad-pipeline`, `cad-process-docs` (historical).

## Agent skill
See `skills/idea-to-print/SKILL.md`. Follow it without asking the user to restate the mission.

## Templates
- `templates/IDEA.md.template`
- `templates/DEBRIEF.md.template`
