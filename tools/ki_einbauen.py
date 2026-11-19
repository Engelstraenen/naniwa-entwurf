#!/usr/bin/env python3
"""Baut KI-Fotos aus ki_sushi/ in die Sushi-Karte ein.
Dateiname = '<Nr>.jpg' oder '<Nr> <NAME>.jpg' (z. B. 'M12 TEKKA-AVO.jpg'). Aufruf: python3 tools/ki_einbauen.py"""
import json, pathlib, re, subprocess
root = pathlib.Path(__file__).resolve().parent.parent
p = root / "site/assets/menu-data.js"
s = p.read_text(encoding="utf-8")
d = json.loads(s[len("window.NANIWA_MENU="):-1])
out = root / "site/assets/img/karte"
n = 0
for f in sorted((root / "ki_sushi").glob("*.jpg")):
    if f.stem.startswith("uebersicht"):
        continue
    parts = f.stem.split(" ", 1)
    for c in d["sushi"]:
        for g in c["g"]:
            if g["nr"] == parts[0] and (len(parts) == 1 or g["n"] == parts[1]):
                slug = "ki_" + re.sub(r"[^a-z0-9]+", "-", f.stem.lower()).strip("-") + ".jpg"
                subprocess.run(["sips", "-Z", "1000", "-s", "formatOptions", "78", str(f), "--out", str(out / slug)], capture_output=True)
                g["b"] = "../assets/img/karte/" + slug
                g["ki"] = 1
                n += 1
p.write_text("window.NANIWA_MENU=" + json.dumps(d, ensure_ascii=False) + ";", encoding="utf-8")
print("eingebaut:", n, "| ohne Foto:", [g["nr"] + " " + g["n"] for c in d["sushi"] for g in c["g"] if not g["b"]].__len__())
