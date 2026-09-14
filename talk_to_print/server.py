#!/usr/bin/env python3
"""Talk-to-print server. Voice/text → param patch → STL → orbit viewer."""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, send_file

from kernel import load_params, save_params, build_part

ROOT = Path(__file__).resolve().parent
app = Flask(__name__, static_folder=str(ROOT / "static"), static_url_path="/static")


def parse_command(text: str, p: dict) -> tuple[dict, str]:
    t = text.lower().strip()
    note = []
    if re.search(r"\b(outer|cup|rotor)\b", t) and "inner" not in t:
        p["part"] = "outer"; note.append("showing outer")
    if re.search(r"\binner\b", t) or re.search(r"\bhub\b", t):
        p["part"] = "inner"; note.append("showing inner")
    if re.search(r"\bcage\b", t) or "coil" in t or "stator" in t:
        p["part"] = "cage"; note.append("showing cage")
    if re.search(r"\bcap\b", t) or "lid" in t:
        p["part"] = "cap"; note.append("showing cap")
    m = re.search(r"air\s*gap\s*(?:to|of|=)?\s*([0-9.]+)", t)
    if m:
        p["air_gap_mm"] = max(0.4, min(3.0, float(m.group(1))))
        note.append(f"air gap {p['air_gap_mm']} mm")
    m = re.search(r"(\d+)\s*poles?", t)
    if m:
        n = int(m.group(1))
        if n in (8, 12, 16, 18, 24):
            p["poles"] = n; note.append(f"{n} poles")
    if "thinner" in t or "less filament" in t or "lighter" in t:
        if p["part"] == "inner":
            p["inner_spine_w_mm"] = max(2.2, p["inner_spine_w_mm"] - 0.6)
        else:
            p["spine_w_mm"] = max(3.5, p["spine_w_mm"] - 1.0)
        note.append("spines thinned")
    if "thicker" in t or "stronger" in t:
        if p["part"] == "inner":
            p["inner_spine_w_mm"] = min(8.0, p["inner_spine_w_mm"] + 0.6)
        else:
            p["spine_w_mm"] = min(12.0, p["spine_w_mm"] + 1.0)
        note.append("spines thickened")
    if "unlock pocket" in t:
        p["pockets_locked"] = False; note.append("pockets unlocked")
    if "lock pocket" in t:
        p["pockets_locked"] = True; note.append("pockets locked")
    if not note:
        note.append("no numeric change")
    return p, "; ".join(note)


def llm_patch(text: str, p: dict):
    key = os.environ.get("XAI_API_KEY")
    if not key:
        return None
    body = json.dumps({
        "model": "grok-4-fast-non-reasoning",
        "messages": [
            {"role": "system", "content": "Return ONLY JSON overrides for keys part, poles, air_gap_mm, spine_w_mm, inner_spine_w_mm, rotor_od_mm, pockets_locked. Never change pocket diameters."},
            {"role": "user", "content": f"params={json.dumps(p)} command={text}"},
        ],
        "temperature": 0,
    }).encode()
    req = urllib.request.Request("https://api.x.ai/v1/chat/completions", data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            raw = json.loads(r.read().decode())["choices"][0]["message"]["content"]
        raw = raw.strip().strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
        patch = json.loads(raw)
        p.update({k: v for k, v in patch.items() if k in p or k == "part"})
        return p
    except Exception:
        return None


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.get("/api/params")
def get_params():
    return jsonify(load_params())

@app.post("/api/say")
def say():
    text = (request.json or {}).get("text", "")
    p = load_params()
    patched = llm_patch(text, dict(p))
    if patched:
        p, note = patched, "llm patch"
    else:
        p, note = parse_command(text, p)
    save_params(p)
    path = build_part(p["part"], p)
    return jsonify({"ok": True, "note": note, "params": p, "stl": f"/stl/{path.name}?v={path.stat().st_mtime_ns}"})

@app.post("/api/rebuild")
def rebuild():
    p = request.json or load_params()
    save_params(p)
    path = build_part(p.get("part", "outer"), p)
    return jsonify({"ok": True, "params": p, "stl": f"/stl/{path.name}?v={path.stat().st_mtime_ns}"})

@app.get("/stl/<name>")
def stl(name):
    from kernel import OUT
    f = OUT / name
    if not f.exists():
        p = load_params()
        f = build_part(p["part"], p)
    return send_file(f, mimetype="model/stl")

if __name__ == "__main__":
    p = load_params()
    try:
        build_part(p["part"], p)
    except Exception as e:
        print("initial build skipped:", e)
    print("Talk-to-print  http://127.0.0.1:8787")
    app.run(host="127.0.0.1", port=8787, debug=False)
