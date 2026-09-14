#!/usr/bin/env python3
"""CadQuery kernel for the RF16S family. Params in, STL out."""
from __future__ import annotations

import json
import math
from pathlib import Path

import cadquery as cq

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "out"
OUT.mkdir(exist_ok=True)
PARAMS_PATH = ROOT / "params.json"

LOCKED_OUTER = 20.60
LOCKED_INNER = 5.60


def load_params() -> dict:
    return json.loads(PARAMS_PATH.read_text())


def save_params(p: dict) -> None:
    PARAMS_PATH.write_text(json.dumps(p, indent=2) + "\n")


def _radial_cyl(r0, depth, dia, z):
    return (
        cq.Workplane("YZ")
        .workplane(offset=r0)
        .circle(dia / 2.0)
        .extrude(depth)
        .translate((0, 0, z))
    )


def _bar(r0, r1, half_w, h, zmid, ang):
    depth = r1 - r0
    return (
        cq.Workplane("XY")
        .center(r0 + depth / 2.0, 0)
        .box(depth, 2 * half_w, h)
        .translate((0, 0, zmid))
        .rotate((0, 0, 0), (0, 0, 1), ang)
    )


def build_part(part: str, p: dict) -> Path:
    poles = int(p["poles"])
    pitch = 360.0 / poles
    air = float(p["air_gap_mm"])
    outer_face = float(p["outer_face_r_mm"])
    cage_thk = 4.00
    cage_outer = outer_face - air
    cage_inner = cage_outer - cage_thk
    inner_face = cage_inner - air
    slide = float(p["slide_mm"])
    if p.get("pockets_locked", True):
        od = LOCKED_OUTER
        id_ = LOCKED_INNER
    else:
        od = 20.0 + 2 * slide
        id_ = 5.0 + 2 * slide
    rotor_or = float(p["rotor_od_mm"]) / 2.0
    floor = 4.00
    mag_ax = 20.00
    interior = 28.00
    h = floor + interior
    z_cl = floor + 4.00 + mag_ax / 2.0
    lip = 0.80
    cup_id = outer_face - lip
    bearing = 22.20
    boss = (bearing + 8.0) / 2.0
    shaft = 8.00

    if part == "outer":
        wp = _outer(poles, pitch, outer_face, od, lip, cup_id, rotor_or, floor, interior, h, z_cl, bearing, boss, shaft, float(p["spine_w_mm"]))
    elif part == "inner":
        wp = _inner(poles, pitch, inner_face, id_, float(p["inner_spine_w_mm"]), bearing, shaft)
    elif part == "cage":
        wp = _cage(poles, pitch, cage_inner, cage_outer)
    elif part == "cap":
        wp = _cap(cup_id, bearing, shaft)
    else:
        raise ValueError(part)

    dest = OUT / f"RF16S-{part.upper()}.stl"
    cq.exporters.export(wp, str(dest), exportType="STL", tolerance=0.25, angularTolerance=0.4)
    return dest


def _outer(poles, pitch, face, od, lip, cup_id, rotor_or, floor, interior, h, z_cl, bearing, boss, shaft, spine_w):
    cup = cq.Workplane("XY").circle(rotor_or).extrude(h)
    cup = cup.faces(">Z").workplane().circle(cup_id).cutBlind(-interior)
    for i in range(poles):
        body = _radial_cyl(face - 0.2, 5.55, od, z_cl)
        lp = _radial_cyl(face - lip - 0.6, 1.6, 18.40, z_cl)
        cup = cup.cut(body.union(lp).rotate((0, 0, 0), (0, 0, 1), i * pitch))
    r_hub, r_hoop0, r_hoop1, r_rim = boss + 5, 33.5, 37.5, cup_id - 2.2
    mid = 0.5 * (r_hub + r_rim)
    gap = (2 * math.pi * mid / poles - spine_w) / 2.0 - 0.2
    for i in range(poles):
        cup = cup.cut(_bar(r_hub, r_hoop0, gap, floor, floor / 2, i * pitch))
        cup = cup.cut(_bar(r_hoop1, r_rim, gap * 0.9, floor, floor / 2, i * pitch))
    cup = cup.union(
        cq.Workplane("XY").circle(boss).extrude(7.2).translate((0, 0, -(7.2 - floor)))
    )
    cup = cup.cut(
        cq.Workplane("XY").circle(bearing / 2).extrude(10).translate((0, 0, -(7.2 - floor) - 1))
    )
    cup = cup.cut(cq.Workplane("XY").circle(shaft / 2 + 0.25).extrude(h + 4).translate((0, 0, -2)))
    return cup


