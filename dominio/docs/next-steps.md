# Next steps — corso-llm

- **Revisione editoriale completa di Genealogia/Meccanismo, rinomina in saggio/, sidebar
  unica nel compilato, estrazione in repository proprio (2 settembre 2026)**: dettagli
  completi in decision-log. Il saggio è ora nel proprio repository
  (`~/projects/corso-llm/`), storia git preservata via `git filter-repo`.

- **Presentazione del case study "Dal bit alle entità semantiche" riscritta (1 settembre
  2026)**: titolo, sottotitolo, apertura (gioco linguistico re/donna/regina, due fasi,
  agente AI, mercato del lavoro) e le tre Parti (Framework epistemologico; Il dominio:
  struttura e composizione del saggio interattivo; La lente semantica) riscritte in
  `src/corso-llm/build_output.py` (`build_intro_and_toc()`) e in
  `src/corso-llm/lezioni/presentazione.html` — le due copie duplicate deliberatamente
  (scelta esplicita dell'utente), da tenere allineate a mano a ogni modifica futura.
  Sidebar fissa con indice ad accordion (compresi i pallini luminosi di scroll-spy sulle
  tre Parti) aggiunta a `presentazione.html`, e voce "Presentazione" aggiunta come
  accordion anche in `lezioni/indice.html`.
- **Pagina "Lente semantica" interattiva — da costruire, non ancora iniziata (1 settembre
  2026)**: Claude Design ha proposto 4 tavole per una cartografia visiva del
  vocabolario/ontologia (Atlante topografico, Matrice riordinabile, Lente semantica,
  Flusso corso↔vocabolario — export in `src/corso-llm/Cartografia semantica dei LLM.zip`).
  Decisione dell'utente: solo la tavola "Lente semantica" (un termine alla volta, vicini
  di 1°/2° grado raggruppati per relazione) va ricostruita come componente interattivo,
  in una pagina dedicata linkata da Parte 3 della Presentazione — **da fare dopo
  l'aggiornamento dell'ontologia stessa a editing del saggio concluso**, non prima (i dati
  della tavola riflettono l'ontologia pre-editing). Le altre tre tavole restano proposte
  non ancora assegnate a una destinazione.
- **Fase 1 completata (2026-07-07)**: revisione di tono su tutti i 12 file di
  `src/corso-llm/lezioni/` (Modulo 00 narrativo completo + Moduli 1-6 tecnici), da
  registro narrativo/pedagogico a professionale/accademico. Checkpoint sull'Unità 1.1
  confermato dall'utente prima di propagare a tutti gli altri file. Verifica meccanica OK
  su tutti e 12 (HTML ben formato, id invariati, `<script>`/`<style>` identici
  byte-per-byte, sintassi JS con motore reale). Nessun fatto/citazione/domanda aperta
  alterato. Dettagli completi in decision-log. Commit di questa fase in arrivo.
- **Piano rivisto dall'utente (2026-07-07)**: le traduzioni EN/FR/DE (Fasi 3, prompt 3-8)
  sono rimandate a fine progetto, non urgenti — annotato nel file dei prompt.
- **Verifica interattiva dei widget completata (2026-07-07)**: tutti gli 8 file con widget
  reali testati dal vivo in browser (workaround scratchpad+server, funzionante al primo
  tentativo). Un bug reale trovato e corretto in `lezione_02_probabilita.html` (etichetta
  "parolae"→"parole" nella funzione condivisa del predittore n-grammi). Tutto il resto
  verificato corretto, incluso il widget WebGL/shader del Modulo 4 (riletto pixel per
  pixel). Fable sospeso per questo compito su richiesta dell'utente — verifica e fix fatti
  direttamente in conversazione. Dettagli completi, incluse le note metodologiche sul tool
  di anteprima (limiti di `preview_click` su elementi SVG e su pagine con
  `visibilityState:"hidden"`, timing dei widget con fade via `setTimeout`), in decision-log.
- **Fase 2 completata (2026-07-07)**: `output/dal-bit-alle-entita-semantiche_it.html` — tutti e 12 i
  file compilati in un unico documento autocontenuto, con indice, introduzione originale,
  navigazione a tre livelli (barra capitoli + topbar-unità + rail-sezioni) e tema
  chiaro/scuro con persistenza. Namespacing per capitolo (id univoci, IIFE, query scoped)
  gestito da `src/corso-llm/build_output.py`, script riutilizzabile lasciato nel progetto
  (servirà anche per le Fasi 3 EN/FR/DE). Tre bug reali introdotti dal meccanismo di
  namespacing trovati e corretti prima della consegna (collisione id/class, riferimenti id
  in forme sintattiche non previste — chiavi `*Id:`, argomenti posizionali, selettori `#id`
  in stringhe —, timing di `IntersectionObserver` su capitoli inizialmente nascosti).
  Palette del tema chiaro rifatta una volta su segnalazione esplicita dell'utente (niente
  beige/sabbia neutro, stessa tinta verde/rame del tema scuro solo con contrasto invertito).
  Verifica meccanica completa (sintassi JS reale, HTML ben formato, 440 id univoci, zero
  riferimenti id orfani, 13 dataset incorporati identici byte-per-byte alle costanti
  originali) e interattiva in browser reale (cambio capitolo, widget di più moduli, toggle
  tema con persistenza). Riserva onestamente segnalata: il tool di anteprima aveva
  `document.visibilityState` bloccato su `"hidden"` per questa sessione (limite noto già
  incontrato con lo shader di M4), quindi lo stato "attivo" del rail-dot al primo cambio
  capitolo non è stato confermabile al 100% con lo strumento automatico — verificare con una
  rapida occhiata reale, la logica del fix è comunque corretta nei momenti in cui la
  visibilità era normale. File copiato su Desktop
  (`dal-bit-alle-entita-semantiche_it.html`) per la verifica visiva finale. Dettagli completi,
  inclusi tutti i valori della palette e la spiegazione tecnica dei tre bug, in decision-log.
  Prossimo passo naturale: Fase 3 (traduzioni EN/FR/DE), rimandata su richiesta esplicita
  dell'utente, non ancora da avviare.

