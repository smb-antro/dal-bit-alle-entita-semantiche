# Dal bit alle entità semantiche — Case study 1

Primo caso studio del portfolio di Stefano Bongiovanni.

## Cosa mette insieme

Due lavori nati separati:

- **[dominio/](dominio/)** — "Dal bit alle entità semantiche", saggio interattivo su
  come funzionano i modelli linguistici: dai principi discreti dell'hardware fino allo
  spazio vettoriale in cui si rappresenta il significato. Tre parti (Fondamenti,
  Genealogia, Meccanismo), dichiarato definitivo il 4 settembre 2026. Versione
  compilata: [`dominio/output/dal-bit-alle-entita-semantiche_it.html`](dominio/output/dal-bit-alle-entita-semantiche_it.html).
- **[ontologia/](ontologia/)** — un vocabolario controllato SKOS (111 concetti) e una
  micro-ontologia OWL (9 classi, 16 object property + 2 datatype property) che
  modellano quel saggio come dominio, validati con reasoner OWL-RL e SHACL. Deliverable
  primario: [`ontologia/docs/decisioni-modellazione.md`](ontologia/docs/decisioni-modellazione.md)
  — il resoconto delle scelte di modellazione, non il codice. Include anche una
  struttura di consultazione HTML ([`ontologia/output/index.html`](ontologia/output/index.html))
  e "Lente semantica", un grafo radiale interattivo per esplorare i concetti uno alla
  volta ([`ontologia/lente-semantica/output/index.html`](ontologia/lente-semantica/output/index.html)).

## Il sito

La radice del repository è anche la radice del sito: `index.html` è una pagina di
ingresso con tre porte — il saggio, l'ontologia, la Lente semantica — e non contiene
nient'altro, perché tutto ciò che conta sta dietro quei collegamenti. È l'unico file
HTML scritto a mano fuori dal design system, e ne usa i token.

`vercel.json` fa due cose sole, entrambe sul `Content-Type`: serve i `.ttl` come
`text/turtle` invece che come file da scaricare — sono il deliverable dell'ontologia,
non un allegato — e `LICENSE`, che non ha estensione, come testo.

**Il namespace non è dereferenziabile**, ed è una scelta dichiarata: l'ontologia si
identifica con `https://smb-antro.github.io/dal-bit-alle-entita-semantiche/vocabolario#`,
che è un identificatore, non un indirizzo. Nessun file viene servito a quel percorso.
Renderlo risolvibile richiederebbe un dominio stabile nel tempo, e un namespace agganciato
a un dominio che un giorno non si rinnova è peggio di uno che non ha mai risolto.

## Aprire il saggio compilato

[`dominio/output/dal-bit-alle-entita-semantiche_it.html`](dominio/output/dal-bit-alle-entita-semantiche_it.html)
è **un file solo**: caratteri, immagini, CSS e JavaScript sono incorporati, e la Lente
semantica è dentro come capitolo. Non fa nessuna richiesta di rete e non dipende da
nessun altro file — si può spostare o allegare così com'è. Si apre con un doppio clic.

**Una nota su Safari.** Se il file viene raggiunto incollando il percorso nella barra
degli indirizzi, Safari si rifiuta di aprirlo. Non è un difetto del documento: Safari
dà accesso a un file locale soltanto quando è il sistema a consegnarglielo, e lo stesso
vale per qualunque pagina HTML locale. Le vie che funzionano sono tre:

- doppio clic sul file;
- in Safari, **File → Apri file…** (⌘O);
- dal Terminale, `open -a Safari <percorso del file>`.

Chrome non ha questa restrizione. Servito da un server (http) la questione non si pone
affatto, in nessun browser.

## Perché stanno insieme

Il caso studio non è la somma di due strumenti scollegati: dimostra il rapporto tra un
dominio narrativo — un saggio pensato per essere letto in ordine, con la propria logica
pedagogica — e la sua cartografia semantica, cioè cosa succede quando quello stesso
dominio viene riformalizzato come vocabolario e ontologia, con vincoli di coerenza
formale propri. Il vocabolario non è un indice del saggio: è un'altra proiezione dello
stesso territorio.

## Struttura

```
dominio/          il saggio interattivo (copia sola lettura da cartografia-semantica)
ontologia/        vocabolario SKOS + ontologia OWL + Lente semantica (copia sola
                   lettura da vocabolario-ontologia-llm)
design-system/    linee guida di design e i prototipi che le hanno stabilite
docs/             decision-log, next-steps, snapshot di questo repository
```

`dominio/` e `ontologia/` mantengono la propria documentazione interna (README.md,
CLAUDE.md, docs/) esattamente come nei repository sorgente — sono copie integrali,
non riscritte per l'occasione.

## Stato

Integrazione sostanzialmente conclusa (9 settembre 2026): design chiaro uniforme su
tutte le pagine navigabili, tenda dei concetti su tutto il saggio (110 concetti
cliccabili), poster statico del grafo completo, secondo grado della Lente semantica
reso leggibile — vedi lo stato di dettaglio in [docs/snapshot.md](docs/snapshot.md).
Storia di commit solo locale, non ancora pubblicato su GitHub (decisione a parte, da
confermare).
Il bundle statico a file singolo è stato rifatto il 23 settembre 2026: autosufficiente,
senza richieste di rete, con la Lente semantica inclusa come capitolo — vedi
[docs/next-steps.md](docs/next-steps.md). La card è già riservata in
`portfolio/site/lab.html` ("Dal bit alle entità semantiche"), da collegare qui
quando il repository sarà pubblicato.

## Licenza

Tre regimi, uno per tipo di materiale — dettagli in [LICENSE](LICENSE):

- **Codice** (script, JavaScript, CSS) — MIT.
- **Ontologia e vocabolario** (`ontologia/src/*.ttl` e quanto ne è generato) — CC BY 4.0,
  dichiarata anche dentro i dati (`dct:license`).
- **Prosa del saggio e documentazione** — tutti i diritti riservati.

D3.js (ISC), EB Garamond (OFL) e Noto Sans Mono (OFL) restano con la propria
licenza originale.
