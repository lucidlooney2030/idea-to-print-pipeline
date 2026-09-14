# Where the three files live

Searched 2026-09-14:

- GitHub `lucidlooney2030` — **no blob** named `radial_flux_16_inward_rotor.stl`, `03_serpentine_coil_former(1).stl`, or `02_inner_magnet_hub.stl`
- Google Drive (connected) — **no title match**

Closest committed artifacts:

| Closest file | Repo | Notes |
|---|---|---|
| `HF-RF16-SERP/stl/HF-RF16-ROTOR.stl` | generators | Same *idea* as inward-face outer cup, but that project has a grooved stator, **not** an inner magnet hub |
| `HF-RF16-SERP/stl/HF-RF16-STATOR.stl` | generators | Not the coil former you named |
| `RF16S-v2/README.md` | generators | Describes OUTER / INNER / CAGE exactly. **STLs were never committed** (folder only has README/PRINT/DOWNLOADS) |
| `serpentine_pm_generator.scad` | retired snapshot | `02` hub + `03` former numbering; geometry is a stub |

**If the three STLs are on your laptop (Downloads / slicer / chat export), attach them in this chat or drop them into `generators/RF16S-v2/reference/`.** Until then we treat `parameters.yaml` as source of truth and rebuild.
