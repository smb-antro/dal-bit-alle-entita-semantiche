#!/usr/bin/env python3
"""Compila i file di src/saggio/ in un unico output/dal-bit-alle-entita-semantiche_<lingua>.html.

Il compilato e' UN SOLO file: nessun asset accanto, nessuna richiesta di rete.
Il design system arriva da design-system/css/design-system.inline.css (la
variante con i font in data-URI base64), il resto dei font e delle immagini e'
incorporato allo stesso modo.

Tre namespacing, non uno, perche' 14 pagine nate autonome finiscono nello
stesso DOM e nello stesso <style>:

  id      ogni id interno al capitolo prende il prefisso dello slug
          (`namespace_tokens`), ovunque compaia — markup, CSS, JavaScript.
  CSS     ogni selettore dello <style> del capitolo viene discendente di
          `#chapter-<slug>` (`scope_css`). Da quando il guscio comune e'
          passato al design system, in quello <style> resta solo il CSS dei
          widget — e li' i nomi si ripetono fra capitoli (`.switch`,
          `.truth-table`, `.timeline`, `.playground .ptitle`) con valori
          diversi: senza scoping vince l'ultimo capitolo concatenato, per
          tutti.
  JS      lo script del capitolo e' avvolto in una IIFE che espone
          `chapterRoot`, e le query di shell che cercano elementi del
          capitolo passano da `document.` a `chapterRoot.`
          (`scope_shell_queries`).

Uso: python3 build_output.py [--trial] [--lang it]
  --trial   compila solo i due capitoli della prova tecnica di namespacing
            (c00a: pagina singola; cm1: multi-unita' con rail+UNITS)
"""
import argparse
import base64
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

SRC_DIR = Path(__file__).parent
LEZIONI_DIR = SRC_DIR / "saggio"
OUTPUT_DIR = SRC_DIR.parent / "output"
REPO_ROOT = SRC_DIR.parent.parent
DESIGN_SYSTEM_DIR = REPO_ROOT / "design-system"
INLINE_CSS = DESIGN_SYSTEM_DIR / "css" / "design-system.inline.css"
BUILD_CSS_SCRIPT = DESIGN_SYSTEM_DIR / "scripts" / "build_css.py"

# La Lente semantica: dal 23 settembre 2026 e' un capitolo del compilato, non
# un collegamento che esce dal file.
#
# Il motivo: Safari e' sandboxed e riceve l'accesso a un file locale SOLO se
# glielo consegna il sistema — il pannello di apertura, il doppio clic,
# `open`. Qualunque ALTRO file locale, che l'utente non ha consegnato, gli e'
# negato: il clic sul rimando alla Lente non faceva semplicemente nulla. Non
# e' una regola sulle cartelle superiori (cosi' l'avevo descritta all'inizio,
# ed era sbagliato): e' per file. Che e' una ragione piu' forte, non piu'
# debole — vale per qualunque riferimento esterno, a qualunque profondita'.
# Un deliverable "un file solo" non puo' dipendere da nessun altro file.
LENTE_DIR = REPO_ROOT / "ontologia" / "lente-semantica" / "output"
LENTE_DATI = REPO_ROOT / "ontologia" / "lente-semantica" / "src" / "grafo.js"
LENTE_SLUG = "lente"
LENTE_TITOLO = "Lente semantica"
LENTE_PARTE = "Strumenti"

# (file, slug, etichetta barra capitoli, kind: 'intro' | 'single' | 'multi', titolo indice)
#
# `presentazione.html` e `dietro-i-widget.html` sono capitoli come gli altri:
# la prima non e' piu' prosa ricopiata a mano qui dentro, la seconda non e'
# piu' un file copiato accanto al bundle. Il compilato torna a essere un
# file solo.
CHAPTERS = [
    ("presentazione.html", "intro", "P", "intro", "Presentazione"),
    ("fondamenti-1-funzioni-booleane.html", "c00a", "F1", "single", "1. Funzioni booleane"),
    ("fondamenti-2-hardware-software.html", "c00b", "F2", "single", "2. Hardware e software"),
    ("genealogia-1-disputa.html", "cba", "G1", "multi", "1. La storia come sequenza di problemi irrisolti"),
    ("genealogia-2-limiti.html", "cbb", "G2", "multi", "2. I limiti attuali"),
    ("genealogia-3-villaggio.html", "cbc", "G3", "multi", "3. Perché ci vuole un villaggio"),
    ("genealogia-4-corpo.html", "cbd", "G4", "multi", "4. Lo spazio, il corpo, la macchina"),
    ("meccanismo-1-testo-come-dato.html", "cm1", "M1", "multi", "1. Il testo come dato"),
    ("meccanismo-2-probabilita.html", "cm2", "M2", "multi", "2. Probabilità e linguaggio"),
    ("meccanismo-3-embedding.html", "cm3", "M3", "multi", "3. Parole come punti nello spazio"),
    ("meccanismo-4-reti-neurali.html", "cm4", "M4", "multi", "4. Reti neurali"),
    ("meccanismo-5-transformer.html", "cm5", "M5", "multi", "5. Il Transformer"),
    ("meccanismo-6-large.html", "cm6", "M6", "multi", "6. Cosa significa \"Large\""),
    ("dietro-i-widget.html", "capp", "A", "multi", "Dietro i widget"),
]

INTRO_SLUG = "intro"

# Il binario di navigazione e' identico in tutti e 14 i file sorgente a meno
# dei marcatori statici del file corrente — tranne in presentazione.html, che
# espande la propria voce in un elenco con scroll-spy invece di tenerla
# chiusa. Nel compilato la voce corrente e' dinamica, quindi la sorgente
# della sidebar condivisa e' la forma "vista da un altro capitolo".
SIDEBAR_SOURCE = "fondamenti-1-funzioni-booleane.html"

# Raggruppamento in Parti per il Sommario (non usato da extract_chapter,
# solo per la costruzione del Sommario gerarchico in build_sommario).
PARTI = [
    ("Parte I — Fondamenti", ["c00a", "c00b"]),
    ("Parte II — Genealogia", ["cba", "cbb", "cbc", "cbd"]),
    ("Parte III — Meccanismo", ["cm1", "cm2", "cm3", "cm4", "cm5", "cm6"]),
    ("Appendice", ["capp"]),
    (LENTE_PARTE, [LENTE_SLUG]),
]

