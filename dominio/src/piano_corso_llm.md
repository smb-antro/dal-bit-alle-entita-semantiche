# Corso: Come funzionano i Large Language Model
### Piano didattico — versione di lavoro

**Destinatari**: studenti universitari preparati, provenienti da discipline non-STEM (nessuna conoscenza pregressa di matematica, informatica, programmazione)

**Obiettivo**: comprensione genuina del *come funzionano* gli LLM — non solo del *cosa fanno* — con collegamenti espliciti a linguistica, filosofia, scienze cognitive, neuroscienze

**Metodo**: approccio induttivo e socratico. Si parte da esempi concreti e domande, non da definizioni. Si dà per scontato nulla. Le connessioni interdisciplinari sono nominate esplicitamente, non lasciate implicite. Le domande senza risposta restano aperte — non si forza una falsa risoluzione.

---

## Struttura generale — 7 moduli

```
Modulo 0  │ Fondamenti già noti
          │ Booleana, binario, hardware/software
          │ "Il computer non capisce niente"

Modulo 1  │ Il testo come dato
          │ Rappresentazione delle parole, token, encoding

Modulo 2  │ Probabilità e linguaggio
          │ "Qual è la prossima parola più probabile?"
          │ Modelli n-gram, catene di Markov
          │ → il primo "modello linguistico" ingenuo

Modulo 3  │ Parole come punti nello spazio
          │ Vettori, embedding, similarità
          │ "Re - Uomo + Donna = Regina" come fenomeno, non magia

Modulo 4  │ Reti neurali
          │ Il neurone artificiale, strati, addestramento
          │ Funzione di perdita, intuizione del gradiente

Modulo 5  │ Il Transformer
          │ Attention mechanism
          │ Perché l'attenzione risolve ciò che prima non si risolveva
          │ Architettura ad alto livello

Modulo 6  │ Cosa significa "Large"
          │ Scala, dati, parametri, capacità emergenti
          │ Fine-tuning e RLHF

Modulo 7  │ Limiti e fraintendimenti
          │ Allucinazione, ragionamento, confidenza non calibrata
```

**Nota di metodo**: i moduli 1-6 spiegano la meccanica. Il modulo 7 confluisce nel Modulo 00, espanso come introduzione narrativa — non come chiusura tecnica. Si entra dal limite e dal dubbio, non dal trionfo.

---

## Modulo 00 — Introduzione narrativa (espanso in 4 blocchi)

Il Modulo 00 non spiega meccanismi. Racconta una storia, mappa un territorio di domande aperte, e pianta dei semi che germinano nei moduli successivi. Ogni blocco termina con domande esplicitamente irrisolte, che vengono riprese più avanti nel corso.

---

### Blocco A — La storia come sequenza di problemi irrisolti

**Filo narrativo**: ogni epoca dell'AI ha fallito per lo stesso motivo strutturale — ha sottovalutato la distanza tra la rappresentazione di un problema e il problema stesso. Ogni "inverno" è una crisi di modello del mondo, non di fondi.

**Tappe**:

