# How talk-to-print works for you

You do **not** need a CAD website, Fusion, SolidWorks, or Onshape.

## Required (you already have this)

1. **This Grok chat** — voice or text. That is the talk half.
2. **GitHub connected** — already done (`lucidlooney2030`). Designs land in repos.
3. **Slicer + Kobra 3 Max** — Orca / Anycubic. That is the print half.

## Optional

| Install | Only if |
|---------|---------|
| [FreeCAD](https://www.freecad.org/downloads.php) | You want to open `.step` on your laptop and drag a face |
| [OpenSCAD](https://openscad.org/downloads.html) | You want a local code viewer. Not required for this family |
| Python + `pip install cadquery` | You want to rebuild STLs on your machine. I can rebuild them here |

## Not required

- New GitHub repos
- Cloud CAD accounts
- Attaching lost STLs
- Connecting Drive for this loop

## The loop you will actually run

1. You talk here ("gap 1.5 mm", "print the coupon").
2. I change `families/radial_outer/parameters.yaml` and the CadQuery script.
3. I export STEP + STL.
4. You download the STL from the chat or GitHub, slice, print.
5. You report fit / volts. We change one parameter and repeat.

Send-to-printer from chat is later. First prints are download → Orca → Kobra.
