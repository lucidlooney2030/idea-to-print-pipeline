# Process: Voice/Chat → Finished Design

## Goal
Minimize friction between "I have an idea" and "I have a printable STL that works."

## Step 1 — Capture Intent (you speak, I listen)
- You describe the part or change in plain words.
- I respond with a short **intent summary** + any clarifying questions (max 3).
- No dimensions yet. No code yet.

## Step 2 — Lock Parameters
- I write/update `parameters.py` with named constants and units.
- Example: `OUTER_MAGNET_DIA = 20.0  # mm, N52 disc`
- You approve or correct. This is the only place numbers live.

## Step 3 — Generate Geometry
- Scripts in `parts/` rebuild solids from `parameters.py`.
- OpenSCAD for simple CSG; CadQuery for complex mating/B-rep.
- Never edit the resulting STL by hand.

## Step 4 — Simulate & Gate
- `simulate.py` checks:
  - Pocket clearance (magnet + 0.2–0.4 mm)
  - Wall thickness ≥ 1.2 mm (0.4 mm nozzle)
  - Manifold / watertight
  - EMF / flux linkage (for generators)
  - Assembly interference
- Output: `SIM_REPORT.md`. **All PASS required** to proceed.

## Step 5 — Commit & Tag
- Commit: param change + `SIM_REPORT.md` + regenerated STLs.
- Message format: `feat(part): short description [param-sha]`
- Tag release when a version is print-ready.

## Step 6 — Print & Learn
- Print a **fit coupon** (small test of mating geometry) first.
- Then full parts.
- Log any real-world hiccup back into this file.

## Hiccup Log (living)
| Date | Symptom | Root cause | Fix | Commit SHA |
|------|---------|------------|-----|------------|
| | | | | |
