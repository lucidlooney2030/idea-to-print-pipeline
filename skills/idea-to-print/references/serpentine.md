---
description: "Serpentine dual-magnet axial generator facts. Read when the user talks magnets, weave, poles, or EMF."
connections: [fdm-rules, geometry-gate]
---

# Serpentine PM generator

Dual-magnet axial machine. Air-cored. No iron in v1.

| Item | Spec |
|---|---|
| Outer magnets | 16 × Ø20×5 mm N52 discs |
| Inner magnets | 48 × Ø5×5 mm N52 (16 groups × 3 stack) |
| Coil | Wave serpentine through 32 columns (16 outer + 16 inner windows) |
| Weave | NOT zigzag — zigzag cancels |
| Bearing | 608 on stator stand |
| Air gap | 1.0 mm (param) |

Parts:

| Target | Role |
|---|---|
| coupon | One outer pocket, one inner pocket, 608 seat, 1.2 mm wall witness |
| outer | 16 inward pockets + spoke floor |
| inner | 16 × 3 stacked pockets |
| coil | 32-col × 5-row former, Ø2.5 mm weave holes |
| stand | 608 seat + 3 legs |

After print: log designed vs measured in generator `DEBRIEF.md`. Next param tweak uses those deltas. Clearance defaults for those pockets are in [[fdm-rules]]. How the coupon is built and gated is in [[geometry-gate]].
