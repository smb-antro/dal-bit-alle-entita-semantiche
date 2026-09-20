# Decision log — cs-1-cartografia-semantica

## 2026-09-04 — Creazione del repository

Primo caso studio del portfolio, creato come repository indipendente in
`~/projects/cs-1-cartografia-semantica/`. Combina due lavori dichiarati maturi lo
stesso giorno o poco prima:

- `dominio/` — copiato da `~/projects/cartografia-semantica/` (HEAD `bea0aaa`) via
  `git archive`, non `cp`/clone: solo i file tracciati, nessuna storia git preservata,
  nessun file `.git/`. Rimosso manualmente `.claude/worktrees/.gitkeep` dalla copia —
  era tracciato nel sorgente come scaffold per la propria convenzione worktree, ma non
  ha senso qui: `dominio/` non è un repository a sé in questo contesto.
- `ontologia/` — copiato da `~/projects/vocabolario-ontologia-llm/` (HEAD `1765f29`)
  con lo stesso metodo. Nessun file `.claude`/`.git` presente nella copia.
- `assets/` non copiata in nessuno dei due casi: era vuota (ontologia) o assente
  (dominio) su disco in entrambi i sorgenti al momento della copia, verificato prima di
  procedere — nessuna perdita. Se in futuro uno dei due sorgenti accumula contenuto in
  `assets/` prima di una nuova copia, andrà incluso deliberatamente.
- `design-system/` lasciata vuota di proposito: le linee guida sono ancora in test in
  `portfolio/site/`, non ancora mature da formalizzare qui.

**Trovato durante la creazione, non toccato**: esiste già un laboratorio informale precedente in un'altra cartella locale,
uno spazio (si definisce così nel proprio README) con prototipi
precedenti dello stesso concetto — struttura vera dichiarata esplicitamente rimandata a
quando il lavoro fosse più maturo. Fuori scope per questo repository, che è quel
momento di maturità con un'altra struttura; non migrato né toccato.

## 2026-09-04 — Design system: prima consolidazione dopo 5 prototipi verificati

Sessione dedicata a leggere il saggio e l'ontologia, prototipare in
`design-system/lab/` (non nei file reali) e infine scrivere
[`../design-system/README.md`](../design-system/README.md). Decisioni che vale la pena
registrare qui perché non ovvie a rileggerle in futuro:

- **Palette**: adottata quella già confermata di `portfolio/` (non
  inventata qui), con un vincolo non scritto altrove — ogni famiglia di colore
  appartiene a un solo dominio (blu = navigazione del saggio, arancio = apparato del
  saggio, verde = ontologia) e non si mescolano mai nello stesso componente. Verificato
  esplicitamente rimuovendo l'arancio lasciato per errore nella sidebar.
- **Eccezione categoriale**: i widget con più di 3 categorie (mappe embedding, 4
  gruppi) riusano le 3 famiglie a piena saturazione più *un solo* colore preso da
  altrove nel progetto (il prugna `--cat-attribuzione`, già nella Lente semantica) —
  mai una palette nuova costruita da zero per un widget.
- **Integrazione dominio/ontologia** — la tesi del case study, per la prima volta
  concreta: termini nel saggio (scelti da `:discussoInUnita` nell'ontologia, non a
  occhio) aprono una tenda con dati letti da `ontologia/output/concetti/*.html` più un
  link alla Lente. Deliberatamente *non* la lente incorporata in miniatura (idea
  originale del brief) — troppo lavoro per essere fatto due volte, rimandato a dopo
  aver convertito `ontologia/output/`. Fatto solo per Meccanismo · 3 finora.
- **Vincolo esplicito dell'utente, rispettato in tutti i test**: mai toccare
  `ontologia/src/*.ttl` né `ontologia/scripts/*.py` — trattati come asset, non come
  codice di questo repository. Confermato possibile: tutta la logica colore di
  `lente.js` passa già per `var(--token)`, mai valori letterali — ristilizzare senza
  toccare la logica è stato possibile riscrivendo solo `lente.css`.
- **Bug trovati verificando dal vivo, non a lettura**: `.opcard .symbol` non renderizzava
  mai in mono per un conflitto di specificità CSS (classe `mono` presente ma inerte);
  una regola `.ctx-grid` persa durante una riscrittura ha reso la mini-mappa di
  Meccanismo · 5 fuori scala, poi trovata con un diff sistematico di tutti i selettori
  contro l'originale — pratica da ripetere per ogni conversione successiva.

Non ancora deciso: i due esempi originali del brief (box "1"/"0", linea luminosa) —
vedi `design-system/README.md`, sezione Componenti verificati.

## 2026-09-04 — Box "1"/"0" e linea luminosa: fuori scope

I due esempi rimasti aperti dal brief originale — box "1"/"0" a bordo sfumato, "linea
luminosa" con la curva smoothstep di Unità 4.5 — vengono scartati invece che
prototipati. Decisione di priorità: il lavoro restante va sulla conversione dei
capitoli e sull'estensione del rapporto dominio/ontologia, il cuore del case study;
questi due erano rifiniture decorative, non necessarie per dimostrarlo. I box "1"/"0"
restano con il trattamento già verificato nelle tavole di verità (vero →
arancio-scuro, falso → grigio-soft); nessuna linea luminosa viene introdotta. Prototipi
originali intatti in `portfolio/site/test-campioni/`, se in futuro servissero
altrove.

## 2026-09-04 — Promozione ai file reali: 5 capitoli, Lente, ontologia/output

