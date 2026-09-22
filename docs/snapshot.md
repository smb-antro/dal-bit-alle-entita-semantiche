# Snapshot — cs-1-cartografia-semantica

**9 settembre 2026** — saggio e Lente semantica interamente integrati e rifiniti:
design chiaro uniforme, tenda dei concetti su tutto il saggio, poster del grafo,
indice della presentazione riorganizzato in 4 parti, secondo grado della Lente
reso leggibile. Nessun commit pubblicato su GitHub.

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
- `LICENSE` definita il 19 settembre 2026: codice MIT, ontologia CC BY 4.0 (anche
  dentro i dati, con `owl:versionInfo "1.0"`), prosa e documentazione riservate.
- ✅ **Font self-hosted in una copia sola** (22 settembre 2026): `design-system/fonts/`
  con EB Garamond e IBM Plex Mono, nessuna richiesta a Google da nessuna pagina del
  saggio. Ha riparato un difetto reale: tre dei quattro simboli logici di Fondamenti · 1
  non erano coperti dai subset serviti e ripiegavano sul monospaziato di sistema. Primo
  passo della trasformazione del design system da prosa a sistema funzionante.
- ✅ **Harness di regressione visiva** (22 settembre 2026): `design-system/verify/`,
  28 bersagli e 65 immagini per giro, deterministico — verificato con 4 catture
  indipendenti e 6 confronti a coppie a zero fallimenti. Tolleranza basata
  sull'entità della differenza (delta per canale), non sulla percentuale di pixel.
  Ha fatto emergere una lacuna di accessibilità: animazioni infinite che non si
  fermano sotto `prefers-reduced-motion`.
- ✅ **Riconciliazione tipografica** (22 settembre 2026): i tre lignaggi di
  conversione avevano lasciato tre scale diverse nello stesso saggio — la sidebar,
  identica in ogni pagina, era resa a 17,3 / 15,7 / 13,1px a seconda del capitolo.
  121 sostituzioni verificate a una a una: ora radice, voce, intestazione di parte
  e interlinea sono identiche su tutte e 14 le pagine. Ontologia, Lente e i canvas
  di `meccanismo-4` a zero differenze. Baseline rifatta su questo stato.
- Storia di commit solo locale (`feat(init)`, `feat(design-system)`, i due
  `feat(saggio)`, `feat(lente)`, più la passata di pulizia pre-pubblicazione).
  Non pubblicato su GitHub. Card del portfolio riservata in
  `portfolio/site/lab.html` ma non collegata.

Prossimo passo reale: nessun lavoro di contenuto resta aperto né sul saggio né sulla
Lente. È in corso la trasformazione del design system da prosa e prototipi sparsi a
sistema funzionante e autonomo — token, CSS condiviso, componenti, esportabile su
Claude Design — con una rete di sicurezza di regressione visiva costruita prima di
toccare le pagine. Solo dopo vengono l'aggiornamento di `build_output.py` e la
rigenerazione del bundle statico (che serve anche come verifica), poi le decisioni
aperte in `next-steps.md` e il push.
