# Moduli 1-6 — Struttura testuale dettagliata (bozza)

**Stato**: bozza di struttura in unità, concordata in conversazione. Non è contenuto
scritto (nessuna prosa, nessuna narrativa) — solo titoli, temi per unità, note di
raccordo e i punti di innesco del filo discreto/continuo. Riferimento generale:
`piano_corso_llm.md` (righe 12-46), che resta la fonte per la struttura a 7 moduli e
per il Modulo 00 narrativo (già completo, Blocchi A-D).

**Prossimo passo, non ancora avviato**: prototipazione grafica dei componenti
interattivi (spazio degli embedding, discesa del gradiente, attention in azione),
poi contenuto in prosa, poi HTML — ordine e processo ancora da stabilire nel
dettaglio quando si affronterà quella fase.

**Note aperte, volutamente non sviluppate qui**:
- *Ragionamento causale* (Blocco B.3.2 / Nodo 2 di Blocco C, Pearl/Hume): connesso
  intimamente alla stanza cinese di Searle. Nessuna unità tecnica in Moduli 1-6 lo
  ospita ancora esplicitamente — Modulo 5 (natura correlazionale/associativa
  dell'attention, non causale) è il candidato più probabile, ma la collocazione resta
  da decidere, non ora.
- *Linguaggio shader/SDF* (Signed Distance Function, stile Shadertoy) per rendere una
  superficie continua vera (es. la discesa del gradiente in 4.5) invece di un grafico
  discreto — coerente in modo quasi programmatico col contenuto insegnato, ma è una
  decisione di implementazione, non di struttura testuale. Rimandata esplicitamente
  alla fase di inventario grafico definitivo.

---

## Modulo 1 — Il testo come dato

1. **1.1 — Da lettere a numeri: l'encoding**
   Il testo è già numeri prima ancora di arrivare a un LLM (ASCII/Unicode). Riaggancio
   esplicito al Modulo 0 (booleano/hardware, già sviluppato): "quando scrivi una
   lettera, cosa 'vede' davvero la macchina?"
   *Filo discreto/continuo*: tesi di apertura da rendere esplicita — la "digitalizzazione"
   non nasce col computer. La scrittura stessa, l'alfabeto, è il primo grande atto di
   discretizzazione della storia umana: trasforma il continuo del parlato (suoni che
   sfumano l'uno nell'altro) in un insieme finito di simboli discreti e ricombinabili,
   molto prima che esistesse una parola per nominare l'operazione. Il concetto diventa
   consapevole solo nel Novecento — von Neumann, *The Computer and the Brain* (1958,
   titolo non casuale: mette a confronto le stesse due cose che il Modulo 4 confronterà
   meccanicamente) — ed esplicito su scala industriale solo con i progetti di
   digitalizzazione di massa dei primi anni 2000. Il computer non inventa la
   discretizzazione: la eredita e la porta all'estremo.

2. **1.2 — Cos'è una "parola" per una macchina? La tokenizzazione**
   Gli spazi non bastano a definire una parola: parole composte, lingue senza spazi
   (es. cinese), morfologia. Connessione esplicita alla linguistica (morfologia,
   tipologia linguistica). Introduce token vs parola.

3. **1.3 — Il problema del vocabolario**
   Perché non si può avere una tabella con "tutte le parole del mondo" (neologismi,
   errori di battitura, lingue miste, nomi propri). Porta alla tokenizzazione a
   sotto-parole (BPE) come soluzione ingegneristica, non ovvia.

4. **1.4 — Dai token agli ID: numeri senza significato**
   Il vocabolario come dizionario numerico. Chiusura del modulo: il testo è ormai una
   sequenza di numeri arbitrari — l'ID 47 non ha nessuna relazione con l'ID 48.
   Domanda aperta che aggancia sia Modulo 2 (sequenze di simboli) sia soprattutto
   Modulo 3 (embedding): come si rappresenta che "gatto" e "cane" sono più simili tra
   loro di "gatto" e "ministero"?
   *Filo discreto/continuo*: qui si può nominare esplicitamente che questo è il punto
   più discreto dell'intero corso — simboli finiti, numerabili, senza nozione di
   "vicinanza" tra loro. Serve da riferimento per contrasto nei moduli successivi.
   Analogia concreta da usare: un'immagine raster (JPEG/PNG) è una griglia fissa di
   pixel — ingrandirla costringe il computer a *interpolare*, cioè a inventare valori
   plausibili nei "buchi" (da cui la pixelazione). Un'immagine vettoriale (SVG) è invece
   una descrizione matematica continua, ricalcolata a ogni scala senza perdita. I token
   con ID numerico sono "raster" — un insieme fisso, senza nulla nel mezzo. Gli embedding
   del Modulo 3 saranno "SVG" — uno spazio continuo, ricalcolabile in qualunque punto.

5. **1.5 — Gödel: i limiti di un sistema discreto**
   Unità di approfondimento che paga un debito narrativo aperto fin dal Blocco A, dove
   compare esplicitamente, come domanda irrisolta, "Un LLM è un sistema formale nel senso
   di Gödel?" — finora lasciata solo retorica. Percorso (accessibile, nello stile
   induttivo del corso, senza notazione pesante): cos'è un sistema formale — regole
   finite, simboli finiti, dimostrazioni come sequenze finite di simboli — cioè un
   oggetto discreto ed enumerabile, esattamente come il vocabolario di token appena
   costruito in 1.3/1.4. La mossa di Gödel: numerare tutto (aritmetizzazione) — una
   dimostrazione diventa un numero, il sistema finisce per parlare di se stesso. La frase
   autoreferenziale ("questa frase non è dimostrabile in questo sistema") e il dilemma
   che ne segue: se è falsa, è dimostrabile (il sistema è incoerente); se è vera, non è
   dimostrabile (il sistema è incompleto). Payoff esplicito: si torna alla domanda del
   Blocco A con più strumenti, non risolvendola ma affrontandola sul serio — un LLM ha
   un vocabolario finito e pesi finiti (per quanto enormi): è, in un senso preciso, un
   sistema discreto ed enumerabile. Se l'analogia con un sistema formale gödeliano
   tenesse, ne seguirebbero limiti strutturali interni — ma se l'analogia sia precisa o
   solo suggestiva resta esplicitamente una domanda aperta, non richiusa qui.

