# design-system/

Linee guida derivate da cinque prototipi verificati dal vivo in
[`lab/`](lab/README.md) (Fondamenti · 1, Genealogia · 1, Meccanismo · 3/4/5, Lente
semantica) — non ancora applicate ai file reali di `dominio/` o `ontologia/`. Questo
documento raccoglie le regole; il *perché* di ciascuna, con i casi limite discussi per
arrivarci, resta in `lab/README.md` e nella cronologia git.

## Da dove veniamo

Prima di questi test esistevano **tre sistemi indipendenti**, mai confrontati fra loro:

- il saggio (`dominio/`): tre font (Source Serif 4, Space Grotesk, IBM Plex Mono) su
  tema scuro, accento rame — mai pensato come "design system", cresciuto capitolo per
  capitolo;
- l'ontologia (`ontologia/output/` e la Lente semantica): un solo font (EB Garamond)
  su carta chiara, apparato in maiuscoletto invece che con un secondo font;
- il portfolio (`~/projects/portfolio/`): una palette confermata
  (`design-system/tokens.css` lì) mai ancora collegata a nessuno dei due.

Le regole sotto adottano la palette del portfolio ovunque, e il principio
"un solo font, l'apparato si distingue per trattamento non per famiglia" già
dell'ontologia — esteso anche al saggio, che non lo seguiva.

## Font

**EB Garamond**, self-hosted (OFL — stessi file di `ontologia/output/fonts/`, non
riscaricare). Un'unica famiglia per argomentazione e apparato. Pesi: 500 per
h1/h2/h3 (600+ è pensato per un grottesco come Space Grotesk, su Garamond risulta
pesante). Corsivo sempre vero (`font-style: italic`, mai simulato), per enfasi,
termini stranieri, citazioni.

**Mono** (IBM Plex Mono) **ristretto ai quattro simboli logici letterali** (∧ ∨ ¬ ⊕) —
decisione già presa altrove nel portfolio (`tokens.css`, 27 agosto 2026) prima ancora
di questi test, e confermata qui. Tutto il resto che nel saggio originale era mono —
kicker, readout dal vivo dei widget, intestazioni di tabella, valori vero/falso — passa
a Garamond in maiuscoletto (vedi sotto), anche i numeri che cambiano in tempo reale:
verificato dal vivo che non "ballano" percettibilmente, perché stanno in riquadri a
larghezza fissa, non in mezzo a una frase.

**Apparato = maiuscoletto, non un secondo font.** `font-variant: small-caps` più
`letter-spacing: .06em` sulla stessa Garamond, per: kicker, eyebrow, etichette di
form, intestazioni di tabella, footer-note, nomi di gruppo nella Lente. Colore
`--grigio-soft` di default — l'arancio (o il verde, nell'ontologia) resta riservato a
numeri e rimandi, non a ogni etichetta.

## Palette

| Token | Hex | Ruolo |
|---|---|---|
| `--bianco` | `#FFFFFF` | pannelli, superfici elevate |
| `--brina` | `#F6F8FB` | sfondo di pagina |
| `--inchiostro` | `#1a1a1a` | testo principale |
| `--grigio-testo` | `#4a4540` | testo secondario, didascalie |
| `--grigio-soft` | `#8A8580` | apparato, etichette, bordi di enfasi minima |
| `--blu-scuro` / `--blu` / `--blu-chiaro` | `#1F2B6B` / `#2B3A8C` / `#5A6FB8` | **solo** navigazione del saggio |
| `--arancio-scuro` / `--arancio` / `--arancio-chiaro` | `#A85419` / `#D4722A` / `#E9A66B` | apparato del saggio: link, numeri, stati attivi |
| `--verde-scuro` / `--verde` / `--verde-chiaro` | `#2A5628` / `#3D7A3A` / `#7AAD76` | **solo** ontologia: Lente semantica, tenda dei concetti |
| `--line` | `rgba(26,26,26,.12)` | bordi/divisori |

