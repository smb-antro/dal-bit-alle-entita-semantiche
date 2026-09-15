#!/usr/bin/env python3
"""Query SPARQL di esempio contro il grafo popolato — verifica che il modello
sia davvero interrogabile, non solo sintatticamente valido.

Uso: .venv/bin/python3 scripts/query-esempio.py
"""
import rdflib

DATA_FILES = ["src/vocabolario.ttl", "src/ontologia.ttl", "src/dati.ttl"]
PREFIXES = """
PREFIX : <https://smb-antro.github.io/dal-bit-alle-entita-semantiche/vocabolario#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
"""


def carica_grafo():
    g = rdflib.Graph()
    for f in DATA_FILES:
        g.parse(f, format="turtle")
    return g


def label_di(g, uri):
    lbl = g.value(uri, rdflib.URIRef("http://www.w3.org/2004/02/skos/core#prefLabel"))
    if lbl is None:
        lbl = g.value(uri, rdflib.RDFS.label)
    return str(lbl) if lbl is not None else str(uri).split("#")[-1]


def esegui(g, titolo, query):
    print(f"\n=== {titolo} ===")
    risultati = list(g.query(PREFIXES + query))
    if not risultati:
        print("(nessun risultato)")
    for row in risultati:
        print(" -", " | ".join(str(v) for v in row))
    return risultati


def main():
    g = carica_grafo()
    print(f"Grafo caricato: {len(g)} triple.")

    # 1. Concetti-cardine (senza skos:broader) — dovrebbero essere esattamente
    #    i 14 top concept dello schema SKOS.
    esegui(g, "Concetti-cardine (senza skos:broader)", """
        SELECT ?label WHERE {
            ?c a skos:Concept .
            FILTER NOT EXISTS { ?c skos:broader ?qualsiasi }
            ?c skos:prefLabel ?label .
        } ORDER BY ?label
    """)

    # 2. Catena di prerequisiti per raggiungere RLHF (via SPARQL property path
    #    sulla proprietà transitiva prerequisitoDi: dimostra che la chiusura
    #    transitiva ModelloDiBase -> FineTuning -> Rlhf viene attraversata in
    #    un solo passo di query, non solo il collegamento diretto).
    esegui(g, "Catena di prerequisiti per arrivare a :Rlhf", """
        SELECT ?label WHERE {
            ?c :prerequisitoDi+ :Rlhf .
            ?c skos:prefLabel ?label .
        } ORDER BY ?label
    """)

    # 3. Tutti i concetti del filo trasversale discreto/continuo, nell'ordine
    #    dichiarato nella skos:OrderedCollection.
    print("\n=== Filo trasversale «discreto/continuo», in ordine ===")
    lista = g.value(rdflib.URIRef("https://smb-antro.github.io/dal-bit-alle-entita-semantiche/vocabolario#FiloDiscretoContinuo"),
                     rdflib.URIRef("http://www.w3.org/2004/02/skos/core#memberList"))
    membri = list(g.items(lista)) if lista else []
    for m in membri:
        print(" -", label_di(g, m))

    # 4. Concetti senza alcun discussoInUnita — segnala lacune di popolamento.
    esegui(g, "Concetti senza :discussoInUnita (lacune di popolamento)", """
        SELECT ?label WHERE {
            ?c a skos:Concept .
            FILTER NOT EXISTS { ?c :discussoInUnita ?qualsiasi }
            ?c skos:prefLabel ?label .
        } ORDER BY ?label
    """)

    # 5. I cinque Teorici più citati (per numero di concetti che teorizzano).
    esegui(g, "Teorici con più concetti teorizzati (top 5)", """
        SELECT ?label (COUNT(?c) AS ?n) WHERE {
            ?c :teorizzatoDa ?t .
            ?t rdfs:label ?label .
        } GROUP BY ?label ORDER BY DESC(?n) LIMIT 5
    """)

    # 6. Dataset per stato epistemico.
    esegui(g, "Dataset per stato epistemico", """
        SELECT ?stato (COUNT(?d) AS ?n) WHERE {
            ?d a :Dataset ; :haStatoEpistemico ?s .
            ?s rdfs:label ?stato .
        } GROUP BY ?stato
    """)


if __name__ == "__main__":
    main()