# Titoli delle unità interne di ciascun capitolo multi-unità, per mostrarli nel
# Sommario sotto il titolo del modulo (presi da vocabolario-ontologia-llm/src/dati.ttl,
# non reinventati).
UNIT_TITLES = {
    "cba": [
        "Il sogno di Leibniz / Boole / Frege–Russell–Principia",
        "Gödel rompe tutto / Turing / Lucas",
        "Dartmouth / il Perceptron / Minsky e Papert",
        "Sistemi esperti / il secondo inverno / la rivincita statistica",
        "Backpropagation / deep learning / Word2Vec",
        "L'attenzione e il salto finale",
    ],
    "cbb": ["Cosa sanno fare davvero", "Cosa simulano di saper fare", "Cosa non sanno fare affatto"],
    "cbc": [
        "Il problema del significato",
        "Il problema della causalità",
        "Il problema biologico",
        "Il problema della coscienza",
        "Cosa siamo, per contrasto",
    ],
    "cbd": ["Cos'è lo spazio? Il corpo come strumento di misura", "Il corpo mancante"],
    "cm1": ["Encoding", "Tokenizzazione", "Problema del vocabolario", "Dagli ID al punto più discreto", "Gödel"],
    "cm2": [
        "Prevedere la parola successiva",
        "Unigrammi/bigrammi, induzione, calibrazione",
        "N-grammi e assunzione di Markov",
        "Sparsità e dipendenze lontane",
    ],
    "cm3": [
        "Il problema lasciato aperto",
        "Le parole come vettori (embedding)",
        "L'ipotesi distribuzionale",
        "L'aritmetica vettoriale",
        "Polisemia ed embedding statico",
    ],
    "cm4": [
        "Dal neurone biologico al neurone artificiale",
        "Il perceptron e XOR",
        "Strati e profondità",
        "La funzione di perdita",
        "Il gradiente e la backpropagation",
    ],
    "cm5": [
        "Il problema che l'attenzione risolve",
        "L'idea dell'attention",
        "Query, Key, Value",
        "Embedding contestuale",
        "Multi-head e posizione",
        "Parallelismo e scala",
    ],
    "cm6": [
        "Scala",
        "Capacità emergenti",
        "I dati",
        "Fine-tuning",
        "RLHF",
        "Quantizzazione (chiusura dell'arco tecnico)",
    ],
    "capp": [
        "Il tokenizzatore (Meccanismo · 1)",
        "Il predittore n-grammi (Meccanismo · 2)",
        "La mappa embedding (Meccanismo · 3)",
        "Neurone, XOR, superficie di perdita (Meccanismo · 4)",
        "L'attention (Meccanismo · 5)",
        "Scala e capacità (Meccanismo · 6)",
    ],
}

TRIAL_SLUGS = {"c00a", "cm1"}

ID_ATTR_RE = re.compile(r'id="([a-zA-Z0-9_-]+)"')
STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)
SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)
BODY_RE = re.compile(r"<body>(.*?)</body>", re.S)
SIDEBAR_RE = re.compile(r'\s*<nav class="sidebar".*?</nav>\n?', re.S)
SIDEBAR_HREF_RE = re.compile(r'href="([a-z0-9-]+\.html)(#[a-zA-Z0-9_-]+)?"')
BODY_HREF_RE = re.compile(r'href="([a-z0-9-]+\.html)(#[a-zA-Z0-9_-]+)?"')

# I sorgenti vivono in dominio/src/saggio/, il compilato in dominio/output/:
# un livello in meno da risalire per arrivare alla radice del repository.
FUORI_ALBERO = ("../../../", "../../")


CLASS_ATTR_RE = re.compile(r'class="[^"]*"|class=\'[^\']*\'')


def namespace_tokens(text, slug, ids):
    """Prefissa ogni id noto con `{slug}-` ovunque compaia come token esatto
    tra apici (id="X", getElementById('X'), id:'X'/inputId:'X'/barsId:'X' nei
    widget a config-object, data-target="X", argomenti posizionali passati a
    funzioni come setLight('outAND', ...), ecc.) o come selettore CSS `#X`
    incorporato in una stringa piu' ampia (es. querySelectorAll('#X .foo')).

    Un elenco chiuso di contesti noti si e' rivelato incompleto (il
    codebase referenzia gli id in troppe forme sintattiche diverse per
    elencarle tutte): l'unico contesto realmente pericoloso e' `class="..."`,
    dove alcuni elementi riusano deliberatamente lo stesso nome come id e
    come classe CSS — quello va protetto esplicitamente, il resto va
    sostituito ovunque."""
    masked = []

    def mask(m):
        masked.append(m.group(0))
        return f"\x00CLASSMASK{len(masked) - 1}\x00"

    text = CLASS_ATTR_RE.sub(mask, text)

    for id_value in sorted(ids, key=len, reverse=True):
        escaped = re.escape(id_value)
        quoted = re.compile(r'(?<=["\'])' + escaped + r'(?=["\'])')
        text = quoted.sub(f"{slug}-{id_value}", text)
        hashref = re.compile(r"(#)" + escaped + r"(?![a-zA-Z0-9_-])")
        text = hashref.sub(lambda m: m.group(1) + slug + "-" + id_value, text)

    for i, original in enumerate(masked):
        text = text.replace(f"\x00CLASSMASK{i}\x00", original)
    return text


# ---------------------------------------------------------------------------
# Scoping del CSS di capitolo
# ---------------------------------------------------------------------------
#
# Finche' ogni pagina ricopiava nel proprio <style> l'intero guscio condiviso
# (4.539 righe), i selettori che si ripetevano fra capitoli erano identici e
# concatenarli non cambiava nulla. Dal passaggio al design system nello
# <style> resta solo il CSS dei widget (1.250 righe) e li' gli stessi nomi
# significano cose diverse: `.switch` e' 84x42 in Fondamenti 1 e 90x44 in
# Fondamenti 2, `.truth-table` ha due scale di corpo, `.tl-*` due, e
# `presentazione.html` — che da oggi e' un capitolo — dichiara un nudo
# `section{ padding: 96px 0 88px; border-bottom: ... }` che senza scoping
# colpirebbe ogni <section> del documento, `.chapter` compreso.
#
# Ogni selettore diventa quindi discendente del contenitore del capitolo.
# Lo <style> dei capitoli resta non stratificato, quindi continua a vincere
# sul design system senza alzare la specificita' contro di esso; il prefisso
# aggiunge lo stesso id a tutte le regole di un capitolo, quindi il loro
# ordine reciproco non cambia.


def _skip_comment(css, i):
    end = css.find("*/", i + 2)
    return len(css) if end == -1 else end + 2


def _skip_string(css, i):
    quote = css[i]
    j = i + 1
    while j < len(css):
        if css[j] == "\\":
            j += 2
            continue
        if css[j] == quote:
            return j + 1
        j += 1
    return j


def _match_brace(css, i):
    """Indice della `}` che chiude la `{` in posizione i."""
    depth = 0
    j = i
    while j < len(css):
        c = css[j]
        if c == "/" and css[j:j + 2] == "/*":
            j = _skip_comment(css, j)
            continue
        if c in "\"'":
            j = _skip_string(css, j)
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return j
        j += 1
    raise ValueError("CSS del capitolo: graffa non chiusa")