1. **Il sogno di Leibniz** (XVII sec.) — *Characteristica Universalis*: il pensiero come calcolo
2. **Boole, Frege, Russell** (XIX-XX sec.) — il sogno diventa matematica formale; *Principia Mathematica* (1910)
3. **Gödel rompe tutto** (1931) — teorema di incompletezza: nessun sistema formale abbastanza potente può dimostrare tutte le proposizioni vere che contiene. *Primo inverno, prima ancora del computer.*
4. **Turing reincornicia la domanda** (1936, 1950) — non "il pensiero è calcolo?" ma "una macchina può imitarlo abbastanza bene da ingannare un osservatore?"
5. **Nasce l'AI — e si sopravvaluta** (1956, Dartmouth) — McCarthy, Minsky, Shannon; previsioni entusiastiche, successi limitati
6. **Il Perceptron e la sua caduta** (1958–1969) — Rosenblatt; poi Minsky e Papert (1969) dimostrano l'incapacità di risolvere lo XOR. *Primo vero inverno dell'AI.*
7. **I sistemi esperti** (anni '70-'80) — approccio simbolico, regole scritte da umani; funzionano in domini chiusi, falliscono per *brittleness*. *Secondo inverno.*
8. **La rivincita statistica** (anni '90) — Hidden Markov Models, Support Vector Machines; pattern estratti dai dati invece che codificati
9. **Il ritorno delle reti neurali, con la scala** (2006, Hinton) — il backpropagation esisteva dagli anni '80, ma serviva scala
10. **Le parole diventano vettori** (2013, Word2Vec) — "Re - uomo + donna = regina"
11. **L'attenzione, poi il Transformer** (2015–2017) — "Attention is All You Need" (2017): l'architettura sotto tutti gli LLM attuali

**Domande aperte che emergono (→ Blocco C)**:
- Un LLM è un sistema formale nel senso di Gödel?
- Cosa ha cambiato, esattamente, la profondità nelle reti neurali?
- Gli LLM sono sistemi esperti molto più grandi, o c'è una differenza qualitativa?

---

### Blocco B — I limiti attuali come mappa del territorio inesplorato

**Filo narrativo**: gli LLM sono funzioni da testo a testo. Il mondo non è testo. Tutto il resto discende da qui.

**Parte 1 — Cosa sanno fare davvero** (prima di criticare, riconoscere cosa è straordinario e perché non è del tutto compreso)
- Completamento statistico a scala massiva
- In-context learning (capacità non prevista prima che emergesse)
- Transfer cross-dominio
- Capacità emergenti al crescere della scala

**Parte 2 — Cosa simulano di saper fare**
- *Ragionamento*: il modello interpola, non deduce; fallisce su problemi banali fuori distribuzione
- *Conoscenza*: nessuna rappresentazione separata e verificabile dei fatti — tutto compresso in pesi statistici. L'allucinazione non è un bug: è il comportamento atteso di un sistema senza accesso a una fonte di verità
- *Metacognizione*: "non lo so" è una stringa di testo come un'altra, non una stima calibrata dell'incertezza

**Parte 3 — Cosa non sanno fare affatto**
- *Grounding* (Harnad, 1990): i simboli non si riferiscono a niente nel mondo
- *Ragionamento causale* (Pearl): correlazione appresa, non modello causale degli interventi e dei controfattuali
- *Generalizzazione composizionale*: forte dentro la distribuzione di training, debole fuori
- *Apprendimento continuo*: pesi statici, nessun aggiornamento dall'esperienza conversazionale

**Domande aperte che emergono (→ Blocco C)**:
- Il grounding richiede un corpo, o basta un modello del mondo sufficientemente ricco?
- Il ragionamento causale può emergere dal linguaggio con l'architettura giusta?
- La generalizzazione composizionale illimitata è esclusiva del biologico?
- Un sistema a pesi fissi può essere "intelligente" in qualsiasi senso utile?
- Tolti grounding, causalità, apprendimento continuo, metacognizione calibrata — cosa resta dell'intelligenza?

---

### Blocco C — Perché ci vuole un villaggio

**Filo narrativo**: ogni domanda aperta dei blocchi precedenti indica esattamente quale disciplina manca al tavolo.

**Nodo 1 — Il problema del significato** *(filosofia del linguaggio, linguistica, semiotica)*
- Frege: senso vs riferimento
- Wittgenstein tardivo: significato come uso in pratiche sociali condivise
- Searle, la stanza cinese (1980): manipolazione sintattica senza contenuto semantico
- Domanda aperta: un modello addestrato su testo umano partecipa in modo derivato a quelle pratiche, o ne è solo uno specchio?

**Nodo 2 — Il problema della causalità** *(statistica, epistemologia, scienze cognitive)*
- La scala causale di Pearl: associazione → intervento → controfattuale
- Gli LLM operano quasi solo al primo livello
- Connessione con Hume: se anche gli umani inferiscono la causalità invece di osservarla, in cosa differisce il processo umano da quello statistico?

**Nodo 3 — Il problema biologico** *(neuroscienze, biologia computazionale)*
- Cosa è stato preso dal biologico: McCulloch-Pitts (1943), Hebb (1949), organizzazione gerarchica della corteccia visiva
- Cosa è stato abbandonato: il backpropagation non è biologicamente plausibile; i neuroni biologici lavorano con spike temporali; la plasticità è continua e locale, non discesa del gradiente globale
- Cosa insegna il biologico che l'ingegneria ha ignorato: efficienza (20W contro megawatt), apprendimento paucisample, consolidamento e dimenticanza attivi
- Ricerca attiva: spiking neural networks, few-shot learning, architetture ispirate alla corteccia prefrontale

**Nodo 4 — Il problema della coscienza** *(filosofia della mente, neuroscienze, fisica teorica)*
- Chalmers: problema facile (meccanismi) vs problema difficile (esperienza soggettiva)
- Integrated Information Theory (Tononi): Φ come misura, intrattabile per sistemi grandi
- Global Workspace Theory (Baars, Dehaene): analogia superficiale con l'attenzione dei transformer — probabilmente fuorviante
- Higher-Order Theories: rappresentazioni di secondo ordine — un LLM che genera testo *su* testo basta?
- Punto pedagogico: queste teorie sono programmi di ricerca falsificabili, non speculazione pura. L'AI fornisce modelli controllabili per testarle.

**Tabella riassuntiva dei gap come programma multidisciplinare**:

| Gap | Discipline coinvolte | Applicazioni se risolto |
|---|---|---|
| Grounding | Filosofia, linguistica, robotica | Sistemi che capiscono, non solo parlano |
| Causalità | Statistica, epidemiologia, scienze cognitive | AI scientifica affidabile, diagnosi medica |
| Efficienza biologica | Neuroscienze, fisica | AI accessibile, su dispositivi piccoli |
| Apprendimento continuo | Biologia, psicologia cognitiva | Sistemi che si adattano senza riaddestrare |
| Composizionalità | Linguistica formale, logica | Generalizzazione fuori distribuzione |
| Coscienza/esperienza | Filosofia della mente, neuroscienze, fisica | Comprensione dell'intelligenza stessa |

**Chiusura del blocco**: studiare i limiti degli LLM è studiare, per contrasto, cosa siamo — perché non sappiamo ancora bene come funziona il linguaggio umano, la causalità, la generalizzazione, la coscienza.

---

### Blocco D — Lo spazio, il corpo, la macchina

**Filo narrativo**: tutta la cognizione umana è cognizione di un animale con un corpo, che si muove, cade, ha fame, afferra oggetti — evoluto in un ambiente fisico per milioni di anni. Un LLM non ha mai avuto fame, non è mai caduto, non ha mai allungato una mano.

**Sezione 1 — Cos'è lo spazio? (Non è ovvio)**
- Newton: spazio come contenitore assoluto
- Kant: spazio come forma dell'intuizione, non del mondo
- Merleau-Ponty: spazio vissuto attraverso il corpo — "destra" e "sinistra" esistono perché ho una mano destra e una sinistra

**Sezione 2 — Il corpo come strumento di misura**
- Il bicchiere: vicino perché posso allungare il braccio; davanti perché ho una faccia orientata; piccolo perché confrontato con la mia mano
- Le illusioni ottiche come prova che la percezione è costruttiva, non passiva — il cervello genera un'ipotesi compatibile con i segnali, non riceve un'immagine (Bayesian brain)
- Domanda: se la percezione umana è già costruzione, in cosa differisce da quella di una macchina?

**Sezione 3 — Cosa vede la macchina, quale corpo abita**
- *Computer vision*: matrice di pixel, coordinate in millimetri — nessun punto di vista, nessun vicino/lontano motorio
- *Robot*: corpo limitato e definito, spazio propriocettivo rudimentale, loop sensorimotor chiuso ma povero (pochi gradi di libertà, nessun sistema vestibolare)
- *Claude*: non abita nessuno spazio. Conosce "vicino" solo come token coerente con altri token. Il suo "corpo", se vogliamo usare la parola, è il corpus di testo di addestramento — un corpo di linguaggio, non di materia

**Sezione 4 — Il gap sensorimotor come gap cognitivo**
- Rodney Brooks (anni '80): l'intelligenza forse non richiede rappresentazioni simboliche, richiede corpi — origine della robotica embodied
- Connessione con Blocco B: il grounding mancante è in larga parte grounding sensorimotor
- Lakoff e Johnson: le metafore concettuali hanno origine sensorimotoria ("capire è afferrare", "il futuro è davanti a noi")
- L'apprendimento paucisample dei bambini è embodied, non testuale

**Domanda di chiusura, aperta**: dotare un LLM di un corpo (sensori, attuatori, loop sensorimotor) lo renderebbe più intelligente, o il problema è nell'architettura stessa, non integrabile con quel tipo di informazione?

**Posizionamento**: il Blocco D funge da raccordo diretto al Modulo 0 tecnico (hardware/software) — il corpo fisico di Claude (data center, GPU) è il primo caso concreto su cui applicare le domande appena poste.

---

## Lezione 00 — Hardware e Software: il corpo e la voce di Claude

*Prima lezione tecnica del corso, sviluppata per intero. Approccio: zoom-out progressivo dall'esperienza dello studente fino al transistor, poi risalita fino al concetto di software.*

### Apertura — Il momento zero
Gli studenti mandano un messaggio a Claude e osservano l'attesa di pochi secondi. Domanda: *cosa è successo, fisicamente, in quei secondi?* Le risposte saranno vaghe ("il computer elabora") — l'intera lezione è lo smontaggio di questa vaghezza.

### Strato 1 — Cosa è Claude?
Non un robot, non una mente — una funzione: `Input: testo → [?] → Output: testo`. Il centro resta scatola nera (verrà riempito nei moduli successivi). Si fissa solo: Claude è software che gira su hardware.

### Strato 2 — Dove vive Claude?
Il messaggio viaggia fino a un **data center**: un capannone pieno di server, raffreddato attivamente, che consuma quanto una piccola città.
*[Immagine: file server rack in un data center]*

Questo è il corpo di Claude — fisico, localizzato, soggetto a termodinamica, ma senza posizione soggettiva né sensori sul mondo. Contrasto utile: cervello umano ~20W; infrastruttura di un modello come Claude, ordini di grandezza superiori. Aggancio diretto al Nodo 3 del Blocco C (efficienza biologica).

### Strato 3 — Su cosa gira Claude? CPU vs GPU
**CPU** = un chirurgo esperto: poche operazioni complesse, in sequenza, alta precisione.
**GPU** = migliaia di operai: operazioni semplici, tutte in parallelo.
*[Immagine: die shot di una GPU al microscopio]*

Le reti neurali sono moltiplicazioni di matrici — milioni di operazioni semplici e indipendenti: esattamente il lavoro per cui la GPU è fatta.

Nota storica da rendere esplicita: le GPU non sono nate per l'AI, ma per i videogiochi. Quando i ricercatori hanno notato che la stessa architettura per renderizzare pixel in parallelo serviva anche per addestrare reti neurali, si è sbloccato qualcosa che era già pronto, in attesa di essere riconosciuto. Aggancio al Blocco A: a volte il pezzo mancante non è una nuova invenzione, ma il riconoscimento che qualcosa di esistente risolve un problema diverso da quello per cui è nato.

### Strato 4 — Cosa fa l'hardware, fisicamente? (riconnessione alle funzioni booleane)
Un **transistor** è un interruttore: passa corrente o non passa, 1 o 0.
*[Immagine: wafer di silicio al microscopio]*

Una GPU moderna contiene decine di miliardi di transistor. Combinati, implementano i gate logici AND, OR, NOT — la realizzazione fisica delle tavole di verità già costruite a mano nella lezione precedente.

```
Transistor (interruttore fisico)
    → Gate logici (AND, OR, NOT — cablati)
    → Circuiti (sommatori, moltiplicatori)
    → Unità aritmetica
    → Istruzioni macchina
    → CUDA / driver GPU
    → PyTorch
    → Il modello neurale di Claude
```

Punto pedagogico centrale: la funzione F = (A E B) O (NON A), costruita a mano, è letteralmente cablata in forma fisica dentro ogni transistor della GPU — non è metafora, è la stessa cosa a una diversa scala.

### Strato 5 — Hardware vs Software: la distinzione finale
**Hardware**: il fisico — cambia lentamente, ha massa, consuma energia.
**Software**: le istruzioni — si copia a costo zero, non ha peso, esiste solo perché un hardware lo esegue.

Precisazione anti-fraintendimento: il software non fa nulla che l'hardware non possa fisicamente fare. L'intelligenza di Claude, in fondo, è una cascata di accensioni e spegnimenti di transistor, ripetuta miliardi di miliardi di volte.

### Chiusura — Il paradosso pedagogico
Claude descritto come funzione testo-a-testo, implementata in moltiplicazioni di matrici, eseguita da transistor in un capannone che consuma quanto una città. Niente in questa descrizione sembra intelligente. Eppure il risultato, in certi contesti, lo è — o lo sembra. Il paradosso resta aperto, da riprendere in ogni modulo successivo.

---

## Stato di avanzamento

**Piano dei contenuti** (narrativa, analogie, domande aperte — quanto scritto sopra in questo file):

- [x] Struttura generale a 7 moduli
- [x] Modulo 00 — Blocco A (storia)
- [x] Modulo 00 — Blocco B (limiti)
- [x] Modulo 00 — Blocco C (interdisciplinarità)
- [x] Modulo 00 — Blocco D (spazio e corpo)
- [ ] Moduli 1-6 (meccanica tecnica) — piano dei contenuti da scrivere
- [ ] Eventuale modulo tecnico di approfondimento su gate logici / progettazione digitale (rimandato, se necessario)

**Sviluppo HTML** (lezioni interattive in `lezioni/`, sviluppate su branch/worktree `corso-llm-moduli-1-6`):

- [x] Lezione 00.A — Funzioni booleane
- [x] Lezione 00 — Hardware e software (sviluppata per intero, con immagini)
- [x] Modulo 00 — Blocco A, Unità A.1-A.6 (`lezione_00_blocco_a.html`, file unico con navigazione a due livelli)
- [x] Modulo 00 — Blocco B, Unità B.1-B.3 (`lezione_00_blocco_b.html`, stesso shell, 3 unità una per parte)
- [x] Modulo 00 — Blocco C, Unità C.1-C.5 (`lezione_00_blocco_c.html`, stesso shell + chip disciplinari + tabella dei gap in C.5)
- [x] Modulo 00 — Blocco D, Unità D.1-D.2 (`lezione_00_blocco_d.html`, stesso shell, 2 unità; D.2 chiude anche l'intero Modulo 00 narrativo con raccordo al Modulo 0 tecnico)
- [ ] Moduli 1-6 — da sviluppare, piano dei contenuti ancora da scrivere (Modulo 00 narrativo A-D completo)
