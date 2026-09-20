#!/usr/bin/env python3
"""Genera la struttura di consultazione HTML/CSS vanilla in output/ leggendo
src/vocabolario.ttl + src/ontologia.ttl + src/dati.ttl.

Nessun motore di template: pagine costruite con semplici funzioni Python che
restituiscono stringhe. Non genera output/index.html una volta sola e basta:
rigenera l'intera cartella output/{concetti,moduli,fili,teorici}/ da zero ogni
volta, così la struttura di consultazione non può disallinearsi dal grafo.

Uso: .venv/bin/python3 scripts/genera_html.py
"""
import os
import shutil
import rdflib
from rdflib.namespace import RDF, RDFS

N = rdflib.Namespace("https://smb-antro.github.io/dal-bit-alle-entita-semantiche/vocabolario#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

DATA_FILES = ["src/vocabolario.ttl", "src/ontologia.ttl", "src/dati.ttl"]
OUT = "output"

# Object property -> (etichetta diretta, etichetta inversa) per la sezione
# "Relazioni" di ogni pagina Concetto. L'etichetta inversa esiste perché una
# relazione come prerequisitoDi è interessante da leggere in entrambe le
# direzioni (leggo la pagina di Embedding e voglio vedere sia "richiede" sia
# "è richiesto da").
RELAZIONI_CONCETTO = [
    (N.prerequisitoDi, "È prerequisito di", "Richiede come prerequisito"),
    (N.risolve, "Risolve", "È risolto da"),
    (N.analogoA, "È analogo a", "È analogo a"),
    (N.contrappostoA, "Si contrappone a", "Si contrappone a"),
    (N.esemplifica, "Esemplifica", "È esemplificato da"),
    (N.spiegataDa, "È spiegato da", "Spiega"),
    (N.rendeOperativo, "Rende operativo", "È reso operativo da"),
    (N.collegatoA, "È collegato a", "È collegato a"),
]


def load_graph():
    g = rdflib.Graph()
    for f in DATA_FILES:
        g.parse(f, format="turtle")
    return g


def label(g, uri):
    v = g.value(uri, SKOS.prefLabel) or g.value(uri, RDFS.label)
    return str(v) if v is not None else str(uri).split("#")[-1]


def slug(uri):
    return str(uri).split("#")[-1]


def kind(g, uri):
    types = set(g.objects(uri, RDF.type))
    if SKOS.Concept in types:
        return "concetto"
    if N.Teorico in types:
        return "teorico"
    if N.Parte in types:
        return "parte"
    if N.Capitolo in types:
        return "capitolo"
    if N.Unita in types:
        return "unita"
    if N.Dataset in types:
        return "dataset"
    return "altro"


def href_citabile(g, u, da_radice=False):
    """URL relativo verso il bersaglio di un :discussoInUnita — che ora può
    essere un'Unità (link con ancora dentro la pagina del suo Capitolo) o,
    per i 2 Capitoli di Fondamenti (nessuna sotto-unità), il Capitolo stesso
    (link diretto, senza ancora)."""
    prefisso = "" if da_radice else "../"
    if kind(g, u) == "capitolo":
        return f"{prefisso}moduli/{slug(u)}.html"
    capitolo = g.value(u, N.partOfCapitolo)
    return f"{prefisso}moduli/{slug(capitolo)}.html#{slug(u)}"


def pagina(titolo, sottotitolo, briciole, corpo, profondita=1, titolo_html=None):
    """titolo: testo semplice per <title> (mai HTML). titolo_html: markup per
    <h1>, se diverso da titolo (es. per aggiungere il tag "Tecnica")."""
    css = "../style.css" if profondita else "style.css"
    briciole_html = ""
    if briciole:
        parti = []
        for i, (testo, link) in enumerate(briciole):
            if link:
                parti.append(f'<a href="{link}">{testo}</a>')
            else:
                parti.append(testo)
        briciole_html = (
            '<nav class="briciole">'
            + '<span class="sep">›</span>'.join(parti)
            + "</nav>"
        )
    sottotitolo_html = f'<p class="sottotitolo">{sottotitolo}</p>' if sottotitolo else ""
    return f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titolo} — Vocabolario del saggio «Dal bit alle entità semantiche»</title>
