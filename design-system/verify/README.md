# Harness di regressione visiva

Rete di sicurezza per la migrazione al design system: dimostra, a pixel, che
estrarre il CSS condiviso non cambia l'aspetto delle pagine.

Serve a rispondere a una domanda sola, e a risponderla con un numero invece che
a occhio: *questa modifica ha cambiato qualcosa che si vede?*

## Uso

```bash
cd design-system/verify
npm install                  # una volta: scarica playwright-core, nessun binario di browser
node cattura.js --baseline   # registra lo stato attuale in baseline/
# … si modifica il CSS …
node cattura.js              # registra il nuovo stato in attuale/
python3 confronta.py         # confronta e stampa il rapporto
```

`confronta.py` esce con codice 1 se qualcosa è cambiato in modo percettibile, e
scrive in `differenze/` un'immagine amplificata per ogni bersaglio fallito.

Nessuna delle tre cartelle di immagini è versionata: si rigenerano. Gli script sì.

## Cosa serve

- **Node** e **Chrome** già installati. `playwright-core` pilota il Chrome di
  sistema (`channel: 'chrome'`): non scarica binari di browser, a differenza del
  pacchetto `playwright` completo che ne scaricherebbe ~150 MB.
- **Python 3 con Pillow** per il confronto.
- Nessun server da avviare a mano: `cattura.js` ne accende uno suo, interno, su
  una porta scelta dal sistema, con radice il repository, e lo spegne alla fine.

## Cosa copre

28 bersagli, 65 immagini per giro, circa 90 secondi.

- **Saggio** — tutte e 14 le pagine, a 1280×900 e 390×844. Il viewport stretto
  non è decorativo: il layout cambia davvero a 900px.
- **Ontologia** — 8 pagine campione: la home, un concetto, un teorico, un modulo
  e i quattro indici. Rappresentano i modelli di pagina da cui `genera_html.py`
  produce le ~194 pagine: se un modello regredisce si vede qui.
- **Lente semantica** — il grafo radiale con "Attention" selezionato e il secondo
  grado attivato per interazione reale sul bottone, non simulato.
- **Stati interattivi**, perché una pagina a riposo non è tutta la pagina: la
  tenda dei concetti aperta, un `<details>` aperto con un click vero,
  `:focus-visible` raggiunto tabulando (non con `.focus()` programmatico, che in
  Chromium non fa sempre scattare lo stesso stato).
- **`prefers-reduced-motion: reduce`** su 14 bersagli.
- **I due canvas di `meccanismo-4`**, salvati anche via `toDataURL` come immagini
  a sé: è il widget più fragile della migrazione, perché il suo JavaScript legge
  le custom property CSS *per nome* — un nome che sparisce non dà errore, dà un
  canvas nero.

## Cosa NON copre, dichiarato

- **Le ~186 pagine dell'ontologia non campionate.** Sono generate dagli stessi
  modelli; un errore che tocchi solo una pagina specifica non verrebbe visto.
- **I widget che richiedono un'interazione per disegnare** (un click, un
  trascinamento). Lo scorrimento fa partire quelli agganciati all'intersezione,
  non gli altri.
- **Che le animazioni si fermino davvero sotto reduced-motion.** L'harness
  congela le animazioni in entrambe le varianti per poter essere deterministico,
  quindi non può verificarlo per immagine. Lo verifica invece un censimento
  esplicito, vedi sotto.
- **Il comportamento su browser diversi da Chrome.** Un solo motore.
- **`file://`.** Le pagine si servono via HTTP, come in sviluppo.
- **Stampa.** Nel repository non esiste alcun `@media print`, quindi non c'è
  nulla da regredire.

## Determinismo: come ci si è arrivati

Un harness che dà falsi positivi è peggio che non averlo, perché insegna a
ignorarlo. Il requisito posto era: due catture consecutive dello stesso codice
immutato devono dare zero differenze. Arrivarci ha richiesto di trovare quattro
cause distinte, tutte emerse solo dal doppio giro e mai da una cattura singola.

