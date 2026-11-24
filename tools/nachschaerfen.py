#!/usr/bin/env python3
"""Videos (und Bilder) nachschärfen, ohne Hochskalieren.
Kette: leichtes Entrauschen (sonst werden Kompressions-Klötzchen mitgeschärft)
→ CAS (kontrastadaptiv, schärft nur echte Kanten) → feines Unsharp.
Danach Schärfe vorher/nachher je Sekunde messen (Laplace-Varianz).

Aufruf:
  python3 tools/nachschaerfen.py <eingang.mp4|.jpg> [ausgang] [--staerke leicht|mittel|stark] [--vergleich]
  --vergleich: zusätzlich Vorher|Nachher-Video (links Original, rechts geschärft) als <ausgang>-vergleich.mp4
"""
import sys, subprocess, tempfile, pathlib, argparse
import numpy as np
from PIL import Image
from scipy import ndimage as nd

STUFEN = {  # hqdn3d (Rauschen), cas (0–1), unsharp-Menge
    "leicht": ("1:1:2:2", 0.35, 0.35),
    "mittel": ("1.5:1.5:3:3", 0.55, 0.55),
    "stark":  ("2:2:4:4", 0.75, 0.8),
}

def kette(stufe):
    dn, cas, us = STUFEN[stufe]
    return f"hqdn3d={dn},cas=strength={cas},unsharp=5:5:{us}:5:5:0"

def probe(p, key):
    return subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", key,
                           "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout.strip()

def schaerfe(img):
    a = np.asarray(img.convert("L"), dtype=np.float32)
    return float(nd.laplace(a).var())

def bild(t, video, tmp, name):
    f = tmp / f"{name}_{t:.1f}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t}", "-i", str(video), "-frames:v", "1", str(f)], check=True)
    return Image.open(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ein"); ap.add_argument("aus", nargs="?")
    ap.add_argument("--staerke", default="mittel", choices=STUFEN)
    ap.add_argument("--vergleich", action="store_true")
    a = ap.parse_args()
    ein = pathlib.Path(a.ein)
    aus = pathlib.Path(a.aus) if a.aus else ein.with_name(f"{ein.stem}-scharf{ein.suffix}")
    vf = kette(a.staerke)

    if ein.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ein), "-vf", vf.split(",", 1)[1],
                        "-q:v", "2", str(aus)], check=True)
        print(f"Bild: Schärfe {schaerfe(Image.open(ein)):.0f} → {schaerfe(Image.open(aus)):.0f} · {aus}")
        return

    w, h = probe(ein, "stream=width,height").split(",")
    fps = probe(ein, "stream=r_frame_rate")
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(ein)],
                               capture_output=True, text=True).stdout)
    hat_ton = bool(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index",
                                   "-of", "csv=p=0", str(ein)], capture_output=True, text=True).stdout.strip())
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", str(ein), "-vf", vf + ",format=yuv420p",
           "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-movflags", "+faststart"]
    cmd += ["-c:a", "copy"] if hat_ton else ["-an"]
    subprocess.run(cmd + [str(aus)], check=True)

    tmp = pathlib.Path(tempfile.mkdtemp())
    print(f"{ein.name} {w}x{h} @ {fps}, {dur:.1f} s · Stufe {a.staerke} ({vf})")
    vs, ns = [], []
    for s in range(int(dur)):
        v = schaerfe(bild(s + .5, ein, tmp, "v")); n = schaerfe(bild(s + .5, aus, tmp, "n"))
        vs.append(v); ns.append(n)
        print(f"  {s:2d}-{s+1:2d} s: {v:7.0f} → {n:7.0f}  (+{(n / v - 1) * 100:3.0f} %)")
    print(f"Mittel {np.mean(vs):.0f} → {np.mean(ns):.0f} (+{(np.mean(ns) / np.mean(vs) - 1) * 100:.0f} %) · {aus}")

    if a.vergleich:
        vg = aus.with_name(f"{aus.stem}-vergleich.mp4")
        hw = int(w) // 2
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ein), "-i", str(aus), "-filter_complex",
                        f"[0:v]crop={hw}:{h}:0:0[l];[1:v]crop={int(w) - hw}:{h}:{hw}:0[r];[l][r]hstack,"
                        f"drawbox=x={hw - 1}:y=0:w=2:h={h}:color=white@0.9:t=fill,format=yuv420p",
                        "-c:v", "libx264", "-crf", "15", "-preset", "slow", "-movflags", "+faststart", "-an", str(vg)],
                       check=True)
        print(f"Vergleich (links vorher, rechts nachher): {vg}")

if __name__ == "__main__":
    main()
