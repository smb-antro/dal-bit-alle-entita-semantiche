#!/usr/bin/env python3
"""check_contrast.py — verifica il contrasto WCAG 2 delle coppie testo/sfondo
realmente usate nel design system.

    python3 scripts/check_contrast.py

Legge i colori direttamente da tokens/tokens.css (non da tokens.json: questo
script non dipende da export_tokens.py, gira anche se il JSON non esiste
ancora). Le coppie verificate sono quelle elencate in COPPIE qui sotto, ognuna
con il file e il selettore CSS reale dove è usata — non un elenco a memoria,
ma cercato in design-system/css/ prima di scrivere questo script (vedi il
commento su ciascuna).

Formula (WCAG 2, la stessa per tutte le versioni 2.x — non cambia nella 2.2):
luminanza relativa sui canali sRGB linearizzati, coefficienti
0.2126/0.7152/0.0722; rapporto di contrasto (L1+0.05)/(L2+0.05) con L1 il più
chiaro dei due. Soglia 4.5:1 per testo normale, 3:1 per testo grande (>=24px,
o >=18.66px in grassetto) — ma SOLO dove una coppia è usata esclusivamente per
testo grande: altrimenti vale comunque 4.5:1, perché la stessa coppia serve
anche a testo normale altrove. Nessuna soglia abbassata per far passare un
colore: se qualcosa non passa, questo script lo segnala e basta.
"""

import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
TOKENS_CSS = RADICE / "tokens" / "tokens.css"


