# Decision log — vocabolario-ontologia-llm

## 2026-08-26 — Bootstrap del progetto

Creato il repository con lo scaffolding standard di `~/projects/` (vedi
`memoria/governance_new_projects.md`), a partire da un piano approvato in modalità piano
(salvato in `~/.claude/plans/`).

Dominio scelto: il corso "Come funzionano i LLM" (`qa-tool/src/corso-llm/`) — Modulo 00
narrativo (Blocchi A-D) e Moduli tecnici 1-6, con i tre fili trasversali già presenti nel
materiale (discreto/continuo; Galileo/crollo quantistico; logica-informazione-biologia
della cognizione). Verificato contro i tre vincoli del dominio:

- **Diritti**: `corso-llm` è interamente scritto dall'utente. Le citazioni presenti (von
  Neumann, Wei et al., Bacone/Bayle, Herculano-Houzel, Ouyang et al.) sono riferimenti
  fattuali a lavori pubblicati, non riproduzione di testo altrui.
- **Nessun dato personale di terzi**: i dati sensibili di `qa-tool` (interviste un progetto di ricerca,
  materiale di un collaboratore terzo) vivono in `capstone-qualitativo/` e `data/`, cartelle
  sorelle mai toccate da questo progetto.
- **Complessità**: decine di concetti tecnici, teorici citati, moduli/unità, dataset
  verificati, relazioni di prerequisito/analogia/contrapposizione già esplicitate in
  prosa nel corso — sufficiente per un'ontologia, non solo una lista.

**Nota sulla fonte**: `corso-llm` è segnato nel proprio `CLAUDE.md` come "non definitivo,
revisione manuale dell'utente in corso". Questo progetto legge quel materiale come fonte
di riferimento per estrarne terminologia, senza modificarlo. Il vocabolario riflette lo
stato del corso **alla data odierna (26 agosto 2026)** — un'istantanea datata, non una
fonte che si aggiorna da sola. Se il corso cambierà in modo sostanziale, andrà
rivalutato esplicitamente, non aggiornato in automatico.

**Nota operativa**: la cartella è stata creata con percorsi assoluti da una sessione
radicata in un worktree della root (`.claude/worktrees/worktree`, branch
`branch`), non nella root reale — stesso precedente già
documentato in `qa-tool/docs/decision-log.md` (nota del 2026-07-05). Nessun worktree
aggiuntivo creato per questo bootstrap.

## 2026-09-04 — Aggiornamento post-estrazione: cartografia-semantica

Tra il bootstrap e oggi, l'utente ha estratto il corso da `qa-tool/src/corso-llm/` in un
repository indipendente, `~/projects/cartografia-semantica/` (storia git preservata via
`git filter-repo`), e lo ha trasformato: non più un corso a lezioni numerate ma un saggio
in tre Parti (Fondamenti/Genealogia/Meccanismo), titolo "Dal bit alle entità semantiche",
~20 citazioni storiche verificate (2 errori reali corretti — attribuzione della frase
"neurons that fire together, wire together" a Hebb invece che a Carla Shatz; titolo
anacronistico di McCulloch), e una nuova appendice "Dietro i widget".

**Verifica preliminare, non presa per buona sul solo resoconto dell'utente**: tre
sub-agenti Explore lanciati in parallelo (inventario strutturale completo di
`cartografia-semantica`, audit di ogni riferimento obsoleto in questo progetto, verifica
puntuale delle citazioni corrette contro il testo attuale). Uno dei tre è fallito per
limite di sessione (rate limit, non un problema di merito) — rieseguito a mano con query
dirette invece di ritentare lo spawn. La verifica ha trovato due discrepanze reali col
resoconto iniziale dell'utente (poi chiarite e risolte insieme): il file compilato non
era ancora rinominato e l'appendice viveva solo in un worktree non ancora unito a `main`
— entrambe sistemate dall'utente prima di procedere. Ha anche trovato, come effetto
collaterale non richiesto, un'incoerenza reale nel saggio stesso: la correzione
Hebb/Shatz è presente in `genealogia-3-villaggio.html` ma non nel passaggio parallelo di
`meccanismo-4-reti-neurali.html` — segnalata all'utente, non corretta qui (non è un file
di questo repository).

**Cosa è cambiato nel modello** (piano completo in `~/.claude/plans/`, tutte le fasi
verificate prima di passare alla successiva):

- Nuova classe OWL `:Parte` (Fondamenti/Genealogia/Meccanismo); `:Modulo` rinominata
  `:Capitolo`, `:partOfModulo` rinominata `:partOfCapitolo`; nuova `:partOfParte`.
  `owl:AllDisjointClasses` da 6 a 7 membri.
- Il range di `:discussoInUnita` allargato a `owl:unionOf(:Unita :Capitolo)`: i 2
  Capitoli di Fondamenti non hanno sotto-unità e restano il bersaglio citabile più fine,
  invece di essere dual-tipizzati anche `:Unita` (che avrebbe richiesto un
  `:partOfCapitolo` auto-referenziale) — verificato con un test isolato via owlrl prima
  di investire nel resto (rischio #2 del piano, disinnescato).
- Tutti i 111 valori `:fonte` di `vocabolario.ttl` riscritti sulla nuova numerazione
  (vecchi codici Blocco A-D/Modulo 00 → Genealogia/Fondamenti), tramite una funzione di
  trasformazione scritta e testata prima di essere applicata (zero errori su 111 valori,
  inclusi i casi con virgola dentro punto e virgola). 5 `scopeNote` che citavano ancora
  "Blocco"/"Modulo 00" come testo vivo, aggiornate.
- `scripts/genera_dati.py` ristrutturato (`PARTI`+`CAPITOLI` al posto di `MODULI`); 3
  nuovi Teorico — Peirce ed Emil Post (ora con contenuto reale in Fondamenti, prima
  Peirce era solo un'intestazione, caso dubbio escluso in Fase 2), Carla Shatz (nuova,
  dalla correzione Hebb) — nessuna relazione `teorizzatoDa` forzata per i tre.
- Trovato e corretto un gap non previsto dal piano: `src/shapes.ttl` referenziava ancora
  `:partOfModulo`/`:Modulo`, 47 violazioni SHACL al primo tentativo — corretto
  (`:ModuloShape`→`:CapitoloShape`, nuova `:ParteShape`).
- `scripts/genera_html.py` riscritto oltre la semplice rinomina: le pagine Concetto/
  Teorico assumevano che ogni bersaglio di `discussoInUnita` avesse un genitore
  Capitolo/Modulo — falso per i 2 Capitoli di Fondamenti (bersaglio diretto, nessun
  genitore da risolvere), avrebbe prodotto link rotti verso `moduli/None.html`. Isolato
  in un helper dedicato (`href_citabile`), verificato in browser. Rimossa anche una
  funzione (`href()`) rimasta morta dalla Fase 5 originale, mai chiamata.
- Cornice "non definitivo" aggiornata a "dichiarato definitivo dall'autore al 4 settembre
  2026" in tutti i file, su richiesta esplicita dell'utente.

**Verifica end-to-end finale**: rigenerazione completa (dati + HTML), OWL-RL (zero
incoerenze) + SHACL (conforms) entrambe OK, 1656 link interni verificati (0 rotti, erano
1606 prima dell'aggiornamento — 195 pagine totali, erano 187). Dettagli completi delle
decisioni di modellazione in `docs/decisioni-modellazione.md`, sezione "Aggiornamento
post-estrazione".
