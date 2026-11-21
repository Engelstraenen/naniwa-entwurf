#!/usr/bin/env python3
"""Baut die drei Seiten des NANIWA-Entwurfs nach site/. Aufruf: python3 build.py"""
import pathlib

ROOT = pathlib.Path(__file__).parent / "site"

BRUSH = """<svg width="0" height="0" style="position:absolute" aria-hidden="true"><filter id="brush" x="-5%" y="-40%" width="110%" height="180%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.09" numOctaves="3" seed="7"/><feDisplacementMap in="SourceGraphic" scale="46"/></filter></svg>"""


def head(title, desc, r, cls=""):
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#000000">
<link rel="icon" href="{r}assets/img/naniwa-logo.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/style.css">
</head>
<body class="{cls}">
{BRUSH}
<div class="draft">Design-Entwurf · nicht die offizielle Seite</div>
"""


def top(r, nav):
    return f"""<header class="top">
  <a class="logo" href="{r}" aria-label="NANIWA Startseite"><img src="{r}assets/img/naniwa-logo.svg" alt="NANIWA" width="200" height="213"></a>
  <nav class="nav" aria-label="Hauptnavigation">{nav}</nav>
</header>
"""


def vsec(video, cls, inner, r, eager=False):
    return f"""<section class="vsec {cls}">
  <video data-bg muted loop playsinline preload="{'auto' if eager else 'none'}" {'autoplay ' if eager else ''}poster="{r}assets/img/{video}.jpg" src="{r}assets/video/{video}.mp4"></video>
  <div class="txt rv">{inner}</div>
  <button class="pause" type="button" aria-pressed="false" aria-label="Video anhalten"></button>
</section>
"""


def footer(r):
    return f"""<footer>
  <span>© K &amp; M Restaurant GmbH · Düsseldorf</span>
  <nav aria-label="Fußnavigation">
    <a href="{r}noodles/">Noodles &amp; Soups</a><a href="{r}sushi/">Sushi &amp; More</a>
    <a href="https://naniwa.de/impressum">Impressum</a><a href="https://naniwa.de/datenschutzerklaerung">Datenschutz</a>
    <a href="https://sushi.naniwa.de/allergien">Allergien</a>
  </nav>
</footer>
"""


def tail(r, menu=True):
    m = f'<script src="{r}assets/menu-data.js"></script>\n' if menu else ""
    return f"""{m}<script src="{r}assets/app.js"></script>
</body>
</html>
"""


def menu(shop, lead, note):
    return f"""<section class="menu" id="karte" data-menu="{shop}">
  <div class="in">
    <span class="jp" lang="ja">メニュー</span>
    <h2>Speisekarte</h2>
    <p class="lead">{lead}</p>
    <div class="cats" role="tablist" aria-label="Kategorien"></div>
    <div class="dishes"></div>
    <p class="note">{note}</p>
  </div>
