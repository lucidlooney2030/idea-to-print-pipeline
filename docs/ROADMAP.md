# Roadmap

## Phase 0 — Organize (this commit)

- [x] Declare this repo the system of record
- [x] Point duplicate morning repos at this one
- [x] Write agent + hiccup + architecture docs
- [ ] CadQuery available in the build environment
- [ ] One family ported from `generators` OpenSCAD → CadQuery + STEP

## Phase 1 — One family is boringly editable

Target: AFPM-Desk *or* HF-RF16, not both.

- parameters.yaml drives every mating dimension
- `pipeline/simulate.py` geometry gates + lumped EM estimate
- Fit coupon STL regenerates from the same params
- You can say "gap 1.5 mm, 8 poles, N42 20x3" and get new STEP/STL without a new topology

Done when: one coupon printed from the new pipeline matches the old OpenSCAD coupon within tape-measure tolerance.

## Phase 2 — Voice sits on top of the family

- Reuse `voice-stl-orbit` UI ideas (speech, param sliders) but target CadQuery families
- Intent → spec.json → param diff → you approve → rebuild
- FEMM 2D cross-section optional for gap sweeps
- Slicer profile + watch-folder drop for Kobra 3 Max

## Phase 3 — Freeform only where families do not exist

- Blank-page CadQuery with compile-and-repair
- Still no mesh-diffusion parts in a load path
- 3D FEM only when bench disagrees with tier 2/3 by a lot

## Explicit non-goals

- Overunity / self-running machines
- Utility-voltage from a hand crank
- Deleting `generators/` history
- Another process-only GitHub repo
