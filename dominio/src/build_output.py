#!/usr/bin/env python3
"""Compila i file di src/saggio/ in un unico output/dal-bit-alle-entita-semantiche_<lingua>.html.

Namespacing per evitare collisioni tra capitoli (id duplicati, `const`/`function`
ridichiarati a livello top-level): ogni capitolo viene avvolto in un contenitore
`.chapter` con id/data-chapter univoci, ogni id interno viene prefissato con lo slug
del capitolo, e lo script del capitolo viene avvolto in una IIFE che referenzia il
proprio contenitore (`chapterRoot`) invece di `document` per le query di shell
condivise (unit-tab, rail, unit-block, reveal).

Uso: python3 build_output.py [--trial] [--lang it]
  --trial   compila solo i due capitoli della prova tecnica di namespacing
            (c00a: pagina singola; cm1: multi-unità con topbar+rail+UNITS)
"""
import argparse
import base64
import mimetypes
import re
import shutil
from pathlib import Path

LEZIONI_DIR = Path(__file__).parent / "saggio"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

# (file, slug, etichetta barra capitoli, kind: 'single' | 'multi', titolo indice)
CHAPTERS = [
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
]

# Raggruppamento in Parti per il Sommario (non usato da extract_chapter/chapterbar,
# solo per la costruzione del Sommario gerarchico in build_intro_and_toc).
PARTI = [
    ("Parte I — Fondamenti", ["c00a", "c00b"]),
    ("Parte II — Genealogia", ["cba", "cbb", "cbc", "cbd"]),
    ("Parte III — Meccanismo", ["cm1", "cm2", "cm3", "cm4", "cm5", "cm6"]),
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
}

TRIAL_SLUGS = {"c00a", "cm1"}

ID_ATTR_RE = re.compile(r'id="([a-zA-Z0-9_-]+)"')
STYLE_RE = re.compile(r"<style>(.*?)</style>", re.S)
SCRIPT_RE = re.compile(r"<script>(.*?)</script>", re.S)
BODY_RE = re.compile(r"<body>(.*?)</body>", re.S)
SIDEBAR_RE = re.compile(r'\s*<nav class="sidebar".*?</nav>\n?', re.S)
SIDEBAR_HREF_RE = re.compile(r'href="([a-z0-9-]+\.html)(#[a-zA-Z0-9_-]+)?"')


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


ASSET_SRC_RE = re.compile(r'src="([^"]+)"')


def inline_relative_assets(markup, filename):
    """Incorpora come data: URI gli asset referenziati con un percorso
    relativo (es. src="immagini_modulo1/foo.png") — nel file sorgente sono
    relativi alla cartella saggio/, ma il file compilato vive in output/,
    quindi lo stesso percorso relativo non risolverebbe piu' allo stesso file."""

    def replace(m):
        src = m.group(1)
        if src.startswith(("data:", "http://", "https://", "//")):
            return m.group(0)
        asset_path = LEZIONI_DIR / src
        if not asset_path.is_file():
            raise ValueError(f"{filename}: asset referenziato non trovato: {src}")
        mime, _ = mimetypes.guess_type(asset_path.name)
        encoded = base64.b64encode(asset_path.read_bytes()).decode("ascii")
        return f'src="data:{mime};base64,{encoded}"'

    return ASSET_SRC_RE.sub(replace, markup)