1. **Il tempo di rasterizzazione dei font.** Anche dopo che
   `document.fonts.ready` si risolve, il compositor di Chrome impiega ancora
   ~100-200 ms per finire di rasterizzare il testo appena passato al font
   definitivo. Sotto i 200 ms, le pagine con titoli grandi mostravano differenze
   reali fra due catture identiche, sempre nella stessa fascia verticale. La
   pausa è fissata a 300 ms: margine deliberato sopra la soglia misurata.

2. **Animazioni a tempo.** `animation-duration: 0s` e `transition-duration: 0s`
   iniettati prima dello scatto — non `animation: none`, che farebbe ricadere
   l'elemento sullo stile non animato e lascerebbe invisibile ciò che parte da
   `opacity: 0` con `fill-mode: forwards`. Con durata zero il motore gira
   comunque e rispetta il `fill-mode`: l'aspetto finale è autentico, solo
   istantaneo. Stubbato anche `window.setInterval`, per un orologio testuale in
   `fondamenti-2` che non converge mai da solo.

3. **Un loop `requestAnimationFrame`** nel widget "paesaggio di perdita" di
   `meccanismo-4`, che il congelamento CSS non ferma. La sua fisica è
   deterministica (stessa posizione iniziale, stesso learning rate, soglia di
   arresto fissa), quindi il punto di arrivo è sempre lo stesso: l'harness
   aspetta che il testo smetta di cambiare, invece di indovinare un numero di
   millisecondi.

4. **Il dithering delle sfumature**, che ha richiesto di ripensare la tolleranza
   — vedi la sezione seguente.

5. **I blocchi `.reveal`, che non si rivelavano affatto** — la scoperta più grave,
   e arrivata tardi: vedi la sezione seguente.

Una pista esplorata e **scartata**: il limite di 16384px (2¹⁴) alla dimensione
delle texture di Chrome. 25 bersagli su 65 superano quell'altezza, fino a
54.900px, e una differenza intermittente cadeva in un riquadro che finiva esatto
a y=16384 — indizio convincente. Si è provato a catturare a fasce da 8000px. Ma
misurando l'*entità* di quelle differenze si è visto che erano tutte di 1 livello
su 255: Playwright cuce bene, il limite non corrompe nulla. Le fasce sono state
rimosse, perché introducevano più rumore di quanto ne togliessero.

## I `.reveal`: il 64% che non veniva fotografato

Trovato il **23 settembre 2026**, cambiando il carattere monospaziato. I quattro
simboli logici di Fondamenti · 1, alti 40px, non comparivano in *nessuno* dei due
screenshot — né prima né dopo il cambio. Cercandoli per colore nell'immagine
intera: una sola banda arancione in tutta la pagina.

La causa: il saggio avvolge quasi tutto il proprio contenuto in blocchi `.reveal`,
che partono a `opacity: 0` e diventano visibili quando un `IntersectionObserver`
li incontra. `cattura.js` non scorreva la pagina, quindi l'osservatore non
scattava mai. Misurato sulle 14 pagine: **il 64% dell'altezza complessiva stava
dentro `.reveal` mai resi visibili.** Il confronto a pixel vedeva circa un terzo
del contenuto e dichiarava «zero differenze» su pagine in gran parte vuote.

Cosa **non** era compromesso, e vale la pena dirlo: i confronti di stile calcolato
leggono i valori a prescindere dall'opacità; i confronti di altezza sono validi
perché un elemento a opacità zero occupa comunque il suo spazio; i controlli su
link, rete e token non c'entrano. Era cieco il solo confronto a pixel.

La correzione fa due cose: **scorre** l'intera pagina e torna in cima, così gli
osservatori scattano e i widget agganciati all'intersezione disegnano davvero; e
porta i `.reveal` allo stato finale **per dichiarazione** (`opacity: 1;
transform: none`), perché un `translateY` residuo promuove l'elemento a livello
compositato e ne cambia la rasterizzazione. La cattura passa da ~88 a ~186
secondi: è il prezzo di guardare tutta la pagina invece di un terzo.

