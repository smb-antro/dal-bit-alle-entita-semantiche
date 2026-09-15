# Snapshot — vocabolario-ontologia-llm

**26 agosto 2026** — Bootstrap completato: scaffolding di repository, `.gitignore`,
`CLAUDE.md`, `README.md`, `docs/`, venv con `rdflib`/`pyshacl` (`requirements.txt`).
Fase 1 completata: `docs/termini-grezzi.md` (367 righe) — ~85 Concetti, 18
Tecniche/Algoritmi, ~55 Teorici/Autori citati, mappa completa di Moduli/Unità, 15
Dataset/Asset, 3 Fili trasversali, ~38 relazioni osservate.

Fase 2 completata: `src/vocabolario.ttl` — schema SKOS con 111 skos:Concept (14 top
concept + 97 narrower, validato con rdflib: 748 triple, gerarchia coerente) e 3
skos:OrderedCollection per i fili trasversali. Prima versione di
`docs/decisioni-modellazione.md` scritta (9 decisioni motivate).

Fase 3 completata: `src/ontologia.ttl` — 8 classi OWL (Concetto≡skos:Concept, Tecnica,
Teorico, Modulo, Unità, Dataset, FiloTrasversale, StatoEpistemico), 15 object property +
2 datatype property, 18 individui ritipizzati `:Tecnica`. Validato con rdflib (914 triple
SKOS+OWL) e con reasoner owlrl (chiusura a 2004 triple, inferenza corretta, zero
incoerenze via owl:Nothing). 5 nuove decisioni in `docs/decisioni-modellazione.md`.

Fase 4 completata: `scripts/genera_dati.py` genera `src/dati.ttl` (7 Moduli, 49 Unità, 61
Teorici, 16 Dataset, 259 discussoInUnita, 47 teorizzatoDa, 26 relazioni fra concetti).
`src/shapes.ttl` (SHACL: campi obbligatori, lingua, assenza di cicli in prerequisitoDi).
`scripts/valida.py` (OWL-RL + SHACL, entrambi OK: 1703→3562 triple, zero incoerenze,
conforms=True) e `scripts/query-esempio.py` (6 query, tutte verificate a mano) da riga di
comando. 8 nuove decisioni in `docs/decisioni-modellazione.md`, inclusi i gap dichiarati
(relazioni di Fase 1 non mappate per assenza di nodo target).

Fase 5 completata: `scripts/genera_html.py` genera 195 pagine statiche in `output/`
(111 concetti, 12 capitoli, 3 fili trasversali, 64 teorici, 5 indice/home) + `style.css` +
font EB Garamond self-hosted (WOFF2, scaricati da google/fonts, OFL). Verificato in
browser reale (server locale su `python3 -m http.server`): 1606 link interni, 0 rotti
dopo la correzione di un bug reale (pagine Modulo mescolavano Concetti e Teorici nella
stessa lista). Tre compiti d'uso concreti eseguiti e documentati in
`docs/decisioni-modellazione.md` (prerequisiti di RLHF, filo discreto/continuo, ricerca
per Bateson).

Fase 6 completata: `docs/decisioni-modellazione.md` riscritto in forma finale — da log
per fase (2-3-4-5, 28 voci numerate) a saggio in prosa organizzato per argomento (6
sezioni tematiche + limiti noti + sintesi), senza perdere nessuna decisione registrata.

Fase 7 completata: `README.md` finale scritto per un lettore esterno (recruiter),
con `docs/decisioni-modellazione.md` indicato esplicitamente come deliverable primario.
**Verifica end-to-end** (26 agosto 2026, tutta rieseguita da zero in questa fase):
- Rigenerazione completa: `genera_dati.py` → `dati.ttl` (1703 triple totali) →
  `genera_html.py` → 187 pagine.
- `valida.py`: coerenza OWL-RL (1703→3562 triple, zero `owl:Nothing`) e conformità
  SHACL (`conforms: True`) — entrambi OK.
