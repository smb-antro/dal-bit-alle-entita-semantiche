# design-system/

Il sistema che tiene insieme le due metà di questo caso studio: il saggio
interattivo (`dominio/`) e la sua cartografia semantica (`ontologia/`).

Non è una raccolta di linee guida da leggere e applicare a mano. È CSS che le
pagine collegano: cambiare un valore qui cambia tutte e 14 le pagine del saggio,
le 194 dell'ontologia e la Lente semantica, senza toccarle.

## Come si usa

Le pagine del saggio collegano il sistema intero:

```html
<link rel="stylesheet" href="../../../design-system/css/design-system.css">
```

L'ontologia e la Lente collegano solo le **fondamenta** — font, tavolozza,
azzeramenti — perché sono superfici di consultazione con una tipografia propria
(radice a 16px invece di 19,2, colonna da 46rem invece di 740px, link color
inchiostro invece che arancio). Condividono la tavolozza, non la scala di lettura:

```html
<link rel="stylesheet" href="../../design-system/css/fondamenta.css">
<link rel="stylesheet" href="style.css">
```

Il CSS della pagina viene **dopo** e non è stratificato: per le dichiarazioni
normali questo basta a sovrascrivere il sistema senza alzare la specificità.

## Come è fatto

```
tokens/tokens.css          SORGENTE dei token. Primitivi → semantici.
css/reset.css              azzeramenti, e il reset di prefers-reduced-motion
css/base.css               tipografia, corpo, titoli, link
css/layout.css             colonna, binario, ritmo delle sezioni
css/components/*.css       sidebar, hero, apparato, richiami, tenda dei concetti
fonts/                     EB Garamond + IBM Plex Mono, self-hosted, una copia sola
components/<nome>/         schede di anteprima, una per componente
scripts/build_css.py       assembla le varianti generate
verify/                    harness di regressione visiva — vedi verify/README.md
lab/                       archivio dei prototipi che hanno stabilito le regole
```

Tre file sono **generati** e non si editano a mano (`build_css.py` li rifà,
`build_css.py --check` fallisce se sono disallineati):

| generato | a chi serve |
|---|---|
| `css/design-system.css` | le pagine del saggio, con `<link>`. Versionato: un clone deve funzionare senza far girare Python. |
| `css/fondamenta.css` | ontologia e Lente: solo `reset` e `tokens`. |
| `css/design-system.inline.css` | il bundle a file singolo: i font in data-URI, perché lì un percorso relativo non significa più niente. Non versionato — sono i font di `fonts/` ricodificati. |

### I cascade layer, e la regola che ne è uscita

L'ordine è dichiarato una volta sola in testa ai file generati:

```css
@layer reset, tokens, base, layout, components;
```

**I layer scavalcano la specificità**, e questo ha una conseguenza che non si vede
leggendo il codice: due regole che prima si ordinavano per specificità, separate in
due layer, si ordinano per layer. È costato 30px per ogni hero su 11 pagine prima che
l'harness lo mostrasse — `.hero` e `.unit-block section` si contendono `padding-top`.

> **Due regole che si contendono la stessa proprietà stanno nello stesso layer.**

Per questo `.hero` vive in `layout` accanto a ciò con cui compete, e non in
`components` dove la sua tipografia starebbe più comoda.

Attenzione al rovescio, controintuitivo: per le dichiarazioni `!important` l'ordine
dei layer **si inverte**, e un `!important` non stratificato diventa il più debole di
tutti. Per questo nel sistema c'è un solo `!important`, nel layer `reset`, dove
serve che vinca davvero.

## Il contratto pubblico

I nomi dei **primitivi non si rinominano**. Il JavaScript li legge per nome in 21
punti, in due modi:

- `getComputedStyle(...).getPropertyValue('--brina')` — `meccanismo-4-reti-neurali.html`,
  per disegnare i due canvas. Un nome inesistente non dà errore: restituisce `""` e
  produce un canvas nero.
- `var(--arancio-scuro)` dentro stringhe JavaScript che generano SVG inline —
  `meccanismo-1`, `meccanismo-3`, `meccanismo-5`, `meccanismo-6`, `lente.js`.

Per questo i primitivi conservano i nomi storici e valori letterali: chi disegna su
un canvas ha bisogno di un colore concreto, non di un ruolo. È un'eccezione
dichiarata alla regola dei tre livelli, non una svista.

I **semantici** (`--colore-navigazione`, `--dim-testo`…) sono invece liberi, e sono
quelli che i componenti devono usare.

## I principi

**Una famiglia di colore appartiene a un solo dominio, e le famiglie non si
mescolano mai nello stesso componente.** Blu vive solo nel binario di navigazione del
saggio — mai l'arancio lì, verificato togliendolo quando c'era per errore. Arancio è
tutto il resto dell'apparato del saggio. Verde è tutto ciò che viene dall'ontologia,
saggio compreso quando la tocca. Non è un vincolo estetico: è il modo in cui chi
legge distingue «sono ancora nel saggio» da «sto guardando dentro l'ontologia» senza
doverlo leggere. Dal 22 settembre 2026 il principio è visibile nei nomi stessi:
`--colore-navigazione`, `--colore-apparato`, `--colore-ontologia`.

