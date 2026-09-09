# Snapshot — cs-1-cartografia-semantica

**9 settembre 2026** — saggio e Lente semantica interamente integrati e rifiniti:
design chiaro uniforme, tenda dei concetti su tutto il saggio, poster del grafo,
indice della presentazione riorganizzato in 4 parti, secondo grado della Lente
reso leggibile. 5 commit, nessuno pubblicato su GitHub.

- `dominio/` e `ontologia/` copiati integralmente (`git archive`) dai rispettivi
  repository sorgente, al loro stato del 4 settembre 2026 (HEAD `bea0aaa` e `1765f29`
  rispettivamente).
- ✅ **Design system chiaro su tutte le pagine navigabili**: i 12 capitoli,
  `presentazione.html`, l'appendice `dietro-i-widget.html`, la Lente semantica e
  tutto `ontologia/output/` (194 pagine, un solo `style.css` condiviso). Dimensione
  dei caratteri +20% e verde dei rimandi schiarito da `--verde-scuro` a `--verde`
  su 13 dei 14 file (tutti tranne l'appendice per il font-size), dopo un test di
  grafica su un prototipo di portfolio — contrasto ricalcolato prima di
  generalizzare. Vedi `decision-log.md`.
- **`indice.html`** rimosso il 9 settembre 2026: ridondante con la sidebar già
  presente in ogni pagina, era orfano e nel vecchio tema scuro dal 4 settembre.
  Recuperabile dallo storico git se mai servisse.
- ✅ **Tenda dei concetti su tutto il saggio**: 110 concetti unici cliccabili sui 12
  capitoli (da 4 in Fondamenti · 1 a 18 in Meccanismo · 4, il capitolo più grande)
  più `presentazione.html` (`Embedding`, come esempio dal vivo) — dati letti da
  `ontologia/output/concetti/`, link alla Lente reale, verificato end-to-end su ogni
  bottone con click reale, non a lettura di codice. Sempre scelti da
  `:discussoInUnita` nell'ontologia, mai a occhio.
- ✅ **Poster del grafo completo con lightbox**, in fondo a `presentazione.html`:
  layout calcolato con una simulazione a forze D3 sugli stessi dati della Lente
  semantica (258 nodi, 537 relazioni) — non disegnato a mano — salvato come SVG
  statico in `dominio/src/saggio/immagini_presentazione/`. Click per ingrandire
  senza perdita di qualità.
- ✅ **Presentazione riorganizzata**: sidebar con titolo in maiuscoletto/blu
  (link diretto ad apertura+abstract), indice a 4 parti ("Da «re» a «regina»",
  "I limiti che condividiamo", "Struttura, composizione e stack del saggio
  interattivo", "Il grafo e la lente semantica"), abstract editoriale distinto
  dal resto del testo. Corretto anche un bug reale nello scrollspy della sidebar
  (soglia dell'`IntersectionObserver` mai raggiungibile per sezioni più alte del
  viewport).
- ✅ **Secondo grado della Lente semantica reso leggibile**: prima erano punti
  muti senza etichetta, collegati da una linea dritta quasi invisibile — ora rami
  visibili (curva su misura, non un dendrogramma standard, che diverge subito
  dall'angolo del nodo padre) con etichetta sempre leggibile. Messo a punto e
  verificato — non solo a occhio, con un controllo geometrico automatico — su
  due prototipi isolati in `ontologia/lente-semantica/lab/` prima di portare la
  correzione in `output/`. Corretto anche un bug indipendente: il filtro della
  legenda non toccava affatto il secondo grado (mancava `data-cat`).
- `dominio/output/dal-bit-alle-entita-semantiche_it.html` (bundle generato da
  `build_output.py`) ancora **non rigenerato**: lo script si è rivelato in parte
  disallineato (contiene testo e font vecchi hardcoded) — non un semplice
  ri-lancio, va prima aggiornato. Deliberatamente rimandato.
- `docs/` (questo file, decision-log, next-steps) sincronizzati il 9 settembre
  2026 dopo essere rimasti indietro rispetto al lavoro di giornata.
- `LICENSE` placeholder con quattro alternative, nessuna scelta ancora fatta.
- **5 commit** (`feat(init)`, `feat(design-system)`, `feat(saggio)` tema chiaro
  completo, `feat(saggio)` sidebar/presentazione riorganizzata, `feat(lente)`
  secondo grado). Non pubblicato su GitHub. Card del portfolio riservata in
  `portfolio/site/lab.html` ma non collegata.

Prossimo passo reale: nessun lavoro di contenuto bloccante resta aperto né sul
saggio né sulla Lente. Quello che resta è amministrativo — aggiornare
`build_output.py` e rigenerare il bundle statico, poi licenza/push, in
quest'ordine o nell'ordine che l'utente preferisce (vedi `next-steps.md`,
sezione "Debito rimasto").