def scope_shell_queries(script, kind):
    """Riscrive le query di navigazione condivisa da `document.` a `chapterRoot.`
    Sostituzioni meccaniche, identiche in tutti i file dello stesso `kind`.

    Dalla sidebar fissa (che ha sostituito topbar/rail/rail-dot in tutti i file
    sorgente), la shell condivisa e' ridotta a due query: il fade-in `.reveal`
    (comune a tutti i 12 file) e lo scroll-spy sui `.unit-block` (comune ai 10
    file multi-unita' — Genealogia + Meccanismo). Lo scroll-spy stesso usa un
    selettore con id (`#local-scrollspy ...`), gia' reso univoco per capitolo
    dal namespacing generico degli id sopra — non necessita di scoping qui."""
    if kind == "multi":
        requirements = [
            [("const reveals = document.querySelectorAll('.reveal');",
              "const reveals = chapterRoot.querySelectorAll('.reveal');")],
            [("const unitBlocksForSpy = document.querySelectorAll('.unit-block');",
              "const unitBlocksForSpy = chapterRoot.querySelectorAll('.unit-block');")],
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
    # usati da widget "esempio rapido" presenti solo in alcuni file (non tutti,
    # quindi non nella lista `requirements` sopra, che e' un requisito per ogni
    # file del kind). Vanno scopate se presenti, senza errore se assenti.
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
    ]
    for old, new in optional:
        script = script.replace(old, new)

    return script, missing


def extract_chapter(filename, slug, kind):
    raw = (LEZIONI_DIR / filename).read_text(encoding="utf-8")

    style_m = STYLE_RE.search(raw)
    body_m = BODY_RE.search(raw)
    script_m = SCRIPT_RE.search(raw)
    if not (style_m and body_m and script_m):
        raise ValueError(f"{filename}: struttura head/body/script non riconosciuta")

    style = style_m.group(1)
    body = body_m.group(1)
    script = script_m.group(1)

    # il markup del capitolo e' il body meno lo <script> (gia' estratto separatamente)
    markup = body[: body.index("<script>")] if "<script>" in body else body
    # la sidebar del file sorgente viene rimossa qui: nel compilato ce n'e' una
    # sola condivisa (vedi build_shared_sidebar), non una copia per capitolo
    markup = SIDEBAR_RE.sub("", markup, count=1)
    markup = inline_relative_assets(markup, filename)

    ids = set(ID_ATTR_RE.findall(raw))

    style = namespace_tokens(style, slug, ids)
    markup = namespace_tokens(markup, slug, ids)
    script = namespace_tokens(script, slug, ids)

    script, missing = scope_shell_queries(script, kind)
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


def build_shared_sidebar():
    """Costruisce un'unica sidebar condivisa per l'intero documento compilato,
    riscrivendo gli href della sidebar sorgente (identica in tutti e 12 i file,
    a parte i marcatori statici "current"/open per il file corrente) in modo
    che passino da showChapter() invece che navigare a un file separato. Lo
    stato "corrente" e lo scroll-spy diventano dinamici via JS (vedi
    NAV_CONTROLLER), non piu' marcati staticamente per file."""
    raw = (LEZIONI_DIR / CHAPTERS[0][0]).read_text(encoding="utf-8")
    sidebar_m = SIDEBAR_RE.search(raw)
    if not sidebar_m:
        raise ValueError("sidebar sorgente non trovata per costruire la sidebar condivisa")
    sidebar = sidebar_m.group(0).strip()
    sidebar = sidebar.replace('<nav class="sidebar"', '<nav class="sidebar" id="master-sidebar"', 1)
    # la voce Appendice non entra nella compilazione SPA (resta un documento
    # a se', non un capitolo namespacizzato), ma deve restare raggiungibile
    # da un file compilato aperto direttamente via file://: un link che esce
    # dalla cartella di output/ viene bloccato dal sandbox file:// di Safari/
    # Chrome, indipendentemente da quanto sia corretto il percorso relativo
    # (verificato dal vivo: "Ignoring request to load this main resource
    # because it is outside the sandbox"). Soluzione: `dietro-i-widget.html`
    # viene copiato dentro output/ da build() qui sotto, cosi' il link bare
    # gia' presente nella sidebar sorgente (stesso schema di ogni altro
    # capitolo) resta valido cosi' com'e' - stessa cartella, nessun sandbox
    # da attraversare. Il passthrough esplicito e' in rewrite() piu' sotto.
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

    slug_by_file = {file: slug for file, slug, *_ in CHAPTERS}

    def rewrite(m):
        file, frag = m.group(1), m.group(2)
        if file == "dietro-i-widget.html":
            # passthrough: non e' un capitolo compilato (non e' in CHAPTERS),
            # resta un file bare sibling - build() lo copia dentro output/.
            return f'href="dietro-i-widget.html{frag or ""}"'
        if file == "presentazione.html":
            chapter = "intro"
            target = frag[1:] if frag else "chapter-intro"
        else:
            chapter = slug_by_file[file]
            target = f"{chapter}-{frag[1:]}" if frag else f"chapter-{chapter}"
        spy = f' data-spy-target="{target}"' if frag else ""
        return f'href="#{target}" data-nav-chapter="{chapter}"{spy}'

    return SIDEBAR_HREF_RE.sub(rewrite, sidebar)


