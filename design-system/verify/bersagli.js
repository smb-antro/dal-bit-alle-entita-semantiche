// bersagli.js — elenco di cosa cattura l'harness di regressione visiva.
//
// Ogni voce e' un "bersaglio": una pagina (o una pagina + un'interazione) da
// fotografare. `cattura.js` legge questo file e per ciascun bersaglio scatta
// uno screenshot per ogni viewport elencato in `viewports` (di default
// entrambi: 'desktop' e 'mobile', vedi VIEWPORTS sotto), piu' una variante
// `prefers-reduced-motion: reduce` quando `reducedMotion: true`.
//
// Per aggiungere un bersaglio: aggiungi un oggetto a `bersagli`. Campi:
//   id            stringa univoca, usata nei nomi dei file — niente spazi.
//   url           percorso assoluto dalla radice del repository (il server
//                 statico di cattura.js serve l'intero repo), puo' includere
//                 un fragment (#...) per bersagli con stato via hash-routing.
//   gruppo        etichetta libera per organizzare il rapporto di confronto.
//   viewports     opzionale, default ['desktop','mobile'].
//   reducedMotion opzionale, default false: cattura anche una variante con
//                 prefers-reduced-motion: reduce, SENZA il CSS di
//                 congelamento (vedi README, sezione "Determinismo") — serve
//                 a verificare il comportamento reale sotto quella media
//                 query, non lo stato forzatamente fermo.
//   interazione   opzionale, chiave in INTERAZIONI (cattura.js) da eseguire
//                 dopo il caricamento e prima dello screenshot.
//   assestamento  opzionale, selettore CSS il cui textContent deve
//                 stabilizzarsi (nessun cambiamento per 400ms) prima dello
//                 screenshot — usato per i widget animati via JS che le
//                 regole CSS di congelamento non toccano (vedi loss-canvas).
//   canvas        opzionale { selettore } — dopo lo screenshot, chiama
//                 .toDataURL('image/png') su quell'elemento canvas e salva
//                 il risultato come PNG a se': <id>.png.
//   canvasAttr    opzionale { selettore, attributo } — come sopra ma legge
//                 un data: URL gia' presente in un attributo (per i canvas
//                 offscreen il cui risultato e' incorporato nel DOM, es.
//                 l'heatmap XOR incorporata come href di un <image> SVG).
//   soloCanvas    opzionale, default false — se true non scatta lo
//                 screenshot a pagina intera (perche' gia' coperto da un
//                 altro bersaglio sulla stessa pagina), solo l'estrazione
//                 canvas/canvasAttr.

export const VIEWPORTS = {
  desktop: { width: 1280, height: 900 },
  mobile: { width: 390, height: 844 },
};

// meccanismo-4-reti-neurali.html contiene il widget "paesaggio di perdita":
// un canvas WebGL animato via requestAnimationFrame (discesa del gradiente
// verso un minimo) piu' una minimappa 2D che gli sta accanto. Il loop non e'
// un'animazione CSS (il congelamento via !important non lo tocca) e non si
// ferma da solo finche' la pallina non converge (vedi cattura.js). Ogni
// bersaglio che carica questa pagina deve aspettare quella convergenza,
// altrimenti lo screenshot cattura la pallina a meta' corsa in un punto che
// dipende dal timing reale — il primo modo in cui l'harness diventava non
// deterministico durante lo sviluppo (vedi README).
const ASSESTAMENTO_LOSS = '#loss-readout';

