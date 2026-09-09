# Snapshot — cs-1-cartografia-semantica

**9 settembre 2026** — design system e tenda dei concetti applicati all'intero
saggio; poster del grafo aggiunto in chiusura della presentazione; verde dei rimandi
schiarito ovunque; `indice.html` rimosso. Ancora 2 commit — tutto il lavoro sotto, di
questa e della sessione precedente, non è stato committato.

- `dominio/` e `ontologia/` copiati integralmente (`git archive`) dai rispettivi
  repository sorgente, al loro stato del 4 settembre 2026 (HEAD `bea0aaa` e `1765f29`
  rispettivamente).
- ✅ **Design system chiaro su tutte le pagine navigabili**: i 12 capitoli,
  `presentazione.html`, l'appendice `dietro-i-widget.html`, la Lente semantica e
  tutto `ontologia/output/` (194 pagine, un solo `style.css` condiviso). Un colore
  hex vecchio, sfuggito il 4 settembre perché scritto dentro una stringa SVG
  generata via JS (non CSS) in Meccanismo · 1, trovato e corretto l'8 settembre —
  vedi `decision-log.md`. Verde dei rimandi schiarito da `--verde-scuro` a `--verde`
  ovunque (saggio e Lente semantica) il 9 settembre, dopo un test di grafica su un
  prototipo di portfolio — contrasto ricalcolato prima di generalizzare.
- **`indice.html`** rimosso il 9 settembre 2026: ridondante con la sidebar già
  presente in ogni pagina, era orfano e nel vecchio tema scuro dal 4 settembre.
  Recuperabile dallo storico git se mai servisse — vedi `decision-log.md`.
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
- `dominio/output/dal-bit-alle-entita-semantiche_it.html` (bundle generato da
  `build_output.py`) ancora **non rigenerato** — rimandato dal 4 settembre in
  attesa che il saggio fosse interamente convertito; ora lo è, la rigenerazione
  resta comunque da fare.
- `docs/` con decision-log, next-steps, questo snapshot — aggiornati insieme,
  l'8 settembre 2026, dopo essere rimasti fermi al 4 (debito di sincronizzazione
  segnalato ma non richiuso fino ad ora).
- `LICENSE` placeholder con quattro alternative, nessuna scelta ancora fatta.
- 2 commit (`feat(init)`, `feat(design-system)`). Tutto il lavoro sopra — conversione
  degli ultimi capitoli, tenda dei concetti sull'intero saggio, poster del grafo —
  non è ancora committato. Non pubblicato su GitHub. Card del portfolio riservata in
  `portfolio/site/lab.html` ma non collegata.

Prossimo passo reale: nessun lavoro di contenuto bloccante resta aperto sul saggio
stesso. Quello che resta è amministrativo — rigenerare il bundle statico, poi
commit/licenza/push, in quest'ordine o nell'ordine che l'utente preferisce (vedi
`next-steps.md`, sezione "Debito rimasto").
