#!/usr/bin/env python3
"""export_tokens.py — genera tokens/tokens.json da tokens/tokens.css.

    python3 scripts/export_tokens.py            scrive tokens/tokens.json
    python3 scripts/export_tokens.py --check    fallisce se non è aggiornato

SORGENTE DI VERITÀ resta `tokens/tokens.css` — non si edita tokens.json a
mano, si rigenera. A cosa serve allora un JSON, se il CSS già esiste ed è
l'unica cosa che il browser legge davvero?

1. **Claude Design** accetta un JSON di token con `$type` e `$description`
   espliciti per ogni valore, invece di dover indovinare il livello
   semantico (primitivo/ruolo) dai soli nomi delle custom property — cosa
   che un tool non può fare in modo affidabile quando i nomi sono storici
   e in italiano, come `--brina` o `--arancio-scuro`.
2. **Figma**, via Tokens Studio, che importa direttamente un file DTCG per
   tenere la libreria dei colori/tipografia sincronizzata col codice.
3. **Style Dictionary v4**, che tratta il formato DTCG come cittadino di
   prima classe e da un unico JSON genera piattaforme che questo
   repository non tocca direttamente — JS, SCSS, Tailwind, iOS/Android.
4. È un formato **W3C neutro e stabile** (Design Tokens Community Group,
   prima release stabile 2025.10): un contratto che non dipende dalla
   beta di Claude Design né da nessun altro consumatore in particolare,
   e che sopravvive se uno di questi strumenti cambia o sparisce.

**Limite noto, dichiarato qui perché non è ovvio leggendo il JSON**: la
specifica DTCG 2025.10 non standardizza temi o modalità (niente "modes"
alla Figma-Variables, niente struttura per varianti chiaro/scuro dentro
lo stesso file). Il tema chiaro è l'unico che questo file rappresenta.
Se in futuro nascerà un tema scuro (rimandato, vedi docs/decision-log.md,
voce del 4 settembre 2026), sarà un **secondo file** — non una chiave in
più dentro questo, perché la spec non gli darebbe un posto dove stare.

── STRUTTURA DEI GRUPPI ────────────────────────────────────────────────
Rispecchia i due livelli dichiarati in tokens.css (primitivi, semantici:
tokens.css non ha un terzo livello "componente" — quello vive solo nel
CSS dei componenti, come valori diretti ai semantici, mai in tokens.css).

Il nome-foglia di ogni token è SEMPRE il nome della custom property CSS
meno "--" (`--grigio-testo` → foglia `grigio-testo`), qualunque sia il
gruppo che lo contiene. Questa è la regola che rende il mapping
nome-CSS ↔ percorso-JSON deterministico e invertibile: dato un percorso
JSON, il nome CSS è sempre il suo ultimo segmento con "--" davanti,
senza bisogno di consultare altro. L'appartenenza di ciascun nome al suo
gruppo è dichiarata esplicitamente in TOKENS qui sotto (i nomi storici
non condividono un prefisso comune abbastanza regolare — `bianco`,
`blu-scuro`, `cat-gerarchia`, `rail-w` — per essere derivata da una
regola sola), ma resta una tabella fissa e verificata: `--check` fallisce
se un nome compare in tokens.css e non in questa tabella, o viceversa.
"""

import argparse
import json
import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
TOKENS_CSS = RADICE / "tokens" / "tokens.css"
TOKENS_JSON = RADICE / "tokens" / "tokens.json"