---

## Modulo 2 — Probabilità e linguaggio

1. **2.1 — Prevedere la parola successiva: il compito centrale**
   Si parte dall'intuizione umana (autocomplete, "il gatto è salito sul ___") per
   isolare il compito che tutto il modulo formalizza. Richiamo esplicito al registro
   critico di Blocco B ("completamento statistico" come ciò che gli LLM sanno fare
   davvero).

2. **2.2 — Contare per prevedere: unigrammi e bigrammi**
   Esempio concreto con un piccolo corpus: contare le frequenze per stimare una
   probabilità. Primo "modello linguistico", nella sua forma più ingenua.
   *Filo discreto/continuo*: prima crepa nel discreto — una probabilità è un numero
   reale tra 0 e 1, non più uno stato binario. I simboli (le parole) restano discreti,
   ma per la prima volta il corso lavora con una gradazione. Accenno breve, non una
   digressione.
   Vocabolario canonico da introdurre qui: quello che il modello fa contando frequenze
   è un caso preciso di **induzione** — generalizzare da casi osservati a una regola
   probabile — non deduzione (applicare una regola certa). Aggancio a Blocco B.2, che
   parla già di "interpolazione, non deduzione" senza nominare il termine tecnico.
   Payoff di un debito esplicito lasciato in Blocco B.2 ("un tema che tornerà, in forma
   tecnica, quando si parlerà di calibrazione"): un modello è **calibrato** se, tra
   tutte le previsioni fatte con una data confidenza (es. 70%), circa quella
   percentuale risulta effettivamente corretta. È qui, dove nasce per la prima volta
   il concetto di probabilità in uscita da un modello, che va onorata quella promessa.

3. **2.3 — N-grammi, finestra di contesto e assunzione di Markov**
   Generalizzazione a più parole di contesto; si nomina esplicitamente l'assunzione di
   Markov e si mostra che è un'idea più ampia della linguistica (es. previsioni
   meteo, giochi da tavolo) — non un trucco specifico del testo.

4. **2.4 — I limiti strutturali: dati mai visti e dipendenze lontane**
   Sparsità (combinazioni di parole mai incontrate) e il problema delle dipendenze a
   lungo raggio — frasi con incisi o subordinate annidate che un n-gramma non può
   catturare per costruzione. Possibile aggancio alla critica di Chomsky ai modelli a
   stati finiti del linguaggio. Chiude aprendo esplicitamente la domanda che il
   Modulo 5 (Transformer/attention) risolverà.