- `corso-llm/`, Modulo 00 narrativo **completo**: Blocco A (`lezione_00_blocco_a.html`,
  Unità A.1-A.6), Blocco B (`lezione_00_blocco_b.html`, Unità B.1-B.3), Blocco C
  (`lezione_00_blocco_c.html`, Unità C.1-C.5) e Blocco D (`lezione_00_blocco_d.html`,
  Unità D.1-D.2, che chiude anche l'intero Modulo 00 con raccordo al Modulo 0 tecnico).
  Lavoro da proseguire sullo stesso branch/worktree `corso-llm-moduli-1-6`.
- Verifica visiva in browser di tutti e tre i file (`lezione_00_blocco_b.html`,
  `lezione_00_blocco_c.html`, `lezione_00_blocco_d.html`) fatta dall'utente e confermata
  positiva. Modulo 00 narrativo (A-D) da considerarsi chiuso a tutti gli effetti.
- **Struttura testuale dei Moduli 1-6 completa** (`src/corso-llm/struttura_moduli_1-6.md`,
  committato): scomposizione in unità per tutti i sei moduli tecnici, con il filo
  discreto/continuo tracciato come tema trasversale (non unità a sé). Non è ancora contenuto
  in prosa — solo titoli, temi e note di raccordo interdisciplinare. Dettagli e motivazioni in
  decision-log (voce del 2026-07-06).
- **Pianificazione grafica avviata**: inventario concettuale dei componenti interattivi per
  ciascun modulo (vedi decision-log) — pattern confermato di un componente centrale riusato per
  modulo, non un widget per unità. Blender MCP valutato ed escluso per ora (riservato a
  un'eventuale fase "libro" futura). Idea mantenuta: collegamento tra il widget di M3 (spazio
  embedding) e quello di M5 (attention) — parola polisemica che si muove nello stesso spazio da
  statica a contestuale.
- **Dataset di embedding reali per M3/M5 pronto**: `src/corso-llm/lezioni/embedding_dati_moduli_3_5.json`
  — 23 parole, vettori reali (fastText italiano), tre modalità di coordinate (esplorazione,
  aritmetica, polisemia) con assi costruiti su misura per ciascuna, perché la PCA generica non
  preservava le relazioni volute. Dettagli tecnici completi in decision-log.
- **Struttura testuale rivista con nuovo contesto (fase 1 di revisione, 2026-07-06)**:
  integrati nel `struttura_moduli_1-6.md` il Dialogo Flora/Tolomeo (continuo/discreto, Gödel,
  Cantor, Galileo/quantistico, Lawvere) e la sezione di Calasso su Kelly/digitalizzazione
  universale. Nuova unità 1.5 (Gödel — paga la domanda aperta di Blocco A), rafforzamenti in
  1.1, 1.4, 3.1, 3.2, 3.4, 5.4, 6.3, 6.6. Dettagli completi in decision-log.
- **Fase 2 di revisione completata (2026-07-06)**: nove osservazioni dell'utente (Bateson,
  Varela, deduzione/induzione/abduzione, calibrazione, memristor/BCI, shader/SDF) integrate in
  `struttura_moduli_1-6.md` — nuovo "terzo filo" trasversale (logica/informazione/biologia
  della cognizione) da Modulo 2 a Modulo 4. Due punti esplicitamente rimandati: ragionamento
  causale/Searle (nota aperta, nessuna unità ancora assegnata) e linguaggio shader/SDF
  (decisione di implementazione, non di struttura). Dettagli completi in decision-log.
