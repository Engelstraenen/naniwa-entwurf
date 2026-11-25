#!/usr/bin/env python3
"""Liest aus der echten Nudel-Speisekarte (data/pdf/speisekarteeng.pdf) je Gericht:
- Allergen-Symbole (kleine farbige Kreise unter der Beschreibung, per Bildvergleich mit der Legende auf der letzten Seite)
- Zusatzstoff-Hochzahlen hinter dem Namen (1–7)
- grünes Schild „Also available completely vegetarian“
Schreibt data/noodle_symbols.json und die Symbol-Bilder nach site/assets/img/allergene/.
Braucht PyMuPDF (pip install pymupdf). Aufruf: python3 tools/nudel_symbole.py"""
import json, pathlib, re
import numpy as np
import pymupdf
from PIL import Image

root = pathlib.Path(__file__).resolve().parent.parent
doc = pymupdf.open(root / "data/pdf/speisekarteeng.pdf")
outimg = root / "site/assets/img/allergene"
outimg.mkdir(parents=True, exist_ok=True)

KEY = {  # Legenden-Text → Schlüssel, deutscher Name
    "Wheat": ("weizen", "Weizen"), "Rye": ("roggen", "Roggen"), "Barley": ("gerste", "Gerste"), "Oats": ("hafer", "Hafer"),
    "Spelt": ("dinkel", "Dinkel"), "Khorasan wheat": ("kamut", "Khorasan-Weizen"), "Crustaceans": ("krebstiere", "Krebstiere"),
    "Eggs": ("eier", "Eier"), "Fish": ("fisch", "Fisch"), "Peanuts": ("erdnuss", "Erdnüsse"), "Soybeans": ("soja", "Soja"),
    "Dairy": ("milch", "Milch"), "Almonds": ("mandeln", "Mandeln"), "hazelnuts": ("haselnuss", "Haselnüsse"),
    "Walnuts": ("walnuss", "Walnüsse"), "Cashews": ("cashew", "Cashewkerne"), "Peacans": ("pekan", "Pekannüsse"),
    "Brazil nuts": ("paranuss", "Paranüsse"), "Pistachios": ("pistazie", "Pistazien"), "Macadamias": ("macadamia", "Macadamianüsse"),
    "Celery": ("sellerie", "Sellerie"), "Mustard": ("senf", "Senf"), "Sesame seeds": ("sesam", "Sesam"),
    "Sulphor dioxide / Sulphites": ("sulfite", "Schwefeldioxid/Sulfite"), "Lupines": ("lupinen", "Lupinen"), "Molluscs": ("weichtiere", "Weichtiere"),
}

SMASK = {im[0]: im[1] for pg in doc for im in pg.get_images(full=True)}

def bild(xref):
    pix = pymupdf.Pixmap(doc, xref)
    if pix.n - pix.alpha > 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    if SMASK.get(xref):  # Transparenz (runde Symbole) aus der Soft-Mask
        pix = pymupdf.Pixmap(pix, pymupdf.Pixmap(doc, SMASK[xref]))
    im = Image.frombytes("RGBA" if pix.alpha else "RGB", (pix.width, pix.height), pix.samples).convert("RGBA")
    return im

def vec(im):
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255)); bg.alpha_composite(im)
    return np.asarray(bg.convert("RGB").resize((32, 32), Image.LANCZOS), dtype=float)

# Legende (letzte Seite)
leg = {}
lp = doc[-1]
for im in lp.get_images(full=True):
    for r in lp.get_image_rects(im[0]):
        t = lp.get_textbox(pymupdf.Rect(r.x1 + 2, r.y0 - 2, r.x1 + 400, r.y0 + 16)).strip().split("\n")[0]
        name = next(k for k in KEY if t.startswith(k))
        leg[KEY[name][0]] = vec(bild(im[0]))

cache, gesp = {}, set()
def allergen(xref):
    if xref not in cache:
        im = bild(xref); v = vec(im)
        k = min(leg, key=lambda k: np.abs(v - leg[k]).mean())
        assert np.abs(v - leg[k]).mean() < 15, (xref, k)
        cache[xref] = k
        if k not in gesp:
            im.save(outimg / f"{k}.png"); gesp.add(k)
    return cache[xref]

