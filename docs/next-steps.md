# Next steps — cs-1-cartografia-semantica

## Prima della pubblicazione

- **Licenza** — scegliere tra le quattro alternative in [`../LICENSE`](../LICENSE)
  (discusse il 4 settembre 2026, decisione lasciata aperta di proposito).
- **Push su GitHub** — decisione a parte, da confermare esplicitamente quando il resto
  sarà pronto (vedi `../CLAUDE.md`, Regole operative).

## Roadmap

1. **Linee guida di design**, derivate dai test già in corso in
   `~/projects/portfolio/site/`. Due esempi concreti già esistenti da cui partire:
   il ridisegno dei box "1"/"0" che aprono ogni lezione del saggio (angoli smussati,
   bordo sfumato), e una "linea luminosa" che riusa la curva smoothstep del widget
   "Discesa del gradiente" già nel saggio (Unità 4.5).

2. **Applicare quelle linee guida** sia a `dominio/` sia a `ontologia/` (in particolare
   alla Lente semantica).

3. **Solo dopo, integrare i due**: cliccando un termine nel saggio (es. "embedding") si
   apre una tendina laterale con la lente centrata su quel termine; cliccando
   l'immagine della lente dentro la tendina si va alla pagina a schermo pieno della
   lente.

4. **Solo dopo l'integrazione**, valutare se e come includere altre visualizzazioni già
   abbozzate ma non costruite:
   - **Atlante topografico** — vista d'insieme del grafo, complementare al "un nodo
     alla volta" della lente.
   - **Matrice riordinabile** — vista strutturale ad adiacenza.
   - **Flusso corso↔vocabolario** — diagramma fra moduli del corso e facet del
     vocabolario, dichiarata "la tesi del case study".

   Altri mockup potrebbero aggiungersi.

5. **Collegare la card** già riservata in `~/projects/portfolio/site/lab.html`
   ("Dal bit alle entità semantiche") a questo repository, una volta pronto.