---

## Modulo 3 — Parole come punti nello spazio

*Modulo più denso, cuore visivo del corso.*

1. **3.1 — Il problema lasciato aperto**
   Riprende due fili: gli ID arbitrari del Modulo 1 (47 non è "vicino" a 48) e il
   limite del Modulo 2 (un n-gramma non generalizza tra "gatto" e "cane" anche se
   sono intercambiabili in molti contesti). Nesso causale da rendere esplicito: un
   simbolo discreto non ha "vicini" per costruzione → nessuna nozione di similarità →
   nessuna generalizzazione a combinazioni mai viste. È la spiegazione tecnica della
   sparsità del Modulo 2, non solo un cambio di rappresentazione.
   *Filo discreto/continuo, versione più precisa*: gli n-grammi si comportano come un
   insieme *denso ma pieno di buchi* — dato un contesto, di solito si trova *qualcosa* di
   vicino nei dati visti (densità), ma restano lacune che nessun affinamento del conteggio
   può colmare (le combinazioni mai osservate). Gli embedding si comportano invece come
   un continuo *senza buchi*: l'interpolazione geometrica è sempre possibile, anche verso
   punti mai visti esplicitamente. Non è solo "più dati aiutano" — è un cambio nel tipo di
   struttura matematica sottostante, non solo nella quantità.
   Fondamento rigoroso (si appoggia a 1.5): l'argomento diagonale di Cantor mostra che un
   insieme numerabile (elencabile con un metodo sistematico, come i sistemi formali di
   1.5 o un vocabolario discreto di token) è strutturalmente più "piccolo" dell'insieme
   dei numeri reali, che nessuna lista può mai contenere per intero. Non è un'analogia
   di stile: un vocabolario discreto è numerabile per costruzione; uno spazio di
   embedding a valori reali non lo è. È la stessa distinzione matematica, non solo la
   stessa intuizione.

2. **3.2 — Le parole come vettori: coordinate in uno spazio di significato**
   Introduce l'idea di vettore come lista di numeri/coordinate, con un'intuizione
   geometrica minima (spazio a 2 dimensioni prima di quello ad alta
   dimensionalità): vicinanza spaziale = somiglianza semantica.
   Qui va introdotto esplicitamente il termine tecnico **"embedding"** (non solo
   "vettore"/"rappresentazione vettoriale") — il momento in cui il vocabolario
   tecnico si fissa, perché i Moduli 4-6 lo daranno per acquisito.
   *Filo discreto/continuo*: cenno puntuale a Leibniz — lo stesso Leibniz che apre il
   Blocco A col sogno del pensiero come calcolo simbolico discreto è anche tra gli
   inventori del calcolo infinitesimale, lo strumento per trattare il continuo.
   Richiamo puntuale, non una digressione storica.
   *Secondo filo, Galileo e le qualità*: Galileo separò le qualità primarie
   (quantificabili: forma, posizione, numero) da quelle secondarie (colore, sapore,
   tutto ciò che sembra soggettivo e relazionale) e fondò la scienza moderna scegliendo
   di occuparsi solo delle prime. Il significato di una parola era il caso limite di
   qualità "secondaria" — sembrava impossibile misurarlo. Il Modulo 3 fa esattamente
   la mossa che Galileo escludeva: trasforma il significato in coordinate quantificabili.
   Non è solo un trucco statistico: è un'estensione radicale, quattro secoli dopo, dello
   stesso programma galileiano a un territorio che Galileo aveva dichiarato fuori
   portata. Punto da riprendere in 5.4, dove questa stessa distinzione comincia a
   incrinarsi.

3. **3.3 — Come si imparano questi vettori: l'ipotesi distribuzionale**
   Firth ("si conosce una parola dalla compagnia che tiene") — callback esplicito a
   Wittgenstein e "significato come uso" già visto nel Nodo 1 del Blocco C.
   Intuizione di Word2Vec: prevedere il contesto come compito di addestramento.