def _split_selector_list(prelude):
    parts, buf, depth, i = [], [], 0, 0
    while i < len(prelude):
        c = prelude[i]
        if c == "/" and prelude[i:i + 2] == "/*":
            j = _skip_comment(prelude, i)
            buf.append(prelude[i:j])
            i = j
            continue
        if c in "\"'":
            j = _skip_string(prelude, i)
            buf.append(prelude[i:j])
            i = j
            continue
        if c in "([":
            depth += 1
        elif c in ")]":
            depth -= 1
        elif c == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    parts.append("".join(buf))
    return parts


# At-rule condizionali: il corpo contiene altre regole, va percorso.
AT_RULES_CON_REGOLE = {"media", "supports", "container", "layer", "scope"}


def scope_css(css, scope):
    """Rende ogni selettore di `css` discendente di `scope`.

    Ricorre dentro @media/@supports/@container; lascia intatto il corpo di
    @keyframes (dove `0%`/`from` non sono selettori) e di @font-face."""
    out, buf, i = [], [], 0
    while i < len(css):
        c = css[i]
        if c == "/" and css[i:i + 2] == "/*":
            j = _skip_comment(css, i)
            buf.append(css[i:j])
            i = j
            continue
        if c in "\"'":
            j = _skip_string(css, i)
            buf.append(css[i:j])
            i = j
            continue
        if c == "{":
            prelude = "".join(buf)
            buf = []
            close = _match_brace(css, i)
            body = css[i + 1:close]
            stripped = prelude.lstrip()
            if stripped.startswith("@"):
                name = re.match(r"@([\w-]+)", stripped).group(1).lower()
                if name in AT_RULES_CON_REGOLE:
                    out.append(prelude + "{" + scope_css(body, scope) + "}")
                else:
                    out.append(prelude + "{" + body + "}")
            else:
                selectors = []
                for part in _split_selector_list(prelude):
                    bare = part.strip()
                    selectors.append(f"{scope} {bare}" if bare else part)
                out.append(",\n".join(selectors) + "{" + body + "}")
            i = close + 1
            continue
        if c == ";" and "".join(buf).lstrip().startswith("@"):
            out.append("".join(buf) + ";")
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    out.append("".join(buf))
    return "".join(out)


ASSET_SRC_RE = re.compile(r'src="([^"]*)"')


def inline_relative_assets(markup, filename):
    """Incorpora come data: URI gli asset referenziati con un percorso
    relativo (es. src="immagini_modulo1/foo.png") — nel file sorgente sono
    relativi alla cartella saggio/, ma il file compilato vive in output/,
    quindi lo stesso percorso relativo non risolverebbe piu' allo stesso file."""

    def replace(m):
        src = m.group(1)
        # src="" e' un segnaposto riempito dal JavaScript (la <img> della
        # lightbox di presentazione.html): non e' un asset da incorporare.
        if not src or src.startswith(("data:", "http://", "https://", "//", "#")):
            return m.group(0)
        asset_path = LEZIONI_DIR / src
        if not asset_path.is_file():
            raise ValueError(f"{filename}: asset referenziato non trovato: {src}")
        mime, _ = mimetypes.guess_type(asset_path.name)
        encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
        return f'src="data:{mime};base64,{encoded}"'

    return ASSET_SRC_RE.sub(replace, markup)


def rewrite_body_links(markup, filename, slug_by_file):
    """Riscrive i rimandi da capitolo a capitolo che stanno nel corpo del
    testo (non nel binario: quello lo fa build_shared_sidebar) in modo che
    passino da showChapter invece di navigare a un file che accanto al
    compilato non esiste. Due casi oggi: la nota di chiusura di
    presentazione.html verso Fondamenti 1, e un rimando di Fondamenti 1
    dentro Meccanismo 4.

    Va chiamata PRIMA di namespace_tokens: il frammento `#u3-sez-mlp` che
    compare qui appartiene al capitolo di destinazione, non a questo, e il
    namespacing lo prefisserebbe con lo slug sbagliato se per caso i due
    file usassero lo stesso id."""

    def rewrite(m):
        file, frag = m.group(1), m.group(2)
        slug = slug_by_file.get(file)
        if slug is None:
            return m.group(0)
        target = f"{slug}-{frag[1:]}" if frag else f"chapter-{slug}"
        return f'href="#{target}" data-nav-chapter="{slug}"'

    return BODY_HREF_RE.sub(rewrite, markup)


def scope_shell_queries(script, kind, slug):
    """Riscrive le query di navigazione condivisa da `document.` a `chapterRoot.`
    Sostituzioni su stringhe esatte: il JavaScript dei sorgenti non va
    riformattato, o queste smettono di agganciare.

    Attenzione: girano DOPO namespace_tokens, quindi i selettori con id sono
    gia' prefissati — per questo le stringhe che ne contengono uno sono
    costruite con lo slug.

    La tenda dei concetti e il suo velo restano volutamente su `document`:
    sono la stessa superficie condivisa in ogni capitolo, e il listener di
    apertura e' delegato sul documento intero."""
    if kind == "multi":
        requirements = [
            [("const reveals = document.querySelectorAll('.reveal');",
              "const reveals = chapterRoot.querySelectorAll('.reveal');")],
            [("const unitBlocksForSpy = document.querySelectorAll('.unit-block');",
              "const unitBlocksForSpy = chapterRoot.querySelectorAll('.unit-block');")],
        ]
    elif kind == "intro":
        # presentazione.html: il fade-in come tutti gli altri, piu' il suo
        # scroll-spy locale, che cerca due cose diverse — le voci nel binario
        # (che nel compilato e' condiviso, quindi fuori dal capitolo: scopata
        # qui, la query non trova nulla e lo spy locale resta inerte, come
        # gia' accade per `#local-scrollspy` negli altri 11 capitoli) e le
        # quattro <section> delle Parti, che sono dentro il capitolo e
        # senza scoping verrebbero cercate in tutto il documento.
        requirements = [
            [("const reveals = document.querySelectorAll('.reveal');",
              "const reveals = chapterRoot.querySelectorAll('.reveal');")],
            [(f"const spyLinks = document.querySelectorAll('#{slug}-presentazione-scrollspy a[data-spy-target]');",
              f"const spyLinks = chapterRoot.querySelectorAll('#{slug}-presentazione-scrollspy a[data-spy-target]');")],
            [(f"const spySections = document.querySelectorAll('#{slug}-parte-1, #{slug}-parte-2, #{slug}-parte-3, #{slug}-parte-4');",
              f"const spySections = chapterRoot.querySelectorAll('#{slug}-parte-1, #{slug}-parte-2, #{slug}-parte-3, #{slug}-parte-4');")],
        ]
    else:  # single (Fondamenti 1/2): solo il fade-in, nessuno scroll-spy
        requirements = [
            [("const reveals = document.querySelectorAll('.reveal');",
              "const reveals = chapterRoot.querySelectorAll('.reveal');")],
        ]
    missing = []
    for variants in requirements:
        for old, new in variants:
            if old in script:
                script = script.replace(old, new, 1)
                break
        else:
            missing.append(variants[0][0])

    # Query opzionali: selettori di classe bare, non ancorati a un id univoco,
    # usati da widget presenti solo in alcuni file (non tutti, quindi non
    # nella lista `requirements` sopra, che e' un requisito per ogni file del
    # kind). Vanno scopate se presenti, senza errore se assenti.
    optional = [
        ("document.querySelectorAll('.pg-example-btn')",
         "chapterRoot.querySelectorAll('.pg-example-btn')"),
        ("document.querySelectorAll('.neuron-examples .pg-example-btn')",
         "chapterRoot.querySelectorAll('.neuron-examples .pg-example-btn')"),
        # trovato nell'audit di stasera: selettore di classe non scopato nel
        # widget di quantizzazione (Meccanismo 6) — stessa famiglia dei bug
        # scroll-spy gia' corretti, funzionava solo per il fatto che nessun
        # altro capitolo usa questa classe.
        ("document.querySelectorAll('.quant-level-btn')",
         "chapterRoot.querySelectorAll('.quant-level-btn')"),
        # stessa famiglia: la scala di astrazione di Fondamenti 2.
        ("document.querySelectorAll('.ladder-item')",
         "chapterRoot.querySelectorAll('.ladder-item')"),
    ]
    for old, new in optional:
        script = script.replace(old, new)

    return script, missing


