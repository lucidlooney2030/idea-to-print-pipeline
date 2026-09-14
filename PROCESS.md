# Process: idea → verified print

Companion to `docs/ARCHITECTURE.md` and `docs/AGENTS.md`.

## 0. Pick the lane

- Changing an existing machine → work in `generators/<project>` and keep params in one file.
- Improving the *system* → work in this repo.
- Do not open a new GitHub repo for a new idea.

## 1. Capture intent (no dimensions in prose)

Write `templates/IDEA.md` fields: what, why, success criteria, constraints, non-claims.
The Intent agent emits `schemas/spec.schema.json` — topology + goals, not XYZ coordinates.

## 2. Lock parameters

One `parameters.yaml` per family. Named, unit-commented, derived values computed in code.
You review the parameter block. You do not edit CadQuery by voice.

## 3. Generate geometry

CadQuery / build123d script imports parameters.
Export:
- `.step` — editable B-rep for FreeCAD / other CAD
- `.stl` — print only, regenerated, never hand-edited
- `.json` bbox + mass properties for the gate

## 4. Gate (mandatory, honest)

Run `pipeline/simulate.py`.
PASS means the *checks that exist* passed — not that Elmer/FEMM ran.
See `docs/HICCUPS.md` for what the current gate cannot know.

## 5. Print

Fit coupon first. Then parts. PETG/ABS/ASA/nylon on Kobra 3 Max. Not PLA for loaded rotors.

## 6. Debrief

Measured vs predicted in `DEBRIEF.md`. This is the only thing that makes the next voice prompt smarter.