export const bersagli = [
  // ================= Saggio: le 14 pagine, stato a riposo =================
  { id: 'saggio-dietro-i-widget', url: '/dominio/src/saggio/dietro-i-widget.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-fondamenti-1-funzioni-booleane', url: '/dominio/src/saggio/fondamenti-1-funzioni-booleane.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-fondamenti-2-hardware-software', url: '/dominio/src/saggio/fondamenti-2-hardware-software.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-genealogia-1-disputa', url: '/dominio/src/saggio/genealogia-1-disputa.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-genealogia-2-limiti', url: '/dominio/src/saggio/genealogia-2-limiti.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-genealogia-3-villaggio', url: '/dominio/src/saggio/genealogia-3-villaggio.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-genealogia-4-corpo', url: '/dominio/src/saggio/genealogia-4-corpo.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-meccanismo-1-testo-come-dato', url: '/dominio/src/saggio/meccanismo-1-testo-come-dato.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-meccanismo-2-probabilita', url: '/dominio/src/saggio/meccanismo-2-probabilita.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-meccanismo-3-embedding', url: '/dominio/src/saggio/meccanismo-3-embedding.html', gruppo: 'saggio', reducedMotion: true },
  {
    id: 'saggio-meccanismo-4-reti-neurali', url: '/dominio/src/saggio/meccanismo-4-reti-neurali.html', gruppo: 'saggio',
    reducedMotion: true, assestamento: ASSESTAMENTO_LOSS,
  },
  { id: 'saggio-meccanismo-5-transformer', url: '/dominio/src/saggio/meccanismo-5-transformer.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-meccanismo-6-large', url: '/dominio/src/saggio/meccanismo-6-large.html', gruppo: 'saggio', reducedMotion: true },
  { id: 'saggio-presentazione', url: '/dominio/src/saggio/presentazione.html', gruppo: 'saggio', reducedMotion: true },

  // ================= Ontologia: campione =================
  // Scelti per coprire i 4 modi di consultazione dichiarati in
  // ontologia/output/index.html (Glossario, Moduli, Fili, Teorici) piu' le
  // due pagine di dettaglio piu' intrecciate con la Lente semantica e col
  // saggio: "Attention" e' il concetto scelto anche per il bersaglio Lente
  // sotto, "Bahdanau" e' il suo teorico, "Meccanismo5" e' il capitolo (della
  // struttura ontologia/output/moduli/) in cui "Attention" e' discussa.
  { id: 'ontologia-index', url: '/ontologia/output/index.html', gruppo: 'ontologia' },
  { id: 'ontologia-concetti-index', url: '/ontologia/output/concetti/index.html', gruppo: 'ontologia' },
  { id: 'ontologia-teorici-index', url: '/ontologia/output/teorici/index.html', gruppo: 'ontologia' },
  { id: 'ontologia-moduli-index', url: '/ontologia/output/moduli/index.html', gruppo: 'ontologia' },
  { id: 'ontologia-fili-index', url: '/ontologia/output/fili/index.html', gruppo: 'ontologia' },
  { id: 'ontologia-concetto-attention', url: '/ontologia/output/concetti/Attention.html', gruppo: 'ontologia' },
  { id: 'ontologia-teorico-bahdanau', url: '/ontologia/output/teorici/Bahdanau.html', gruppo: 'ontologia' },
  { id: 'ontologia-modulo-meccanismo5', url: '/ontologia/output/moduli/Meccanismo5.html', gruppo: 'ontologia' },

  // ================= Lente semantica =================
  // La selezione e' hash-routing (vedi lente.js: `location.hash = id`,
  // letto all'avvio da `location.hash.slice(1)`); "Attention" e' un id di
  // nodo valido (src/grafo.js). Il 2° grado si attiva cliccando
  // #btn-grado-2 (vedi INTERAZIONI.lente-grado2 in cattura.js).
  {
    id: 'lente-attention-grado2', url: '/ontologia/lente-semantica/output/index.html#Attention', gruppo: 'lente',
    interazione: 'lente-grado2',
  },

  // ================= Stati interattivi =================
  // Solo viewport desktop: la miscela viewport × stato-interattivo cresce
  // in fretta; qui contano gli stati in se', non il loro responsive (gia'
  // verificato dai bersagli "a riposo" sopra, entrambi a 1280 e 390).
  {
    id: 'saggio-meccanismo-4-tenda-aperta', url: '/dominio/src/saggio/meccanismo-4-reti-neurali.html', gruppo: 'stato',
    viewports: ['desktop'], interazione: 'apri-tenda', assestamento: ASSESTAMENTO_LOSS,
  },
  {
    id: 'saggio-fondamenti-1-focus-visible', url: '/dominio/src/saggio/fondamenti-1-funzioni-booleane.html', gruppo: 'stato',
    viewports: ['desktop'], interazione: 'focus-visible',
  },
  {
    id: 'saggio-genealogia-1-details-aperti', url: '/dominio/src/saggio/genealogia-1-disputa.html', gruppo: 'stato',
    viewports: ['desktop'], interazione: 'apri-details',
  },

  // ================= Canvas: bersaglio piu' fragile =================
  // meccanismo-4-reti-neurali.html ha DUE canvas che leggono i colori da
  // getComputedStyle(...).getPropertyValue(nome) invece che da valori fissi
  // (funzione themeVarHex, righe ~1089 del file sorgente) — esattamente il
  // punto che una migrazione del CSS puo' rompere in silenzio: rinominare
  // una custom property senza aggiornare questo JS produce un canvas
  // sbagliato che un diff testuale del CSS non intercetta, ma un confronto
  // a pixel si'. Catturiamo entrambi:
  //  - #loss-minimap: canvas 2D reale nel DOM (sfondo statico da
  //    themeVarHex + pallina dinamica) — toDataURL diretto, affidabile.
  //  - #xor-heatmap-img: il risultato di un canvas 2D offscreen, mai
  //    inserito nel DOM, il cui .toDataURL() e' gia' incorporato dal codice
  //    stesso come href di un <image> SVG (renderXorHeatmap, riga ~1114) —
  //    lo leggiamo da li' invece di ricrearlo.
  // Il grande canvas WebGL (#loss-canvas, il "paesaggio 3D") NON e' fra
  // questi: legge una palette JS fissa per tema (LOSS_SHADER_PALETTE), non
  // custom property CSS per nome, quindi non e' il bersaglio descritto — e
  // toDataURL() su un canvas WebGL senza preserveDrawingBuffer e' comunque
  // inaffidabile (vedi README, sezione "Cosa NON copre"). E' comunque
  // presente nello screenshot a pagina intera di meccanismo-4.
  {
    id: 'saggio-meccanismo-4-canvas-loss-minimap', url: '/dominio/src/saggio/meccanismo-4-reti-neurali.html', gruppo: 'canvas',
    viewports: ['desktop'], assestamento: ASSESTAMENTO_LOSS, soloCanvas: true,
    canvas: { selettore: '#loss-minimap' },
  },
  {
    id: 'saggio-meccanismo-4-canvas-xor-heatmap', url: '/dominio/src/saggio/meccanismo-4-reti-neurali.html', gruppo: 'canvas',
    viewports: ['desktop'], soloCanvas: true,
    canvasAttr: { selettore: '#xor-heatmap-img', attributo: 'href' },
  },
];
