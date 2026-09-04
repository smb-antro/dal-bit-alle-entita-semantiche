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
design-system/    vuota per ora — vedi design-system/README.md
docs/             decision-log, next-steps, snapshot di questo repository
```

`dominio/` e `ontologia/` mantengono la propria documentazione interna (README.md,
CLAUDE.md, docs/) esattamente come nei repository sorgente — sono copie integrali,
non riscritte per l'occasione.

## Stato

Repository appena creato (4 settembre 2026), struttura in ordine, non ancora integrato
— vedi la roadmap in [docs/next-steps.md](docs/next-steps.md) — e non ancora pubblicato
su GitHub. La card è già riservata in `portfolio/site/lab.html` ("Dal bit alle
entità semantiche"), da collegare qui solo a integrazione avvenuta.

## Licenza

Non ancora decisa — vedi [LICENSE](LICENSE) per le quattro alternative in discussione.
Le librerie di terze parti vendorizzate (D3.js, EB Garamond) restano con la propria
licenza originale, indipendentemente da questa scelta.
