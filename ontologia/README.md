# vocabolario-ontologia-llm

Un vocabolario controllato (SKOS) e una micro-ontologia (OWL) costruiti su un dominio
reale — il saggio interattivo "Dal bit alle entità semantiche" (ex corso "Come
funzionano i LLM") — validati con un reasoner e con SHACL, interrogabili via SPARQL da
riga di comando, e derivati in una struttura di consultazione HTML/CSS navigabile.
Pezzo di portfolio per ruoli di metadati, vocabolari controllati e architettura
dell'informazione.

**Il deliverable primario è [`docs/decisioni-modellazione.md`](docs/decisioni-modellazione.md)**,
non il codice: è il resoconto di dove il modello ha dovuto scegliere fra due strade
entrambe difendibili, perché ho preso quella che ho preso, e cosa quella scelta ha
lasciato fuori. Il codice e i dati esistono per dare a quel documento qualcosa di
verificabile da indicare, non il contrario.

## Cosa dimostra

Due competenze che di norma stanno in stanze separate:

1. **Modellazione formale** — `src/vocabolario.ttl` (111 concetti SKOS, gerarchia
   disciplinata genere-specie/parte-tutto, 3 percorsi di lettura ordinati) e
   `src/ontologia.ttl` (9 classi OWL — inclusa `Parte`, aggiunta il 4 settembre 2026
   quando il saggio si è riorganizzato in tre Parti — 17 object property + 2 datatype
   property + 1 annotation property, con caratteristiche formali — transitività, simmetria, disgiunzione —
   verificate, non solo dichiarate: `scripts/valida.py` chiude il grafo con un
   reasoner OWL-RL e controlla la disgiunzione classe per classe, e l'ontologia è
   **nel profilo OWL 2 DL** e **coerente secondo HermiT** (vedi «Verifica formale»).
2. **Architettura dell'informazione** — `output/`, una struttura di consultazione
   HTML/CSS vanilla in quattro viste (glossario, moduli, fili trasversali, teorici)
   generata dal grafo RDF, verificata contro compiti di ricerca concreti in browser, non
   solo contro la coerenza del modello.

## Struttura

```
src/
  vocabolario.ttl    schema SKOS — scritto a mano (Fase 2)
  ontologia.ttl       classi e proprietà OWL — scritto a mano (Fase 3)
  dati.ttl            popolamento — generato da scripts/genera_dati.py (Fase 4)
  shapes.ttl           vincoli SHACL
scripts/
  genera_dati.py      genera src/dati.ttl da strutture dati esplicite
  valida.py            coerenza OWL-RL + conformità SHACL
  query-esempio.py     6 query SPARQL di esempio
  genera_html.py       genera output/ dal grafo RDF
output/                struttura di consultazione statica (195 pagine), aprire output/index.html
docs/
  decisioni-modellazione.md   deliverable primario — le scelte di modellazione, argomento per argomento
  decision-log.md              cronologia dei fatti del progetto
  termini-grezzi.md            estrazione grezza di Fase 1, con fonti e casi dubbi dichiarati
  next-steps.md / snapshot.md  stato del lavoro
```

## Il dominio

Il saggio interattivo "Dal bit alle entità semantiche" (`~/projects/cartografia-semantica/src/saggio/`,
progetto sorella, **sola lettura** — mai modificato da qui). Nato come corso "Come
funzionano i LLM" dentro `qa-tool/`, estratto in un repository proprio e trasformato in
saggio in tre Parti (Fondamenti/Genealogia/Meccanismo) il 2 settembre 2026. Materiale
interamente scritto dall'autore; nessun dato personale di terzi; verificato contro i tre
vincoli del dominio in `docs/decision-log.md`. Il modello è un'**istantanea del saggio al
26 agosto 2026, aggiornata alla nuova struttura il 4 settembre 2026** — stato dichiarato
definitivo dall'autore in quella data; il vocabolario comunque non si aggiorna da solo se
il saggio cambia ancora.

## Riprodurre

Ambiente Python isolato, reinstallabile da zero (verificato: un venv pulito installato
solo da `requirements.txt` riproduce risultati identici):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Validare (coerenza logica OWL-RL + conformità SHACL):

```bash
.venv/bin/python3 scripts/valida.py
```

**Cosa questa validazione copre, e cosa no.** Due controlli, non uno. Il primo
chiude deduttivamente il grafo con un reasoner OWL-RL (1.775 triple → chiusura) e
verifica che `owl:Nothing` resti vuoto. Il secondo verifica la **disgiunzione**
classe per classe, sulla forma che questo file usa davvero.

Il secondo esiste perché il primo, da solo, non bastava — e lo si è scoperto il
25 settembre 2026, quando HermiT ha dichiarato incoerente un'ontologia che
`valida.py` dava per buona. La ragione è precisa: la disgiunzione qui è scritta
come `owl:AllDisjointClasses` con `owl:members`, e `owlrl` implementa la regola
che agisce sulla forma `owl:disjointWith` — che in questo grafo non compare mai,
né asserita né derivata. La regola non aveva su cosa scattare, e il controllo
passava mentre misurava altro. Oggi le 21 coppie disgiunte sono verificate
esplicitamente; provato sui dati precedenti alla correzione, dove trova i 64
individui che erano insieme `:Concetto` e `:Teorico`.

**Resta fuori dal profilo RL**, e quindi ignorato dal reasoner: il `rdfs:range`
di `:discussoInUnita` e di `:citatoInUnita` è `owl:unionOf ( :Unita :Capitolo )`,
e OWL 2 RL ammette in posizione di superclasse solo classi nominate. Gli assiomi
sono validi in OWL 2 DL e restano scritti perché descrivono il modello con
precisione — ma nessuna conclusione viene tratta da essi qui.

### Verifica formale con un reasoner DL

L'ontologia è **nel profilo OWL 2 DL** («Ontology and imports closure in
profile») e **coerente** secondo HermiT. Riproducibile con
[ROBOT](http://robot.obolibrary.org/), che non è incluso nel repository — serve
un runtime Java e `robot.jar` dalle release del progetto:

```bash
.venv/bin/python3 -c "import rdflib; g=rdflib.Graph(); \
  [g.parse(f) for f in ['src/vocabolario.ttl','src/ontologia.ttl','src/dati.ttl']]; \
  g.serialize(destination='/tmp/unito.ttl', format='turtle')"
java -jar robot.jar validate-profile --profile DL --input /tmp/unito.ttl
java -jar robot.jar reason --reasoner hermit --input /tmp/unito.ttl --output /tmp/ragionato.ttl
```

Il 25 settembre 2026 questo controllo riportava **738 violazioni di profilo** e
un'ontologia incoerente. Le violazioni erano tutte di dichiarazione: SKOS e
Dublin Core sono usati senza `owl:imports` (scelta documentata: il namespace non
è dereferenziabile), e in OWL 2 DL ogni IRI deve essere dichiarato. Senza
dichiarazione il reasoner indovinava, e indovinava male — `skos:broader`
risultava una proprietà di *annotazione*, cioè ignorata da ogni inferenza, pur
essendo la gerarchia portante del vocabolario. I termini esterni sono ora
dichiarati in fondo a `ontologia.ttl` con il tipo che SKOS attribuisce loro.

Interrogare il grafo (6 query di esempio: concetti-cardine, catena di prerequisiti
transitiva, filo trasversale in ordine, lacune di popolamento, teorici più citati,
dataset per stato epistemico):

```bash
.venv/bin/python3 scripts/query-esempio.py
```

Rigenerare popolamento e struttura di consultazione dopo una modifica a
`vocabolario.ttl` o `ontologia.ttl`:

```bash
.venv/bin/python3 scripts/genera_dati.py > src/dati.ttl
.venv/bin/python3 scripts/genera_html.py
```

Consultare: aprire `output/index.html` in un browser (nessun server necessario — tutti
i link sono relativi).

## Vincoli tecnici seguiti

Nessun build tooling. HTML/CSS vanilla. Font self-hosted con licenza OFL (EB Garamond,
variabile, scaricato dal repository ufficiale Google Fonts — non linkato da un CDN a
runtime). RDF in Turtle sotto controllo di versione, leggibile in diff. Validazione e
query da riga di comando, ambiente Python isolato e reinstallabile.

## Stato

Tutte le sette fasi del piano approvato sono complete (26 agosto 2026). Aggiornate il
4 settembre 2026 per la nuova struttura in tre Parti del saggio estratto — nuova classe
`Parte`, rinumerazione di 51 concetti, 3 nuovi Teorici (Peirce, Post, Shatz). Verifica
end-to-end più recente: validazione OWL-RL + SHACL conforme, 1656 link interni della
struttura di consultazione verificati (0 rotti), reinstallazione da `requirements.txt`
in un venv pulito verificata. Dettagli in `docs/snapshot.md`.