LENTE_HREF_RE = re.compile(r'href="(?:\.\./)+ontologia/lente-semantica/output/index\.html(#\$\{id\})?"')
LENTE_JS_RE = re.compile(
    r'tendaLinkLente\.href = `(?:\.\./)+ontologia/lente-semantica/output/index\.html#\$\{id\}`;'
)
TENDA_LENTE_A_RE = re.compile(r'(<a class="tenda-lente"[^>]*?)\s+target="_blank" rel="noopener"')


def rewrite_lente_links(markup):
    """Nel compilato la Lente e' un capitolo, non un file accanto: i rimandi
    ci arrivano con showChapter. Si toglie anche `target="_blank"`, che qui
    aprirebbe una seconda copia dello stesso file da 2 MB."""
    markup = LENTE_HREF_RE.sub('href="#chapter-' + LENTE_SLUG + '" data-nav-chapter="' + LENTE_SLUG + '"', markup)
    return TENDA_LENTE_A_RE.sub(r"\1", markup)


def rewrite_lente_script(script):
    """L'unica riga del JS dei capitoli che punta alla Lente. Sostituzione su
    stringa esatta, come le altre di `scope_shell_queries`: il JavaScript dei
    capitoli non si riformatta. Il nodo da centrare viaggia in `data-nodo`,
    e il guscio lo passa a window.lenteSeleziona dopo aver mostrato il
    capitolo (vedi NAV_CONTROLLER)."""
    return LENTE_JS_RE.sub(
        "tendaLinkLente.href = '#chapter-" + LENTE_SLUG + "';\n"
        "    tendaLinkLente.setAttribute('data-nav-chapter', '" + LENTE_SLUG + "');\n"
        "    tendaLinkLente.setAttribute('data-nodo', id);",
        script,
    )


def extract_lente():
    """La Lente semantica come capitolo del compilato.

    Non passa da `extract_chapter`: non viene da saggio/, non ha una sidebar
    da togliere ne' query di guscio da riscopare, e i suoi id non vanno
    prefissati — verificato che nessuno dei nove (`svg-grafo`, `ricerca`,
    `lista-nodi`, `breadcrumb-nodo`, `badge-relazione`, `legenda`,
    `glossario-relazioni`, `btn-grado-1`, `btn-grado-2`) collide con un id
    del resto del compilato. Il prefisso costringerebbe a riscrivere
    `lente.js`, che li cerca per nome: non prefissarli e' piu' sicuro, non
    meno.

    Il suo JavaScript non misura mai il layout reale (nessun
    getBoundingClientRect, nessun clientWidth: il grafo e' disegnato in
    coordinate `viewBox`), quindi puo' inizializzarsi mentre il capitolo e'
    ancora `hidden` — che e' la condizione in cui si trova al caricamento."""
    index = (LENTE_DIR / "index.html").read_text(encoding="utf-8")
    m = re.search(r"<body>(.*?)<script", index, re.S)
    if not m:
        raise ValueError("lente/index.html: struttura body/script non riconosciuta")
    markup = m.group(1)

    # Le briciole portano alla home dell'ontologia, che nel compilato non
    # esiste: era il secondo collegamento verso l'esterno.
    markup, n = re.subn(r'\s*<nav class="briciole-root">.*?</nav>', "", markup, flags=re.S)
    if n != 1:
        raise ValueError(f"lente: attese 1 briciole-root, trovate {n}")

    style = scope_css((LENTE_DIR / "lente.css").read_text(encoding="utf-8"), f"#chapter-{LENTE_SLUG}")

    # Due conti da rifare, perche' nella pagina a se' la Lente vive da sola e
    # qui vive dentro il saggio. Misurati guardando la resa, non previsti:
    #
    # 1. Sopra i 900px il binario del saggio e' fisso a sinistra e il
    #    contenuto gli lascia spazio con `main{ padding-left: --misura-rail }`.
    #    La Lente non ha un <main> che avvolga tutta la pagina, quindi partiva
    #    da x=0, sotto il binario.
    # 2. Peggio: il <main class="pannello-grafo"> che la Lente ha DENTRO di se'
    #    quel padding lo prendeva — il riquadro del grafo si spostava di 300px
    #    dentro un contenitore che non si era allargato, e l'elenco dei nodi
    #    restava senza etichette.
    #
    # Non si tocca `layout.css`: la regola e' giusta per il saggio. Si
    # correggono qui i due effetti, dentro il capitolo, dove il CSS non e'
    # stratificato e quindi vince senza alzare la specificita'.
    style += (
        f"\n@media (min-width: 900px){{\n"
        f"  #chapter-{LENTE_SLUG}{{ padding-left: var(--misura-rail); }}\n"
        f"  #chapter-{LENTE_SLUG} main.pannello-grafo{{ padding-left: 0; }}\n"
        f"}}\n"
    )

    wrapped_markup = (
        f'<section class="chapter" id="chapter-{LENTE_SLUG}" data-chapter="{LENTE_SLUG}" '
        f'data-kind="lente" hidden>\n{markup}\n</section>'
    )

    # Tre script separati e nell'ordine originale, non concatenati nel blocco
    # degli altri capitoli: grafo.js dichiara GRAFO, d3 e' un UMD che si
    # aggancia a window, lente.js presuppone entrambi. Tenerli come li ha
    # scritti chi li ha scritti costa tre tag e toglie una classe intera di
    # sorprese.
    scripts = [
        "window.LENTE_INCORPORATA = true;",
        LENTE_DATI.read_text(encoding="utf-8"),
        (LENTE_DIR / "vendor" / "d3.v7.min.js").read_text(encoding="utf-8"),
        (LENTE_DIR / "lente.js").read_text(encoding="utf-8"),
    ]
    return style, wrapped_markup, scripts


