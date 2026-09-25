#!/usr/bin/env python3
"""Genera la scheda «Caratteri»: lo specimen delle tre facce del design system.

    python3 design-system/scripts/specimen_caratteri.py
    python3 design-system/scripts/specimen_caratteri.py --check

PERCHE' E' GENERATA E NON SCRITTA A MANO. La colonna di copertura dice quali
codepoint ciascun file DICHIARA nella propria `cmap`, letta con fontTools. Non
si puo' scrivere a mano, e soprattutto non si puo' dedurre guardando la pagina:
un glifo assente non lascia un quadratino, ripiega in silenzio su un font di
sistema e sembra giusto. In questo repository quell'errore e' costato due
affermazioni false, corrette il 23 settembre 2026 (vedi docs/decision-log.md).
Rendere e dichiarare sono due cose diverse: la pagina mostra la prima, la
tabella riporta la seconda.

`--check` rigenera in memoria e confronta con il file su disco: fallisce se i
font sono cambiati senza che la scheda sia stata rigenerata.

fontTools viene importato dentro la funzione, come in subset_font.py: nel
python di sistema c'e' gia' (4.60.2) e non serve alcun ambiente virtuale.
"""
import argparse
import re
import sys
from pathlib import Path

DS = Path(__file__).resolve().parent.parent
FONTS = DS / "fonts"
USCITA = DS / "components" / "caratteri" / "index.html"

# Le tre facce dichiarate in fonts.css, nell'ordine in cui vi compaiono.
FACCE = [
    ("EB Garamond", "tondo", "EBGaramond-Variable.woff2"),
    ("EB Garamond", "corsivo", "EBGaramond-Italic-Variable.woff2"),
    ("Noto Sans Mono", "tondo", "NotoSansMono-Tecnico.woff2"),
]

# I glifi su cui vale la pena dichiarare la copertura: quelli tecnici (la
# ragione per cui il monospaziato esiste), gli apici (usati da un widget), e
# ␣, che non ha nessuna delle tre facce ed e' qui come caso noto di ripiego.
GRUPPI_COPERTURA = [
    ("simboli logici", "∧∨¬⊕"),
    ("altri segni tecnici", "↔≈∼→↓−›"),
    ("apici", "ⁿ⁰¹²⁸⁹"),
    ("assente ovunque, documentato", "␣"),
]

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
MINUSCOLE = "abcdefghijklmnopqrstuvwxyz"
CIFRE = "0123456789"
ACCENTI = "àèéìòùÀÈÉÌÒÙ"
PUNTEGGIATURA = "«»’“”–—…·"

CSS = """
  body{ padding: 32px; max-width: 980px; }
  h2{ font-size: var(--dim-lede); font-variant: small-caps;
      letter-spacing: var(--traccia-apparato); color: var(--colore-apparato);
      margin: 34px 0 14px; }
  .nota{ font-size: .96rem; color: var(--colore-testo-attenuato); max-width: 62ch; }
  .campione{ font-size: 2.1rem; line-height: 1.45; word-spacing: .12em; margin: 6px 0 2px; }
  .campione.corsivo{ font-style: italic; }
  .campione.mono{ font-family: var(--font-mono); font-size: 1.8rem; }
  .etichetta{ font-size: .72rem; color: var(--colore-testo-tenue);
              font-variant: small-caps; letter-spacing: var(--traccia-apparato); }
  table{ border-collapse: collapse; margin-top: 10px; font-size: .9rem; }
  th, td{ text-align: left; padding: 7px 14px 7px 0; border-bottom: 1px solid var(--colore-bordo); }
  th{ font-size: .72rem; font-variant: small-caps; letter-spacing: var(--traccia-apparato);
      color: var(--colore-testo-tenue); font-weight: 400; }
  td.glifo{ font-size: 1.5rem; }
  td.glifo.mono{ font-family: var(--font-mono); }
  td.cp, td.num{ font-family: var(--font-mono); font-size: .8rem;
                 color: var(--colore-testo-attenuato); }
  .si{ color: var(--colore-ontologia); }
  .no{ color: var(--colore-apparato); font-weight: 500; }
  .peso{ margin: 4px 0; font-size: 1.4rem; }
"""


