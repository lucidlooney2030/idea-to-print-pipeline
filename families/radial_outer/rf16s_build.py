#!/usr/bin/env python3
"""RF16S dual-magnet radial flux — CadQuery family.

Source of truth: dimensions below match families/radial_outer/parameters.yaml.
Exports STEP + STL. No hand-edited meshes.
"""
from __future__ import annotations

import math
from pathlib import Path

import cadquery as cq

POLES = 16
PITCH = 360.0 / POLES
AIR_GAP = 1.00

OUTER_MAG_DIA = 20.00
OUTER_MAG_THK = 5.00
INNER_MAG_DIA = 5.00
INNER_MAG_THK = 5.00
INNER_STACK = 3

OUTER_FACE_R = 56.38
CAGE_THK = 4.00
CAGE_OUTER_R = OUTER_FACE_R - AIR_GAP
CAGE_INNER_R = CAGE_OUTER_R - CAGE_THK
INNER_FACE_R = CAGE_INNER_R - AIR_GAP
INNER_BACK_R = INNER_FACE_R - INNER_MAG_THK
OUTER_BACK_R = OUTER_FACE_R + OUTER_MAG_THK

SLIDE = 0.30
OUTER_POCKET_D = OUTER_MAG_DIA + 2 * SLIDE
OUTER_POCKET_DEPTH = OUTER_MAG_THK + 0.35
OUTER_LIP_ID = 18.40
OUTER_LIP = 0.80
INNER_POCKET_D = INNER_MAG_DIA + 2 * SLIDE
INNER_POCKET_DEPTH = INNER_MAG_THK + 0.35

ROTOR_OD = 132.00
ROTOR_OR = ROTOR_OD / 2.0
ROTOR_FLOOR = 4.00
MAG_AXIAL = OUTER_MAG_DIA
ROTOR_INTERIOR = MAG_AXIAL + 8.00
ROTOR_H = ROTOR_FLOOR + ROTOR_INTERIOR

BEARING_BORE = 22.20
BEARING_DEPTH = 7.20
SHAFT_D = 8.00

CAGE_H = MAG_AXIAL + 6.00
WINDOW_W = 12.00
HUB_H = INNER_STACK * INNER_POCKET_DEPTH + 3.00
HUB_CORE_R = 16.00
HUB_SPOKE_W = 6.00

OUT = Path(__file__).resolve().parent / "exports"
OUT.mkdir(parents=True, exist_ok=True)


def _export(name: str, wp: cq.Workplane) -> None:
    stl = OUT / f"{name}.stl"
    step = OUT / f"{name}.step"
    cq.exporters.export(wp, str(stl), exportType="STL", tolerance=0.15, angularTolerance=0.3)
    cq.exporters.export(wp, str(step), exportType="STEP")
    print(f"wrote {stl.name} {stl.stat().st_size // 1024} KiB")


def _radial_cyl(r0: float, depth: float, dia: float, z: float) -> cq.Workplane:
    return (
        cq.Workplane("YZ")
        .workplane(offset=r0)
        .circle(dia / 2.0)
        .extrude(depth)
        .translate((0, 0, z))
    )


def make_fit_coupon() -> cq.Workplane:
    plate = cq.Workplane("XY").box(50, 28, 8)
    plate = plate.faces(">Z").workplane().center(-12, 0).hole(OUTER_POCKET_D, OUTER_POCKET_DEPTH)
    plate = plate.faces(">Z").workplane().center(12, 0).hole(INNER_POCKET_D, INNER_POCKET_DEPTH)
    plate = plate.faces(">Z").workplane().center(-12, 10).hole(2.0, 2.0)
    plate = plate.faces(">Z").workplane().center(12, 10).hole(1.2, 2.0)
    return plate


