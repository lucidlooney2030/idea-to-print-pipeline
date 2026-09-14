# Hiccups and annoyances (expect these)

This list is the design. If a step below is painful, the system is working — it is showing where voice-to-part is actually hard.

## Product / process

| Hiccup | Why it exists | Mitigation |
|--------|---------------|------------|
| Voice cannot specify a 3D stack | You will omit gap, fill factor, polarity pattern | Intent agent asks 5 structured questions, then stops talking |
| Too many GitHub repos | This morning created 4 process repos | Work only in this repo + `generators` |
| "Orbit the STL" feels done | Preview ≠ function | Ban mesh-only tools from the generator path |
| Agents rewrite dimensions in chat | Context drift | Parameters file is the only legal number store |
| New repo per idea | Feels like progress | Forbidden. New folder under `families/` or `generators/` |

## CAD

| Hiccup | Why | Mitigation |
|--------|-----|------------|
| CadQuery/OCC throws on a fillet | Kernel is picky | Keep Phase 1 parts fillet-light; repair loop with simpler ops |
| OpenSCAD still in `generators/` | That is the working history | Port one family at a time; do not rewrite all four tonight |
| STEP looks different in FreeCAD | Unit / placement | Always mm, always origin at shaft axis |
| LLM writes CadQuery that never compiled | Models hallucinate APIs | Family templates + compile-and-repair, not blank-page codegen |
| Coil copper is not a printable solid | Turns live in the winding spec | Model the *former*, not 200 tubes of copper |

## Physics / simulation

| Hiccup | Why | Mitigation |
|--------|-----|------------|
| Air-cored dipole formulas lie | Near-field magnets are not point dipoles | Lumped Faraday + measured Bg, or FEMM |
| Zigzag serpentine cancels | Adjacent windows see opposite dΦ/dt | Wave winding only; QA rule |
| "Optimized magnet placement" | Optimization needs an objective and a model | Sweep 2–3 discrete gaps, print, measure |
| Steel back-iron vs eddy | Helps Bg, adds loss at high RPM | Thin / laminated; hand-crank eddy is small |
| Simulated V ≫ bench V | Fill factor, gap, polarity errors | Debrief beats another formula |
| Calling a print statement "simulation" | Theater | Gate file names the tier |

## Shop

| Hiccup | Why | Mitigation |
|--------|-----|------------|
| Magnet pinch crushes PETG | Dual-rotor attraction is huge | Spacers, one magnet at a time, last-install magnets |
| Pockets too tight after shrink | Filament + temp | Fit coupon every material change; clearance classes in params |
| PLA rotors creep | Heat + preload | PETG/ABS/ASA/nylon |
| Send-to-printer is vendor glue | Kobra ecosystem | Export STL + Orca profile first |
| 28 AWG pack will not fit the window | Fill factor ~0.55 not 1.0 | Window check in QA before print |

## People / session

| Hiccup | Why | Mitigation |
|--------|-----|------------|
| Frustration at the model | The job is genuinely underspecified | Smaller loop: one family, one parameter change, one coupon |
| Starting over every morning | No single source of truth | This repo |
