#!/usr/bin/env python3
"""check_public_names.py — verifica il contratto fra i token e il JavaScript.

    python3 design-system/scripts/check_public_names.py

Alcuni nomi di custom property non sono un dettaglio interno del CSS: sono un
contratto pubblico, perche' il JavaScript li legge per nome. Rinominarne uno
senza aggiornare il JS non produce un errore visibile — produce un canvas nero,
o un SVG senza colore, e nessuna riga in console.

Questo script trova i nomi che il JavaScript usa e li confronta con quelli che
i token definiscono. Tre modi d'uso, che hanno conseguenze diverse:

  LETTO         `getComputedStyle(...).getPropertyValue('--brina')`, anche
                attraverso una funzione di comodo come themeVarHex().
                Se il nome non esiste il valore e' la stringa vuota.

  INTERPOLATO   `var(--arancio-scuro)` dentro una stringa JavaScript che
                genera SVG o HTML iniettato nel DOM. Il var() viene risolto
                dal browser al momento del rendering: se il nome non esiste,
                l'attributo resta senza valore e l'elemento perde il colore.

  SCRITTO       `elemento.style.setProperty('--colore-gruppo', ...)`.
                Qui e' il JavaScript a creare la variabile: NON deve essere
                definita nei token, e infatti non lo e'.

Esce con 1 se un nome letto o interpolato non esiste fra i token, o se un nome
interpretato come esadecimale non ha un valore esadecimale.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
TOKENS = REPO / "design-system/tokens/tokens.css"

# Dove puo' esserci JavaScript che tocca i token.
SORGENTI_JS = [
    REPO / "dominio/src/saggio",
    REPO / "ontologia/lente-semantica/output",
    REPO / "ontologia/output",
]

# Funzioni di comodo che leggono una custom property e ne interpretano il
# valore come esadecimale. Per queste non basta che il nome esista: il valore
# deve essere un colore in notazione esadecimale, altrimenti il parsing a
# valle produce NaN senza dirlo.
LETTORI_ESADECIMALI = {"themeVarHex"}


def blocchi_js(percorso):
    """Il JavaScript di un file, con l'offset da cui parte (per le righe)."""
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    if percorso.suffix == ".js":
        return [(testo, 0)]
    return [(m.group(1), m.start(1)) for m in re.finditer(r"<script[^>]*>(.*?)</script>", testo, re.S)]


def riga_di(percorso, offset):
    testo = percorso.read_text(encoding="utf-8", errors="replace")
    return testo.count("\n", 0, offset) + 1


def token_definiti():
    """{nome: valore} dal :root di tokens.css, commenti esclusi."""
    css = re.sub(r"/\*.*?\*/", "", TOKENS.read_text(encoding="utf-8"), flags=re.S)
    return {m.group(1): m.group(2).strip() for m in re.finditer(r"(--[a-z0-9-]+)\s*:\s*([^;]+);", css)}


def risolvi(nome, definiti, profondita=0):
    """Segue la catena di var() fino a un valore letterale."""
    valore = definiti.get(nome, "")
    m = re.fullmatch(r"var\(\s*(--[a-z0-9-]+)\s*\)", valore.strip())
    if m and profondita < 8:
        return risolvi(m.group(1), definiti, profondita + 1)
    return valore


def scandisci():
    letti, interpolati, scritti, esadecimali = {}, {}, {}, {}
    file_js = []
    for radice in SORGENTI_JS:
        if not radice.exists():
            continue
        file_js += sorted(radice.rglob("*.html")) + sorted(radice.rglob("*.js"))

    for f in file_js:
        for js, offset in blocchi_js(f):
            # scritto: setProperty("--nome", …)
            for m in re.finditer(r"""setProperty\(\s*['"](--[a-z0-9-]+)['"]""", js):
                scritti.setdefault(m.group(1), []).append((f, riga_di(f, offset + m.start())))
            # letto attraverso una funzione che lo interpreta come esadecimale
            for lettore in LETTORI_ESADECIMALI:
                for m in re.finditer(lettore + r"""\(\s*['"](--[a-z0-9-]+)['"]""", js):
                    esadecimali.setdefault(m.group(1), []).append((f, riga_di(f, offset + m.start())))
            # letto: qualunque altra stringa letterale che sia un nome di token
            for m in re.finditer(r"""['"](--[a-z0-9-]+)['"]""", js):
                nome = m.group(1)
                posizione = (f, riga_di(f, offset + m.start()))
                if posizione in scritti.get(nome, []):
                    continue
                letti.setdefault(nome, []).append(posizione)
            # interpolato: var(--nome) dentro una stringa JavaScript
            for m in re.finditer(r"var\(\s*(--[a-z0-9-]+)\s*\)", js):
                interpolati.setdefault(m.group(1), []).append((f, riga_di(f, offset + m.start())))

    # un nome scritto dal JS non e' anche "letto": si toglie dal primo insieme
    for nome in scritti:
        letti.pop(nome, None)
    return letti, interpolati, scritti, esadecimali


