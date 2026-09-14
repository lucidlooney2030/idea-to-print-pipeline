# Changelog

## 2026-09-14

- **Generalized**: idea-to-print is now generator-agnostic. Added `references/generator-contract.md` and a registry (`generators/<id>.yaml`) so any parametric OpenSCAD project plugs in without rewriting the workflow.
- Replaced hard-coded `serpentine-pm-generator` / `serpentine-v1` commands with registry-driven `emit` / `coupon_target` / `all_target`.
- Serpentine moved to `references/examples/serpentine.yaml` as one worked example among many.
- FDM rules, geometry-gate, and evals/triggers rewritten to be domain-neutral (bracket, housing, gear, magnet pocket all covered).
- Coupon-gate gotcha and derived-params warning retained as process-level rules.

## 2026-09-14 (earlier)

- Skill-creator pass: INDEX graph, coupon-gate gotcha, derived-params warning, expanded evals/triggers
- Bound to `serpentine-pm-generator` / `idea-to-print-pipeline` on branch `serpentine-v1`
- Initial skill: voice/chat → params.yaml → OpenSCAD → trimesh gate → coupon-first print
