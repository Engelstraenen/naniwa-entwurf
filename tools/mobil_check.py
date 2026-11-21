#!/usr/bin/env python3
"""Handy-Prüfung (Masterfile V2.25): Querscroll, Schrift < 14 px, Tipp-Flächen < 44 px, Konsolenfehler.
Aufruf: python3 tools/mobil_check.py   (Server: cd site && python3 -m http.server 4391)"""
import json, pathlib, re, subprocess
SITE = pathlib.Path(__file__).resolve().parent.parent / "site"
CH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HEAD = '<script>window.__err=[];window.addEventListener("error",function(e){__err.push(String(e.message||(e.target&&e.target.src)))},true);var _ce=console.error;console.error=function(){__err.push([].join.call(arguments," "));_ce.apply(console,arguments)}</script>'
JS = r'''<script>setTimeout(function(){document.querySelectorAll(".rv").forEach(function(e){e.classList.add("vis")});
var W=document.documentElement.clientWidth,o={w:W,sw:document.documentElement.scrollWidth,small:{},tap:{},over:[],err:window.__err};
document.querySelectorAll("body *").forEach(function(el){var cs=getComputedStyle(el);if(cs.display=="none"||cs.visibility=="hidden"||el.closest(".zoom,#dbg"))return;
var r=el.getBoundingClientRect();if(!r.width||!r.height)return;
var t=[].some.call(el.childNodes,function(n){return n.nodeType==3&&n.textContent.trim()});
var k=el.tagName.toLowerCase()+(typeof el.className=="string"&&el.className?"."+el.className.split(" ")[0]:"");
if(t&&parseFloat(cs.fontSize)<14)o.small[k]=cs.fontSize;
if(/^(A|BUTTON|SUMMARY)$/.test(el.tagName)&&(r.height<44&&r.width<44||r.height<32))o.tap[k]=Math.round(r.width)+"x"+Math.round(r.height);
var clip=false;for(var a=el.parentElement;a;a=a.parentElement){var ov=getComputedStyle(a).overflowX;if(ov=="hidden"||ov=="clip"){clip=true;break}}if(!clip&&r.right>W+1&&cs.position!="fixed"&&o.over.length<6)o.over.push(k+":"+Math.round(r.right))});
var d=(window.parent&&window.parent!==window)?window.parent.document:document;var p=d.createElement("pre");p.id="dbg";p.textContent=JSON.stringify(o);d.body.appendChild(p)},2500)</script>'''
SIZES = ["390,844", "360,740", "430,932", "844,390"]
bad = 0
for page in ["index.html", "noodles/index.html", "sushi/index.html", "story/index.html"]:
    src = (SITE / page).read_text(encoding="utf-8")
    test = SITE / pathlib.Path(page).parent / "_chk.html"
    test.write_text(src.replace("<head>", "<head>" + HEAD, 1).replace("</body>", JS + "</body>", 1), encoding="utf-8")
    for sz in SIZES:
        # Headless-Chrome kann keine Fenster unter ~500 px: deshalb iframe in exakter Handygröße
        w, h = map(int, sz.split(","))
        wrap = test.parent / "_wrap.html"
        wrap.write_text(f'<!doctype html><body style="margin:0"><iframe src="_chk.html" style="border:0;width:{w}px;height:{h}px"></iframe></body>', encoding="utf-8")
        out = subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--mute-audio", f"--window-size={max(w,520)+40},{h+40}",
                              "--virtual-time-budget=6000", "--dump-dom", f"http://localhost:4391/{wrap.relative_to(SITE)}"],
                             capture_output=True, text=True, timeout=90).stdout
        wrap.unlink()
        m = re.search(r'<pre id="dbg">([^<]*)', out)
        o = json.loads(m.group(1).replace("&quot;", '"').replace("&amp;", "&")) if m else {"fehler": "keine Ausgabe"}
        prob = {k: v for k, v in o.items() if k in ("small", "tap", "over", "err") and v}
        if o.get("sw", 0) > o.get("w", 0): prob["querscroll"] = f'{o["sw"]}>{o["w"]}'
        if "fehler" in o: prob = o
        bad += bool(prob)
        print(page, sz, "OK" if not prob else json.dumps(prob, ensure_ascii=False))
    test.unlink()
print("FERTIG", "ohne Befund" if not bad else f"{bad} Befunde")