<link rel="stylesheet" href="{css}">
</head>
<body>
<div class="pagina">
{briciole_html}
<header class="testata">
<span class="apparato">Vocabolario del saggio «Dal bit alle entità semantiche»</span>
<h1>{titolo_html or titolo}</h1>
{sottotitolo_html}
</header>
{corpo}
<footer class="piede">
Generato da <code>scripts/genera_html.py</code> a partire da
<code>src/vocabolario.ttl</code>, <code>src/ontologia.ttl</code>,
<code>src/dati.ttl</code>. Istantanea del saggio al 26 agosto 2026, aggiornata alla
nuova struttura in tre Parti il 4 settembre 2026 — vedi
<code>docs/decisioni-modellazione.md</code> per il razionale delle scelte di
modellazione.
</footer>
</div>
</body>
</html>
"""


def scrivi(percorso, contenuto):
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(contenuto)


# ---------------------------------------------------------------------------
# Pagine Concetto
# ---------------------------------------------------------------------------

def genera_pagina_concetto(g, c):
    lbl = label(g, c)
    nota = g.value(c, SKOS.scopeNote)
    broader = g.value(c, SKOS.broader)
    narrower = sorted(g.subjects(SKOS.broader, c), key=lambda x: label(g, x))
    is_tecnica = (c, RDF.type, N.Tecnica) in g

    briciole = [("Home", "../index.html"), ("Glossario", "../concetti/index.html")]
    if broader:
        briciole.append((label(g, broader), f"{slug(broader)}.html"))
    briciole.append((lbl, None))

    tag = ' <span class="tag-tecnica">Tecnica</span>' if is_tecnica else ""
    titolo_html = f"{lbl}{tag}"
    corpo = [f'<p class="scope-note">{nota}</p>' if nota else ""]

    if narrower:
        corpo.append("<h2>Concetti più specifici</h2><ul class=\"lista-piatta\">")
        for n in narrower:
            corpo.append(f'<li><a href="{slug(n)}.html">{label(g, n)}</a></li>')
        corpo.append("</ul>")

    # relazioni tipizzate, dirette e inverse
    blocchi_relazioni = []
    for prop, lbl_diretta, lbl_inversa in RELAZIONI_CONCETTO:
        diretti = sorted(g.objects(c, prop), key=lambda x: label(g, x))
        inversi = sorted(g.subjects(prop, c), key=lambda x: label(g, x))
        if diretti:
            voci = ", ".join(f'<a href="{slug(t)}.html">{label(g, t)}</a>' for t in diretti)
            blocchi_relazioni.append(f'<li><span class="relazione-tipo">{lbl_diretta}</span> {voci}</li>')
        if inversi:
            voci = ", ".join(f'<a href="{slug(t)}.html">{label(g, t)}</a>' for t in inversi)
            blocchi_relazioni.append(f'<li><span class="relazione-tipo">{lbl_inversa}</span> {voci}</li>')
    if blocchi_relazioni:
        corpo.append("<h2>Relazioni con altri concetti</h2><ul class=\"lista-piatta\">")
        corpo.extend(blocchi_relazioni)
        corpo.append("</ul>")

    # teorici
    teorici = sorted(set(g.objects(c, N.teorizzatoDa)), key=lambda x: label(g, x))
    discussi_da = sorted(set(g.objects(c, N.messoInDiscussioneDa)), key=lambda x: label(g, x))
    if teorici or discussi_da:
        corpo.append("<h2>Teorici</h2><ul class=\"lista-piatta\">")
        if teorici:
            voci = ", ".join(f'<a href="../teorici/{slug(t)}.html">{label(g, t)}</a>' for t in teorici)
            corpo.append(f'<li><span class="relazione-tipo">Teorizzato da</span> {voci}</li>')
        if discussi_da:
            voci = ", ".join(f'<a href="../teorici/{slug(t)}.html">{label(g, t)}</a>' for t in discussi_da)
            corpo.append(f'<li><span class="relazione-tipo">Messo in discussione da</span> {voci}</li>')
        corpo.append("</ul>")

    # fonti / unità (o, per Fondamenti, il Capitolo stesso — nessuna sotto-unità)
    unita = sorted(g.objects(c, N.discussoInUnita), key=lambda x: label(g, x))
    if unita:
        corpo.append("<h2>Discusso in</h2><ul class=\"lista-piatta\">")
        for u in unita:
            codice, _, descrizione = label(g, u).partition(" — ")
            corpo.append(
                f'<li><span class="codice-unita">{codice}</span> '
                f'— <a class="rimando" href="{href_citabile(g, u)}">{descrizione}</a></li>'
            )
        corpo.append("</ul>")

    contenuto = pagina(lbl, None, briciole, "\n".join(corpo), profondita=1, titolo_html=titolo_html)
    scrivi(f"{OUT}/concetti/{slug(c)}.html", contenuto)


def genera_indice_concetti(g):
    top = sorted(g.subjects(SKOS.topConceptOf, N.DalBitAlleEntitaSemantiche), key=lambda x: label(g, x))
    corpo = ["<p>Tutti i 111 concetti, raggruppati per area tematica. Ogni pagina mostra la sua gerarchia, le relazioni tipizzate con altri concetti, i teorici collegati e le unità del corso in cui è discusso.</p>"]
    for t in top:
        figli = sorted(g.subjects(SKOS.broader, t), key=lambda x: label(g, x))
        corpo.append(f'<h2><a href="{slug(t)}.html">{label(g, t)}</a></h2>')
        corpo.append('<div class="griglia-indice">')
        for f_ in figli:
            corpo.append(f'<a class="card-nav" href="{slug(f_)}.html"><span class="titolo-card">{label(g, f_)}</span></a>')
        corpo.append('</div>')
    briciole = [("Home", "../index.html"), ("Glossario", None)]
    contenuto = pagina("Glossario", "111 concetti in 14 aree tematiche", briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/concetti/index.html", contenuto)


# ---------------------------------------------------------------------------
# Pagine Capitolo (cartella output/moduli/ non rinominata — vedi
# decisioni-modellazione.md, Aggiornamento post-estrazione: plumbing interno,
# il contenuto delle pagine usa comunque "Parte"/"Capitolo" corretti)
# ---------------------------------------------------------------------------

def _blocco_citazioni(g, target):
    """Le righe 'Concetti discussi qui' / 'Teorici citati qui' per un bersaglio
    di :discussoInUnita (un'Unità o, per Fondamenti, il Capitolo stesso)."""
    citanti = sorted(g.subjects(N.discussoInUnita, target), key=lambda x: label(g, x))
    concetti = [x for x in citanti if kind(g, x) == "concetto"]
    teorici_qui = [x for x in citanti if kind(g, x) == "teorico"]
    righe = []
    if concetti:
        voci = ", ".join(f'<a class="rimando" href="../concetti/{slug(c)}.html">{label(g, c)}</a>' for c in concetti)
        righe.append(f'<p>Concetti discussi qui: {voci}</p>')
    if teorici_qui:
        voci = ", ".join(f'<a class="rimando" href="../teorici/{slug(t)}.html">{label(g, t)}</a>' for t in teorici_qui)
        righe.append(f'<p class="apparato">Teorici citati qui: {voci}</p>')
    return righe


def genera_pagina_capitolo(g, m):
    lbl = label(g, m)
    parte = g.value(m, N.partOfParte)
    unita = sorted(g.subjects(N.partOfCapitolo, m), key=lambda u: str(g.value(u, RDFS.label)))
    corpo = []
    if not unita:
        # Fondamenti: nessuna sotto-unità — il Capitolo stesso è il bersaglio
        # citabile (vedi ontologia.ttl, :discussoInUnita).
        corpo.extend(_blocco_citazioni(g, m))
    else:
        for u in unita:
            u_lbl = label(g, u)
            rimandi = sorted(g.objects(u, N.rimandaA), key=lambda x: label(g, x))
            corpo.append(f'<h2 id="{slug(u)}"><span class="codice-unita">{u_lbl.split(" — ")[0]}</span> — {u_lbl.split(" — ", 1)[1] if " — " in u_lbl else ""}</h2>')
            corpo.extend(_blocco_citazioni(g, u))
            if rimandi:
                voci = ", ".join(f'<a href="#{slug(r)}">{label(g, r)}</a>' for r in rimandi)
                corpo.append(f'<p class="apparato">Rimanda a → {voci}</p>')
    briciole = [
        ("Home", "../index.html"), ("Moduli", "../moduli/index.html"),
        (label(g, parte), f"../moduli/index.html#{slug(parte)}"), (lbl, None),
    ]
    sottotitolo = f"{len(unita)} unità" if unita else "Nessuna sotto-unità — questo è già il bersaglio citabile più fine"
    contenuto = pagina(lbl, sottotitolo, briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/moduli/{slug(m)}.html", contenuto)


def genera_indice_moduli(g):
    # Ordine narrativo fisso (Fondamenti, Genealogia, Meccanismo), non alfabetico.
    ordine_parti = [N.ParteFondamenti, N.ParteGenealogia, N.ParteMeccanismo]
    corpo = []
    for p in ordine_parti:
        capitoli = sorted(g.subjects(N.partOfParte, p), key=lambda m: str(g.value(m, RDFS.label)))
        corpo.append(f'<h2 id="{slug(p)}">{label(g, p)}</h2>')
        corpo.append('<div class="griglia-indice">')
        for m in capitoli:
            n_unita = len(list(g.subjects(N.partOfCapitolo, m)))
            desc = f"{n_unita} unità" if n_unita else "Nessuna sotto-unità"
            corpo.append(f'<a class="card-nav" href="{slug(m)}.html"><span class="titolo-card">{label(g, m)}</span><span class="desc-card">{desc}</span></a>')
        corpo.append('</div>')
    briciole = [("Home", "../index.html"), ("Moduli", None)]
    contenuto = pagina("Moduli", "3 Parti, 12 capitoli — la struttura organizzativa del saggio", briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/moduli/index.html", contenuto)


# ---------------------------------------------------------------------------
# Pagine Filo trasversale
# ---------------------------------------------------------------------------

def genera_pagina_filo(g, filo_uri, filo_slug):
    lbl = g.value(filo_uri, SKOS.prefLabel)
    nota = g.value(filo_uri, SKOS.scopeNote)
    lista = g.value(filo_uri, SKOS.memberList)
    membri = list(g.items(lista)) if lista else []
    corpo = [f'<p class="scope-note">{nota}</p>' if nota else ""]
    corpo.append('<ol class="percorso-ordinato">')
    for m in membri:
        nota_m = g.value(m, SKOS.scopeNote)
        corpo.append(
            f'<li><a class="rimando" href="../concetti/{slug(m)}.html">{label(g, m)}</a>'
            f'<br><span class="scope-note">{nota_m}</span></li>'
        )
    corpo.append('</ol>')
    briciole = [("Home", "../index.html"), ("Fili trasversali", "../fili/index.html"), (str(lbl), None)]
    contenuto = pagina(str(lbl), f"Percorso di lettura ordinato — {len(membri)} tappe", briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/fili/{filo_slug}.html", contenuto)


def genera_indice_fili(g):
    fili = [
        (N.FiloDiscretoContinuo, "discreto-continuo"),
        (N.FiloGalileoCrolloQuantistico, "galileo-crollo-quantistico"),
        (N.FiloLogicaInformazioneBiologia, "logica-informazione-biologia"),
    ]
    corpo = ['<p>Tre percorsi di lettura ordinati, trasversali ai moduli: non termini del vocabolario, ma sequenze di concetti già definiti nel glossario.</p>']
    corpo.append('<div class="griglia-indice">')
    for uri, fslug in fili:
        lbl = g.value(uri, SKOS.prefLabel)
        nota = g.value(uri, SKOS.scopeNote)
        corpo.append(f'<a class="card-nav" href="{fslug}.html"><span class="titolo-card">{lbl}</span><span class="desc-card">{nota}</span></a>')
        genera_pagina_filo(g, uri, fslug)
    corpo.append('</div>')
    briciole = [("Home", "../index.html"), ("Fili trasversali", None)]
    contenuto = pagina("Fili trasversali", None, briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/fili/index.html", contenuto)


# ---------------------------------------------------------------------------
# Pagine Teorico
# ---------------------------------------------------------------------------

def genera_pagina_teorico(g, t):
    lbl = label(g, t)
    ruolo = g.value(t, RDFS.comment)
    opera = g.value(t, N.citaOpera)
    teorizzati = sorted(g.subjects(N.teorizzatoDa, t), key=lambda x: label(g, x))
    discussi = sorted(g.subjects(N.messoInDiscussioneDa, t), key=lambda x: label(g, x))
    risposte_a = sorted(g.objects(t, N.riprendeArgomentazioneDi), key=lambda x: label(g, x))
    unita = sorted(g.objects(t, N.discussoInUnita), key=lambda x: label(g, x))

    corpo = [f'<p class="scope-note">{ruolo}</p>' if ruolo else ""]
    if opera:
        corpo.append(f'<p class="apparato">Opera citata: <em>{opera}</em></p>')
    if teorizzati:
        voci = ", ".join(f'<a class="rimando" href="../concetti/{slug(c)}.html">{label(g, c)}</a>' for c in teorizzati)
        corpo.append(f'<h2>Concetti teorizzati</h2><p>{voci}</p>')
    if discussi:
        voci = ", ".join(f'<a class="rimando" href="../concetti/{slug(c)}.html">{label(g, c)}</a>' for c in discussi)
        corpo.append(f'<h2>Mette in discussione</h2><p>{voci}</p>')
    if risposte_a:
        voci = ", ".join(f'<a href="{slug(x)}.html">{label(g, x)}</a>' for x in risposte_a)
        corpo.append(f'<h2>Riprende l\'argomentazione di</h2><p>{voci}</p>')
    if unita:
        voci = ", ".join(f'<a href="{href_citabile(g, u)}">{label(g, u)}</a>' for u in unita)
        corpo.append(f'<h2>Citato in</h2><p>{voci}</p>')

    briciole = [("Home", "../index.html"), ("Teorici", "../teorici/index.html"), (lbl, None)]
    contenuto = pagina(lbl, None, briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/teorici/{slug(t)}.html", contenuto)


def genera_indice_teorici(g):
    teorici = sorted(g.subjects(RDF.type, N.Teorico), key=lambda t: label(g, t))
    corpo = ['<p>Le persone citate nel corso come autrici di un concetto, una tecnica o un\'obiezione — un indice dei nomi, come in un apparato editoriale.</p>']
    corpo.append('<ul class="lista-piatta">')
    for t in teorici:
        corpo.append(f'<li><a href="{slug(t)}.html">{label(g, t)}</a></li>')
    corpo.append('</ul>')
    briciole = [("Home", "../index.html"), ("Teorici", None)]
    contenuto = pagina("Teorici", f"{len(teorici)} nomi citati nel corso", briciole, "\n".join(corpo), profondita=1)
    scrivi(f"{OUT}/teorici/index.html", contenuto)


# ---------------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------------

def genera_home(g):
    n_concetti = len(set(g.subjects(RDF.type, SKOS.Concept)))
    n_capitoli = len(set(g.subjects(RDF.type, N.Capitolo)))
    n_teorici = len(set(g.subjects(RDF.type, N.Teorico)))
    corpo = f"""
<p>Tre modi di consultare lo stesso modello — un vocabolario controllato (SKOS) e una
micro-ontologia (OWL) costruiti sul saggio «Dal bit alle entità semantiche» — a seconda
di cosa si sta cercando.</p>
<div class="griglia-indice">
<a class="card-nav" href="concetti/index.html"><span class="titolo-card">Glossario</span><span class="desc-card">{n_concetti} concetti per area tematica — parti da un termine</span></a>
<a class="card-nav" href="moduli/index.html"><span class="titolo-card">Moduli</span><span class="desc-card">{n_capitoli} capitoli in 3 Parti — parti dalla struttura del saggio</span></a>
<a class="card-nav" href="fili/index.html"><span class="titolo-card">Fili trasversali</span><span class="desc-card">3 percorsi di lettura ordinati attraverso le Parti</span></a>
<a class="card-nav" href="teorici/index.html"><span class="titolo-card">Teorici</span><span class="desc-card">{n_teorici} nomi citati — parti da un autore</span></a>
</div>
<h2>Sul progetto</h2>
<p>Vocabolario, ontologia, dati e questa struttura di consultazione sono generati/scritti
a partire da un unico grafo RDF (<code>src/*.ttl</code>), validato con un reasoner OWL-RL
e con SHACL. Il documento delle decisioni di modellazione —
<code>docs/decisioni-modellazione.md</code> — è il deliverable primario del progetto: qui
solo la sua superficie navigabile.</p>
"""
    contenuto = pagina("Vocabolario del saggio «Dal bit alle entità semantiche»", "Un vocabolario controllato, una micro-ontologia, tre modi di leggerli", None, corpo, profondita=0)
    scrivi(f"{OUT}/index.html", contenuto)


def main():
    g = load_graph()

    for d in ["concetti", "moduli", "fili", "teorici"]:
        path = f"{OUT}/{d}"
        if os.path.isdir(path):
            shutil.rmtree(path)

    for c in g.subjects(RDF.type, SKOS.Concept):
        genera_pagina_concetto(g, c)
    genera_indice_concetti(g)

    for m in g.subjects(RDF.type, N.Capitolo):
        genera_pagina_capitolo(g, m)
    genera_indice_moduli(g)

    genera_indice_fili(g)  # genera anche le 3 pagine-filo al suo interno

    for t in g.subjects(RDF.type, N.Teorico):
        genera_pagina_teorico(g, t)
    genera_indice_teorici(g)

    genera_home(g)

    n_concetti = len(set(g.subjects(RDF.type, SKOS.Concept)))
    n_capitoli = len(set(g.subjects(RDF.type, N.Capitolo)))
    n_teorici = len(set(g.subjects(RDF.type, N.Teorico)))
    print(f"Generate {n_concetti} pagine concetto, {n_capitoli} pagine capitolo, "
          f"3 pagine filo, {n_teorici} pagine teorico, 5 pagine indice/home.")


if __name__ == "__main__":
    main()
