#!/usr/bin/env python3
"""Genera lente-semantica/src/grafo.json leggendo i tre .ttl di root
(../../src/vocabolario.ttl, ontologia.ttl, dati.ttl) — sola lettura, non li
modifica mai.

A differenza di scripts/genera_dati.py e scripts/genera_html.py (root), qui non
si scrivono nuove decisioni di modellazione: si esporta una VISTA del grafo già
esistente, in una forma che il browser possa disegnare senza dover parlare RDF.
Ogni proprietà esportata come arco è elencata esplicitamente sotto (PROPRIETA) —
non "ogni tripla il cui oggetto è un URI", per evitare di esporre triple di
bookkeeping (rdf:type, skos:inScheme, le liste RDF di skos:memberList) come se
fossero relazioni di dominio.

Uso: .venv/bin/python3 lente-semantica/scripts/genera_grafo.py > lente-semantica/src/grafo.json
(il venv è quello di root: questo script non ha dipendenze proprie oltre rdflib)
"""
import json
from pathlib import Path

import rdflib
from rdflib.namespace import RDF, RDFS

ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILES = [ROOT / "src" / f for f in ("vocabolario.ttl", "ontologia.ttl", "dati.ttl")]
# .js e non .json: output/index.html lo carica con <script src>, non fetch() —
# fetch() di un file locale e' bloccato da Chrome/Firefox quando la pagina e'
# aperta come file:// (nessun server). Un <script src> di un file .js invece
# funziona sempre, anche a doppio clic. Stesso identico contenuto JSON, solo
# preceduto da "const GRAFO =" per essere eseguibile invece che solo dati.
OUT = Path(__file__).resolve().parent.parent / "src" / "grafo.js"

