# Piano — Appendice sui widget di Meccanismo

Pianificazione di processo, non contenuto pubblicato — stesso trattamento di
`piano_corso_llm.md` e `struttura_moduli_1-6.md`. Copre solo il **punto 1** della
roadmap discussa in chat (5 punti totali): l'appendice che spiega, widget per widget,
perché ogni componente interattivo di Parte III (Meccanismo) è stato costruito così.

**Fuori scope qui, deliberatamente**: non il grafo in sé — le strutture relazionali
che M3 (vicinanza tra embedding) e M5 (pesi di attention come archi tra token) mostrano
*sono* grafi, e descriverle come tali fa parte a pieno titolo del "perché così" di quei
due widget, resta dentro questo piano. Ciò che resta fuori è il passo successivo:
**confrontare quel grafo con un'ontologia formale (OWL/SHACL) e le sue applicazioni
pratiche** — quello è il punto 5, ancora da definire nella forma e nella collocazione,
non è detto finisca in questa stessa appendice. Fuori scope anche l'estensione della
Presentazione con la Lente Semantica (va lì, non qui — vedi decisione in chat:
l'appendice parla solo di lavoro concluso e verificato, la Lente com'è oggi è un
mockup, non un widget).

## Perché questa appendice, in una frase

Il saggio mostra i widget; l'appendice mostra il lavoro dietro — la scelta di design,
lo stack, il dataset reale — con un taglio esplicitamente "dietro le quinte", utile sia
a un lettore tecnico del saggio sia, in prospettiva, come base per la sintesi da
portfolio (da cui il registro professionale, non divulgativo).

## Collocazione e forma (deciso)

- **Un solo file**, `src/saggio/dietro-i-widget.html` — non in una cartella a sé
  (`src/appendice/`, la prima scelta): spostato dentro `saggio/`, sibling di ogni
  altro capitolo, dopo che la cartella separata ha causato un percorso relativo
  sbagliato nel compilato (`../appendice/` risolto da `output/` puntava a un
  percorso inesistente — bug reale, trovato testando il link dal vivo). Da
  `saggio/` i riferimenti sono bare filename come ovunque altro nel sito, niente
  di speciale da calcolare per profondità di cartella. Riusa lo shell/design
  system esistente (sidebar fissa, tema chiaro/scuro).
- Agganciata a `indice.html` con lo stesso pattern già in uso per Genealogia/
  Meccanismo, non con un meccanismo nuovo: un quarto blocco `.parte` **dopo** Parte
  III — Meccanismo (prima del `<footer>`), con un unico `<details class="modulo">`
  ("Appendice — dietro i widget") e una `unita-list` di sei ancore (una per widget,
  M1→M6) dentro l'unico file dell'appendice — stesso rapporto capitolo↔unità già usato
  per ogni modulo tecnico, solo applicato all'appendice invece che a un modulo. Non
  entra nella compilazione di `output/` per ora (fuori scope di questa fase).

## Struttura per ciascuna delle sei sezioni

Schema fisso, ripetuto sei volte (un widget = una sezione):

1. **Cosa fa** — richiamo breve, non ripete il saggio, giusto l'ancora per chi non lo
   ha sotto mano.
2. **Perché così** — la scelta di design reale: perché uno slider e non un valore
   fisso, perché una heatmap continua e non punti discreti, perché quel widget è
   riusato su più unità invece di uno per unità (pattern confermato nel progetto: un
   componente centrale per modulo, non un widget per unità — vedi decision-log
   6 luglio 2026).
3. **Con quali dati** — il dataset reale dietro, come è stato costruito/verificato,
   citando il file `.json` sorgente specifico.

## Contenuto per widget (base fattuale già raccolta da decision-log/next-steps)

- **M1 — Tokenizzatore/BPE** (`meccanismo-1-testo-come-dato.html`): playground unico
  riusato su encoding, tokenizzazione, vocabolario/parole inventate, ID, comparazione
  raster/SVG, diagonale di Cantor. Dati: BPE addestrato realmente sul corpus del saggio
  (`bpe_merges_modulo1.json`, 300 merge, verificato a round-trip zero errori),
  `cantor_diagonale_modulo1.json`, asset raster+SVG in `immagini_modulo1/`.
- **M2 — Predittore n-grammi + calibrazione** (`meccanismo-2-probabilita.html`):
  componente cresciuto progressivamente (finestra fissa → confronto unigramma/
  bigramma → slider 1-3 con preimpostazioni → riuso per la sparsità), più il reliability
  diagram SVG cliccabile. Perché-così degno di nota: il conteggio gira dal vivo in JS
  sul corpus di 46 frasi, non è precotto — scelta verificata contro 9 casi di
  riferimento con un motore JS reale. Dati: `ngram_dati_modulo2.json`,
  `calibrazione_modulo2.json` (reliability diagram misurato su held-out reale, non
  simulato).
