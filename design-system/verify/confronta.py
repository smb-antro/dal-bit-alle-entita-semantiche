#!/usr/bin/env python3
"""confronta.py — confronta baseline/ e attuale/ con Pillow, a pixel.

Uso:
    python3 confronta.py
    python3 confronta.py --soglia 0.05
    python3 confronta.py --base baseline --attuale attuale --diff differenze

Per ogni file .png presente in entrambe le cartelle: conta i pixel che
differiscono in almeno un canale RGB, calcola la percentuale sul totale,
scrive un'immagine di differenza amplificata in differenze/ (solo se ci sono
differenze) e stampa un rapporto riga per riga con l'esito (OK / FALLITO).

La tolleranza NON e' una percentuale di pixel: e' l'ENTITA della
differenza. Il cancello di qualita' ha mostrato che due catture consecutive
sullo stesso codice immutato possono differire su centinaia di migliaia di
pixel — ma sempre e solo di 1 livello su 255, nelle aree di sfumatura, dove
il dithering di Chrome non e' riproducibile al bit. Una tolleranza
percentuale avrebbe dovuto salire fino al 4% per assorbirlo, e a quel punto
avrebbe lasciato passare cambiamenti veri. Misurando invece il delta per
canale, le due popolazioni si separano nettamente:

  - delta 1   -> rumore di rasterizzazione, centinaia di migliaia di pixel
  - delta >=2 -> differenza reale (il caso trovato: un cursore lampeggiante
                 colto a fase diversa, 96 pixel con delta fino a 10)

Quindi si FALLISCE su qualunque pixel con delta > DELTA_RUMORE, mentre i
pixel a delta 1 si contano e si riportano, senza far fallire.
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops

# Differenza massima per canale considerata rumore di rasterizzazione.
# Misurato su tre catture consecutive dello stesso codice immutato: il grosso
# del rumore sta a delta 1 (sfumature), ma un bersaglio ha mostrato 16 pixel a
# delta 2 in un confronto e zero nel successivo — quindi anche 2 e' rumore
# casuale, non un segnale. Da 3 in su non si e' mai osservato rumore.
DELTA_RUMORE = 2

# Quanti pixel percettibili (delta > DELTA_RUMORE) si tollerano: nessuno.
MAX_PIXEL_PERCETTIBILI = 0

# Eccezioni per bersaglio: id-bersaglio -> (numero massimo di pixel
# percettibili tollerati, ragione con la misura di partenza). Vuoto: finora
# nessun bersaglio ne ha avuto bisogno — vedi README.md.
SOGLIE_PER_BERSAGLIO = {
    # Due pixel bistabili sull'antialiasing dei bordi nel grafo radiale, a
    # (817,524) e (891,888): su tre catture dello stesso codice, la prima e la
    # terza sono identiche e la seconda differisce in quei due soli pixel,
    # sempre con gli stessi due valori alternativi (delta 9 e 7). E' una
    # coordinata che cade esatta su un mezzo pixel e arrotonda in un verso o
    # nell'altro, non contenuto che cambia. Margine 4 = il doppio del
    # misurato: due pixel non possono nascondere una regressione in un grafo.
    'lente-attention-grado2__desktop': (4, "2 px bistabili di antialiasing, misurati su 3 catture"),
}


def id_bersaglio(nome_file):
    """'saggio-foo__desktop__reduced-motion.png' -> 'saggio-foo__desktop__reduced-motion'"""
    return Path(nome_file).stem


def gruppo_di(id_b):
    for prefisso in ("saggio-", "ontologia-", "lente-"):
        if id_b.startswith(prefisso):
            return prefisso.rstrip("-")
    return "altro"


def istogramma_delta(diff_rgb):
    """Distribuzione del delta massimo per canale, pixel per pixel.

    Non si usa .convert('L') sull'immagine di differenza: la conversione in
    luminanza puo' arrotondare a 0 differenze piccole ma reali (es. un
    canale che differisce di 1 pesa .114-.299 in L, sotto la soglia di
    arrotondamento a 8 bit) — un falso negativo esattamente nel tipo di
    micro-differenza che questo harness deve poter dimostrare essere zero.
    Si prende invece il massimo pixel-per-pixel fra i tre canali, senza
    perdita di precisione, e se ne restituisce l'istogramma: l'indice e' il
    delta, il valore quanti pixel lo hanno.
    """
    r, g, b = diff_rgb.split()
    massimo = ImageChops.lighter(ImageChops.lighter(r, g), b)
    return massimo.histogram()


def confronta_coppia(path_base, path_attuale, path_diff):
    im_base = Image.open(path_base).convert("RGB")
    im_attuale = Image.open(path_attuale).convert("RGB")

    dimensioni_diverse = im_base.size != im_attuale.size
    if dimensioni_diverse:
        # Non si puo' fare un diff pixel-a-pixel fra dimensioni diverse:
        # si mette ciascuna immagine su una tela delle dimensioni massime
        # (sentinella magenta per l'area che manca da un lato), cosi' il
        # confronto resta possibile e onesto — l'intera area mancante conta
        # come "diversa", il che e' corretto: e' contenuto che non c'era o
        # non c'e' piu'.
        w = max(im_base.width, im_attuale.width)
        h = max(im_base.height, im_attuale.height)
        sentinella = (255, 0, 255)
        tela_base = Image.new("RGB", (w, h), sentinella)
        tela_base.paste(im_base, (0, 0))
        tela_attuale = Image.new("RGB", (w, h), sentinella)
        tela_attuale.paste(im_attuale, (0, 0))
        im_base, im_attuale = tela_base, tela_attuale

    diff = ImageChops.difference(im_base, im_attuale)
    isto = istogramma_delta(diff)
    pixel_rumore = sum(isto[1:DELTA_RUMORE + 1])
    pixel_percettibili = sum(isto[DELTA_RUMORE + 1:])
    pixel_diversi = pixel_rumore + pixel_percettibili
    delta_massimo = max((d for d, n in enumerate(isto) if n and d), default=0)
    totale_pixel = im_base.width * im_base.height
    percentuale = (pixel_diversi / totale_pixel * 100) if totale_pixel else 0.0

    if pixel_diversi > 0:
        # amplifica per renderla leggibile a occhio: differenze reali sono
        # spesso di pochi livelli su 255 e altrimenti sembrerebbero nere.
        amplificata = diff.point(lambda x: min(255, x * 12))
        amplificata.save(path_diff)

    return {
        "pixel_diversi": pixel_diversi,
        "pixel_rumore": pixel_rumore,
        "pixel_percettibili": pixel_percettibili,
        "delta_massimo": delta_massimo,
        "totale_pixel": totale_pixel,
        "percentuale": percentuale,
        "dimensioni_diverse": dimensioni_diverse,
        "dim_base": Image.open(path_base).size,
        "dim_attuale": Image.open(path_attuale).size,
    }


def main():
    qui = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description="Confronta baseline/ e attuale/ a pixel con Pillow.")
    ap.add_argument("--base", default=str(qui / "baseline"))
    ap.add_argument("--attuale", default=str(qui / "attuale"))
    ap.add_argument("--diff", default=str(qui / "differenze"))
    ap.add_argument("--max-pixel", type=int, default=None,
                    help="pixel percettibili tollerati (default 0)")
    args = ap.parse_args()

    dir_base = Path(args.base)
    dir_attuale = Path(args.attuale)
    dir_diff = Path(args.diff)

    if not dir_base.is_dir():
        print(f"Cartella baseline assente: {dir_base} — esegui prima 'node cattura.js --baseline'", file=sys.stderr)
        sys.exit(2)
    if not dir_attuale.is_dir():
        print(f"Cartella attuale assente: {dir_attuale} — esegui prima 'node cattura.js'", file=sys.stderr)
        sys.exit(2)

    dir_diff.mkdir(parents=True, exist_ok=True)
    for vecchio in dir_diff.glob("*.png"):
        vecchio.unlink()

    file_base = {p.name for p in dir_base.glob("*.png")}
    file_attuale = {p.name for p in dir_attuale.glob("*.png")}

    solo_base = sorted(file_base - file_attuale)
    solo_attuale = sorted(file_attuale - file_base)
    comuni = sorted(file_base & file_attuale)

    if not comuni:
        print("Nessun file in comune fra baseline/ e attuale/: niente da confrontare.", file=sys.stderr)
        sys.exit(2)

    righe = []
    falliti = 0
    for nome in comuni:
        idb = id_bersaglio(nome)
        gruppo = gruppo_di(idb)
        soglia, motivo = SOGLIE_PER_BERSAGLIO.get(idb, (None, None))
        if args.max_pixel is not None:
            soglia = args.max_pixel
        elif soglia is None:
            soglia = MAX_PIXEL_PERCETTIBILI

        path_diff = dir_diff / nome
        ris = confronta_coppia(dir_base / nome, dir_attuale / nome, path_diff)

        esito_ok = (not ris["dimensioni_diverse"]) and ris["pixel_percettibili"] <= soglia
        if not esito_ok:
            falliti += 1

        righe.append({
            "nome": nome, "gruppo": gruppo, "esito_ok": esito_ok,
            "soglia": soglia, "motivo": motivo, **ris,
        })

    # ---- rapporto ----
    larghezza_nome = max(len(r["nome"]) for r in righe)
    gruppo_corrente = None
    for r in sorted(righe, key=lambda r: (r["gruppo"], r["nome"])):
        if r["gruppo"] != gruppo_corrente:
            gruppo_corrente = r["gruppo"]
            print(f"\n== {gruppo_corrente} ==")
        esito = "OK     " if r["esito_ok"] else "FALLITO"
        if r["dimensioni_diverse"]:
            dettaglio = f"dimensioni diverse: baseline {r['dim_base']} vs attuale {r['dim_attuale']}"
        else:
            dettaglio = (f"percettibili {r['pixel_percettibili']:>7} (soglia {r['soglia']})"
                         f"   rumore {r['pixel_rumore']:>7}   delta max {r['delta_massimo']:>3}")
        suffisso_motivo = f"  — {r['motivo']}" if r['motivo'] else ""
        print(f"  {esito}  {r['nome']:<{larghezza_nome}}  {dettaglio}{suffisso_motivo}")

    if solo_base:
        print(f"\nSolo in baseline/ (mancanti in attuale/, {len(solo_base)}):")
        for n in solo_base:
            print(f"  - {n}")
    if solo_attuale:
        print(f"\nSolo in attuale/ (nuovi rispetto a baseline/, {len(solo_attuale)}):")
        for n in solo_attuale:
            print(f"  - {n}")

    rumore_tot = sum(r["pixel_rumore"] for r in righe)
    px_tot = sum(r["totale_pixel"] for r in righe)
    print(f"\n{len(comuni)} confrontati, {falliti} falliti, {len(solo_base)} mancanti, {len(solo_attuale)} nuovi.")
    print(f"Rumore assorbito (delta <= {DELTA_RUMORE}): {rumore_tot} pixel su {px_tot}.")
    if falliti or solo_base:
        sys.exit(1)


if __name__ == "__main__":
    main()
