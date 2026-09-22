#!/usr/bin/env python3
"""build_css.py — assembla il design system in due varianti generate.

    python3 scripts/build_css.py            scrive le due varianti
    python3 scripts/build_css.py --check    fallisce se non sono aggiornate

Sorgenti (queste si editano a mano):
    tokens/tokens.css
    fonts/fonts.css
    css/reset.css, css/base.css, css/layout.css, css/components/*.css

Generati (questi NON si editano a mano):
    css/design-system.css          le pagine del saggio lo collegano con <link>.
                                   I font hanno url() relativi a css/.
    css/fondamenta.css             solo font, azzeramenti e token. Lo collegano
                                   l'ontologia e la Lente semantica, che sono
                                   superfici di consultazione con una tipografia
                                   propria — condividono la tavolozza e i font,
                                   non la scala di lettura del saggio.
    css/design-system.inline.css   per il bundle a file singolo: i font sono
                                   incorporati in data-URI base64, perché un
                                   url() relativo non significa più niente una
                                   volta che il CSS è dentro un <style>.

Perché due varianti e non una sola con percorsi assoluti: un percorso
assoluto legherebbe il repository a un dominio, e il bundle deve
funzionare anche aperto da file://, dove nessun percorso esterno è
garantito. Vedi build_output.py e la nota sul sandbox.

L'ORDINE DEI LAYER è dichiarato una volta in testa al file generato, e da
quel momento non dipende più da come i pezzi sono concatenati:

    @layer reset, tokens, base, layout, components;

Il `<style>` che resta dentro ogni capitolo (CSS dei suoi widget) non è
stratificato, e per le dichiarazioni normali il non stratificato vince su
qualunque layer: ogni pagina può ancora sovrascrivere il sistema senza
alzare la specificità. Attenzione al rovescio, che è controintuitivo: per
le dichiarazioni `!important` l'ordine si inverte, e un `!important` non
stratificato diventa il PIÙ debole. Per questo nel design system non si usa
`!important` se non nel layer `reset`, e lì di proposito.
"""

import argparse
import base64
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
ORDINE_LAYER = "@layer reset, tokens, base, layout, components;"

INTESTAZIONE = """/* ===================================================================
   {nome}
   FILE GENERATO — non editare a mano.
   Si rigenera con:  python3 design-system/scripts/build_css.py
   Le sorgenti sono tokens/tokens.css, fonts/fonts.css, css/*.css e
   css/components/*.css.
   =================================================================== */

"""


def sorgenti():
    """I pezzi, nell'ordine in cui finiscono nel file generato."""
    componenti = sorted((RADICE / "css" / "components").glob("*.css"))
    return {
        "reset": [RADICE / "css" / "reset.css"],
        "tokens": [RADICE / "tokens" / "tokens.css"],
        "base": [RADICE / "css" / "base.css"],
        "layout": [RADICE / "css" / "layout.css"],
        "components": componenti,
    }


def blocco_layer(nome, percorsi):
    corpo = []
    for p in percorsi:
        corpo.append(f"/* ---- {p.relative_to(RADICE)} ---- */")
        corpo.append(p.read_text(encoding="utf-8").rstrip())
        corpo.append("")
    rientrato = "\n".join("  " + r if r.strip() else "" for r in "\n".join(corpo).split("\n"))
    return f"@layer {nome} {{\n{rientrato}\n}}\n"


def font_link():
    """fonts.css con gli url() risolti rispetto a css/ invece che a fonts/."""
    css = (RADICE / "fonts" / "fonts.css").read_text(encoding="utf-8")
    return re.sub(r"url\('([^']+\.woff2)'\)", r"url('../fonts/\1')", css)


def font_inline():
    """fonts.css con i file incorporati in data-URI base64."""
    css = (RADICE / "fonts" / "fonts.css").read_text(encoding="utf-8")

    def incorpora(m):
        f = RADICE / "fonts" / m.group(1)
        if not f.exists():
            raise SystemExit(f"font mancante: {f}")
        dati = base64.b64encode(f.read_bytes()).decode("ascii")
        return f"url('data:font/woff2;base64,{dati}')"

    return re.sub(r"url\('([^']+\.woff2)'\)", incorpora, css)


def assembla(font_css, nome, solo=None):
    """`solo` limita i layer inclusi: serve alla variante `fondamenta`."""
    pezzi = [INTESTAZIONE.format(nome=nome), ORDINE_LAYER, "", font_css.rstrip(), ""]
    for nome_layer, percorsi in sorgenti().items():
        if solo is not None and nome_layer not in solo:
            continue
        pezzi.append(blocco_layer(nome_layer, percorsi))
    return "\n".join(pezzi).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                    help="non scrive: esce con 1 se i generati non corrispondono alle sorgenti")
    args = ap.parse_args()

    uscite = {
        RADICE / "css" / "design-system.css":
            assembla(font_link(), "design-system.css — variante <link>"),
        RADICE / "css" / "fondamenta.css":
            assembla(font_link(), "fondamenta.css — solo font, azzeramenti e token",
                     solo=["reset", "tokens"]),
        RADICE / "css" / "design-system.inline.css":
            assembla(font_inline(), "design-system.inline.css — variante da incorporare"),
    }

    disallineati = []
    for percorso, contenuto in uscite.items():
        if args.check:
            attuale = percorso.read_text(encoding="utf-8") if percorso.exists() else None
            if attuale != contenuto:
                disallineati.append(percorso)
        else:
            percorso.write_text(contenuto, encoding="utf-8")
            kb = len(contenuto.encode("utf-8")) / 1024
            print(f"  scritto  {percorso.relative_to(RADICE.parent)}  ({kb:.0f} KB)")

    if args.check:
        if disallineati:
            print("Generati non aggiornati rispetto alle sorgenti:", file=sys.stderr)
            for p in disallineati:
                print(f"  - {p.relative_to(RADICE.parent)}", file=sys.stderr)
            print("Rigenerali con: python3 design-system/scripts/build_css.py", file=sys.stderr)
            sys.exit(1)
        print("generati allineati alle sorgenti")


if __name__ == "__main__":
    main()
