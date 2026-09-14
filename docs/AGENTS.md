# Agent team

These are roles, not six always-on chatbots. One Grok session can wear them in order. Separate them when a step is fragile (CAD compile, EM claims, Git writes).

## 1. Intent (`skills/intent-spec`)

**In:** voice transcript or chat.
**Out:** `spec.json` matching `schemas/spec.schema.json`.
**Does:** pick a family, extract goals ("more voltage", "fit these magnets"), flag contradictions.
**Does not:** invent dimensions, write CAD, claim watts.

## 2. Parameters (`skills/param-lock`)

**In:** spec.json + family defaults.
**Out:** `parameters.yaml` + a short human diff ("gap 2.0 → 1.5 mm").
**Does:** derive pocket sizes from magnet stock + clearance class.
**Stops for you** when a derived value violates a constraint (window smaller than wire pack, gap < layer height, rotor OD > bed).

## 3. CAD (`skills/cadquery-family`)

**In:** parameters.yaml.
**Out:** CadQuery modules, STEP, STL, bbox JSON.
**Does:** compile, repair on OCC errors, keep parts mating from the same param file.
**Does not:** sculpt meshes or "approximate" a coil as decoration.

## 4. Geometry QA (`skills/print-gate`)

**In:** solids / meshes.
**Out:** PASS/FAIL with numbers.
Checks: manifold, min wall, hole vs pin, magnet pocket vs stock, interference, bed fit, known-bad winding layouts (zigzag cancellation on even-pole single-phase).

## 5. EM (`skills/em-estimate`)

**In:** parameters + family physics notes.
**Out:** `estimate.json` + assumption list.
**Must label** every voltage/power number as estimate.
**Must refuse** overunity, self-running, and "optimized" claims with no measurement.
Tier 2 lumped model now. FEMM later.

## 6. Print + debrief (`skills/print-debrief`)

**In:** passing artifacts.
**Out:** coupon instruction, material, orientation, `DEBRIEF.md` after the bench.
Closes the loop by writing measured V/RPM back into family notes — not into chat lore.

## Handoff rule

An agent may only consume the previous agent's *file*, never a paraphrased memory of it. That is how we stop the lost-in-translation problem that started this project.