# ─────────────────────────────────────────────────────────────────────
# Tabella dei token: (nome-css, percorso-gruppo, tipo, descrizione).
#
# "tipo" guida sia la validazione del valore letto dal CSS sia la resa
# nel JSON:
#   color-hex     valore letterale "#RRGGBB"
#   color-rgba    valore letterale "rgba(r,g,b,a)"
#   dimension     valore letterale numero+unità, unità ammesse rem/px
#   fontfamily    valore letterale, stack di nomi separati da virgola
#   number        valore letterale, numero puro
#   number-em     valore letterale in "em": la spec DTCG 2025.10 non
#                 ammette "em" come unità di $type dimension (solo
#                 assolute); reso come $type "number" con l'em lasciato
#                 alla descrizione — vedi la voce --traccia-apparato.
#   alias         valore letterale "var(--altro-nome)": risolto nel
#                 percorso JSON del token puntato, non ricopiato.
# ─────────────────────────────────────────────────────────────────────

TOKENS = [
    # ── primitivo.colore.neutro ──
    ("bianco", ("primitivo", "colore", "neutro"), "color-hex",
     "Neutro: bianco puro."),
    ("brina", ("primitivo", "colore", "neutro"), "color-hex",
     "Neutro: grigio-azzurro chiarissimo, il più chiaro dopo il bianco."),
    ("inchiostro", ("primitivo", "colore", "neutro"), "color-hex",
     "Neutro: quasi nero, il più scuro della tavolozza."),
    ("grigio-testo", ("primitivo", "colore", "neutro"), "color-hex",
     "Neutro: grigio-bruno per testo attenuato."),
    ("grigio-soft", ("primitivo", "colore", "neutro"), "color-hex",
     "Neutro: grigio tenue, il più chiaro dei grigi di testo."),

    # ── primitivo.colore.blu (navigazione del saggio) ──
    ("blu-scuro", ("primitivo", "colore", "blu"), "color-hex",
     "Famiglia blu (navigazione del saggio): tono più scuro."),
    ("blu", ("primitivo", "colore", "blu"), "color-hex",
     "Famiglia blu (navigazione del saggio): tono medio, il colore base della famiglia."),
    ("blu-chiaro", ("primitivo", "colore", "blu"), "color-hex",
     "Famiglia blu (navigazione del saggio): tono più chiaro."),

    # ── primitivo.colore.arancio (apparato del saggio) ──
    ("arancio-scuro", ("primitivo", "colore", "arancio"), "color-hex",
     "Famiglia arancio (apparato del saggio): tono più scuro."),
    ("arancio", ("primitivo", "colore", "arancio"), "color-hex",
     "Famiglia arancio (apparato del saggio): tono medio, il colore base della famiglia."),
    ("arancio-chiaro", ("primitivo", "colore", "arancio"), "color-hex",
     "Famiglia arancio (apparato del saggio): tono più chiaro."),

    # ── primitivo.colore.verde (ontologia) ──
    ("verde-scuro", ("primitivo", "colore", "verde"), "color-hex",
     "Famiglia verde (ontologia): tono più scuro."),
    ("verde", ("primitivo", "colore", "verde"), "color-hex",
     "Famiglia verde (ontologia): tono medio, il colore base della famiglia — "
     "quello usato come testo, contrasto ≈5,2:1 su bianco (vedi docs/decision-log.md, 8 settembre 2026)."),
    ("verde-chiaro", ("primitivo", "colore", "verde"), "color-hex",
     "Famiglia verde (ontologia): tono più chiaro."),

    # ── primitivo.colore.tratto ──
    ("line", ("primitivo", "colore", "tratto"), "color-rgba",
     "Tratto: inchiostro a bassa opacità, per bordi e divisori — mai come colore di testo."),

    # ── primitivo.colore.categoria (Lente semantica — contratto pubblico) ──
    ("cat-gerarchia", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: categoria di relazione «gerarchia». Letta per nome da lente.js: non ridisegnare."),
    ("cat-concettuale", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: categoria di relazione «concettuale». Letta per nome da lente.js: non ridisegnare."),
    ("cat-attribuzione", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: categoria di relazione «attribuzione». Letta per nome da lente.js: non ridisegnare."),
    ("cat-struttura", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: categoria di relazione «struttura». Letta per nome da lente.js: non ridisegnare."),
    ("cat-gerarchia-tenue", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: variante tenue di «gerarchia», per i collegamenti di secondo grado."),
    ("cat-concettuale-tenue", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: variante tenue di «concettuale», per i collegamenti di secondo grado."),
    ("cat-attribuzione-tenue", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: variante tenue di «attribuzione», per i collegamenti di secondo grado."),
    ("cat-struttura-tenue", ("primitivo", "colore", "categoria"), "color-hex",
     "Lente semantica: variante tenue di «struttura», per i collegamenti di secondo grado."),

    # ── primitivo.colore.gruppo-nodo (Lente semantica — contratto pubblico) ──
    ("grp-concetto", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Concetto». Letto per nome da lente.js: non ridisegnare."),
    ("grp-teorico", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Teorico». Letto per nome da lente.js: non ridisegnare."),
    ("grp-unita", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Unità». Letto per nome da lente.js: non ridisegnare."),
    ("grp-dataset", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Dataset». Letto per nome da lente.js: non ridisegnare."),
    ("grp-capitolo", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Capitolo». Letto per nome da lente.js: non ridisegnare."),
    ("grp-parte", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Parte». Letto per nome da lente.js: non ridisegnare."),
    ("grp-altro", ("primitivo", "colore", "gruppo-nodo"), "color-hex",
     "Lente semantica: colore del gruppo di nodo «Altro». Letto per nome da lente.js: non ridisegnare."),

    # ── primitivo.font ──
    ("serif", ("primitivo", "font"), "fontfamily",
     "Stack per il testo in tondo: EB Garamond con le ricadute di sistema."),
    ("mono", ("primitivo", "font"), "fontfamily",
     "Stack monospaziato per simboli logici ed etichette tecniche: IBM Plex Mono con le ricadute di sistema."),

    # ── primitivo.misura ──
    ("rail-w", ("primitivo", "misura"), "dimension",
     "Larghezza del binario di navigazione fisso."),

    # ── semantico.colore.superficie ──
    ("colore-fondo", ("semantico", "colore", "superficie"), "alias",
     "Sfondo della pagina."),
    ("colore-superficie", ("semantico", "colore", "superficie"), "alias",
     "Superfici sollevate — card, pannelli, bottoni pieni."),
    ("colore-testo", ("semantico", "colore", "superficie"), "alias",
     "Testo principale."),
    ("colore-testo-attenuato", ("semantico", "colore", "superficie"), "alias",
     "Testo secondario — note, sottotitoli."),
    ("colore-testo-tenue", ("semantico", "colore", "superficie"), "alias",
     "Testo più tenue — apparato, occhielli."),
    ("colore-bordo", ("semantico", "colore", "superficie"), "alias",
     "Bordi e divisori a bassa opacità."),

    # ── semantico.colore.navigazione ──
    ("colore-navigazione", ("semantico", "colore", "navigazione"), "alias",
     "Navigazione del saggio: dove sei, dove puoi andare."),
    ("colore-navigazione-forte", ("semantico", "colore", "navigazione"), "alias",
     "Variante più scura della navigazione."),
    ("colore-navigazione-tenue", ("semantico", "colore", "navigazione"), "alias",
     "Variante più chiara della navigazione."),

    # ── semantico.colore.apparato ──
    ("colore-apparato", ("semantico", "colore", "apparato"), "alias",
     "Apparato del saggio: ciò che parla del testo senza esserne parte (occhielli, note, rimandi, domande)."),
    ("colore-apparato-medio", ("semantico", "colore", "apparato"), "alias",
     "Variante media dell'apparato."),
    ("colore-apparato-tenue", ("semantico", "colore", "apparato"), "alias",
     "Variante più chiara dell'apparato."),

    # ── semantico.colore.ontologia ──
    ("colore-ontologia", ("semantico", "colore", "ontologia"), "alias",
     "Passaggio dal saggio alla sua cartografia semantica."),
    ("colore-ontologia-forte", ("semantico", "colore", "ontologia"), "alias",
     "Variante più scura dell'ontologia."),
    ("colore-ontologia-tenue", ("semantico", "colore", "ontologia"), "alias",
     "Variante più chiara dell'ontologia."),

    # ── semantico.font ──
    ("font-testo", ("semantico", "font"), "alias",
     "Famiglia tipografica del corpo del testo."),
    ("font-mono", ("semantico", "font"), "alias",
     "Famiglia tipografica monospaziata."),

    # ── semantico.dimensione (scala tipografica, unica dal 22 settembre 2026) ──
    ("dim-testo", ("semantico", "dimensione"), "dimension",
     "Corpo del testo."),
    ("dim-lede", ("semantico", "dimensione"), "dimension",
     "Paragrafo d'attacco."),
    ("dim-citazione", ("semantico", "dimensione"), "dimension",
     "Citazioni (blockquote)."),
    ("dim-richiamo", ("semantico", "dimensione"), "dimension",
     "Richiamo/domanda (.question)."),
    ("dim-nota", ("semantico", "dimensione"), "dimension",
     "Note a margine (.aside p)."),
    ("dim-apparato", ("semantico", "dimensione"), "dimension",
     "Occhiello, nota di chiusura."),
    ("dim-apparato-minore", ("semantico", "dimensione"), "dimension",
     "Etichetta minore di .aside."),
    ("dim-nav-titolo", ("semantico", "dimensione"), "dimension",
     "Titolo nel binario di navigazione."),
    ("dim-nav-parte", ("semantico", "dimensione"), "dimension",
     "Intestazione di parte nel binario di navigazione (kicker)."),
    ("dim-nav-voce", ("semantico", "dimensione"), "dimension",
     "Voce di modulo nel binario di navigazione."),
    ("dim-nav-sottovoce", ("semantico", "dimensione"), "dimension",
     "Voce di unità nel binario di navigazione."),
    ("dim-nav-numero", ("semantico", "dimensione"), "dimension",
     "Numero nel binario di navigazione."),
    ("traccia-apparato", ("semantico", "dimensione"), "number-em",
     "Spaziatura delle lettere del maiuscoletto d'apparato, in em. Reso come "
     "$type \"number\" (valore 0,06) perché la DTCG 2025.10 non ammette \"em\" "
     "come unità di $type dimension — vedi il docstring di questo script."),

    # ── semantico.numero ──
    ("interlinea-testo", ("semantico", "numero"), "number",
     "Interlinea del corpo del testo, unica per tutte le pagine del saggio dal 22 settembre 2026."),

    # ── semantico.struttura ──
    ("misura-colonna", ("semantico", "struttura"), "dimension",
     "Larghezza massima della colonna di lettura."),
    ("misura-rail", ("semantico", "struttura"), "alias",
     "Larghezza del binario di navigazione."),
]

# Descrizioni dei gruppi (facoltative, solo dove aiutano a orientarsi) e
# $type dichiarato una volta sola per gruppo — i token dentro lo ereditano.
GROUP_META = {
    ("primitivo",): {
        "description": "Il valore grezzo. Nessun significato semantico: solo il colore o la misura."},
    ("primitivo", "colore"): {
        "type": "color",
        "description": "La tavolozza. Verificata identica in tutti i 16 file che la definivano prima di questo design system."},
    ("primitivo", "colore", "neutro"): {},
    ("primitivo", "colore", "blu"): {},
    ("primitivo", "colore", "arancio"): {},
    ("primitivo", "colore", "verde"): {},
    ("primitivo", "colore", "tratto"): {},
    ("primitivo", "colore", "categoria"): {
        "description": "Categorie di relazione della Lente semantica — contratto pubblico, non ridisegnare."},
    ("primitivo", "colore", "gruppo-nodo"): {
        "description": "Colori per gruppo di nodo della Lente semantica — contratto pubblico, non ridisegnare."},
    ("primitivo", "font"): {"type": "fontFamily"},
    ("primitivo", "misura"): {"type": "dimension"},
    ("semantico",): {
        "description": "Il ruolo, non il valore. I componenti puntano solo ai semantici, mai ai primitivi."},
    ("semantico", "colore"): {"type": "color"},
    ("semantico", "colore", "superficie"): {
        "description": "Superfici e testo."},
    ("semantico", "colore", "navigazione"): {},
    ("semantico", "colore", "apparato"): {},
    ("semantico", "colore", "ontologia"): {},
    ("semantico", "font"): {"type": "fontFamily"},
    ("semantico", "dimensione"): {"type": "dimension"},
    ("semantico", "numero"): {"type": "number"},
    ("semantico", "struttura"): {"type": "dimension"},
}

# Ordine in cui i nodi-gruppo vengono creati (e quindi appaiono nel JSON),
# così $type/$description precedono i token che li ereditano.
GROUP_ORDER = [
    ("primitivo",),
    ("primitivo", "colore"),
    ("primitivo", "colore", "neutro"),
    ("primitivo", "colore", "blu"),
    ("primitivo", "colore", "arancio"),
    ("primitivo", "colore", "verde"),
    ("primitivo", "colore", "tratto"),
    ("primitivo", "colore", "categoria"),
    ("primitivo", "colore", "gruppo-nodo"),
    ("primitivo", "font"),
    ("primitivo", "misura"),
    ("semantico",),
    ("semantico", "colore"),
    ("semantico", "colore", "superficie"),
    ("semantico", "colore", "navigazione"),
    ("semantico", "colore", "apparato"),
    ("semantico", "colore", "ontologia"),
    ("semantico", "font"),
    ("semantico", "dimensione"),
    ("semantico", "numero"),
    ("semantico", "struttura"),
]

TOP_DESCRIPTION = (
    "Token DTCG (2025.10) generati da design-system/tokens/tokens.css, che resta "
    "la sorgente di verità — non editare questo file a mano, rigenerarlo con "
    "scripts/export_tokens.py. Rappresenta solo il tema chiaro: la spec DTCG non "
    "standardizza temi/modalità, un eventuale tema scuro sarà un secondo file."
)


def leggi_dichiarazioni_root(testo_css):
    """Estrae { nome-senza-doppio-trattino: valore-letterale } dal blocco
    :root di tokens.css, in ordine di apparizione, ignorando i commenti."""
    inizio = testo_css.index(":root")
    apertura = testo_css.index("{", inizio) + 1
    chiusura = testo_css.rindex("}")
    corpo = testo_css[apertura:chiusura]
    corpo_senza_commenti = re.sub(r"/\*.*?\*/", "", corpo, flags=re.S)

    dichiarazioni = {}
    ordine = []
    for m in re.finditer(r"--([A-Za-z0-9-]+)\s*:\s*([^;]+?)\s*;", corpo_senza_commenti):
        nome, valore = m.group(1), m.group(2).strip()
        if nome in dichiarazioni:
            raise SystemExit(f"--{nome} dichiarata più di una volta in tokens.css")
        dichiarazioni[nome] = valore
        ordine.append(nome)
    return dichiarazioni, ordine


def hex_a_colore(hex_str, alpha=1):
    hex_str = hex_str.strip()
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", hex_str):
        raise ValueError(f"valore colore inatteso: {hex_str!r}")
    hex_str = hex_str.upper()
    r = int(hex_str[1:3], 16) / 255
    g = int(hex_str[3:5], 16) / 255
    b = int(hex_str[5:7], 16) / 255
    return {
        "colorSpace": "srgb",
        "components": [round(r, 4), round(g, 4), round(b, 4)],
        "alpha": alpha,
        "hex": hex_str,
    }


def rgba_a_colore(raw):
    m = re.fullmatch(r"rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)", raw.strip())
    if not m:
        raise ValueError(f"valore rgba inatteso: {raw!r}")
    r, g, b, a = int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))
    hex_str = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return {
        "colorSpace": "srgb",
        "components": [round(r / 255, 4), round(g / 255, 4), round(b / 255, 4)],
        "alpha": a,
        "hex": hex_str,
    }


def dimensione_a_valore(raw):
    m = re.fullmatch(r"([\d.]+)(rem|px)", raw.strip())
    if not m:
        raise ValueError(f"valore dimension inatteso (unità ammesse rem/px): {raw!r}")
    numero = float(m.group(1))
    if numero == int(numero):
        numero = int(numero)
    return {"value": numero, "unit": m.group(2)}


def em_a_numero(raw):
    m = re.fullmatch(r"([\d.]+)em", raw.strip())
    if not m:
        raise ValueError(f"valore em inatteso: {raw!r}")
    return round(float(m.group(1)), 4)


def numero_a_valore(raw):
    raw = raw.strip()
    if not re.fullmatch(r"-?[\d.]+", raw):
        raise ValueError(f"valore number inatteso: {raw!r}")
    numero = float(raw)
    if numero == int(numero):
        numero = int(numero)
    return numero


def stack_font_a_lista(raw):
    pezzi = [p.strip().strip("'\"") for p in raw.split(",")]
    if not pezzi or any(not p for p in pezzi):
        raise ValueError(f"stack di font inatteso: {raw!r}")
    return pezzi


def nome_alias(raw):
    m = re.fullmatch(r"var\(--([A-Za-z0-9-]+)\)", raw.strip())
    if not m:
        raise ValueError(f"valore alias inatteso (atteso var(--nome)): {raw!r}")
    return m.group(1)


def costruisci_json(dichiarazioni):
    """Costruisce l'albero DTCG in memoria, leggendo i valori letterali da
    `dichiarazioni` (nome-css → valore-css) e validandoli contro il tipo
    dichiarato in TOKENS. Solleva SystemExit con un messaggio chiaro se un
    valore non ha la forma attesa per il suo tipo — non prova a indovinare."""

    percorso_di = {nome: gruppo + (nome,) for nome, gruppo, _tipo, _descr in TOKENS}

    # Il mapping nome-CSS <-> percorso-JSON e' invertibile solo se e' una
    # biiezione: ogni nome CSS a un solo percorso, ogni percorso a un solo
    # nome. La seconda condizione vale per costruzione (il nome e' sempre
    # l'ultimo segmento), la prima si verifica qui.
    if len(percorso_di) != len(TOKENS):
        raise SystemExit("nomi duplicati nella tabella TOKENS")
    if len(set(percorso_di.values())) != len(TOKENS):
        raise SystemExit("percorsi duplicati nella tabella TOKENS (mapping non invertibile)")

    nomi_tabella = set(percorso_di)
    nomi_css = set(dichiarazioni)
    if nomi_tabella != nomi_css:
        mancano_nel_css = nomi_tabella - nomi_css
        mancano_in_tabella = nomi_css - nomi_tabella
        msg = ["tokens.css e la tabella TOKENS sono disallineati:"]
        for n in sorted(mancano_nel_css):
            msg.append(f"  - --{n} è in TOKENS ma non più in tokens.css")
        for n in sorted(mancano_in_tabella):
            msg.append(f"  - --{n} è in tokens.css ma manca in TOKENS")
        raise SystemExit("\n".join(msg))

    radice = {"$description": TOP_DESCRIPTION}

    def nodo(percorso):
        n = radice
        for segmento in percorso:
            n = n.setdefault(segmento, {})
        return n

    for percorso in GROUP_ORDER:
        n = nodo(percorso)
        meta = GROUP_META.get(percorso, {})
        if "description" in meta:
            n["$description"] = meta["description"]
        if "type" in meta:
            n["$type"] = meta["type"]

    for nome, gruppo, tipo, descrizione in TOKENS:
        raw = dichiarazioni[nome]
        try:
            if tipo == "color-hex":
                valore = hex_a_colore(raw)
            elif tipo == "color-rgba":
                valore = rgba_a_colore(raw)
            elif tipo == "dimension":
                valore = dimensione_a_valore(raw)
            elif tipo == "fontfamily":
                valore = stack_font_a_lista(raw)
            elif tipo == "number":
                valore = numero_a_valore(raw)
            elif tipo == "number-em":
                valore = em_a_numero(raw)
            elif tipo == "alias":
                bersaglio = nome_alias(raw)
                if bersaglio not in percorso_di:
                    raise ValueError(f"alias verso --{bersaglio}, non presente in TOKENS")
                valore = "{" + ".".join(percorso_di[bersaglio]) + "}"
            else:
                raise ValueError(f"tipo sconosciuto: {tipo}")
        except ValueError as e:
            raise SystemExit(f"--{nome}: {e}")

        token = {"$value": valore, "$description": descrizione}
        if tipo == "number-em":
            # scarto dichiarato dal gruppo (dimension): questo token e'
            # un numero puro, non una dimensione - vedi TOP_DESCRIPTION/TOKENS.
            token = {"$type": "number", **token}

        n = nodo(gruppo)
        n[nome] = token

    return radice


def genera():
    testo_css = TOKENS_CSS.read_text(encoding="utf-8")
    dichiarazioni, _ordine = leggi_dichiarazioni_root(testo_css)
    albero = costruisci_json(dichiarazioni)
    return json.dumps(albero, ensure_ascii=False, indent=2) + "\n"


def diff_ricorsivo(a, b, percorso=""):
    """Elenca le differenze fra due alberi JSON già parsati, un path per riga."""
    righe = []
    if type(a) is not type(b):
        return [f"{percorso or '.'}: tipo diverso ({type(a).__name__} vs {type(b).__name__})"]
    if isinstance(a, dict):
        chiavi = sorted(set(a) | set(b))
        for k in chiavi:
            p = f"{percorso}.{k}" if percorso else k
            if k not in a:
                righe.append(f"{p}: presente solo nel file su disco")
            elif k not in b:
                righe.append(f"{p}: presente solo nella rigenerazione")
            else:
                righe.extend(diff_ricorsivo(a[k], b[k], p))
    elif a != b:
        righe.append(f"{percorso}: {a!r} (rigenerato) vs {b!r} (su disco)")
    return righe


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true",
                     help="non scrive: esce con 1 se tokens.json non corrisponde a tokens.css")
    args = ap.parse_args()

    contenuto = genera()

    if args.check:
        if not TOKENS_JSON.exists():
            print(f"{TOKENS_JSON} non esiste. Generalo con: python3 design-system/scripts/export_tokens.py",
                  file=sys.stderr)
            sys.exit(1)
        attuale = TOKENS_JSON.read_text(encoding="utf-8")
        if attuale == contenuto:
            print("tokens.json allineato a tokens.css")
            return
        print("tokens.json NON è allineato a tokens.css:", file=sys.stderr)
        try:
            atteso = json.loads(contenuto)
            trovato = json.loads(attuale)
            differenze = diff_ricorsivo(trovato, atteso)
            if differenze:
                for d in differenze:
                    print(f"  - {d}", file=sys.stderr)
            else:
                print("  - stesso contenuto JSON, ma formattazione diversa nel file su disco", file=sys.stderr)
        except json.JSONDecodeError:
            print("  - il file su disco non è JSON valido", file=sys.stderr)
        print("Rigeneralo con: python3 design-system/scripts/export_tokens.py", file=sys.stderr)
        sys.exit(1)

    TOKENS_JSON.write_text(contenuto, encoding="utf-8")
    kb = len(contenuto.encode("utf-8")) / 1024
    print(f"  scritto  {TOKENS_JSON.relative_to(RADICE.parent)}  ({kb:.0f} KB, {len(TOKENS)} token)")


if __name__ == "__main__":
    main()