NEW_CSS = """
  /* ============ compilato: sidebar unica condivisa + tema ============ */
  /* Tema chiaro derivato dalla STESSA tinta del tema scuro (verde ~162 gradi
     per bg/surface/superfici, rame ~28-30 gradi per gli accenti), non da una
     famiglia di colori nuova (niente beige/sabbia neutro): --text riusa
     esattamente il valore di --bg del tema scuro (stesso swatch, ruolo
     invertito); --copper/--copper-bright restano nella stessa tinta del
     tema scuro, solo scuriti per il contrasto su sfondo chiaro. */
  :root[data-theme="light"]{
    --bg: #F0F5F3;
    --surface: #E0EBE8;
    --surface-2: #CDDFDA;
    --copper: #804C1E;
    --copper-bright: #6D3D0D;
    --text: #0F2A22;
    --text-dim: #326253;
    --line: rgba(15,42,34,0.14);
    --true: #804C1E;
    --false: #6B8177;
  }

  .chapter[hidden]{ display:none; }
  body{ padding-top: 0; }

  /* la sidebar condivisa (#master-sidebar) riusa lo stile .sidebar gia'
     duplicato nello <style> di ogni capitolo (identico in tutti i file
     sorgente) — qui va solo azzerato il padding-left che ciascun capitolo
     applicava al proprio <main> pensando di essere l'unica pagina, e
     spostato una volta sola su <body>, cosi' vale anche per l'introduzione
     (che non ha un proprio <main>). */
  main{ padding-left: 0 !important; }
  @media (min-width: 900px){
    body{ padding-left: var(--rail-w); }
  }
  #master-sidebar{ z-index: 90; }

  .theme-toggle{
    position: fixed; z-index: 95; top: 16px; right: 16px;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.74rem;
    color: var(--text-dim); background: var(--surface); border: 1px solid var(--line); border-radius: 4px;
    padding: 6px 12px; cursor: pointer; white-space: nowrap;
  }
  .theme-toggle:focus-visible{ outline: 2px solid var(--copper-bright); outline-offset: 2px; }

  .intro-wrap{ max-width: 740px; margin: 0 auto; padding: 80px 24px 100px; }
  .intro-wrap h1{ font-size: clamp(1.8rem, 5vw, 2.6rem); margin-bottom: 20px; }
  .intro-wrap .sottotitolo{ font-size: 1.15rem; color: var(--text-dim); margin: 0 0 56px; max-width: 62ch; }
  .intro-wrap h2{ font-size: clamp(1.3rem, 3.2vw, 1.7rem); line-height: 1.2; margin: 0 0 24px; }
  .intro-wrap section.parte{ margin-bottom: 52px; }
  .intro-wrap p{ font-size: 1.05rem; color: var(--text); margin-bottom: 20px; }
  .toc{ margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--line); }
  .toc h2{ font-size: 1.2rem; color: var(--copper-bright); margin-bottom: 18px; }
  .toc-parte{ margin-bottom: 28px; }
  .toc-parte:last-child{ margin-bottom: 0; }
  .toc-parte-heading{
    font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--text-dim); margin-bottom: 10px;
  }
  .toc-list{ display:flex; flex-direction:column; gap: 6px; }
  .toc-entry{ display:flex; flex-direction:column; }
  .toc-item{
    text-align:left; font-family: 'Space Grotesk', sans-serif; font-size: 0.98rem;
    color: var(--text); background: var(--surface); border: 1px solid var(--line); border-radius: 6px;
    padding: 12px 16px; cursor: pointer; transition: border-color .2s, background .2s;
  }
  .toc-item:hover{ border-color: var(--copper); background: var(--surface-2); }
  .toc-units{
    font-family: 'Source Serif 4', Georgia, serif; font-size: 0.82rem; color: var(--text-dim);
    padding: 8px 16px 2px; line-height: 1.6;
  }
"""


