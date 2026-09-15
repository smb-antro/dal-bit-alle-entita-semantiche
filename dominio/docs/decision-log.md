# Decision log — corso-llm

## 2026-07-05 — Blocco A di corso-llm: file unico invece di un file per unità

Le Unità A.1 e A.2 esistevano come due file HTML separati (stesso shell CSS/JS, quasi
identico). Con l'aggiunta dei contenuti di A.3-A.6 (scritti dall'utente in
`blocco_a_unita_3-4-5-6_contenuti.md`, poi rimosso dopo la trascrizione), si è deciso di
unire l'intero Blocco A in un solo file scrollabile, `lezione_00_blocco_a.html`, invece di
6 file separati — motivazione: A.6 chiude il blocco con una timeline riepilogativa di tutte
le tappe, che ha senso solo nello stesso documento delle unità precedenti.

Navigazione a due livelli (decisione esplicita, tra due opzioni proposte): una mini-nav
superiore fissa per saltare tra le unità (A.1...A.6) più un rail laterale contestuale che
mostra solo i pallini delle sezioni dell'unità attualmente in vista, rigenerato via JS ad
ogni cambio di unità — scartata l'alternativa di un rail piatto con un pallino per ogni
sezione di tutte le unità (sarebbe arrivato a 30+ pallini, illeggibile).

I due file originari di A.1/A.2 sono stati rimossi con `git rm` dopo aver migrato il loro
contenuto (con id namespaced per unità, es. `a1-apertura` → evita collisioni con `a2-apertura`
ecc.) nel file unico.

Metodo di lavoro adottato per la trascrizione: shell, migrazione di A.1/A.2 e progettazione
della navigazione fatte direttamente in conversazione; trascrizione meccanica di A.3-A.6 dal
markdown (già scritto e definitivo, con convenzioni di conversione indicate dall'utente)
delegata a un subagente (modello Sonnet) — scelta motivata dal fatto che, con un contenuto
già finale e una mappatura testo→classi CSS già esplicita, il lavoro residuo era trascrizione
a basso rischio di ambiguità, non scrittura pedagogica da negoziare. Verificato dopo la
consegna: id univoci, corrispondenza tra sezioni HTML e array di navigazione JS, nessuna
classe CSS inventata, HTML ben formato (parsing pulito, tag bilanciati). La verifica visiva
nel browser (scroll-spy, rail contestuale, responsive) non è stata possibile in sessione per
un limite del sandbox di anteprima (nessun server statico avviabile) — da fare a mano.

## 2026-07-05 — Blocco B e C di corso-llm: struttura in unità, sessione in modalità autonoma

Sessione dedicata a completare Blocco B (limiti attuali) e Blocco C (interdisciplinarità)
del Modulo 00, seguendo il piano già scritto in `piano_corso_llm.md`. Decisioni di struttura
prese esplicitamente con l'utente prima di scrivere contenuto:

- **Blocco B — 3 unità**, una per "parte" del piano (B.1 cosa sanno fare davvero, B.2 cosa
  simulano di saper fare, B.3 cosa non sanno fare affatto), invece di una singola unità o di
  un raggruppamento 2+1. Le 5 domande aperte di sintesi dell'intero blocco confluiscono nella
  chiusura di B.3, sul modello con cui A.6 aveva già ospitato sia la timeline riepilogativa
  sia la chiusura del Blocco A intero.
- **Blocco C — 5 unità**: un'unità per ciascuno dei 4 nodi disciplinari (C.1 significato,
  C.2 causalità, C.3 biologico, C.4 coscienza) più una **C.5 dedicata** alla tabella
  riassuntiva dei gap e alla sintesi multidisciplinare finale — scelta esplicita di dare
  spazio proprio alla tabella (mai comparsa nel Blocco A) invece di comprimerla nell'ultimo
  nodo.

Dopo la conferma dell'utente sul contenuto di B.1 (primo campione di prosa, sviluppato in
conversazione), l'utente ha esplicitamente concesso fiducia per il resto del lavoro
("mi fido... procedi in modalità auto fino alla fine"), rimandando la propria verifica al
momento in cui entrambi i blocchi fossero pronti in HTML. Il resto della sessione — prosa
di B.2/B.3 e C.1-C.5, conversione HTML, aggiornamento di questa documentazione — è stato
quindi condotto senza ulteriori checkpoint intermedi, mantenendo comunque lo schema di
lavoro già validato (contenuto pieno in markdown prima dell'HTML, shell/navigazione/design
in conversazione diretta, trascrizione meccanica delegata a un subagente Sonnet).

**Nuovi componenti visivi per il Blocco C** (decisi in conversazione diretta, non delegati):
chip disciplinari (`.disc-chip`, pillole in font mono con bordo rame, elenco delle discipline
coinvolte in apertura di ogni nodo C.1-C.4 — visivamente imparentati con `.tl-tag` del
Blocco A ma senza contesto di timeline) e una tabella HTML reale (`.gap-table`, non una card
grid) per la tabella riassuntiva dei gap in C.5, con layout che si impila su mobile
(`data-label` per colonna, coerente con l'attenzione già data al responsive nel Blocco A).

Trascrizione meccanica delegata a due subagenti Sonnet separati (uno per Blocco B, uno per
Blocco C, lanciati in parallelo in background) — stesso criterio di rischio-basso già usato
per A.3-A.6. Verificato dopo ciascuna consegna, con controlli propri (non solo il resoconto
dell'agente): id univoci e coincidenti con l'array `UNITS` di navigazione, nessuna classe CSS
non definita nello `<style>`, HTML ben formato (parsing con parser Python, tag bilanciati),
tabella dei gap con esattamente 6 righe corrispondenti al markdown. Verifica visiva nel
browser (scroll-spy, rail contestuale, responsive) lasciata esplicitamente all'utente, che
l'ha richiesta come propria verifica finale di entrambi i blocchi.

**Nota ambientale**: la shell di questa sessione è risultata radicata in un worktree del
repo `projects/` (root) invece che nel worktree `corso-llm-moduli-1-6` di `qa-tool`
richiesto dal compito. Tutte le operazioni sono state indirizzate con path assoluti dentro
il worktree corretto; nessun nuovo worktree è stato creato. Segnalato esplicitamente
all'utente nel piano di questa sessione.

## 2026-07-05 — Blocco D di corso-llm: chiusura del Modulo 00 narrativo

Dopo la conferma dell'utente sul Blocco B e C ("tutto perfetto"), completato anche il
Blocco D (spazio, corpo, macchina) nella stessa sessione, con lo stesso schema di lavoro.
Decisione di struttura presa esplicitamente con l'utente: **2 unità**, invece di una unità
unica o di 4 unità (una per sezione del piano) — il contenuto di Blocco D è più snello di B
e C (4 sezioni concettuali, nessuna tabella, nessun nodo disciplinare), ma abbastanza denso
da giustificare comunque una mini-nav a due voci:

- D.1 — Cos'è lo spazio? Il corpo come strumento di misura (Newton, Kant, Merleau-Ponty,
  illusioni ottiche/Bayesian brain) — scritta in conversazione diretta e confermata
  dall'utente prima di procedere, stesso primo passo già validato con B.1.
- D.2 — Cosa vede/abita la macchina, il gap sensorimotor (computer vision, robot, Claude,
  Brooks, Lakoff e Johnson) — scritta in autonomia dopo la conferma di D.1, come concesso
  dall'utente per l'intero resto della sessione. Ospita anche la chiusura dell'intero
  Blocco D e la chiusura narrativa dell'intero Modulo 00 (A-D), con il raccordo esplicito
  al Modulo 0 tecnico già sviluppato (`lezione_00b_hardware_software.html`).

Nessun nuovo componente visivo necessario per D (a differenza dei chip/tabella di C):
tutte le sezioni riusano `.hero`, `.eyebrow`, `.aside`, `.question`, `blockquote`,
`.chiusura`, `.footer-note` già esistenti.

Trascrizione meccanica di D.2 delegata a un subagente Sonnet, come per B e C — stesso
criterio di rischio basso. Verificato dopo la consegna con controlli propri: id univoci e
coincidenti con l'array `UNITS`, nessuna classe CSS non definita, HTML ben formato (parser
Python, tag bilanciati), nessun residuo di markup non trascritto. Verifica visiva in
browser lasciata all'utente, come per B e C.

Con Blocco D completo, il Modulo 00 narrativo (Blocchi A-D) è terminato per intero. I file
markdown di appoggio (`blocco_b_contenuti.md`, `blocco_c_contenuti.md`,
`blocco_d_contenuti.md`) sono stati rimossi a fine sessione, con lo stesso trattamento già
riservato al file di appoggio del Blocco A: il contenuto autorevole vive ora nell'HTML, non
più in un file di scratch separato. Prossimo passo naturale, non ancora richiesto: il piano
dei contenuti dei Moduli 1-6 tecnici, ancora da scrivere.

## 2026-07-06 — Moduli 1-6: struttura testuale e avvio della pianificazione grafica

**Struttura testuale**. Su richiesta esplicita dell'utente, la scomposizione in unità dei
sei moduli tecnici (1 - testo come dato, 2 - probabilità, 3 - embedding, 4 - reti neurali,
5 - Transformer, 6 - scala) è stata fatta come processo a sé, prima di qualunque contenuto
in prosa: bozze di titoli/temi per modulo, proposte da me e corrette dall'utente in più
round. Numero di unità libero per modulo (da 4 a 6), non uniforme per scelta esplicita.
Deciso insieme anche un filo trasversale — discreto vs continuo, dal booleano del Modulo 0
ai vettori continui degli embedding — trattato non come unità a sé ma come punti di innesco
mirati in unità già esistenti (1.4, 2.2, 3.1/3.2/3.4, 4.4, 5.3, chiusura in 6.6 con la
quantizzazione). Salvato in `src/corso-llm/struttura_moduli_1-6.md`, già committato.

**Ordine del lavoro su testo vs grafica**: a differenza del Modulo 00, qui la componente
grafica/interattiva è centrale, non decorativa. L'utente ha scelto esplicitamente di
strutturare prima il testo (anche non definitivo) e solo dopo la grafica — motivazione: capire
prima il quadro dei contenuti permette di individuare temi/unità da integrare che potrebbero
emergere da altri testi non ancora portati in conversazione, prima di investire nella
progettazione grafica.

**Blender MCP valutato ed escluso per ora**: discusso l'uso di Blender per la parte grafica;
deciso di escluderlo dal lavoro corrente. È stato tenuto solo come opzione futura, eventuale,
per una fase "libro" successiva al completamento dell'intero corso — non per i componenti
interattivi veri, che devono girare nel browser e rispondere in tempo reale (Blender produce
render, non runtime interattivo).

**Inventario concettuale dei componenti grafici, modulo per modulo**: emerso un pattern
esplicito, confermato dall'utente — un componente centrale riusato/arricchito lungo le unità
di un modulo, non un widget per unità. Playground del tokenizzatore per M1; predittore
n-grammi con slider di contesto per M2; mappa navigabile dello spazio degli embedding per M3
(riusata per esplorazione, aritmetica vettoriale, polisemia); tre componenti eterogenei per M4
(neurone con pesi regolabili, XOR non separabile linearmente, discesa del gradiente animata);
frase cliccabile con pesi di attention per M5; componenti più leggeri e meno "certi" per M6, per
non dare falsa concretezza a fenomeni ancora dibattuti (es. capacità emergenti).

