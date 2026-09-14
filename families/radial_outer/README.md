# Family: radial_outer (RF16S)

**First process target.** Dual-magnet radial flux, 16/16 poles.

This is the machine behind the three files you named. Those exact filenames are **local / chat-export names**. They are not in GitHub or Drive under those strings. The living spec is this folder + `generators/RF16S-v2`.

## File identity

| What you called it | What it is | Canonical name going forward |
|---|---|---|
| `radial_flux_16_inward_rotor.stl` | Outer **cup**. 16× Ø20×5 magnets on the **inner wall**, faces pointing **in** (N-S-N-S). | `RF16S-OUTER.stl` |
| `03_serpentine_coil_former(1).stl` | Stationary **coil cage** between the two magnet rings. `(1)` is a Windows/macOS duplicate suffix. | `RF16S-CAGE.stl` |
| `02_inner_magnet_hub.stl` | Inner **hub**. 16 poles × 3 stacked Ø5×5 magnets (48 total), faces pointing **out**. | `RF16S-INNER.stl` |

Related, not this family:
- `generators/HF-RF16-SERP` is an earlier **single-ring** outer-rotor with a grooved stator drum and steel tube. Different machine. Do not mix those STLs with this stack.
- Retired `serpentine-pm-generator` used the `02_` / `03_` numbering and a 32-hole former sketch. That sketch is not printable truth.

## Stack (radial, mm)

```
shaft → inner hub (5 mm magnets face OUT)
     → 1.00 mm gap
     → coil cage (windows, wave winding)
     → 1.00 mm gap
     → outer cup (20 mm magnets face IN)
```

Pitch 22.5°. Poles aligned so each inner column faces an outer disc **attracting** across a window (opposite polarity).

Numbers live in `parameters.yaml`. Change a number there, regenerate. Do not edit STLs.

## Process for this family

1. Attach or upload the three local STLs if you still have them (reference meshes only).
2. Approve `parameters.yaml`.
3. CadQuery rebuilds STEP + STL from the yaml.
4. `pipeline/simulate.py` gates pockets / gap / winding.
5. Print coupons, then parts, PETG, pockets up.

See `IDEA.md` and `docs/` in the repo root.