N = rdflib.Namespace("http://example.org/corso-llm-vocabolario#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

# Proprietà esposte come archi del grafo: (property URI, etichetta diretta,
# etichetta inversa, categoria per il colore). Le etichette dirette/inverse
# per le 8 relazioni Concetto-Concetto sono le stesse di
# scripts/genera_html.py, RELAZIONI_CONCETTO — stessa fonte di verità, non
# reinventate qui.
PROPRIETA = [
    (SKOS.broader, "è più specifico di", "ha come specificazioni", "gerarchia"),
    (N.prerequisitoDi, "è prerequisito di", "richiede come prerequisito", "concettuale"),
    (N.risolve, "risolve", "è risolto da", "concettuale"),
    (N.analogoA, "è analogo a", "è analogo a", "concettuale"),
    (N.contrappostoA, "si contrappone a", "si contrappone a", "concettuale"),
    (N.esemplifica, "esemplifica", "è esemplificato da", "concettuale"),
    (N.spiegataDa, "è spiegato da", "spiega", "concettuale"),
    (N.rendeOperativo, "rende operativo", "è reso operativo da", "concettuale"),
    (N.collegatoA, "è collegato a", "è collegato a", "concettuale"),
    (N.teorizzatoDa, "teorizzato da", "teorizza", "attribuzione"),
    (N.messoInDiscussioneDa, "messo in discussione da", "mette in discussione", "attribuzione"),
    (N.riprendeArgomentazioneDi, "riprende l'argomentazione di", "la cui argomentazione è ripresa da", "attribuzione"),
    (N.discussoInUnita, "discusso in", "discute", "struttura"),
    (N.partOfCapitolo, "fa parte del capitolo", "contiene l'unità", "struttura"),
    (N.partOfParte, "fa parte della parte", "contiene il capitolo", "struttura"),
    (N.rimandaA, "rimanda a", "è richiamato da", "struttura"),
    (N.haStatoEpistemico, "ha stato epistemico", "è lo stato epistemico di", "struttura"),
]

# Tipi riconosciuti, in ordine di controllo (un nodo può avere più tipi, es.
# Concetto + Tecnica — a differenza di kind() in genera_html.py che ne
# restituisce uno solo, qui servono tutti per il badge "Concetto + Tecnica"
# visto nel mockup).
TIPI = [
    (SKOS.Concept, "Concetto"),
    (N.Tecnica, "Tecnica"),
    (N.Teorico, "Teorico"),
    (N.Parte, "Parte"),
    (N.Capitolo, "Capitolo"),
    (N.Unita, "Unità"),
    (N.Dataset, "Dataset"),
    (N.StatoEpistemico, "StatoEpistemico"),
    (N.FiloTrasversale, "FiloTrasversale"),
]


def label(g, uri):
    v = g.value(uri, SKOS.prefLabel) or g.value(uri, RDFS.label)
    return str(v) if v is not None else str(uri).split("#")[-1]


def slug(uri):
    return str(uri).split("#")[-1]


def tipi_di(g, uri):
    tipi_uri = set(g.objects(uri, RDF.type))
    return [nome for uri_tipo, nome in TIPI if uri_tipo in tipi_uri]


def main():
    g = rdflib.Graph()
    for f in DATA_FILES:
        g.parse(f, format="turtle")

    # skos:OrderedCollection (i 3 fili trasversali): il memberList è una lista
    # RDF (blank node a catena), non un arco singolo — sintetizziamo un arco
    # semplice "contiene" filo->membro per ciascun elemento, invece di esporre
    # la struttura a lista che il browser non avrebbe motivo di dover capire.
    fili_archi = []
    for filo in g.subjects(RDF.type, SKOS.OrderedCollection):
        lista = g.value(filo, SKOS.memberList)
        if lista:
            for membro in g.items(lista):
                fili_archi.append((filo, membro))

    nodi_ids = set()
    archi = []

    for prop, lbl_dir, lbl_inv, categoria in PROPRIETA:
        for s, o in g.subject_objects(prop):
            if not isinstance(o, rdflib.URIRef):
                continue  # scarta i valori letterali (non dovrebbero comparire qui)
            archi.append({
                "da": slug(s), "a": slug(o), "prop": slug(prop),
            })
            nodi_ids.add(s)
            nodi_ids.add(o)

    for filo, membro in fili_archi:
        archi.append({"da": slug(filo), "a": slug(membro), "prop": "contieneNelFilo"})
        nodi_ids.add(filo)
        nodi_ids.add(membro)

    grado = {}
    for a in archi:
        grado[a["da"]] = grado.get(a["da"], 0) + 1
        grado[a["a"]] = grado.get(a["a"], 0) + 1

    nodi = []
    for uri in sorted(nodi_ids, key=slug):
        sid = slug(uri)
        nodi.append({
            "id": sid,
            "label": label(g, uri),
            "tipi": tipi_di(g, uri) or ["FiloTrasversale" if (uri, RDF.type, SKOS.OrderedCollection) in g else "Altro"],
            "grado": grado.get(sid, 0),
        })

    proprieta_meta = {
        slug(prop): {"diretta": lbl_dir, "inversa": lbl_inv, "categoria": categoria}
        for prop, lbl_dir, lbl_inv, categoria in PROPRIETA
    }
    proprieta_meta["contieneNelFilo"] = {
        "diretta": "contiene, in ordine", "inversa": "fa parte del filo", "categoria": "struttura",
    }

    out = {
        "generato": "2026-09-04",
        "nota": "Vista a grafo di src/*.ttl (root) — generata, sola lettura. Vedi docs/decisioni-modellazione.md per il modello sorgente.",
        "nodi": nodi,
        "archi": archi,
        "proprieta": proprieta_meta,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    contenuto = "const GRAFO = " + json.dumps(out, ensure_ascii=False, indent=1) + ";\n"
    OUT.write_text(contenuto, encoding="utf-8")
    print(f"Scritto {OUT}: {len(nodi)} nodi, {len(archi)} archi.")


if __name__ == "__main__":
    main()