Primo lavoro sui file reali di `dominio/` e `ontologia/` (finora tutto era rimasto in
`design-system/lab/`). Prima di iniziare, corretta un'imprecisione: si era detto che
Fondamenti · 1 fosse "già fatto" — falso, esisteva solo in `lab/`. Verificato con grep
mirati prima di procedere (mai fidarsi di un riepilogo senza controllare lo stato
attuale dei file).

- **Promossi ai file reali**: Fondamenti · 1, Genealogia · 1, Meccanismo · 3/4/5
  (`dominio/src/saggio/*.html`), la Lente semantica (`ontologia/lente-semantica/
  output/lente.css`) e tutto `ontologia/output/` (`style.css`, un solo file condiviso
  da 194 pagine — zero `style=` inline, zero colori letterali fuori da esso, verificato
  con grep su tutta la cartella prima di procedere). Ogni rewrite verificato con diff
  sistematico dei selettori contro l'originale (zero persi, zero inattesi) più test dal
  vivo nel browser (font caricati, console pulita, colori letti via
  `getComputedStyle`).
- **Font EB Garamond**: `dominio/src/saggio/` non aveva una casa reale per i file
  self-hosted (in `lab/` era una copia locale di comodo). Creata
  `dominio/src/saggio/fonts/`, stessi file di `ontologia/output/fonts/` — copia
  locale deliberata, non un riferimento incrociato fra `dominio/` e `ontologia/`
  (restano alberi indipendenti), stesso principio già applicato in `lab/`.
- **Bug reale trovato in promozione**: il link dalla tenda di Meccanismo · 3 alla Lente
  semantica usava `../../ontologia/...`, profondità corretta per la posizione in
  `design-system/lab/` (2 livelli sotto radice) ma sbagliata per la posizione reale
  `dominio/src/saggio/` (3 livelli) — puntava a `dominio/ontologia/...`, inesistente.
  Corretto in `../../../ontologia/...` e verificato end-to-end: click sul termine nel
  saggio reale → tenda con dati corretti → Lente reale, nodo giusto selezionato via
  hash-routing. Nessun altro riferimento relativo di questo tipo nei 5 file (verificato
  con grep su tutti).
- **`ontologia/output/style.css`**: la palette cream (`--carta`/`--bordo`/
  `--inchiostro-attenuato` unico) sostituita da bianco/brina/inchiostro/grigio +
  verde a tre gradi. `--inchiostro-attenuato` e `--bordo` non erano rinominabili 1:1:
  ogni uso è stato riclassificato per ruolo (apparato/breadcrumb → `--grigio-soft`,
  prosa secondaria come sottotitoli e note → `--grigio-testo`, bordi/divisori reali →
  `--line`; mai `--line` come colore di testo, è pensato solo per tratti a bassa
  opacità) — stessa distinzione già fatta per `lente.css`, non una scelta nuova.
- **`dominio/output/dal-bit-alle-entita-semantiche_it.html`** (bundle generato da
  `dominio/src/build_output.py` da tutti i capitoli di `saggio/`) lasciato intatto
  deliberatamente: rigenerarlo ora, con 7 capitoli ancora da convertire, produrrebbe un
  bundle a metà. Decisione separata, da riprendere quando tutto il saggio sarà
  convertito.

## 2026-09-04 — Licenza: decisione rimandata a prima della pubblicazione

Discusse quattro alternative (MIT + CC BY 4.0, MIT + CC BY-NC 4.0, Apache 2.0 +
CC BY-SA 4.0, tutti i diritti riservati). L'utente ha scelto di lasciare la decisione
aperta invece di sceglierne una ora, e di documentarla con un file `LICENSE`
placeholder che elenca le quattro opzioni invece di ometterlo — vedi
[`../LICENSE`](../LICENSE) e [next-steps.md](next-steps.md) per la roadmap verso la
pubblicazione. Non riguarda D3.js (BSD) né EB Garamond (OFL), già vendorizzati con
licenza propria.

## 2026-09-04 — Tema chiaro confermato come default, scuro rimandato a un tasto futuro