def build_intro_and_toc():
    abstract = """
    <p class="abstract">C'è un piccolo gioco linguistico che chiunque risolve all'istante, quasi senza pensarci. Alla parola «re» si toglie mentalmente tutto ciò che ha a che fare con l'essere un uomo, e si aggiunge tutto ciò che ha a che fare con l'essere una donna. La risposta arriva da sola: «regina». Sembra solo buon senso linguistico, non un calcolo. Eppure è precisamente questo calcolo — fatto non con le parole ma con i numeri che le rappresentano dentro un modello linguistico — a rivelare qualcosa di sorprendente su come i modelli linguistici (ovvero le reti neurali che imparano il linguaggio) trattano il significato.</p>

    <p class="abstract">Un interruttore non sa cosa vuol dire «regina». Sa solo accendersi o spegnersi — un bit, niente altro. Eppure, sommando miliardi di quegli scatti in una rete addestrata a prevedere la parola successiva, succede qualcosa che nessun singolo interruttore prevede: le parole finiscono per occupare posizioni in uno spazio a centinaia di dimensioni, e quelle posizioni si comportano come se avessero una geometria del senso. Quella stessa sottrazione e quella stessa somma, fatte non sulle parole ma sui numeri che le rappresentano, atterrano nello stesso punto: vicino a «regina». Nessuno ha scritto questa regola: è emersa dai dati, non è stata dichiarata da nessuno — ed è precisamente qui che comincia la domanda a cui il resto di questo lavoro prova a rispondere. Una cosa è vedere il significato comportarsi in modo prevedibile dentro un vettore. Un'altra è poterlo dichiarare, interrogare, sottoporre a un controllo che non dipenda dal fidarsi della geometria. Quello che segue racconta entrambi i percorsi: come si arriva dal primo bit a quel punto nello spazio, e cosa serve, dopo, per trasformare quella posizione in un concetto di cui si possa rispondere.</p>

    <p class="abstract">Il caso di studio è stato costruito in due fasi. La prima ha prodotto il dominio: il saggio interattivo, con i componenti tecnici — tokenizzatore, embedding, aritmetica vettoriale — calcolati su dati reali, non simulati; la stessa aritmetica che il saggio chiama esplicitamente non deduzione ma abduzione, inferenza all'analogia più plausibile. La seconda ha prodotto la mappa: il vocabolario controllato in SKOS e la micro-ontologia in OWL, verificati con un reasoner. Le due fasi corrispondono a due forme di rappresentazione della conoscenza: sub-simbolica la prima, dove il significato emerge dai dati come geometria, plausibile ma mai certa; simbolica la seconda, dove il significato è dichiarato come categoria verificabile — difendibile in un tribunale che non conosce sfumature geometriche.</p>

    <p class="abstract">Entrambe le fasi sono state svolte in collaborazione con un agente AI — un assistente in grado di leggere e scrivere codice, eseguire strumenti di verifica e iterare sul proprio lavoro, con modelli diversi impiegati a seconda del compito. Nella prima fase l'agente ha contribuito alla stesura e alla verifica tecnica dei componenti del saggio. Nella seconda, alla costruzione e al controllo formale dell'ontologia. La verifica finale, in entrambe le fasi, resta umana.</p>

    <p class="abstract">Chi lavora oggi fuori dai grandi laboratori — un'organizzazione piccola, un progetto indipendente — raramente può permettersi entrambe le competenze come ruoli separati: la scrittura tecnica che rende un dominio comprensibile a un lettore, e la costruzione di un grafo di conoscenza o di un'ontologia che lo rende interrogabile da una macchina — quello che oggi si chiama knowledge engineering. Di solito resta solo una delle due, e l'altra si perde. Questo caso di studio è un piccolo controesempio: la stessa persona, con l'aiuto dello stesso agente, ha attraversato entrambe le fasi in sequenza — prima il mestiere di chi spiega, poi quello di chi formalizza. Non perché le due competenze siano diventate la stessa cosa, ma perché un assistente capace di scrivere codice, verificare un'ontologia e iterare sul proprio lavoro abbassa il costo di attraversare il confine tra l'una e l'altra: è un piccolo contrappeso tecnico alla logica per cui solo chi possiede grande scala — infrastrutture, laboratori, ruoli distinti e retribuiti separatamente — può permettersi entrambe le competenze insieme.</p>
    """
    parte1 = """
    <section class="parte" id="parte-1">
      <h2>Framework epistemologico: i limiti che condividiamo con le macchine</h2>

      <p>Il confine appena attraversato — tra chi spiega e chi formalizza, reso più economico da un agente capace di entrambi i mestieri — è un caso piccolo di una domanda più grande, e più temuta. C'è un timore che circola, oggi, attorno a ogni discorso sull'intelligenza artificiale: che le macchine stiano per sostituire l'uomo — nel lavoro, nel pensiero, forse anche nella coscienza. Il lavoro appena descritto suggerisce altro: un agente ha reso più facile attraversare un confine tra due competenze umane, non ha eliminato nessuna delle due. Eppure è proprio questo timore a costruire gran parte della retorica di mercato di questi anni, tanto nell'annuncio trionfale quanto nell'allarme. Non si può governare ciò che non si conosce, e conoscere la macchina — davvero, nei suoi meccanismi, non nelle sue promesse — è indispensabile per saperla governare. Conoscere, qui, significa conoscerne i limiti epistemologici: i limiti di ciò che possiamo sapere della macchina.</p>

      <p>La retorica della sostituzione tratta l'intelligenza artificiale come un rimpiazzo dell'uomo, un nuovo arrivato che rende obsoleto il vecchio. In <em>Ridondanza e Codificazione</em>, Bateson smonta un'idea analoga a proposito del linguaggio iconico: se fosse sostituzione, i vecchi canali sarebbero decaduti. Invece cinetica e paralinguaggio sono fioriti in parallelo al linguaggio verbale — danza, musica, arte — perché comunicano ciò che il linguaggio non può: la relazione (amore, fiducia, timore), proprio perché parzialmente involontaria e difficile da falsificare. Nella storia della comunicazione, il nuovo non ha mai sostituito il vecchio quando i due svolgono funzioni realmente diverse — è cresciuto accanto.</p>

      <p>Forse per la stessa ragione, la domanda «la macchina ha coscienza?» è mal posta. Forse chiedere «la macchina ha coscienza?» tratta la coscienza come una sostanza che un ente possiede o non possiede — un errore categoriale che Bateson aveva messo radicalmente in discussione dal punto di vista epistemologico. La domanda ben posta sarebbe relazionale: non chi ce l'ha, ma tra quali sistemi, a quale livello di contesto, si genera quella particolare ridondanza che chiamiamo coscienza — dove i limiti di mente e macchina si intersecano, e cosa quell'intersezione lascia visibile, o cieco.</p>

      <p>Un sistema totalmente cosciente è impossibile, perché ogni circuito aggiunto per riferire su ciò che manca genera a sua volta nuovi processi all'infinito. La coscienza resta quindi «una piccola parte della verità sull'io» — non per pigrizia, ma per economia di sistema. Quello che offre non è un campione rappresentativo del tutto, ma «archi di circuito» isolati — «una mostruosa negazione dell'integrazione di quel tutto». Per le stesse ragioni è stato portato ad affermare: «la pura razionalità finalizzata, senza l'aiuto di fenomeni come l'arte, la religione, il sogno... è di necessità patogena e distruttrice di vita» (<em>Stile, Grazia, Informazione</em>) — perché la vita dipende da circuiti di contingenze interconnessi, mentre la coscienza vede solo i brevi archi su cui può intervenire. Operare al contrario implicherebbe un errore che si autoalimenta a ogni intervento successivo.</p>

      <p>È in questo spazio — dove i limiti della coscienza umana incontrano i limiti, ancora da mappare, di un sistema che la estende — che si colloca il lavoro che segue.</p>
    </section>
    """
    parte2 = """
    <section class="parte" id="parte-2">
      <h2>Il dominio: struttura e composizione del saggio interattivo</h2>

      <p>Il saggio è organizzato in tre parti. La prima comincia dalle funzioni booleane e dall'hardware — i mattoni discreti su cui tutto il resto poggia. La seconda racconta, in quattro tappe, da dove viene il sogno di una macchina che calcola il pensiero e quali limiti ha oggi — informatica, filosofia della mente, biologia e fisica messe in dialogo, non separate. La terza e ultima ricostruisce il funzionamento tecnico vero e proprio: tokenizzazione, probabilità, lo spazio vettoriale del significato già anticipato in apertura, reti neurali, Transformer, scala.</p>
      <p>Un filo attraversa l'intera trattazione: la tensione tra discreto e continuo. Il saggio non risolve questa tensione ma la usa come chiave di lettura. Un vocabolario di token è un insieme enumerabile, finito; lo spazio vettoriale in cui quei token vengono proiettati è invece continuo, ad alta dimensionalità — la stessa distanza che separa, in matematica, i numeri naturali dai numeri reali. Inoltre ogni componente interattivo è verificato su dati reali, non simulato: il tokenizzatore BPE è addestrato per davvero sul testo del saggio stesso; i vettori sono fastText reali, non inventati per l'occasione; la rete neurale del modulo sulle reti è effettivamente addestrata sul problema XOR, non animata a mano. Chi clicca guarda l'output di un calcolo realmente avvenuto, non una messinscena.</p>
    </section>
    """
    parte3 = """
    <section class="parte" id="parte-3">
      <h2>La lente semantica</h2>

      <p>Formalizzare un dominio come ontologia non è raccontarlo di nuovo in un linguaggio più rigido: è essere costretti a decidere cose che la prosa lascia sospese. Tre esempi bastano a mostrare la differenza. Cos'è un termine, e cosa non lo è? I teorici citati nel saggio non sono concetti nel dominio: sono agenti, autori di un'affermazione. Confonderli con i concetti che nominano avrebbe mescolato una gerarchia con una relazione di attribuzione. Dove finisce una gerarchia genere-specie, e comincia una relazione di tutt'altro tipo? Un generico «è collegato a» avrebbe appiattito «risolve un problema» e «è analogo a» sotto la stessa freccia. Quale incertezza va formalizzata, e quale resta solo descritta? Che un dataset sia reale o illustrativo non è una sfumatura da lasciare a un commento: è una classe che un reasoner può far rispettare, o violare visibilmente.</p>

      <p>Il risultato non è un doppione del saggio in un altro formato: è una mappa che mostra, per ogni scelta fatta scrivendo, l'alternativa che è stata scartata — visibile solo a chi guarda attraverso questa lente. Una versione esplorabile di questa lente, termine per termine, è in preparazione: arriverà a editing del saggio concluso, quando anche il vocabolario e l'ontologia saranno aggiornati di conseguenza.</p>
    </section>
    """
    by_slug = {slug: (label, title) for _, slug, label, _, title in CHAPTERS}

    def build_toc_parte(heading, slugs):
        entries = []
        for slug in slugs:
            _, title = by_slug[slug]
            units = UNIT_TITLES.get(slug)
            units_html = (
                f'<div class="toc-units">{" · ".join(units)}</div>' if units else ""
            )
            entries.append(
                f'<div class="toc-entry">'
                f'<button class="toc-item" onclick="window.showChapter(\'{slug}\')">{title}</button>'
                f'{units_html}'
                f'</div>'
            )
        return (
            f'<div class="toc-parte">'
            f'<div class="toc-parte-heading">{heading}</div>'
            f'<div class="toc-list">{"".join(entries)}</div>'
            f'</div>'
        )

    toc_parti = "\n".join(build_toc_parte(heading, slugs) for heading, slugs in PARTI)
    return (
        f'<section class="chapter" id="chapter-intro" data-chapter="intro" hidden>\n'
        f'  <div class="intro-wrap">\n'
        f'    <h1>Dal bit alle entità semantiche</h1>\n'
        f'    <p class="sottotitolo">Un saggio interattivo come dominio, formalizzato in un\'ontologia: cartografia della conoscenza tra spazio vettoriale e grafo — dall\'apprendimento dei modelli linguistici al knowledge engineering.</p>\n'
        f'    <p class="abstract">Il presente caso di studio integra in un unico lavoro la scrittura tecnica, che produce un saggio interattivo su come funzionano i modelli linguistici — dai principi discreti dell\'hardware fino allo spazio vettoriale in cui si rappresenta il significato — e la sua cartografia: un vocabolario controllato e un\'ontologia OWL che formalizzano quello stesso dominio in un grafo di entità semantiche verificabile da un reasoner, non solo descritto in prosa.</p>\n'
        f'{abstract}\n'
        f'{parte1}\n'
        f'{parte2}\n'
        f'{parte3}\n'
        f'    <div class="toc">\n'
        f'      <h2>Indice</h2>\n'
        f'      {toc_parti}\n'
        f'    </div>\n'
        f'  </div>\n'
        f'</section>'
    )


