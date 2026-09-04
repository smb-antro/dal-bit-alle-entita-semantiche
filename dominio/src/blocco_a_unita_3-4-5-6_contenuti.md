# Blocco A — Unità A.3, A.4, A.5, A.6
### Contenuti per conversione HTML (Claude Code)

---

## Nota di convenzione (leggere prima di convertire)

Questo file contiene il testo integrale delle quattro unità mancanti, pensato per essere trasferito nel template HTML già stabilito in A.1 e A.2 (palette circuit-board, Space Grotesk + Source Serif 4 + IBM Plex Mono, rail di scroll-spy, reveal-on-scroll). Convenzioni usate qui sotto e relativa classe CSS di destinazione:

- `**[ASIDE: etichetta]**` seguito da un paragrafo → blocco `.aside` con `.label`
- `**[QUESTION]**` seguito da un paragrafo → blocco `.question`
- Blocchi `>` a fine sezione "Il quadro" → `.timeline` con nodi `.tl-node` (pieno = costruzione, vuoto = rottura, usare il modificatore `.crack` già introdotto in A.2 — vedi legenda `.tl-legend`)
- Il blocco finale di ogni unità in corsivo/quote → `blockquote` nella sezione `.chiusura`
- Ogni unità = un file HTML a sé, identico impianto CSS delle precedenti due

A.6 chiude l'intero Blocco A: oltre alla propria timeline locale, propongo un riepilogo timeline dell'intero blocco (tutte le tappe da Leibniz al Transformer) come elemento visivo capstone — segnalato più sotto.

---
---

## Unità A.3 — Euforia e primo schianto pratico

**Kicker**: Modulo 00 · Blocco A · Unità 3
**Tappe**: Dartmouth (1956) · Il Perceptron (1958) · Minsky e Papert (1969)

### Apertura

Immagini una proposta di ricerca che comincia dichiarando che il problema è, in sostanza, già risolto in linea di principio — resta solo da metterlo per iscritto in un modo che una macchina possa eseguire. Non è ironia retrospettiva: è, con qualche parafrasi, il tono reale della proposta che nell'estate del 1956 riunisce un gruppo di ricercatori a Dartmouth College, e che dà per la prima volta un nome al campo di cui questo corso si occupa.

Notare la sequenza temporale, perché conta: cinque anni prima Lucas non ha ancora scritto una riga contro il meccanicismo. La rottura filosofica dell'Unità 2 e l'euforia ingegneristica di questa unità corrono, per un tratto, fianco a fianco — non in fila indiana.

### Tappa 1 · 1956 — Dartmouth: nasce un nome, non ancora un campo

John McCarthy, insieme a Marvin Minsky, Claude Shannon e Nathaniel Rochester, firma la proposta che convoca l'incontro — ed è McCarthy a coniare, in quella proposta, l'espressione "intelligenza artificiale". La tesi di fondo, parafrasata: ogni aspetto dell'apprendimento e ogni altro tratto dell'intelligenza può, in linea di principio, essere descritto con tale precisione da permettere a una macchina di simularlo.

Vale la pena leggerla due volte. Non dice "forse". Dice "può", con la sicurezza di chi sta descrivendo un problema di ingegneria, non un mistero aperto.

