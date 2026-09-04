#!/usr/bin/env python3
"""Valida vocabolario.ttl + ontologia.ttl + dati.ttl in due passi indipendenti:

1. Coerenza logica OWL-RL (owlrl): il grafo, chiuso deduttivamente, non deve
   produrre alcuna istanza di owl:Nothing (violazione delle disjointness fra
   Concetto/Teorico/Modulo/Unita/Dataset/FiloTrasversale, o di cardinalità
   funzionale su partOfModulo/haStatoEpistemico/dataVerifica).
2. Forma dei dati (pySHACL contro src/shapes.ttl): campi obbligatori, lingua
   delle etichette, assenza di cicli in prerequisitoDi.

I due passi sono deliberatamente separati (non un'unica chiamata pyshacl con
inference='rdfs'): un errore di coerenza logica e una violazione di forma sono
categorie diverse di problema, e tenerle distinte rende più facile capire dove
guardare quando qualcosa fallisce.

Uso: .venv/bin/python3 scripts/valida.py
"""
import sys
import rdflib
from rdflib.namespace import RDF, OWL
import owlrl
from pyshacl import validate

DATA_FILES = ["src/vocabolario.ttl", "src/ontologia.ttl", "src/dati.ttl"]
SHAPES_FILE = "src/shapes.ttl"


def carica_grafo_dati():
    g = rdflib.Graph()
    for f in DATA_FILES:
        g.parse(f, format="turtle")
    return g


def verifica_coerenza_owl(g):
    print("--- 1. Coerenza logica (OWL-RL) ---")
    chiuso = rdflib.Graph()
    chiuso += g
    prima = len(chiuso)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(chiuso)
    dopo = len(chiuso)
    print(f"Triple prima della chiusura: {prima}")
    print(f"Triple dopo la chiusura:      {dopo}")
    incoerenti = list(chiuso.subjects(RDF.type, OWL.Nothing))
    if incoerenti:
        print(f"INCOERENTE: {len(incoerenti)} individui inferiti come owl:Nothing:")
        for i in incoerenti:
            print(f"  - {i}")
        return False
    print("Nessuna incoerenza (owl:Nothing vuoto).")
    return True


def verifica_forma_shacl(g):
    print("\n--- 2. Forma dei dati (SHACL) ---")
    shapes = rdflib.Graph()
    shapes.parse(SHAPES_FILE, format="turtle")
    conforms, results_graph, results_text = validate(
        g, shacl_graph=shapes, inference="none", abort_on_first=False
    )
    print(results_text)
    return conforms


def main():
    g = carica_grafo_dati()
    print(f"Grafo caricato: {len(g)} triple da {', '.join(DATA_FILES)}\n")

    owl_ok = verifica_coerenza_owl(g)
    shacl_ok = verifica_forma_shacl(g)

    print("\n--- Esito ---")
    print(f"Coerenza OWL-RL: {'OK' if owl_ok else 'FALLITA'}")
    print(f"Forma SHACL:     {'OK' if shacl_ok else 'FALLITA'}")

    if not (owl_ok and shacl_ok):
        sys.exit(1)


if __name__ == "__main__":
    main()
