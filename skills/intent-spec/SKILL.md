---
name: intent-spec
description: "Turn voice or chat into a schema-valid spec.json. Use when the user describes a generator or part idea. Not for writing CAD or claiming voltages."
type: workflow
lifecycle: active
---

# Intent → spec.json

1. Identify family: `afpm_ssdr` | `radial_outer` | `coax_drums` | `unknown`.
2. If unknown, ask which existing machine in `generators/` this is closest to. Do not invent a fourth topology in the same breath.
3. Write `goal` with zero dimensions.
4. Put stock magnets, printer, material, AWG under `constraints`.
5. Put any spoken numbers under `requested_overrides` only.
6. Always include `non_claims`: not overunity, not grid voltage unless the user is explicitly building something else (they are not).
7. Validate against `schemas/spec.schema.json`.
8. Hand the file to the parameters agent. Do not start CadQuery.