**[ASIDE: quello che è successo davvero, quell'estate]** L'incontro dura circa due mesi, i partecipanti sono una decina, i progressi concreti sono modesti rispetto alle attese dichiarate. Quello che resta, in modo duraturo, non è un risultato tecnico ma un nome — e un gruppo di persone che, da quel momento, si riconoscono come appartenenti allo stesso campo.

### Tappa 2 · 1958 — Il Perceptron: la macchina che impara guardando

Frank Rosenblatt costruisce il Perceptron, ispirandosi al modello matematico del neurone di McCulloch e Pitts (1943) — un dispositivo capace di *imparare* a classificare pattern semplici regolando i propri pesi in base agli esempi che riceve, invece di eseguire regole scritte a mano. È la prima incarnazione pratica e visibile di un'idea che tornerà, sotto altro nome e con altra scala, in ogni rete neurale di questo corso.

La stampa dell'epoca non si trattiene. Il New York Times, nel 1958, riporta che secondo la Marina degli Stati Uniti il dispositivo sarebbe diventato capace di <span class="mono">"walk, talk, see, write, reproduce itself and be conscious of its existence"</span> — camminare, parlare, vedere, scrivere, riprodursi ed essere cosciente della propria esistenza.

**[ASIDE: da tenere a mente]** Il Perceptron di Rosenblatt, nella sua forma del 1958, è a un solo strato. Sa separare solo pattern che si possono dividere con una linea retta — la nozione tecnica è "separabilità lineare". Tenga in mente questo dettaglio: nella prossima tappa diventa l'intera storia.

### Tappa 3 · 1969 — Minsky e Papert: il conto che nessuno aveva fatto

Undici anni dopo, Marvin Minsky — lo stesso nome che compare nella proposta di Dartmouth — pubblica con Seymour Papert un libro dal titolo asciutto, *Perceptrons*. Contiene una dimostrazione matematica rigorosa: un Perceptron a un solo strato non può calcolare la funzione XOR — esattamente l'operatore che ha già incontrato in Lezione 00.A, con un avviso lasciato lì apposta per questo momento.

Il motivo è geometrico, non un dettaglio implementativo: gli esempi in cui XOR è vero e quelli in cui è falso non si possono separare con una singola linea retta. Nessuna quantità di addestramento aggiuntivo risolve il problema — è un limite strutturale del modello a un solo strato, non un difetto correggibile con più dati.

**[ASIDE: un dettaglio che complica la storia standard]** Minsky e Papert, nello stesso libro, riconoscono che uno strato aggiuntivo risolverebbe il problema in linea di principio — ma congetturano, sbagliando, che estensioni multistrato avrebbero sofferto di limiti simili. In più: nel 1969 non esisteva ancora un algoritmo capace di addestrare efficacemente una rete a più strati. Il libro non ha "ucciso" le reti neurali da solo — la ricerca connessionista era già in difficoltà da anni per ragioni di finanziamento e di risultati; alcuni storici della disciplina considerano il ruolo del libro nella vicenda più mitologico che causale. Resta, comunque, il momento in cui il pubblico smette di crederci.

**[QUESTION]** Una macchina lodata dalla stampa come capace, in prospettiva, di essere cosciente della propria esistenza non riesce a calcolare una funzione a due variabili che ha già padroneggiato manipolando due interruttori. Tenga in tasca questo scarto tra promessa e limite: tornerà, con proporzioni diverse, ogni volta che nel corso si parlerà di capacità emergenti e dei loro confini reali.

### Il quadro

Legenda: nodo pieno = costruzione, nodo vuoto = rottura.

- **1956** — Dartmouth: nasce il nome "intelligenza artificiale", con aspettative che il campo impiegherà decenni a onorare. *(costruzione)*
- **1958** — Rosenblatt: il Perceptron, prima macchina che impara dai dati invece di eseguire regole. *(costruzione)*
- **1969** — Minsky e Papert: il Perceptron a uno strato non risolve XOR — limite geometrico, non correggibile con più addestramento. *(rottura)*

**[QUESTION]** Lo schema costruzione-rottura, già visto nell'Unità 2 con Gödel-Turing-Lucas, si ripete qui con protagonisti diversi — e con un dettaglio in comune sorprendente: in entrambi i casi, chi scrive la rottura (Gödel, Minsky) lo fa con gli stessi strumenti concettuali di chi aveva costruito il sogno. Vale la pena chiedersi se sia un caso, o se ogni programma abbastanza ambizioso porti in sé i mezzi della propria confutazione.

### Chiusura

> Nel 1958 un giornale nazionale prometteva una macchina cosciente della propria esistenza. Undici anni dopo, la stessa comunità scientifica ammette che quella macchina non sa risolvere un problema che un bambino, con un minimo di pazienza, impara a gestire intuitivamente.
>
> Non è la fine della storia. È solo la fine di un capitolo scritto troppo in fretta.

Nella prossima unità il pendolo si sposta dall'altra parte: se le macchine non possono imparare da sole, si prova a scrivere a mano tutto ciò che sanno gli esperti umani. Funziona, per un po' — poi si scopre perché non basta.

**Footer**: Modulo 00 — Blocco A · Unità 3 — Euforia e primo schianto pratico

---
---

## Unità A.4 — Regole scritte a mano, poi i dati

**Kicker**: Modulo 00 · Blocco A · Unità 4
**Tappe**: I sistemi esperti (anni '70-'80) · Il secondo inverno (1987–1993) · La rivincita statistica (anni '90)

### Apertura

Se una macchina non impara da sola, resta un'altra strada, apparentemente più solida: prendere un esperto umano, sedersi con lui per mesi, ed estrarre tutto ciò che sa sotto forma di regole — "se il paziente presenta questi sintomi, allora considera questa diagnosi". Niente apprendimento, niente ambiguità statistica: solo logica scritta a mano, dalla persona che ne sa di più al mondo. Sembra imbattibile. Per un decennio, quasi lo è.

### Tappa 1 · Anni '70-'80 — I sistemi esperti: l'intelligenza come elenco di regole

L'approccio si chiama, con qualche variazione, "sistema esperto": un motore di regole logiche del tipo "se-allora", scritte a mano da un umano esperto del dominio insieme a un "ingegnere della conoscenza" che le traduce in codice. MYCIN, sviluppato a Stanford, suggerisce terapie antibatteriche con un'accuratezza che regge il confronto con specialisti umani, in un dominio ristretto. XCON (noto anche come R1), alla Digital Equipment Corporation, configura ordini complessi di computer VAX e fa risparmiare all'azienda decine di milioni di dollari l'anno.

Intorno a questi sistemi cresce un'industria vera: macchine specializzate — le "macchine LISP", costruite apposta per eseguire questo tipo di software — vendute da aziende come Symbolics a prezzi molto superiori a un computer generico, giustificati dalle prestazioni superiori su questo carico di lavoro specifico.

**[ASIDE: perché funziona, in un dominio ristretto]** Un sistema esperto non ha bisogno di "capire" la medicina o la configurazione hardware. Ha bisogno che qualcuno abbia già trasformato la competenza in una lista sufficientemente esaustiva di condizioni. Finché il dominio resta stretto e stabile, la lista può davvero essere abbastanza esaustiva.

### Tappa 2 · 1987–1993 — Il secondo inverno: quando la lista non basta più

Il problema si chiama, nel gergo del campo, *brittleness* — fragilità: un sistema esperto non degrada con eleganza fuori dal proprio dominio, si rompe di colpo. Non "non lo so" — semplicemente non ha una regola per quel caso, e non ha modo di accorgersi che gli manca. Ogni cambiamento nel dominio richiede che un ingegnere della conoscenza, costoso e specializzato, aggiorni a mano centinaia di regole. Il sistema non impara da un caso nuovo: va riscritto.

Nel 1987 il mercato delle macchine LISP collassa: workstation generiche di Apple e Sun, sempre più potenti per la legge di Moore, raggiungono le stesse prestazioni a una frazione del costo — e nessuno ha più motivo di comprare hardware specializzato per eseguire regole scritte a mano. Nel 1991 la Strategic Computing Initiative della DARPA valuta deludenti i propri progetti di AI e ritira i finanziamenti. Il progetto giapponese di "quinta generazione", basato sullo stesso paradigma, viene abbandonato senza aver raggiunto i propri obiettivi originali.

**[ASIDE: questo, a differenza di Gödel e del Perceptron, è l'inverno propriamente detto]** Il termine "inverno dell'AI" nasce nel 1984, coniato da ricercatori che avevano già attraversato i tagli di finanziamento degli anni '70, per analogia con "inverno nucleare". Questo — 1987-1993 — insieme al primo (1974-1980, innescato dal Lighthill Report), è uno dei due episodi a cui il termine si applica in senso storiografico stretto.

### Tappa 3 · Anni '90 — La rivincita statistica: lasciar parlare i dati

Mentre i sistemi a regole collassano sotto il proprio peso, un approccio diverso guadagna terreno — non nuove regole scritte meglio, ma modelli statistici che estraggono pattern direttamente dai dati, senza che nessun umano codifichi esplicitamente la conoscenza. Gli Hidden Markov Model permettono progressi concreti nel riconoscimento vocale. Le Support Vector Machines, formalizzate da Vladimir Vapnik, offrono un metodo matematicamente elegante per classificare dati complessi.

Il cambio di filosofia è più importante del singolo strumento: invece di chiedere "cosa sa l'esperto, e come lo scriviamo come regola", la domanda diventa "quali pattern sono già nei dati, e come li estraiamo automaticamente". È la prima comparsa, in forma ancora acerba, dell'idea che guiderà tutto il resto di questo corso.

**[QUESTION]** Un sistema esperto e un modello linguistico moderno hanno in comune più di quanto sembri a prima vista: entrambi comprimono conoscenza in una forma eseguibile. La differenza — se è una differenza di natura o solo di scala — è una delle domande che il piano di questo corso lascia esplicitamente aperta per il Blocco B. Non la risolva ora: la tenga in mente.

### Il quadro

- **Anni '70-'80** — Sistemi esperti: MYCIN, XCON, un'industria intera costruita su regole scritte a mano. *(costruzione)*
- **1987–1993** — Secondo inverno dell'AI: collasso del mercato LISP, tagli DARPA, abbandono del progetto giapponese di quinta generazione. *(rottura)*
- **Anni '90** — Rivincita statistica: Hidden Markov Model, Support Vector Machine — i dati sostituiscono le regole scritte a mano. *(costruzione)*

### Chiusura

> Per un decennio, insegnare a un computer significa scrivere tutto ciò che sai, per iscritto, in una lista che non finisce mai. Poi la lista si rompe contro il primo caso che non aveva previsto — e qualcuno si accorge che forse il problema non era scrivere meglio la lista, ma smettere di scriverla a mano.

Nella prossima unità quell'intuizione statistica incontra di nuovo le reti neurali — la stessa idea del Perceptron, uscita di scena nel 1969, che aspettava solo che il mondo le fornisse abbastanza scala per funzionare.

**Footer**: Modulo 00 — Blocco A · Unità 4 — Regole scritte a mano, poi i dati

---
---

## Unità A.5 — Tornano le reti, stavolta con la scala

**Kicker**: Modulo 00 · Blocco A · Unità 5
**Tappe**: Backpropagation (anni '80) · Hinton e il deep learning (2006) · Word2Vec (2013)

### Apertura

Ogni tanto un'idea scartata non era sbagliata — era solo arrivata prima di quello che le serviva per funzionare. Questa unità racconta esattamente un caso del genere: la stessa intuizione del Perceptron, morta sulla carta nel 1969, che risorge non perché qualcuno la corregge concettualmente, ma perché il mondo, col tempo, le fornisce ciò che le mancava.

### Tappa 1 · Anni '80 — Backpropagation: il problema del 1969, risolto

Un algoritmo chiamato *backpropagation* — la cui origine tecnica risale addirittura ai primi anni '70, ma che diventa noto alla comunità scientifica soprattutto grazie a un articolo di David Rumelhart, Geoffrey Hinton e Ronald Williams nel 1986 — permette finalmente di addestrare reti neurali a più strati, non solo il singolo strato del Perceptron originale.

Il dettaglio che chiude un cerchio aperto in questo blocco: una rete neurale a più strati **risolve** XOR. Il limite geometrico che Minsky e Papert avevano dimostrato riguardava specificamente i modelli a un solo strato — loro stessi lo sapevano, come già notato nell'Unità 3. Mancava solo un metodo per addestrare più strati insieme. Ora c'è.

**[ASIDE: perché non è bastato, comunque]** La disponibilità dell'algoritmo non basta a rilanciare il campo su vasta scala. Mancano ancora due cose: dati sufficienti, e potenza di calcolo sufficiente per reti abbastanza profonde. Le reti neurali degli anni '80-'90 restano, per lo più, poco profonde — l'addestramento di reti davvero profonde soffre di un problema tecnico (il gradiente che si "affievolisce" attraversando molti strati) che nessuno sa ancora affrontare bene.

### Tappa 2 · 2006 — Hinton: il "deep learning" prende un nome

Geoffrey Hinton, insieme a Simon Osindero e Yee-Whye Teh, pubblica un metodo per addestrare reti profonde strato per strato, dimostrando che l'addestramento di reti realmente profonde è possibile. Il termine "deep learning" comincia a diffondersi da questo momento come etichetta per l'intero approccio.

Vale la pena essere onesti su cosa sia davvero nuovo qui, e cosa no: l'idea di base — strati di neuroni artificiali, pesi aggiustati tramite backpropagation — è la stessa degli anni '80. Quello che cambia, nel decennio successivo, è tutt'altro: la disponibilità di dataset molto più grandi, e — aggancio diretto alla lezione sull'hardware già trattata in questo corso — la scoperta che le GPU, nate per i videogiochi, sono perfette per addestrare reti neurali su scala molto maggiore di prima.

**[QUESTION]** Nota lo schema, di nuovo: un'idea concettualmente completa aspetta vent'anni un contesto materiale — dati, hardware — che la renda praticabile. È lo stesso schema che ha separato il sogno di Leibniz dalla sua realizzazione. Vale la pena chiedersi quante altre idee "morte" della storia dell'AI aspettino, in questo momento, solo il contesto giusto.

### Tappa 3 · 2013 — Word2Vec: le parole diventano punti nello spazio

Un gruppo di ricercatori guidato da Tomas Mikolov, a Google, pubblica Word2Vec: un metodo per rappresentare ogni parola come un vettore — un punto in uno spazio a molte dimensioni — addestrato in modo che parole con significati simili finiscano vicine tra loro. L'esempio diventato celebre, e che il corso riprenderà per intero nel Modulo 3: sottraendo il vettore di "uomo" da quello di "re" e aggiungendo quello di "donna", il punto più vicino nello spazio risultante è "regina" — un'operazione puramente aritmetica che produce un risultato semanticamente sensato.

**[ASIDE: perché sorprende anche chi lo ha costruito]** Nessuno ha progettato esplicitamente questa struttura algebrica: emerge dall'addestramento sui dati, senza che sia stata codificata a mano da nessuna parte. È il primo caso, in questo corso, di una capacità che compare senza essere stata esplicitamente costruita — un tema che tornerà, con proporzioni molto maggiori, quando si parlerà di capacità emergenti nel Blocco B.

### Il quadro

Da notare: questa unità, a differenza delle precedenti, non contiene una vera rottura — è l'arco della ricostruzione dopo due inverni.

- **Anni '80** — Backpropagation: il limite del 1969 (XOR) viene risolto strutturalmente, ma manca ancora scala. *(costruzione)*
- **2006** — Hinton: le reti profonde si addestrano davvero, nasce il termine "deep learning". *(costruzione)*
- **2013** — Word2Vec: le parole diventano vettori, e l'algebra tra vettori produce senso semantico. *(costruzione)*

**[QUESTION]** Per la prima volta in questo blocco, tre tappe di fila senza un crollo. Vale la pena chiedersi se questo significhi che il ciclo costruzione-rottura si sia interrotto per sempre, o solo che la prossima rottura non è ancora avvenuta.

### Chiusura

> Un'idea del 1958, dichiarata clinicamente morta nel 1969, risolta sulla carta negli anni '80, e finalmente utile su vasta scala solo a partire dal 2006. Cinquant'anni tra l'intuizione e la sua realizzazione pratica — non per un errore concettuale, ma perché al mondo mancava, per decenni, il contesto materiale giusto.

Resta un problema che nessuna delle tre tappe di questa unità risolve: le reti che abbiamo visto processano l'informazione in sequenza, un pezzo alla volta, e faticano a tenere a mente ciò che hanno visto molti passi prima. Nella prossima e ultima unità del blocco, un'idea diversa elimina il problema alla radice — ed è l'architettura su cui gira, oggi, ogni modello linguistico di grandi dimensioni, incluso quello con cui sta interagendo in questo momento.

**Footer**: Modulo 00 — Blocco A · Unità 5 — Tornano le reti, stavolta con la scala

---
---

## Unità A.6 — L'attenzione e il salto finale

**Kicker**: Modulo 00 · Blocco A · Unità 6 (chiusura del blocco)
**Tappe**: Il limite delle reti ricorrenti · L'attenzione (2014-15) · Il Transformer (2017) · Chiusura del Blocco A

### Apertura

Provi a tradurre una frase lunga leggendola una parola alla volta, tenendo a mente solo un riassunto sempre più compresso di tutto ciò che ha letto finora, senza mai poter tornare indietro a rileggere l'inizio. È più o meno il modo in cui le reti neurali "ricorrenti" — il tipo di architettura dominante per il linguaggio prima del 2017 — gestiscono le sequenze. Funziona, fino a un certo punto. Poi la frase si allunga, e il riassunto compresso comincia a perdere esattamente i dettagli che servivano.

### Tappa 1 — Il limite delle reti ricorrenti

Le reti ricorrenti (e le loro varianti più sofisticate, le LSTM) processano una sequenza — una frase, un testo — un elemento alla volta, mantenendo uno stato interno che riassume tutto ciò che hanno visto fino a quel punto. Due problemi strutturali: primo, le dipendenze a lungo raggio si degradano — informazione rilevante all'inizio di una frase lunga tende a "svanire" prima che la rete raggiunga la fine. Secondo, e forse più limitante nella pratica: il processamento è intrinsecamente sequenziale — non si può calcolare l'elemento numero 50 prima di aver calcolato il numero 49. Questo rende l'addestramento su grandi quantità di testo molto più lento di quanto potrebbe essere.

### Tappa 2 · 2014-2015 — L'attenzione: guardare indietro, selettivamente

Nel contesto della traduzione automatica, un gruppo di ricercatori guidato da Dzmitry Bahdanau introduce un meccanismo che permette a una rete, nel produrre ogni parola di output, di "guardare" direttamente a tutte le parole dell'input — pesando ciascuna in base a quanto è rilevante in quel momento specifico — invece di affidarsi a un unico riassunto compresso dell'intera frase. L'idea si chiama, semplicemente, *attenzione*.

**[ASIDE: cosa risolve, in una frase]** Invece di comprimere l'intera frase di input in un solo vettore e sperare che basti, il modello impara a consultare selettivamente le parti dell'input più rilevanti per ogni parola che sta generando — un po' come un traduttore umano che, scrivendo la parola dieci, rilegge la parola tre dell'originale perché è quella che conta davvero in quel punto.

### Tappa 3 · 2017 — "Attention Is All You Need": il Transformer

Un gruppo di ricercatori a Google, con un articolo dal titolo che è già un programma — *Attention Is All You Need* — compie il passo decisivo: elimina del tutto la componente ricorrente, e costruisce un'architettura basata unicamente sull'attenzione (più semplici strati di elaborazione). Il nome dell'architettura: **Transformer**.

Il vantaggio pratico è enorme, e si riaggancia direttamente alla lezione sull'hardware già affrontata in questo corso: senza il vincolo sequenziale delle reti ricorrenti, tutte le posizioni di una sequenza possono essere elaborate in parallelo — esattamente il tipo di carico di lavoro per cui una GPU, con le sue migliaia di operazioni simultanee, è stata costruita. Non è un dettaglio marginale: è, in buona parte, il motivo per cui i modelli linguistici di oggi possono essere addestrati sulla scala che vede nel Modulo 6.

**[QUESTION]** Il Transformer è l'architettura sotto ogni modello linguistico di grandi dimensioni oggi in uso — incluso quello con cui interagisce in questo momento. Come funzioni esattamente il meccanismo di attenzione, in dettaglio, è materia del Modulo 5. Qui basti sapere che esiste, che ha una data di nascita precisa, e che senza il passaggio dell'Unità 5 — GPU, scala, dati — sarebbe rimasto teoricamente interessante e praticamente inutilizzabile, come già successo altre volte in questo blocco.

### Il quadro — timeline locale

- **Prima del 2017** — Reti ricorrenti: gestiscono sequenze, ma soffrono di dipendenze a lungo raggio e di un collo di bottiglia sequenziale. *(rottura, in senso tecnico più che narrativo)*
- **2014-2015** — Attenzione: un modo per consultare selettivamente l'intero input invece di comprimerlo in un solo vettore. *(costruzione)*
- **2017** — Transformer: l'attenzione diventa l'intera architettura, il calcolo si parallelizza, la scala diventa gestibile. *(costruzione)*

### Il quadro — timeline dell'intero Blocco A (elemento capstone, solo in questa unità)

Proposta per Claude Code: un'unica timeline riassuntiva, più lunga di quelle locali di ogni unità, che attraversi l'intero blocco dal XVII secolo al 2017 — l'unico posto nel blocco dove ha senso vederle tutte insieme.

- **XVII sec.** — Leibniz, *Characteristica Universalis*. *(costruzione)*
- **1854** — Boole, *The Laws of Thought*. *(costruzione)*
- **1879–1913** — Frege, il paradosso di Russell, *Principia Mathematica*. *(costruzione)*
- **1931** — Gödel, teoremi di incompletezza. *(rottura)*
- **1936, 1950** — Turing, la macchina universale e il test dell'imitazione. *(costruzione)*
- **1961** — Lucas, l'obiezione matematica formalizzata. *(rottura)*
- **1956** — Dartmouth, nasce il nome "intelligenza artificiale". *(costruzione)*
- **1958** — Rosenblatt, il Perceptron. *(costruzione)*
- **1969** — Minsky e Papert, il limite di XOR. *(rottura)*
- **1970-80** — Sistemi esperti. *(costruzione)*
- **1987–1993** — Il secondo inverno dell'AI. *(rottura)*
- **Anni '90** — Rivincita statistica. *(costruzione)*
- **1986, 2006** — Backpropagation, poi deep learning. *(costruzione)*
- **2013** — Word2Vec. *(costruzione)*
- **2017** — Transformer. *(costruzione)*

**[QUESTION]** Guardata tutta insieme, la timeline del blocco mostra qualcosa che nessuna singola unità poteva mostrare da sola: le rotture sono minoranza (quattro su quindici tappe), eppure sono quelle che si ricordano. Vale la pena chiedersi se la storia dell'AI sia davvero fatta soprattutto di crolli, come la si racconta spesso, o se la si racconti così perché i crolli fanno storie migliori delle costruzioni lente.

### Chiusura del blocco

> Tre secoli, quindici tappe, quattro rotture. Un filosofo secentesco che sogna di eliminare il disaccordo con un calcolo; un teorema che dimostra che nessun calcolo del genere può essere completo; una macchina lodata dalla stampa come futura coscienza, che non sa risolvere un problema a due variabili; e infine un'architettura, nata per tradurre frasi meglio, che oggi genera questo stesso testo.
>
> Niente di tutto questo era inevitabile. Ogni tappa avrebbe potuto fermarsi lì.

Prima di chiudere davvero il blocco, alcune domande restano deliberatamente senza risposta — non per pigrizia, ma perché nessuna risposta onesta esiste ancora, e il corso le riprenderà da prospettive diverse più avanti:

- Un modello linguistico di grandi dimensioni è un sistema formale nel senso di Gödel? E se lo è, l'obiezione di Lucas — qualunque cosa valga per una mente umana — si applica anche a lui?
- Cosa ha cambiato, esattamente, l'introduzione della profondità nelle reti neurali — è una differenza di grado o di natura rispetto ai modelli a singolo strato del 1958?
- Un modello linguistico di oggi è, in fondo, un sistema esperto molto più grande — o c'è una differenza qualitativa tra regole scritte a mano e pattern estratti da miliardi di esempi?

Queste domande non si chiudono qui. Il Blocco B parte esattamente da dove questo blocco si ferma: non più la storia di come si è arrivati fin qui, ma una mappa onesta di cosa un modello come questo sa fare davvero, cosa simula di saper fare, e cosa non sa fare affatto.

**Footer**: Modulo 00 — Blocco A · Unità 6 — L'attenzione e il salto finale (chiusura del blocco)