</section>
"""


REVIEWS = {
    "noodles": {
        "google": ("4,5", 4.5, "5.288", "https://www.google.com/maps/search/?api=1&query=Naniwa+Noodles+%26+Soups+Oststra%C3%9Fe+55+D%C3%BCsseldorf"),
        "trip": ("4,3", 4.3, "949", "https://www.tripadvisor.de/Restaurant_Review-g187373-d3345259-Reviews-Naniwa_Noodles_Soups-Dusseldorf_North_Rhine_Westphalia.html", "Platz 30 von 1.990 Restaurants in Düsseldorf"),
        "themes": "Am häufigsten erwähnt in den Google-Bewertungen: <b>Nudelsuppen</b> · <b>Brühe</b> · <b>Warteschlange</b>",
    },
    "sushi": {
        "google": ("4,6", 4.6, "530", "https://www.google.com/maps/search/?api=1&query=Naniwa+Sushi+%26+More+Klosterstra%C3%9Fe+68A+D%C3%BCsseldorf"),
        "trip": ("4,0", 4.0, "223", "https://www.tripadvisor.de/Restaurant_Review-g187373-d1976176-Reviews-Naniwa_Sushi_More-Dusseldorf_North_Rhine_Westphalia.html", ""),
        "themes": "",
    },
}


def reviews(shop):
    d = REVIEWS[shop]
    g, t = d["google"], d["trip"]
    rank = f'<span class="rank">{t[4]}</span>' if t[4] else ""
    themes = f'<p class="themes">{d["themes"]}</p>' if d["themes"] else ""
    return f"""<section class="reviews" id="bewertungen">
  <div class="in">
    <span class="jp" lang="ja">お客様の声</span>
    <h2>Das sagen unsere Gäste</h2>
    <div class="rgrid">
      <a class="rcard rv" href="{g[3]}" target="_blank" rel="noopener">
        <span class="plat">Google</span>
        <span class="score">{g[0]}<small> / 5</small></span>
        <span class="stars" style="--r:{g[1]}" role="img" aria-label="{g[0]} von 5 Sternen"></span>
        <span class="cnt">{g[2]} Bewertungen</span>
        <span class="go">Bewertungen lesen →</span>
      </a>
      <a class="rcard rv" href="{t[3]}" target="_blank" rel="noopener">
        <span class="plat">Tripadvisor</span>
        <span class="score">{t[0]}<small> / 5</small></span>
        <span class="stars" style="--r:{t[1]}" role="img" aria-label="{t[0]} von 5 Punkten"></span>
        <span class="cnt">{t[2]} Bewertungen</span>{rank}
        <span class="go">Bewertungen lesen →</span>
      </a>
      <a class="rcard leer rv" href="https://de.trustpilot.com/evaluate/naniwa.de" target="_blank" rel="noopener">
        <span class="plat">Trustpilot</span>
        <span class="score">Noch keine Bewertung</span>
        <span class="cnt">Auf Trustpilot gibt es bisher kein NANIWA-Profil.</span>
        <span class="go">Als Erste:r bewerten →</span>
      </a>
    </div>
    {themes}
    <p class="stand">Stand: 21.11.2026 · Werte von Google Maps, Tripadvisor und Trustpilot</p>
  </div>
</section>
"""


def visit(shop, name, street, tel_show, tel, hint, maps):
    return f"""<section class="visit" id="besuch">
  <div class="in">
    <span class="jp" lang="ja">アクセス</span>
    <h2>Besuch uns</h2>
    <div class="grid">
      <div class="card rv">
        <h3>{name}</h3>
        <address>{street}<br>40211 Düsseldorf</address>
        <p class="hint">{hint}</p>
        <div class="row">
          <a class="pill lime" href="tel:{tel}">{tel_show}</a>
          <a class="pill" href="{maps}" target="_blank" rel="noopener">Route planen</a>
        </div>
      </div>
      <div class="card rv">
        <h3>Öffnungszeiten</h3>
        <table class="hours" data-shop="{shop}"></table>
      </div>
    </div>
  </div>
</section>
<div class="bar"><a href="tel:{tel}">Anrufen</a><a href="{maps}" target="_blank" rel="noopener">Route</a></div>
"""


# ---------- Startseite: Auswahl ----------
index = head("NANIWA Düsseldorf – Ramen & Sushi seit 1986", "Zwei Restaurants im japanischen Viertel von Düsseldorf: NANIWA Noodles & Soups und NANIWA Sushi & More.", "./", "home")
index += top("./", '<a class="switch" href="noodles/">Noodles &amp; Soups</a><a class="switch" href="sushi/">Sushi &amp; More</a>')
index += """<main>
<div class="brandline"><h1>NANIWA</h1><p>Ramen &amp; Sushi im japanischen Viertel, seit 1986</p></div>
<section class="choose" aria-label="Restaurant wählen">
  <a class="side" href="noodles/">
    <video data-bg muted loop playsinline autoplay preload="auto" poster="assets/img/n-anrichten.jpg" src="assets/video/n-anrichten.mp4"></video>
    <span class="jp" lang="ja">ラーメン</span>
    <h2>Noodles<br>&amp; Soups</h2>
    <p>Frische, handgemachte Nudelsuppen in einem der ältesten japanischen Noodle-Restaurants in Düsseldorf.</p>
    <div class="row"><span class="pill lime">Zu den Nudeln</span><span class="status" data-status="noodles"></span></div>
  </a>
  <a class="side" href="sushi/">
    <video data-bg muted loop playsinline autoplay preload="auto" poster="assets/img/s-teller.jpg" src="assets/video/s-teller.mp4"></video>
    <span class="jp" lang="ja">寿司</span>
    <h2>Sushi<br>&amp; More</h2>
    <p>Feinste traditionelle Sushi-Qualität und bester Service im Herzen von Düsseldorf.</p>
    <div class="row"><span class="pill lime">Zum Sushi</span><span class="status" data-status="sushi"></span></div>
  </a>