NAV_CONTROLLER = """
(function(){
  const chapters = document.querySelectorAll('.chapter');
  const sidebar = document.getElementById('master-sidebar');
  const sidebarModules = sidebar.querySelectorAll('details.modulo');
  const sidebarSimple = sidebar.querySelectorAll('.voce-semplice');

  function nudgeIntersectionObservers(){
    // Gli IntersectionObserver di ciascun capitolo (fade-in .reveal) e quello
    // globale di scroll-spy vengono creati mentre il capitolo e' ancora
    // hidden: il passaggio a display:block non basta da solo a far scattare
    // il loro ricalcolo in questo motore di rendering. Un piccolo delta di
    // scroll reale (anche se il documento e' gia' a scrollY 0) forza il
    // ricalcolo dell'intersezione in modo affidabile.
    window.scrollBy(0, 1);
    window.scrollBy(0, -1);
  }

  function updateSidebarState(id){
    sidebarSimple.forEach(a => a.classList.toggle('current', a.dataset.navChapter === id));
    sidebarModules.forEach(d => {
      const belongs = !!d.querySelector('a[data-nav-chapter="' + id + '"]');
      d.open = belongs;
      const summary = d.querySelector('summary');
      if(summary) summary.classList.toggle('current', belongs);
    });
  }

  function showChapter(id){
    chapters.forEach(c => { c.hidden = (c.id !== 'chapter-' + id); });
    updateSidebarState(id);
    window.scrollTo({ top: 0 });
    nudgeIntersectionObservers();
    requestAnimationFrame(nudgeIntersectionObservers);
    setTimeout(nudgeIntersectionObservers, 60);
    window.dispatchEvent(new CustomEvent('corso:chapterchange'));
  }

  sidebar.addEventListener('click', (e) => {
    const a = e.target.closest('a[data-nav-chapter]');
    if(!a) return;
    e.preventDefault();
    const targetId = a.getAttribute('href').slice(1);
    showChapter(a.dataset.navChapter);
    requestAnimationFrame(() => {
      const el = document.getElementById(targetId);
      if(el) el.scrollIntoView({ behavior: 'smooth' });
    });
  });

  window.showChapter = showChapter;
  showChapter('intro');
})();

(function(){
  // scroll-spy globale: illumina nella sidebar l'unita' in vista, in
  // qualunque capitolo sia visibile. Non usa IntersectionObserver: creato
  // una sola volta osservando anche gli unit-block dei capitoli ancora
  // nascosti (display:none finche' non si naviga li'), in Chrome reale non
  // scatta mai per quei target — bug verificato dal vivo (zero callback
  // durante lo scroll reale), non solo un sospetto. Ricalcolo diretto da
  // getBoundingClientRect ad ogni scroll, scoped al solo capitolo
  // effettivamente visibile in quel momento: nessun observer creato su
  // elementi nascosti, nessuna dipendenza da un comportamento del browser
  // rivelatosi inaffidabile qui.
  const spyLinks = document.querySelectorAll('#master-sidebar a[data-spy-target]');
  let ticking = false;

  function updateActive(){
    ticking = false;
    const visibleChapter = document.querySelector('.chapter:not([hidden])');
    if(!visibleChapter) return;
    const targets = visibleChapter.querySelectorAll('.unit-block, #parte-1, #parte-2, #parte-3');
    if(!targets.length) return;
    const centerY = window.innerHeight / 2;
    let current = null;
    targets.forEach(el => {
      const rect = el.getBoundingClientRect();
      if(rect.top <= centerY && rect.bottom >= centerY) current = el;
    });
    if(current){
      spyLinks.forEach(a => a.classList.toggle('active', a.dataset.spyTarget === current.id));
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

(function(){
  const KEY = 'corso-llm-theme';
  const btn = document.getElementById('theme-toggle');
  const saved = localStorage.getItem(KEY);
  if(saved === 'light' || saved === 'dark'){ document.documentElement.dataset.theme = saved; }
  function label(){ return document.documentElement.dataset.theme === 'light' ? 'Tema: chiaro' : 'Tema: scuro'; }
  btn.textContent = label();
  btn.addEventListener('click', () => {
    const next = document.documentElement.dataset.theme === 'light' ? 'dark' : 'light';
    document.documentElement.dataset.theme = next;
    localStorage.setItem(KEY, next);
    btn.textContent = label();
    // Alcuni widget (canvas 2D pre-renderizzati, shader WebGL) non seguono
    // da soli le variabili CSS del tema: si ridisegnano ascoltando questo
    // evento invece di un semplice cambio di `data-theme`.
    window.dispatchEvent(new CustomEvent('corso:themechange'));
  });
})();
"""