def extract_chapter(filename, slug, kind, slug_by_file):
    raw = (LEZIONI_DIR / filename).read_text(encoding="utf-8")

    style_m = STYLE_RE.search(raw)
    body_m = BODY_RE.search(raw)
    script_m = SCRIPT_RE.search(raw)
    if not (body_m and script_m):
        raise ValueError(f"{filename}: struttura body/script non riconosciuta")

    # Un capitolo senza <style> e' legittimo: genealogia-4-corpo.html era la
    # pagina piu' pura del saggio — tutto il suo CSS era guscio condiviso, ed
    # e' finito nel design system. Zero righe rimaste, nessun <style>.
    style = style_m.group(1) if style_m else ""
    body = body_m.group(1)
    script = script_m.group(1)

    # il markup del capitolo e' il body meno lo <script> (gia' estratto separatamente)
    markup = body[: body.index("<script>")] if "<script>" in body else body
    # la sidebar del file sorgente viene rimossa qui: nel compilato ce n'e' una
    # sola condivisa (vedi build_shared_sidebar), non una copia per capitolo
    markup = SIDEBAR_RE.sub("", markup, count=1)
    markup = rewrite_body_links(markup, filename, slug_by_file)
    markup = rewrite_lente_links(markup)
    markup = inline_relative_assets(markup, filename)
    markup = markup.replace(*FUORI_ALBERO)

    # Prima del namespacing: la riga tocca `${id}`, che e' una variabile del
    # JavaScript e non un id di elemento, e non ha niente da guadagnare a
    # passare di li'.
    script = rewrite_lente_script(script)

    ids = set(ID_ATTR_RE.findall(raw))

    style = namespace_tokens(style, slug, ids)
    markup = namespace_tokens(markup, slug, ids)
    script = namespace_tokens(script, slug, ids)
    script = script.replace(*FUORI_ALBERO)

    style = scope_css(style, f"#chapter-{slug}")

    script, missing = scope_shell_queries(script, kind, slug)
    if missing:
        raise ValueError(f"{filename}: pattern di scoping non trovati: {missing}")

    wrapped_markup = (
        f'<section class="chapter" id="chapter-{slug}" data-chapter="{slug}" '
        f'data-kind="{kind}" hidden>\n{markup}\n</section>'
    )
    wrapped_script = (
        f"(function(){{\n"
        f"  const chapterRoot = document.getElementById('chapter-{slug}');\n"
        f"{script}\n"
        f"}})();"
    )
    return style, wrapped_markup, wrapped_script


def build_shared_sidebar(slug_by_file):
    """Costruisce un'unica sidebar condivisa per l'intero documento compilato,
    riscrivendo gli href della sidebar sorgente in modo che passino da
    showChapter() invece che navigare a un file separato. Lo stato "corrente"
    e lo scroll-spy diventano dinamici via JS (vedi NAV_CONTROLLER), non piu'
    marcati staticamente per file.

    Da quando presentazione.html e dietro-i-widget.html sono capitoli come
    gli altri, i loro rami speciali sono spariti: una regola sola, uguale per
    tutte e 14 le voci, che e' anche l'unica coerente con extract_chapter —
    che prefissa ogni id con lo slug del suo capitolo."""
    raw = (LEZIONI_DIR / SIDEBAR_SOURCE).read_text(encoding="utf-8")
    sidebar_m = SIDEBAR_RE.search(raw)
    if not sidebar_m:
        raise ValueError("sidebar sorgente non trovata per costruire la sidebar condivisa")
    sidebar = sidebar_m.group(0).strip()
    sidebar = sidebar.replace('<nav class="sidebar"', '<nav class="sidebar" id="master-sidebar"', 1)
    sidebar = sidebar.replace(' current', "")
    sidebar = sidebar.replace('<details class="modulo" open>', '<details class="modulo">')
    # nel compilato qualunque parte puo' diventare quella "corrente" (navigazione
    # dinamica via showChapter), non solo quella che era current nel file sorgente
    # da cui questa sidebar e' estratta: la classe scrollspy - che aggancia il CSS
    # del pallino luminoso (.unita-list.scrollspy a.active) - va quindi su ogni
    # unita-list, non solo su quella che il file sorgente marcava come tale. Prima
    # veniva rimossa (pensando fosse solo uno stato statico da azzerare): risultato,
    # .active veniva sempre applicato correttamente dal JS ma senza scrollspy sul
    # contenitore quella classe non agganciava alcuna regola CSS - nessun pallino
    # visibile, mai. Bug verificato dal vivo (class="active" presente, zero effetto).
    sidebar = re.sub(r'class="unita-list(?: scrollspy)?"', 'class="unita-list scrollspy"', sidebar)
    sidebar = sidebar.replace(' id="local-scrollspy"', "").replace(' id="presentazione-scrollspy"', "")

    def rewrite(m):
        file, frag = m.group(1), m.group(2)
        slug = slug_by_file.get(file)
        if slug is None:
            raise ValueError(f"sidebar: voce verso un file che non e' un capitolo compilato: {file}")
        target = f"{slug}-{frag[1:]}" if frag else f"chapter-{slug}"
        spy = f' data-spy-target="{target}"' if frag else ""
        return f'href="#{target}" data-nav-chapter="{slug}"{spy}'

    sidebar = SIDEBAR_HREF_RE.sub(rewrite, sidebar)

    # La voce della Lente si aggiunge DOPO la riscrittura: `rewrite` solleva
    # eccezione su un href che non corrisponde a un file di saggio/, ed e'
    # giusto che lo faccia — questa voce non ne ha uno.
    voce = (
        '\n  <div class="parte">\n'
        f'    <div class="parte-heading">{LENTE_PARTE}</div>\n'
        f'    <a class="voce-semplice" href="#chapter-{LENTE_SLUG}" '
        f'data-nav-chapter="{LENTE_SLUG}">{LENTE_TITOLO}</a>\n'
        '  </div>\n'
    )
    return sidebar.replace("</nav>", voce + "</nav>", 1)


