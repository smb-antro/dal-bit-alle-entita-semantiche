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

## 2026-09-22 — Font self-hosted in una copia sola, e un difetto trovato nei subset

Primo passo della trasformazione del design system da prosa a sistema funzionante:
i font. Fatto **prima** di qualunque altra cosa e prima di registrare le immagini di
riferimento per la regressione visiva, perché un cambio di font sposta l'aspetto di
ogni pagina e si sarebbe confuso con le regressioni della migrazione vera.

**Il difetto trovato.** Tutti e 14 i file del saggio dichiaravano `'IBM Plex Mono'` in
`font-family`, ma solo 5 lo caricavano davvero (Fondamenti · 1, Genealogia · 1,
Meccanismo · 3/4/5): negli altri 9 il monospaziato era da sempre quello di sistema,
diverso da macchina a macchina. E nei 5 che lo caricavano, nessuno dei `unicode-range`
serviti da Google copriva U+2227 (∧), U+2228 (∨), U+2295 (⊕). Un `@font-face` non
viene usato per un codepoint fuori dal proprio `unicode-range` — anche quando il file
contiene il glifo: è la regola, non un caso limite. Quindi in Fondamenti · 1 i «quattro
simboli logici» a 2.1rem, affiancati in quattro riquadri, erano tre glifi di sistema
accanto a un `¬` in IBM Plex Mono. Il commento nel sorgente diceva «l'unico posto in
questa pagina dove `--mono` è confermato»: era esattamente il punto in cui non lo era.

Vale la pena registrare **come** è stato accertato, perché il primo metodo era sbagliato:
i confronti a pixel nel browser davano risultati contraddittori, dato che mettevano a
confronto due *file* diversi dello stesso carattere e il fallback dello stack non era
il monospaziato generico ma SF Mono. La prova non sta nel rendering ma nella
dichiarazione: i `unicode-range` del CSS servito.

**Cosa è stato fatto.** `design-system/fonts/` diventa l'unica copia dei font del
repository: EB Garamond spostato da `dominio/src/saggio/fonts/` (cartella ora
inesistente) e IBM Plex Mono nei tre pesi richiesti, dal pacchetto ufficiale
`@ibm/plex-mono` 2.5.0 (OFL-1.1), ciascuno con la propria licenza accanto.
`fonts.css` dichiara i cinque `@font-face` con percorsi relativi a sé stesso, così
funziona da qualunque pagina lo colleghi. I 14 file perdono 28 `@font-face` inline e
15 righe verso `fonts.googleapis.com`/`fonts.gstatic.com`: 14 righe aggiunte, 225
tolte.

**Verificato**, non dato per buono: ~~i 17 glifi non latini usati nel saggio (compresi
↔ ≈ ∼ ␣, anch'essi scoperti) sono tutti presenti nei file completi~~ —
**AFFERMAZIONE FALSA, corretta il 23 settembre 2026: vedi la voce di quel giorno.
IBM Plex Mono non contiene ∧ ∨ ⊕, e il metodo con cui l'avevo "verificato" non poteva
accorgersene.** Resta vero che: a pagina caricata
il browser dichiara 5 face invece di 17 e nessun `@font-face` inline; nessuna richiesta
di rete esterna; tutti i `<link>` dei 14 file risolvono su file esistenti.

**Cambiamento d'aspetto voluto e messo a verbale**: i 9 capitoli che ripiegavano sul
monospaziato di sistema ora mostrano IBM Plex Mono, e i tre simboli logici cambiano
disegno. Non è una regressione: è la correzione che rende uniforme la resa del
monospaziato sull'intero saggio, su qualunque macchina.

**Resta aperto**: i pesi 500 e 600 non risultano caricati sulla pagina provata, segno
che nessun elemento li usa. Se la registrazione delle immagini di riferimento lo
conferma su tutte le pagine, sono due file da eliminare — deciso sui dati, non adesso.

**Non toccati**: `ontologia/output/fonts/` e `design-system/lab/fonts/`, che restano
copie a sé finché l'ontologia non passerà anch'essa al design system condiviso.

## 2026-09-22 — Rete di sicurezza prima della migrazione: harness di regressione visiva

Prima di toccare il CSS condiviso serviva poter dimostrare, con un numero invece
che a occhio, che l'estrazione non cambia l'aspetto. `design-system/verify/`
pilota il Chrome di sistema con `playwright-core` (nessun binario di browser
scaricato) e confronta le immagini con Pillow: 28 bersagli, 65 immagini per giro,
circa 90 secondi. Copre le 14 pagine del saggio su due viewport, 8 pagine
campione dell'ontologia, la Lente con il secondo grado attivato per interazione
reale, gli stati interattivi (tenda aperta, `<details>` aperto, `:focus-visible`
raggiunto tabulando), `prefers-reduced-motion`, e i due canvas di `meccanismo-4`
salvati anche via `toDataURL`.

**Il requisito che ha fatto la differenza** era: due catture consecutive dello
stesso codice immutato devono dare zero differenze. Senza quel cancello l'harness
sarebbe sembrato funzionante fin dal primo giro; con esso sono emerse quattro
cause di non determinismo che una cattura singola non mostra mai.

- Una **corsa di rasterizzazione dei font**: dopo `document.fonts.ready` Chrome
  impiega ancora 100-200 ms a finire il testo appena passato al font definitivo.
  Pausa fissata a 300 ms, sopra la soglia misurata.
- Animazioni a tempo, congelate con `animation-duration: 0s` e non con
  `animation: none` — che farebbe ricadere sullo stile non animato e lascerebbe
  invisibile ciò che parte da `opacity: 0` con `fill-mode: forwards`.
- Un loop `requestAnimationFrame` in `meccanismo-4`, deterministico nella fisica
  ma non nei tempi: si aspetta che converga, non un numero di millisecondi.
- Il **dithering delle sfumature**, che ha costretto a ripensare la tolleranza.

**La tolleranza non è una percentuale di pixel, è l'entità della differenza.** Due
catture identiche possono differire su centinaia di migliaia di pixel restando
indistinguibili, perché il dithering non è riproducibile al bit. Una soglia
percentuale sarebbe dovuta salire al 4% per assorbirlo, e a quel punto avrebbe
lasciato passare cambiamenti veri. Misurando il delta per canale le due
popolazioni si separano nettamente: fino a 2 è rumore (~18.000 pixel per giro su
~900 milioni), da 3 in su è segnale. Il valore non è a occhio: un bersaglio ha
mostrato 16 pixel a delta 2 in un confronto e zero nel successivo.

**Una pista convincente e sbagliata, registrata perché il ragionamento si
ripeterà**: 25 bersagli su 65 superano i 16384px di altezza (il limite delle
texture di Chrome, fino a 54.900px) e una differenza intermittente cadeva in un
riquadro che finiva esatto a y=16384. Sembrava causa ed effetto. La cattura a
fasce da 8000px è stata implementata e poi rimossa: misurando l'entità di quelle
differenze erano tutte di 1 livello su 255 — Playwright cuce bene, il limite non
corrompe nulla, e le fasce introducevano più rumore di quanto ne togliessero.
Correlazione scambiata per causa, smontata misurando invece di contare.

Validazione finale: 4 catture indipendenti, 6 confronti a coppie, zero fallimenti.

**Trovata una lacuna di accessibilità reale**, non un difetto dell'harness:
`fondamenti-2-hardware-software.html` ha tre cursori con
`animation: 1.2s infinite blink` che continuano a lampeggiare anche sotto
`prefers-reduced-motion: reduce`, perché il blocco `@media` di tutte e 14 le
pagine contiene soltanto `scroll-behavior: auto`. L'harness ora la censisce a ogni
giro (`animazioni-infinite.json`). Va chiusa nel layer `reset` del design system,
con un reset che fermi davvero animazioni e transizioni sotto quella media query.

## 2026-09-22 — Riconciliazione tipografica: una sola scala per tutto il saggio

L'inventario del CSS a livello di dichiarazione (parser scritto per l'occasione,
non `diff` testuale) ha trovato **41 selettori con valori diversi a seconda del
file**, e la buona notizia accanto: **zero divergenze nella palette** — le 33
custom property hanno lo stesso valore in tutti i 16 file che le definiscono. La
deriva era tutta tipografica, e seguiva i tre lignaggi di conversione già
registrati qui: 5 capitoli promossi da `lab/`, 7 convertiti con script, 2 a mano.

**Quanto si vedeva.** La sidebar è lo stesso indice in ogni pagina, ma era resa in
tre dimensioni: voce a 17,28px nei 5, 15,74px nei 9, 13,12px nell'appendice.
Passando da Genealogia · 2 a Genealogia · 1 l'indice di navigazione cambiava taglia
sotto gli occhi del lettore.