def elenco(titolo, mappa, definiti, problemi, tipo):
    if not mappa:
        return
    print(f"\n{titolo} ({len(mappa)})")
    for nome in sorted(mappa):
        posizioni = mappa[nome]
        dove = ", ".join(sorted({p.name for p, _ in posizioni}))
        valore = risolvi(nome, definiti, 0) if nome in definiti else None
        if valore is None:
            print(f"  ✗ {nome:<26} NON DEFINITO NEI TOKEN     {dove}")
            problemi.append(f"{nome} — {tipo} in {dove} ma non definito nei token")
        else:
            print(f"    {nome:<26} = {valore:<34} {dove}")


def main():
    definiti = token_definiti()
    letti, interpolati, scritti, esadecimali = scandisci()
    problemi = []

    print(f"Token definiti in tokens.css: {len(definiti)}")

    elenco("LETTI dal JavaScript per nome", letti, definiti, problemi, "letto")
    elenco("INTERPOLATI come var() dentro stringhe JavaScript", interpolati, definiti, problemi, "interpolato")

    if esadecimali:
        print(f"\nINTERPRETATI COME ESADECIMALE ({len(esadecimali)})")
        for nome in sorted(esadecimali):
            dove = ", ".join(sorted({p.name for p, _ in esadecimali[nome]}))
            valore = risolvi(nome, definiti, 0)
            ok = bool(re.fullmatch(r"#[0-9a-fA-F]{3,8}", valore.strip()))
            marca = "  " if ok else "✗ "
            print(f"  {marca}{nome:<26} = {valore:<34} {dove}")
            if not ok:
                problemi.append(
                    f"{nome} vale «{valore}», che non e' esadecimale, ma viene passato "
                    f"a una funzione che lo interpreta come tale ({dove})")

    if scritti:
        print(f"\nSCRITTI dal JavaScript, non devono stare nei token ({len(scritti)})")
        for nome in sorted(scritti):
            dove = ", ".join(sorted({p.name for p, _ in scritti[nome]}))
            avviso = "  ← ATTENZIONE: definito anche nei token" if nome in definiti else ""
            print(f"    {nome:<26} {dove}{avviso}")

    # informativo: token definiti che nessuno usa, ne' in CSS ne' in JS
    usati_css = set()
    for f in (REPO / "design-system").rglob("*.css"):
        if "/lab/" in str(f) or f.name.startswith("design-system"):
            continue
        for m in re.finditer(r"var\(\s*(--[a-z0-9-]+)", f.read_text(encoding="utf-8")):
            usati_css.add(m.group(1))
    for radice in SORGENTI_JS:
        for f in list(radice.rglob("*.html")) + list(radice.rglob("*.css")):
            for m in re.finditer(r"var\(\s*(--[a-z0-9-]+)", f.read_text(encoding="utf-8", errors="replace")):
                usati_css.add(m.group(1))
    mai_usati = sorted(set(definiti) - usati_css - set(letti) - set(interpolati) - set(esadecimali))
    if mai_usati:
        print(f"\nDEFINITI MA MAI USATI ({len(mai_usati)}) — informativo, non un errore")
        for nome in mai_usati:
            print(f"    {nome}")

    print()
    if problemi:
        print(f"CONTRATTO ROTTO — {len(problemi)} problemi:")
        for p in problemi:
            print(f"  - {p}")
        sys.exit(1)
    print("Contratto rispettato: ogni nome usato dal JavaScript esiste fra i token.")


if __name__ == "__main__":
    main()