NEW_CSS = """
  /* ============ compilato: quel che esiste solo qui ============ */
  /* Tutto con i token del design system. Niente tema: il saggio ha una
     sola resa, quella chiara, e il commutatore con localStorage che stava
     qui e' stato tolto insieme al blocco :root[data-theme="light"]. */

  .chapter[hidden]{ display:none; }

  /* ---------- Sommario ----------
     L'unico pezzo di interfaccia che nasce nel compilato e non esiste in
     nessuna pagina sorgente: il binario porta a un'unita' alla volta, il
     Sommario da' la mappa intera. Stessa famiglia del resto (una sola nel
     sistema), apparato in maiuscoletto e non in un secondo font, arancio
     perche' e' apparato e non navigazione — il blu resta al binario. */
  .sommario h2{
    font-size: var(--dim-lede);
    font-variant: small-caps; letter-spacing: var(--traccia-apparato);
    color: var(--colore-apparato);
    margin-bottom: 24px;
  }
  .sommario-parte{ margin-bottom: 26px; }
  .sommario-parte:last-child{ margin-bottom: 0; }
  .sommario-parte-heading{
    font-variant: small-caps; letter-spacing: var(--traccia-apparato);
    font-size: var(--dim-apparato); color: var(--colore-testo-tenue);
    padding-bottom: 8px; margin-bottom: 12px;
    border-bottom: 1px solid var(--colore-bordo);
  }
  .sommario-list{ display:flex; flex-direction:column; gap: 10px; }
  .sommario-entry{ display:flex; flex-direction:column; }
  .sommario-item{
    text-align: left;
    font-family: var(--font-testo); font-size: var(--dim-testo);
    line-height: var(--interlinea-testo);
    color: var(--colore-testo);
    background: var(--colore-superficie);
    border: 1px solid var(--colore-bordo); border-radius: 6px;
    padding: 12px 16px; cursor: pointer;
    transition: border-color .2s ease, color .2s ease;
  }
  .sommario-item:hover{ border-color: var(--colore-apparato-medio); color: var(--colore-apparato); }
  .sommario-item:focus-visible{ outline: 2px solid var(--colore-apparato); outline-offset: 2px; }
  .sommario-unita{
    font-size: var(--dim-nota); color: var(--colore-testo-tenue);
    padding: 8px 16px 2px;
  }
"""


def build_sommario():
    """Il Sommario gerarchico: Parti, capitoli, e sotto ciascun capitolo
    multi-unita' i titoli delle sue unita'. Viene innestato dentro il
    capitolo `intro` (vedi build), non piu' accompagnato da prosa ricopiata
    a mano: la prosa dell'introduzione e' presentazione.html, che ora e' un
    capitolo estratto come tutti gli altri."""
    by_slug = {slug: (label, title) for _, slug, label, _, title in CHAPTERS}
    # La Lente non viene da saggio/: non e' in CHAPTERS, ma nel Sommario e'
    # una voce come le altre.
    by_slug[LENTE_SLUG] = ("L", LENTE_TITOLO)

    def build_parte(heading, slugs):
        entries = []
        for slug in slugs:
            _, title = by_slug[slug]
            units = UNIT_TITLES.get(slug)
            units_html = (
                f'<div class="sommario-unita">{" · ".join(units)}</div>' if units else ""
            )
            entries.append(
                f'<div class="sommario-entry">'
                f'<button class="sommario-item" type="button" '
                f'onclick="window.showChapter(\'{slug}\')">{title}</button>'
                f'{units_html}'
                f'</div>'
            )
        return (
            f'<div class="sommario-parte">'
            f'<div class="sommario-parte-heading">{heading}</div>'
            f'<div class="sommario-list">{"".join(entries)}</div>'
            f'</div>'
        )

    parti = "\n      ".join(build_parte(heading, slugs) for heading, slugs in PARTI)
    return (
        '  <section id="sommario" class="sommario">\n'
        '    <div class="wrap">\n'
        '      <h2>Sommario</h2>\n'
        f'      {parti}\n'
        '    </div>\n'
        '  </section>\n'
    )


def innesta_sommario(markup, slug):
    """Inserisce il Sommario nel capitolo intro, prima della nota di
    chiusura (che rimanda al capitolo successivo: la mappa viene prima
    dell'indicazione di dove andare)."""
    sommario = build_sommario()
    ancora = f'<section id="{slug}-chiusura"'
    if ancora in markup:
        return markup.replace(ancora, sommario + "\n  " + ancora, 1)
    if "</main>" in markup:
        return markup.replace("</main>", sommario + "</main>", 1)
    raise ValueError("capitolo intro: nessun punto dove innestare il Sommario")