**Verificato dopo la correzione**: estratti dalla storia lo stato prima
(`c8db785`) e dopo (`1791eda`) la migrazione al design system, resi entrambi con
la cattura corretta e confrontati. **26 confronti su 28 identici**; i due con
differenze mostrano esattamente i valori bistabili già catalogati sotto. La
migrazione regge anche su ciò che l'harness non aveva mai guardato.

## Tolleranza: l'entità, non il numero

La tolleranza non è una percentuale di pixel diversi. Due catture dello stesso
codice possono differire su **centinaia di migliaia** di pixel restando identiche
all'occhio, perché il dithering delle sfumature non è riproducibile al bit. Una
tolleranza percentuale avrebbe dovuto salire fino al 4% per assorbirlo, e a quel
punto avrebbe lasciato passare cambiamenti veri.

Misurando invece il delta massimo per canale, le due popolazioni si separano:

| delta per canale | natura | quantità osservata |
|---|---|---|
| 1–2 | rumore di rasterizzazione | ~18.000 pixel per giro su ~900 milioni |
| ≥ 3 | differenza reale | il cursore lampeggiante: 96 px con delta fino a 10 |

Quindi: **si fallisce su qualunque pixel con delta > 2**, e i pixel a delta ≤ 2
si contano e si riportano senza far fallire. Il valore 2 non è scelto a occhio:
su tre catture consecutive un bersaglio ha mostrato 16 pixel a delta 2 in un
confronto e zero nel successivo, quindi anche 2 è rumore casuale. Da 3 in su non
si è mai osservato rumore.

Un'unica eccezione per bersaglio, in `SOGLIE_PER_BERSAGLIO`: il grafo della Lente
ha due pixel bistabili sull'antialiasing dei bordi, a (817,524) e (891,888). Su
tre catture, la prima e la terza sono identiche e la seconda differisce in quei
due soli pixel, sempre con gli stessi due valori alternativi. È una coordinata
che cade su un mezzo pixel esatto e arrotonda in un verso o nell'altro. Margine
concesso: 4 pixel, il doppio del misurato.

Dal 23 settembre, con i `.reveal` finalmente visibili, tre pagine molto dense di
widget — Meccanismo · 1, 2 e 6 — mostrano una instabilità di rasterizzazione su
bordi e maiuscoletto. Non è deriva ma **bistabilità**: su tre catture consecutive
dello stesso codice ricorrono sempre gli stessi valori esatti (240, 183, 133, 73),
cioè la pagina rende in una di due varianti, indistinguibili guardandole da
vicino. L'impronta del disegno (canvas, SVG, testo) è identica: cambia solo come
viene rasterizzato. Margine concesso: 300 pixel, sopra il massimo misurato di 240.
Non nasconde una regressione vera — un cambio di colore, misura o spaziatura
produce migliaia o milioni di pixel percettibili su pagine da ~20 milioni, non
centinaia sparse sui bordi.

**Validazione**: 4 catture indipendenti e 6 confronti a coppie prima della
correzione dei `.reveal`; 3 catture e 3 confronti dopo, più il confronto
prima/dopo migrazione descritto sopra.

## Animazioni infinite sotto reduced-motion

Quando cattura la variante `prefers-reduced-motion: reduce`, e **prima** di
congelare alcunché, `cattura.js` censisce le animazioni infinite ancora in corso
e scrive l'elenco in `animazioni-infinite.json`.

Non è un controllo di regressione, è un controllo di accessibilità, ed è nato da
una scoperta del cancello di qualità: `fondamenti-2-hardware-software.html` ha
tre cursori con `animation: 1.2s infinite blink` che continuano a lampeggiare
anche per chi ha chiesto meno animazioni, perché il blocco
`@media (prefers-reduced-motion: reduce)` delle pagine contiene soltanto
`scroll-behavior: auto`. Il posto giusto dove chiudere questa lacuna è il layer
`reset` del design system, con un reset che fermi davvero animazioni e
transizioni sotto quella media query.

Finché l'elenco non è vuoto, c'è lavoro da fare.
