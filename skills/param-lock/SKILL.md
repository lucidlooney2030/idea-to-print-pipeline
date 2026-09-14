---
name: param-lock
description: "Merge spec overrides into a family parameters.yaml and show a human diff. Use when spec.json exists and geometry is next."
type: workflow
lifecycle: active
---

# Lock parameters

1. Load family defaults.
2. Apply `requested_overrides` only if they pass constraints (bed, wall, window vs AWG pack).
3. Recompute derived pocket sizes from magnet stock + clearance class. Never leave pocket = magnet size.
4. Emit a 5-line human diff and wait for approval on first-of-session or any gap/pole change.
5. Write `parameters.yaml`. That file is now the only legal number source.