**Idea mantenuta, non scartata**: un collegamento tra il widget di M3 (spazio embedding) e
quello di M5 (attention) — la stessa parola polisemica che si "muove" nello stesso spazio da
statica a contestuale. Più ambizioso del resto, ma l'utente ha deciso di tenerlo, sfruttando la
settimana corrente in cui Fable è incluso nel piano per testarlo su un compito delimitato
(coerente con l'interesse già registrato in memoria per test hands-on di nuovi modelli).

**Metodo di delega per questa fase**: la specifica concreta di ogni componente va definita in
conversazione (design, dataset, logica) — solo dopo, con una specifica chiusa in mano, la
costruzione del prototipo viene delegata (a Fable, per il collegamento M3↔M5). Stesso principio
di rischio già usato per le trascrizioni meccaniche affidate a Sonnet nel Modulo 00, esteso qui:
il design non è delegabile, l'esecuzione da specifica chiusa sì.

**Primo passo tecnico concreto — dataset di embedding reali per M3/M5**: scelte 23 parole in
4 gruppi (reale/genere, sportivo, chimico, animali). Corretto in corsa un mio errore: avevo
proposto "banca" come esempio di polisemia seguendo la convenzione inglese ("bank" =
istituto/riva), ma in italiano "banca" non ha quella doppia lettura — sostituita con "calcio"
(gioco / elemento chimico / colpo), verificata come scelta valida.

Decisione esplicita di usare vettori reali (fastText italiano, `cc.it.300.vec`) invece di
coordinate costruite a mano, per coerenza con il punto pedagogico dell'unità 3.4: mostrare il
fenomeno dell'aritmetica vettoriale con le sue fragilità reali, non fabbricarlo. Vettori estratti
in streaming (senza scaricare l'intero file di 1.27GB) via `curl | gunzip | grep`.

Scoperta tecnica in corso di verifica: la PCA generica (sia su un campione ampio di vocabolario
sia sul solo set di 23 parole) non preservava le relazioni che i moduli vogliono mostrare — le
prime due componenti spiegavano solo il 6% della varianza su un campione ampio. Causa
concomitante isolata: il vettore di "re" aveva una norma anomala (3.65, contro 0.9-1.2 delle
altre parole — artefatto noto di fastText sui token brevi/ambigui), che deformava qualunque asse
di massima varianza. Risolta normalizzando tutti i vettori a lunghezza 1, ma anche dopo la
normalizzazione la PCA generica restava insufficiente.

Soluzione adottata: assi costruiti su misura per ciascuna delle tre modalità del widget, sempre
a partire da vettori reali (nessuna coordinata inventata) — non una singola mappa generica
condivisa, contrariamente all'ipotesi iniziale del pattern di riuso:
- *esplorazione*: PCA sui soli 23 vettori normalizzati — separa nettamente i 4 gruppi tematici;
- *aritmetica*: asse genere (media di donna−uomo e principessa−principe) + asse regalità (media
  di regina−donna e re−uomo, ortogonalizzato), verificato che "regina" è la parola più vicina al
  risultato di "re − uomo + donna" (distanza 0.445, seconda "principessa" a 0.636, poi salto
  netto);
- *polisemia*: asse dalla differenza tra i centroidi sportivo/chimico, verificato che "calcio"
  è molto più vicino al centroide sportivo (0.139) che a quello chimico (0.748), coerente con le
  similarità coseno nello spazio reale a 300 dimensioni (0.62 vs 0.44).

Dati salvati in `src/corso-llm/lezioni/embedding_dati_moduli_3_5.json`, con metadata che
documenta fonte, metodo e razionale di ciascuna modalità — collocati dentro `lezioni/` (non a
livello di `src/corso-llm/`) su richiesta esplicita dell'utente, perché il dato serve
direttamente al widget, non alla pianificazione.

Costruita anche una pagina HTML temporanea di sola verifica visiva (non il widget finale, nessun
design system) per controllare a occhio i tre risultati — rimossa dopo il controllo dell'utente,
stesso trattamento già riservato ai file di appoggio in markdown nelle fasi precedenti.
Prossimo passo, non ancora avviato: definire la specifica concreta del widget (interazioni,
transizioni tra modalità, collegamento con M5) e costruirne un primo prototipo con Fable.

## 2026-07-06 — Fase 1 di revisione della struttura testuale: integrazione di nuovo contesto

Prima di passare alle scelte di implementazione sui moduli rimasti (M1, M2, M4, M6), l'utente
ha deciso di portare nuovo contesto — letto direttamente da file locali in questa sessione — per
verificare se toccasse la struttura già scritta, seguendo il principio già stabilito: vedere il
contesto prima di spendere lavoro tecnico che potrebbe dover essere rifatto.

**Fonti lette in questa fase**:
- Un dialogo salvato in locale (appunti personali) — conversazione integrale
  utente/Opus 4.7 (Flora/Tolomeo), 9 capitoli: lezione su continuo/discreto (ℤ, ℚ, ℝ,
  numerabilità), lo scalare degli SVG, Gödel, la diagonale di Cantor, due nozioni di
  completezza, Galileo e le qualità primarie/secondarie, il crollo quantistico di quella
  distinzione, platonismo/formalismo matematico e Wigner, chiusura con la geometria
  differenziale sintetica di Lawvere (continuo primitivo, discreto come suo aggiunto).
- Roberto Calasso, *L'impronta dell'editore: I libri unici* (copia personale in PDF) —
  letto per intero via `pdftotext`, con attenzione
  particolare, su richiesta esplicita, alla sezione dalle copertine al saggio di Kevin Kelly
  sulla digitalizzazione universale (righe ~944-1470 del testo estratto), scomposta passo per
  passo senza comprimerla in sintesi lineare.

**Decisioni sull'uso del materiale**:
- Queste letture sono servite da contesto, non da fonte di testo. **Voce corretta il 15
  settembre 2026**: una versione precedente diceva che la tesi "il mondo si digitalizza da
  millenni, senza saperlo" fosse stata ripresa come tesi generale del corso. Verificato con
  una ricerca sul testo di tutti i capitoli: non compare, né quella formulazione né alcun
  riferimento a Calasso o a Kevin Kelly — la voce descriveva un'intenzione mai entrata nel
  saggio, e nessun testo altrui è stato riprodotto. Restano citate come fatti verificabili: von Neumann (*The Computer
  and the Brain*, 1958) e la coppia *veritas filia temporis* (Bacone) / *error filius
  temporis* (Bayle, via Blumenberg).
- Scartata la digressione sui *bandhu* vedici (concordato con l'utente): bellissima ma
  decorativa per moduli dichiaratamente "meccanici", non narrativi — riservata a un'eventuale
  revisione futura del Modulo 00, non usata qui.
- **Gödel/Cantor e Galileo/meccanica quantistica**: proposti inizialmente come scarti (troppo
  avanzati per un pubblico non-STEM, secondo una prima valutazione), ma l'utente ha corretto
  questa valutazione — motivando che il pubblico non-STEM debba essere istruito su questi temi,
  non solo sfiorato. Riconsiderati e integrati con vero peso, non solo come note, dopo aver
  trovato agganci tecnici precisi non colti alla prima lettura:
  - **Gödel/Cantor** paga un debito narrativo esplicito del Blocco A, dove compare già come
    domanda aperta e mai richiusa: "Un LLM è un sistema formale nel senso di Gödel?" (riga 77
    del piano). Un sistema formale gödeliano è discreto ed enumerabile, come un vocabolario di
    token; Cantor mostra che il continuo (ℝ, e per estensione lo spazio degli embedding) è
    strutturalmente più grande di qualunque insieme enumerabile — fondamento rigoroso, non solo
    intuitivo, del nesso causale già presente in 3.1 su perché il discreto non generalizza.
  - **Galileo (primarie/secondarie) e il crollo quantistico** si legano non al Blocco C (che
    resta chiuso, nessuna riapertura) ma direttamente ai Moduli 3 e 5: gli embedding come
    estensione radicale, quattro secoli dopo, del programma galileiano di quantificare solo ciò
    che è misurabile — applicato qui a un territorio (il significato) che Galileo aveva
    escluso; l'embedding contestuale del Modulo 5 come il punto in cui quel valore "fisso e
    indipendente dall'osservatore" crolla, con la stessa mossa concettuale della misura
    quantistica (posizione e quantità di moto non definite indipendentemente dalla misura).

**Modifiche concrete a `struttura_moduli_1-6.md`**: nuova unità **1.5** (Gödel, dedicata);
rafforzamento di 1.1 (tesi millenaria della digitalizzazione, von Neumann), 1.4 (analogia
raster/SVG), 3.1 (argomento diagonale di Cantor), 3.2 (Galileo, oltre al già presente cenno a
Leibniz), 3.4 (domanda aperta platonismo/formalismo, aggancio a Wigner), 5.4 (il crollo
quantistico applicato all'embedding contestuale — reso "cuore concettuale, non solo
decorazione"), 6.3 (l'arco lungo digitalizzazione→dati di addestramento, con collegamento
avanti al Modulo 5), 6.6 (provocazione di Lawvere come domanda di chiusura del corso,
esplicitamente non risolta). Aggiunta anche una riga nel riepilogo del filo discreto/continuo
per un secondo filo minore, Galileo/quantistico, che corre in parallelo tra 3.2 e 5.4.

**Stato del processo**: questa è la "fase 1" di una revisione in due fasi, dichiarata
esplicitamente dall'utente. La fase 2 non prevede altri file locali da leggere, ma
ragionamento diretto su punti che l'utente porrà in conversazione. Solo al termine della fase 2
si passerà all'inventario grafico definitivo e alle scelte di implementazione per i moduli
diversi da M3/M5.

## 2026-07-06 — Fase 2 di revisione: nove osservazioni dell'utente, senza nuovi file da leggere

Fase di ragionamento diretto, come anticipato: l'utente ha portato nove osservazioni proprie
(non da testi esterni) collegando concetti già presenti in Blocco B/C del Modulo 00 — già
completo e non riaperto — a possibili approfondimenti nei Moduli 1-6 tecnici. Per ciascuna,
prima di rispondere, sono stati riletti i passaggi originali in `lezione_00_blocco_b.html` e
`lezione_00_blocco_c.html` (non si è ragionato a memoria su frasi scritte in sessioni
precedenti).

**Le nove osservazioni e dove sono atterrate**:
1. Pleroma/creatura di Bateson (via Jung) applicati alla metafora "non c'è nessun architetto"
   di B.1 → domanda aperta in **4.3**, su cosa emerga davvero nella profondità di una rete.
2. Il "sillogismo dell'erba" di Bateson (logica della metafora, distinta dal sillogismo in
   Barbara) applicato all'interpolazione di B.2 → **3.4**, come fondamento filosofico
   dell'aritmetica vettoriale (perché funziona, e perché a volte fallisce).
3. Deduzione/induzione/abduzione, mai nominate esplicitamente finora → **2.2** (induzione) e
   **3.4** (abduzione, legata al punto 2).
4. Il termine tecnico "calibrazione", promesso esplicitamente ma mai onorato in B.2 ("un tema
   che tornerà, in forma tecnica, quando si parlerà di calibrazione") → payoff in **2.2**. La
   chiusura di B.2 ("Il quadro" — "stesso meccanismo, stesso punto cieco") riformulata come
   domanda filosofica per il modulo tecnico → chiusura di **4.5**.
5. Ragionamento causale (B.3.2/Nodo 2 di Blocco C) e stanza cinese di Searle — su richiesta
   esplicita dell'utente, solo annotato come nota aperta, non sviluppato (rischio di
   sconfinare troppo). Nessuna unità tecnica lo ospita ancora; Modulo 5 è il candidato più
   probabile.
6. Backpropagation confrontato con la schismogenesi di Bateson (*Naven*, 1936) e col feedback
   negativo classico → **4.5**: dà un quadro teorico preciso, non solo un'asserzione, alla
   distinzione già presente in C.3 fra addestramento discreto/globale e plasticità biologica
   continua/locale (il backprop è strutturalmente più vicino a un processo selettivo/
   evolutivo che a un vero feedback omeostatico).
7. Confronto Varela/Bateson sulla biologia della cognizione (autopoiesi e chiusura
   operazionale) → **4.1**, come secondo biologo in contrappunto a Bateson, a dare vocabolario
   più preciso al punto già presente in B.2 sui pesi che non "rappresentano" i dati in modo
   trasparente.
8. Plasticità sinaptica "continua e locale" (già in C.3) confrontata con hardware reale: i
   memristor (1971/2008) e il neuromorphic computing come corrispettivo hardware non
   speculativo → **4.5**, a dare corpo concreto alle "spiking neural networks" già nominate in
   C.3. Tenuto esplicitamente distinto: EEG/BCI non replicano la plasticità, sono
   un'ulteriore istanza pratica del filo discreto/continuo (segnale continuo campionato e
   discretizzato).
9. Un linguaggio "shape"/shader per disegnare con equazioni fisiche, identificato come
   GLSL/fragment shader in stile Shadertoy con tecnica SDF (Signed Distance Function) —
   riconosciuto come coerente in modo quasi programmatico col contenuto del corso (una
   superficie continua vera, non un grafico discreto, per la discesa del gradiente in 4.5),
   ma esplicitamente rimandato alla fase di inventario grafico/implementazione, non trattato
   come struttura testuale.

**Nuova struttura emersa**: un "terzo filo" trasversale (logica, informazione, biologia della
cognizione — Bateson, Varela, Peirce), distinto dal filo discreto/continuo e dal filo
Galileo/quantistico già tracciati, che corre da Modulo 2 a Modulo 4. Aggiunto un riepilogo
dedicato in `struttura_moduli_1-6.md`, sullo stesso modello degli altri due fili.

**Stato del processo**: fase 2 chiusa su dichiarazione esplicita dell'utente ("questo chiude
la fase 2"). Prossimo passo: inventario grafico definitivo e scelte di implementazione per i
moduli diversi da M3/M5 (per cui il lavoro tecnico è già stato fatto in una sessione
precedente).

## 2026-07-06 — Inventario grafico definitivo, in un file separato dalla struttura testuale

Chiusa la revisione testuale in due fasi, si è tornati sull'inventario concettuale dei
componenti grafici abbozzato a inizio sessione (prima delle fasi 1 e 2), per aggiornarlo alla
luce di tutto il contenuto aggiunto nel frattempo — senza per questo gonfiare l'inventario
solo perché il testo è cresciuto: confermato esplicitamente il principio già validato (un
componente interattivo centrale per modulo, non un widget per unità), con l'aggiunta che non
tutto il nuovo contenuto richiede grafica dedicata (pleroma/creatura, Varela, calibrazione come
concetto restano testuali, senza widget).

**Aggiunte concrete rispetto all'inventario iniziale**, motivate da contenuto emerso nelle fasi
1-2: comparazione raster/SVG con slider di zoom per 1.4; diagramma della diagonale di Cantor
per 1.5 (nuova unità); diagramma di calibrazione (reliability diagram) per 2.2; timeline
dell'arco storico digitalizzazione→dati per 6.3, nello stile già usato dal Blocco A narrativo.

**Decisione tecnica esplicita, la prima eccezione al design system vanilla**: la superficie di
perdita del Modulo 4.5 (discesa del gradiente) sarà resa con uno shader GLSL, tecnica SDF
(Signed Distance Function, stile Shadertoy) — invece di Canvas/SVG classico come tutto il
resto del sito. Motivazione dell'utente e mia, condivisa: è coerente in modo quasi
programmatico con ciò che il modulo insegna (una superficie continua vera, non un grafico
discreto che la simula) — la forma del componente incarna il contenuto, non solo lo illustra.
Comporta un impegno tecnico reale (WebGL, non solo Canvas 2D) da tenere presente
nell'implementazione.

Consolidato tutto in un nuovo file, `src/corso-llm/inventario_grafico_moduli_1-6.md`,
deliberatamente separato da `struttura_moduli_1-6.md` (quest'ultimo resta sulla sola struttura
testuale) — stessa logica di separazione già seguita per i dati di embedding, tenuti in
`lezioni/` invece che a livello di `src/corso-llm/`.

**Decisioni esplicitamente rimandate alla fase di implementazione**: la specifica concreta del
widget M3↔M5 (interazioni, transizioni, condivisione di dati/stato — poi prototipo con Fable);
come impostare l'infrastruttura WebGL/GLSL per 4.5 mantenendo coerenza col resto del sito;
dataset/contenuti concreti per i componenti di M1, M2, M4 (M6 è perlopiù
esplorativo/illustrativo, meno dipendente da dati reali come M3/M5).

**Stato del processo**: con questo, il lavoro preparatorio sui Moduli 1-6 (struttura testuale
in due fasi + inventario grafico) è concluso. Prossimo passo, non ancora avviato: le scelte di
implementazione vere e proprie per M1, M2, M4, M6.

## 2026-07-06 — Implementazione Modulo 1: tokenizzatore BPE reale, cerchio raster/SVG, diagonale di Cantor

Prima decisione di implementazione, discussa esplicitamente prima di eseguire: per il
playground del tokenizzatore (1.1-1.4) si è scelto di addestrare un vero algoritmo BPE
(Byte-Pair Encoding, Sennrich et al. 2016) invece di importare il vocabolario di un
tokenizzatore di produzione — stessa scelta di principio già fatta per gli embedding di M3
(autenticità reale, non messinscena), reso possibile qui dal fatto che l'algoritmo BPE è
semplice abbastanza da implementare per intero, a differenza degli embedding.

**Corpus di addestramento**: il testo integrale del Modulo 00 narrativo già scritto in questo
progetto (Blocchi A-D, ripulito da tag HTML) — 13.974 parole grezze, 2.989 uniche. Scelta
autoreferenziale esplicita: il corso che insegna la tokenizzazione viene tokenizzato usando se
stesso, nessun problema di provenienza.

**Risultato**: 300 unioni apprese, vocabolario finale di 334 simboli (34 caratteri base + 300
merge) — deliberatamente piccolo contro le ~50.000 unità di un sistema di produzione, per
restare leggibile in una demo. Verificato per intero: 0 errori di round-trip su tutte le 2.989
parole uniche del corpus (i token ricompongono sempre la parola originale esatta). Verificato
anche su parole mai viste nel corpus, incluse invenzioni pure (es. "blorpificazione"): il
suffisso italiano "-azione" viene riconosciuto correttamente anche lì, mentre il resto si
scompone in unità più piccole — esattamente il comportamento che l'unità 1.3 deve mostrare.
Salvato in `lezioni/bpe_merges_modulo1.json`, con metadata che documenta fonte, metodo e gli
esempi di verifica.

**Comparazione raster/SVG (1.4)**: generato un cerchio raster a bassa risoluzione (24×24 px,
`immagini_modulo1/cerchio_raster_24px.png`, via Pillow) e il suo equivalente SVG
(`immagini_modulo1/cerchio_vettoriale.svg`), stessi colori e proporzioni del design system
(sfondo `#0F2A22`, cerchio `#F0A85E`). Nota tecnica: creata prima una cartella
`assets_modulo1/`, poi rinominata in `immagini_modulo1/` dopo aver controllato il `.gitignore`
del progetto (contiene la regola `assets/`, che in git corrisponde a qualunque cartella
chiamata esattamente "assets" — il nome scelto inizialmente non ci sarebbe incappato, ma si è
preferito un nome più esplicito e coerente con le convenzioni italiane già in uso nel progetto,
per evitare ambiguità future).

**Diagonale di Cantor (1.5)**: costruita una lista di 8 sequenze di cifre e la sequenza
"costruita" modificando la cifra diagonale di ciascuna. Le prime 4 sequenze riprendono
deliberatamente l'esempio già usato nel Dialogo Flora/Tolomeo (fonte letta in fase 1 di
revisione), per continuità con quel materiale; le altre 4 aggiunte per una griglia più piena.
Verificato algoritmicamente che il numero costruito differisca da ogni numero della lista nella
cifra diagonale corrispondente (il nucleo dell'argomento di Cantor). Salvato in
`lezioni/cantor_diagonale_modulo1.json`.

**Stato**: Modulo 1 ha ora tutti i dati/asset necessari per i suoi componenti grafici (nessuno
richiede ulteriore lavoro di raccolta dati) — resta da costruire il widget HTML/JS vero e
proprio, non ancora iniziato.

## 2026-07-06 — Implementazione Modulo 2, 4, 6: dati e asset (sessione in modalità piano)

Lavoro pianificato esplicitamente in modalità piano di Claude Code (piano approvato
dall'utente, salvato in `~/.claude/plans/`), con una fase di esplorazione (verifica dello
stato di `inventario_grafico_moduli_1-6.md`, `struttura_moduli_1-6.md` e della metodologia
già stabilita per M1/M3) e una di progettazione prima dell'esecuzione. Un'unica decisione
aperta è stata sottoposta esplicitamente all'utente prima di procedere: il corpus per il
predittore n-grammi del Modulo 2 (vedi sotto).

**Correzioni emerse in fase di verifica, prima di scrivere il piano**: la cifra "86 miliardi
di neuroni" non era ancora scritta da nessuna parte nel progetto (solo "20 Watt" lo è, in
Blocco C) — andava aggiunta con citazione reale, non semplicemente "riusata" come il testo
esistente lasciava intendere. Confermata anche l'esistenza di una voce "1958 — Rosenblatt, il
Perceptron" già in Blocco A (righe 552-553) — coincidenza reale con von Neumann (anch'esso
1958), non un errore da correggere.