Domanda aperta fin dal primo test in `lab/` (vedi `lab/README.md`, "Cosa NON è
confermato"): il saggio era scuro prima di questa sessione, il resto del sistema
(portfolio, ontologia) già chiaro. Prima di convertire i 7 capitoli restanti, testata
una variante scura di Fondamenti · 1 (`design-system/lab/fondamenti-1-dark.html`) per
decidere con un confronto reale invece di un'assunzione.

- **Deciso**: chiaro resta il tema di default per tutto il saggio. Scuro confermato
  come idea valida ma rimandato a un tasto di switch da costruire in un secondo
  momento, non ora.
- **Perché rimandarlo non crea debito**: ogni colore in ogni file passa già per
  `var(--token)`, zero valori letterali (verificato ripetutamente in questa sessione).
  La prova è il test stesso: la variante scura ha richiesto di cambiare 14 valori in
  `:root` e zero delle ~30 regole di componente sotto. Un tasto reale in futuro costerà
  la stessa cosa, capitolo per capitolo — derivare i valori scuri partendo da questo
  file come modello, più uno switch JS con persistenza — non serve un'architettura
  diversa preparata in anticipo.
- **Valori scuri derivati e verificati** (contrasto WCAG calcolato per ogni coppia
  testo/sfondo, tutte ≥4.5:1): `--bianco:#1E2128 --brina:#14161B
  --inchiostro:#EDEAE4 --grigio-testo:#B4AEA2 --grigio-soft:#928B7D
  --blu:#8296E0 --arancio-scuro:#F0A363 --arancio:#D4823F --line:rgba(237,234,228,.16)`.
  Nota: in questo file "-scuro"/"-chiaro" descrivono il ruolo ereditato dal chiaro
  (testo/link vs bordi), non il rango di luminosità assoluta — un tasto reale vorrà
  nomi propri, non un riuso di questi.
- `fondamenti-1-dark.html` resta in `lab/` come riferimento, non cancellato — punto di
  partenza pronto quando il tasto verrà costruito.

## 2026-09-04 — Fondamenti · 2: primo capitolo convertito senza passaggio in lab/

Primo capitolo genuinamente nuovo (non promosso da un prototipo già verificato).
Confermato che si può andare dritti sul file reale: l'impianto è abbastanza stabile da
non richiedere più una tappa `lab/` separata, verificando comunque dal vivo nel
browser prima di considerarlo fatto (stessa disciplina, un passaggio in meno).

- **Principio chiarito qui, valido per i 6 capitoli restanti**: si preserva ogni
  numero specifico del capitolo (padding, dimensioni, clamp, timing delle animazioni —
  scelte editoriali pre-esistenti, non toccate) ma si applicano i valori di sistema
  ormai confermati per tutto il resto (famiglia di font, colori per ruolo,
  `letter-spacing: .06em` per il maiuscoletto) — anche quando il capitolo originale
  aveva fatto una scelta diversa (es. l'eyebrow qui era arancio acceso nell'originale,
  ora grigio-soft come da regola, non preservato "per fedeltà al capitolo").
- **Codice morto trovato e rimosso**: regole CSS per pallini di scroll-spy
  (`.unita-list.scrollspy`) mai usate in questo file — Fondamenti non ha la struttura
  ad accordion per unità che Genealogia/Meccanismo hanno. Verificato con grep che il
  markup corrispondente non esiste da nessuna parte nel file prima di toglierle.
- **Difformità dalla regola sui simboli mono**: due cifre binarie ("1" e "0" in mezzo a
  una frase) erano in `<span class="mono">` — non uno dei quattro simboli logici
  ammessi, quindi passate a `<em>`, stesso trattamento già dato ai box "1"/"0" di
  Fondamenti · 1.
- **Font Google non più necessari**: il capitolo non usa nessuno dei quattro simboli
  logici, quindi tolto anche il link a IBM Plex Mono su Google Fonts (zero richieste
  di rete in meno) — il token `--mono` resta dichiarato per coerenza con gli altri
  file, semplicemente inutilizzato qui.
- **Verifica sistematica**: diff dei selettori contro l'originale (110 → 107: -4 dead
  scrollspy, +1 `.apparato`, nessuna perdita imprevista) più test dal vivo di ogni
  componente nuovo del capitolo (chat mockup, rack-grid del data center, confronto
  CPU/GPU, interruttore del transistor con la scala che si illumina, tabella di
  verità) — inclusi i colori accesi via interazione (click sull'interruttore),
  verificati con `getComputedStyle`, non solo a occhio.

## 2026-09-04 — Ultimi 6 capitoli: conversione con script, verifica delegata all'utente

Su richiesta esplicita dell'utente ("metodo rapido... con risparmio di token
delegando a me la verifica in browser"), Genealogia · 2/3/4 e Meccanismo · 1/2/6
convertiti con uno script Python invece che a mano file per file. Prima di scrivere
lo script, verificato con grep che tutti e 6 usano lo stesso identico schema di
token vecchio (`--bg/--surface/--surface-2/--copper/--copper-bright/--text/
--text-dim`) — confermato, zero varianti — e che nessuno dei widget unici di
ciascun capitolo usa canvas, `getComputedStyle` o colori letterali fuori da
`:root` (a differenza di Meccanismo · 4/5): sono tutti CSS puro, automatizzabile
con sicurezza.

- **Script in due stadi** (`convert_chapter.py`, in scratchpad, non nel
  repository): stadio 1 sostituisce per intero i ~10 blocchi CSS condivisi
  (font-face/`:root`/body/heading/sidebar/eyebrow/aside/question/blockquote/
  hero/scrolldown/chiusura) con il testo già verificato di Fondamenti · 2 —
  ogni blocco deve comparire esattamente 1 volta o lo script si ferma e lo
  segnala, non prova a indovinare. Stadio 2 gestisce il resto (i widget unici
  di ogni capitolo) con sostituzioni di token non ambigue ovunque, più
  un'euristica per i tre token ambigui (`copper-bright`, `copper`, `text-dim`):
  un blocco con maiuscoletto e senza un proprio bordo è un'etichetta muta
  (→ grigio-soft), altrimenti è un accento (→ arancio-scuro/arancio/
  grigio-testo). L'euristica ha classificato correttamente casi non banali
  verificati a mano dopo: `.disc-chip`/`.tl-tag` (badge col bordo proprio →
  accento, non etichetta) e `.gap-table th` (intestazione con sottolineatura
  propria nell'originale → accento, coerente con la distinzione già fatta
  dall'autore originale, non con la regola delle tavole di verità booleane).
- **Semplificazione dichiarata**: la spaziatura delle lettere del maiuscoletto
  non è stata normalizzata a `.06em` come nei capitoli fatti a mano — resta il
  valore originale di ciascuna etichetta (si va da .05em a .14em a seconda del
  capitolo). Differenza impercettibile a occhio su testo così piccolo; scelta
  fatta per tenere lo script semplice, non un compromesso di qualità.
- **Tre casi non automatizzabili, corretti a mano**: nel widget di Cantor
  (Meccanismo · 1), tre elementi hanno testo colorato con quello che nel tema
  scuro era `var(--bg)` per restare leggibile sul proprio riempimento colorato
  — un ruolo diverso da "colore di sfondo pagina", che lo script non poteva
  distinguere da solo. Contrasto calcolato (WCAG) per scegliere fra testo
  scuro o chiaro caso per caso: `.cantor-digit.diag` (riempimento arancio più
  chiaro) → testo inchiostro (contrasto 5.17:1); `.cantor-digit.flipped` e
  `.cantor-btn` (riempimento arancio-scuro più scuro) → testo bianco
  (5.32:1) — la stessa risposta univoca non avrebbe funzionato per entrambi.
- **Verifica**: diff dei selettori e grep dei token vecchi su tutti e 6 i file,
  zero perdite e zero residui ovunque; test dal vivo solo su due file scelti
  come campione (Genealogia · 4, il più semplice; Meccanismo · 2, il più
  complesso — grafico di calibrazione SVG, barre n-grammi, diagramma di
  dipendenza) per un controllo di ragionevolezza, non una verifica completa.
  La verifica visiva/interattiva di tutti e 6 i file resta all'utente, come
  concordato.

## 2026-09-04 — Presentazione, appendice widget, e primi 2 capitoli con tenda concetti

Chiusa la conversione di palette (`presentazione.html` e `dietro-i-widget.html`,
mancanti dal giro precedente — nessuna `:Unita` propria in `dati.ttl` per queste due
pagine, quindi fuori dallo scope dell'integrazione ontologica sotto). Trovato e
lasciato intatto `indice.html`: stesso tema vecchio, ma zero link in entrata da
qualunque pagina raggiungibile — orfano, non toccato.

`presentazione.html` aveva una formattazione leggermente diversa (es. `.mono` su più
righe) che ha fatto fallire silenziosamente alcuni blocchi dello script — convertito
a mano invece di forzare lo script a tollerarla. Trovate e rimosse tre regole CSS
morte (`.aside`, `blockquote`, `.scrolldown`): mai usate nel corpo di questa pagina
specifica, verificato con grep prima di toglierle.

Poi estesa la tenda di concetti (finora solo Meccanismo · 3) a Fondamenti · 1 e 2,
dopo che l'utente ha chiesto di vedere questi due prima di dare il via libera sul
resto del saggio (9 capitoli, ~115 termini stimati, contati da `:discussoInUnita`
— vedi la tabella nella conversazione, non ripetuta qui).

- **Conteggio corretto durante il lavoro**: la stima iniziale data all'utente per
  Fondamenti · 1 era 5 concetti; controllando `dati.ttl` con grep mirato (non a
  memoria) sono 4 — `Discretizzazione` è assegnato solo a Fondamenti · 2, non a
  Fondamenti · 1. Corretto prima di scrivere codice, non dopo.
- **Bug reale trovato ed esteso a tutti i capitoli, non solo ai due nuovi**: la
  funzione `apriTenda` di Meccanismo · 3 aveva "Meccanismo · " scritto a mano nel
  template della sezione "Discusso in" — innocuo lì perché ogni concetto di quel
  capitolo è discusso solo dentro Meccanismo, ma sbagliato in generale: alcuni
  concetti (es. `Discretizzazione`) sono discussi in capitoli di Parti diverse
  (Fondamenti E Meccanismo). Tolto il prefisso fisso dal template, spostato dentro i
  dati stessi di ogni concetto (`discussoIn: [["Fondamenti · 2", ...], ["Meccanismo ·
  1.1", ...]]` invece di `[["2", ...]]`) — aggiornati anche gli 11 dati di
  Meccanismo · 3 per lo stesso formato, verificato dal vivo che il caso
  multi-capitolo (`QualitaPrimarieSecondarie`, discusso sia in 3.2 sia in 5.4) renda
  correttamente entrambi i prefissi.
- **Due concetti senza corrispondenza testuale letterale**: `HardwareEFondamenta
  Computazionali` (l'ombrello dei due capitoli) e `Discretizzazione` non compaiono
  come parole nel testo di Fondamenti. Agganciati a parole evocative già presenti
  nella prosa — "silicio" e "transistor" per la prima (stessa frase di chiusura di
  Fondamenti · 1), "sequenze di 0 e 1" per la seconda (nella card Software di
  Fondamenti · 2) — stesso principio già usato per `SpazioSemanticoEEmbedding` in
  Meccanismo · 3, agganciato alla sola parola "spazio" nell'hero.
- **Verifica**: ogni bottone testato dal vivo (click reale via JS, non lettura del
  codice) — titolo, dati nel corpo della tenda, e link alla Lente risolto
  correttamente per tutti i 9 concetti nuovi; colore verde-scuro confermato via
  `getComputedStyle` anche dentro il riquadro `.question` (arancio di suo), per
  controllare che la cascata CSS non venisse silenziosamente sovrascritta.

## 2026-09-08 — Tenda dei concetti estesa a tutto il saggio: i 9 capitoli restanti

Completato il rollout della tenda di concetti (finora solo Meccanismo · 3 e
Fondamenti · 1/2) ai 9 capitoli rimanenti — Genealogia · 1/2/3/4, Meccanismo ·
1/2/4/5/6 — dopo il via libera dell'utente a procedere sul resto del saggio senza
ulteriori check-in per capitolo. Stesso metodo ovunque: concetti scelti da
`:discussoInUnita` in `dati.ttl` (mai a occhio), ancore verbatim nel testo esistente
(letterali dove possibile, una singola frase evocativa onesta per i concetti-ombrello
senza corrispondenza testuale — stesso principio già stabilito per Fondamenti),
verifica dal vivo con click reale via JS su ogni bottone di ogni capitolo prima di
considerarlo fatto.

- **Bilancio, contato con grep sui file reali, non a memoria**: Genealogia ·
  1/2/3/4 → 14/12/11/8 concetti; Meccanismo · 1/2/4/5/6 → 14/10/18/11/11 concetti.
  Meccanismo · 4 è il capitolo più grande dell'intero saggio (18 concetti), unico a
  includere il "terzo filo" del corso — biologia della cognizione e teoria dei
  sistemi (Autopoiesi, Chiusura operazionale, Pleroma e creatura, Schismogenesi) —
  accanto ai concetti tecnici delle reti neurali.
- **Bug reale trovato in Meccanismo · 1, non ipotizzato**: un colore hex vecchio del
  tema (`#F0A85E`, copper-bright) era rimasto scritto a mano dentro una stringa SVG
  generata via JS (`rs-svg-frame`, il cerchio del confronto raster/vettoriale) —
  invisibile sia allo script di conversione a token CSS del 4 settembre (che vede
  solo CSS, non stringhe JS) sia a un primo audit grep che escludeva deliberatamente
  i 7 valori hex vecchi come "già considerati risolti" — un errore metodologico
  proprio, non solo dello script. Corretto in `#A85419` (arancio-scuro nuovo); rifatto
  un audit completo senza esclusioni su tutti i 14 file del saggio per verificare che
  fosse un caso isolato — confermato, zero altre occorrenze (a parte `indice.html`,
  già orfano e fuori scope).
- **Formato `discussoIn` cross-Parte**: la correzione del 4 settembre (prefisso
  "Parte · Numero" dentro i dati di ogni concetto, non nel template `apriTenda`) è
  stata usata fin dall'inizio per tutti i 9 nuovi capitoli — nessun retrofitting
  necessario questa volta.
- **Verifica**: ogni bottone di ogni capitolo cliccato via JS (non letto a codice),
  con controllo di titolo e corpo della tenda; i widget interattivi preesistenti di
  ogni capitolo ri-verificati funzionanti dopo le modifiche (predittore n-grammi e
  diagramma di calibrazione in Meccanismo · 2; neurone/XOR/paesaggio della perdita
  in Meccanismo · 4; grafi di attention e chip di posizione in Meccanismo · 5; slider
  di scala e barra di quantizzazione in Meccanismo · 6).

## 2026-09-08 — Presentazione: testo di chiusura riscritto, prima tenda concetti sulla pagina

`presentazione.html` non aveva ancora la tenda dei concetti (fuori scope nel giro
del 4 settembre, insieme a `dietro-i-widget.html`, per assenza di `:Unita` proprie
in `dati.ttl`). Il paragrafo di chiusura della Parte 3 ("La lente semantica")
descriveva ancora l'esplorazione termine-per-termine come "in preparazione" — non
più vero, visto il rollout appena completato. Riscritto su testo proposto e poi
emendato dall'utente in più passaggi, spiegando il meccanismo reale in due livelli
(tenda inline → Lente semantica) e tenendo esplicitamente distinte le due
suddivisioni della Lente, facili da confondere: nodi per tipo nel menu a tendina
della sidebar, relazioni per categoria nel glossario in fondo al pannello.

- Aggiunto per la prima volta lo scaffold completo della tenda (CSS + markup + dati)
  a `presentazione.html`, con un solo concetto (`Embedding`) reso cliccabile come
  esempio dal vivo — scelto perché è lo stesso concetto dietro l'esempio «re, donna,
  regina» già in apertura della pagina, a chiudere il cerchio.
- Verificato dal vivo: click reale sul bottone, dati corretti nel corpo della
  tenda, link alla Lente semantica risolto.

## 2026-09-08 — Poster del grafo completo con lightbox, su richiesta dell'utente

L'utente ha chiesto una rappresentazione del grafo da mettere in fondo alla
presentazione. Valutate tre opzioni (poster statico calcolato sui dati reali,
mini-Lente interattiva incorporata, diagramma tassonomico semplificato disegnato a
mano) — scelta la prima: coerente con il principio già stabilito nel saggio ("ogni
componente è calcolato su dati reali, non inscenato") e senza rischiare di
duplicare/indebolire lo strumento interattivo già linkato subito sopra.

- **Calcolo**: nessuna libreria Python per grafi disponibile sulla macchina
  (networkx/matplotlib/graphviz assenti) — usato invece D3 (già vendorizzato per la
  Lente semantica) con gli stessi dati reali di `grafo.js` (258 nodi, 537 relazioni).
  Simulazione a forze (`d3.forceSimulation`, 400 tick, eseguita in una pagina di
  scratch nel browser, non in un build step) per calcolare un layout reale — nessun
  nodo o collegamento disposto a mano. Colori riusati identici a quelli di
  `lente.js`/`lente.css` (7 colori per tipo di nodo, 4 per categoria di relazione),
  non una palette nuova.
- **Etichette selettive**: solo i ~20 nodi di tipo Concetto/Teorico/FiloTrasversale/
  StatoEpistemico con grado ≥6 sono etichettati (Attention, Embedding, Reale, Storia
  dell'intelligenza artificiale...) — unità/capitoli/parti restano punti non
  etichettati, per non riempire il poster di codici interni (`U41`, `Gen12`...)
  illeggibili fuori contesto.
- **Asset**: salvato come SVG statico in
  `dominio/src/saggio/immagini_presentazione/mappa_del_grafo.svg` (99KB dopo
  arrotondamento delle coordinate, non inline nell'HTML) — non in una cartella
  `assets/`, che nel `.gitignore` di questo repository non viene tracciata.
- **Lightbox**: click sull'immagine per ingrandirla (overlay a schermo intero,
  chiusura con click fuori/sulla X/Esc) — trattandosi di un SVG l'ingrandimento è
  senza perdita di qualità. Bug trovato e corretto durante la verifica: il
  contenitore del lightbox non aveva una larghezza esplicita, causando un collasso a
  0×0 dell'immagine (sizing circolare fra un box shrink-to-fit e un'immagine con
  `max-width:100%`) — risolto dando al contenitore `width: min(94vw, 1200px)`
  invece di lasciarlo intrinseco.
- **Verifica**: apertura/chiusura in tutte le modalità testate con click reale (non
  solo lettura del codice); dimensioni renderizzate confrontate col viewBox per
  escludere schiacciamenti.

## 2026-09-08 — Verde più luminoso: dal tono più scuro al tono medio, ovunque

Test di grafica su un prototipo separato di pagina di portfolio: il verde usato per il testo dei rimandi era `--verde-scuro` (`#2A5628`,
il più scuro dei tre), giudicato troppo cupo. Passato a `--verde` (`#3D7A3A`, il tono
medio) lì, poi esteso su richiesta dell'utente a tutto ciò che condivide lo stesso
ruolo — "verde = stai per lasciare la prosa ed entrare nell'ontologia" — nel saggio
reale e nella Lente semantica.

- **Contrasto verificato prima di scegliere** (stesso metodo WCAG già usato altrove
  in questo progetto): `verde-scuro` su bianco ≈ 8.5:1, `verde` ≈ 5.2:1 (passa
  comunque la soglia di leggibilità 4.5:1), `verde-chiaro` (`#7AAD76`, il terzo tono
  della palette) solo ≈ 2.6:1 — troppo poco per essere usato come testo, scartato.
  La stessa verifica vale simmetricamente per gli usi come sfondo con testo bianco
  sopra (es. bottone attivo della Lente): contrasto identico, ~5.2:1.
- **Cambiati** (13 file del saggio — tutti e 12 i capitoli più `presentazione.html`):
  colore a riposo di `.termine-concetto`, `.tenda-eyebrow`, `.tenda-titolo .tag`,
  `.tenda-lista .rel-tipo`. Verificato con grep che i 13 file avessero lo scaffold
  byte-identico prima di applicare la stessa sostituzione a tutti in un colpo solo.
- **Cambiati** (Lente semantica, `lente.css`): colore di base dei link, bottone di
  grado attivo, contatore per gruppo, riga selezionata nella sidebar, badge di
  grado, numero nel breadcrumb.
- **Lasciati intenzionalmente invariati**: i due stati `:hover` che usano
  `verde-scuro` (`.tenda-chiudi:hover` nel saggio, `.satellite:hover text` nella
  Lente) — è un pattern di interazione legittimo (il colore si approfondisce al
  passaggio del mouse), non un rimando che si legge normalmente, quindi fuori dallo
  scope della richiesta.
- **Verifica**: colore letto via `getComputedStyle` (non a occhio) su un capitolo
  campione e sulla Lente semantica dopo la modifica; screenshot di conferma.

## 2026-09-08 — Dimensione dei caratteri +20%, non registrato finora

Voce mancante in questo log fino ad ora: lo stesso test di grafica sul
prototipo PMI che ha portato al verde più luminoso (voce precedente) aveva
confermato anche che EB Garamond risultava visivamente piccolo. Applicato
`font-size: 120%` su `html` a 13 dei 14 file navigabili del saggio (i 12
capitoli più `presentazione.html`), stesso giro di lavoro, stesso commit.
L'appendice `dietro-i-widget.html` è rimasta fuori — non risulta una
motivazione registrata all'epoca; verificare se sia un'omissione o una scelta
deliberata prima di un prossimo intervento sulla tipografia.

## 2026-09-09 — `indice.html` rimosso, non ricollegato

Deciso dall'utente dopo aver riletto il contenuto: la sidebar presente in ogni
pagina del saggio copre già la stessa funzione di mappa di consultazione che
`indice.html` offriva come pagina a sé — mantenerlo come pagina separata non
aggiunge nulla, solo un secondo posto da tenere sincronizzato.

Verificato prima di rimuoverlo che non fosse contenuto obsoleto da salvare in altra
forma: tutti gli anchor (`#unit-a1`, `#unit-b1`, ecc.) referenziati puntavano a id
realmente presenti nei file attuali — la struttura elencata era accurata al 100%,
il problema era solo l'isolamento (tema scuro originale mai convertito, font
diversi dal resto — Space Grotesk/Source Serif 4 invece di EB Garamond) e la totale
ridondanza con la sidebar. File committato nel commit iniziale
(`feat(init)`, 4 settembre 2026) — rimosso dalla working tree ma recuperabile dallo
storico git in qualunque momento, nessuna perdita reale.

## 2026-09-09 — Sidebar e presentazione: indice riorganizzato, abstract editoriale

Sessione di modifiche puntuali guidate dal vivo nel browser (screenshot +
elemento selezionato, una modifica alla volta, verifica immediata) su
`presentazione.html`.

- **Sidebar**: titolo del saggio passato da tutto maiuscolo a maiuscoletto, blu,
  grassetto, e reso un link diretto al titolo/abstract in apertura pagina
  (`<a class="sidebar-title" href="presentazione.html#apertura">`). Kicker
  "Indice" passato da grigio a blu chiaro.
- **Bug reale trovato e corretto**: la voce "Presentazione" nell'indice
  risultava nera invece che blu — `.sidebar .voce-presentazione` (specificità
  0,2,0) perdeva contro la regola preesistente `.sidebar details.modulo summary`
  (0,2,2) nonostante fosse dichiarata dopo nel foglio di stile; la specificità
  decide, non l'ordine. Risolto qualificando il selettore
  (`.sidebar details.modulo summary.voce-presentazione`, 0,3,2).
- **"Presentazione" non è più una voce collassabile**: era un `<details>` con
  `<summary>` proprio, unica voce dell'indice trattata diversamente dalle
  "Parte I/II/III" (semplici `<div class="parte-heading">`). Uniformata: ora è
  un `div.parte-heading` come le altre, la lista dei 4 sotto-capitoli resta
  sotto come prima (con lo scrollspy che la illumina scorrendo). La regola CSS
  duplicata `summary.voce-presentazione` (identica a `.parte-heading`, non più
  referenziata) è stata rimossa.
- **Bug reale nello scrollspy, trovato verificando lo scroll dal vivo, non a
  lettura**: l'`IntersectionObserver` usava `threshold: 0.5` — una sezione
  doveva occupare il 50% del viewport per "accendere" il pallino
  corrispondente nell'indice. Le quattro sezioni sono tutte più alte del
  viewport (calcolato: il massimo raggiungibile va dal 29% al 41% per tre
  sezioni su quattro), quindi la soglia non era quasi mai raggiungibile.
  Sostituito con una fascia sottile al centro del viewport
  (`rootMargin: '-45% 0px -45% 0px', threshold: 0`) — tecnica standard per
  scrollspy con sezioni di altezza variabile, indipendente dall'altezza della
  sezione.
- **Contenuto riorganizzato**: il contenuto introduttivo, prima paragrafi
  sciolti sotto un unico "abstract" generico, è diventato una vera Parte 1
  ("Da «re» a «regina»", i 5 paragrafi sul gioco linguistico re/regina, bit,
  le due fasi del lavoro, l'agente AI, il controesempio) — indice a 4 voci
  (1 Da «re» a «regina», 2 I limiti che condividiamo, 3 Struttura,
  composizione e stack del saggio interattivo, 4 Il grafo e la lente
  semantica), rinumerando le vecchie Parte 1/2/3 a 2/3/4 con titoli più
  brevi.
- **Malinteso corretto durante il lavoro**: un'istruzione in due punti
  ("qui inizia il paragrafo 1 del nuovo indice" + "il primo paragrafo diventa
  l'abstract") è stata inizialmente fraintesa come riferita allo stesso
  paragrafo — in realtà il secondo "primo paragrafo" indicava il primissimo
  paragrafo della pagina (il sottotitolo), non il primo elemento della nuova
  Parte 1. Corretto spostando il trattamento editoriale (etichetta "Abstract"
  centrata) sul sottotitolo, non sul paragrafo re/regina.
- **Trattamento editoriale dell'abstract**, affinato in tre passaggi su
  richiesta esplicita: capolettera grande e colorato con linee di bordo →
  capolettera più piccolo senza bordi → nessun capolettera. Resta solo
  l'etichetta "Abstract" in maiuscoletto centrato sopra il testo.

## 2026-09-09 — Lente semantica: secondo grado come ramificazione leggibile

Lacuna di leggibilità nota da tempo (già segnalata in `next-steps.md`): nel
grafo radiale, i vicini di secondo grado erano punti pieni collegati da una
linea dritta quasi invisibile (`opacity: 0.35`), nominati solo dal tooltip
nativo del browser al passaggio del mouse — nessuna etichetta visibile, nessun
filtro di legenda funzionante (mancava `data-cat` sui nodi di secondo grado,
bug indipendente trovato durante il lavoro).

Messo a punto in due prototipi isolati in `ontologia/lente-semantica/lab/`
(`backpropagation-grado2.*`, poi `attention-grado2.*` come caso denso — 16
relazioni di primo grado contro le 9 di Backpropagation) prima di toccare la
pagina reale, su richiesta esplicita dell'utente.

- **Prima ipotesi sbagliata, corretta durante il lavoro**: sembrava bastasse
  una curva a ramo (`d3.linkRadial`, geometria da dendrogramma) al posto della
  linea dritta. Verificato dal vivo che i rami continuavano ad attraversare
  l'etichetta del proprio nodo padre — **causa reale**: l'etichetta del nodo
  non corre tangente al cerchio come sembrava a un primo sguardo, corre
  radialmente verso l'esterno (stessa direzione in cui si aprono i rami), e
  `d3.linkRadial` resta vicino all'angolo di partenza per quasi tutta la
  lunghezza della curva (verificato campionando punti lungo il tracciato: a
  metà percorso ancora a metà dello scarto angolare totale) — comodo per
  alberi con salti di raggio ampi, non per questo caso.
- **Fix**: curva su misura (`ramoPath`) che diverge subito dall'angolo del
  nodo padre invece di restarci vicina; ventaglio simmetrico che alterna i
  figli a destra/sinistra a distanza crescente (mai a scarto zero, dove
  cadrebbe esattamente sulla direzione dell'etichetta); etichetta piccola ma
  sempre visibile, non solo al hover; `data-cat` aggiunto (il filtro della
  legenda ora nasconde anche il secondo grado, prima non lo toccava affatto).
- **Verifica non solo a occhio**: controllo geometrico automatico (bounding
  box del testo ruotato, campionamento di punti lungo ogni ramo) su tutti i
  nodi di entrambi i prototipi — zero rami che attraversano l'etichetta del
  proprio nodo padre, in entrambi i casi. Confermato anche visivamente con
  zoom mirati nei punti più affollati del caso denso (Attention).
- **Portato in `output/lente.js`/`lente.css`** e riverificato sulla pagina
  reale con lo stesso controllo geometrico (stesso risultato: zero
  attraversamenti) più test funzionali dal vivo (click di navigazione sui
  nodi di secondo grado, filtro di legenda). Un problema di cache del
  server locale di sviluppo durante la verifica (script serviti stale anche
  dopo una navigazione fresca) risolto temporaneamente con un parametro
  anti-cache sui tag `<script>`/`<link>`, rimosso prima del commit.
- Due commit separati: uno per il lavoro di sidebar/presentazione sopra, uno
  per questa correzione — lavoro semanticamente indipendente.

## 2026-09-15 — Seconda passata di pulizia e riscrittura della storia git

Un audit indipendente (agente separato, modello diverso, istruito a leggere come un
revisore esterno ostile) ha trovato ciò che la prima passata aveva mancato: il nome
del repository privato del portfolio in 11 punti fuori da `dominio/src/saggio/`, un
percorso locale dentro l'RDF pubblicato (`dct:description` dello schema di concetti),
un commento che dichiarava ancora provvisorio il namespace già sostituito, percorsi che
iniziavano per `Desktop/` invece che per `/Users/` o `~/` — sfuggiti proprio per il
pattern usato nella prima ricerca — e una voce del decision-log di `dominio/` che
affermava la ripresa di una tesi letta in un libro. Verificata con una ricerca su tutti i
capitoli: quella tesi non compare nel saggio; la voce è stata corretta registrando la
verifica, non cancellata.

**La scoperta più importante riguardava il metodo, non il contenuto**: i commit di
correzione del primo giro erano additivi, quindi nomi e percorsi redatti restavano
leggibili nella cronologia (`git log -p`). Il repository non era mai stato pubblicato,
quindi la storia è stata riscritta con `git filter-repo` (`--replace-text` e
`--replace-message`, sui contenuti e sui messaggi), conservando tutti i commit e il loro
racconto — cambiano solo gli hash. Verifica dopo la riscrittura: zero occorrenze delle
stringhe sensibili in qualunque blob o messaggio di qualunque commit. Deliberatamente
**non** sostituito `example.org`: non è un dato sensibile, ed è il valore che questo
stesso log documenta come rimpiazzato — sostituirlo nella storia avrebbe reso
incomprensibile la voce che registra la sostituzione.

## 2026-09-19 — Licenza: tre regimi, uno per tipo di materiale

Chiusa la decisione rimandata dal 4 settembre. Nessuna delle quattro alternative
iniziali distingueva fra i tre beni presenti nel repository, che hanno valore diverso:

- **Il codice** vale poco in sé — la licenza è soprattutto un segnale di igiene. MIT.
- **L'ontologia** esiste per essere referenziata: un vocabolario pubblicato sotto un
  namespace dereferenziabile ma non riusabile è una contraddizione. CC BY 4.0,
  dichiarata anche dentro i dati (`dct:license`), con `owl:versionInfo "1.0"` a marcare
  la prima versione pubblicata.
- **La prosa del saggio** è capitale editoriale dell'autore. Tutti i diritti riservati,
  documentazione compresa.

Scartate le varianti NC e SA per l'ontologia: "non commerciale" è mal definito
proprio per il pubblico che deve valutare il lavoro (un'azienda non sa se aprirla in
contesto lavorativo sia uso commerciale); share-alike su un vocabolario obbligherebbe
chi lo importa a rilicenziare il proprio. Per la prosa, preferito il riservato a CC
BY-NC-ND per l'asimmetria di reversibilità: da riservato si può sempre allentare, da
una licenza aperta non si torna indietro sulle copie già distribuite — e resta
possibile un'eventuale cessione in esclusiva a un editore.

Corretto anche un errore del placeholder: D3.js v7 è sotto licenza **ISC**, non BSD.

## 2026-09-20 — Identificatori legacy rinominati prima della pubblicazione

Il namespace era già stato sostituito (15 settembre), ma il segmento locale di due
identificatori portava ancora il nome del corso da cui il saggio è stato estratto:
`:CorsoLLM` (lo schema di concetti, radice dell'intero vocabolario) e
`:VocabolarioBpeDelCorso` (il dataset del tokenizzatore). Stesso motivo del namespace:
un identificatore pubblicato è citabile, e rinominarlo dopo il push romperebbe ogni
riferimento esterno — oggi, con il repository ancora locale, è una sostituzione senza
costi di compatibilità, senza bisogno di `owl:sameAs`.

- Lo schema diventa **`:DalBitAlleEntitaSemantiche`**, specchio del titolo del saggio
  (già nel suo `dct:title`). Scartato `:VocabolarioDelSaggio`: sarebbe stato quasi
  omonimo del dataset `:VocabolarioBpe…`, due "vocabolari" di natura diversa (l'uno di
  concetti, l'altro di token del tokenizzatore).
- Il dataset diventa **`:VocabolarioBpeDelSaggio`**, con etichetta «Vocabolario BPE del
  saggio».
- Sostituiti alla fonte, non a mano nell'output: 126 occorrenze in `vocabolario.ttl`,
  `genera_html.py` (la query sui concetti di primo livello), `genera_dati.py`, da cui
  `dati.ttl` è stato rigenerato (diff: due righe). Reasoner OWL-RL e SHACL rieseguiti:
  conformi. Le pagine di `output/` sono risultate identiche a prima — controllo
  significativo, perché la home ne elenca i concetti di primo livello proprio tramite lo
  schema rinominato: se la query non avesse trovato più nulla, la pagina sarebbe cambiata.
  Nel grafo della Lente cambiano solo le tre righe del dataset.
- Non toccati: `termini-grezzi.md` (elenco storico del materiale grezzo di partenza) e le
  copie storiche dentro `design-system/lab/`, destinate a non essere pubblicate.
