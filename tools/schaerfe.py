#!/usr/bin/env python3
"""Echte Detail-Auflösung eines Videos messen (Masterfile: MiniMax „2K“ ist kein echtes 2K).
Vergleicht die Kanten-Schärfe (Laplace-Varianz) jeder Sekunde mit dem 4K-Startbild,
das auf 2560/1920/1280/854 px heruntergerechnet und wieder auf Videogröße hochgerechnet wurde.
Aufruf: python3 tools/schaerfe.py <video.mp4> <startbild.jpg>"""
import sys, subprocess, tempfile, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage as nd

video, start = sys.argv[1], sys.argv[2]
w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", video], capture_output=True, text=True).stdout.strip().split(","))
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", video], capture_output=True, text=True).stdout)

def sharp(img):
    a = np.asarray(img.convert("L"), dtype=np.float32)
    return float(nd.laplace(a).var())

ref = Image.open(start).convert("RGB").resize((w, h), Image.LANCZOS)
levels = {}
for lw in (w, 1920, 1280, 854):
    if lw > w: continue
    lh = round(lw * h / w)
    levels[lw] = sharp(ref.resize((lw, lh), Image.LANCZOS).resize((w, h), Image.BICUBIC))
print(f"Datei {w}x{h}, {dur:.1f} s · Startbild-Schärfe je Stufe:", {k: round(v) for k, v in levels.items()})
tmp = pathlib.Path(tempfile.mkdtemp())
for s in range(int(dur)):
    f = tmp / f"s{s}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{s + 0.5}", "-i", video, "-frames:v", "1", str(f)], check=True)
    v = sharp(Image.open(f))
    best = min(levels, key=lambda k: abs(levels[k] - v))
    print(f"  {s:2d}-{s+1:2d} s: Schärfe {v:7.0f} ≈ {best}px-Detail")