**Modulo 2 — corpus e n-grammi**. Decisione esplicita dell'utente (non del corpus del Modulo
00, per la ragione opposta a quella che aveva motivato l'uso di quel corpus per il BPE di M1):
un piccolo corpus **conversazionale scritto apposta** (46 frasi italiane semplici, pattern
ripetuti: gatto/cane che sale, dorme, salta, mangia...) invece del testo letterario del
Modulo 00, che essendo prosa densa a bassa ripetizione avrebbe prodotto soprattutto contesti
mai visti invece di previsioni che si affinano. Costruite le tabelle di conteggio per finestre
di contesto 1/2/3 parole; scelti tre prefissi dimostrativi **dopo** aver calcolato le
distribuzioni reali (non decisi a priori, stessa disciplina di M1/M3): "il gatto è salito sul
___" (previsione netta, tetto dominante 4/7), "il gatto salta sul ___" (distribuzione ambigua,
3 candidati quasi alla pari), "Ieri il gatto ___" (sparsità genuina: zero occorrenze a finestra
3 mentre finestre 1 e 2 hanno dati pieni — la parola "ieri" non compare mai nel corpus).
Verificato che le probabilità esatte sommano sempre a 1. Salvato in
`lezioni/ngram_dati_modulo2.json`.

**Modulo 2 — calibrazione (2.2)**. Tentata prima una misura reale (stesso principio già
seguito con la PCA di M3: si prova il metodo reale prima di ricorrere a dati illustrativi) —
split 34 frasi di training / 12 held-out (seed 42), tabella bigramma costruita solo sul
train, confidenza dichiarata vs accuratezza reale misurata su 65 predizioni valutabili nel
held-out. **Riuscito al primo tentativo**, nessun fallback necessario: tre bucket di
confidenza (n=14, 18, 33) mostrano un pattern reale e coerente con la letteratura — overconfidence
sistematica (l'accuratezza reale resta sempre sotto la confidenza dichiarata in ogni bucket).
Salvato in `lezioni/calibrazione_modulo2.json`.

**Modulo 4 — rete XOR (4.2/4.3)**. Addestrata via backpropagation (numpy puro) una rete
2-input/2-hidden/1-output, sigmoidale. Provati 30 seed casuali: 21/30 convergono in modo
netto (4/4 corretti), 9/30 restano bloccati in un minimo con solo 2/4 corretti — un
fallimento di ottimizzazione reale e osservato, non ipotetico, utile di per sé come nota
metodologica. Selezionato il seed 0 (convergenza pulita, margine di decisione ampio, 0.4868).
Valutata la rete su una griglia 100×100 per il vero confine di decisione curvo. Salvato in
`lezioni/xor_rete_modulo4.json`.

**Modulo 4 — superficie di perdita (4.4/4.5)**. Costruita come somma di due gaussiane
invertite (una più profonda/ampia = minimo globale, una più superficiale/stretta = minimo
locale) — non una griglia precalcolata ma una **specifica** (formula, parametri, gradiente
analitico), coerente con la decisione già presa di renderla come shader GLSL/SDF valutato
live, non Canvas/SVG. Verificato numericamente: discesa del gradiente da (0.9, 0.3) converge
esattamente al minimo globale (distanza finale ~1.5e-10); da (-0.65, -0.35) resta bloccata nel
minimo locale (loss finale identica al valore teorico nel centro del minimo locale). Inclusa
anche una funzione di prova più semplice (singolo paraboloide) per verificare la pipeline
WebGL/SDF separatamente dalla scelta della funzione pedagogica. Salvato in
`lezioni/paesaggio_perdita_modulo4.json`.

**Modulo 4 — neurone singolo (4.1)**. Nessun addestramento necessario (calcolatore live a
pesi regolabili). Riusati gli input booleani (0,0)/(0,1)/(1,0)/(1,1) di
`lezione_00a_funzioni_booleane.html` per continuità esplicita, più esempi continui; sigmoide
come attivazione (coerente con l'inquadramento "variante continua" del calcolatore booleano
discreto). Salvato in `lezioni/neurone_esempi_modulo4.json`.

**Modulo 6 — numeri di scala (6.1)**. Verificati via ricerca web: neuroni del cervello umano
~86 miliardi (Herculano-Houzel 2009, Frontiers in Human Neuroscience — sostituisce il vecchio
"100 miliardi" impreciso); GPT-3 (Brown et al. 2020) da 125 milioni a 175 miliardi di
parametri; PaLM (Chowdhery et al. 2022, Google) 540 miliardi di parametri, 780 miliardi di
token — tutte cifre storiche stabili e ufficialmente pubblicate, preferite a stime non
confermate su modelli più recenti/chiusi. Salvato in `lezioni/scala_modulo6.json`.

**Modulo 6 — timeline (6.3)**. Riusate verbatim le classi CSS `.timeline`/`.tl-node`/
`.tl-tag`/`.tl-date`/`.tl-title`/`.tl-desc` di `lezione_00_blocco_a.html`, nessun nuovo stile.
Quattro voci verificate: alfabeto fenicio (framing a intervallo ca. XI-X secolo a.C., non
falsa precisione — le iscrizioni sopravvissute datate con sicurezza sono del X secolo, l'XI è
convenzione storiografica); von Neumann 1958 (già deciso in fase 1); Google Books, data reale
precisa **14 dicembre 2004** (sostituisce il generico "primi anni 2000" del testo esistente);
corpora LLM 2018-oggi (intervallo, non falsa data singola). Salvato in
`lezioni/timeline_modulo6.json`.

**Modulo 6 — capacità emergenti (6.2)**. Riletto il testo esatto di
`lezione_00_blocco_b.html` prima di scrivere, per allineare terminologia (usa già "aritmetica
a più cifre" e "ragionamento a più passi" come esempi, e cita già Schaeffer et al. 2023 per
la critica). Costruita una curva illustrativa (dichiarata esplicitamente come tale nel
metadata, non spacciata per dati di un paper) con la soglia collocata in un ordine di
grandezza coerente con gli anchor reali di 6.1. Aggiunta la citazione mancante di Wei et al.
2022 (TMLR, arXiv:2206.07682) come origine reale del framing. Salvato in
`lezioni/capacita_emergenti_modulo6.json`.

**Modulo 6 — base vs fine-tuned (6.4/6.5) e quantizzazione (6.6)**. Scritta una coppia
prompt/risposta che illustra, senza caricatura, il fenomeno reale e documentato (Ouyang et
al. 2022, InstructGPT) per cui un modello di base continua il pattern superficiale del testo
invece di eseguire un'istruzione. Livelli di quantizzazione reali (FP32/FP16-BF16/INT8/INT4)
con nota d'uso pratico per ciascuno. Salvati in `lezioni/base_vs_tuned_modulo6.json` e
`lezioni/quantizzazione_modulo6.json`.

**Stato**: tutti i dati/asset per M2, M4, M6 sono pronti e verificati meccanicamente (stesso
standard di M1/M3). Restano da costruire i widget HTML/JS per tutti i moduli (1-6), incluso
il collegamento M3↔M5 non ancora specificato e l'infrastruttura WebGL/GLSL per 4.5 — nessuno
di questi due punti affrontato in questa sessione.

## 2026-07-06 — Primo widget costruito: Modulo 1 completo (lezione_01_testo_come_dato.html)

Prima costruzione di un widget vero (non solo dati di supporto). Metodo di lavoro: costruita
prima l'Unità 1.1 da sola (encoding, con lo stadio 1 del playground del tokenizzatore),
verificata dall'utente in browser e confermata prima di procedere con le altre quattro unità
in autonomia — stesso schema di conferma-su-primo-campione già validato per il contenuto in
prosa del Modulo 00.

**Struttura**: shell a due livelli di navigazione (tab in alto per le 5 unità, rail
contestuale per sezione), stessa architettura CSS/JS già stabilita per i Blocchi A-D del
Modulo 00 — nessuno stile nuovo introdotto. Contenuto in prosa scritto per tutte le unità
1.1-1.5 a partire dalle descrizioni già presenti in `struttura_moduli_1-6.md`.

**Playground del tokenizzatore, cresciuto progressivamente come da inventario grafico**:
stadio 1 (1.1, codici carattere Unicode live), stadio 2 (1.2, confronto taglio ingenuo sugli
spazi vs token BPE reali), stadio 3 (1.3, parole inventate con pulsanti di esempio —
"blorpificazione", "chatbotaggine", "supercazzola" — per mostrare il fallback su parole mai
viste), stadio 4 (1.4, ID numerici dei token). Comparazione raster/SVG con slider di zoom
(1.4, immagini già pronte in `immagini_modulo1/`). Widget della diagonale di Cantor con
pulsante che rivela il numero costruito (1.5, dati già pronti in
`cantor_diagonale_modulo1.json`).

**Arricchimento di `bpe_merges_modulo1.json`**: aggiunto un campo `vocabolario` esplicito
(334 simboli con ID sequenziale — 34 caratteri base ordinati alfabeticamente, poi le 300
unioni nell'ordine di apprendimento), necessario per mostrare gli ID dei token in 1.4. Prima
versione del calcolo conteneva un errore (i caratteri base venivano dedotti dai soli merge,
perdendo 6 caratteri mai coinvolti in un'unione entro 300 iterazioni) — corretto ricavando i
caratteri base direttamente dal corpus originale, non per inferenza dai merge.

**Limite di sandbox incontrato**: tentato l'uso del server di anteprima integrato
(`preview_start`), fallito due volte con `PermissionError`/`getcwd: cannot access parent
directories` — il processo lanciato dallo strumento non ha accesso a `getcwd()` in questo
sandbox. Creato comunque un `.claude/launch.json` (server statico Python su porta 8532 per
`lezioni/`) come riferimento futuro, anche se non utilizzabile dallo strumento di anteprima
in questo ambiente. Verifica quindi condotta copiando i file su Desktop per apertura diretta
da parte dell'utente (stesso trattamento già riservato al file di verifica di M3).

**Bug reale trovato e corretto — lezione sul metodo di verifica**: la prima consegna
mostrava solo l'intestazione della prima unità, nient'altro. Causa: un doppio backslash in
una stringa JS (`label:'Dal token all\\'ID'`) chiudeva la stringa in anticipo, rendendo il
resto (`ID'`) sintassi non valida — un errore di sintassi ovunque nel blocco `<script>`
impedisce l'esecuzione dell'intero blocco, quindi l'observer che rende visibili le sezioni
`.reveal` non veniva mai installato (solo il contenuto dell'hero, non avvolto in `.reveal`,
restava visibile). La verifica precedente (bilanciamento tag HTML, corrispondenza ID) non
intercettava questo tipo di errore, perché è un errore di sintassi JavaScript, non HTML.
Corretto (virgolette doppie per la label con apostrofo), poi verificata la sintassi con un
motore JS reale — `osascript -l JavaScript` (JavaScriptCore, nessun Node disponibile
nell'ambiente) via `new Function(codice)`, che compila senza eseguire (evita falsi errori per
`document`/`window` assenti in quel contesto). Nessun altro caso di doppio backslash trovato
nel file. L'utente ha confermato il funzionamento dopo la correzione.

**Stato**: Modulo 1 completo (contenuto + widget) e verificato funzionante dall'utente.
Metodo di verifica per i prossimi widget aggiornato: controllo sintassi JS reale (via
`osascript -l JavaScript`), non solo controlli strutturali HTML — la classe di bug che ha
causato questo fallimento non sarebbe stata presa altrimenti.

## 2026-07-06 — Moduli 3 e 5 completi, primo uso reale di Claude Fable 5

Sessione in modalità piano, a differenza delle gemelle M2/M4/M6: qui la progettazione dei
widget non è stata delegata fin da subito, perché il compito includeva un collegamento
concettuale ambizioso tra le due pagine (la parola polisemica "calcio" che si sposta da
statica a contestuale) su cui l'utente aveva già deciso di non fare vera interazione live
tra i file. La specifica di interazione è stata quindi negoziata in conversazione diretta
(quattro domande mirate via `AskUserQuestion`, tutte risolte con l'opzione raccomandata)
prima di scrivere il piano finale e solo dopo delegare la costruzione a Fable.

**Decisioni di specifica confermate esplicitamente dall'utente**:
- M5 non ha un vero Transformer dietro: i pesi di attention (spessore/opacità delle
  connessioni) sono numeri scritti a mano, dichiarati esplicitamente come illustrativi nel
  metadata — stesso trattamento già usato per la curva delle capacità emergenti nel
  Modulo 6. Scartata l'alternativa di un calcolo QKV "giocattolo" con matrici casuali: più
  complesso da costruire e verificare, senza guadagno reale di autenticità (non sarebbe
  comunque stato un vero Transformer addestrato).
- Frasi proposte da me e confermate senza modifiche: frase principale per 5.2/5.3
  ("Il gatto che il vicino aveva adottato dormiva sul divano.", dipendenza lunga
  soggetto-verbo), e la coppia per 5.4 ("Ieri la squadra ha vinto la partita di calcio."
  vs "Il calcio rinforza le ossa insieme al ferro.").
- In 3.4, confermata la selezione libera A/B/C tra tutte le 23 parole (non solo il caso
  di default re-uomo+donna): il calcolo del bersaglio è dal vivo sulle coordinate 2D già
  proiettate, matematicamente legittimo perché la proiezione è lineare (verificato in
  sessione precedente che coincide con `aritmetica.target` per il caso di default) — non
  un problema se una combinazione arbitraria produce un risultato "brutto", è la fragilità
  che l'unità deve mostrare.
- Per la mini-mappa di 5.4, confermata l'interpolazione dichiarata (0.6, calcio si sposta
  dalla posizione statica reale verso il centroide reale calcolato dal vivo) come
  illustrazione concettuale esplicita del "collasso contestuale", non un vero embedding
  contestuale calcolato.

**Preparazione dati non delegata (come per M1/M2/M4/M6)**: prima di invocare Fable, ho
scritto io stesso `src/corso-llm/lezioni/attention_dati_modulo5.json` — matrice 10×10 di
pesi "sintattici" per la frase principale (scritta a mano, verificata che ogni riga sommi
esattamente a 1), una seconda testa "posizionale" generata da una formula deterministica
(peso ∝ 1/distanza², con un raw fisso più basso per il peso verso sé stessi in modo che il
massimo di ogni riga cada sempre sul vicino immediato — proprietà verificata
programmaticamente per tutte le 10 righe, non solo asserita), una terza testa "tematica"
con coppie gatto↔dormiva/vicino↔adottato/divano↔sul, e le due righe di attention di
"calcio" nelle frasi sportivo/chimico. Stesso principio già seguito nel progetto: il
contenuto autorale (i numeri, le frasi, il loro significato pedagogico) non è delegabile,
solo l'implementazione meccanica del widget lo è.

**Delega a Fable (`model:"fable"`, Claude Fable 5)** — primo uso reale di questo modello
nel progetto, con un'unica chiamata per entrambi i file (condividevano dati e metodo):
prompt esteso con l'intera specifica confermata, i contenuti completi da incorporare di
`embedding_dati_moduli_3_5.json` e del nuovo `attention_dati_modulo5.json`, il riferimento
esplicito a `lezione_01_testo_come_dato.html` come modello di shell, e le sezioni di
`struttura_moduli_1-6.md` (Modulo 3 e 5) da cui scrivere la prosa. Istruzione esplicita:
due file autonomi, nessun riferimento incrociato, nessuna vera interazione live.

**Valutazione di Fable sul compito** (prima valutazione reale, vale la pena registrarla
in dettaglio): risultato solido, aderente alla specifica su tutti i punti verificati in
autonomia dall'agente stesso durante il lavoro (non solo dichiarato a consegna avvenuta):
dati incorporati iniettati programmaticamente e riverificati byte-per-byte contro le
sorgenti (non trascritti a mano, quindi a rischio zero di errori di trascrizione), test
interattivi in un browser vero durante la costruzione (nearest list, toggle legenda,
hover, tab 5.4, shuffle posizionale), e un bug di sintassi JS trovato e corretto in
autonomia — un'altra label con apostrofo racchiusa in virgolette singole, la stessa classe
di errore già incontrata con il Modulo 1 (`'…dell'erba'`), stavolta intercettata da Fable
prima della consegna, non dopo. Nessun caso analogo sopravvissuto: verificato di nuovo io
stesso con `osascript -l JavaScript` su entrambi i file, sintassi pulita.

**Verifica indipendente mia, dopo la consegna** (non solo il resoconto dell'agente):
sintassi JS con motore reale confermata OK su entrambi i file; HTML ben formato (parser
Python, tag bilanciati, zero errori); nessuna classe CSS usata (in HTML o generata da JS,
incluse `classList`/`className`) assente dal proprio `<style>`; id tutti univoci (40 in
lezione_03, 47 in lezione_05) e coerenti con l'array `UNITS` di navigazione (ogni id di
sezione e ogni unit-block presente nel DOM); dati incorporati (`EMB` in lezione_03, `ATT`
e la copia indipendente `POLI5`/`POLI5_GRUPPI` in lezione_05) confrontati byte-per-byte
con i JSON sorgente via un motore JS reale — uguaglianza esatta su tutti e tre; calcolo
dell'aritmetica vettoriale di default (re − uomo + donna) rieseguito indipendentemente in
Python sulle stesse coordinate — confermato "regina" a distanza 0.445, "principessa" a
0.636, esattamente come nel metadata e come mostrato dal widget; nessun riferimento a
RNN/LSTM in 5.1 (ponte narrativo rimasto anonimo, come richiesto); presenza confermata di
tutti i nodi concettuali obbligatori (Cantor in 3.1, Leibniz+termine "embedding"+Galileo in
3.2, Firth+Wittgenstein in 3.3, sillogismo dell'erba di Bateson+Wigner in 3.4, Galileo/
crollo quantistico in 5.4, QKV in 5.3, pagine del libro in 5.5, GPU/2017 in 5.6).

**Nota di metodo per il futuro**: Fable ha risposto bene a una specifica molto estesa e
dettagliata (frasi, numeri, formule, struttura dati tutti forniti esplicitamente, non
inventati) — coerente con l'ipotesi di partenza che il modello vada testato su un compito
delimitato, non su una progettazione aperta. Non emerge da questa sessione alcuna evidenza
su come si comporterebbe con una specifica più vaga.

File copiati su Desktop per la verifica visiva dell'utente (stesso limite noto del server
di anteprima integrato, non riprovato). Nessun commit ancora eseguito in questa sessione.

**Stato**: Moduli 1, 3 e 5 completi (contenuto + widget) e verificati meccanicamente.
Verifica visiva in browser di M3/M5 lasciata all'utente. Restano da costruire i widget di
M2, M4 (incluso lo shader GLSL/SDF di 4.5) e M6 — dati/asset già pronti per tutti e tre.

## 2026-07-06 — Modulo 2 completo (lezione_02_probabilita.html)

Sessione in modalità piano (worktree già esistente, nessun nuovo worktree creato). Metodo
di lavoro concordato esplicitamente con l'utente: costruire prima l'unità 2.1 da sola,
copiarla su Desktop per la verifica dell'utente, attendere conferma, poi procedere in
autonomia con 2.2-2.4 — stesso schema di conferma-sul-primo-campione già validato per il
Modulo 1. Shell CSS/JS e navigazione a due livelli copiate verbatim da
`lezione_01_testo_come_dato.html`, nessuno stile nuovo nella shell.

**Predittore n-grammi (componente centrale, cresciuto progressivamente 2.1→2.4, come da
inventario grafico)**: a differenza di quanto inizialmente ipotizzabile, il file
`ngram_dati_modulo2.json` non contiene una tabella di conteggio generale per prefissi
arbitrari, solo il corpus grezzo (46 frasi) e tre esempi dimostrativi precalcolati come
riferimento. Il widget conta quindi gli n-grammi **dal vivo in JavaScript** sul corpus
(marcatori `<inizio>`/`<fine>`, finestra scorrevole di 1-3 parole), non da una tabella
precotta — scelta tecnica necessaria, non solo preferita, resa possibile dalla piccola
dimensione del corpus. Verificata la correttezza di questa logica di conteggio **prima
della consegna**, non solo dichiarata: la funzione JS riproduce esattamente, byte per
byte, tutti e 9 i valori di riferimento (3 esempi dimostrativi × 3 finestre) del JSON già
verificato in sessione precedente — controllo eseguito con un motore JS reale
(`osascript -l JavaScript`), non a mano.

**Progressione del widget per unità**: 2.1 introduce il compito con finestra fissa a 1
parola (nessuno slider ancora); 2.2 affianca unigramma e bigramma sullo stesso prefisso
per mostrare il passaggio conteggio→probabilità, e introduce il diagramma di calibrazione
(reliability diagram SVG generato dal vivo, 3 punti cliccabili per i dettagli del bucket,
diagonale di riferimento); 2.3 sblocca lo slider completo (1-3) con due preimpostazioni
(previsione netta, distribuzione ambigua) per mostrare l'assunzione di Markov; 2.4 riusa lo
stesso widget con una terza preimpostazione (sparsità, default a finestra 2) per mostrare
dal vivo la rottura a finestra 3, più un piccolo diagramma statico HTML/CSS (nessun
dataset) per le dipendenze lontane — scartata una versione con arco SVG posizionato sopra
la frase, troppo fragile da allineare correttamente con testo a larghezza variabile;
sostituita con un riquadro "finestra" schematico, sempre corretto indipendentemente dal
contenuto.

**Verifica indipendente della calibrazione**: oltre al riuso diretto dei tre bucket già
presenti in `calibrazione_modulo2.json`, i bucket sono stati anche ricalcolati in modo
indipendente dalle 65 predizioni grezze (`predizioni_valutate`) con un motore JS reale, per
verificare che non ci fosse disallineamento fra il dato aggregato e quello grezzo prima di
incorporare entrambi nel file — coincidenza esatta (n, confidenza media, accuratezza) su
tutti e tre i bucket.

**Contenuti**: 2.1 (compito centrale, richiamo a "completamento statistico" di Blocco B);
2.2 (conteggio→probabilità, prima crepa nel discreto — probabilità come numero reale,
termine tecnico "induzione" in aggancio a Blocco B.2, payoff del debito "calibrazione"
lasciato esplicitamente in Blocco B.2); 2.3 (n-grammi generalizzati, assunzione di Markov
nominata esplicitamente con esempi extra-linguistici — previsioni meteo, giochi da tavolo);
2.4 (sparsità e dipendenze lontane, cenno alla critica di Chomsky ai modelli a stati
finiti, chiusura con apertura esplicita verso il Modulo 5 per le dipendenze lontane e
verso il Modulo 3, che segue subito, per il passaggio a uno spazio continuo).

**Verifica finale**: sintassi JS reale confermata OK sull'intero file (non solo dopo 2.1);
tag bilanciati, nessun id duplicato, nessuna classe CSS orfana, corrispondenza esatta fra
tab della topbar e unit-block, tutti gli id dell'array `UNITS` presenti nel DOM. File
copiato su Desktop per la verifica visiva dell'utente, sia dopo l'unità 2.1 sia dopo il
file completo (stesso limite noto del server di anteprima integrato, non riprovato).

**Stato**: Moduli 1, 2, 3 e 5 completi (contenuto + widget) e verificati meccanicamente.
Restano da costruire i widget di M4 (incluso lo shader GLSL/SDF di 4.5) e M6 — dati/asset
già pronti per entrambi.

## 2026-07-06/07 — Modulo 4 completo (lezione_04_reti_neurali.html), incluso lo shader GLSL/SDF

Sessione in modalità piano (piano approvato dall'utente, salvato in `~/.claude/plans/`), con
fase di esplorazione diretta (lettura di decision-log, next-steps, `struttura_moduli_1-6.md`
sezione Modulo 4, shell di `lezione_01_testo_come_dato.html`, i tre JSON di dati già pronti) e
un agente Plan dedicato a progettare in dettaglio l'infrastruttura WebGL/GLSL/SDF — il punto
esplicitamente più a rischio del modulo, prima eccezione al vanilla JS/Canvas/SVG del resto
del sito. Metodo di lavoro seguito come da piano: prima l'Unità 4.1 da sola (verificata
dall'utente su Desktop), poi 4.2/4.3 in autonomia, poi il widget shader per ultimo.

**Unità 4.1 — neurone singolo**: variante continua del calcolatore booleano di
`lezione_00a_funzioni_booleane.html`, slider per x1/x2/w1/w2/b, calcolo `sigma(w1x1+w2x2+b)`
dal vivo in JS (nessuna tabella precotta). Dati di riferimento in
`neurone_esempi_modulo4.json` verificati byte-per-byte e ricalcolati con motore JS reale.
Contenuto solo-testuale integrato nella stessa sezione del widget: Varela/Maturana
(autopoiesi, chiusura operazionale) in contrappunto a Bateson, collegato esplicitamente al
punto già presente in Blocco B.2 sui pesi che non "rappresentano" i dati in modo trasparente.

**Unità 4.2/4.3 — XOR**: su richiesta esplicita dell'utente, la griglia di decisione 100×100
di `xor_rete_modulo4.json` è resa come **heatmap continua** (non solo contorno), via
`canvas.putImageData` su un canvas offscreen iniettato come `data:` URL in un `<image>` SVG —
stessa tecnica di mappatura valore→colore già a basso rischio. Prima di scrivere il mapping
riga/colonna→coordinate, verificato con Python che la cella più vicina a ciascuno dei 4 punti
XOR noti riproducesse il valore atteso (~0.01/~0.99): confermato che l'indice di riga cresce
con `y` (nessuna inversione nei dati, l'inversione va fatta solo in fase di disegno per la
convenzione SVG). 4.2 mostra i 4 punti con un tentativo di retta che fallisce (illustrativo,
richiama verbatim l'aside "un certo modello del 1958" di `lezione_00a`); 4.3 mostra il
confine curvo reale della rete addestrata (4/4 corretto). Contenuto solo-testuale: pleroma/
creatura di Bateson (via Jung) come domanda esplicitamente aperta sulle rappresentazioni
astratte emergenti per strato.

**Unità 4.4/4.5 — superficie di perdita, shader GLSL/SDF**: implementata con successo,
**nessun fallback necessario**. Tecnica scelta (diversa dallo sphere-tracing SDF generico
proposto inizialmente, per minor rischio): ray-terrain intersection a passo fisso (80
passi) + bisezione di raffinamento (10 iterazioni), su un height-field WebGL con vista
prospettica inclinata (non piatta dall'alto) — camera con base look-at standard (forward/
right/up), luce direzionale fissa, colore terreno interpolato in funzione del valore di
loss nel punto colpito dal raggio. Minimappa 2D separata (Canvas 2D, heatmap calcolata dal
vivo con la stessa formula) per l'interazione di click (scelta del punto di partenza) — evita
il raycasting 3D→2D sulla vista prospettica. Discesa del gradiente calcolata dal vivo in JS
puro con la formula analitica del JSON, **verificata byte-per-byte** contro
`paesaggio_perdita_modulo4.json`: arrivo esatto sia al minimo globale da (0.9,0.3) sia al
minimo locale da (-0.65,-0.35), via motore JS reale (`osascript -l JavaScript`), risultati
identici ai valori Python di riferimento fino alle cifre decimali riportate nel JSON.

**Scoperta ambientale rilevante per le sessioni future**: il server di anteprima integrato,
fallito in tutte le sessioni precedenti (`PermissionError`/`getcwd: cannot access parent
directories`), è stato fatto funzionare in questa sessione con un workaround: uno script
Python minimale (`http.server.ThreadingHTTPServer` + `SimpleHTTPRequestHandler` con
`directory` passato direttamente, non tramite `-m http.server --directory` che chiama
`os.getcwd()` nel parsing degli argomenti e fallisce comunque) servito da una cartella
accessibile al processo sandboxato (la scratchpad di sessione), con i file copiati lì per
la preview. Questo ha permesso, per la prima volta nel progetto, di verificare i widget
**visivamente e interattivamente in un browser reale** durante la costruzione, non solo con
controlli strutturali offline. Grazie a questo, è stato trovato e corretto **un bug reale
nello shader**: gli argomenti di `smoothstep` per il decal della pallina erano invertiti
(`smoothstep(edge_alto, edge_basso, x)` invece di `smoothstep(edge_basso, edge_alto, x)`),
che su questa implementazione GLSL produceva `ring≈0` ovunque, colorando l'intero terreno
visibile del colore della pallina invece di mostrare il paesaggio — bug non rilevabile con i
soli controlli di sintassi JS/HTML, solo con rendering reale. Corretto (ordine degli argomenti
invertito, stesso fix per il glow), poi riverificato con screenshot e letture dirette dei
pixel via `gl.readPixels`. Verificata anche l'interazione di click sulla minimappa: partenza
scelta nel bacino del minimo locale converge correttamente e si blocca a loss≈0.4500,
partenza di default converge al minimo globale a loss≈0.0000 — entrambi i comportamenti
attesi, osservati dal vivo.

Contenuto solo-testuale di 4.5: backpropagation confrontata con la schismogenesi di Bateson
(*Naven*, 1936) e il termostato (feedback continuo/locale vs procedura offline/discreta/
globale, più vicina a un processo selettivo); memristor (1971/2008) e neuromorphic computing
(Loihi/TrueNorth) come corrispettivo hardware della plasticità, tenuto esplicitamente
distinto da EEG/BCI; domanda di chiusura del modulo (se ragionamento/conoscenza/
metacognizione condividono in un LLM lo stesso meccanismo di discesa del gradiente, è una
scoperta sulla loro natura anche biologica o un artefatto della costruzione della macchina)
lasciata esplicitamente aperta nel `.quadro` finale.

**Verifica meccanica finale**: sintassi JS con motore reale (`osascript -l JavaScript`) OK
sull'intero file; HTML ben formato (parser Python, tag bilanciati); 58 id, tutti univoci e
coincidenti con l'array `UNITS`; nessuna classe CSS (HTML o generata da JS) assente dal
proprio `<style>`; dati incorporati (`NEURON_DATA`, `XOR_DATA`, `LOSS_META`) confrontati
byte-per-byte con i tre JSON sorgente. File copiato su Desktop per la verifica visiva
complessiva dell'utente.

**Stato**: Moduli 1, 2, 3, 4 e 5 completi (contenuto + widget) e verificati sia
meccanicamente sia visivamente/interattivamente in browser reale. Resta da costruire il
Modulo 6 — dati/asset già pronti (`scala_modulo6.json`, `timeline_modulo6.json`,
`capacita_emergenti_modulo6.json`, `base_vs_tuned_modulo6.json`,
`quantizzazione_modulo6.json`).

## 2026-07-07 — Modulo 6 completo (lezione_06_large.html), chiusura dell'intero arco tecnico 1-6

Sessione in modalità piano (piano approvato dall'utente, salvato in `~/.claude/plans/`),
con una fase di esplorazione diretta (lettura di decision-log, next-steps,
`struttura_moduli_1-6.md` e `inventario_grafico_moduli_1-6.md` sezione Modulo 6, shell di
`lezione_01_testo_come_dato.html`, il blocco CSS della timeline in
`lezione_00_blocco_a.html`, i cinque JSON già pronti) e un agente Plan dedicato a
dettagliare la logica di ciascuno dei cinque widget prima dell'esecuzione. Metodo di
lavoro seguito come da istruzione ricevuta: prima l'Unità 6.1 da sola (verificata
dall'utente su Desktop dopo conferma esplicita "procedi"), poi 6.2-6.6 in un'unica
sessione di autonomia.

**Principio guida del modulo, diverso dagli altri**: interattività deliberatamente più
leggera, per non dare falsa certezza su fenomeni dibattuti (capacità emergenti) — nessuno
slider o controllo che permetta di alterare la curva di 6.2, nessuna animazione superflua.

**Unità 6.1 — scala**: slider su scala logaritmica (dominio 1e8-1e12), con funzioni
`sliderToValue`/`valueToSliderPos` reciprocamente inverse (verificato numericamente che
`valueToSliderPos(sliderToValue(x)) = x` esattamente su tutto il range con motore JS
reale) e i 4 punti di ancoraggio di `scala_modulo6.json` (Cervello umano 86 miliardi
neuroni, GPT-3 125M/175B parametri, PaLM 540B parametri) posizionati con la stessa
funzione di mappatura, mai hard-coded — tutti verificati caduti dentro `[0,1000]`. Nota di
cautela neuroni≠parametri resa come `.aside` fissa, non contestuale al valore corrente.

**Unità 6.2 — capacità emergenti**: grafico SVG disegnato via JS dagli 8 punti di
`capacita_emergenti_modulo6.json` (curva dichiarata esplicitamente come illustrativa, non
dati di un paper), asse Y fisso 0-1 (nessun auto-fit, onestà visiva), banda soglia
7e10-1.3e11 disegnata come rettangolo semitrasparente — verificato che tutti gli 8 punti
cadano dentro il viewBox e che la banda soglia cada esattamente tra il punto 5 (70
miliardi, accuratezza 0.15) e il punto 6 (130 miliardi, accuratezza 0.42), dove il salto
reale nei dati avviene. Nessuna interazione che permetta di alterare la curva — solo
didascalia permanente con le citazioni reali (Wei et al. 2022, critica di Schaeffer et
al. 2023, già citata in `lezione_00_blocco_b.html`). Sezione dedicata al dibattito aperto,
non solo un accenno.

**Unità 6.3 — dati/timeline**: le 4 voci di `timeline_modulo6.json` riusano verbatim le
classi CSS `.timeline`/`.tl-node`/`.tl-tag`/`.tl-date`/`.tl-title`/`.tl-desc` di
`lezione_00_blocco_a.html`, nessuno stile nuovo. Decisione esplicita di non usare
`tl-break` su nessun nodo (a differenza dell'uso originale in Blocco A, dove segnala un
fallimento/rottura) — qui l'arco storico è cumulativo, non ha rotture, e forzare quella
classe sarebbe stato un uso semanticamente scorretto.

**Unità 6.4/6.5 — fine-tuning e RLHF**: un'unica funzione di rendering (`initTuningWidget`)
montata due volte nel DOM (`tuning-widget-64`, `tuning-widget-65`) sullo stesso dato di
`base_vs_tuned_modulo6.json` (coppia fotosintesi), incorniciata diversamente nelle due
unità (istruzione-vs-pattern in 6.4, personalità/preferenze in 6.5) — nessuna duplicazione
di logica.

**Unità 6.6 — quantizzazione, chiusura dell'intero corso**: barra continua unica per
FP32 (stato "non ancora quantizzato", sempre reso come blocco unico indipendentemente da
qualunque mappa), che si spacca in blocchi via via più grandi e meno numerosi per
FP16/BF16 (12), INT8 (6), INT4 (4 bit → 3 blocchi) — mappa bit→segmenti dichiaratamente
non letterale, solo per leggibilità visiva, verificata monotona non-crescente tra i tre
livelli effettivamente quantizzati. Sezione dedicata alla domanda finale del corso
(discreto-fondamentale vs continuo-primitivo, con riferimento alla geometria differenziale
sintetica di Lawvere già emersa nella fase 1 di revisione della struttura testuale),
lasciata esplicitamente irrisolta. Chiusura dell'unità riscritta per chiudere l'intero
arco tecnico Moduli 1-6, non solo l'unità: nessun rimando a un'unità successiva.

**Refactoring minore in corsa**: la classe `.ptitle` (etichetta di titolo dei widget), che
in `lezione_01`/`lezione_02` risultava scoping-dipendente (`.playground .ptitle`, non
applicata quando riusata sotto contenitori diversi come `.rs-compare` — un'incoerenza
minore già presente e mai notata nei moduli precedenti), è stata qui definita come classe
generica di primo livello, riusabile identica da tutti e cinque i widget del modulo senza
duplicare la stessa regola CSS cinque volte. Nessuna modifica ai file dei moduli
precedenti, che restano come consegnati e già approvati.

**Verifica meccanica finale**: sintassi JS con motore reale (`osascript -l JavaScript`,
`new Function`) OK sull'intero file (verificata sia dopo il campione 6.1 sia dopo il file
completo); HTML ben formato (parser Python, tag bilanciati, zero errori); 46 id, tutti
univoci e coincidenti con l'array `UNITS`; nessuna classe CSS (HTML o generata da JS,
incluse le classi generate dentro template string con espressioni `${...}`) assente dal
proprio `<style>`; tutti i dati incorporati (`SCALA_DATA`, `EMERGENTI_DATA.punti`,
`TIMELINE_DATA`, `TUNING_DATA`, `QUANT_DATA`) confrontati byte-per-byte con i cinque JSON
sorgente — coincidenza esatta su tutti.

**Limite di sandbox confermato di nuovo**: il server di anteprima integrato resta
vincolato alla worktree della sessione corrente (`projects/`, non `qa-tool`) — stesso
limite già documentato nella sessione Blocco B/C. File copiato su Desktop per la verifica
visiva dell'utente, sia dopo il campione 6.1 (confermato dall'utente prima di procedere)
sia per il file completo. Creato anche `.claude/serve_lezioni.py` (ThreadingHTTPServer con
directory esplicita, stesso pattern già usato con successo in M4) e aggiornato
`.claude/launch.json` di conseguenza, per una futura sessione in cui il tool di anteprima
sia radicato correttamente nella worktree di `qa-tool`.

**Stato**: Modulo 6 completo (contenuto + widget) e verificato meccanicamente. Con questo,
**l'intero arco tecnico dei Moduli 1-6 del corso "Come funzionano gli LLM" è completo**
(contenuto + widget per tutti e sei i moduli). Verifica visiva finale in browser reale
lasciata all'utente. Prossimo passo naturale, non ancora richiesto: `corso-agenti/` e il
suo laboratorio, non toccato in questa sessione.

## 2026-07-07 — Pianificazione: revisione di tono, compilazione multilingua, tema chiaro/scuro

Dopo la conferma dell'utente sul Modulo 6 in browser, richiesta esplicita di tre lavori
collegati: (1) rendere il registro dell'intero corso più professionale/accademico e meno
pedagogico; (2) compilare un file unico autocontenuto con tutte le lezioni (00a/00b prima
dei Blocchi A-D, poi Moduli 1-6), indice iniziale, introduzione, e un tema chiaro accanto a
quello scuro esistente; (3) tradurre il tutto in inglese, francese e tedesco. Richiesta
esplicita dell'utente: produrre non il lavoro stesso ma **prompt di sessione ben scritti**
per farlo eseguire in autonomia in sessioni future — stesso schema già usato per M2/M4/M6/
M3-M5 (`docs/prompt-sessioni-widget-m2-m4-m6-m3m5.md`).

**Quattro decisioni chiarite esplicitamente con l'utente** (via domande mirate, tutte
risolte prima di scrivere i prompt):
- **Ambito della revisione di tono**: l'intero corso (12 file: 00a, 00b, Blocco A-D,
  Moduli 1-6), non solo i moduli tecnici — nonostante il Modulo 00 narrativo fosse già
  stato approvato più volte dall'utente in un registro diverso.
