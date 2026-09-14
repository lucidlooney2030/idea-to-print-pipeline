# Idea-to-Print Pipeline

**Mission:** Voice or chat idea → parametric CAD (editable) → gated simulation → print → measure → revise.

This is the **system repo**. Hardware lives in [`generators`](https://github.com/lucidlooney2030/generators).
The earlier mesh-orbit prototype lives in private `voice-stl-orbit` and is **not** the geometry source of truth.

## What this is (and is not)

| This is | This is not |
|---------|-------------|
| Parametric code as source of truth (CadQuery / build123d → STEP + STL) | A text-to-mesh toy that orbits a blob |
| Constrained generator *families* you can edit with sliders | Freeform "imagine a generator" that invents dimensions |
| Physics *estimates* with stated assumptions, then bench measurements | A pass/fail script that pretends FEM ran |
| Faraday machines: work in → electricity out | Free energy / overunity |

## Account map (use these two, ignore the rest for daily work)

| Repo | Role |
|------|------|
| **[idea-to-print-pipeline](https://github.com/lucidlooney2030/idea-to-print-pipeline)** (this) | Process, agents, skills, schemas, gates |
| **[generators](https://github.com/lucidlooney2030/generators)** | Real printed machines (AFPM v1–v4, HF-RF16, Coax-Faraday) |
| `voice-stl-orbit` (private) | Frozen prototype: speech → OpenSCAD templates → orbit STL |
| `parametric-cad-pipeline`, `cad-process-docs`, `serpentine-pm-generator` | **Redirects.** Do not add work there. |

## The loop

```
1. Voice / chat          Intent agent → spec JSON (no magic numbers in prose)
2. Lock parameters       You approve parameters.yaml  ← single source of truth
3. Generate CAD          CadQuery family script → STEP (edit) + STL (print)
4. Gate                  fit / clearance / printability / EM estimate
5. Print                 fit coupon first on Kobra 3 Max
6. Bench                 V vs RPM, gap, turns → DEBRIEF.md → next revision
```

Golden rule: if you are re-describing a dimension in chat, stop. Put it in `parameters.yaml` and regenerate.

## Layout

```
idea-to-print-pipeline/
  README.md                 you are here
  docs/
    ARCHITECTURE.md         stack + why CadQuery not mesh
    AGENTS.md               the team and handoffs
    HICCUPS.md              real failure modes, not vibes
    ROADMAP.md              phases 0–3
  skills/                   agent-readable procedures
  schemas/                  spec + parameter contracts
  pipeline/                 runnable gates (no fake FEM)
  families/                 parametric generator families (code)
  templates/                IDEA / DEBRIEF / SIM_REPORT
```

## Right now (2026-09-14)

- Process and agent contracts: **this repo**
- Printable machines and learned physics notes: **generators**
- Next build target: CadQuery port of one existing family (AFPM-Desk or HF-RF16) with shared `parameters.yaml` — not a new topology from a voice dump.

## Safety

NdFeB magnets pinch, jump, and shatter. Dual-rotor and outer-rotor stacks can crush printed plastic. Eye protection. Assemble with spacers. These are educational watt-scale machines.

## License

MIT. Print, remix, share. Attribution appreciated.