NAV_CONTROLLER = """
(function(){
  const chapters = document.querySelectorAll('.chapter');
  const sidebar = document.getElementById('master-sidebar');
  const sidebarModules = sidebar.querySelectorAll('details.modulo');
  const sidebarSimple = sidebar.querySelectorAll('.voce-semplice');

  // Esegue uno spostamento di scroll SENZA animazione, qualunque cosa dica il
  // CSS. Serve perche' il design system dichiara `html{ scroll-behavior:
  // smooth }`: con quella regola attiva ogni scrollTo/scrollBy programmatico
  // diventa un'animazione, e ogni nuova chiamata ANNULLA quella in corso
  // ricalcolando il bersaglio dalla posizione del momento.
  //
  // Era il difetto che faceva "saltare" la pagina cambiando capitolo dal
  // Sommario: showChapter chiedeva di tornare in cima, e i due scrollBy del
  // nudge — partiti un istante dopo — cancellavano quel viaggio ripuntando a
  // "dove sono adesso ±1". Misurato: partendo da 3000px si finiva a 2998,
  // cioe' in mezzo al capitolo nuovo invece che al suo inizio.
  //
  // Si agisce sulla proprieta' CSS e non su `behavior: 'instant'` perche'
  // quel valore dell'enum e' arrivato tardi in alcuni browser e una stringa
  // non riconosciuta fa eccezione invece di degradare.
  function senzaAnimazione(azione){
    const html = document.documentElement;
    const prima = html.style.scrollBehavior;
    html.style.scrollBehavior = 'auto';
    // Il reflow forzato NON e' superstizione: senza, il motore risolve il
    // `behavior: auto` della chiamata leggendo lo stile calcolato ancora
    // vecchio, e lo spostamento parte animato lo stesso. Misurato sui quattro
    // modi possibili: stile inline senza reflow -> scrollY invariato subito
    // dopo la chiamata (animazione in corso); con reflow -> gia' a
    // destinazione. Vedi decision-log del 23 settembre.
    void html.offsetHeight;
    try { azione(); } finally { html.style.scrollBehavior = prima; }
  }

  function nudgeIntersectionObservers(){
    // Gli IntersectionObserver di ciascun capitolo (fade-in .reveal) e quello
    // globale di scroll-spy vengono creati mentre il capitolo e' ancora
    // hidden: il passaggio a display:block non basta da solo a far scattare
    // il loro ricalcolo in questo motore di rendering. Un piccolo delta di
    // scroll reale (anche se il documento e' gia' a scrollY 0) forza il
    // ricalcolo dell'intersezione in modo affidabile.
    senzaAnimazione(() => { window.scrollBy(0, 1); window.scrollBy(0, -1); });
  }

  function updateSidebarState(id){
    // Il pallino dello scroll-spy si spegne al cambio di capitolo, non a ogni
    // scorrimento: `updateActive` lascia l'ultimo acceso quando non trova un
    // bersaglio in vista — giusto mentre si scorre fra due unita', sbagliato
    // quando si e' cambiato capitolo. Senza questa riga, andando su un
    // capitolo senza unita' (Fondamenti, per esempio) restava acceso il
    // pallino di un'unita' di un ALTRO capitolo, nascosto dentro il suo
    // accordion chiuso finche' non lo si riapriva. Chi riaccende quello
    // giusto e' `updateActive`, che parte subito dopo su corso:chapterchange.
    sidebar.querySelectorAll('a.active').forEach(a => a.classList.remove('active'));
    sidebarSimple.forEach(a => a.classList.toggle('current', a.dataset.navChapter === id));
    sidebarModules.forEach(d => {
      const belongs = !!d.querySelector('a[data-nav-chapter="' + id + '"]');
      d.open = belongs;
      const summary = d.querySelector('summary');
      if(summary) summary.classList.toggle('current', belongs);
    });
  }

  function chiudiSovrapposizioni(){
    // Ogni capitolo ha la propria tenda dei concetti e il proprio velo, e il
    // listener che li apre e' delegato su `document`: con 14 capitoli nello
    // stesso DOM, un clic su un termine apre anche le tende degli altri
    // capitoli che dichiarano quello stesso concetto. Finche' quei capitoli
    // sono nascosti non si vedono — ma cambiando capitolo senza prima
    // chiudere ci si arriva con la tenda gia' aperta e il velo sopra la
    // pagina. Verificato dal vivo: «Embedding» dalla Presentazione, poi
    // Meccanismo 3 dal binario, e Meccanismo 3 si apre velato.
    document.querySelectorAll('.tenda-concetto.visibile, .lightbox-box.visibile').forEach(el => {
      el.classList.remove('visibile');
      if(el.hasAttribute('aria-hidden')) el.setAttribute('aria-hidden', 'true');
    });
    document.querySelectorAll('.tenda-scrim.visibile, .lightbox-scrim.visibile')
      .forEach(el => el.classList.remove('visibile'));
    document.querySelectorAll('.termine-concetto.aperto')
      .forEach(el => el.classList.remove('aperto'));
  }

  // Porta la pagina esattamente sul bordo superiore di `bersaglio`, senza
  // animazione. Torna false se il bersaglio non esiste, cosi' chi chiama sa
  // che deve ripiegare sull'inizio del capitolo.
  //
  // PERCHE' DIRETTAMENTE. Cliccando una sotto-sezione nel binario, prima si
  // tornava all'inizio del capitolo e da li' partiva uno scorrimento dolce
  // fino al bersaglio: si vedeva il capitolo ripartire dalla prima parte e
  // poi correre fino alla quarta. Sono due gesti diversi trattati come uno
  // solo — cambiare capitolo SENZA bersaglio deve portare in cima, cambiare
  // capitolo CON un bersaglio deve portare li' e basta. Il viaggio
  // intermedio non aggiunge orientamento, lo toglie.
  function vaiAlBersaglio(bersaglio){
    const el = bersaglio ? document.getElementById(bersaglio) : null;
    if (!el) return false;
    senzaAnimazione(() => {
      // Il capitolo e' appena passato da hidden a visibile: la posizione si
      // legge dopo che il motore ha rifatto l'impaginazione, non prima.
      // `senzaAnimazione` forza gia' quel ricalcolo.
      const y = Math.max(0, Math.round(el.getBoundingClientRect().top + window.scrollY));
      window.scrollTo(0, y);
    });
    return true;
  }

  // `opzioni.bersaglio` e' l'id su cui atterrare; `opzioni.poi` una funzione
  // da eseguire quando l'ultimo nudge e' passato (oggi solo la selezione del
  // nodo nella Lente, che deve avvenire a capitolo gia' visibile).
  function showChapter(id, opzioni){
    opzioni = opzioni || {};
    chiudiSovrapposizioni();
    chapters.forEach(c => { c.hidden = (c.id !== 'chapter-' + id); });
    updateSidebarState(id);
    if (!vaiAlBersaglio(opzioni.bersaglio)) {
      senzaAnimazione(() => window.scrollTo(0, 0));
    }
    nudgeIntersectionObservers();
    requestAnimationFrame(nudgeIntersectionObservers);
    setTimeout(() => {
      nudgeIntersectionObservers();
      // I nudge sono istantanei e a somma zero, ma rivelare i blocchi puo'
      // far comparire contenuto che sposta il bersaglio: si ricontrolla una
      // volta sola, e solo se serve davvero.
      if (opzioni.bersaglio) vaiAlBersaglio(opzioni.bersaglio);
      if (opzioni.poi) opzioni.poi();
    }, 60);
    window.dispatchEvent(new CustomEvent('corso:chapterchange'));
  }

  // Delegato sul documento e non sulla sola sidebar: i rimandi da capitolo a
  // capitolo esistono anche dentro il testo (la nota di chiusura della
  // Presentazione, un rimando di Fondamenti 1 verso Meccanismo 4), e in un
  // file solo devono cambiare capitolo invece di cercare un file accanto.
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[data-nav-chapter]');
    if(!a) return;
    e.preventDefault();
    const targetId = a.getAttribute('href').slice(1);
    const nodo = a.dataset.nodo;
    if (nodo) {
      // La Lente e' un capitolo, e la tenda di un concetto ci arriva chiedendo
      // un nodo preciso. Si centra dopo che il capitolo e' visibile, perche'
      // selezionaNodo scorre la lista laterale fino alla voce scelta.
      showChapter(a.dataset.navChapter, { poi: () => {
        if (typeof window.lenteSeleziona === 'function') window.lenteSeleziona(nodo);
      } });
    } else {
      showChapter(a.dataset.navChapter, { bersaglio: targetId });
    }
  });

  window.showChapter = showChapter;
  // Il primo capitolo nel DOM, non uno slug scritto a mano: cosi' regge
  // anche la compilazione --trial, che di capitoli ne mette due.
  const primo = document.querySelector('.chapter');
  if(primo) showChapter(primo.dataset.chapter);
})();

(function(){
  // scroll-spy globale: illumina nella sidebar l'unita' in vista, in
  // qualunque capitolo sia visibile. Non usa IntersectionObserver: creato
  // una sola volta osservando anche gli unit-block dei capitoli ancora
  // nascosti (display:none finche' non si naviga li'), in Chrome reale non
  // scatta mai per quei target — bug verificato dal vivo (zero callback
  // durante lo scroll reale), non solo un sospetto. Ricalcolo diretto da
  // getBoundingClientRect ad ogni scroll.
  //
  // I bersagli non sono piu' un elenco di selettori scritto qui (che
  // conosceva `.unit-block` e le tre Parti della vecchia introduzione
  // ricopiata a mano, e non sopravviverebbe al fatto che le Parti della
  // Presentazione ora si chiamano `intro-parte-N`): sono gli elementi che
  // le voci del binario dichiarano come proprio bersaglio. Una regola sola,
  // valida per ogni capitolo presente e futuro.
  const spyLinks = Array.from(document.querySelectorAll('#master-sidebar a[data-spy-target]'));
  let ticking = false;

  function updateActive(){
    ticking = false;
    const visibleChapter = document.querySelector('.chapter:not([hidden])');
    if(!visibleChapter) return;
    const links = spyLinks.filter(a => a.dataset.navChapter === visibleChapter.dataset.chapter);
    if(!links.length) return;
    const centerY = window.innerHeight / 2;
    let current = null;
    links.forEach(a => {
      const el = document.getElementById(a.dataset.spyTarget);
      if(!el) return;
      const rect = el.getBoundingClientRect();
      if(rect.top <= centerY && rect.bottom >= centerY) current = a.dataset.spyTarget;
    });
    if(current){
      spyLinks.forEach(a => a.classList.toggle('active', a.dataset.spyTarget === current));
    }
  }

  function onScroll(){
    if(ticking) return;
    ticking = true;
    requestAnimationFrame(updateActive);
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('corso:chapterchange', updateActive);
  updateActive();
})();
"""


