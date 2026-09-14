# Voice / chat → printable STL

One kernel (OpenSCAD). One param file (`params.yaml` in the generator repo). Coupon before rotors.

```
you speak  →  param table (approve)  →  params.yaml
       →  generate_params.py  →  OpenSCAD CLI  →  out/*.stl
       →  trimesh gate (SIM_REPORT.md)
       →  print coupon  →  DEBRIEF.md  →  make all
```

Live work: `lucidlooney2030/serpentine-pm-generator` branch `serpentine-v1`.
Agent skill: `skills/idea-to-print/`.