def make_outer() -> cq.Workplane:
    cup = cq.Workplane("XY").circle(ROTOR_OR).extrude(ROTOR_H)
    inner_r = OUTER_FACE_R - OUTER_LIP
    cup = cup.faces(">Z").workplane().circle(inner_r).cutBlind(-ROTOR_INTERIOR)
    z_cl = ROTOR_FLOOR + 4.00 + MAG_AXIAL / 2.0
    for i in range(POLES):
        ang = i * PITCH
        body = _radial_cyl(OUTER_FACE_R - 0.2, OUTER_POCKET_DEPTH + 0.2, OUTER_POCKET_D, z_cl)
        lip = _radial_cyl(OUTER_FACE_R - OUTER_LIP - 0.6, OUTER_LIP + 0.8, OUTER_LIP_ID, z_cl)
        cup = cup.cut(body.union(lip).rotate((0, 0, 0), (0, 0, 1), ang))
    boss = (
        cq.Workplane("XY")
        .circle((BEARING_BORE + 8.0) / 2.0)
        .extrude(BEARING_DEPTH)
        .translate((0, 0, -(BEARING_DEPTH - ROTOR_FLOOR)))
    )
    cup = cup.union(boss)
    bore = (
        cq.Workplane("XY")
        .circle(BEARING_BORE / 2.0)
        .extrude(BEARING_DEPTH + 2)
        .translate((0, 0, -(BEARING_DEPTH - ROTOR_FLOOR) - 1))
    )
    return cup.cut(bore)


def make_inner() -> cq.Workplane:
    rim_outer = INNER_FACE_R + 0.4
    rim_inner = INNER_BACK_R - 2.0
    hub = cq.Workplane("XY").circle(rim_outer).circle(rim_inner).extrude(HUB_H)
    hub = hub.union(cq.Workplane("XY").circle(HUB_CORE_R).extrude(HUB_H))
    for i in range(6):
        spoke = (
            cq.Workplane("XY")
            .box(rim_inner, HUB_SPOKE_W, HUB_H)
            .translate((rim_inner / 2.0, 0, HUB_H / 2.0))
            .rotate((0, 0, 0), (0, 0, 1), i * 60.0)
        )
        hub = hub.union(spoke)
    z0 = 1.50 + INNER_POCKET_D / 2.0
    for i in range(POLES):
        for k in range(INNER_STACK):
            z = z0 + k * INNER_POCKET_DEPTH
            body = _radial_cyl(INNER_FACE_R - INNER_POCKET_DEPTH, INNER_POCKET_DEPTH + 0.8, INNER_POCKET_D, z)
            hub = hub.cut(body.rotate((0, 0, 0), (0, 0, 1), i * PITCH))
    shaft = cq.Workplane("XY").circle(SHAFT_D / 2.0 + 0.15).extrude(HUB_H + 2).translate((0, 0, -1))
    return hub.cut(shaft)


def make_cage() -> cq.Workplane:
    ring = cq.Workplane("XY").circle(CAGE_OUTER_R).circle(CAGE_INNER_R).extrude(CAGE_H)
    flange_t = 2.2
    for z in (0.0, CAGE_H - flange_t):
        fl = (
            cq.Workplane("XY")
            .circle(CAGE_OUTER_R + 1.2)
            .circle(CAGE_INNER_R - 1.2)
            .extrude(flange_t)
            .translate((0, 0, z))
        )
        ring = ring.union(fl)
    depth = (CAGE_OUTER_R - CAGE_INNER_R) + 3.0
    z0 = flange_t
    h = CAGE_H - 2 * flange_t
    mid_r = 0.5 * (CAGE_OUTER_R + CAGE_INNER_R)
    for i in range(POLES):
        win = (
            cq.Workplane("XY")
            .center(mid_r, 0)
            .box(depth, WINDOW_W, h)
            .translate((0, 0, z0 + h / 2.0))
            .rotate((0, 0, 0), (0, 0, 1), i * PITCH)
        )
        ring = ring.cut(win)
    for i in range(4):
        a = i * 90.0
        x = 20.0 * math.cos(math.radians(a))
        y = 20.0 * math.sin(math.radians(a))
        hole = cq.Workplane("XY").center(x, y).circle(1.7).extrude(CAGE_H + 4).translate((0, 0, -2))
        ring = ring.cut(hole)
    return ring


def main() -> None:
    _export("RF16S-COUPON", make_fit_coupon())
    _export("RF16S-OUTER", make_outer())
    _export("RF16S-INNER", make_inner())
    _export("RF16S-CAGE", make_cage())


if __name__ == "__main__":
    main()