def leggi_design_system_inline():
    """Il CSS del design system con i font in data-URI base64. Non e'
    versionato (sono i woff2 di design-system/fonts/ ricodificati): se manca,
    si rigenera invece di fallire. E' il motivo per cui il compilato non fa
    una sola richiesta di rete — niente Google Fonts, che per giunta serviva
    subset privi di tre dei quattro simboli logici — il monospaziato oggi e
    Noto Sans Mono, che li contiene tutti."""
    if not INLINE_CSS.is_file():
        print(f"{INLINE_CSS.name} assente (non versionato): lo rigenero con build_css.py")
        subprocess.run([sys.executable, str(BUILD_CSS_SCRIPT)], check=True, cwd=DESIGN_SYSTEM_DIR)
    if not INLINE_CSS.is_file():
        raise ValueError(f"{INLINE_CSS} non generato da build_css.py")
    return INLINE_CSS.read_text(encoding="utf-8")


def build(trial=False, lang="it"):
    chapters = [c for c in CHAPTERS if (c[1] in TRIAL_SLUGS)] if trial else CHAPTERS
    slug_by_file = {file: slug for file, slug, *_ in CHAPTERS}

    design_system_css = leggi_design_system_inline()

    styles, markups, scripts = [], [], []
    for filename, slug, label, kind, title in chapters:
        style, markup, script = extract_chapter(filename, slug, kind, slug_by_file)
        if slug == INTRO_SLUG:
            markup = innesta_sommario(markup, slug)
        styles.append(f"\n  /* ===== capitolo {slug} ({filename}) ===== */\n{style}")
        markups.append(markup)
        scripts.append(script)

    # La Lente entra per ultima: in --trial no, perche' la prova tecnica serve
    # a verificare il namespacing dei capitoli di saggio/ e la Lente non ne
    # usa.
    lente_scripts = []
    if not trial:
        lente_style, lente_markup, lente_scripts = extract_lente()
        styles.append(f"\n  /* ===== capitolo {LENTE_SLUG} (lente-semantica) ===== */\n{lente_style}")
        markups.append(lente_markup)

    # data-theme="light" e' l'unico residuo del tema, e non e' un tema: e' la
    # stessa dichiarazione che meccanismo-4-reti-neurali.html porta sul
    # proprio <html>. Il suo shader della superficie di perdita sceglie la
    # tavolozza leggendola (currentLossPalette), e senza questo attributo nel
    # compilato disegnerebbe la variante scura su una pagina chiara.
    html = f"""<!DOCTYPE html>
<html lang="{lang}" data-theme="light">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dal bit alle entità semantiche — saggio interattivo</title>
<style>
/* ===================================================================
   design system, variante da incorporare: token, azzeramenti,
   tipografia, impianto, componenti — e i font (EB Garamond, Noto Sans
   Mono) in data-URI base64. Il compilato non fa richieste di rete.
   Generato da design-system/scripts/build_css.py: non si edita qui.
   =================================================================== */
{design_system_css}

/* ===================================================================
   CSS dei widget, un blocco per capitolo, ciascuno reso discendente
   del proprio #chapter-<slug>. Non stratificato: vince sul design
   system senza alzare la specificita' contro di esso.
   =================================================================== */
{"".join(styles)}
{NEW_CSS}
</style>
</head>
<body>

{build_shared_sidebar(slug_by_file)}

{chr(10).join(markups)}

<script>
{NAV_CONTROLLER}
{chr(10).join(scripts)}
</script>
{"".join(chr(10) + "<script>" + chr(10) + x + chr(10) + "</script>" for x in lente_scripts)}

</body>
</html>
"""

    # Controlli sullo stato finale, non sui passaggi: e' il file scritto che
    # deve essere autosufficiente, non l'intenzione di renderlo tale.
    if not trial:
        fuori = re.findall(r'(?:src|href)="(?!#|data:)([^"]+)"', html)
        if fuori:
            raise ValueError(f"il compilato non e' autosufficiente: {sorted(set(fuori))[:5]}")
        attesi = len([c for c in chapters if c[0] != "dietro-i-widget.html"])
        trovati = html.count("tendaLinkLente.setAttribute('data-nodo', id)")
        if trovati != attesi:
            raise ValueError(
                f"rimandi alla Lente dalla tenda: attesi {attesi}, riscritti {trovati}"
            )
        # Il percorso, non il nome: due capitoli nominano
        # `ontologia/lente-semantica` dentro un commento, parlando della
        # provenienza di una tinta. Quello resta ed e' giusto che resti.
        if "lente-semantica/output/index.html" in html:
            raise ValueError("resta un percorso verso la Lente fuori dal file")

    OUTPUT_DIR.mkdir(exist_ok=True)
    suffix = "_trial" if trial else ""
    out_path = OUTPUT_DIR / f"dal-bit-alle-entita-semantiche_{lang}{suffix}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Scritto {out_path} ({len(html)} caratteri, {len(chapters)} capitoli)")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", action="store_true")
    parser.add_argument("--lang", default="it")
    args = parser.parse_args()
    build(trial=args.trial, lang=args.lang)
