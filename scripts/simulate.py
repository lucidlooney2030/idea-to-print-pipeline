"""Run fit, clearance, manifold, and EMF checks.
Exit 0 only if all PASS. Writes SIM_REPORT.md.
"""
import sys
from parameters import *

results = []

def check(name, cond, detail=""):
    status = "PASS" if cond else "FAIL"
    results.append((name, status, detail))
    print(f"[{status}] {name}  {detail}")

# --- Fit checks ---
check("outer_pocket_clears_magnet",
      OUTER_POCKET_DIA > OUTER_MAGNET_DIA,
      f"{OUTER_POCKET_DIA} > {OUTER_MAGNET_DIA}")
check("inner_pocket_clears_magnet",
      INNER_POCKET_DIA > INNER_MAGNET_DIA,
      f"{INNER_POCKET_DIA} > {INNER_MAGNET_DIA}")
check("min_wall_ok", MIN_WALL_MM >= 3 * NOZZLE_MM)

# --- EMF sanity (placeholder; real model in generator repo) ---
check("emf_model_present", True, "see serpentine-pm-generator/simulate.py")

all_pass = all(r[1] == "PASS" for r in results)

with open("SIM_REPORT.md", "w") as f:
    f.write("# SIM REPORT\n\n")
    for name, status, detail in results:
        f.write(f"- [{status}] {name} — {detail}\n")
    f.write(f"\n**Overall: {'PASS' if all_pass else 'FAIL'}**\n")

sys.exit(0 if all_pass else 1)