def leggi_primitivi_colore():
    """Estrae { nome-senza-doppio-trattino: (r,g,b) 0-255 } dal blocco :root
    di tokens.css, per i soli valori colore (esadecimali o rgba)."""
    testo = TOKENS_CSS.read_text(encoding="utf-8")
    inizio = testo.index(":root")
    apertura = testo.index("{", inizio) + 1
    chiusura = testo.rindex("}")
    corpo = re.sub(r"/\*.*?\*/", "", testo[apertura:chiusura], flags=re.S)

    colori = {}
    for m in re.finditer(r"--([A-Za-z0-9-]+)\s*:\s*([^;]+?)\s*;", corpo):
        nome, valore = m.group(1), m.group(2).strip()
        hm = re.fullmatch(r"#([0-9A-Fa-f]{6})", valore)
        if hm:
            h = hm.group(1)
            colori[nome] = (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            continue
        rm = re.fullmatch(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*[\d.]+\s*\)", valore)
        if rm:
            colori[nome] = (int(rm.group(1)), int(rm.group(2)), int(rm.group(3)))
    return colori


def luminanza_relativa(rgb):
    """WCAG 2: canali sRGB [0,255] -> luminanza relativa [0,1]."""
    def lineare(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lineare(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def rapporto_contrasto(rgb1, rgb2):
    l1, l2 = luminanza_relativa(rgb1), luminanza_relativa(rgb2)
    piu_chiaro, piu_scuro = max(l1, l2), min(l1, l2)
    return (piu_chiaro + 0.05) / (piu_scuro + 0.05)


# ─────────────────────────────────────────────────────────────────────
# Le coppie realmente usate, ognuna con la soglia che le si applica e il
# perché. Per ogni coppia ho cercato in design-system/css/ (compresi i
# component-css) ogni regola che usa quel colore di testo su quello sfondo
# semantico, e ho preso la dimensione più grande fra tutti gli usi trovati:
# se anche uno solo scende sotto i 24px (o i 18.66px in grassetto), la
# soglia per l'intera coppia resta 4.5:1 — non si spacca una coppia in
# "questo uso passa a 3:1" quando la userebbe anche altrove come testo
# normale. Con la radice a 120% (base.css, html{font-size:120%}), 1rem
# vale qui 19.2px: le taglie sotto sono già convertite.
#
#   testo            sfondo    soglia  dove (file:selettore, taglia massima trovata)
# ─────────────────────────────────────────────────────────────────────
COPPIE = [
    ("inchiostro", "brina", 4.5,
     "base.css: body{color:var(--colore-testo)} su body{background:var(--colore-fondo)} — "
     "dim-testo 1.05rem/20.16px, peso normale."),
    ("inchiostro", "bianco", 4.5,
     "components/richiami.css: blockquote{color:var(--colore-testo)} dentro .aside/.tenda su "
     "colore-superficie — dim-citazione 1.1rem/21.12px, peso normale."),
    ("grigio-testo", "brina", 4.5,
     "base.css: p.dim{color:var(--colore-testo-attenuato)} su sfondo pagina — "
     "dim-testo 1.05rem/20.16px, peso normale."),
    ("grigio-testo", "bianco", 4.5,
     "components/richiami.css: .aside p{color:var(--colore-testo-attenuato)} su "
     "colore-superficie — dim-nota 0.96rem/18.43px, peso normale."),
    ("grigio-soft", "brina", 4.5,
     "components/apparato.css: .eyebrow/.footer-note/.scrolldown{color:var(--colore-testo-tenue)} "
     "su sfondo pagina — dim-apparato 0.78rem/14.98px, small-caps, peso normale."),
    ("grigio-soft", "bianco", 4.5,
     "components/sidebar.css: .sidebar-kicker{color:var(--colore-testo-tenue)} su "
     "colore-superficie — dim-nav-parte 0.74rem/14.21px, small-caps, peso normale."),
    ("blu", "bianco", 4.5,
     "components/sidebar.css: .sidebar-title/.parte-heading/.voce-semplice.current{"
     "color:var(--colore-navigazione)} su colore-superficie — il più grande è "
     "dim-nav-titolo 1.02rem/19.58px, peso 500 (non 700: non conta come grassetto ai fini "
     "della soglia grande)."),
    ("arancio-scuro", "brina", 4.5,
     "base.css: a{color:var(--colore-apparato)} su sfondo pagina — eredita la taglia del "
     "testo che lo contiene, mai sopra dim-lede 1.2rem/23.04px, peso normale."),
    ("arancio-scuro", "bianco", 4.5,
     "components/richiami.css: .question{color:var(--colore-apparato)} dentro superfici — "
     "dim-richiamo 1.0rem/19.2px, peso normale."),
    ("verde", "bianco", 4.5,
     "components/tenda-concetti.css: .termine-concetto{color:var(--colore-ontologia)} "
     "(font:inherit, mai isolato a testo grande) — contrasto noto e già verificato "
     "≈5,2:1, docs/decision-log.md 8 settembre 2026."),
    ("verde-scuro", "bianco", 4.5,
     "components/tenda-concetti.css: .tenda-chiudi:hover{color:var(--colore-ontologia-forte)} "
     "su colore-superficie — font-size 1.1rem/21.12px, peso normale."),
    ("bianco", "verde", 4.5,
     "components/tenda-concetti.css: .tenda-lente{color:var(--colore-superficie); "
     "background:var(--colore-ontologia)} — 0.98rem/18.82px, small-caps, peso normale."),
]


def formatta(rapporto):
    return f"{rapporto:.2f}:1"


def main():
    colori = leggi_primitivi_colore()

    mancanti = sorted({nome for testo, sfondo, _s, _d in COPPIE for nome in (testo, sfondo)} - set(colori))
    if mancanti:
        print("Primitivi non trovati in tokens.css:", ", ".join(mancanti), file=sys.stderr)
        sys.exit(2)

    righe = []
    tutte_passano = True
    for nome_testo, nome_sfondo, soglia, dove in COPPIE:
        rgb_testo = colori[nome_testo]
        rgb_sfondo = colori[nome_sfondo]
        rapporto = rapporto_contrasto(rgb_testo, rgb_sfondo)
        passa = rapporto >= soglia
        tutte_passano &= passa
        righe.append((nome_testo, nome_sfondo, rapporto, soglia, passa, dove))

    largh_testo = max(len(f"--{t}") for t, _, _, _, _, _ in righe)
    largh_sfondo = max(len(f"--{s}") for _, s, _, _, _, _ in righe)

    intestazione = (
        f"{'testo':<{largh_testo}}  {'sfondo':<{largh_sfondo}}  {'contrasto':>9}  "
        f"{'soglia':>7}  esito"
    )
    print(intestazione)
    print("-" * len(intestazione))
    for nome_testo, nome_sfondo, rapporto, soglia, passa, dove in righe:
        esito = "PASSA" if passa else "NON PASSA"
        print(
            f"{'--' + nome_testo:<{largh_testo}}  {'--' + nome_sfondo:<{largh_sfondo}}  "
            f"{formatta(rapporto):>9}  {soglia:>5.1f}:1  {esito}"
        )
        if not passa:
            print(f"    -> {dove}")

    print()
    if tutte_passano:
        print(f"Tutte le {len(righe)} coppie passano la propria soglia.")
    else:
        falliti = [r for r in righe if not r[4]]
        print(f"{len(falliti)} coppia/e sotto soglia su {len(righe)}:", file=sys.stderr)
        for nome_testo, nome_sfondo, rapporto, soglia, _passa, dove in falliti:
            print(
                f"  - --{nome_testo} su --{nome_sfondo}: {formatta(rapporto)} "
                f"(richiesto {soglia:.1f}:1) — {dove}",
                file=sys.stderr,
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
