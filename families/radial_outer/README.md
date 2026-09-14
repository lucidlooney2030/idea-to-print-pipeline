# Family: radial_outer (RF16S) — FIRST BUILD

Dual-magnet radial flux, 16/16. Designed from parameters, not recovered STLs.

## Kinematics

Outer cup and inner hub are **rotors** (same shaft later). Cage is the **stator**.
Magnets attract across each window: outer face IN, inner face OUT, opposite polarity.

## Rebuild

```bash
pip install cadquery
python families/radial_outer/rf16s_build.py
```

Exports `exports/RF16S-{COUPON,OUTER,INNER,CAGE}.{stl,step}`

Print order: coupon → measure pockets on your N52 stock → then cage → inner → outer.
PETG. Not PLA. Pockets face up. Supports off if it stands.