</section>
</main>
"""
index += footer("./") + tail("./", menu=False)

# ---------- Noodles & Soups ----------
nav_n = '<a href="#karte">Speisekarte</a><a href="#bewertungen">Bewertungen</a><a href="#besuch">Besuch</a><a href="#faq">FAQ</a><a class="switch" href="../sushi/">Zu Sushi &amp; More</a>'
noodles = head("NANIWA Noodles & Soups – Ramen in Düsseldorf", "Hausgemachte Ramen seit 1986. Oststraße 55, Düsseldorf. Keine Reservierungen.", "../")
noodles += top("../", nav_n) + "<main>\n"
noodles += vsec("n-anrichten", "", """<span class="status" data-status="noodles"></span>
    <h1>NANIWA</h1>
    <p class="sub">Noodles &amp; Soups. Ramen im japanischen Viertel, seit 1986.</p>
    <div class="row"><a class="pill" href="#karte">Speisekarte</a><a class="pill" href="#besuch">Besuch uns</a></div>""", "../", eager=True)
noodles += vsec("n-vorspeisen", "", """<span class="jp" lang="ja">前菜</span>
    <h2>Vorspeisen,<br>frisch angerichtet.</h2>
    <p class="body">Gyoza direkt aus der Pfanne, Kimchi, Edamame und mehr: Unsere Vorspeisen kommen frisch auf den Teller, perfekt zum Teilen vor der Nudelsuppe.</p>""", "../")
noodles += vsec("n-kueche", "", """<span class="jp" lang="ja">自家製麺</span>
    <h2>Hausgemachte Nudeln.<br>Jeden Tag.</h2>
    <p class="body">Unsere Ramennudeln machen wir täglich selbst, nach eigener Rezeptur mit japanischem Mehl. Je nach Suppe servieren wir dünne, gerade Straight-Nudeln oder die dickeren, welligen Miso-Ramen.</p>""", "../")
noodles += vsec("n-schale-v2", "", """<span class="jp" lang="ja">スープ</span>
    <h2>Täglich frische Brühe.</h2>
    <p class="body">Die NANIWA-Brühe ist die Basis aller unserer Nudelsuppen. Seit über dreißig Jahren setzen wir sie jeden Morgen frisch auf, aus regionalen und ausschließlich natürlichen Zutaten: klassisch aus Schweineknochen oder als reine Gemüsebrühe.</p>""", "../")
noodles += vsec("n-schlange-v3", "brush-bottom", """<span class="jp" lang="ja">ようこそ</span>
    <h2>Keine Reservierung.<br>Die Schlange lohnt sich.</h2>
    <p class="body">Nicht selten bildet sich vor unserer Tür eine Warteschlange. Trotz kleiner Wartezeit finden wir bestimmt einen Platz für euch.</p>""", "../")
noodles += """<section class="quote">
  <blockquote class="rv">„Die Suppen, die vermutlich nirgendwo auf der Welt besser schmecken, werden in traditionellem Porzellan serviert. Die Suche nach der perfekten Nudel findet hier täglich statt.“<cite>Düsseldorf geht aus 2012/2013</cite></blockquote>