def spans_of(p):
    return [s for b in p.get_text("dict")["blocks"] for l in b.get("lines", []) for s in l["spans"] if s["text"].strip()]

items = []
for i, p in enumerate(doc[:-1]):
    sp = spans_of(p)
    if "RAMEN EXTRAS" in p.get_text():  # Raster: Nummer + Name in einer Zeile, Symbole rechts neben dem Preis
        tags = [s for s in sp if s["size"] == 25 and s["font"].startswith("Gopher") and re.fullmatch(r"E\d+", s["text"].strip())]
        imgs = [(r, im[0]) for im in p.get_images(full=True) for r in p.get_image_rects(im[0]) if r.width < 40]
        for t in tags:
            tx, ty = t["bbox"][0], t["bbox"][1]
            al = []
            for r, x in sorted(imgs, key=lambda q: q[0].x0):
                best = min(tags, key=lambda u: (u["bbox"][0] > r.x0 or u["bbox"][1] > r.y0, abs(r.y0 - u["bbox"][1]) + abs(r.x0 - u["bbox"][0]) * .2))
                if best is t and allergen(x) not in al: al.append(allergen(x))
            items.append({"seite": i + 1, "nr": t["text"].strip(), "name": "", "allergene": al, "zusatz": [], "schwein": 0, "veg": False})
        continue
    # Namen: fett, groß, ohne Preis, nicht die Navigation rechts; Spans einer Zeile zusammenfassen
    roh = sorted((s for s in sp if s["size"] >= 30 and s["font"].startswith("Gopher") and "€" not in s["text"] and s["bbox"][0] < 1400),
                 key=lambda s: (round(s["bbox"][0] / 200), s["bbox"][1], s["bbox"][0]))
    namen = []
    for s in roh:
        x0, y0, x1, y1 = s["bbox"]
        if namen and abs(namen[-1]["y0"] - y0) < 4 and abs(namen[-1]["x1"] - x0) < 30:
            namen[-1]["t"] += s["text"]; namen[-1]["x1"] = x1
        else:
            namen.append({"t": s["text"], "x0": x0, "y0": y0, "x1": x1, "y1": y1})
    imgs = [(r, im[0]) for im in p.get_images(full=True) for r in p.get_image_rects(im[0]) if r.width < 40]
    pigs = [g["rect"] for g in p.get_drawings() if g.get("fill") == (1.0, 1.0, 1.0) and len(g["items"]) == 57]
    for k, n in enumerate(namen):
        spalte = [m for m in namen if abs(m["x0"] - n["x0"]) < 60]
        nach = [m["y0"] for m in spalte if m["y0"] > n["y0"] + 4]
        bis = min(nach) - 2 if nach else 9999
        inb = lambda y: n["y0"] - 2 <= y < bis
        inx = lambda x: n["x0"] - 15 <= x < n["x0"] + 460
        nr = next((s["text"].strip() for s in sp if s["size"] == 25 and s["font"].startswith("Gopher")
                   and n["y0"] - 60 < s["bbox"][1] < n["y0"] and inx(s["bbox"][0])), "")
        zus = sorted({int(z) for s in sp if s["size"] < 12 and n["y0"] - 8 <= s["bbox"][1] <= n["y1"]
                      and n["x1"] - 12 <= s["bbox"][0] <= n["x1"] + 60 for z in re.findall(r"\d", s["text"])})
        al = []
        for r, x in sorted(((r, x) for r, x in imgs if inb(r.y0) and inx(r.x0)), key=lambda t: t[0].x0):
            k2 = allergen(x)
            if k2 not in al: al.append(k2)
        sw = [r for r in pigs if inb(r.y0) and inx(r.x0)]
        x2 = any(s["text"].strip() == "x2" and inb(s["bbox"][1]) and inx(s["bbox"][0]) for s in sp)
        veg = any("completely vegetarian" in s["text"] and inb(s["bbox"][1]) and inx(s["bbox"][0]) for s in sp)
        items.append({"seite": i + 1, "nr": nr, "name": n["t"].strip(), "allergene": al, "zusatz": zus,
                      "schwein": (2 if x2 else 1) if sw else 0, "veg": veg})