- `query-esempio.py`: 6 query eseguite, risultati coerenti con Fase 4 (14 concetti
  cardine, catena transitiva Rlhf, filo discreto/continuo in ordine, 0 concetti senza
  fonte, top 5 teorici, 12 dataset reali/4 illustrativi).
- Link check: 1606 link interni della struttura di consultazione, 0 rotti.
- **Riproducibilità verificata**: `requirements.txt` reinstallato in un venv pulito e
  isolato (`/tmp/verifica-venv-reinstall`, poi rimosso) — `valida.py` eseguito lì
  produce lo stesso risultato (1703→3562 triple, conforms=True), confermando che
  l'ambiente è ricostruibile da zero senza dipendenze non dichiarate.

Tutte le sette fasi del piano approvato sono complete. **Commit iniziale effettuato**
(`55cc1c4`, su richiesta esplicita dell'utente) — nota corretta qui perché questa
voce diceva ancora "nessun commit" mesi dopo il fatto, non aggiornata a suo tempo.

## 2026-09-04 — Aggiornamento post-estrazione: cartografia-semantica

Il corso è stato estratto da `qa-tool/` in `~/projects/cartografia-semantica/` e
trasformato in saggio a tre Parti (Fondamenti/Genealogia/Meccanismo). Modello
aggiornato di conseguenza, non ricostruito da zero — verificato in modalità piano con
"la massima scrupolosità" richiesta esplicitamente dall'utente: tre sub-agenti Explore
in parallelo (uno fallito per rate limit di sessione, rieseguito a mano) prima di
scrivere una riga di codice.

- **Schema** (`src/ontologia.ttl`): nuova classe `:Parte`, `:Modulo`→`:Capitolo`,
  `:partOfModulo`→`:partOfCapitolo`, nuova `:partOfParte`, range di `:discussoInUnita`
  allargato a `owl:unionOf(:Unita :Capitolo)` — verificato con un test owlrl isolato
  prima di procedere.
- **Vocabolario** (`src/vocabolario.ttl`): tutti i 111 valori `:fonte` riscritti sulla
  nuova numerazione tramite una funzione scritta e testata (0 errori su 111, verificata
  a campione sui casi complessi prima dell'applicazione); 5 scopeNote con riferimenti
  "Blocco"/"Modulo 00" vivi aggiornate; titolo/descrizione/cornice "definitivo"
  aggiornati.
- **Popolamento** (`scripts/genera_dati.py`): ristrutturato `PARTI`+`CAPITOLI`; 3 nuovi
  Teorico (Peirce, Post, Shatz), nessuna relazione forzata per loro.
- **Due gap non previsti dal piano, trovati dalla validazione stessa e corretti**:
  `src/shapes.ttl` ancora su `:partOfModulo`/`:Modulo` (47 violazioni SHACL al primo
  giro); `scripts/genera_html.py` assumeva sempre un'Unità con Capitolo genitore,
  falso per i 2 Capitoli di Fondamenti (avrebbe rotto i link) — isolato in
  `href_citabile`, verificato in browser. Rimossa anche una funzione morta
  (`href()`) mai chiamata, invece di aggiornarla.
- **Scoperta collaterale fuori perimetro**: un'incoerenza reale nel saggio sorgente
  (correzione Hebb/Shatz presente in Genealogia ma non nel passaggio parallelo di
  Meccanismo) — segnalata all'utente, non corretta qui.

**Verifica end-to-end finale**: OWL-RL (1739→3716 triple, zero incoerenze) + SHACL
(conforms=True) entrambe OK; 1656 link interni su 195 pagine (erano 1606 su 187),
0 rotti. Nuova sezione "Aggiornamento post-estrazione" in
`docs/decisioni-modellazione.md`; nuova voce datata in `docs/decision-log.md` (le
voci precedenti non riscritte). Nessun nuovo commit ancora effettuato per questo
aggiornamento.
