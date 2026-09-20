# Next steps — cs-1-cartografia-semantica

## Prima della pubblicazione

- ~~**Licenza**~~ — ✅ decisa il 19 settembre 2026: tre regimi (codice MIT, ontologia
  CC BY 4.0, prosa riservata), vedi [`../LICENSE`](../LICENSE) e `decision-log.md`.
- ~~**Identificatori legacy**~~ — ✅ 20 settembre 2026: `:CorsoLLM` (schema di concetti)
  diventa `:DalBitAlleEntitaSemantiche`, `:VocabolarioBpeDelCorso` diventa
  `:VocabolarioBpeDelSaggio`. Vedi `decision-log.md`.
- **IBM Plex Mono** — 5 capitoli la caricano da Google Fonts (serve ai quattro simboli
  logici). Self-hosting o accettare la dipendenza di rete: decisione aperta.
- **Cartelle `lab/`** (`design-system/lab/`, `ontologia/lente-semantica/lab/`) — da non
  pubblicare; per ora restano nel repository, da escludere prima del push.
- **Push su GitHub** — decisione a parte, da confermare esplicitamente quando il resto
  sarà pronto (vedi `../CLAUDE.md`, Regole operative).

## Roadmap

1. **Linee guida di design** — ✅ scritte in [`../design-system/README.md`](../design-system/README.md),
   derivate da 5 prototipi verificati in `../design-system/lab/`. I due esempi originali
   del brief — box "1"/"0" a bordo sfumato, "linea luminosa" (curva smoothstep di Unità
   4.5) — sono stati valutati e scartati il 4 settembre 2026 (vedi `decision-log.md`).

2. **Applicare quelle linee guida** sia a `dominio/` sia a `ontologia/` — ✅ **fatto,
   tutte le pagine navigabili del saggio + la Lente semantica + tutto
   `ontologia/output/`**, il 4 settembre 2026: i 12 capitoli, più `presentazione.html`
   e l'appendice `dietro-i-widget.html`. Fondamenti · 1, Genealogia · 1, Meccanismo ·
   3/4/5 promossi da `lab/`; Fondamenti · 2 e `presentazione.html` convertiti a mano;
   Genealogia · 2/3/4, Meccanismo · 1/2/6 e `dietro-i-widget.html` convertiti con uno
   script di sostituzione token (vedi `decision-log.md` per metodo e verifiche).
   Nessun capitolo passa più per `design-system/lab/` — quella cartella resta come
   archivio dei test che hanno stabilito le regole, non un passaggio obbligato.
   **Nota storica**: era stato trovato `dominio/src/saggio/indice.html`, ancora nel
   tema scuro originale e orfano (nessun link in entrata) — non convertito in questo
   giro. Rimosso il 9 settembre 2026: la sidebar presente in ogni pagina copre già
   la stessa funzione di mappa di consultazione, vedi `decision-log.md`.

3. **Integrare i due** — ✅ **fatto per l'intero saggio**, l'8 settembre 2026: invece
   di una tendina con la lente centrata sul termine (piano originale), i termini del
   saggio riconosciuti dall'ontologia aprono una tenda con i dati del concetto (letti
   da `ontologia/output/concetti/*.html`) più un link alla pagina a schermo intero
   della lente. Copertura finale: **110 concetti unici** resi cliccabili su tutti i
   12 capitoli — Fondamenti · 1/2 (4/5), Genealogia · 1/2/3/4 (14/12/11/8), Meccanismo
   · 1/2/3/4/5/6 (14/10/11/18/11/11) — più `presentazione.html` (1, `Embedding`, come
   esempio dal vivo legato al «re, donna, regina» dell'apertura). Sempre scelti da
   `:discussoInUnita` nell'ontologia, mai a occhio (vedi `decision-log.md` per il
   dettaglio dei due bug reali trovati e corretti nel farlo). L'incorporare la lente
   in miniatura dentro la tendina, invece del solo link, resta un'idea possibile ma
   non decisa — nessun blocco tecnico residuo (`ontologia/output/` è convertito).

4. **Atlante topografico** — ✅ **fatto**, l'8 settembre 2026: poster statico del
   grafo completo (258 nodi, 537 relazioni) calcolato con una simulazione a forze
   D3 sugli stessi dati della Lente semantica, in fondo a `presentazione.html`, con
   lightbox per ingrandirlo (vedi `decision-log.md`). Restano da valutare, senza
   scadenza fissata:
   - **Matrice riordinabile** — vista strutturale ad adiacenza.
   - **Flusso corso↔vocabolario** — diagramma fra moduli del corso e facet del
     vocabolario, dichiarata "la tesi del case study".
   - **Tasto chiaro/scuro** — chiaro confermato come default il 4 settembre 2026
     (vedi `decision-log.md`); valori scuri già derivati e verificati su Fondamenti · 1
     (`design-system/lab/fondamenti-1-dark.html`), da estendere agli altri capitoli e
     costruire lo switch solo quando si arriva a questo punto.

   Altri mockup potrebbero aggiungersi.

   **Aggiornamento 9 settembre 2026**: il secondo grado della Lente semantica
   (vicini dei vicini) era una lacuna di leggibilità nota — punti muti senza
   etichetta, segnalata come "ancora da fare" in una versione precedente di
   questo file. ✅ **Risolta**: vedi `decision-log.md`, voce "Lente semantica:
   secondo grado come ramificazione leggibile".

5. **Collegare la card** già riservata in `portfolio/site/lab.html`
   ("Dal bit alle entità semantiche") a questo repository, una volta pronto.

## Debito rimasto, non ancora fatto

- **Rigenerare `dominio/output/dal-bit-alle-entità-semantiche_it.html`** via
  `dominio/src/build_output.py` — deliberatamente non rigenerato dal 4 settembre.
  Il bundle statico è ormai molto indietro rispetto ai file reali (contenuto,
  design system, tenda dei concetti, indice riorganizzato), e lo script stesso
  si è rivelato in parte disallineato (testo e font vecchi hardcoded in alcuni
  punti) — non un semplice ri-lancio, va prima aggiornato.
- **Push su GitHub** — vedi sopra, "Prima della pubblicazione".

## Fatto, non più debito

- ~~**Commit**~~ — ✅ 9 settembre 2026: il lavoro è committato (`feat(init)`,
  `feat(design-system)`, i due `feat(saggio)`, `feat(lente)`), più la passata di
  pulizia pre-pubblicazione del 15 settembre. Repository ancora non pubblicato su
  GitHub — decisione a parte, vedi sopra.