**Le scelte, prese dall'utente su un confronto visivo reale** e non su numeri
astratti:
- **Canonica la scala più piccola, quella dei 9.** La voce dell'indice sta a 0,78
  del testo invece che a 0,86: la navigazione resta apparato e non compete con la
  prosa, e nel binario da 300px le voci vanno meno a capo. La scala più grande era
  probabilmente un residuo dei prototipi `lab/`, già ingranditi prima che il +20%
  sulla radice venisse applicato a tutti.
- **L'appendice si allinea** (`html{font-size:120%}` anche lì). Era l'unica pagina
  al 100%: passando da un capitolo all'appendice tutto rimpiccioliva del 17%. La
  voce dell'8 settembre registrava l'esclusione come non motivata e chiedeva di
  chiarirla «prima di un prossimo intervento sulla tipografia»: era questo.
- **Interlinea 1.65**, **`.lede` 1.2rem** (unico caso senza maggioranza, 7 contro 7:
  scelto lo stacco più marcato, perché l'attacco si riconosca come tale).
- `fondamenti-2` torna alla norma dei capitoli: seguiva `presentazione` per un
  artefatto della conversione a mano, non per una scelta.

**Differenze conservate, e dichiarate tali** invece di essere appiattite:
`presentazione` resta variante copertina (hero più grande e maiuscolo, titolo di
sidebar in maiuscoletto blu cliccabile, kicker in `--blu-chiaro`, footer ravvicinato);
`ontologia/output` e la Lente mantengono corpo e interlinea propri, perché sono
superfici di consultazione, non di lettura continua; `.truth-table`, `.switch`,
`.tl-*`, `.playground .ptitle`, `.pg-example-btn` restano CSS locale — stesso nome
di classe ma widget diversi in pagine diverse. Quest'ultima è **collisione di nomi
da conoscere**: innocua finché quel CSS resta inline e non stratificato, un problema
il giorno in cui qualcuno provasse a estrarla.

**Metodo**: 121 sostituzioni, ciascuna con il valore atteso dichiarato prima; un
giro a vuoto ha verificato che tutte e 121 trovassero esattamente ciò che si
aspettavano, e solo allora si è scritto. Nessuna sostituzione a tentoni.

**Verifica.** L'harness, con la baseline registrata prima della riconciliazione, ha
separato nettamente il voluto dall'involontario: 45 bersagli del saggio cambiati,
**tutti e 18 quelli dell'ontologia e i 2 della Lente a zero differenze**, e
**a zero anche i due canvas di `meccanismo-4`** — cioè i nomi di custom property
letti dal JavaScript sono rimasti intatti. Controllato anche che nessuna delle 14
pagine tracimi orizzontalmente ai due viewport, e a occhio l'appendice, dove `rem`
e `px` convivono nei widget e il 20% in più poteva rompere qualcosa: integra.
A riconciliazione fatta, radice, voce, intestazione di parte e interlinea sono
**identiche su tutte e 14 le pagine**.

La baseline è stata poi rifatta su questo stato. Da qui la migrazione al design
system dovrà risultare a **zero differenze**: non è più «quasi uguale», è uguale.

**Perché prima e non dopo.** Riconciliare dopo l'estrazione avrebbe mescolato il
cambiamento voluto con le eventuali regressioni della migrazione, rendendo la rete
di sicurezza inutile proprio nel momento in cui serve. Stessa logica dei font.

## 2026-09-22 — Il design system diventa un sistema: token, layer, componenti

Le regole di design esistevano come prosa (`design-system/README.md`) e come CSS
ricopiato in 14 file. Ora esistono come **una fonte sola**, che le pagine
collegano: `design-system/css/design-system.css`, generato da token, base,
impianto e componenti. Il CSS inline dei capitoli passa da **4.539 a 1.250
righe**: quello che resta è CSS di widget, che è giusto stia dove sta.

**Tre livelli di token, con un'eccezione dichiarata.** Primitivi (la tavolozza) →
semantici (il ruolo) → componenti, che puntano ai semantici. L'eccezione: i
**primitivi conservano i nomi storici** e valori letterali, perché sono un
contratto pubblico — il JavaScript li legge per nome in 21 punti, sia via
`getComputedStyle` per disegnare i canvas di `meccanismo-4`, sia come
`var(--nome)` dentro stringhe che generano SVG inline (`meccanismo-1/3/5/6`,
`lente.js`). Chi disegna su un canvas ha bisogno di un colore concreto, non di un
ruolo. Un nome inesistente lì non dà errore: dà un canvas nero.

Il vincolo fondativo del design system — «una famiglia di colore appartiene a un
solo dominio» — smette di essere una regola scritta e diventa visibile nei nomi:
`--colore-navigazione`, `--colore-apparato`, `--colore-ontologia`.

**I cascade layer scavalcano la specificità: tre conseguenze vere, tutte trovate
dall'harness e nessuna prevista leggendo il codice.**

1. `.hero` (componente) contro `.unit-block section` (impianto). Prima vinceva la
   seconda per specificità: in 11 pagine su 14 l'hero sta dentro un unit-block e
   prende 92px, nelle altre 3 è autonomo e prende i suoi 62. Messe in due layer
   diversi, ha iniziato a vincere `.hero`, e 11 pagine hanno perso 30px per ogni
   hero. **Regola generale adottata**: due regole che si contendono la stessa
   proprietà devono stare nello stesso layer, così decide la specificità come
   prima. `.hero` è quindi in `layout`, accanto a ciò con cui si contende.
2. In `fondamenti-1` un `section` di pagina — non stratificato, quindi più forte
   di qualunque layer — ha iniziato a battere `.hero` del design system. La pagina
   ora ridichiara `.hero`, con il commento che spiega perché.
3. La variante copertina di `.sidebar-title` in `presentazione` dichiarava
   `font-variant: small-caps` ma non `text-transform`: prima non serviva, perché
   nessuna regola lo impostava; ora che una regola di base esiste, il maiuscolo
   filtrava. La variante dichiara esplicitamente `text-transform: none`.

**Un errore mio, registrato perché è istruttivo.** Per risolvere il caso 2 avevo
spostato nel design system anche `section` e `section:last-of-type` delle tre
pagine a sezioni nude. Sbagliato: `section:last-of-type` non significa «l'ultima
sezione della pagina» ma «l'ultima di ogni genitore», quindi toglieva un bordo
all'ultima sezione di **ogni** `.unit-block`. Undici pagine si sono accorciate.
L'harness l'ha mostrato al primo giro, la modifica è stata annullata e il caso 2
risolto in modo mirato. Generalizzare una regola perché tre file la condividono
non basta: bisogna guardare cosa seleziona davvero.

**Metodo della migrazione.** Uno strumento confronta ogni regola della pagina con
quelle del design system e la toglie **solo** se, a parità di contesto `@media`,
selettore e dichiarazioni coincidono — dopo aver risolto gli alias semantici
(`var(--colore-testo)` → `var(--inchiostro)`) e normalizzato i numeri (`.06em` e
`0.06em` sono lo stesso valore). Se qualcosa differisce, la regola resta: meglio
un duplicato che una differenza silenziosa. Lo strumento ha riconosciuto da solo
le differenze volute — le varianti copertina di `presentazione`, la testata
propria di `dietro-i-widget` — e le ha lasciate dov'erano.

**Verifica**: harness a **zero differenze su tutti e 65 i bersagli**, compresi i
due canvas di `meccanismo-4` e le pagine dell'ontologia. 793 link, nessuno rotto.
Nessun `:root` residuo nei capitoli, nessun riferimento a Google, un solo
`!important` in tutto il design system — quello del reset, che deve stare in un
layer proprio perché `!important` inverte l'ordine dei layer.

**Due varianti generate**, non una: `design-system.css` con i font via `url()`
relativi, per le pagine navigabili; `design-system.inline.css` con i font in
data-URI base64 (980 KB), per il bundle a file singolo, dove un percorso relativo
non significherebbe più niente. `build_css.py --check` fallisce se i generati non
corrispondono alle sorgenti.

## 2026-09-22 — Ontologia e Lente sulle fondamenta condivise, non sulla tipografia del saggio

Terzo passo del design system. La domanda non era «come faccio ereditare anche
all'ontologia il CSS del saggio» ma «che cosa condividono davvero».

L'ontologia è una **superficie di consultazione**, non di lettura continua: radice
a 16px contro i 19,2 del saggio, corpo 1.15rem, stack di font proprio (con
`Iowan Old Style` fra i ripieghi), colonna da 46rem invece di 740px, link color
inchiostro invece che arancio. La Lente semantica ha misure sue ancora diverse.
Farle ereditare la scala di lettura del saggio le avrebbe peggiorate in nome
dell'uniformità.

Condividono invece font, tavolozza e azzeramenti. Da qui una terza variante
generata, `design-system/css/fondamenta.css` (9 KB): solo i layer `reset` e
`tokens`, senza `base`, `layout` e `components` — quindi senza il
`html{font-size:120%}` che è proprio del saggio. Ontologia e Lente la collegano
**prima** del proprio CSS, che non essendo stratificato la sovrascrive dove serve.

- `pagina()` in `genera_html.py` è l'unico punto cambiato per tutte e 194 le
  pagine: una riga di `<link>` in più, calcolata sulla profondità come già faceva
  per `style.css`.
- `output/style.css` perde 28 righe (due `@font-face`, il `:root`, `box-sizing`),
  `lente.css` ne perde 47 (le stesse più le due scale categoriali).
- Le scale categoriali della Lente — `--cat-*` e `--grp-*`, 15 nomi — entrano nei
  token **fra i primitivi**, non fra i semantici: `lente.js` le legge per nome
  esattamente come gli altri primitivi, quindi valgono le stesse regole del
  contratto pubblico. Non sono state ridisegnate: erano già validate per contrasto
  e distinguibilità.
- **`ontologia/output/fonts/` eliminata**: 584 KB di font identici a quelli di
  `design-system/fonts/`. Nel repository resta una copia sola, più quella in
  `design-system/lab/`, che è archivio destinato a non essere pubblicato.

Verifica: harness a zero differenze; il diff delle 194 pagine rigenerate è
esattamente una riga per pagina; 1.869 link nell'ontologia, nessuno rotto; nessun
riferimento residuo alla cartella dei font rimossa.

## 2026-09-22 — Animazioni ferme sotto reduced-motion, e le schede dei componenti

**La lacuna di accessibilità, chiusa.** Tutte e 14 le pagine dichiaravano
`@media (prefers-reduced-motion: reduce)` ma ci mettevano dentro solo
`scroll-behavior: auto`. In `fondamenti-2` tre cursori continuavano a lampeggiare
(`animation: blink 1.2s infinite`) insieme a un bagliore e a due pulsazioni, anche
per chi aveva chiesto meno animazioni. L'ha trovata l'harness, non una lettura del
codice.

Il reset sta nel layer `reset` del design system e azzera **solo le animazioni**,
non le transizioni. Le transizioni non erano il problema — sono brevi e quasi tutte
di colore o opacità — e i componenti che avevano qualcosa da dire sotto
reduced-motion lo dicevano già: `.reveal` tiene la dissolvenza e toglie lo
spostamento, `.scrolldown` ferma la freccia. Un reset generalizzato avrebbe
cancellato quelle decisioni invece di rispettarle.

Durata quasi nulla e una sola iterazione, non `animation: none`: `none` farebbe
ricadere l'elemento sullo stile non animato, lasciando invisibile ciò che parte da
`opacity: 0` con `fill-mode: forwards`. Verificato prima di scegliere: nessuna delle
5 animazioni del repository usa `fill-mode`, ma la ricetta sicura vale comunque per
chi riuserà il sistema.

Misurato, non dedotto: con `prefers-reduced-motion: reduce` le animazioni in corso su
`fondamenti-2` passano da **46 a zero**; senza, restano 46. Zero differenze
nell'harness, perché lì le animazioni erano già congelate: il cambiamento riguarda
le persone, non gli screenshot.

Corretto anche un difetto dell'harness stesso: il censimento delle animazioni
infinite scriveva il proprio rapporto quando trovava qualcosa ma non lo cancellava
quando non trovava più nulla, quindi dopo la correzione continuava a segnalare un
problema risolto. Un rapporto che mente è peggio di nessun rapporto.

**Le schede dei componenti.** Otto anteprime autonome in `design-system/components/`,
ciascuna apribile nel browser così com'è e con il marcatore
`<!-- @dsCard group="…" -->` sulla prima riga, che è il modo in cui il pannello di
Claude Design costruisce il proprio indice (la registrazione esplicita via
`register_assets` è legacy). Raggruppate secondo la logica del progetto — Fondamenta,
Navigazione, Lettura, Ontologia — non secondo categorie generiche.

Le schede mostrano i componenti con **testo vero del saggio**, non riempitivo: una
scheda con testo finto non fa vedere se la tipografia regge. Verificate renderizzate,
non a lettura — e poi riviste una seconda volta su richiesta, il che ha fatto emergere
difetti che la prima passata non aveva visto:

- **La tavolozza si rompeva a larghezze diverse.** `--bianco` finiva orfano su una riga
  a sé, le etichette lunghe andavano a capo sfalsando le celle. Conta più di
  un'inezia: il pannello di Claude Design decide lui quanto è larga una scheda. Ora è
  una griglia adattiva, verificata a 860/720/560/430px con **zero nomi troncati** —
  su una scheda della tavolozza il nome del token è l'informazione principale, e
  troncarlo sarebbe stato peggio del difetto di partenza.
- **I due quasi-bianchi erano invisibili**: `--bianco` su fondo bianco e `--brina` su
  fondo brina. Il primo ora si legge su una scacchiera, il secondo perché la scheda
  sta su superficie.
- **L'hero occupava una scheda intera per tre righe.** Ora mostra anche la variante
  copertina di `presentazione`, che era una decisione reale del sistema mai
  documentata.
- **Mancavano gli stati interattivi.** `:hover` e `:focus-visible` sono parte del
  componente quanto il colore a riposo. Non si forzano in uno screenshot, ma la scheda
  è una pagina vera: ci si può passare sopra e tabularci dentro. Così diventa visibile
  una scelta deliberata prima sepolta nel CSS — il fuoco da tastiera ha lo stesso
  trattamento del mouse, non un anello di ripiego.

La tenda dei concetti è **markup come documentazione**, non una seconda
implementazione: il JavaScript resta uno solo, nelle pagine.

**Il README riscritto.** Da prosa che descriveva regole a porta d'ingresso di un
sistema: come si collega, come è fatto, il contratto pubblico, i principi con il loro
perché, le due tabelle (tavolozza e scala), l'indice delle schede, e come si cambia
qualcosa — editare la sorgente, rigenerare, far girare l'harness. Quest'ultimo punto
non è una formalità: è il motivo per cui 3.300 righe di CSS ricopiato sono sparite
senza che cambiasse un pixel.

## 2026-09-23 — Export DTCG, controllo del contrasto, contratto dei nomi — e un fallimento WCAG trovato

Tre script che rendono verificabile ciò che finora era affermato.

**`check_public_names.py`** — il contratto fra token e JavaScript. Distingue tre modi
d'uso con conseguenze diverse: nomi **letti** via `getComputedStyle` (2, in
`meccanismo-4`), nomi **interpolati** come `var()` dentro stringhe che generano SVG
(20, fra `lente.js` e quattro capitoli), nomi **scritti** dal JavaScript (1,
`--colore-gruppo`, che infatti non deve stare nei token). Controlla anche che chi
viene passato a una funzione che lo interpreta come esadecimale abbia davvero un
valore esadecimale: un `rgba()` lì produrrebbe NaN senza dirlo.

