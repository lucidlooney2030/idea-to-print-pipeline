---
description: "How any OpenSCAD generator project plugs into idea-to-print. Read when selecting or adding a generator."
connections: [geometry-gate, fdm-rules, examples/serpentine]
---

# Generator contract

Every project that idea-to-print can drive declares a registry entry. The skill never assumes a specific repo, branch, or part name — it reads them from here.

## Registry file

`generators/<id>.yaml` in this pipeline repo (or a path the user points at). Minimal shape:

```yaml
id: my-part
repo: owner/my-part-generator
branch: main
kernel: openscad
param_file: params.yaml
emit: python3 generate_params.py
coupon_target: make coupon
all_target: make all
clean: make clean
parts: [coupon, body, lid, stand]
gate: python3 simulate.py
notes: "Brief domain facts the agent should know."
```

## Rules for a healthy generator

- One param file is the single source of truth. All dimensions, counts, and clearances live there.
- `derived:` values are copied by the emitter, never recomputed — update them when inputs change.
- The kernel exposes a part selector so coupon and full parts build from the same source.
- The gate writes `SIM_REPORT.md` and is scoped: missing STLs for unbuilt parts must not block a coupon-only run.
- `out/` is gitignored; STLs are regenerated, not committed (unless policy says otherwise).
- A `DEBRIEF.md` captures designed-vs-measured deltas after the first print.

## Adding a new generator

1. Create or point at the repo with a parametric OpenSCAD kernel + `params.yaml`.
2. Add `generators/<id>.yaml` with the fields above.
3. Verify: `emit` → `coupon_target` → scoped gate PASS → print coupon → log DEBRIEF → `all_target`.
4. No change to SKILL.md is required. The process is identical.

## Example

See [[examples/serpentine]] for a filled-in entry. It is one of many possible generators, not the default.