- **Inventario grafico definitivo completato (2026-07-06)**: consolidato in
  `src/corso-llm/inventario_grafico_moduli_1-6.md`, separato dalla struttura testuale.
  Principio confermato: un componente interattivo centrale per modulo, non un widget per
  unità. Decisione tecnica esplicita: la superficie di perdita di 4.5 userà shader
  GLSL/SDF, prima eccezione al vanilla JS/SVG usato altrove — comporta WebGL, non solo
  Canvas 2D. Dettagli completi in decision-log.
- **Modulo 1 — dati/asset pronti (2026-07-06)**: tokenizzatore BPE reale addestrato sul
  corpus del Modulo 00 (`lezioni/bpe_merges_modulo1.json`, 300 merge, verificato con 0 errori
  di round-trip); cerchio raster+SVG per la comparazione 1.4 (`lezioni/immagini_modulo1/`);
  dati per la diagonale di Cantor 1.5 (`lezioni/cantor_diagonale_modulo1.json`). Nessun dato
  ancora raccolto per M2, M4, M6. Dettagli completi in decision-log.
- **Modulo 2, 4, 6 — dati/asset pronti (2026-07-06, sessione in modalità piano)**: rete XOR
  addestrata e verificata (`lezioni/xor_rete_modulo4.json`, 4/4 corretto), superficie di
  perdita specificata e verificata numericamente per lo shader GLSL/SDF
  (`lezioni/paesaggio_perdita_modulo4.json`), esempi del neurone singolo
  (`lezioni/neurone_esempi_modulo4.json`); corpus conversazionale scritto apposta e tabelle
  n-grammi (`lezioni/ngram_dati_modulo2.json`), diagramma di calibrazione misurato realmente
  su held-out (`lezioni/calibrazione_modulo2.json`); numeri di scala verificati via ricerca
  web (`lezioni/scala_modulo6.json`), timeline storica (`lezioni/timeline_modulo6.json`), dati
  capacità emergenti (`lezioni/capacita_emergenti_modulo6.json`), contenuto base/fine-tuned e
  quantizzazione (`lezioni/base_vs_tuned_modulo6.json`, `lezioni/quantizzazione_modulo6.json`).
  Dettagli completi in decision-log.
- **Modulo 1 completo (2026-07-06)**: `lezioni/lezione_01_testo_come_dato.html` — contenuto
  in prosa e playground del tokenizzatore per tutte e 5 le unità (encoding, tokenizzazione,
  vocabolario/parole inventate, ID, comparazione raster/SVG, diagonale di Cantor). Verificato
  funzionante dall'utente in browser dopo la correzione di un errore di sintassi JS (doppio
  backslash in una label) che bloccava l'intero script. Metodo di verifica aggiornato:
  controllo sintassi JS reale via `osascript -l JavaScript`, non solo controlli HTML.
  Dettagli in decision-log.
