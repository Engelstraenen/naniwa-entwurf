#!/usr/bin/env python3
"""Schneidet die Nudel-Gerichtfotos komplett (ganzer Teller, ohne Text/Pfeile) aus den PDF-Seiten aus.
PDF: https://noodle.naniwa.de/speisekarteeng.pdf (Seite NN = nudeln/nNN.jpg).
Seiten rendern: osascript -l JavaScript render.js <pdf> <ordner> 3
Aufruf: python3 tools/nudel_fotos.py <ordner-mit-pNN.png> [kontaktbogen.png]"""
import sys, pathlib
import numpy as np
from PIL import Image
from scipy import ndimage as nd

pages_dir = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(__file__).resolve().parent.parent / "site/assets/img/nudeln"
LW = 480  # Arbeitsbreite für die Erkennung

def dish_mask(im):
    W, H = im.size
    sc = LW / W
    g = np.asarray(im.convert("L").resize((LW, int(H*sc)), Image.BILINEAR)) > 30
    h, w = g.shape
    g[:, :int(.03*w)] = 0; g[:, int(.80*w):] = 0          # Logo-Rand und Menüspalte rechts
    g[:int(.035*h), :] = 0; g[int(.955*h):, :] = 0         # Pfeile oben/unten
    g = nd.binary_opening(g, iterations=2)                 # dünne Linien und Schrift weg
    lab, n = nd.label(nd.binary_dilation(g, iterations=1))
    sizes = nd.sum(np.ones_like(lab), lab, range(1, n+1))
    big = int(np.argmax(sizes)) + 1
    keep = lab == big
    # weitere große Teile (Löffel, Wasabi-Schälchen), keine Schrift
    objs = nd.find_objects(lab)
    by, bx = objs[big-1]
    mh, mw = (by.stop-by.start)*.05, (bx.stop-bx.start)*.05
    for k, s in enumerate(sizes, 1):
        if k == big or s < 0.03*sizes[big-1]: continue
        y, x = objs[k-1]   # nur Teile, die im Bereich des Gerichts liegen (keine Schrift/Linien daneben)
        if x.start >= bx.start-mw and x.stop <= bx.stop+mw and y.start >= by.start-mh and y.stop <= by.stop+mh:
            keep |= lab == k
    keep = nd.binary_fill_holes(keep)
    return nd.binary_dilation(keep, iterations=4), sc

thumbs = []
for f in sorted(out_dir.glob("n*.jpg")):
    p = pages_dir / f"p{f.stem[1:]}.png"
    im = Image.open(p).convert("RGB"); W, H = im.size
    m, sc = dish_mask(im)
    ys, xs = np.where(m)
    l, t, r, b = int(xs.min()/sc), int(ys.min()/sc), int((xs.max()+1)/sc), int((ys.max()+1)/sc)
    full = Image.fromarray((m*255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
    clean = Image.composite(im, Image.new("RGB", (W, H)), full)   # alles außer dem Gericht schwarz
    # Blätter-Pfeile der PDF (oben/unten Mitte) schwarz übermalen
    from PIL import ImageDraw
    d = ImageDraw.Draw(clean)
    d.rectangle((int(.44*W), 0, int(.56*W), int(.038*H)), fill=(0, 0, 0))
    d.rectangle((int(.44*W), int(.955*H), int(.56*W), H), fill=(0, 0, 0))
    pad = int(.035*H)
    l, t, r, b = max(l-pad, 0), max(t-pad, 0), min(r+pad, W), min(b+pad, H)
    crop = clean.crop((l, t, r, b)); w, h = crop.size
    nw, nh = (int(h*1.5), h) if w/h < 1.5 else (w, int(w/1.5))
    canvas = Image.new("RGB", (nw, nh)); canvas.paste(crop, ((nw-w)//2, (nh-h)//2))
    canvas = canvas.resize((1200, 800), Image.LANCZOS)
    canvas.save(f, quality=86, optimize=True, progressive=True)
    thumbs.append(canvas.resize((240, 160)))
print(len(thumbs), "Fotos")
if len(sys.argv) > 2:
    cols = 8; rows = (len(thumbs)+cols-1)//cols
    sheet = Image.new("RGB", (cols*240, rows*160), (40, 40, 40))
    for k, t in enumerate(thumbs): sheet.paste(t, ((k % cols)*240, (k//cols)*160))
    sheet.save(sys.argv[2])