**Il grado (scuro / base / chiaro) è intensità d'uso, non scelta libera.** `-scuro`
per testo e link, dove serve contrasto su bianco e brina; base per bordi e hover;
`-chiaro` per tinte di sfondo di stato.

**Un solo carattere.** EB Garamond per argomentazione e apparato. Pesi: 500 per i
titoli — 600 e oltre è pensato per un grottesco, su Garamond risulta pesante. Corsivo
sempre vero, mai simulato.

**L'apparato si distingue per trattamento, non per famiglia.** `font-variant:
small-caps` più `letter-spacing: .06em` sulla stessa Garamond, colore
`--colore-testo-tenue`. Niente secondo font.

**Il monospaziato ha due usi, entrambi dichiarati**: i quattro simboli logici
`∧ ∨ ¬ ⊕` di Fondamenti · 1, e i valori tecnici che cambiano dal vivo in
Meccanismo · 4 e 6 (formula, perdita, prompt). Tutto il resto che nel saggio
originale era monospaziato è passato a Garamond in maiuscoletto.

È **Noto Sans Mono**, ridotto ai 133 caratteri che servono (10 KB) da
`scripts/subset_font.py`. Ha sostituito IBM Plex Mono il 23 settembre 2026 per una
ragione misurata: Plex non contiene `∧`, `∨`, `⊕` — verificato leggendo la `cmap`
dei file, non a occhio — quindi tre dei quattro simboli ripiegavano su un font di
sistema, visibilmente più piccoli delle lettere accanto. Fra otto monospaziati con
licenza aperta esaminati, Noto Sans Mono è l'unico che li ha tutti e tre.
Tutto ciò che nel saggio originale era monospaziato — kicker, valori dei widget,
intestazioni di tabella — è passato a Garamond in maiuscoletto, verificato dal vivo
che i numeri che cambiano in tempo reale non «ballano», perché stanno in riquadri a
larghezza fissa.

**Mai verde per «vero».** Nelle tavole di verità il valore vero è arancio-scuro e il
falso grigio-soft. La scorciatoia ovvia è evitata di proposito: il ruolo del verde è
«viene dall'ontologia», non «logicamente vero», e confonderli costerebbe la
distinzione su cui regge tutto il resto.

### L'eccezione categoriale

Alcuni widget devono distinguere **più di tre categorie insieme**, e tre famiglie non
bastano senza farne coincidere due — una coincidenza lì significa perdere l'unica cosa
che il grafico esiste per mostrare. In ordine:

1. Riusa le famiglie confermate a piena saturazione, per quante categorie puoi.
2. Per ciò che resta, riusa un colore già presente altrove **con lo stesso ruolo
   categoriale**, invece di inventarne uno.
3. Mai una palette nuova costruita da zero per un singolo widget.

Le due scale categoriali della Lente (4 categorie di relazione, 7 gruppi di nodo)
sono un caso già risolto e validato per contrasto e distinguibilità: stanno nei token
fra i primitivi, e non si ridisegnano.

## La tavolozza

| Primitivo | Hex | Ruolo semantico |
|---|---|---|
| `--bianco` | `#FFFFFF` | `--colore-superficie` |
| `--brina` | `#F6F8FB` | `--colore-fondo` |
| `--inchiostro` | `#1a1a1a` | `--colore-testo` |
| `--grigio-testo` | `#4a4540` | `--colore-testo-attenuato` |
| `--grigio-soft` | `#6F6B67` | `--colore-testo-tenue` |
| `--blu-scuro` / `--blu` / `--blu-chiaro` | `#1F2B6B` / `#2B3A8C` / `#5A6FB8` | `--colore-navigazione-forte` / `-navigazione` / `-navigazione-tenue` |
| `--arancio-scuro` / `--arancio` / `--arancio-chiaro` | `#A85419` / `#D4722A` / `#E9A66B` | `--colore-apparato` / `-apparato-medio` / `-apparato-tenue` |
| `--verde-scuro` / `--verde` / `--verde-chiaro` | `#2A5628` / `#3D7A3A` / `#7AAD76` | `--colore-ontologia-forte` / `-ontologia` / `-ontologia-tenue` |
| `--line` | `rgba(26,26,26,.12)` | `--colore-bordo` |

## La scala tipografica

Una sola per tutte e 14 le pagine, dal 22 settembre 2026. Prima erano tre, ereditate
da tre modi diversi di convertire i file: la sidebar, che è lo stesso indice in ogni
pagina, era resa a 17,3 / 15,7 / 13,1px a seconda del capitolo.