- **Widget nelle traduzioni**: l'utente ha scelto **nuovi dataset per lingua** (non solo
  prosa tradotta con widget invariati, non semplificazione) — implica ricostruire con lo
  stesso rigore già documentato per l'italiano (2026-07-06) tre dataset reali per ciascuna
  delle tre lingue: corpus BPE (M1), corpus n-grammi nativo (M2), vettori fastText reali
  con un nuovo esempio di polisemia verificato empiricamente (M3/M5) — non traduzioni
  meccaniche dei dati italiani esistenti. Segnalato esplicitamente all'utente che questo
  moltiplica per tre il lavoro di preparazione dati già fatto in italiano, non è una
  semplice traduzione di stringhe.
- **Fable**: nessuna restrizione di quota imposta nei prompt, nonostante l'utente avesse
  segnalato Fable al 17% di quota residua — usabile liberamente dove già previsto.
- **Tema chiaro**: la palette esatta non è decisa qui, la progetta la sessione esecutiva di
  Fase 2 — ma con l'obbligo, scritto nel prompt, di proporla all'utente per conferma visiva
  prima di considerarla definitiva (stesso principio di checkpoint già seguito per ogni
  altra decisione di design in questo progetto).

**Roadmap risultante, più grande del previsto**: non 5 sessioni ma **8**, perché ogni
lingua richiede due sessioni separate e dipendenti in sequenza (non la stessa unità di
lavoro divisa per comodità) — una che produce la traduzione della prosa e i corpora
linguistici nativi (nuove frasi scritte direttamente nella lingua target, non tradotte
dall'italiano, per il corpus n-grammi; il Modulo 00 tradotto come corpus di addestramento
BPE), una successiva che usa quell'output per ricostruire davvero i dataset (BPE, n-grammi,
embedding) e assemblare il file compilato di quella lingua. Segnalata esplicitamente
questa dimensione (~8 sessioni, comparabile in sforzo alle sessioni di preparazione dati
già registrate per M1/M2/M3/M5 in italiano, moltiplicate per tre lingue) prima di scrivere
i prompt in dettaglio; l'utente ha confermato di voler comunque tutto il roadmap scritto
subito, non solo le prime due fasi.