def build(trial=False, lang="it"):
    chapters = [c for c in CHAPTERS if (c[1] in TRIAL_SLUGS)] if trial else CHAPTERS

    styles, markups, scripts = [], [], []
    for filename, slug, label, kind, title in chapters:
        style, markup, script = extract_chapter(filename, slug, kind)
        styles.append(f"  /* ===== capitolo {slug} ({filename}) ===== */\n{style}")
        markups.append(markup)
        scripts.append(script)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dal bit alle entità semantiche — saggio interattivo</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500;8..60,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
{"".join(styles)}
{NEW_CSS}
</style>
</head>
<body>

{build_shared_sidebar()}
<button class="theme-toggle" id="theme-toggle">Tema: scuro</button>

{build_intro_and_toc()}

{chr(10).join(markups)}

<script>
{NAV_CONTROLLER}
{chr(10).join(scripts)}
</script>

</body>
</html>
"""
    OUTPUT_DIR.mkdir(exist_ok=True)
    suffix = "_trial" if trial else ""
    out_path = OUTPUT_DIR / f"dal-bit-alle-entita-semantiche_{lang}{suffix}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Scritto {out_path} ({len(html)} caratteri, {len(chapters)} capitoli)")

    # L'appendice non e' un capitolo compilato (resta un documento a se', non
    # namespacizzato) ma va raggiungibile da un file aperto via file:// senza
    # server: copiata come sibling dentro output/, cosi' il link bare della
    # sidebar (vedi build_shared_sidebar) resta nella stessa cartella, senza
    # attraversare il sandbox file:// che blocca la navigazione fuori da essa.
    appendice_src = LEZIONI_DIR / "dietro-i-widget.html"
    appendice_dst = OUTPUT_DIR / "dietro-i-widget.html"
    shutil.copyfile(appendice_src, appendice_dst)
    print(f"Copiato {appendice_dst}")

    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", action="store_true")
    parser.add_argument("--lang", default="it")
    args = parser.parse_args()
    build(trial=args.trial, lang=args.lang)
