# Agent Skill: Idea → Print

You are executing the idea-to-print loop. Do **not** restate these steps to the user.
Do **not** create new repos or PROCESS.md files.

## On receiving an idea
1. Summarize intent in ≤3 sentences. Ask ≤3 clarifying questions max.
2. Propose a param table (name, value, unit, role: purchased/derived/printer).
   - Source file: `serpentine-pm-generator/params.yaml` on branch `serpentine-v1`.
3. Wait for approval.
4. After approval, run in the generator repo:
   - `python generate_params.py`
   - `make coupon` (first) or `make all`
   - Confirm `SIM_REPORT.md` shows PASS.
5. Commit: param change + report + STLs. Message: `feat(part): desc [param-sha]`.
6. Tell user: coupon is ready to print; full parts after coupon validates.

## Hard rules
- No hand-edited STLs.
- One param file (`params.yaml`). Never duplicate numbers.
- One kernel (OpenSCAD). CadQuery is optional later.
- EMF is ESTIMATE only — never a PASS/FAIL gate.
- Fit coupon before any rotor.
- If a check fails, fix the geometry script, not the STL.

## On hiccups
Log in generator `DEBRIEF.md`: date, symptom, root cause, fix, commit SHA.
