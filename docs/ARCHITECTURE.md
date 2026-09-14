# Architecture

## Why voice-to-STL failed as a product

Natural language is a lossy codec for 3D. Two translations happen:

1. Picture in your head → words
2. Words → coordinates

Every magnet pitch, air gap, and coil window bleeds precision in those hops. Mesh generators (Meshy, Luma, ChatGPT-image-to-3D, orbit-preview STL apps) optimize for *looking like* the thing. Generators need *mating features that still fit after shrinkage*.

`voice-stl-orbit` was the right first experiment and the wrong long-term kernel: OpenSCAD + heuristic phrase parsing + orbit viewer. Keep it as a UI sketch. Do not feed generator assemblies through it.

## Kernel choice

| Tool | Output | Verdict |
|------|--------|--------|
| Image / NeRF / mesh diffusion | Triangle soup | Never for functional generators |
| OpenSCAD | CSG → mesh | Fine for brackets and coupons. Weak STEP. No real fillets/lofts. |
| FreeCAD PartDesign | Parametric tree + FCStd | Good human edit; painful to drive headless from agents |
| **CadQuery / build123d** (OCCT) | B-rep → STEP + STL | **Default.** Python, parametric, agent-writable, FreeCAD-importable |

Rule: agents write **Python that builds B-rep**. STL is an export. STEP is the archive.

## Constrained families first

Do not ask a model to invent a generator from a paragraph. Ask it to *instantiate a family*:

- `families/afpm_ssdr` — dual-rotor axial sandwich (AFPM-Desk lineage)
- `families/radial_outer` — outer-rotor radial (HF-RF16 lineage)
- `families/coax_drums` — coaxial drums (Coax-Faraday lineage)

Voice may change: pole count, magnet stock (20×5, 5×5, …), gap, turns, wire AWG, coil count, back-iron on/off.
Voice may not change: Faraday's law, Lenz drag, or topology mid-sentence without a new family.

Freeform CadQuery ("make me a novel flux path") is Phase 3, after families compile reliably.

## Data flow

```
utterance
  → Intent agent → spec.json          (schema-validated)
  → Param agent  → parameters.yaml    (human approval gate)
  → CAD agent    → parts/*.py → STEP/STL
  → QA agent     → manifold, wall, interference
  → EM agent     → estimate.json + assumptions.md   (not a lie labeled "FEM")
  → Print agent  → coupon + slice notes
  → Debrief      → measured.json → updates family defaults
```

## Simulation stack (honest tiers)

1. **Geometry gates** (now): wall thickness, hole vs magnet stock, interference, coil window vs AWG pack, print bounding box vs Kobra 3 Max.
2. **Lumped EM** (now, labeled estimate): Faraday + assumed Bg + fill factor. Always print the assumptions.
3. **2D FEMM / ONELAB** (next): magnet + gap + coil window cross-section. Still not a 3D machine.
4. **3D FEM** (later): Elmer / GetDP. Slow. Only when a family is frozen and measurements disagree with tier 2/3.

Never ship a `simulate.py` that prints 4.8 Vrms from a dipole-in-air formula and calls it verified. The 2026-09-14 serpentine script did that. Retired.

## Printer / send-to-print

Anycubic Kobra 3 Max. There is no reliable open "just send the STL and it prints" API that is worth building before the CAD+gate loop is boringly reliable. Phase 1 ends at: verified STL + slice profile + checklist. Phase 2 can talk to the slicer (Orca/Prusa) and a watch folder.