**Rischio tecnico principale segnalato nel prompt di Fase 2** (compilazione): ogni lezione
oggi ridichiara gli stessi nomi JS top-level (`const UNITS`, funzioni di navigazione) e
riusa id di sezione che ricominciano da capo in ogni file (`u1-apertura` in tutte le
lezioni) — concatenare 12 file così com'è produrrebbe `SyntaxError` da ridichiarazione e
collisioni di id. Il prompt istruisce esplicitamente una prova tecnica su solo 2 lezioni
prima di estendere a tutte e 12, e propone (senza deciderla al posto dell'utente) una
strategia di namespacing per capitolo.

**Consolidato in un nuovo file**, `docs/prompt-sessioni-revisione-traduzione-tema.md`,
sullo stesso modello di `prompt-sessioni-widget-m2-m4-m6-m3m5.md`: 8 prompt in sequenza
con dipendenze esplicite (Fase 1 → Fase 2 → per ciascuna lingua, parte a → parte b),
ciascuno con il proprio checkpoint di conferma sul primo campione dove il contenuto è
autoriale (revisione di tono, introduzione, tema chiaro) — non dove è ricostruzione
meccanica di dati già verificata con lo stesso metodo in italiano.

**Stato**: file di prompt scritto, non ancora eseguito. Nessuna sessione della nuova
roadmap è stata lanciata in questa sessione — solo la pianificazione. File non ancora
committato: da fare su richiesta esplicita, non automaticamente.

## 2026-07-07 — Fase 1 eseguita: revisione di tono su tutto il corso (IT)

Eseguito il Prompt 1 di `docs/prompt-sessioni-revisione-traduzione-tema.md`. Riscritta la
prosa (tag `<p>`, `<h1>`, `<h2>`, `<blockquote>`, `.aside p`, `.question`) di tutti e 12 i
file di `src/corso-llm/lezioni/` — Modulo 00 completo (00a, 00b, Blocchi A-D) e Moduli 1-6
tecnici — da un registro narrativo/pedagogico a uno professionale/accademico.

**Checkpoint di conferma**: campione di riferimento l'Unità 1.1 di
`lezione_01_testo_come_dato.html`, mostrato all'utente con prima/dopo testuale prima di
propagare la revisione. Confermato esplicitamente ("conferma, procedi in autonomia") prima
di procedere sugli altri 11 file, coerentemente con l'unica eccezione di checkpoint
prevista dal prompt (tutte le altre decisioni di design della roadmap — Fase 2 in poi —
restano delegate al mio giudizio, da documentare qui man mano).

**Registro applicato, in sintesi**: eliminato lo scaffolding didattico esplicito ("Provi
a...", "Osservi che...", "Tenga a mente...", domande retoriche dirette al lettore non
funzionali), sostituito con forme dichiarative, impersonale "si", o imperativo Lei asciutto
dove l'istruzione resta funzionale (interagire con un widget). Virgolette dritte `"..."`
attorno a termini o citazioni brevi convertite sistematicamente in caporali `«...»`, per
coerenza tipografica con il registro accademico. Nessun fatto, anno, nome, citazione o
numero alterato; nessuna domanda aperta del corso risolta (capacità emergenti 6.2, discreto
vs continuo 6.6, "sistema formale nel senso di Gödel" 1.5, e le altre già presenti sono
rimaste esplicitamente aperte).

**Osservazione emersa in corsa**: i moduli tecnici più recenti (in particolare
`lezione_04_reti_neurali.html` e, in misura minore, `lezione_05_transformer.html` e
`lezione_06_large.html`) erano già scritti, dalle sessioni precedenti, in un registro
vicino al target — uso già presente di caporali per alcune citazioni, forme impersonali,
pochissimo scaffolding esplicito. Per questi file l'intervento si è ridotto quasi
interamente alla conversione sistematica delle virgolette dritte residue e a pochi
aggiustamenti puntuali, non a una riscrittura estesa. Il Modulo 00 narrativo (Blocchi A-D)
e i Moduli 1-3 hanno richiesto interventi più estesi, essendo stati scritti in sessioni
precedenti con un tono più colloquiale.

**Verifica meccanica per ciascuno dei 12 file** (script scritti ad hoc per questa sessione,
non salvati nel repo — solo nello scratchpad di sessione): HTML ben formato (parser Python,
tag bilanciati); insieme e ordine degli `id` identici tra HEAD e la versione rivista;
blocchi `<script>` e `<style>` identici byte-per-byte (nessuna modifica accidentale a dati
incorporati, JS o CSS); sintassi JS verificata con motore reale (`osascript -l JavaScript`,
`new Function`) su ogni file. Esito: OK su tutti e 12 i file, nessuna regressione
strutturale.

**Attenzione prestata alle stringhe JS che duplicano prosa nei widget**: verificato caso per
caso (es. `lezione_02_probabilita.html`, dove il corpus e gli esempi n-grammi vivono in
`NGRAM_DATA`/`CALIBRAZIONE_DATA` dentro `<script>`) che nessuna stringa toccata nella prosa
HTML fosse duplicata anche nel JS — i dati incorporati restano quindi byte-per-byte
identici, come richiesto esplicitamente dal prompt.

**Stato**: Fase 1 completa e verificata su tutti i 12 file. Prossimo passo naturale (Fase 2
del roadmap): compilazione di `output/corso-llm-completo_it.html` — indice, introduzione,
navigazione a tre livelli, tema chiaro/scuro — con decisioni di design (architettura di
navigazione, palette del tema chiaro, testo dell'introduzione) da assumere in autonomia
secondo le istruzioni ricevute, documentandole qui.

## 2026-07-07 — Revisione del piano in corsa, a Fase 1 già completata

Prima di avviare la Fase 2, l'utente ha rivisto il piano su tre punti:

1. **Traduzioni rimandate**: le Fasi 3 (EN/FR/DE, prompt 3-8 del roadmap) restano previste
   ma non sono urgenti — rimandate a quando il resto del progetto sarà terminato. Annotato
   esplicitamente in `docs/prompt-sessioni-revisione-traduzione-tema.md` (blocco di nota
   sopra l'elenco della roadmap) per non lanciarle per errore in una sessione futura prima
   del momento giusto.
2. **Sostituzione nella pipeline odierna**: al posto delle traduzioni, la sessione odierna
   dedicherà un passo alla verifica del funzionamento dei widget di tutti i 12 file (ed
   eventuale correzione) — non ancora specificato nel dettaglio: l'utente darà le specifiche
   separatamente prima che io proceda.
3. Le altre istruzioni della sessione (autonomia sulle decisioni di design, checkpoint già
   superato, documentazione in decision-log/next-steps, commit per fase) restano invariate.

**Stato**: in attesa delle specifiche dell'utente sul passo di verifica/correzione widget.
Nessun lavoro di Fase 2 (compilazione del file unico) ancora iniziato — un primo tentativo
di scrivere lo script di compilazione era in corso quando è arrivata questa revisione del
piano, interrotto senza aver scritto alcun file (nessuno stato da ripulire).

## 2026-07-07 — Verifica interattiva dei widget di tutti i 12 file (senza Fable)

Su richiesta esplicita dell'utente, sospeso l'uso di Fable per questo compito (giudicato
sproporzionato per un lavoro di verifica/debug fatto di molti piccoli cicli — Fable resta
riservato, in questo progetto, alla costruzione di widget da specifica confermata, come in
M3/M5) — verifica e correzione fatte direttamente in conversazione. Pianificato in modalità
piano (vedi `~/.claude/plans/`),
poi eseguito.

**Ambito**: degli 8 file con widget interattivi reali (i 4 file di Blocco A-D non ne
contengono alcuno, solo prosa e timeline/tabelle statiche — confermato ed escluso).

**Ambiente di verifica dal vivo, funzionante questa volta**: workaround già noto (copia dei
file — inclusa `immagini_modulo1/`, per l'asset PNG referenziato — nella scratchpad di
sessione, server Python minimale `ThreadingHTTPServer`+`SimpleHTTPRequestHandler(directory=...)`,
`.claude/launch.json` creato nella sessione corrente puntato allo script) andato a buon fine
al primo tentativo — a differenza delle sessioni precedenti, questa volta senza fallback
necessario. Verifica quindi condotta con interazione reale in browser (click, digitazione,
lettura DOM/console/network) per ogni widget elencato nel piano.

**Un bug reale trovato e corretto** — `lezione_02_probabilita.html`, funzione condivisa
`creaWidgetNgram` (usata sia dallo slider 2.3 sia da quello 2.4): l'etichetta della finestra
di contesto pluralizzava in modo scorretto, producendo "parolae" invece di "parole" per
finestra > 1 (`` `${finestra} parola${finestra > 1 ? 'e' : ''}` `` concatenava "e" dopo
"parola" invece di sostituire la desinenza). Bug preesistente, non introdotto dalla
revisione di tono di Fase 1 (i blocchi `<script>` erano già stati verificati identici
byte-per-byte in quella fase). Corretto in
`` `${finestra} ${finestra > 1 ? 'parole' : 'parola'}` ``, riverificato dal vivo (label
corretta "1 parola"/"3 parole" su entrambi gli slider) prima di proseguire.

**Tutto il resto verificato corretto**, con alcuni casi che meritano nota per sessioni
future:
- **Modulo 1**: tokenizzazione BPE su tutti e 4 gli stadi corretta (id numerici confermati
  contro il vocabolario), asset PNG raster caricato correttamente (nessun 404), diagonale di
  Cantor coincidente col JSON. Osservazione non-bug: la tokenizzazione di "sul" produce un
  token separatore di fine-parola isolato (il carattere "·", id 33) invece di fondersi con
  "l" — comportamento legittimo del tokenizzatore appreso, non un difetto del widget.
- **Modulo 2**: predittore n-grammi corretto su tutti gli stadi (valori coincidenti col
  JSON), diagramma di calibrazione corretto sui tre bucket (valori coincidenti).
- **Modulo 3**: mappa embedding corretta nelle tre modalità (esplorazione, aritmetica —
  incluso un ricalcolo con combinazione diversa da quella di default, principe−uomo+donna→
  principessa — polisemia, valori di similarità coincidenti col documentato 0.62/0.44).
- **Modulo 4**: neurone e XOR (heatmap) corretti (pattern a scacchiera coerente con la
  tavola di verità XOR, verificato leggendo i pixel del canvas offscreen). Superficie di
  perdita WebGL: **verificata con lettura diretta dei pixel via `gl.readPixels`** (stesso
  metodo che in una sessione precedente aveva trovato il bug reale dello smoothstep) — colori
  coerenti con la formula della loss, nessun contesto perso, ordine degli argomenti di
  `smoothstep` ancora corretto (il fix di quella sessione non è regredito). Discesa del
  gradiente osservata dal vivo convergere correttamente al minimo globale dopo il reset
  (loss≈0.024). **Nota tecnica per sessioni future**: durante questa verifica
  `document.visibilityState` è diventato `"hidden"` per la scheda (causa non identificata
  con certezza, sospetta un'interazione con `preview_resize`), il che sospende
  `requestAnimationFrame` per *qualunque* codice della pagina, non solo per questo widget —
  confermato con un contatore rAF indipendente che non incrementava. Non è un difetto del
  sito: la discesa del gradiente era già stata osservata funzionare correttamente prima che
  lo stato cambiasse. Da tenere presente: se in una sessione futura un widget basato su
  `requestAnimationFrame` sembra "bloccato" senza errori in console, controllare prima
  `document.visibilityState` prima di sospettare un bug nel codice.
- **Modulo 5**: widget attention corretto in tutte e 4 le riletture (5.2/5.3 condiviso, 5.4
  con spostamento animato del punto "calcio" nella minimappa in base al contesto, 5.5
  multi-head con pesi che cambiano coerentemente tra teste). Widget di codifica posizionale
  (shuffle/reset) corretto.
- **Modulo 6**: slider di scala corretto (verificato anche matematicamente il calcolo
  dell'àncora più vicina), timeline e grafico capacità emergenti coerenti coi dati, barra di
  quantizzazione corretta (12/6/3 segmenti, monotona), entrambe le istanze del toggle
  base/tuned e prima/dopo-RLHF corrette.

**Nota metodologica sul tool di anteprima** (rilevante per sessioni future): `preview_click`
non ha registrato correttamente il click in due casi — un cerchio SVG cliccabile (diagramma
di calibrazione, Modulo 2) e un bottone dopo il cambio di stato di visibilità della pagina
(shuffle posizionale, Modulo 5) — mentre `element.dispatchEvent(new MouseEvent('click',
{bubbles:true}))` via `preview_eval` ha sempre funzionato. In entrambi i casi era un limite
del tool di simulazione del click, non un bug del sito (verificato leggendo lo stato JS
sottostante). Analogamente, il widget toggle base/tuned (Modulo 6) usa un `setTimeout(120ms)`
per il fade del testo mentre la classe `active` del bottone cambia subito — leggere il testo
troppo presto dopo un click dà un falso positivo di "contenuto non aggiornato": aspettare
almeno ~200ms dopo il click prima di leggere `.textContent` in test futuri di widget con
transizioni di opacità.

**Verifica meccanica finale**: rilanciati su tutti e 12 i file gli stessi controlli della
Fase 1 (HTML ben formato, id invariati, `<script>`/`<style>` identici byte-per-byte tranne
la riga corretta in `lezione_02`, sintassi JS con motore reale) — OK ovunque, nessuna
regressione. File copiati su Desktop per la verifica visiva dell'utente (stesso limite di
sempre: la worktree servita per l'anteprima è quella di sessione, non `qa-tool`, ma stavolta
il workaround scratchpad ha coperto la verifica interattiva stessa, non solo l'apertura
finale).

**Stato**: verifica completa, un bug corretto, nessun altro problema reale trovato. Fase 2
(compilazione del file unico) resta sospesa, da riprendere su richiesta esplicita.

## 2026-07-07 — Fase 2 eseguita: compilazione output/corso-llm-completo_it.html

Eseguito il Prompt 2 di `docs/prompt-sessioni-revisione-traduzione-tema.md`. A differenza
delle istruzioni originali del prompt, l'utente ha delegato in questa sessione le tre
decisioni di design (architettura di navigazione, testo dell'introduzione, palette del
tema chiaro) alla mia autonomia, da documentare qui senza fermarmi ad attendere conferma —
resta invece obbligatoria, come da prompt, la prova tecnica di namespacing su 2 lezioni
prima di estendere a tutte e 12.

**Correzione alla coppia di prova indicata nel prompt**: il prompt originale suggeriva
00a+00b per la prova tecnica, ma questi due file sono entrambi pagine a un solo livello
(solo `<nav class="rail">`, nessun `topbar`/`unit-tab`/array `UNITS`) — quel pattern esiste
solo nei 10 file "multi-unità" (Blocco A-D e Moduli 1-6). Una prova su 00a+00b non avrebbe
esercitato la collisione più rilevante segnalata dal prompt stesso (`const UNITS`,
`function setActiveUnit`/`renderRail` ridichiarati identici in ogni file multi-unità). Ho
scelto **00a + lezione_01** come coppia di prova, per coprire entrambe le strutture
realmente presenti nei 12 file.

**Decisione 1 — Architettura di navigazione a tre livelli**: Opzione A (barra fissa di
selezione capitolo, 12 voci + "Indice", sopra l'attuale coppia topbar-unità/rail-sezioni di
ciascun capitolo, che ne sostituisce il contenuto al cambio capitolo). Scartata l'Opzione B
(indice laterale sempre visibile con l'intera gerarchia) perché avrebbe richiesto un
componente nuovo con comportamento responsive da progettare da zero, mentre l'Opzione A
estende meccanicamente un pattern a due livelli già scritto, verificato e responsive in
tutti i 10 file multi-unità. Per 00a/00b (senza `UNITS`), la barra di livello 2 resta
assente, si passa direttamente dalla barra capitoli al rail di sezione.

**Decisione 2 — Palette del tema chiaro**: prima proposta (sfondo `#F5F0E6`, un beige/sabbia
neutro) corretta su segnalazione esplicita dell'utente ("il tema chiaro dovrebbe utilizzare
gli stessi colori del tema scuro ma in rapporti di contrasto diversi, quindi il colore
sabbia/avorio non va bene"). Palette rifatta derivando `--bg`/`--surface`/`--surface-2` come
tinte chiare della STESSA tonalità verde (~162°) di `--bg` del tema scuro (`#0F2A22`), non
da una famiglia di colori neutra estranea; `--text` del tema chiaro riusa esattamente il
valore esadecimale di `--bg` del tema scuro (stesso swatch, ruolo invertito); `--copper`/
`--copper-bright` restano nella stessa tinta rame del tema scuro, solo scuriti per il
contrasto su sfondo chiaro. Valori finali: `--bg:#F0F5F3`, `--surface:#E0EBE8`,
`--surface-2:#CDDFDA`, `--text:#0F2A22`, `--text-dim:#326253`, `--copper:#804C1E`,
`--copper-bright:#6D3D0D`. Contrasti verificati con la formula di luminanza relativa WCAG
(calcolo Python): tutte le coppie testo/sfondo superano AA (4.5:1) anche nel caso peggiore
(testo su surface-2, 5.04:1), la maggior parte supera AAA. Toggle con persistenza
`localStorage`, default `dark`.

**Decisione 3 — Introduzione**: testo originale di ~360 parole (posizione del corso,
struttura in due parti — Modulo 0 narrativo e Moduli 1-6 tecnici —, il filo discreto/
continuo come chiave di lettura trasversale, il principio dei componenti interattivi
verificati su dati reali). Inserito nella sezione "Indice" del file compilato, non
sottoposto a conferma preventiva per istruzione esplicita dell'utente.

**Architettura tecnica di namespacing**: per ciascun capitolo, slug breve (`c00a`, `c00b`,
`cba`..`cbd`, `cm1`..`cm6`). Ogni capitolo avvolto in `<section class="chapter"
id="chapter-{slug}" data-chapter="{slug}" hidden>`; lo script di ciascun capitolo avvolto in
una IIFE che referenzia il proprio contenitore (`chapterRoot`) per le query di shell
condivise (`.unit-tab`, `.rail`, `.unit-block`, `.reveal`) invece di `document` — risolve la
ridichiarazione di `const UNITS`/`function setActiveUnit` tra capitoli. CSS: un solo blocco
`:root{}` globale (i valori dei design token sono risultati identici byte-per-byte in tutti
i 12 file) + un solo `:root[data-theme="light"]{}`; il resto della CSS di ciascun capitolo
resta non scoped e concatenato verbatim (verificato che le classi specifiche dei widget non
collidono tra capitoli con significati diversi — unica eccezione nota, `.ptitle` generica in
M6 vs `.playground .ptitle`/`.neuron-box .ptitle` scoped altrove, innocua per specificità
CSS più alta delle regole scoped). Script di build: `src/corso-llm/build_output.py`, lasciato
come asset riutilizzabile del progetto (non file di scratch) perché le Fasi 3 (EN/FR/DE)
dovranno seguire la stessa architettura di namespacing/navigazione/tema.

**Tre bug reali trovati e corretti durante la compilazione** (non nei file sorgente, che
restano intatti — bug introdotti dalla prima versione del meccanismo di namespacing stesso,
tutti trovati con verifica meccanica sistematica prima della consegna, non lasciati alla
verifica visiva):

1. **Collisione id/class**: alcuni elementi (es. `id="cantor-grid" class="cantor-grid"` in
   lezione_01) riusano deliberatamente lo stesso nome come id e come classe CSS. La prima
   versione del prefixing (sostituzione di qualunque token tra apici coincidente con un id
   noto) prefissava per errore anche il valore di `class="..."`, disallineandolo dalla
   regola CSS (rimasta senza prefisso) e rompendo lo stile. Risolto mascherando gli attributi
   `class="..."` prima della sostituzione e ripristinandoli invariati dopo.
2. **Riferimenti id in forme sintattiche non previste**: un primo tentativo con un elenco
   chiuso di contesti noti (`id="X"`, `getElementById('X')`, `id:'X'`, `data-target="X"`) si
   è rivelato incompleto — il codebase referenzia gli id anche come chiavi di configurazione
   che finiscono in "Id" (`inputId:`, `barsId:`, `sliderValId:` nel widget n-grammi di M2),
   come argomenti posizionali passati a funzioni (`setLight('outAND', 'valAND', and)` in
   00a), e come selettori CSS `#id` incorporati in stringhe più ampie
   (`querySelectorAll('#u3-sez-markov .pg-example-btn')`, `'#m5-head-tabs .at-tab'` in M5).
   Ciascuno di questi, se non prefissato, produceva un riferimento id "orfano" che causava
   un'eccezione JS non gestita al primo widget del capitolo, interrompendo silenziosamente
   l'esecuzione di **tutto lo script del capitolo e di tutti i capitoli successivi nello
   stesso tag `<script>`** (le istruzioni top-level dopo un'eccezione non gestita non vengono
   eseguite) — motivo per cui un singolo riferimento rotto in M2 bloccava anche M3-M6.
   Risolto abbandonando l'elenco chiuso di contesti a favore di una sostituzione universale
   (qualunque occorrenza tra apici o dopo `#` che coincide esattamente con un id noto, ovunque
   compaia) con la sola eccezione mascherata di `class="..."`. Verificato con una scansione
   sistematica di tutti i `getElementById`, i selettori `#id` e i campi `*Id:`/`id:` del
   documento compilato contro l'insieme reale degli id: zero riferimenti orfani residui.
3. **Timing di `IntersectionObserver` su capitoli nascosti**: gli `IntersectionObserver` di
   ciascun capitolo (rail-dot attivo, fade-in `.reveal`, unit-tab attivo) vengono creati
   mentre il capitolo è ancora `hidden` (tutti tranne "Indice" lo sono al caricamento). Il
   passaggio da `hidden` a visibile al cambio capitolo non fa scattare da solo il ricalcolo
   dell'intersezione in modo affidabile — bug non di sintassi ma di tempistica, diagnosticato
   escludendo prima un'eccezione JS (nessuna, verificato avvolgendo temporaneamente ogni IIFE
   di capitolo in try/catch con cattura dell'errore in una variabile globale, dato che il
   tool di anteprima non intercetta le eccezioni non gestite nei log console) e osservando poi
   che un piccolo scroll manuale (`scrollBy(0,1)` seguito da `scrollBy(0,-1)`) risolveva
   sempre lo stato. Corretto in `showChapter()`: dopo aver mostrato il capitolo, un piccolo
   delta di scroll reale (sincrono + su `requestAnimationFrame` + dopo 60ms, per coprire
   diverse tempistiche di layout) forza il ricalcolo di tutti gli observer del capitolo
   appena mostrato.

**Verifica meccanica finale**: sintassi JS con motore reale (`osascript -l JavaScript`, `new
Function`) sull'intero documento compilato; HTML ben formato (parser Python, tag bilanciati);
440 id nel documento, tutti univoci; scansione sistematica di `getElementById`/selettori
`#id`/campi `*Id:` senza riferimenti orfani; tutti i 13 dataset incorporati (BPE, Cantor,
n-grammi, calibrazione, embedding, attention, neurone, XOR, scala, timeline, capacità
emergenti, tuning, quantizzazione) confrontati byte-per-byte con le rispettive costanti nei
12 file sorgente originali (non con i JSON grezzi, che in alcuni casi includono metadata mai
incorporato nel widget) — coincidenza esatta ovunque.

**Verifica interattiva in browser reale** (workaround scratchpad+server, stesso pattern già
noto): confermati cambio capitolo su tutti e 12, cambio unità con sincronizzazione
rail-dot/unit-tab dentro almeno 3 capitoli multi-unità dopo click reali (non solo simulati),
calcolatore booleano di 00a, widget n-grammi di M2 (quello del bug #2), mappa embedding di
M3, elementi del widget shader WebGL di M4 tutti correttamente namespaced e senza errori
console, toggle tema chiaro/scuro con persistenza dopo reload, palette del tema chiaro
corretta visivamente su più capitoli (nessun beige/sabbia residuo). **Limite di verifica
segnalato per onestà**: in questa sessione `document.visibilityState` è rimasto
persistentemente `"hidden"` nel tool di anteprima (stesso limite già documentato nella
sessione di verifica interattiva precedente per lo shader WebGL di M4, lì risolto in un
momento di visibilità normale) — impedisce di confermare in modo affidabile, IN QUESTA
SESSIONE, che il fix del bug #3 (stato attivo del rail-dot) scatti sempre al primo cambio
capitolo; la logica del fix è comunque verificata corretta nei momenti in cui la visibilità
era normale, e nessun utente reale ha mai una tab genuinamente "hidden" mentre interagisce.
Da confermare con un'osservazione rapida in un browser reale dell'utente.

File compilato copiato su Desktop (`corso-llm-completo_it.html`) per la verifica visiva
finale dell'utente. Script di build (`src/corso-llm/build_output.py`) e file compilato
(`output/corso-llm-completo_it.html`) non ancora committati in questa voce — commit a fine
sessione dopo l'aggiornamento di next-steps.md, come da istruzione del prompt.

**Stato**: Fase 2 completa, verificata meccanicamente e interattivamente (con la riserva
sopra su un solo aspetto cosmetico). Prossimo passo naturale: Fase 3 (traduzioni EN/FR/DE),
rimandata su richiesta esplicita dell'utente fino a data da destinarsi.

**Quarto bug segnalato dall'utente dopo la consegna e corretto**: il widget "Raster e
vettoriale" dell'Unità 1.4 (confronto cerchio raster/SVG con slider di zoom) non funzionava
nel file compilato — l'immagine `<img src="immagini_modulo1/cerchio_raster_24px.png">` in
`lezione_01_testo_come_dato.html` usa un percorso relativo alla cartella `lezioni/` (dove il
file sorgente vive), ma il file compilato vive in `output/`, quindi lo stesso percorso
relativo non risolveva più allo stesso file (404, confermato anche nei log di rete durante
la verifica interattiva di questa stessa sessione, non notato allora come sintomo di un
problema separato). Unico asset con questo pattern in tutti e 12 i file (verificato con
grep su tutti i `src="..."` non-data/non-http). Risolto in `build_output.py` con una nuova
funzione (`inline_relative_assets`) che, durante l'estrazione di ciascun capitolo, incorpora
come `data:` URI base64 ogni asset referenziato con percorso relativo (risolto contro
`lezioni/`, non contro `output/`) — coerente con l'obiettivo del file compilato di essere
autocontenuto, e protegge anche eventuali asset analoghi che compariranno nelle future
compilazioni EN/FR/DE. Verificato: `naturalWidth` dell'immagine 24px, `complete: true`,
nessun riferimento `immagini_modulo1/` residuo nel compilato, slider di zoom funzionante dal
vivo in browser reale (24×24 → 74×74px, 3.1×). File ricopiato su Desktop.

## 2026-07-07 — Rifiniture del tema chiaro segnalate dall'utente dopo la consegna

Quattro widget avevano colori incorporati staticamente (non reattivi alle variabili CSS del
tema), residuo del fatto che sono stati costruiti prima che esistesse un tema chiaro:
funzionavano correttamente nel solo tema scuro perché i valori incorporati coincidevano per
costruzione con la palette scura, ma restavano fissi (scuri) anche passando al tema chiaro.

1. **Unità 1.4 (`lezione_01_testo_come_dato.html`), riquadro SVG del confronto
   raster/vettoriale**: lo sfondo del riquadro SVG era un `<rect fill="#0F2A22">` incorporato
   via JS (colore letterale, non `var(--bg)`), mentre il riquadro raster accanto usa già
   `background: var(--bg)` in CSS — in tema chiaro il primo restava scuro, il secondo
   diventava chiaro, rompendo la simmetria visiva del confronto. Corretto in
   `style="fill:var(--bg)"` (il cerchio arancione resta a colore fisso, per restare
   visivamente lo stesso cerchio del PNG raster accanto, che non cambia con il tema).
2. **Unità 4.3 (`lezione_04_reti_neurali.html`), heatmap continua del confine XOR**: i colori
   dell'interpolazione (`bg`/`bright`) erano array RGB incorporati (`[15,42,34]`,
   `[240,168,94]`, cioè `--bg`/`--copper-bright` del tema scuro scritti a mano), quindi
   l'immagine PNG generata via `canvas.putImageData` restava sempre quella scura. Corretto
   leggendo `--bg`/`--copper-bright` dal tema corrente via `getComputedStyle` al momento del
   rendering (nuove funzioni `themeVarHex`/`hexToRgbArr`), e ri-generando l'immagine
   all'evento `corso:themechange` (nuovo evento globale, disparato dal toggle tema in
   `build_output.py`, a cui ogni widget con contenuto pre-renderizzato può iscriversi).
3. **Unità 4.5, minimappa 2D dello sfondo di perdita**: stesso pattern del punto 2
   (`lossComputeMinimapBg`) più i colori del marcatore di posizione (`lossUpdateMinimap`,
   `fillStyle` incorporato). Stessa correzione: lettura dinamica delle variabili di tema,
   ricalcolo dello sfondo della minimappa all'evento `corso:themechange` (la costante
   `lossMinimapBg` è diventata `let` per permetterne la riassegnazione).
4. **Unità 4.5, shader WebGL/SDF del paesaggio della perdita**: i colori del cielo, del
   terreno (gradiente basso→alto lungo la superficie di perdita) e della pallina erano
   costanti `vec3(...)` scritte direttamente nel sorgente GLSL. Convertiti in `uniform vec3`
   (`uSkyTop`, `uSkyBot`, `uDeep`, `uMid`, `uBright`, `uBallColor`), impostati ad ogni frame
   in `lossRenderLoop` da una tabella JS a due voci (`LOSS_SHADER_PALETTE.dark`/`.light`) in
   base a `document.documentElement.dataset.theme` — nessun bisogno dell'evento
   `corso:themechange` qui, dato che il valore viene riletto naturalmente ad ogni frame del
   render loop. **Decisione di design esplicita, non una semplice sostituzione meccanica**:
   la palette del tema chiaro per questo widget NON riusa `--bg`/`--copper-bright` del tema
   chiaro (scuriti apposta per il contrasto testo-su-sfondo, troppo spenti per restare
   leggibili come rilievo 3D) — usa una palette dedicata pensata per la resa del terreno, con
   il rapporto chiaro/scuro invertito rispetto al tema scuro: nel tema scuro il minimo
   (`deep`) è scuro (si confonde col cielo scuro) e il massimo/pallina sono chiari per
   risaltare; nel tema chiaro il minimo resta chiaro (si confonde col cielo chiaro) e il
   massimo/pallina diventano scuri e saturi per risaltare sul terreno chiaro — stessa logica
   di leggibilità, contrasto invertito coerentemente col resto del tema.

**Verifica**: rebuild completo, nessuna regressione (440 id univoci, zero riferimenti orfani,
HTML ben formato, sintassi JS reale OK). Verificato in browser reale con lettura diretta dei
pixel (non solo screenshot, per lo stesso motivo già documentato per il fix precedente dello
shader): PNG dell'heatmap XOR decodificato via canvas — angoli (239,244,241)≈`--bg` chiaro,
centro (110,63,16)≈`--copper-bright` chiaro; `gl.readPixels` sul canvas WebGL — cielo
(237,243,240) in tema chiaro vs (17,45,36) in tema scuro dopo aver commutato
`data-theme`/disparato `corso:themechange` manualmente, confermando sia la correttezza dei
nuovi valori sia l'assenza di regressioni sul tema scuro. File ricopiato su Desktop.

## 2026-08-29 — "Strato 2": riscritti i riferimenti a Blocco/Modulo 00 nel corpo del testo

Completato il lavoro rimandato il 28 agosto (indice in tre Parti, numerazione decimale,
"corso"→"saggio interattivo" nelle etichette — vedi `next-steps.md`, nessuna voce di
decision-log per quella sessione). Riscritti a mano i ~24 punti nel corpo delle quattro
lezioni di Genealogia dove "Blocco A/B/C/D" o "Modulo 00/0 tecnico" comparivano dentro frasi
vere e proprie: non ridenominazione meccanica, ma verifica del contenuto reale di ogni
rimando prima di riscriverlo, per evitare di puntare al modulo sbagliato.

**Metodo**: per ogni cross-reference, letto il testo reale del modulo o dell'unità citata
(non assunta la corrispondenza 1:1 tra vecchia lettera e nuovo numero) prima di scegliere la
formula sostitutiva. Due correzioni di rotta emerse solo leggendo il contenuto:

1. In `lezione_00_blocco_c.html`, gran parte dei rimandi "il Blocco B" che sembravano
   puntare a unità diverse (2.1, 2.2...) puntano in realtà quasi tutti alla stessa unità,
   **Genealogia · 2.3** ("Cosa non sanno fare affatto") — grounding, causalità,
   composizionalità e apprendimento continuo sono tutte sotto-sezioni di quell'unica unità,
   non unità separate. Solo il rimando di chiusura più ampio (ex "Il Blocco B chiedeva,
   nella sua forma più radicale...", che cita anche la metacognizione discussa altrove in
   Genealogia · 2) è rimasto un riferimento all'intero modulo **Genealogia · 2**, non a una
   sotto-unità.
2. In `lezione_00_blocco_a.html` riga 301 (non nell'elenco originale del 28 agosto, trovato
   rileggendo il file per intero): "manca solo l'hardware — nel senso più letterale del
   Modulo 0 tecnico" si riferiva in realtà a **Fondamenti · 2** ("Hardware e software"), non
   a Meccanismo — un caso in cui il vecchio nome "Modulo 0 tecnico" indicava qualcosa di più
   specifico del semplice "arco tecnico" a cui punta lo stesso termine altrove
   (`lezione_00_blocco_d.html`, dove invece la sostituzione corretta è **Meccanismo**).

**Convenzione adottata per le formule sostitutive**: nomi di Parte (Fondamenti, Genealogia,
Meccanismo) usati senza articolo, come già stabilito nell'introduzione — mai
"il/la Genealogia". Riferimento a un'unità specifica nella forma decimale già usata nei
kicker (`Genealogia · 2.3`), riferimento all'intero modulo nella forma senza decimale
(`Genealogia · 2`). Dove il testo originale usava "questo blocco" o "Nodo N" come
terminologia interna descrittiva (non un rimando al vecchio nome ufficiale) — es. "i quattro
nodi di questo blocco" in `lezione_00_blocco_c.html` — lasciato invariato: non fa parte del
problema (non nomina la vecchia struttura), resta corretto anche nella nuova numerazione.

**Scoperta collaterale, non risolta in questa sessione**: durante la verifica ho trovato
molte altre occorrenze non catalogate della parola "corso" (minuscola, non "saggio
interattivo") nel corpo di queste quattro lezioni — almeno 19 in `lezione_00_blocco_a.html`
da sola, poche in b/c/d — mai toccate dal passaggio "corso"→"saggio interattivo" del 28
agosto (che ha coperto solo etichette strutturali + un paio di menzioni in
`lezione_00a`/`00b`). Ho corretto solo le occorrenze di "corso" nelle frasi già riscritte per
Blocco/Modulo (per non lasciare incoerenza fianco a fianco), non le altre: fuori dallo scope
di oggi, segnalato in `next-steps.md` come lavoro a sé.

**Verifica**: rebuild completo (`build_output.py`, nessun errore), sintassi JS reale OK su
tutti e 4 i file (`osascript -l JavaScript`), HTML ben bilanciato (parser Python dedicato,
nessun tag orfano/mismatch). Verificato nel file compilato che nessuno dei quattro capitoli
di Genealogia contiene più "Blocco A/B/C/D" o "Modulo 00"/"Modulo 0 tecnico" (letto
`innerText` di ogni capitolo via browser reale, non solo grep sul sorgente). Verifica visiva
di massima in browser fatta; lettura approfondita riga per riga lasciata all'utente.

## 2026-08-30 — Indice ad accordion per Genealogia · 1, dopo un primo tentativo scartato

Il 28 agosto era stato costruito, dentro `lezione_00_blocco_a.html`, un primo prototipo di
colonna sinistra al posto della topbar orizzontale ("Option B") — piatto, senza le altre
Parti visibili. Presentato all'utente, giudicato non corrispondente a quanto immaginato:
voleva l'indice completo (Fondamenti/Genealogia/Meccanismo) sempre leggibile, con i moduli
che si aprono al click per rivelare le unità, le sezioni annidate sotto l'unità attiva. Su
sua richiesta esplicita, quel primo tentativo è stato costruito da capo come campione
**separato**, senza toccare il file vero (in una cartella di bozze separata),
verificato e approvato.

**Oggi, su richiesta esplicita dell'utente ("il nuovo indice che mi è piaciuto deve stare in
qa-tool"), portato dentro il file vero**, con due decisioni di scope confermate dall'utente
prima di iniziare: (1) solo Genealogia 1 per ora, le altre 11 lezioni restano invariate; (2)
la chapterbar globale sparisce del tutto mentre Genealogia 1 è attiva — la sidebar diventa
l'unica navigazione, anche verso gli altri capitoli.

**Il tentativo "Option B" è stato rimosso per intero** (variabile `--unit-nav-w`, lo scoping
CSS piatto, il markup dei bottoni della topbar con i titoli in `<span>`) — non conservato,
per esplicita indicazione dell'utente ("si può anche dimenticare"). Verificato con grep che
non ne resta traccia.

**La sidebar vera** riusa senza riscriverlo il meccanismo già esistente e già funzionante
(`UNITS`, `renderRail`, `unitSpy`, click-to-scroll) — solo il contenitore visivo cambia, da
topbar+rail separati a un albero unico. La navigazione verso gli altri capitoli passa da
`window.showChapter(slug)`, già esposto globalmente e già usato altrove nel sito (i bottoni
del Sommario) — nessun meccanismo nuovo, solo un nuovo chiamante. La chapterbar sparisce/
riappare tramite `body:has(#chapter-cba:not([hidden])) .chapterbar{display:none}` — stesso
schema `:has()` già usato in questo file per il repadding di `main`, esteso per la prima
volta alla chapterbar stessa (mai fatto altrove nel progetto). Tutto scoped dietro
`@media (min-width:900px)`: sotto quella soglia Genealogia 1 si comporta come ogni altro
capitolo, nessun lavoro aggiuntivo per il mobile in questo primo passo.

**Un bug reale trovato in fase di build, non in verifica visiva**: `build_output.py` usa
`scope_shell_queries()` per riscrivere in modo sicuro alcune query condivise (es.
`document.querySelectorAll('.unit-tab')` → `chapterRoot.querySelectorAll(...)`) tramite
corrispondenza testuale esatta su righe note. Includere anche i bottoni della sidebar nella
stessa riga (`'.unit-tab, .unita-viva'`) ha rotto quel pattern e fatto fallire la build con
un errore chiaro. Risolto tenendo `tabs` (topbar) e `sidebarTabs` (sidebar) come query
separate — `.unita-viva` è un nome di classe esclusivo di questo file, non condiviso da
altri capitoli, quindi non necessita dello scoping automatico — e factorizzando la riga di
scroll in una funzione `goToUnit(t)` condivisa, così la sostituzione testuale del builder
continua a trovarla una sola volta.

**Verifica**: build completa senza errori; navigazione avanti e indietro testata dal vivo fra
Genealogia 1 e Genealogia 2 (chapterbar/sidebar si scambiano correttamente ogni volta); click
su un'unità (1.4) verificato — scroll, stato attivo su topbar e sidebar, pallini di sezione
tutti corretti; nessuna regressione su due capitoli non toccati (`c00a`, `cm3`) — chapterbar/
topbar/rail identici a prima del cambiamento; comportamento mobile (<900px) confermato
invariato per Genealogia 1; zero errori console in tutta la sessione di prova.

**Nota nota, non un difetto**: il pulsante tema chiaro/scuro vive dentro la chapterbar
globale — mentre Genealogia 1 è attiva (desktop) non è raggiungibile. Il tema già scelto
resta applicato, solo non cambiabile da lì. Non affrontato in questa sessione.

**Correzione di rotta, stesso giorno**: l'utente ha fatto notare che aprendo
`lezione_00_blocco_a.html` da sola (la modalità di lavoro primaria per i file in `src/`,
non il file compilato) la sidebar non compariva affatto — lo scoping `#chapter-cba` usato
sopra esiste solo dopo la compilazione, quindi tutta la sidebar era invisibile fuori da
`output/`. Un primo tentativo di correggerlo (togliere lo scoping dalle sole classi
esclusive di questo file) non ha centrato il punto: l'utente voleva che l'indice fosse un
**file a sé** dentro `src/corso-llm/lezioni/`, non qualcosa di incorporato nella lezione,
per restare coerente con il principio "tutto in `src/`, ricomponibile quando e come
vogliamo" — la cartella `output/` è un artefatto derivato, non deve essere l'unico posto
dove una funzionalità è raggiungibile.

**Rifatto di conseguenza**: `lezione_00_blocco_a.html` riportata esattamente allo stato
di fine Strato 2 (sidebar rimossa per intero, non solo lo scoping). Il menu è ora
`src/corso-llm/lezioni/indice.html`, file indipendente: tre Parti sempre leggibili,
accordion nativo `<details>/<summary>` (zero JavaScript) per Genealogia/Meccanismo, ogni
voce un link reale (`<a href="lezione_00_blocco_a.html#unit-a1">`, verificato che ogni
lezione multi-unità espone id di unità indirizzabili dall'esterno — schema per lettera in
Genealogia, `u1..uN` in Meccanismo) fino all'unità esatta, nessun contenuto duplicato.
Verificato dal vivo: link cliccato apre la lezione vera all'ancora giusta e il meccanismo
di quella lezione (invariato) riconosce da solo l'unità attiva; accordion nativo apre e
chiude senza errori; zero regressioni, perché blocco_a.html è tornata bit per bit
identica a prima di questo intero esperimento.

## 2026-09-02 — Revisione editoriale completa, rinomina in saggio/, sidebar unica nel compilato, estrazione in repository proprio

Sessione lunga, in continuità con "Strato 2" del 29 agosto. Cinque blocchi di lavoro,
in ordine:

**1. Revisione editoriale sistematica di Genealogia e Meccanismo.** Applicando le regole
di `docs/editorial-guidelines.md` (titoli come soggetto grammaticale, verifica citazioni),
usati 10 subagenti in parallelo (uno per file) per una prima ricognizione, poi corretti a
mano ~50 costrutti tipo "Genealogia · 2 mostra che..." in soggetto neutro ("In Genealogia ·
2.2..."). Verifica web mirata su ~20 citazioni storiche/filosofiche (Peirce/Wittgenstein/
Post 1921, Hebb, McCulloch, AI winter, Firth, Word2Vec, Bateson/*Naven*, Chomsky, Wei et
al. 2022): due errori reali trovati e corretti — la frase "neurons that fire together, wire
together" era attribuita direttamente a Hebb 1949 tra virgolette, ma è una parafrasi
coniata decenni dopo da Carla Shatz; il titolo professionale di McCulloch corretto da
"neuroscienziato" (anacronistico per il 1943) a "neurofisiologo". Una citazione (Bacone/
Bayle, "Veritas/Error filius temporis") non verificabile con fonti reperibili online,
lasciata dopo conferma esplicita dell'utente di averla già verificata lui stesso.

**2. Riferimenti "Blocco X"/"Modulo 0" obsoleti in tutto il saggio.** La numerazione interna
di Genealogia era già stata rinominata da "Blocco A/B/C/D" a "Genealogia · 1-4" in kicker/
footer/sidebar, ma non nel testo prosa. Un Explore agent ha mappato ogni occorrenza
(~30 "Blocco X", 11 "Modulo 0/00" riferiti a Fondamenti, 3 "Modulo 00" riferiti al corpus
di Genealogia nel suo insieme) contro la "verità corrente" di ciascun file. Corrette tutte,
con scelte esplicite dell'utente: i riferimenti a Fondamenti risolti nella label corretta
(Fondamenti · 1/2); i 3 riferimenti al corpus di Genealogia riscritti descrittivamente
("il testo dei quattro blocchi di Genealogia"), senza inventare una sigla ufficiale che non
esiste.

**3. Rinomina di `lezioni/` in `saggio/` e dei 12 file.** Il sito non è più un corso a
lezioni numerate ma un saggio in tre Parti — l'utente ha chiesto di allineare anche i nomi
dei file, non solo i titoli visibili. Nuovi nomi con slug brevi (`fondamenti-1-funzioni-
booleane.html`, `genealogia-1-disputa.html`, `meccanismo-3-embedding.html`, ecc.),
`git mv` per preservare la storia, script di sostituzione per i ~740 riferimenti interni
(sidebar duplicata in ogni file + link puntuali). `piano_corso_llm.md`,
`struttura_moduli_1-6.md` e gli altri file di pianificazione in `src/` NON rinominati
(deliberato — registrano la logica reale con cui il lavoro è stato creato, non vanno
riscritti a posteriori per combaciare col naming finale).

**4. Sidebar unica condivisa nel documento compilato.** La rigenerazione di
`output/corso-llm-completo_it.html` era bloccata da mesi: `scope_shell_queries` in
`build_output.py` cercava ancora pattern JS della vecchia navigazione (`.rail`, `.unit-tab`,
`.rail-dot`) rimossi dal refactor della sidebar di fine agosto. Corretto ai pattern attuali.
Verificando visivamente il risultato, emerso un problema più profondo: ogni capitolo
compilato mostrava la propria sidebar sorgente duplicata per intero, con link verso file
separati inesistenti nel contesto a pagina singola. Sostituita con un'unica sidebar
condivisa (`build_shared_sidebar()`), i cui link passano da `showChapter()` invece che da
file; stato "corrente" e scroll-spy dinamici via JS. La vecchia barra dei capitoli in alto
rimossa su scelta esplicita dell'utente — la sidebar è ora l'unica navigazione, ovunque,
coerente con `saggio/`.

**5. Estrazione in repository proprio, `~/projects/corso-llm/`.** Il progetto vive fin qui
dentro `qa-tool/`, insieme a corso-agenti e al capstone-qualitativo — ma non condivide
nulla con loro. Proposta di architettura basata sul template di
`memoria/governance_new_projects.md`, discussa e approvata dall'utente con due decisioni
esplicite: preservare la storia git (via `git filter-repo`, non un repository ripartito da
zero — la storia di 41 commit, ridotta a 31 pertinenti dopo il filtro, resta consultabile
con `git log`/`git blame`) e lasciare `src/corso-llm/` ancora presente dentro `qa-tool/`
per ora, non cancellato subito. `src/corso-llm/` appiattito in `src/` nel nuovo
repository (non serve più l'annidamento con un solo progetto per repo) — richiesto un fix
di `OUTPUT_DIR` in `build_output.py` (un livello di annidamento in meno, il path risaliva
troppo in alto), verificato producendo un output byte-identico a quello pre-estrazione.
`docs/decision-log.md` e `docs/next-steps.md` non trasferibili con `git filter-repo` (sono
log condivisi con altri progetti, appesi nello stesso file nel tempo): estratti a mano,
solo le voci pertinenti a corso-llm, in un'unica revisione — perdono quindi il blame
per-voce che il resto del repository mantiene.

## 2026-09-02 — Rinomina in cartografia-semantica

Il repository nasce come `corso-llm` (nome ereditato da `qa-tool`), ma non è più un
corso — è un saggio interattivo. Rinominato in `cartografia-semantica`, richiamando il
sottotitolo del saggio ("cartografia della conoscenza tra spazio vettoriale e grafo") e
il nome già usato dall'export di Claude Design (`Cartografia semantica dei LLM.zip`, in
`assets/`), invece di ripetere il titolo per esteso o inventare un termine nuovo. Nomi
proposti in alternativa e scartati: `dal-bit-alle-entita-semantiche` (troppo lungo come
nome di cartella), `saggio-semantico`, `bit-a-grafo`. Aggiornati i riferimenti al nome
del progetto in `CLAUDE.md`, `README.md`, `docs/snapshot.md` — non toccati i nomi di file
interni che restano legittimamente `corso-llm-*` (es. `output/corso-llm-completo_it.html`),
non facenti parte dell'identità del repository.

## 2026-09-03 — Rivista la decisione sul nome del file compilato

La voce precedente lasciava deliberatamente `output/corso-llm-completo_it.html`
invariato, non essendo parte dell'identità del repository. Nel worktree
`parte-iii-widget-design-0a34f3`, lavorando alla stessa cosa in parallelo senza
conoscere questa nota (non ancora committata su `main`), l'utente ha chiesto
esplicitamente di rinominarlo comunque, in `dal-bit-alle-entita-semantiche_it.html`
— lo stesso nome scartato il giorno prima per il repository perché "troppo lungo
come nome di cartella", ma qui è il nome di un file, non di una cartella, e il
vincolo non si applica. Decisione confermata e mantenuta: il file resta
coerente col resto del rename (titolo del saggio, non più "corso"), anche se
questo significa che la nota di ieri non descrive più lo stato attuale del
repository. Riferimenti aggiornati in `CLAUDE.md`, `README.md`,
`docs/next-steps.md`, `docs/snapshot.md` e nei prompt di sessione EN/FR/DE non
ancora lanciati (`docs/prompt-sessioni-revisione-traduzione-tema.md`).