- **Modulo 3 e 5 completi (2026-07-06)**: `lezioni/lezione_03_embedding.html` e
  `lezioni/lezione_05_transformer.html` — contenuto in prosa e widget per tutte le unità
  (mappa embedding riusata in 3 modalità: esplorazione, aritmetica con selezione libera
  A/B/C, polisemia con centroidi dal vivo; frase cliccabile con pesi di attention riusata
  in 4 usi: frase principale 5.2/5.3, "calcio" in due contesti con mini-mappa animata in
  5.4, multi-head in 5.5, codifica di posizione in 5.5). Primo uso reale di Claude Fable 5
  nel progetto (delega della costruzione da specifica confermata in conversazione), esito
  positivo — dettagli e valutazione completa in decision-log. Nuovo dato di supporto:
  `lezioni/attention_dati_modulo5.json` (pesi di attention illustrativi, dichiarati come
  tali). Verificato meccanicamente con lo stesso rigore di M1 (sintassi JS reale,
  corrispondenza dati byte-per-byte, id/classi coerenti). Verifica visiva in browser
  lasciata all'utente (file copiati su Desktop). Nessun commit ancora eseguito.
- **Modulo 2 completo (2026-07-06)**: `lezioni/lezione_02_probabilita.html` — contenuto in
  prosa e predittore n-grammi (componente centrale, cresciuto progressivamente 2.1→2.4:
  finestra fissa in 2.1, confronto unigramma/bigramma in 2.2, slider completo 1-3 con
  preimpostazioni in 2.3, riuso con esempio di sparsità in 2.4) per tutte e 4 le unità, più
  il diagramma di calibrazione (2.2, reliability diagram SVG con punti cliccabili) e il
  diagramma statico delle dipendenze lontane (2.4, nessun dataset). Il conteggio n-grammi
  gira dal vivo in JS sul corpus di 46 frasi — il JSON contiene solo il corpus grezzo e tre
  esempi di riferimento, non una tabella precotta per prefissi arbitrari. Verificato con un
  motore JS reale che la funzione di conteggio riproduce esattamente tutti i valori di
  riferimento (9 casi) e che i bucket di calibrazione ricalcolati dalle 65 predizioni
  grezze coincidono con quelli già misurati. Unità 2.1 verificata dall'utente prima di
  procedere con 2.2-2.4, stesso schema di conferma già usato per M1. Verifica visiva del
  file completo lasciata all'utente (file copiato su Desktop). Dettagli in decision-log.
- **Modulo 4 completo (2026-07-06/07)**: `lezioni/lezione_04_reti_neurali.html` — contenuto
  in prosa e tre widget per le 5 unità: neurone singolo a slider (4.1, variante continua del
  calcolatore booleano di `lezione_00a`), XOR con heatmap continua (4.2 tentativo di retta
  fallito, 4.3 confine curvo reale della rete addestrata, 4/4 corretto), superficie di
  perdita resa con **shader GLSL/SDF via WebGL** (4.4/4.5, prima eccezione al vanilla JS del
  sito) — implementata con successo, **nessun fallback necessario**. Contenuti solo-testuali
  integrati: Varela/autopoiesi (4.1), pleroma/creatura di Bateson (4.3), schismogenesi/
  memristor/neuromorphic computing (4.5), domanda di chiusura del modulo su ragionamento/
  metacognizione e discesa del gradiente (lasciata aperta). Verificato sia meccanicamente
  (sintassi JS reale, HTML ben formato, id/classi coerenti, dati byte-per-byte) sia
  **visivamente e interattivamente in browser reale** — grazie a un workaround trovato in
  questa sessione per il limite noto del server di anteprima integrato (vedi decision-log),
  che ha permesso di trovare e correggere un bug reale nello shader (argomenti di
  `smoothstep` invertiti). File copiato su Desktop per la verifica complessiva dell'utente.
  Dettagli completi in decision-log.
