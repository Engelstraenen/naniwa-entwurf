# PROJEKT-MASTERFILE – NANIWA
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Neue Webseite für NANIWA Düsseldorf (Freund von Eugen, kein Kunde) als Design-Entwurf. Eine Webpage, zwei Läden: Start = Auswahl „Noodles & Soups“ / „Sushi & More“, dahinter je ein eigener Bereich.

## 2. Qualitätsanspruch & Referenzen
- CI von naniwa.de beibehalten, nur frischer: Schwarz, Weiß, Limettengrün #A0C41E, Creme #F7E8DF, Pinsel-Kanten. Logo = `site/assets/img/naniwa-logo.svg` (nie neu setzen). Originalschriften Gopher/Gilroy sind kommerziell, Ersatz: Outfit.
- Look wie die Originalseite: clean und herzlich, helle Inhaltsbereiche (Weiß/Schwarz/Limette, grüne Trennlinien), Videos dunkel. Speisekarte = große Fotokarten wie sushi.naniwa.de/speisekarte, ganze Teller sichtbar.
- Bewertungen je Laden: Google + Tripadvisor, bewegt (Hochzählen, Sterne, Laufbänder), Werte in build.py REVIEWS, Stand 21.11.2026. Trustpilot entfernt (kein Profil, Eugen 21.11.).
- Bestätigte Storyboards: `storyboards/sb3_hintergrundvideos.jpg` (wird zuerst gebaut), `sb2_scrollytelling.jpg` (danach). Storyboard 1 abgelehnt.

## 3. Regeln für dieses Projekt
- Immer als „Design-Entwurf · nicht die offizielle Seite“ markiert, `noindex`.
- Clips werden neu gerendert: erst kostenlose Entwürfe, 2K-Endrender nur nach Preis + OK.
- Ab 24.11.2026: Video-Entwürfe auf Dreamina (Seedance 2.5, 720P, Unlimited an), Bilder bis 2K auf Dreamina (GPT Image 2.5 Sunburst), 4K-Standbilder auf sjinn (Nano Banana 2.1). Nur generieren, wo Unlimited an und Preis 0.
- Preise live 24.11.2026: Dreamina Seedance 2.5 8 s · 720P = Unlimited 0 (sonst 256), 1080P = 624 Dreamina-Credits (Guthaben 53,2K). sjinn MiniMax H3 2K = 150 sjinn-Credits/s (15 s = 2.250, echtes Detail nur ca. 1280–1920 px). Für mehr Auflösung zuerst Dreamina 1080P (nativ, günstiger), nicht MiniMax 2K.
- Fassade/Schlange vor dem Lokal: kein echtes Material vorhanden; KI-Bild ohne Schriftzug, Eugen muss es abnehmen.

## 5. Zugänge
gh (Engelstraenen) ✅ · sjinn.ai in Chrome ✅ · WordPress naniwa.de ❌ (nur nötig für Live-Gang)

## 7. Befehle
- Projektordner: `Dropbox/CLAUDE/Projekte/NANIWA` (seit 24.11.2026, vorher Sitzungsordner der App).
- Bauen: `python3 build.py` · Ansehen: `cd site && python3 -m http.server 4391` (vor dem Link `<title>` per curl prüfen, Port kann fremd belegt sein)
- Prüfen: `python3 tools/mobil_check.py` (Handy 390/360/430/quer), `python3 tools/schaerfe.py <video> <startbild>` (echte Detail-Auflösung)
- Pages: `git subtree split --prefix site -b gh-pages && git push -f origin gh-pages`
- Live: https://engelstraenen.github.io/naniwa-entwurf/ · Repo: https://github.com/Engelstraenen/naniwa-entwurf

## 8. Offene Fragen
- Nudel-Karte: Extras + Getränke ergänzt (22.11., aus PDF S. 38, 59–61). „Dunkler Weizen-Tee“ steht in der PDF mit „2.3.00“, als 3,00 € übernommen.

## 9. Entschieden
- 18.11.2026: Naniwa = Freund, Demo öffentlich als Entwurf ok. Echte Clips neu rendern, alles frischer, aber in der CI.
- 19.11.2026: Storyboard 3 gewählt, 2 gefällt auch, 1 nicht. Noodles und Sushi müssen getrennt sein (Auswahl auf der Startseite).
- 19.11.2026: Jedes Gericht braucht ein Foto; fehlende per KI, immer mit dem echten Naniwa-Teller der Kategorie als Vorlage.
- 20.11.2026: Video-Entwürfe nur kostenlos (Unlimited), auch wenn es dauert.
- 20.11.2026: V1b Küche (Nudeln aus dem Sieb, garnieren) abgenommen.
- 21.11.2026: Hauptvideo bei Ramen = echtes Naniwa-Anrichtvideo (originale/noodle.mp4), auch auf der Startseite. Danach KI-Clips im Look der Originalvideos: Vorspeisen anrichten (V6), Tantan Men (V7), Tokusei Miso (V8).
- 21.11.2026: Speisekarte groß und hell im Original-Stil, Fotos nie beschneiden; Nudelfotos komplett aus https://noodle.naniwa.de/speisekarteeng.pdf (tools/nudel_fotos.py).
- 21.11.2026: Bewertungen (Google/Tripadvisor/Trustpilot) gehören auf jede Webseite. Kein Video doppelt auf einer Seite.
- 21.11.2026: V6 Vorspeisen (Gyoza aus der Pfanne, Sesam auf Kimchi/Edamame, Wan-Entwurf 15 s) abgenommen. Endrender nur MiniMax H3 2K, ohne Referenzvideo, mit 4K-Startbild startbilder/f6_vorspeisen.jpg, Preis vorher nennen.
- 21.11.2026: Außenansicht muss der echten Fassade entsprechen (Oststraße-Ecke, weiße Markisen, schwarze NANIWA-Schilder, graues Haus mit Bullauge und großem Ring). Eugens Foto ist geschützt: nur Vorlage (originale/aussen_noodles.jpg, nicht in Git), daraus startbilder/f3c_aussen.jpg mit anderen Leuten/Autos (abgenommen 21.11.); Video V3c daraus. Altes V3 (erfundene Fassade) verworfen.
- 21.11.2026: Nutzer-Bewertungen: bis zur Google-Schnittstelle markierte Beispieltexte (SAMPLES in build.py), ruhig überblendet. Trustpilot entfernt.
- 21.11.2026: V5 Sushi-Teller verworfen (KI-Look), V5b aus echtem Endbild von originale/sushi.mp4.
- 22.11.2026: Tantan nur mit EINEM Pak Choi (V7b). Noodles-Reihenfolge: Original-Anrichtvideo, Vorspeisen, Tantan, Tokusei Miso, Schlange. Sushi: komplettes Original-Video, Nigiri, Sushi-Teller V5b.
- 22.11.2026: V8b Tokusei Miso (MiniMax-Entwurf 15 s) abgenommen. Endrender nur MiniMax H3 2K, ohne Referenzvideo, mit 4K-Startbild startbilder/f8_tokusei_miso.jpg, Preis vorher nennen.
- 24.11.2026: Tantan bleibt erstmal 720P kostenlos (Dreamina V7c), danach nachschärfen; 1080P auf Dreamina (624 Credits) schaut Eugen später an.