Messo alla prova rompendo il contratto di proposito — prima rinominando un primitivo
letto dal JS, poi dandogli un valore non esadecimale: in entrambi i casi esce con 1 e
dice cosa si è rotto e dove. Uno strumento che non ha mai fallito non è dimostrato
funzionante.

**`export_tokens.py`** — genera `tokens/tokens.json` in formato W3C DTCG 2025.10: 66
token, gruppi che dichiarano `$type` una volta sola, colori come
`{colorSpace, components, alpha, hex}`, alias veri (`{primitivo.colore.neutro.brina}`)
e non valori copiati. `--check` fallisce se il JSON va in deriva rispetto al CSS.
Un caso limite dichiarato invece che nascosto: `.06em` non è rappresentabile come
`dimension` nella spec (ammette solo unità assolute), quindi è reso come `number` con
la spiegazione dentro il token stesso.

Scritto da un'implementazione indipendente, di proposito: chi ha disegnato i token
non vede ciò che dà per scontato. Ha fatto emergere due cose vere. **I trittici
`blu-scuro/blu/blu-chiaro` non condividono una regola di prefisso** con i neutri né
con `cat-*`/`grp-*`: non esiste un algoritmo solo che derivi il gruppo dal nome, e
l'appartenenza va dichiarata in una tabella. Scrivendo il CSS a mano una volta sola,
quel problema non si incontra mai. E **`--line` è l'unico primitivo con
trasparenza**: funziona, ma è l'unica voce in cui «il colore vero» include un'alfa.

**`check_contrast.py`** — e qui il risultato che conta. `--grigio-soft` (`#8A8580`)
**non passava WCAG AA**: 3,43:1 su brina e 3,65:1 su bianco, contro i 4,5:1 richiesti.
Non un colore marginale: è il ruolo «testo tenue», e regge occhielli, kicker della
sidebar, note di chiusura, etichette delle note a margine, intestazioni della tenda —
tutto testo fra 13,8 e 16,5px, quindi la soglia dei 3:1 riservata al testo grande non
si applica. Non c'era lettura in cui passasse.