- **Modulo 6 completo (2026-07-07)**: `lezioni/lezione_06_large.html` — contenuto in prosa
  e cinque widget per le 6 unità: slider log-scala (6.1, con i 4 punti di ancoraggio reali
  di `scala_modulo6.json`), grafico SVG statico delle capacità emergenti (6.2,
  deliberatamente poco interattivo, nessun controllo che alteri la curva), timeline (6.3,
  classi CSS `.timeline`/`.tl-*` riusate verbatim da `lezione_00_blocco_a.html`, nessun
  nodo `tl-break` per correttezza semantica), toggle prima/dopo condiviso tra 6.4 e 6.5
  (stessa funzione di rendering, due istanze indipendenti nel DOM), barra che si spacca in
  blocchi discreti per la quantizzazione (6.6). Unità 6.1 verificata dall'utente prima di
  procedere con 6.2-6.6, stesso schema di conferma già usato per gli altri moduli.
  Verificato meccanicamente con lo stesso rigore degli altri moduli (sintassi JS reale via
  `osascript -l JavaScript`, HTML ben formato, 46 id univoci coerenti con `UNITS`, nessuna
  classe CSS orfana, tutti e cinque i dati incorporati confrontati byte-per-byte con i JSON
  sorgente) più verifiche numeriche specifiche del modulo (inversione esatta
  slider↔valore-log su tutto il range; tutti gli 8 punti del grafico 6.2 dentro il viewBox
  e banda soglia esattamente tra il salto reale nei dati; segmenti della barra 6.6 monotoni
  non-crescenti tra i livelli quantizzati). File copiato su Desktop per la verifica visiva
  dell'utente (stesso limite noto del server di anteprima, non risolto in questa sessione
  ma con un nuovo script `.claude/serve_lezioni.py` pronto per un tentativo futuro).
  Dettagli completi in decision-log.
- **Con il Modulo 6, l'intero arco tecnico dei Moduli 1-6 del corso "Come funzionano gli
  LLM" è completo** (contenuto + widget per tutti e sei i moduli).
- **Roadmap pianificata (2026-07-07), non ancora eseguita**: revisione di tono su tutto il
  corso (più professionale/accademico, meno pedagogico), compilazione di un file unico
  `output/dal-bit-alle-entita-semantiche_it.html` (indice, introduzione, navigazione a tre livelli,
  tema chiaro/scuro), poi traduzione in EN/FR/DE con ricostruzione di dataset reali nativi
  per ciascuna lingua (non semplice traduzione di stringhe). **8 prompt di sessione già
  scritti e pronti** in `docs/prompt-sessioni-revisione-traduzione-tema.md`, da lanciare in
  sequenza (ogni fase dipende dalla precedente verificata/committata) — non ancora
  lanciati. Dettagli e decisioni chiarite con l'utente in decision-log.

- File markdown di appoggio `blocco_b_contenuti.md`, `blocco_c_contenuti.md` e
  `blocco_d_contenuti.md` in `src/corso-llm/` rimossi a fine sessione (contenuto ormai
  autorevole solo nell'HTML) — stesso trattamento già riservato al file di appoggio del
  Blocco A.
- Schema di lavoro per ogni blocco/modulo: prima il contenuto in markdown (narrativa,
  analogie, domande aperte), conferma dell'utente, poi conversione in HTML seguendo lo
  shell/design system già stabilito in `lezione_00_blocco_a.html`. Trascrizione meccanica
  del markdown in markup delegabile a un subagente (Sonnet); shell, navigazione e scelte di
  design restano nella conversazione principale.

## corso-llm — riferimenti a Blocco/Modulo 00 nel corpo del testo (COMPLETATO 29 agosto 2026)

Indice, numerazione e "corso"→"saggio interattivo" riscritti il 28 agosto (commit
`409cb3d`): tre Parti (Fondamenti, Genealogia, Meccanismo), unità con numerazione
decimale. I ~24 punti nel corpo delle quattro lezioni di Genealogia dove "Blocco A/B/C/D"
o "Modulo 00/0 tecnico" era nominato dentro frasi vere e proprie sono stati riscritti a
mano il 29 agosto (Strato 2), uno per uno, verificando il contenuto reale di ogni rimando
prima di scegliere la formula sostitutiva (non una corrispondenza meccanica lettera→numero
— dettagli e le due correzioni di rotta emerse in corso d'opera in decision-log). Rebuild e
verifica completi (JS reale, HTML bilanciato, `innerText` di tutti e 4 i capitoli nel file
compilato). Non ancora committato.

**Aperto, non catalogato prima d'ora**: molte altre occorrenze di "corso" (minuscolo, non
"saggio interattivo") restano nel corpo di queste quattro lezioni — almeno 19 solo in
`lezione_00_blocco_a.html` — mai toccate dal passaggio "corso"→"saggio interattivo" del 28
agosto, che aveva coperto solo le etichette strutturali. Corrette solo le occorrenze
adiacenti alle frasi appena riscritte per Blocco/Modulo, per non lasciare incoerenza fianco
a fianco. Il resto è una sessione a sé, non ancora quantificata per b/c/d.