**Una famiglia, un dominio — non si mescolano.** Blu vive solo nella sidebar del
saggio (etichette di parte, numeri unità, voce corrente, pallino di scroll-spy — mai
l'arancio lì, verificato togliendolo esplicitamente). Arancio è tutto il resto del
saggio. Verde è tutto ciò che viene dall'ontologia, saggio compreso quando la tocca
(vedi sotto). Non è un vincolo estetico: è il modo in cui chi legge distingue "sono
ancora nel saggio" da "sto guardando dentro l'ontologia" senza doverlo leggere.

**Grado (scuro/base/chiaro) = intensità d'uso, non scelta libera.** `-scuro` per testo
e link (contrasto migliore su bianco/brina); base per bordi e hover; `-chiaro` per
tinte di sfondo di stati (badge "attivo", riquadro "lit" di un widget).

## L'eccezione categoriale

Alcuni widget devono distinguere **più di tre categorie insieme** (es. le mappe degli
embedding: quattro gruppi tematici di parole). Tre famiglie non bastano senza far
coincidere due categorie — e una coincidenza lì significa perdere l'unica cosa che il
grafico esiste per mostrare. Regola seguita finora, in ordine:

1. Riusa le famiglie confermate **a piena saturazione** (non i toni "chiaro") per
   quante categorie puoi — coprono già 3 casi su 4 nell'unico esempio incontrato finora.
2. Per ciò che resta, riusa un colore **già esistente altrove nel progetto con lo
   stesso ruolo categoriale**, invece di inventarne uno — es. il prugna (`#6B4A7A`)
   della quarta categoria è lo stesso `--cat-attribuzione` già usato dalla Lente
   semantica per lo stesso identico compito (distinguere categorie in un grafo).
3. Mai una palette nuova costruita da zero per un singolo widget.

Le due palette categoriali della Lente semantica (4 categorie di relazione, 7 gruppi
di nodo — in `ontologia/lente-semantica/output/lente.css`) sono un caso già risolto in
precedenza e **non toccate** da questi test: restano fuori da questa regola, non
riducibile a blu/arancio/verde e già validate.

## Componenti verificati

- **Sidebar** (saggio) — blu, vedi Palette.
- **Kicker/eyebrow/etichette** — maiuscoletto, vedi Font.
- **Riquadro `.aside`** — pannello bianco, bordo sinistro arancio.
- **Box `.question`** — bordo tratteggiato, testo arancio-scuro.
- **Tavole di verità / tabelle dati** — intestazioni maiuscoletto grigio-soft; valore
  vero → arancio-scuro; valore falso → grigio-soft. **Mai verde per "vero"** — la
  scorciatoia ovvia, deliberatamente evitata: il ruolo di verde è "viene
  dall'ontologia", non "logicamente vero", e i due non vanno confusi.
- **Widget canvas/WebGL** — leggere i colori da `getComputedStyle` a runtime (pattern
  già presente nel codice originale, non inventato qui) invece di valori fissi, così
  seguono il tema senza duplicare la palette in GLSL. Il paesaggio 3D di Meccanismo ·
  4.5 aveva già una palette per tema chiaro scritta e mai attivata: attivata con
  `data-theme="light"`, non ridisegnata da zero.
- **Box "1"/"0" e "linea luminosa"** — **scartati** (2026-09-04, vedi
  `docs/decision-log.md`): valutati fuori scope rispetto al lavoro restante. I box
  "1"/"0" restano con il trattamento già verificato nelle tavole di verità (vero →
  arancio-scuro, falso → grigio-soft); nessuna linea luminosa viene introdotta.

## Il rapporto dominio/ontologia

Il pezzo che dimostra la tesi del case study: nel saggio, i termini che l'ontologia
riconosce come concetti diventano cliccabili (dotted underline verde, colore
verde-scuro — non arancio, per lo stesso principio "colore = dominio" di cui sopra) e
aprono una tenda laterale con i dati letti **da `ontologia/output/concetti/*.html`,
mai rigenerati né modificati da qui** — più un link diretto alla Lente semantica
centrata su quel nodo (che ha già il proprio hash-routing, non aggiunto da questi
test). I termini da agganciare si scelgono interrogando `:discussoInUnita`
nell'ontologia, non individuandoli a occhio nel testo — finora fatto solo per
Meccanismo · 3 (11 concetti); da ripetere capitolo per capitolo mano a mano che si
converte il resto del saggio.

## Cosa non si tocca mai

- `ontologia/src/*.ttl`, `ontologia/scripts/*.py` — asset, non file di lavoro di
  questo repository.
- Le palette `--cat-*`/`--grp-*` della Lente semantica — già validate.
- `dominio/`, `ontologia/` restano copie sola lettura dei repository sorgente — le
  regole sopra si applicano qui, mai lì.

## Prossimi capitoli

Saggio non ancora convertito: Fondamenti · 2, Genealogia · 2/3/4, Meccanismo · 1/2/6.
Ontologia non ancora convertita: `ontologia/output/` (concetti, teorici, moduli,
fili) — ha ancora Garamond su crema, non questa palette. Dettagli e stato di ogni
test in [`lab/README.md`](lab/README.md).