- **M3 — Mappa embedding** (`meccanismo-3-embedding.html`): stesso componente in tre
  modalità (esplorazione, aritmetica A/B/C, polisemia con centroidi dal vivo). Perché-
  così: assi costruiti su misura per ciascuna modalità, non PCA generica — la PCA non
  preservava le relazioni volute. Da esplicitare qui (dentro il punto 1, non punto 5):
  la vicinanza fra punti *è* un grafo — ogni coppia di parole vicine è implicitamente
  un arco pesato, anche se il widget lo mostra come distanza spaziale e non come linea.
  Dati: `embedding_dati_moduli_3_5.json`, 23 parole, vettori reali fastText italiano
  (condiviso con M5 — punto di raccordo naturale nella narrazione).
- **M4 — Neurone / XOR / superficie di perdita** (`meccanismo-4-reti-neurali.html`):
  lo snodo dell'intera appendice. Tre widget: neurone a slider (variante continua del
  calcolatore booleano di Genealogia), XOR con heatmap continua (confine curvo di una
  rete realmente addestrata, 4/4 corretto), superficie di perdita **in GLSL/SDF via
  WebGL** — l'unica eccezione al vanilla JS/SVG del resto del sito. Il perché-così qui
  è il cuore narrativo: un campo scalare continuo (la superficie di perdita) non è
  reso bene da SVG/Canvas 2D discreto, da cui il salto di stack. Verificato
  visivamente pixel per pixel, un bug reale trovato e corretto (argomenti di
  `smoothstep` invertiti). Dati: `xor_rete_modulo4.json`, `neurone_esempi_modulo4.json`,
  `paesaggio_perdita_modulo4.json` (superficie specificata e verificata
  numericamente prima di scriverla in shader).
- **M5 — Attention** (`meccanismo-5-transformer.html`): frase cliccabile con pesi di
  attention, riusata in quattro contesti (frase principale, "calcio" in due contesti
  con mini-mappa animata collegata a M3, multi-head, codifica di posizione). Da
  esplicitare qui: i pesi di attention *sono* un grafo esplicito, questa volta con
  archi diretti e pesati mostrati apertamente (linee di spessore variabile fra token) —
  il punto di raccordo più diretto con M3 nella narrazione "perché il grafo conta".
  Dati: `attention_dati_modulo5.json`, dichiarati esplicitamente come illustrativi (non
  pesi reali di un modello addestrato) — punto onesto da riportare nell'appendice, non
  da nascondere.
- **M6 — Scala e capacità** (`meccanismo-6-large.html`): cinque widget minori invece di
  uno centrale (unica eccezione al pattern "un componente per modulo") — slider log-
  scala, grafico statico delle capacità emergenti (deliberatamente poco interattivo,
  per correttezza: non ci sono controlli che alterino una curva empirica), timeline,
  toggle prima/dopo, barra di quantizzazione. Dati: `scala_modulo6.json` (verificato via
  ricerca web), `capacita_emergenti_modulo6.json`, `timeline_modulo6.json`,
  `base_vs_tuned_modulo6.json`, `quantizzazione_modulo6.json`.

## Metodo di lavoro proposto

Stesso schema già rodato nel progetto per contenuto esteso multi-unità: prima il
contenuto in prosa di una sezione (M4, essendo lo snodo, buon candidato per la prima),
conferma dell'utente, poi propagazione alle altre cinque — non scrivere tutte e sei le
sezioni "alla cieca" prima di un primo checkpoint.

## Verifica prevista

- Ogni claim di design/dataset in questo piano e nel testo finale deve restare
  ancorato a quanto realmente verificabile in decision-log o nei file `.json` stessi —
  non descrivere un dataset come "reale" se è dichiarato illustrativo (vedi M5), non
  inventare cifre.
- Sintassi JS reale sul file nuovo (stesso metodo già in uso, `osascript -l
  JavaScript`), HTML ben bilanciato, nessun id orfano rispetto al resto del sito se
  l'appendice finisce per essere linkata da `indice.html`.
- Verifica visiva in browser reale prima di considerare la sezione chiusa (stesso
  standard già applicato a tutti i moduli tecnici).

## Aperto, ancora da decidere

- Se l'appendice va menzionata anche in fondo all'ultimo capitolo di Meccanismo
  (`meccanismo-6-large.html`, unità 6.6) con un link di rimando, oltre alla voce in
  `indice.html` — non necessario per aprire il lavoro, valutare in corso d'opera.