</section>
"""
noodles += menu("noodles", "Unsere Karte mit allen Ramen, Reisgerichten und Yakisoba.", "L = groß, S = klein. Extras (Ei, Mais, Wantan, mehr Gemüse) und Getränke gibt es vor Ort.")
noodles += reviews("noodles")
noodles += visit("noodles", "NANIWA Noodles &amp; Soups", "Oststraße 55", "+49 211 16 17 99", "+49211161799", "Keine Reservierungen. Die Schlange lohnt sich! Take-away telefonisch oder vor Ort.", "https://www.google.com/maps/dir/?api=1&destination=Naniwa+Noodles+%26+Soups+Oststra%C3%9Fe+55+40211+D%C3%BCsseldorf")
noodles += """<section class="faq" id="faq">
  <div class="in">
    <h2>Häufige Fragen</h2>
    <details><summary>Kann ich mit EC- oder Kreditkarte bezahlen?</summary><p>Wir akzeptieren EC, Kreditkarten und Apple Pay. American Express können wir leider nicht annehmen.</p></details>
    <details><summary>Kann man bei euch reservieren?</summary><p>Leider nehmen wir keine Reservierungen an. Trotz kleiner Wartezeiten vor unserem Lokal finden wir bestimmt einen Platz für euch.</p></details>
    <details><summary>Bietet ihr Take-away an?</summary><p>Ja. Bestellt telefonisch unter 0211 16 17 99 oder direkt vor Ort zum Mitnehmen.</p></details>
    <details><summary>Wie wird eine Take-away-Nudelsuppe verpackt?</summary><p>Nudeln und Suppe verpacken wir getrennt voneinander. So haben die Nudeln beim Essen die perfekte Konsistenz.</p></details>
    <details><summary>Woraus ist die Brühe für eure Nudelsuppen?</summary><p>Unsere Ramen-Suppe besteht hauptsächlich aus Schwein und verschiedenem Gemüse.</p></details>
    <details><summary>Gibt es eine vegetarische Nudelsuppe?</summary><p>Ja, wir haben auch eine Nudelsuppe mit Gemüsebrühe.</p></details>
    <details><summary>Gibt es Kinderstühle?</summary><p>Wir haben einige Kinderstühle. Sprecht uns bitte vor Ort an.</p></details>
    <details><summary>Kann man Gutscheine kaufen?</summary><p>Nein, leider bieten wir keine Gutscheine an.</p></details>
  </div>
</section>
</main>
"""
noodles += footer("../") + tail("../")

# ---------- Sushi & More ----------
nav_s = '<a href="#karte">Speisekarte</a><a href="#bewertungen">Bewertungen</a><a href="#besuch">Reservieren</a><a class="switch" href="../noodles/">Zu Noodles &amp; Soups</a>'
sushi = head("NANIWA Sushi & More – Sushi in Düsseldorf", "Sushi & More seit 2004. Klosterstraße 68A, Düsseldorf. Reservierung unter 0211 83 0 22 22.", "../")
sushi += top("../", nav_s) + "<main>\n"
sushi += vsec("s-haende", "", """<span class="status" data-status="sushi"></span>
    <h1>NANIWA</h1>
    <p class="sub">Sushi &amp; More. Direkt gegenüber, seit 2004.</p>
    <div class="row"><a class="pill lime" href="tel:+4921183022222">Tisch reservieren</a><a class="pill" href="#karte">Speisekarte</a></div>""", "../", eager=True)
sushi += vsec("s-teller", "", """<span class="jp" lang="ja">寿司</span>
    <h2>Immer frisch.<br>Über 70 Kreationen.</h2>
    <p class="body">Unser Sushi bereiten wir immer frisch und mit den besten Zutaten zu. Über 70 Menü-Kreationen zeigen, wie reich und vielfältig die kulinarische Begegnung sein kann.</p>""", "../")
sushi += vsec("s-nigiri", "brush-bottom", """<span class="jp" lang="ja">いただきます</span>
    <h2>Nouvelle Cuisine Japonaise.</h2>
    <p class="body">Als wir 2004 eröffneten, war das ein kleines Wagnis: klassische japanische Küche, erweitert um europäische Einflüsse. Heute ist die kleine Schwester von Noodles &amp; Soups ein ruhiger, entspannter Ort auf der Klosterstraße. Itadakimasu!</p>""", "../")
sushi += menu("sushi", "Vorspeisen, Nigiri, Maki, Udon, Soba und Don.", "Hinweise zu Allergenen findest du unter „Allergien“ im Fuß der Seite.")
sushi += reviews("sushi")
sushi += visit("sushi", "NANIWA Sushi &amp; More", "Klosterstraße 68A", "+49 211 83 0 22 22", "+4921183022222", "Reservierung telefonisch", "https://www.google.com/maps/dir/?api=1&destination=Naniwa+Sushi+%26+More+Klosterstra%C3%9Fe+68A+40211+D%C3%BCsseldorf")
sushi += "</main>\n" + footer("../") + tail("../")

(ROOT / "index.html").write_text(index, encoding="utf-8")
(ROOT / "noodles" / "index.html").write_text(noodles, encoding="utf-8")
(ROOT / "sushi" / "index.html").write_text(sushi, encoding="utf-8")
print("ok")