def dati_faccia(percorso: Path):
    from fontTools.ttLib import TTFont

    tf = TTFont(percorso)
    cmap = set(tf.getBestCmap())
    assi = [(a.axisTag, a.minValue, a.maxValue) for a in tf["fvar"].axes] if "fvar" in tf else []
    nome = tf["name"].getDebugName(4) or percorso.stem
    return {"nome": nome, "cmap": cmap, "assi": assi, "byte": percorso.stat().st_size}


def pesi_dichiarati(css: str, famiglia: str, stile: str):
    """Intervallo `font-weight` dichiarato in fonts.css per quella faccia."""
    for blocco in re.findall(r"@font-face\s*\{(.*?)\}", css, re.S):
        fam = re.search(r"font-family:\s*'([^']+)'", blocco)
        sty = re.search(r"font-style:\s*(\w+)", blocco)
        wgt = re.search(r"font-weight:\s*([^;]+);", blocco)
        atteso = "italic" if stile == "corsivo" else "normal"
        if fam and fam.group(1) == famiglia and sty and sty.group(1) == atteso:
            return wgt.group(1).strip() if wgt else "non dichiarato"
    return "non trovata in fonts.css"


def pesi_usati():
    """I `font-weight` numerici che il design system chiede davvero."""
    valori = set()
    for f in list((DS / "css").rglob("*.css")) + [DS / "tokens" / "tokens.css"]:
        if f.name in {"design-system.css", "design-system.inline.css", "fondamenta.css"}:
            continue  # generati: ripeterebbero le sorgenti
        for m in re.finditer(r"font-weight:\s*(\d{3})", f.read_text(encoding="utf-8")):
            valori.add(int(m.group(1)))
    return sorted(valori)


def riga_copertura(ch, facce):
    celle = "".join(
        f'<td>{"<span class=si>dichiarato</span>" if ord(ch) in f["cmap"] else "<span class=no>assente</span>"}</td>'
        for f in facce
    )
    mono = " mono" if ord(ch) in (0x2227, 0x2228, 0x00AC, 0x2295) else ""
    return f'<tr><td class="glifo{mono}">{ch}</td><td class="cp">U+{ord(ch):04X}</td>{celle}</tr>'