Il calcolo è stato validato contro i due valori già registrati in questo log prima di
dichiarare il difetto: verde su bianco 5,19:1 (qui era annotato ≈5,2) e verde-scuro
8,54:1 (≈8,5). Combaciano, quindi il difetto era del design system, non della formula.
Ricalcolato poi una seconda volta, in modo indipendente: 3,43 e 3,65 al centesimo.

**Deciso: `--grigio-soft` diventa `#6F6B67`** — 4,97:1 e 5,28:1, con margine invece
che al pelo. Stessa tinta calda, otto punti di luminosità in meno. L'apparato resta
più chiaro del testo attenuato (8,91:1), quindi la gerarchia regge: è solo meno
estrema di prima.

Verificato che il cambiamento sia **solo** quello: confronto degli stili calcolati su
quattro superfici (un capitolo, la presentazione, la home dell'ontologia, la Lente) —
l'unica proprietà che cambia è quel colore, su 286, 246, 29 e 1.007 elementi. Nessuno
spostamento, nessun cambio di misura. Baseline dell'harness rifatta su questo stato.

## 2026-09-23 — Correzione: IBM Plex Mono non contiene ∧ ∨ ⊕, e il mio metodo non poteva accorgersene

La voce del 22 settembre affermava che i file dei font appena self-hostati contenessero
tutti e 17 i glifi non latini usati nel saggio, e che questo **riparasse** il difetto dei
tre simboli logici non coperti dai subset di Google. **È falso.**

Verificato leggendo la `cmap` dentro i file con fontTools — nessun rendering di mezzo:

| file | codepoint | ∧ U+2227 | ∨ U+2228 | ⊕ U+2295 | ¬ U+00AC |
|---|---|---|---|---|---|
| IBMPlexMono-{Regular,Medium,SemiBold} | 1082 | assente | assente | assente | presente |
| EBGaramond-{Variable,Italic} | 2091 / 1972 | assente | assente | assente | presente |

Quindi in Fondamenti · 1 solo `¬` viene da IBM Plex Mono; `∧ ∨ ⊕` ripiegano su un font di
sistema — `⊕` su qualcosa che rende come Courier New, gli altri due su un font che non
corrisponde a nessuno dei candidati provati. Uno su quattro, non quattro su quattro.

**Perché il mio test diceva il contrario.** Rendevo ogni glifo con il font locale e poi
con `monospace`, e concludevo «presente» se i pixel differivano. Ma quando un font non ha
un glifo il browser ripiega **per singolo glifo** su un font di sistema, che non è quello
a cui risolve `monospace`: i pixel differivano comunque. Quel test poteva rilevare solo i
quadratini `.notdef`, non il ripiego — era strutturalmente incapace di rispondere alla
domanda che gli ponevo, e l'ho dichiarato conclusivo.

È la **seconda volta nella stessa giornata** che sbaglio allo stesso modo: poche ore prima
avevo già scambiato «diverso dal monospace generico» per «presente nel font», me ne ero
accorto, l'avevo messo a verbale — e poi ho rifatto lo stesso errore in una forma diversa,
su file locali invece che su subset remoti. La lezione che avevo scritto («la prova non sta
nel rendering ma nella dichiarazione») era giusta e non l'ho applicata: la dichiarazione,
per un file locale, è la sua `cmap`, e leggerla costava una riga di fontTools — che era già
installato nel venv dell'ontologia da settembre.

L'errore l'ha trovato un agente a cui avevo chiesto di verificare i quattro simboli come
parte della fase sul bundle. Ha fatto la cosa giusta: ha misurato invece di fidarsi della
documentazione del repository, e ha dichiarato che la contraddiceva.

**Corretto** in `design-system/fonts/fonts.css`, `design-system/README.md`,
`docs/snapshot.md`, `docs/next-steps.md`, e nella voce del 22 settembre, che porta ora la
correzione sul posto invece di essere riscritta. I due messaggi di commit che contengono
l'affermazione falsa (`2425758`, `152a528`) restano come sono: la storia non si riscrive
per un errore che una voce successiva può correggere.

**Cosa resta vero della voce del 22 settembre**: i font sono self-hostati in una copia
sola, la dipendenza da Google è eliminata, e la resa del monospaziato è ora uniforme su
tutte e 14 le pagine — 9 non lo caricavano affatto. Cambia solo la parte sui tre simboli.

**Decisione aperta**, in `next-steps.md`: un font di ripiego che li contenga, disegnarli
come SVG, o accettare il ripiego dichiarandolo. Visivamente reggono.

## 2026-09-23 — Il bundle a file singolo, rifatto

`build_output.py` non girava più: la migrazione al design system aveva tolto il `<style>`
a `genealogia-4-corpo.html` — era il capitolo più puro, tutto il suo CSS era guscio
condiviso — e lo script pretendeva che ogni capitolo ne avesse uno. Giusto che si sia
rotto: quell'assunzione non valeva più.

Ma il bundle era indietro di più: il suo tema chiaro definiva variabili (`--bg`,
`--surface`, `--copper`) che **nessun capitolo legge più**; il bottone «Tema: scuro» era
in pagina e non faceva niente; l'introduzione e il Sommario erano stilati con quelle
variabili inesistenti e con due font (Space Grotesk, Source Serif 4) che il saggio non usa
da settembre; e i quattordici paragrafi d'introduzione, ricopiati a mano nello script,
annunciavano la Lente semantica come «in preparazione» — esiste da settembre.

**Due decisioni prese**: `presentazione.html` e `dietro-i-widget.html` diventano capitoli
veri, trattati dallo stesso estrattore degli altri. Il bundle torna a essere **un file
solo** (prima erano due) e la sua introduzione è la presentazione reale, per sempre, senza
prosa duplicata.

**Tre cose emerse durante l'esecuzione, che non erano nell'inventario:**

1. **Il CSS dei capitoli andava scopato.** Finché ogni pagina ricopiava l'intero guscio, i
   selettori duplicati erano identici e concatenarli era innocuo. Ora che resta solo il CSS
   dei widget, `.switch` è 84×42 in Fondamenti 1 e 90×44 in Fondamenti 2, e `.truth-table`,
   `.tl-*`, `.hero` hanno valori diversi: concatenati, vinceva l'ultimo capitolo per tutti.
   Era un danno **preesistente e invisibile**, che la migrazione ha solo reso percepibile.
   Ogni selettore diventa ora discendente di `#chapter-<slug>`.
2. **La tenda dei concetti si apriva in tutti i capitoli insieme.** Il suo listener è
   delegato su `document` e ogni capitolo ne registra uno: cliccare un termine nella
   Presentazione apriva anche la tenda di Meccanismo · 3, invisibile finché quel capitolo
   era nascosto — ma navigandoci ci si arrivava con la tenda aperta e il velo sopra la
   pagina. Riprodotto e corretto.
3. **Due rimandi da capitolo a capitolo** puntavano a file che accanto al bundle non
   esistono, e il percorso verso la Lente semantica era rotto nel compilato (un livello di
   profondità in meno rispetto ai sorgenti) — in tutti e 14 i file, da prima.

**Verifica**, misurata e non riferita: zero richieste a host esterni; zero errori in
console su tutti e 14 i capitoli; nessun capitolo vuoto; 13 capitoli su 14 con altezza
identica alla propria pagina sorgente (il quattordicesimo è l'introduzione, più alta
esattamente dell'altezza del Sommario); **816 proprietà di stile calcolato confrontate fra
bundle e sorgenti su quattro capitoli, zero differenze**. Funziona anche aperto da
`file://`, che è il ritorno sull'investimento dei font in data-URI.

Dimensione: da 721.587 byte in due file a **1.879.717 in uno**, di cui 979.783 i font in
base64 e 132.392 le immagini incorporate.

**Un residuo voluto**: `<html data-theme="light">` resta. Non è il tema morto — è la stessa
dichiarazione che `meccanismo-4-reti-neurali.html` porta sul proprio `<html>`, e che il suo
`currentLossPalette()` legge per scegliere la tavolozza dello shader. Senza, la superficie
di perdita sarebbe disegnata in variante scura su pagina chiara.

## 2026-09-23 — Il monospaziato sostituito, e l'harness che guardava un terzo di pagina

**Noto Sans Mono al posto di IBM Plex Mono.** Accertato ieri che Plex non contiene
`∧ ∨ ⊕`, si è cercato un monospaziato con licenza aperta che li avesse. Provati
otto candidati scaricando da ciascuno un sottoinsieme di un paio di KB e
leggendone la `cmap`: **Noto Sans Mono è l'unico che li contiene tutti e tre**
(JetBrains Mono ha ∧ ∨ ma non ⊕; Inconsolata solo ⊕; Fira Mono, Source Code Pro,
Roboto Mono, Space Mono e Plex nessuno).

Il file completo è un variabile da 1,67 MB. Ridotto ai 133 caratteri che il saggio
usa davvero — ASCII, accenti italiani, simboli tecnici — pesa **10,0 KB**, contro
i 146,7 KB dei tre file di Plex, di cui **due non venivano mai caricati**:
verificato sul bundle compilato con tutti e 14 i capitoli, il browser chiede solo
il peso 400.

La riduzione è riproducibile: `design-system/scripts/subset_font.py` la rigenera
dal sorgente, e **fallisce** se il font non contiene i quattro simboli o se il
sottoinsieme ne perde uno. L'ha fatto subito, al primo giro: `␣` (U+2423) era
nell'elenco ma Noto Sans Mono non ce l'ha. Verificato che non serve — l'unico uso
nel saggio è in `.pg-chip .glyph::before` di Meccanismo · 1, che è in **serif**,
non in monospaziato. (Anche EB Garamond non lo contiene: quel glifo ripiega da
sempre, cosa diversa e preesistente.)

Il monospaziato ha **due** usi reali, non uno come diceva il README: i quattro
simboli logici, e i valori tecnici che cambiano dal vivo in Meccanismo · 4 e 6.
Corretto anche quello.

**E poi la scoperta che conta di più.** Cambiato il font, l'harness ha dichiarato
zero differenze. Impossibile: i simboli erano appena cambiati di carattere.
Cercandoli per colore dentro le immagini, si è visto che **non c'erano affatto**,
né prima né dopo.

Il saggio avvolge quasi tutto il contenuto in blocchi `.reveal`, a `opacity: 0`
finché un `IntersectionObserver` non li incontra. `cattura.js` non scorreva la
pagina, quindi l'osservatore non scattava mai. Misurato: **il 64% dell'altezza
complessiva delle 14 pagine stava dentro `.reveal` mai resi visibili.** Il
confronto a pixel — con cui ho certificato la migrazione al design system —
guardava circa un terzo del contenuto.

Cosa non era compromesso, perché va detto con la stessa precisione: i confronti di
**stile calcolato** (816 proprietà su quattro capitoli) leggono i valori a
prescindere dall'opacità; i confronti di **altezza** sono validi perché un
elemento a opacità zero occupa comunque il suo spazio; link, rete e token non
c'entrano. Era cieco il solo confronto a pixel — che però era il cuore della
verifica.

**Corretto e ri-verificato.** L'harness ora scorre l'intera pagina e porta i
`.reveal` allo stato finale per dichiarazione. Poi, per rispondere alla domanda
vera — *la migrazione ha cambiato qualcosa in quel 64%?* — sono stati estratti
dalla storia lo stato prima (`ef918c0`) e dopo (`d2fba43`) la migrazione, resi
entrambi con la cattura corretta e confrontati: **26 confronti su 28 identici**.
I due con differenze mostrano esattamente i valori bistabili già catalogati.
La migrazione regge anche su ciò che non era mai stato guardato.

Rivelare il contenuto ha fatto emergere, in tre pagine dense di widget, una
instabilità di rasterizzazione su bordi e maiuscoletto: non deriva ma
**bistabilità**, con gli stessi valori esatti che ricorrono (240, 183, 133, 73) e
due varianti indistinguibili a occhio. Soglie per bersaglio fissate a 300, sopra
il massimo misurato di 240, con la ragione scritta accanto.

**La lezione, che è la terza dello stesso genere in due giorni**: uno strumento di
verifica va verificato come il codice che verifica. Questo harness ha superato un
cancello di determinismo severo — quattro catture, sei confronti, zero differenze
— e quel cancello era soddisfatto *anche* fotografando pagine vuote. Misurava con
precisione la cosa sbagliata. A trovarlo non è stata una revisione del codice: è
stato un cambiamento che *doveva* produrre una differenza e non l'ha prodotta.

## 2026-09-23 — L'asserzione di copertura: la lezione messa dove non si può dimenticare

Alla domanda «dove vanno salvate queste lezioni», la risposta scelta non è
*dove* ma *quando devono arrivare*. La lezione sui font («la prova non sta nel
rendering, sta nella dichiarazione») era **già scritta** in questo decision-log,
ed è stata violata poche ore dopo: una riga letta all'avvio non ferma nessuno nel
momento in cui conta. Quindi la regola diventa: **ciò che può fallire da solo non
si scrive, si esegue.**

Per i font la forma eseguibile esisteva già — `subset_font.py` si rifiuta di
costruire senza `∧ ∨ ¬ ⊕`, e ha sparato al primo giro. Per l'harness non
esisteva: `rivelaTutto` corregge la causa del 64% non fotografato, ma niente
impediva all'errore di tornare sotto altra forma. Ora `cattura.js` misura prima
di ogni scatto **quanta parte dell'altezza del documento dipinge qualcosa**, e
sotto al 97% fallisce cancellando la cartella di uscita: non si tiene una
baseline che certifica il vuoto. Dettagli e numeri in `design-system/verify/README.md`,
sezione «Copertura».

**La prima versione dell'asserzione misurava la cosa sbagliata** — e questa volta
è emersa in venti minuti invece che in giorni, perché ho guardato *quali*
elementi venivano contati invece del numero che ne usciva. Contava anche i
`position: fixed`: gli unici elementi invisibili di rilievo erano i due velari
`tenda-scrim` e `lightbox-scrim`, 900px di viewport su ogni pagina, che non
contribuiscono a `scrollHeight` e quindi non possono lasciare altezza non
dipinta. Due bersagli fallivano per una ragione che non c'entrava col contenuto.
Corretto: gli elementi fuori flusso non entrano nel conto.

**Provata rompendo apposta ciò che sorveglia**, che è l'unica prova che valga per
uno strumento di verifica: ricreando il bug originale (niente scorrimento, niente
congelamento dei `.reveal`) la copertura crolla a **28,0%** e il giro fallisce;
rendendo invisibile **una sola sezione** scende a **84,0%** e fallisce lo stesso.
È il secondo caso che giustifica la soglia: il disastro si vedrebbe comunque, la
sparizione di una sezione no. Valori reali dopo la correzione: minima 99,4% (la
Lente), mediana 100% su 63 scatti.

Resta fuori dall'eseguibile il nucleo che nessuno script cattura — *un cancello
soddisfatto anche dal vuoto non è un cancello* — e che vale per qualunque
progetto, non per questo: va in `memoria/` come feedback, non qui. Qui resta il
*perché* di questo repository.

## 2026-09-23 — Il bundle che non tornava in cima, e una regola CSS che vinceva sul JavaScript

Segnalato dall'utente: cliccando un capitolo nel Sommario del file compilato,
«la pagina fa degli scatti strani». Misurato invece che dedotto, campionando
`scrollY` a ogni fotogramma in Chrome vero: partendo da 3000px si finiva a
**2998**. Il capitolo cambiava, ma la pagina **non tornava affatto in cima** —
si restava in mezzo al capitolo nuovo, con due pixel di sobbalzo.

**Causa.** Il design system dichiara `html{ scroll-behavior: smooth }`. Con
quella regola attiva, ogni `scrollTo`/`scrollBy` programmatico che non dica
esplicitamente il contrario diventa un'**animazione**, e ogni nuova chiamata
*annulla* quella in corso ricalcolando il bersaglio dalla posizione del momento.
`showChapter` chiedeva `scrollTo({top: 0})` e subito dopo `nudgeIntersectionObservers()`
faceva `scrollBy(0, 1)` e `scrollBy(0, -1)`: il viaggio verso lo zero veniva
cancellato un fotogramma dopo essere partito, ripuntando a «dove sono adesso
meno uno». Ripetuto tre volte (subito, al fotogramma dopo, a 60ms). Una regola
CSS che vince silenziosamente su quello che il JavaScript crede di fare.

**Il primo rimedio non funzionava, e si è visto solo misurando.** Portare
`html.style.scrollBehavior = 'auto'` prima della chiamata non basta: il motore
risolve il `behavior: auto` leggendo lo stile calcolato **ancora vecchio**.
Provate quattro varianti sulla pagina viva, guardando `scrollY` subito dopo la
chiamata (se e' gia' a destinazione lo spostamento e' stato istantaneo):

| Variante | `scrollY` subito dopo |
|---|---|
| stile inline `auto`, nessun reflow | 2000 — animato |
| stile inline `auto` + reflow forzato (`void html.offsetHeight`) | **0** — istantaneo |
| `behavior: 'instant'` | **0** — istantaneo |
| stile inline, ripristino differito di un fotogramma | 2000 — animato |

Scelto il reflow forzato invece di `behavior: 'instant'` perche' quel valore
dell'enum e' arrivato tardi in alcuni browser e una stringa non riconosciuta
solleva un'eccezione invece di degradare.

**Seconda correzione, conseguente.** Il rimando dentro il testo faceva
`scrollIntoView({behavior:'smooth'})` un fotogramma dopo `showChapter`: ora che i
nudge sono istantanei, sarebbe stato il nudge delle 60ms ad annullare *lui*.
`showChapter` prende quindi un secondo argomento, eseguito quando l'ultimo nudge
è passato.

**Verificato dopo**: Sommario 3000 → **0**, due soli cambi di `scrollY`, nessuna
inversione. Sidebar: salto istantaneo a 0, poi **una sola** animazione che
atterra esattamente su 744, che è la posizione reale di `#intro-parte-1`.
Controllato anche che i `.reveal` continuino a rivelarsi nel capitolo appena
mostrato — è il motivo per cui il nudge esiste: 6/6 e 23/23 dopo uno scorrimento
completo. A `scrollY` 0 ne risultano zero visibili, ed è corretto: a quell'altezza
nessun `.reveal` è ancora nel viewport.

## 2026-09-23 — La Lente semantica entra nel compilato, perché Safari aveva ragione

Segnalato dall'utente: nel file compilato «la lente semantica si apre su Chrome
ma non su altri browser». Misurato invece che supposto, contando gli
`href`/`src` del file: su 74 collegamenti, **uno solo usciva dal file** —
`../../ontologia/lente-semantica/output/index.html`, più le tredici copie della
stessa riga che il JavaScript della tenda dei concetti assegna a runtime. Tutto
il resto era già interno o `data:`.

~~Quel percorso risale due cartelle, e Safari rifiuta di seguire un
collegamento locale che esce dalla cartella del documento.~~ **Meccanismo
descritto male, corretto il 24 settembre** (vedi la voce «Non era il file, era
come lo si apriva»): Safari è sandboxed e riceve l'accesso **per singolo file**,
quello che gli consegna il sistema. Qualunque altro file locale gli è negato,
a qualunque profondità: il clic non fa nulla, senza errore visibile. Chrome
quella restrizione non ce l'ha, ed è l'unica ragione per cui funzionava.
Confermato dall'utente: «non succede niente». La regola corretta rende la
decisione più solida, non meno: non basta accorciare il percorso, serve che di
file ce ne sia **uno**.

**Decisione presa dall'utente**: la Lente diventa un capitolo del compilato,
come presentazione e dietro-i-widget. Un deliverable «un file solo» non può
dipendere dall'albero che gli sta intorno — e la prova che non ci dipende non è
un'intenzione, è un controllo: `build_output.py` ora **fallisce** se nel file
scritto resta un solo `href`/`src` che non sia `#` o `data:`.

**Tre fatti misurati prima di scrivere una riga di codice**, perché ciascuno
poteva rendere la cosa impraticabile:
- i nove id della Lente (`svg-grafo`, `ricerca`, `lista-nodi`…) **non collidono**
  con nessun id del compilato → non serve prefissarli, e `lente.js`, che li
  cerca per nome, resta intatto;
- `lente.js` **non misura mai il layout reale** (nessun `getBoundingClientRect`,
  nessun `clientWidth`: il grafo è disegnato in coordinate `viewBox`) → può
  inizializzarsi mentre il capitolo è ancora `hidden`, che è la sua condizione
  al caricamento;
- delle diciotto classi della Lente **una sola** è in comune col resto.

**Due cose sole cambiano in `lente.js`**, dietro un `window.LENTE_INCORPORATA`
che il guscio dichiara: non scrive più il nodo scelto in `location.hash` (nel
compilato l'hash appartiene alla navigazione fra capitoli: ogni clic sul grafo
avrebbe cambiato capitolo) e non ascolta `hashchange`. In più espone
`window.lenteSeleziona`, unico punto d'ingresso dall'esterno.

**Il layout è stato corretto guardandolo, non prevedendolo.** Alla prima resa la
Lente era coperta dal binario del saggio e l'elenco dei nodi appariva senza
etichette, una colonna di soli numeri. Due cause, entrambe da `layout.css`:
`main{ padding-left: var(--misura-rail) }` sopra i 900px non toccava la Lente
(che non ha un `<main>` che avvolga tutta la pagina, quindi partiva sotto il
binario) e toccava invece il suo `<main class="pannello-grafo">` interno,
spostando il riquadro del grafo dentro un contenitore che non si era allargato.
Corretto **dentro il capitolo**, senza toccare `layout.css`: la regola è giusta
per il saggio.

**Differenza dichiarata, non nascosta**: nel compilato la Lente riceve tutto il
design system, mentre la pagina a sé carica le sole `fondamenta.css` — è la
decisione dell'8 settembre, «Lente sulle fondamenta, non sulla tipografia del
saggio». Dentro il saggio quella decisione si rovescia, e a ragione: tutto
risulta il 20% più grande (`html{ font-size: 120% }`) e `.apparato` passa da
13,12px a 19,2px perché la regola del design system vince su quella locale. Le
due rese ora divergono di proposito. Se un domani si volesse riallinearle, il
punto è questo paragrafo.

**Verificato da `file://`**, che è il modo in cui il file viene davvero aperto:
15 capitoli, grafo disegnato anche da nascosto (37 elementi), voce nella sidebar
che mostra il capitolo con 258 nodi in elenco, tenda di un concetto →
«Apri nella Lente semantica» che centra esattamente il nodo chiesto
(`SpazioSemanticoEEmbedding`), tenda chiusa dietro di sé, hash intatto, un clic
nel grafo che non cambia capitolo. Zero errori JavaScript, zero richieste di
rete. Il file passa da 1,69 a **2,09 MB** (+23%): 280 KB sono D3.

~~**Coda**: rieseguito l'harness dopo la modifica a `lente.js`, un bersaglio in
più è risultato fallito — Genealogia · 3 a viewport stretto, 108 pixel con delta
13. È bistabilità di rasterizzazione, dimostrata con tre catture dello stesso
codice immutato. Decima deroga per bersaglio.~~ **Falso, corretto poche ore dopo
dalla voce «L'osservatore che disturba» qui sotto: quei 108 pixel li produceva il
mio stesso strumento di misura. La deroga è stata ritirata.**

## 2026-09-23 — L'osservatore che disturba: la sentinella di copertura cambiava la fotografia

Poche ore dopo aver aggiunto l'asserzione di copertura, l'harness ha cominciato a
segnalare fallimenti che si spostavano da una corsa all'altra — prima uno, poi
quattro, poi tre, tutti a viewport stretto — con il rumore assorbito a **133.747
e 173.744 pixel** contro i 1.182 di una corsa sana. Centoquaranta volte tanto.

Le due spiegazioni comode erano a portata di mano, e tutte e due sbagliate: il
carico della macchina (una corsa era durata 861 secondi invece di 187) e la
bistabilità di rasterizzazione già catalogata. La prima è caduta perché la corsa
successiva è durata 185 secondi e ha fallito lo stesso. La seconda è caduta su un
dettaglio che non tornava: **Genealogia · 4 dava numeri identici in due corse
diverse** — 12 percettibili, 65.978 di rumore, delta massimo 9. Un numero che si
ripete uguale non è casuale.

Le differenze stavano in fondo alle pagine, a tutta larghezza, dove la `.chiusura`
posa una sfumatura — e una sfumatura ditherizza, cioè basta pochissimo perché la
stessa sfumatura venga resa in modo leggermente diverso. E la baseline era delle
14:56, cioè di **prima** che aggiungessi la misura di copertura.

`misuraCopertura` attraversa tutto il DOM chiamando `getComputedStyle` e
`getBoundingClientRect`, e girava **subito prima dello scatto**: forza un
ricalcolo di stile e impaginazione, e quel ricalcolo cambia come Chrome
rasterizza. **Provato disattivando soltanto quella chiamata**: zero pixel di
differenza dalla baseline. Riattivandola: 65.990.

Spostata dopo lo scatto. Non è una misura meno vera — fra la fotografia e la
misura non succede nulla che cambi la pagina, uno screenshot non muta il DOM — ma
non può più influenzarla. Riverificato: corsa completa a **zero fallimenti su 65
confronti**, rumore assorbito 878 pixel, e le due prove di rottura falliscono
ancora con gli stessi valori di prima (28,0% ricreando il bug originale, 84,0%
nascondendo una sola sezione). La sentinella morde ancora e non disturba più.

**Due conseguenze, e la seconda è la più scomoda.**

La prima: la decima deroga aggiunta poche ore prima è stata **ritirata**. Le tre
catture con cui avevo «dimostrato» la bistabilità di Genealogia · 3 giravano
tutte con lo strumento difettoso: la prova era viziata alla radice, e il numero
ricorrente che mi aveva convinto era la perturbazione, che è deterministica.
Oggi quel bersaglio è a zero differenze. Una deroga che documenta un fenomeno
inesistente è peggio di nessuna deroga — un giorno nasconderebbe qualcosa di vero.

La seconda: è la quarta volta in due giorni che sbaglio nella stessa direzione, e
questa volta in un modo che la lezione precedente non copriva. Avevo verificato
che lo strumento **funzionasse**, rompendo apposta ciò che sorveglia. Non avevo
verificato che **non disturbasse**. Sono due proprietà diverse: la prima si prova
introducendo un guasto e pretendendo il fallimento, la seconda si prova togliendo
lo strumento e pretendendo che non cambi nulla. Un osservatore che altera ciò che
osserva misura se stesso.

## 2026-09-24 — Non era il file, era come lo si apriva

Segnalato: «l'output si apre solo in Chrome, non su Safari». Questa volta la
verifica è stata fatta nel motore giusto invece che per analogia. macOS include
WebKit — lo stesso motore di Safari — utilizzabile da riga di comando: scritta
una sonda di quaranta righe in Swift che carica il file in una `WKWebView`,
intercetta `window.onerror`, `unhandledrejection`, `console.error/warn`, e a
caricamento finito interroga il DOM.

**Il compilato in WebKit funziona**: 15 capitoli, capitolo iniziale visibile,
16.267 caratteri di testo, sidebar presente, `showChapter` e `lenteSeleziona`
definite, 3 font caricati, **zero errori e zero avvisi**. Ripetuto concedendo
l'accesso in lettura al **solo file** e a nessuna cartella: identico. Permessi
lungo tutto il percorso normali, nessuna ACL, nessuna quarantena, nessun flag.

Restava una variabile sola, ed è quella giusta: **come Safari arriva al file**.
Safari è sandboxed e riceve l'accesso a un file locale solo se glielo consegna
il sistema — pannello di apertura, doppio clic, `open`. Un percorso incollato
nella barra degli indirizzi non gli è stato consegnato da nessuno, e viene
rifiutato. Verificato dall'utente: **con ⌘O il file si apre benissimo.**

**Il compilato non aveva alcun difetto.** Ed è la seconda volta in due giorni
che una spiegazione plausibile e sbagliata sopravvive perché non la si prova nel
posto giusto: avevo attribuito il primo sintomo a una regola di Safari sulle
cartelle superiori, che non esiste. La regola è per file.

**La correzione precedente resta però giusta, e per una ragione più forte.** Se
l'accesso è per file, allora *qualunque* riferimento esterno sarebbe fallito in
Safari, a qualunque profondità: non bastava accorciare il percorso, serviva che
di file ce ne fosse **uno**. La Lente come capitolo e il controllo che fa
fallire la compilazione su qualsiasi `href`/`src` esterno sono la risposta
corretta a un meccanismo che avevo descritto male. Il meccanismo è stato
corretto sul posto in `build_output.py` e nella voce del 23 settembre.

**Nota operativa per la pubblicazione**: il file va aperto con un doppio clic,
con ⌘O o con `open` — tutte vie che passano da LaunchServices, che è ciò che
concede l'accesso. Incollare il percorso nella barra degli indirizzi di Safari
non funziona, e non è un difetto del file. Servito via http la questione non si
pone affatto.

**Nota di metodo**: la sonda WebKit in Swift costa quaranta righe e non richiede
di installare niente, perché il motore è già nel sistema. Vale la pena ricordarsela
la prossima volta che un difetto è «solo su Safari»: si può guardare, invece di
dedurre da Chrome.

**Verificato anche in WebKit** (24 settembre): esercitato il compilato dentro la
sonda, con l'accesso al solo file. Navigazione fra capitoli dal Sommario: da
2000px a **0 in 120 millisecondi**. Voce di sidebar con ancora: atterra a 736,
che è la posizione esatta del bersaglio. Lente come capitolo: 17 nodi, 258 voci
in elenco, secondo grado che porta a 68 nodi; tenda di un concetto che centra
`SpazioSemanticoEEmbedding` e si chiude dietro di sé. Font: EB Garamond e Noto
Sans Mono, entrambi dai data-URI. Zero errori, hash mai toccato.

Nel farlo ho lanciato due volte un falso allarme sullo scorrimento, per lo stesso
motivo tecnico in entrambi i casi: lo scorrimento di *preparazione* della prova
(`window.scrollTo(0, 2000)`) è a sua volta soggetto a `scroll-behavior: smooth`,
quindi era ancora in volo quando misuravo, e il suo arrivo tardivo sembrava un
mancato ritorno in cima. Rifatta la preparazione con `behavior: 'instant'`, il
difetto è sparito perché non c'era. **Lezione minuta ma ricorrente**: quando si
misura un comportamento di scorrimento, anche il gesto che prepara la misura è un
comportamento di scorrimento, e va reso deterministico per primo.

## 2026-09-24 — Le sotto-sezioni si raggiungono direttamente, non ripartendo dal capitolo

Segnalato: cliccando nel binario una sotto-sezione, «il click fa ripartire dalla
prima parte del capitolo e poi scorre fino alla quarta». Difetto reale, e
**l'avevo già misurato il giorno prima senza riconoscerlo**: nella verifica
dello scorrimento leggevo `3000 → 0 → 744` e l'avevo archiviato come corretto
perché atterrava sul bersaglio giusto. Il numero giusto alla fine di un percorso
sbagliato.

**La causa è concettuale, non tecnica**: avevo trattato come un gesto solo due
gesti diversi. Cambiare capitolo **senza** bersaglio (Sommario, titolo di
capitolo) deve portare in cima, e lì tornare a 0 è giusto. Cambiare capitolo
**con** un bersaglio deve portare lì e basta. Il viaggio intermedio non aggiunge
orientamento: lo toglie, perché mostra un punto di partenza che non è né dove
eri né dove vai.

`showChapter` prende ora un oggetto di opzioni invece di una sola funzione:
`bersaglio` è l'id su cui atterrare, `poi` la funzione da eseguire a capitolo
visibile (oggi solo la selezione del nodo nella Lente). Con un bersaglio si va
direttamente alla sua posizione, senza animazione; senza bersaglio si torna in
cima come prima. Vale anche per le sotto-sezioni del capitolo in cui si è già,
che soffrivano dello stesso difetto ed erano il caso più fastidioso.

**Un secondo difetto trovato dalla verifica, non dalla segnalazione**: passando
a un capitolo senza unità (Fondamenti, per esempio), il pallino dello scroll-spy
restava acceso su un'unità del capitolo *precedente*. `updateActive` lascia
deliberatamente acceso l'ultimo pallino quando non trova un bersaglio in vista —
comportamento giusto mentre si scorre fra due unità, sbagliato dopo un cambio di
capitolo. Spento ora in `updateSidebarState`, cioè al cambio di capitolo e non a
ogni scorrimento; chi riaccende quello giusto è `updateActive`, che parte subito
dopo su `corso:chapterchange`.

**Misurato in Chrome e in WebKit**, campionando `scrollY` a ogni fotogramma:

| caso | Chrome | WebKit |
|---|---|---|
| 4ª sotto-sezione da un altro capitolo | 2500 → 9693, atteso 9693 | 2500 → 9638, atteso 9638 |
| 4ª sotto-sezione del capitolo in cui si è | 2500 → 9693 | 2500 → 9638 |
| voce di capitolo senza ancora | 2500 → 0 | 2500 → 0 |

Nessuna posizione intermedia in nessuno dei casi, pallino giusto in tutti, e
`null` invece di un pallino ereditato sul capitolo senza unità. Controllato anche
che lo scroll-spy continui a seguire lo scorrimento normale: 6 unità su 6.

**Nota**: la prima verifica di questa correzione usava la prima sotto-sezione,
che sta a y=0 — indistinguibile dall'andare in cima. Una prova che non può
fallire non è una prova; rifatta con la quarta.

## 2026-09-25 — La nona scheda: uno specimen che dichiara invece di mostrare soltanto

Domanda dell'utente: perché nel design system non c'è uno specimen. Risposta
verificata: c'è la scheda `tipografia`, 41 righe, intitolata «Scala tipografica»,
ed è esattamente quello — otto gradini di dimensione con il token accanto. Uno
specimen della **scala**, non dei **caratteri**. Misurato ciò che il sistema
contiene e la scheda non mostrava: il corsivo è una faccia separata da 287 KB
usata 167 volte nel saggio e assente da ogni scheda; l'asse di peso va da 400 a
800 e nessun valore era reso; mancavano alfabeto, cifre, accenti e maiuscoletto —
che qui non è un dettaglio, perché è la scelta che sostituisce un secondo font.

Non era una decisione presa e registrata: era un buco di perimetro. Le schede
erano state definite come «~10 componenti reali» estratti dal saggio, e la
tipografia vi era entrata come problema di riconciliazione (tre scale ridotte a
una), non come materiale da documentare.

**Nona scheda, `components/caratteri/`, generata** da
`scripts/specimen_caratteri.py`. Il motivo per cui è generata e non scritta a
mano è il punto della cosa: la colonna di copertura dice quali codepoint ogni
file **dichiara** nella propria `cmap`, letta con fontTools. Quel dato non si può
dedurre dalla pagina — un glifo assente non lascia un quadratino, ripiega in
silenzio su un carattere di sistema e sembra a posto. È l'errore che in questo
repository è costato due affermazioni false. La scheda tiene le due cose
separate e lo dice in testa: *mostrato* a sinistra, *dichiarato* a destra.

Modalità `--check` come `export_tokens.py` e `build_css.py`. **Provata rompendo
apposta ciò che sorveglia**, su una copia di lavoro fuori dal repository:
sostituito `NotoSansMono-Tecnico.woff2` con EB Garamond, `--check` è uscito con
codice 1, e la rigenerazione ha riportato `∧ ∨ ⊕` come assenti da tutte e tre le
facce. fontTools è importato dentro la funzione, come in `subset_font.py`: sta
nel python di sistema (4.60.2), nessun ambiente virtuale.

**Due lacune latenti, trovate dalla scheda al primo giro**, nessuna delle quali
si manifesta oggi:
- il **corsivo** di EB Garamond non contiene `⁰ ¹ ² ⁸ ⁹` (solo `ⁿ` sopravvive);
- il sottoinsieme di **Noto Sans Mono** non contiene `¹` e `²`, coerentemente con
  l'elenco `TECNICI` dichiarato in `subset_font.py`, che non li include.

Verificato dove quei glifi compaiono davvero: `2ⁿ` dentro un `<em>` in
Fondamenti · 1 (e `ⁿ` c'è, nel corsivo), e `¹⁰ ¹¹ ¹²` nelle etichette d'asse del
grafico di Meccanismo · 6, che non dichiarano `font-family` e quindi ereditano EB
Garamond tondo, dove ci sono tutti. Nessun ripiego in atto. Le due lacune passano
da ignote a dichiarate, che è l'unico risultato che uno specimen possa dare
quando non c'è un difetto.

Resa verificata a 1100px: tre facce caricate, cinque tabelle, 21 righe di
copertura, nessuna richiesta fallita, nessun errore JavaScript.

## 2026-09-25 — L'ontologia era incoerente, e il controllo che doveva accorgersene guardava altrove

Prima del push, con ROBOT e HermiT installati per una verifica DL che `valida.py`
non poteva fare. Il reasoner ha trovato due cose, e la seconda è più grave della
prima.

**1. 738 violazioni del profilo OWL 2 DL, tutte di dichiarazione.** SKOS e Dublin
Core sono usati senza `owl:imports` — scelta documentata, il namespace non è
dereferenziabile — e in OWL 2 DL ogni IRI deve essere dichiarato. Senza
dichiarazione il reasoner indovina, e indovinava male: **`skos:broader`
risultava una proprietà di annotazione**, cioè ignorata da ogni inferenza, pur
essendo la gerarchia portante di un vocabolario SKOS. I termini esterni sono ora
dichiarati in fondo a `ontologia.ttl` col tipo che SKOS attribuisce loro.

Questo corregge anche un'affermazione della revisione in sola lettura di ieri, in
cui avevo scritto che «i costrutti usati rientrano in OWL 2 DL». Era falso:
avevo ispezionato le *espressioni* e non le *dichiarazioni*, e senza un
validatore di profilo non potevo saperlo. Lo strumento l'ha visto in un minuto.

**2. L'ontologia era incoerente, e lo era da prima di questa sessione.**
`:discussoInUnita` dichiara `rdfs:domain :Concetto`, ma 85 delle sue 262
asserzioni avevano per soggetto un `:Teorico` — 64 teorici, da Boole a
Wittgenstein. Il dominio inferisce che siano Concetti; `:Concetto` e `:Teorico`
sono disgiunti; contraddizione. Verificato che c'è anche nello stato committato.
Controllati poi tutti e 32 gli assiomi di dominio e range contro i dati: **questo
è l'unico** contraddetto.

**Perché `valida.py` non lo vedeva.** La chiusura OWL-RL *deduce* correttamente
che i 64 teorici sono Concetti — verificato, `True` per ognuno — ma `owl:Nothing`
resta vuoto. La disgiunzione è scritta come `owl:AllDisjointClasses` con
`owl:members`, e `owlrl` implementa la regola sulla forma `owl:disjointWith`, che
in questo grafo non compare **mai**, né asserita né derivata. La regola non aveva
su cosa scattare. Il controllo passava, e il README affermava che la disgiunzione
era «verificata con un reasoner OWL-RL, non solo dichiarata». Era dichiarata e
non verificata: la stessa forma dell'errore sui font e dell'harness cieco — uno
strumento che passa mentre misura altro.

**Correzione scelta dall'utente**: proprietà separata invece di allargare il
dominio. `:citatoInUnita`, dominio `:Teorico`, range `:Unita ⊔ :Capitolo` come la
sorella. Un concetto viene *discusso* in un'unità, un teorico vi è *citato*: due
relazioni diverse, interrogabili separatamente. Una riga sola in
`genera_dati.py`, perché il generatore già trattava i due casi in blocchi
distinti; `genera_html.py` unisce le due proprietà dove la pagina elenca chi cita
un'unità; `genera_grafo.py` la aggiunge alle proprietà della Lente.

**`:dataVerifica` diventa una proprietà di annotazione.** Era l'unica cosa che
teneva l'ontologia fuori dal profilo DL, perché `xsd:date` non appartiene alla
mappa dei datatype di OWL 2 e quel vincolo vale per le proprietà di dati, non per
le annotazioni. La decisione è nata da una domanda dell'utente — «a cosa serve il
tempo in questo lavoro?» — e dalla misura che ne è seguita: gli 11 valori sono
**tutti la stessa data**, la proprietà non compare in nessuna delle 196 pagine
generate, in nessuna delle 6 query, in nessun punto della Lente. È provenienza,
non una dimensione del modello, e ora lo dichiara.

**`valida.py` ora verifica la disgiunzione** sulla forma che il file usa davvero:
21 coppie, controllate individuo per individuo dopo la chiusura. Provato sui dati
precedenti alla correzione, dove trova i 64 e fallisce. Il repository non dipende
da Java per questo: ROBOT resta il controllo di profilo e di coerenza DL,
documentato e riproducibile, ma non incluso.

**Esito.** Profilo OWL 2 DL: «Ontology and imports closure in profile», zero
violazioni. HermiT: coerente. OWL-RL e SHACL: invariati, più il controllo nuovo.
Le 195 pagine rigenerate sono **identiche byte per byte** alle precedenti, il
grafo della Lente conserva 258 nodi e 537 archi (85 passati alla proprietà
nuova), e la pagina di Hebb continua a dire «Citato in Genealogia · 3.3,
Meccanismo · 4.1». La correzione è formalmente sostanziale e visivamente nulla,
che è esattamente ciò che doveva essere.

## 2026-09-25 — Storia riscritta: le cartelle `lab/` fuori dal repository pubblico

Ultimo passo prima del push, come previsto da `next-steps.md`. `git filter-repo`
ha rimosso `design-system/lab/` e `ontologia/lente-semantica/lab/` da **tutti** i
commit: 22 file, da 340 tracciati a 318, `.git` da 12 a 4,1 MB.

Eseguita su un clone usa-e-getta e verificata prima di sostituire il repository
di lavoro: zero occorrenze di `lab/` in tutta la storia, e l'albero di lavoro
identico all'originale a meno delle cartelle rimosse e dei file ignorati
(`design-system.inline.css`, `.venv`, `.DS_Store`).

**Un commit è scomparso**: `feat(design-system): primi test verificati —
tipografia, palette, eccezioni colore` toccava soltanto file di `lab/`, quindi
dopo il filtraggio era vuoto e `filter-repo` lo ha eliminato. Da 25 a 24 commit.
È la conseguenza coerente della decisione: i prototipi non si pubblicano, e il
commit che li registrava se ne va con loro. Ciò che quei test hanno stabilito
resta nelle voci di questo registro, che è dove serve.

**I quattro riferimenti a commit citati in questo file sono stati riscritti** con
la mappa prodotta da `filter-repo` (`c8db785`→`ef918c0`, `1791eda`→`d2fba43`,
`6da4c30`→`2425758`, `352c9c6`→`152a528`). Senza questo passaggio sarebbero
diventati puntatori a nulla: una riscrittura della storia invalida ogni hash
scritto in prosa, ed è il costo meno visibile dell'operazione.
