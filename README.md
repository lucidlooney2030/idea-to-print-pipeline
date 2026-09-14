# Idea-to-Print Pipeline

**Mission:** Turn a voice or chat idea into a finished, printable 3D design as fast and precisely as possible.

This repo is the **process**, not the parts. The generator baseline lives in `serpentine-pm-generator`.

## Core Rules (non-negotiable)
1. **Never hand-edit an STL.** Geometry comes only from parametric scripts.
2. **All dimensions live in `parameters.py`** (or `.scad` params). One source of truth.
3. **Every change is a Git commit** with a clear message and a `DEBRIEF.md` entry.
4. **Simulation must pass before export.** Fit, clearance, EMF, manifold checks.
5. **Print a fit coupon first** on any new mating geometry.

## The 6-Step Loop
1. **Speak the idea** — plain language, no dimensions yet. I extract intent.
2. **Lock parameters** — I propose named constants + units. You approve.
3. **Generate geometry** — scripts rebuild from params. No manual STL work.
4. **Simulate & gate** — `simulate.py` runs checks → `SIM_REPORT.md`. All PASS or iterate.
5. **Commit & tag** — param change + report + regenerated STLs. You get SHA + one-line summary.
6. **Print & learn** — fit coupon first, then parts. Log hiccups back into the process.

## Repo Layout
```
idea-to-print-pipeline/
├── README.md                 # this file
├── PROCESS.md                # full step-by-step + hiccup log
├── templates/
│   ├── IDEA.md.template
│   └── DEBRIEF.md.template
├── scripts/
│   ├── parameters.py          # named constants, units, tolerances
│   ├── parts/                  # one module per printable part
│   ├── simulate.py             # fit, clearance, EMF, manifold
│   └── export.py               # STL + preview renders
└── baseline/                  # pointer to serpentine-pm-generator
```

## Baseline
- Repo: https://github.com/lucidlooney2030/serpentine-pm-generator
- Branch: `serpentine-v1`
- First real change request starts here.

## Hiccup Log
| Date | What broke | Fix applied | Commit |
|------|------------|-------------|
| 2026-09-13 | First winding layout cancelled 16-pole field | Aligned poles + wave serpentine | (see generator repo) |
| 2026-09-13 | STL placeholders instead of real geometry | Parametric .scad/.py is source of truth | (see generator repo) |