| Token | Valore | Uso |
|---|---|---|
| `--dim-lede` | `1.2rem` | paragrafo d'attacco |
| `--dim-testo` | `1.05rem` | corpo del testo |
| `--dim-citazione` | `1.1rem` | `blockquote` |
| `--dim-richiamo` | `1.0rem` | `.question` |
| `--dim-nota` | `0.96rem` | `.aside p` |
| `--dim-apparato` | `0.78rem` | occhiello, nota di chiusura |
| `--dim-apparato-minore` | `0.72rem` | etichetta di `.aside` |
| `--dim-nav-titolo` | `1.02rem` | titolo del binario |
| `--dim-nav-parte` | `.74rem` | intestazione di parte |
| `--dim-nav-voce` | `.9rem` | voce di modulo |
| `--dim-nav-sottovoce` | `.82rem` | voce di unità |

Radice a `120%` per il saggio, lasciata a 16px per l'ontologia. Interlinea `1.65`.

## I componenti

Ogni cartella in [`components/`](components/) è un'anteprima autonoma, apribile nel
browser così com'è, e una scheda per il pannello di Claude Design — il marcatore
`<!-- @dsCard group="…" -->` sulla prima riga dice a quale gruppo appartiene.

| Scheda | Gruppo | Cosa mostra |
|---|---|---|
| [`tavolozza`](components/tavolozza/) | Fondamenta | le tre famiglie e i neutri, con primitivo e ruolo accanto |
| [`tipografia`](components/tipografia/) | Fondamenta | la scala con testo vero, e i quattro simboli logici |
| [`sidebar`](components/sidebar/) | Navigazione | il binario con scroll-spy e moduli apribili |
| [`hero`](components/hero/) | Lettura | apertura di pagina |
| [`richiami`](components/richiami/) | Lettura | nota a margine, domanda, citazione |
| [`apparato`](components/apparato/) | Lettura | occhiello, indicazioni, nota di chiusura |
| [`tenda-concetti`](components/tenda-concetti/) | Ontologia | il ponte fra saggio e ontologia, mostrato aperto |
| [`lente-colori`](components/lente-colori/) | Ontologia | le scale categoriali del grafo |

## Il JSON dei token, e perché esiste

La sorgente resta il CSS. `tokens/tokens.json` è **generato** da
`scripts/export_tokens.py` nel formato W3C Design Tokens Community Group (2025.10),
e serve a farsi leggere da fuori:

- **Claude Design** accetta un JSON di token, con tipi e descrizioni espliciti invece
  di dover dedurre il livello semantico dai nomi.
- **Figma**, via Tokens Studio o l'import delle variabili.
- **Style Dictionary v4**, che ha il DTCG di prima classe e da una sola sorgente
  genera JS, SCSS, Tailwind, mobile — così un altro progetto può consumare questi
  token senza accoppiarsi a questo repository: il flusso va in una direzione sola.

Limite dichiarato: **la spec non standardizza temi e modalità.** Un eventuale tema
scuro sarà un secondo file, non una variante dentro questo.

## Come si cambia qualcosa

1. Si edita la **sorgente** — `tokens/tokens.css` o un file in `css/`. Mai i generati.
2. `python3 scripts/build_css.py` — rigenera le tre varianti.
3. `python3 scripts/export_tokens.py` — rigenera `tokens/tokens.json`.
4. I tre controlli, che escono con 1 se qualcosa non va:

   ```bash
   python3 scripts/check_public_names.py   # il JavaScript trova ancora i nomi che legge?
   python3 scripts/check_contrast.py       # le coppie testo/sfondo passano WCAG AA?
   python3 scripts/export_tokens.py --check # il JSON corrisponde al CSS?
   ```

5. `cd verify && node cattura.js && python3 confronta.py`

L'ultimo passo non è una formalità: è il motivo per cui questo sistema ha potuto
sostituire 3.300 righe di CSS ricopiato senza cambiare un pixel. L'harness confronta
65 immagini su due viewport, stati interattivi compresi, e distingue una differenza
vera dal rumore di rasterizzazione misurando **di quanto** cambia un pixel, non
quanti ne cambiano. Vedi [`verify/README.md`](verify/README.md).

## Cosa non si tocca

- **I nomi dei primitivi** — vedi *Il contratto pubblico*.
- **Le scale `--cat-*` e `--grp-*`** della Lente — già validate.
- **I file generati** in `css/` — si rigenerano, non si editano.
- **`ontologia/src/*.ttl` e `ontologia/scripts/*.py`** — sono il deliverable
  dell'ontologia, non file di lavoro del design system. L'unico punto toccato è la
  riga di `pagina()` che collega le fondamenta.

## Dove sta il resto della storia

Il *perché* di ogni regola, con i casi limite discussi per arrivarci, sta in
[`lab/README.md`](lab/README.md) — l'archivio dei cinque prototipi che le hanno
stabilite — e in [`../docs/decision-log.md`](../docs/decision-log.md), che registra
anche le piste sbagliate: servono più delle conclusioni, perché il ragionamento si
ripete.
