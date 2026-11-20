# PROJEKT-MASTERFILE – NANIWA
Gilt zusätzlich zur globalen Masterfile (~/.claude/CLAUDE.md).

## 1. Ziel und Endprodukt
Neue Webseite für NANIWA Düsseldorf (Freund von Eugen, kein Kunde) als Design-Entwurf. Eine Webpage, zwei Läden: Start = Auswahl „Noodles & Soups“ / „Sushi & More“, dahinter je ein eigener Bereich.

## 2. Qualitätsanspruch & Referenzen
- CI von naniwa.de beibehalten, nur frischer: Schwarz, Weiß, Limettengrün #A0C41E, Creme #F7E8DF, Pinsel-Kanten. Logo = `site/assets/img/naniwa-logo.svg` (nie neu setzen). Originalschriften Gopher/Gilroy sind kommerziell, Ersatz: Outfit.
- Bestätigte Storyboards: `storyboards/sb3_hintergrundvideos.jpg` (wird zuerst gebaut), `sb2_scrollytelling.jpg` (danach). Storyboard 1 abgelehnt.

## 3. Regeln für dieses Projekt
- Immer als „Design-Entwurf · nicht die offizielle Seite“ markiert, `noindex`.
- Clips werden neu gerendert: erst kostenlose Entwürfe, 2K-Endrender nur nach Preis + OK.
- Fassade/Schlange vor dem Lokal: kein echtes Material vorhanden; KI-Bild ohne Schriftzug, Eugen muss es abnehmen.

## 5. Zugänge
gh (Engelstraenen) ✅ · sjinn.ai in Chrome ✅ · WordPress naniwa.de ❌ (nur nötig für Live-Gang)

## 7. Befehle
- Bauen: `python3 build.py` · Ansehen: `cd site && python3 -m http.server 4391`
- Pages: `git subtree split --prefix site -b gh-pages && git push -f origin gh-pages`
- Live: https://engelstraenen.github.io/naniwa-entwurf/ · Repo: https://github.com/Engelstraenen/naniwa-entwurf

## 8. Offene Fragen
- Projekt liegt noch im Sitzungsordner der App, nicht in Dropbox/CLAUDE/Projekte/NANIWA.
- Nudel-Karte: Extras/Getränke fehlen noch (nur im PDF).

## 9. Entschieden
- 18.11.2026: Naniwa = Freund, Demo öffentlich als Entwurf ok. Echte Clips neu rendern, alles frischer, aber in der CI.
- 19.11.2026: Storyboard 3 gewählt, 2 gefällt auch, 1 nicht. Noodles und Sushi müssen getrennt sein (Auswahl auf der Startseite).
