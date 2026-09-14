---
description: "FDM constraints for common printers. Read when choosing walls, clearances, or coupon features."
connections: [geometry-gate, generator-contract]
---

# FDM rules

Default printer assumption: Anycubic Kobra-class. Nozzle 0.4 mm. Layer 0.2 mm. Override per generator if the user names a different machine.

| Rule | Value |
|---|---|
| Min wall | 1.2 mm (3× nozzle) |
| Press fit | +0.15 mm per side (risk of chip) |
| Slide fit | +0.30 mm per side |
| Loose / drop-in | +0.45 mm per side |
| First print | Fit coupon, not the full part |

Material default: PETG or ABS, 5–6 walls, ~40% infill. Adjust for the part's load case.

Do not generate organic AI meshes (Meshy, Tripo, Rodin). They are non-parametric and fail the no-hand-edit rule.

When a clearance changes, update both the clearance entry and any `derived:` block in the generator's param file. Emitters copy derived; they do not recompute it. See [[geometry-gate]].