def _inner(poles, pitch, face, id_, spine_w, bearing, shaft):
    back = face - 5.00
    rim_o, rim_i = face + 0.15, back - 1.6
    hub_h = 3 * 5.35 + 3.00
    boss = (bearing + 7.0) / 2.0
    hub = cq.Workplane("XY").circle(rim_o).circle(rim_i).extrude(hub_h)
    hub = hub.union(cq.Workplane("XY").circle(boss).extrude(hub_h))
    r0, r1 = boss - 0.4, rim_i + 0.6
    for i in range(8):
        ang = i * 45 + 22.5
        sp = (
            cq.Workplane("XY")
            .center((r0 + r1) / 2, 0)
            .box(r1 - r0, spine_w, hub_h)
            .translate((0, 0, hub_h / 2))
            .rotate((0, 0, 0), (0, 0, 1), ang)
        )
        hub = hub.union(sp)
    hub = hub.union(cq.Workplane("XY").circle(30.2).circle(27.5).extrude(hub_h))
    z0 = 1.50 + id_ / 2
    for i in range(poles):
        for k in range(3):
            body = _radial_cyl(face - 5.35, 5.95, id_, z0 + k * 5.35)
            hub = hub.cut(body.rotate((0, 0, 0), (0, 0, 1), i * pitch))
    hub = hub.cut(cq.Workplane("XY").circle(bearing / 2).extrude(7.3).translate((0, 0, -0.1)))
    hub = hub.cut(cq.Workplane("XY").circle(shaft / 2 + 0.25).extrude(hub_h + 2).translate((0, 0, -1)))
    return hub


def _cage(poles, pitch, inner, outer):
    h = 22.0
    ring = cq.Workplane("XY").circle(outer).circle(inner).extrude(h)
    mid = 0.5 * (inner + outer)
    for i in range(poles):
        win = (
            cq.Workplane("XY")
            .center(mid, 0)
            .box(outer - inner + 2.4, 11.0, 18.0)
            .translate((0, 0, 11.0))
            .rotate((0, 0, 0), (0, 0, 1), i * pitch)
        )
        ring = ring.cut(win)
    for i in range(4):
        a = math.radians(i * 90)
        ring = ring.cut(
            cq.Workplane("XY").center(20 * math.cos(a), 20 * math.sin(a)).circle(1.7).extrude(h + 4).translate((0, 0, -2))
        )
    return ring


def _cap(cup_id, bearing, shaft):
    cap = cq.Workplane("XY").circle(cup_id - 1.2).extrude(4.0)
    cap = cap.union(cq.Workplane("XY").circle((bearing + 7) / 2).extrude(7.2))
    cap = cap.cut(cq.Workplane("XY").circle(bearing / 2).extrude(8))
    cap = cap.cut(cq.Workplane("XY").circle(shaft / 2 + 0.3).extrude(12).translate((0, 0, -1)))
    for i in range(4):
        a = math.radians(i * 90)
        cap = cap.cut(
            cq.Workplane("XY").center(20 * math.cos(a), 20 * math.sin(a)).circle(1.7).extrude(8).translate((0, 0, -1))
        )
    return cap