4. **3.4 — "Re − Uomo + Donna = Regina": l'aritmetica vettoriale come fenomeno**
   Spiega perché l'operazione funziona geometricamente (direzioni consistenti nello
   spazio), non solo che funziona — e ne mostra anche la fragilità/i casi in cui
   fallisce, per evitare la mistificazione, coerente col registro critico già
   stabilito in Blocco B.
   *Filo discreto/continuo*: eco esplicita al Blocco A — il corso sta attraversando
   dal basso, tecnicamente, lo stesso passaggio (simbolico → statistico/
   connessionista) che il Blocco A ha già raccontato dall'alto, come storia.
   Domanda aperta da lasciare esplicitamente irrisolta (coerente col metodo del corso):
   la geometria dello spazio degli embedding *descrive* qualcosa di reale sul significato
   — che esisteva anche prima, e il modello lo ha solo trovato — o lo *costruisce*, come
   artefatto statistico utile ma senza nulla di "reale" corrispondente? È la stessa
   domanda, in altra forma, che si pone da secoli su cosa siano davvero i numeri.
   Aggancio possibile a Wigner e alla sua formula sull'"irragionevole efficacia della
   matematica" — perché l'aritmetica vettoriale funzioni così bene resta, in un senso
   preciso, non del tutto spiegato.
   *Il sillogismo dell'erba (Bateson)*: Bateson distingue il sillogismo in Barbara
   ("gli uomini muoiono, Socrate è un uomo, Socrate muore" — valido per struttura di
   classe) dal "sillogismo dell'erba" ("l'erba muore, gli uomini muoiono, gli uomini
   sono erba" — formalmente invalido, ma è la logica reale della metafora). L'aritmetica
   vettoriale *è*, strutturalmente, un sillogismo dell'erba: ragiona per predicato/
   direzione condivisa nello spazio, non per appartenenza di classe. Questo spiega, con
   più precisione filosofica, sia perché funziona (è metafora geometrica reale) sia
   perché a volte fallisce (la logica della metafora non è mai truth-preserving come
   Barbara) — in termini classici, è un caso di **abduzione** (inferenza alla
   spiegazione/analogia più plausibile), non di deduzione né della semplice induzione
   già vista in 2.2. Coerente con Lakoff/Johnson, già presenti in Blocco D.

5. **3.5 — I limiti: un vettore, molti significati**
   Polisemia e il problema degli embedding statici (una parola, un solo vettore
   fisso, indipendente dal contesto). Chiude aprendo esplicitamente al Modulo 5
   (rappresentazioni contestuali via attention).

---

## Modulo 4 — Reti neurali

1. **4.1 — Dal neurone biologico al neurone artificiale**
   McCulloch-Pitts (1943) e Hebb (1949) — già citati narrativamente nel Nodo 3 del
   Blocco C, qui si scende nel meccanismo: somma pesata più funzione di attivazione,
   l'unità minima. Punto pedagogico: quanto poco del biologico è stato davvero preso
   in prestito.
   *Un secondo biologo, in contrappunto a Bateson*: Varela (con Maturana) propone
   l'**autopoiesi** e la **chiusura operazionale** — un sistema vivente non "elabora
   informazioni" dal mondo in senso rappresentazionale forte; è una rete chiusa di
   relazioni che si automantiene, *perturbata* ma non *istruita* dall'esterno. Dà un
   vocabolario più preciso a un punto già presente in Blocco B.2 ("non esiste un punto
   nella rete in cui sia scritto... quel fatto è disperso"): i pesi di una rete non
   rappresentano i dati di addestramento in modo trasparente — costituiscono una
   struttura chiusa e auto-coerente, perturbata dai dati ma non "contenente" i dati.

2. **4.2 — Il perceptron e il ritorno di XOR**
   Chiude un debito narrativo aperto fin dalla prima lezione: l'aside di
   `lezione_00a_funzioni_booleane.html` diceva esplicitamente "tieni da parte questo
   operatore… torna, con conseguenze non banali, quando un certo modello del 1958 si
   troverà davanti a un problema che non sa risolvere." Questa è l'unità che paga
   quella promessa — perché un singolo strato non può separare XOR, e cosa significhi
   "non linearmente separabile" a livello intuitivo/geometrico, non formale.

3. **4.3 — Aggiungere strati: perché la profondità cambia le cose**
   Il multi-layer perceptron risolve XOR; intuizione di rappresentazioni via via più
   abstratte a ogni strato. Risponde direttamente a una domanda aperta già piantata
   nel Blocco A: "cosa ha cambiato, esattamente, la profondità nelle reti neurali?"
   *Pleroma e creatura (Bateson)*: la distinzione, ripresa da Jung, tra pleroma (il
   mondo delle forze fisiche pure, senza informazione) e creatura (il mondo della
   comunicazione e della forma, dove esiste "una differenza che fa la differenza" —
   la definizione di informazione di Bateson). Domanda aperta da lasciare tale: le
   rappresentazioni sempre più astratte che emergono strato dopo strato sono pleroma
   organizzato ad arte che *sembra* informazione, o sono già, in un senso minimo ma
   genuino, creatura? Bateson stesso, con cautela e citando Blake, avanza anche
   l'ipotesi estrema opposta — che non esista affatto un pleroma puro. Il corso non
   la risolve, la pone.

4. **4.4 — Misurare l'errore: la funzione di perdita**
   La loss come superficie continua da minimizzare.
   *Filo discreto/continuo*: punto in cui il filo tocca il suo massimo tecnico — una
   funzione a scalini non si può "scendere" nello stesso modo, serve continuità
   perché il gradiente esista. Non chiudere qui il filo: la chiusura vera è riservata
   al Modulo 6 (quantizzazione).

5. **4.5 — L'intuizione del gradiente e come l'errore si propaga**
   La discesa del gradiente come metafora spaziale (scendere una collina nella
   nebbia), e in breve come l'errore si propaga indietro attraverso gli strati
   (backpropagation), senza formalismo. Richiamo esplicito al Nodo 3 di Blocco C: "il
   backpropagation non è biologicamente plausibile" — il cervello non impara così.
   Riapre la domanda su cosa distingua "apprendimento" artificiale da biologico.
   *Backpropagation e schismogenesi (Bateson)*: rafforza con un quadro teorico preciso
   la distinzione già presente in C.3 ("discreto e globale" vs "continuo e locale"). La
   schismogenesi di Bateson (*Naven*, 1936) e il feedback negativo classico
   (termostato) sono cicli di retroazione *continui*, che agiscono *durante* il
   comportamento in corso. Il backpropagation non lo è: è una procedura offline,
   discreta, globale, che corregge una struttura *prima* che agisca, non mentre agisce
   — strutturalmente più vicino a un processo selettivo (come l'evoluzione: molte
   prove, poi una struttura fissata) che a un vero feedback omeostatico.
   *Plasticità hardware, non solo software*: la plasticità sinaptica "continua e
   locale" ha già un corrispettivo hardware reale, non speculativo — i **memristor**
   (teorizzati nel 1971, realizzati fisicamente nel 2008), componenti la cui resistenza
   cambia in base alla storia di corrente che li ha attraversati, fondamento del
   **neuromorphic computing** (chip come Loihi o TrueNorth), che dà corpo concreto
   alle "spiking neural networks" già nominate in C.3 come programma di ricerca
   attivo. Da tenere distinto: le tecnologie **EEG/BCI** non replicano la plasticità,
   leggono/decodificano segnali neurali — ma sono un'ulteriore istanza pratica e
   attuale del filo discreto/continuo del corso: un segnale elettrico continuo che va
   campionato e discretizzato per essere processato digitalmente.
   *Domanda di chiusura del modulo* (riformulazione tecnica del "quadro" di Blocco B.2,
   "stesso meccanismo, stesso punto cieco"): se ragionamento, conoscenza e
   metacognizione condividono, in un LLM, lo stesso identico meccanismo — un'unica
   funzione di perdita minimizzata per gradiente — è una scoperta su cosa siano
   davvero queste tre facoltà anche negli umani, o solo un artefatto di come abbiamo
   costruito la macchina? Lasciata esplicitamente aperta.

---

## Modulo 5 — Il Transformer

*Modulo su cui converge quasi tutto il resto — densità maggiore giustificata.*

1. **5.1 — Il problema che l'attenzione risolve**
   Riprende insieme i due fili aperti: le dipendenze a lungo raggio dal Modulo 2, gli
   embedding statici dal Modulo 3. Momento unificante: l'attention risolve entrambi i
   problemi con lo stesso meccanismo.
   Prima di arrivare all'attention, accenno breve e anonimo al tentativo intermedio —
   elaborare il testo in sequenza, una parola alla volta, portando avanti una specie
   di "memoria" dello stato precedente — che funzionava per frasi brevi ma perdeva
   forza quanto più la distanza tra le parole rilevanti cresceva. Nessun nome tecnico
   (RNN/LSTM), solo il fallimento come ponte narrativo verso 5.2 — coerente col salto
   già fatto dal Blocco A tra Word2Vec (2013) e Transformer (2017).

2. **5.2 — Guardare tutto insieme: l'idea dell'attention**
   L'intuizione centrale: ogni parola può "guardare" direttamente ogni altra parola
   della frase, indipendentemente dalla distanza. Esempio concreto: un pronome che si
   riferisce a un nome comparso molte parole prima.

3. **5.3 — Query, Key, Value: la meccanica in tre mosse**
   Spiegazione intuitiva (analogia, non formule): cosa sto cercando, cosa ogni parola
   offre come etichetta, cosa porta con sé se scelta. I punteggi di compatibilità
   diventano pesi che sommano a 1 (softmax) — aggancio alla prima "crepa nel
   discreto" già introdotta col concetto di probabilità nel Modulo 2.

4. **5.4 — Perché ora ogni parola ha un significato diverso in ogni frase**
   Chiude esplicitamente il problema lasciato aperto in 3.5: gli embedding non sono
   più statici — la stessa parola ("banca") riceve una rappresentazione diversa in
   base a cosa la circonda, perché è il risultato di un'attenzione calcolata sul
   contesto specifico.
   Cuore concettuale, non solo decorazione (riprende 3.2): l'embedding statico del
   Modulo 3 era ancora "primario" in senso galileiano — un valore fisso, che sta lì
   indipendentemente da chi/cosa lo osserva. Qui quel presupposto crolla, con la stessa
   mossa concettuale della meccanica quantistica: posizione e quantità di moto di una
   particella non sono entrambe definite indipendentemente dalla misura — l'idea che le
   qualità "primarie" fossero osservatore-indipendenti si dissolve. Il vettore di
   "banca" non ha un valore fisso che esiste a prescindere: assume un valore solo nel
   momento in cui viene calcolato insieme alle parole che lo circondano, esattamente
   come una particella non ha una posizione definita finché non viene misurata. Non è
   un'analogia decorativa — è la stessa mossa concettuale, quattro secoli dopo Galileo,
   in un dominio completamente diverso.

5. **5.5 — Multi-head attention e l'architettura ad alto livello**
   Più "teste" di attenzione in parallelo, ciascuna che cattura un tipo diverso di
   relazione; zoom-out sull'architettura complessiva (embedding → informazione di
   posizione → strati di attenzione → blocchi ripetuti).
   Sulla posizione: non solo nota di esistenza, ma un'intuizione concreta — a ogni
   parola viene aggiunto un codice che rappresenta la sua posizione nella frase (un
   po' come numerare le pagine di un libro: anche se le pagine si mescolassero, il
   numero stampato sopra ne direbbe l'ordine originale). Questo codice si somma alla
   rappresentazione della parola, così l'attention — che altrimenti tratterebbe la
   frase come un insieme senza ordine — riceve comunque l'informazione su chi viene
   prima e chi dopo. Niente formule del pattern sinusoidale, solo l'idea che "l'ordine
   va inserito a parte, non è gratuito".

6. **5.6 — Perché questo ha sbloccato tutto: parallelismo e scala**
   A differenza dell'elaborazione sequenziale, l'attention calcola le relazioni
   sull'intera frase in un colpo, massimamente parallelizzabile — richiamo esplicito
   alla GPU come "migliaia di operai" già vista in
   `lezione_00b_hardware_software.html`. Chiude collegandosi al 2017 di "Attention is
   All You Need" già narrato in Blocco A, e apre la porta al Modulo 6.

---

## Modulo 6 — Cosa significa "Large"

*Chiude anche l'intero arco tecnico dei Moduli 1-6.*

1. **6.1 — Quanto è "grande"? Numeri che danno la scala**
   Parametri, token di addestramento, costo computazionale — non per farli
   memorizzare, ma per dare un ordine di grandezza reale. Confronto già preparato dal
   Nodo 3 del Blocco C: gli ~86 miliardi di neuroni di un cervello umano contro i
   miliardi di parametri di un modello, e il consumo energetico (20W contro
   megawatt) già nominato lì.

2. **6.2 — Capacità emergenti: quando la quantità diventa qualità**
   Riprende esplicitamente quanto già nominato in Blocco B (Parte 1): capacità che
   non esistono sotto una certa soglia di scala e appaiono, non gradualmente, sopra
   di essa — senza essere state programmate direttamente. Va mantenuto il registro di
   domanda aperta: il meccanismo dell'emergenza resta dibattuto, non va falsamente
   risolto qui.

3. **6.3 — Dati: da dove viene tutto questo testo**
   Apertura con l'arco lungo già piantato in 1.1: l'umanità discretizza e raccoglie
   il proprio sapere scritto da millenni (l'alfabeto come primo atto, molto prima di
   qualunque parola per nominarlo); il concetto diventa consapevole nel Novecento
   (von Neumann, 1958); diventa esplicito e industriale con i progetti di
   digitalizzazione di massa delle biblioteche dei primi anni 2000 — che promettevano,
   in termini allora quasi utopistici, "ogni parola connessa a ogni altra, in un solo
   tessuto". Il testo di addestramento di un LLM è l'ultimo, più grande, anello di
   quello stesso arco: quantità e qualità restano in tensione. Punto di collegamento
   avanti: quello che quei progetti immaginavano tramite semplici link tra pagine, il
   Modulo 5 mostra come si realizzi meccanicamente tramite l'attention — la profezia
   ingenua di un'epoca diventa la descrizione tecnica esatta di un'altra. Accenno
   leggero mantenuto: i dati determinano in parte cosa il modello "sa" e come lo sa,
   collegandosi a "conoscenza compressa nei pesi" già trattato in Blocco B (Parte 2) —
   con possibile chiusura sulla coppia *veritas filia temporis* (Bacone) / *error
   filius temporis* (contro-tesi, via Bayle): l'idea che l'informazione sul mondo
   possa sostituire il mondo, in gran parte anche in modo errato, precede l'AI di
   secoli.

4. **6.4 — Dal modello di base al modello che risponde: il fine-tuning**
   Il pre-addestramento produce un modello di base — un predittore statistico senza
   comportamento conversazionale intrinseco. Il fine-tuning lo adatta con dati più
   piccoli e curati a comportarsi in un modo specifico (seguire istruzioni,
   rispondere in un certo stile).

5. **6.5 — RLHF: insegnare le preferenze, non solo i fatti**
   Come le valutazioni/preferenze umane vengono trasformate in un segnale di
   addestramento ulteriore. Punto pedagogico importante: la "personalità", la
   disponibilità, i rifiuti di un assistente conversazionale vengono soprattutto da
   questa fase — non dal semplice predire-la-parola-successiva. Si ricollega a "cosa
   simulano di saper fare" del Blocco B: anche l'aria di comportamento intenzionale è,
   in parte, un comportamento addestrato.

6. **6.6 — Chiusura del filo discreto/continuo: la quantizzazione**
   Punto di chiusura riservato dal Modulo 4: dopo l'addestramento con pesi continui ad
   alta precisione, i modelli vengono spesso compressi per il deployment riducendo
   deliberatamente la precisione numerica (discretizzando di nuovo) per risparmiare
   memoria ed energia. Chiude il cerchio con l'apertura del Modulo 0 ("il computer non
   capisce niente", tutto è interruttori discreti) e con l'efficienza biologica del
   Nodo 3 di Blocco C — l'intero arco tecnico dei Moduli 1-6 si richiude su se stesso.
   Domanda finale, lasciata volutamente aperta: tutto il corso, da 1.1 in avanti, ha
   trattato il discreto come il livello fisico di base (i transistor) e il continuo come
   un risultato, costruito sopra — qualcosa che *emerge* dal discreto quando la scala è
   sufficiente. Ma esiste una lettura opposta, altrettanto seria: che il continuo sia
   ciò che viene prima, primitivo, e che il discreto sia solo un modo di *misurarlo* o
   *ritagliarlo* — una specie di "derivato" del continuo, non il suo fondamento. In
   questa seconda lettura la quantizzazione non sarebbe un ritorno al discreto
   fondamentale, ma solo un altro modo, tra i tanti possibili, di ritagliare qualcosa che
   resta comunque, alla radice, continuo. Il corso non prende posizione tra le due
   letture — le lascia entrambe sul tavolo, come le altre domande aperte già incontrate.

---

## Filo discreto/continuo — riepilogo dei punti di innesco

Non è una unità a sé, ma un tema ricorrente con punti di innesco mirati, deciso
esplicitamente in conversazione:

- **Modulo 1 (1.1)** — tesi di apertura: la discretizzazione non nasce col computer,
  nasce con la scrittura/l'alfabeto, millenni prima; von Neumann (1958) come momento
  di consapevolezza concettuale.
- **Modulo 1 (1.4)** — battesimo del discreto: simboli finiti senza nozione di
  vicinanza; analogia raster (discreto, interpola/pixela) vs SVG (continuo,
  ricalcola senza perdita) come anticipazione concreta di token vs embedding.
- **Modulo 1 (1.5, nuova unità)** — Gödel: sistemi formali come oggetti discreti ed
  enumerabili; payoff della domanda aperta in Blocco A ("un LLM è un sistema formale
  nel senso di Gödel?"), affrontata con più strumenti ma non richiusa.
- **Modulo 2 (2.2)** — prima crepa: la probabilità come numero reale, gradazione
  prima ancora degli embedding.
- **Modulo 2→3 (2.4→3.1)** — versione più precisa della sparsità: n-grammi come
  insieme denso ma pieno di buchi, embedding come continuo senza buchi — cambio di
  struttura matematica, non solo di quantità di dati. Rafforzato in 3.1 con
  l'argomento diagonale di Cantor (numerabile vs non numerabile) come fondamento
  rigoroso, non solo analogia.
- **Modulo 3 (3.2, 3.4)** — introduzione del termine "embedding"; cenno a Leibniz;
  eco esplicita al passaggio simbolico→connessionista già narrato in Blocco A;
  domanda aperta descrittivismo/costruttivismo sulla geometria del significato, con
  aggancio a Wigner sull'efficacia della matematica.
- **Modulo 4 (4.4)** — punto tecnicamente più alto: la continuità necessaria per il
  gradiente. Non chiuso qui.
- **Modulo 4 (4.5)** — rafforzato con la schismogenesi di Bateson: il backpropagation
  è discreto/globale/offline (corregge prima di agire), non continuo/locale come un
  vero feedback omeostatico — dà un quadro teorico, non solo un'asserzione, alla
  distinzione già presente in C.3.
- **Modulo 5 (5.3)** — eco minore: softmax/pesi che sommano a 1, stesso principio
  della probabilità continua.
- **Modulo 6 (6.3)** — l'arco lungo arriva a destinazione: dall'alfabeto ai corpora
  di addestramento, passando per von Neumann e i progetti di digitalizzazione di
  massa; collegamento avanti al Modulo 5 (l'attention come realizzazione tecnica di
  ciò che quei progetti immaginavano in prosa).
- **Modulo 6 (6.6)** — chiusura: la quantizzazione come ritorno deliberato al
  discreto per efficienza, richiude il cerchio con Modulo 0 e col Nodo 3 di
  Blocco C — ma lasciando aperta, come domanda finale del corso, la lettura opposta
  (il continuo come primitivo, il discreto come suo derivato/misura), senza
  risolverla.

**Secondo filo, minore ma esplicito — Galileo e le qualità primarie/secondarie**:
non è discreto/continuo, ma corre in parallelo tra Modulo 3 e Modulo 5. In 3.2, gli
embedding come estensione radicale del programma galileiano (quantificare anche il
significato, una qualità che sembrava irriducibilmente "secondaria"). In 5.4, il
crollo di quella distinzione con la stessa mossa concettuale della misura quantistica:
l'embedding contestuale non ha un valore fisso indipendente da chi/cosa lo osserva.

**Terzo filo — logica, informazione e biologia della cognizione (Bateson/Varela/Peirce)**:
corre da Modulo 2 a Modulo 4, distinto dal discreto/continuo ma intrecciato con esso.
In 2.2, l'induzione come nome tecnico corretto per "contare per prevedere" (e il
payoff della calibrazione, debito di Blocco B.2). In 3.4, l'abduzione/sillogismo
dell'erba di Bateson come fondamento filosofico dell'aritmetica vettoriale. In 4.1,
Varela e l'autopoiesi come secondo biologo, in contrappunto a Bateson. In 4.3,
pleroma e creatura come domanda aperta su cosa emerga davvero nella profondità. In
4.5, la schismogenesi come quadro teorico per backpropagation vs feedback reale, più
i memristor come corrispettivo hardware reale (non speculativo) della plasticità
biologica.