def costruisci():
    css_fonts = (FONTS / "fonts.css").read_text(encoding="utf-8")
    facce = []
    for famiglia, stile, file in FACCE:
        d = dati_faccia(FONTS / file)
        d.update(famiglia=famiglia, stile=stile, file=file,
                 pesi=pesi_dichiarati(css_fonts, famiglia, stile))
        facce.append(d)

    unicode_range = css_fonts.count("unicode-range")
    usati = pesi_usati()

    righe_facce = "".join(
        f'<tr><td>{f["famiglia"]} <span class="etichetta">{f["stile"]}</span></td>'
        f'<td class="cp">{f["file"]}</td>'
        f'<td class="num">{f["byte"]:,}</td>'
        f'<td class="num">{len(f["cmap"]):,}</td>'
        f'<td class="cp">{f["pesi"]}</td>'
        f'<td class="cp">{", ".join(t + " " + str(int(a)) + "–" + str(int(b)) for t, a, b in f["assi"]) or "statico"}</td></tr>'
        for f in facce
    )
    intestazioni = "".join(f'<th>{f["famiglia"]} {f["stile"]}</th>' for f in facce)
    tabelle = ""
    for titolo, glifi in GRUPPI_COPERTURA:
        righe = "".join(riga_copertura(ch, facce) for ch in glifi)
        tabelle += (f'<p class="etichetta">{titolo}</p>'
                    f'<table><tr><th>glifo</th><th>codepoint</th>{intestazioni}</tr>{righe}</table>')

    pesi_html = "".join(
        f'<div class="peso" style="font-weight:{p}">Il significato non sta nella parola '
        f'<span class="etichetta">peso {p}</span></div>' for p in usati
    )

    return f"""<!-- @dsCard group="Fondamenta" -->
<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>Caratteri</title>
<link rel="stylesheet" href="../../css/design-system.css">
<style>{CSS}</style>
</head>
<body>
<p class="nota">Le tre facce del sistema, mostrate e dichiarate. <strong>Mostrate</strong>
è ciò che si vede qui sotto; <strong>dichiarate</strong> è ciò che la <code>cmap</code> di
ogni file contiene, letta da <code>scripts/specimen_caratteri.py</code>. Le due cose non
coincidono: un glifo che il font non ha ripiega in silenzio su un carattere di sistema e
sulla pagina sembra a posto. Questa scheda è generata — si modifica nello script, non qui.</p>

<h2>Le facce</h2>
<table>
<tr><th>faccia</th><th>file</th><th>byte</th><th>codepoint</th><th>pesi dichiarati</th><th>assi</th></tr>
{righe_facce}
</table>
<p class="nota">Nessuna delle tre facce dichiara <code>unicode-range</code>
({unicode_range} occorrenze in <code>fonts.css</code>): ogni faccia è candidata per
qualunque codepoint, e il ripiego dipende solo da cosa contiene.</p>

<h2>Alfabeto</h2>
<p class="etichetta">tondo</p>
<div class="campione">{ALFABETO}</div>
<div class="campione">{MINUSCOLE}</div>
<div class="campione">{CIFRE}</div>
<p class="etichetta">corsivo — faccia separata, non una inclinazione calcolata</p>
<div class="campione corsivo">{ALFABETO}</div>
<div class="campione corsivo">{MINUSCOLE}</div>
<div class="campione corsivo">{CIFRE}</div>
<p class="nota">Le cifre sono minuscole (oldstyle): scendono sotto la linea di base e
hanno altezze diverse fra loro. È la resa predefinita di EB Garamond, non una scelta
dichiarata nei token.</p>

<h2>Italiano</h2>
<div class="campione">{ACCENTI}</div>
<div class="campione">{PUNTEGGIATURA}</div>

<h2>Maiuscoletto</h2>
<p class="nota">Il maiuscoletto sostituisce un secondo carattere: tutto ciò che è apparato
lo usa invece di cambiare famiglia. È la scelta da cui dipende il fatto che il sistema
abbia un solo carattere di testo.</p>
<div class="campione"><span class="apparato">Fondamenti · 1 — Funzioni booleane</span></div>

<h2>Pesi</h2>
<p class="nota">L'asse di peso va da 400 a 800. Qui sono resi i valori che il design system
chiede davvero, ricavati dai suoi CSS: {", ".join(str(p) for p in usati)}.</p>
{pesi_html}

<h2>Copertura dichiarata</h2>
<p class="nota">Reso a sinistra, dichiarato a destra. Dove una faccia risulta «assente», in
quella faccia il glifo viene da un carattere di sistema, diverso da macchina a macchina.</p>
{tabelle}

<h2>Cosa questa pagina non prova</h2>
<p class="nota">Che il browser usi davvero la faccia attesa per un certo glifo: la colonna
dice cosa il file contiene, non quale font il motore ha scelto al momento di disegnare.
Per quello serve l'ispettore del browser, o un confronto di metriche.</p>
</body>
</html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="confronta con il file su disco invece di riscriverlo")
    args = ap.parse_args()

    html = costruisci()
    if args.check:
        if not USCITA.is_file():
            print(f"{USCITA.relative_to(DS)} non esiste: rigenerare.", file=sys.stderr)
            return 1
        attuale = USCITA.read_text(encoding="utf-8")
        if attuale != html:
            print(f"{USCITA.relative_to(DS)} non corrisponde ai font in fonts/: rigenerare.",
                  file=sys.stderr)
            return 1
        print("specimen dei caratteri allineato ai file dei font")
        return 0

    USCITA.parent.mkdir(parents=True, exist_ok=True)
    USCITA.write_text(html, encoding="utf-8")
    print(f"Scritto {USCITA.relative_to(DS)} ({len(html)} caratteri, {len(FACCE)} facce)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
