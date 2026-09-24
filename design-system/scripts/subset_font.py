#!/usr/bin/env python3
"""subset_font.py — riduce Noto Sans Mono ai soli caratteri che il saggio usa.

    python3 design-system/scripts/subset_font.py PERCORSO/NotoSansMono.ttf
    python3 design-system/scripts/subset_font.py PERCORSO/NotoSansMono.ttf --check

Il file sorgente NON sta nel repository: è un variabile da 1,67 MB, e tenerlo
qui significherebbe versionare 166 volte il peso di ciò che serve davvero. Si
scarica da:

    https://github.com/google/fonts/tree/main/ofl/notosansmono
    NotoSansMono[wdth,wght].ttf — licenza OFL-1.1

PERCHÉ NOTO SANS MONO, e non IBM Plex Mono che c'era prima. Il monospaziato in
questo progetto ha due usi dichiarati: i quattro simboli logici ∧ ∨ ¬ ⊕ di
Fondamenti · 1, e i valori tecnici che cambiano dal vivo in Meccanismo · 4 e 6.
IBM Plex Mono **non contiene ∧, ∨, ⊕** — verificato leggendo la cmap, non a
occhio — quindi tre dei quattro simboli ripiegavano su un font di sistema,
diverso da macchina a macchina e visibilmente più piccolo delle lettere
accanto. Su otto monospaziati con licenza aperta esaminati, Noto Sans Mono è
l'unico che li contiene tutti e tre.

IL PESO È UNO SOLO. Verificato sul bundle compilato, che contiene tutti e 14 i
capitoli: il browser carica solo il peso 400. Dei tre file di Plex che stavano
qui, due non venivano mai richiesti. Il sorgente è un font variabile con assi
wght e wdth: si istanzia a 400/100 prima di ridurre, così gli assi non
viaggiano insieme al file.
"""

import argparse
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
USCITA = RADICE / "fonts" / "NotoSansMono-Tecnico.woff2"

# Insieme dichiarato, non dedotto: cambiarlo qui e rigenerare è l'unico modo
# di aggiungere un carattere al monospaziato del saggio.
ASCII = "".join(chr(c) for c in range(0x20, 0x7F))
ITALIANO = "àèéìòùÀÈÉÌÒÙ«»’“”–—…·"
# Nessun ␣ (U+2423): Noto Sans Mono non ce l'ha, e non serve — l'unico uso nel
# saggio è in `.pg-chip .glyph::before` di Meccanismo · 1, che è in serif, non
# in monospaziato. (Anche EB Garamond non lo contiene: quel glifo ripiega da
# sempre, cosa diversa e preesistente.)
TECNICI = "∧∨¬⊕↔≈∼→↓−›ⁿ⁰⁸⁹"
CARATTERI = ASCII + ITALIANO + TECNICI

# Questi devono esserci, altrimenti il font non fa il lavoro per cui è stato
# scelto e lo script deve fallire invece di produrre un file inutile.
INDISPENSABILI = "∧∨¬⊕"


def costruisci(sorgente: Path) -> bytes:
    from fontTools.ttLib import TTFont
    from fontTools.varLib import instancer
    from fontTools import subset

    tf = TTFont(sorgente)
    if "fvar" in tf:
        tf = instancer.instantiateVariableFont(tf, {"wght": 400, "wdth": 100}, inplace=True)

    coperti = set()
    for t in tf["cmap"].tables:
        coperti |= set(t.cmap.keys())
    mancanti = [c for c in INDISPENSABILI if ord(c) not in coperti]
    if mancanti:
        raise SystemExit(
            f"{sorgente.name} non contiene {' '.join(mancanti)} — "
            "non è il font giusto per questo lavoro.")

    opzioni = subset.Options()
    opzioni.flavor = "woff2"
    opzioni.layout_features = ["*"]
    opzioni.notdef_outline = True
    opzioni.desubroutinize = True
    s = subset.Subsetter(options=opzioni)
    s.populate(text=CARATTERI)
    s.subset(tf)

    import io
    buf = io.BytesIO()
    tf.flavor = "woff2"
    tf.save(buf)
    tf.close()
    return buf.getvalue()


def verifica(dati: bytes):
    """Il file prodotto contiene davvero ciò che deve."""
    from fontTools.ttLib import TTFont
    import io

    tf = TTFont(io.BytesIO(dati), lazy=True)
    coperti = set()
    for t in tf["cmap"].tables:
        coperti |= set(t.cmap.keys())
    tf.close()
    persi = [c for c in CARATTERI if ord(c) not in coperti]
    return len(coperti), persi


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("sorgente", type=Path, help="NotoSansMono[wdth,wght].ttf")
    ap.add_argument("--check", action="store_true",
                    help="non scrive: esce con 1 se il file nel repository non corrisponde")
    args = ap.parse_args()

    if not args.sorgente.exists():
        raise SystemExit(
            f"sorgente non trovato: {args.sorgente}\n"
            "Scaricalo da https://github.com/google/fonts/tree/main/ofl/notosansmono")

    dati = costruisci(args.sorgente)
    n, persi = verifica(dati)
    if persi:
        raise SystemExit(f"il sottoinsieme ha perso {len(persi)} caratteri: {''.join(persi)}")

    if args.check:
        attuale = USCITA.read_bytes() if USCITA.exists() else None
        if attuale != dati:
            print(f"{USCITA.name} non corrisponde al sorgente: rigeneralo", file=sys.stderr)
            sys.exit(1)
        print(f"{USCITA.name} allineato al sorgente ({n} codepoint)")
        return

    USCITA.write_bytes(dati)
    print(f"  scritto  {USCITA.relative_to(RADICE.parent)}  "
          f"({len(dati)/1024:.1f} KB, {n} codepoint, da {args.sorgente.name})")


if __name__ == "__main__":
    main()