json.dump({"legende": {v[0]: v[1] for v in KEY.values()}, "gerichte": items}, open(root / "data/noodle_symbols.json", "w"), ensure_ascii=False, indent=1)
for s in items:
    print(s["seite"], s["nr"] or "-", s["name"][:28], s["allergene"], s["zusatz"] or "", "SCHWEIN" * bool(s["schwein"]) + ("x2" if s["schwein"] == 2 else ""), "VEG" if s["veg"] else "")
print(len(items), "Gerichte · Symbole:", sorted(gesp))

# Schwein-Symbol als Vektor (SVG, Farbe per CSS) aus der ersten Ramen-Seite
for pg in doc:
    g = next((g for g in pg.get_drawings() if g.get("fill") == (1.0, 1.0, 1.0) and len(g["items"]) == 57), None)
    if g:
        r = g["rect"]; f = lambda q: f"{q.x - r.x0:.2f} {q.y - r.y0:.2f}"
        d, last = [], None
        for it in g["items"]:
            if it[0] == "re":
                q = it[1]; d.append(f"M{q.x0 - r.x0:.2f} {q.y0 - r.y0:.2f}h{q.width:.2f}v{q.height:.2f}h{-q.width:.2f}Z"); last = None; continue
            if it[0] == "qu":
                q = it[1]; d.append(f"M{f(q.ul)}L{f(q.ur)}L{f(q.lr)}L{f(q.ll)}Z"); last = None; continue
            if last is None or abs(it[1].x - last.x) > .01 or abs(it[1].y - last.y) > .01:
                d.append(f"M{f(it[1])}")
            d.append(f"L{f(it[2])}" if it[0] == "l" else f"C{f(it[2])} {f(it[3])} {f(it[4])}")
            last = it[-1]
        rule = "evenodd" if g.get("even_odd") else "nonzero"
        (outimg / "schwein.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {r.width:.2f} {r.height:.2f}"><path fill="currentColor" fill-rule="{rule}" d="{"".join(d)}"/></svg>')
        break

# In die Speisekarte der Seite übernehmen (site/assets/menu-data.js)
mp = root / "site/assets/menu-data.js"
md = json.loads(mp.read_text(encoding="utf-8").strip()[len("window.NANIWA_MENU="):-1])
norm = lambda t: re.sub(r"[^A-Z]", "", t.upper().replace("CHASU", "CHASHU"))
treffer, offen = 0, []
for c in md["noodles"]:
    for g in c["g"]:
        for k in ("al", "zs", "sw", "veg"):
            g.pop(k, None)
        kand = [it for it in items if g["nr"] and it["nr"] == g["nr"]]
        if len(kand) > 1 or not g["nr"]:
            kand = [it for it in (kand or items) if norm(it["name"]) == norm(g["n"])] or [it for it in (kand or items) if norm(it["name"]) and norm(it["name"]) in norm(g["n"])][:1]
        if len(kand) != 1:
            offen.append(g["nr"] + " " + g["n"]); continue
        it = kand[0]; treffer += 1
        if it["allergene"]: g["al"] = it["allergene"]
        if it["zusatz"]: g["zs"] = it["zusatz"]
        if it["schwein"]: g["sw"] = it["schwein"]
        if it["veg"]: g["veg"] = 1
md["leg"] = {"al": {k: v for k, v in {v[0]: v[1] for v in KEY.values()}.items() if k in gesp},
             "zs": {"1": "koffeinhaltig, mit Farbstoff", "2": "mit Farbstoff", "3": "mit Süßungsmitteln", "4": "mit Konservierungsstoffen",
                    "5": "mit Antioxidationsmitteln", "6": "roter Ingwer", "7": "mit Geschmacksverstärker"}}
mp.write_text("window.NANIWA_MENU=" + json.dumps(md, ensure_ascii=False) + ";", encoding="utf-8")
print("Speisekarte:", treffer, "Gerichte mit Daten verknüpft · ohne Treffer:", offen)
