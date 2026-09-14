#!/usr/bin/env python3
"""Honest gates for idea-to-print.

Tier 1: geometry / packing / printer.
Tier 2: lumped Faraday estimate with printed assumptions.
This is not FEM. This is not a verified machine.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

# Default example numbers match schemas/parameters.example.yaml
DEFAULTS = {
    "nozzle_mm": 0.4,
    "layer_mm": 0.2,
    "bed_x_mm": 420.0,
    "bed_y_mm": 420.0,
    "magnet_dia_mm": 20.0,
    "magnet_thk_mm": 3.0,
    "clearance_slide_mm": 0.30,
    "pocket_dia_mm": 20.60,
    "pocket_depth_mm": 3.35,
    "min_wall_mm": 1.2,
    "od_mm": 120.0,
    "gap_mm": 2.0,
    "poles": 8,
    "turns": 200,
    "fill_factor": 0.55,
    "wire_awg": 28,
    "window_area_mm2": 80.0,
    "kc": 0.75,
    "Bg_T": 0.50,  # assumption for dual-rotor + steel; not Br
    "winding": "wave",
}

# Bare copper diameter mm (approx) and ohm/m @ 20C
AWG = {
    22: (0.645, 0.0530),
    24: (0.511, 0.0842),
    26: (0.405, 0.1339),
    28: (0.321, 0.2129),
    30: (0.255, 0.3386),
}


def copper_area_mm2(turns: int, awg: int) -> float:
    d, _ = AWG[awg]
    return turns * math.pi * (d / 2.0) ** 2


def lumped_rms_per_coil(rpm: float, p: dict) -> dict:
    f = (rpm / 60.0) * (p["poles"] / 2.0)
    am = math.pi * (p["magnet_dia_mm"] / 2000.0) ** 2
    phi = p["kc"] * p["Bg_T"] * am
    e_peak = p["turns"] * 2 * math.pi * f * phi
    e_rms = e_peak / math.sqrt(2.0)
    return {"rpm": rpm, "f_hz": f, "e_rms_V": e_rms, "e_peak_V": e_peak}


def run(p: dict) -> dict:
    fails = []
    notes = []

    if p["pocket_dia_mm"] + 1e-9 < p["magnet_dia_mm"] + 2 * p["clearance_slide_mm"]:
        fails.append("pocket_dia tighter than magnet + slide clearance")
    if p["pocket_depth_mm"] + 1e-9 < p["magnet_thk_mm"] + 0.2:
        fails.append("pocket_depth shallower than magnet + 0.2 mm")
    if p["min_wall_mm"] < 3 * p["nozzle_mm"]:
        fails.append("min_wall < 3*nozzle")
    if p["od_mm"] > min(p["bed_x_mm"], p["bed_y_mm"]):
        fails.append("OD exceeds printer bed")
    if p["winding"] == "zigzag" and p["poles"] % 2 == 0:
        fails.append("zigzag winding on even-pole single-phase cancels — use wave")
    if p["wire_awg"] not in AWG:
        fails.append(f"unsupported AWG {p['wire_awg']}")
    else:
        need = copper_area_mm2(p["turns"], p["wire_awg"]) / p["fill_factor"]
        if need > p["window_area_mm2"]:
            fails.append(
                f"coil window {p['window_area_mm2']} mm2 cannot pack "
                f"{p['turns']} turns of AWG {p['wire_awg']} at fill {p['fill_factor']}"
            )

    estimates = [lumped_rms_per_coil(rpm, p) for rpm in (60, 120, 300, 1500)]
    notes.append(
        f"ESTIMATE only. Assumed Bg={p['Bg_T']} T, kc={p['kc']}, not a FEM result."
    )
    notes.append("Energy: P_elec < tau*omega. Magnets do not run the machine.")

    return {
        "tier": "geometry_plus_lumped_faraday",
        "pass": not fails,
        "fails": fails,
        "notes": notes,
        "estimates_per_coil": estimates,
        "assumptions": {
            "Bg_T": p["Bg_T"],
            "kc": p["kc"],
            "turns": p["turns"],
            "poles": p["poles"],
            "fill_factor": p["fill_factor"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--params", type=Path, help="optional JSON overrides")
    args = parser.parse_args()
    p = dict(DEFAULTS)
    if args.params:
        p.update(json.loads(args.params.read_text()))
    report = run(p)
    print(json.dumps(report, indent=2))
    return 0 if report["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
