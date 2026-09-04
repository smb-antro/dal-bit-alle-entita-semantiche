# Termini grezzi — estrazione dal corso "Come funzionano i LLM"

**Fase 1** del progetto di modellazione ontologica (SKOS+OWL). Lista grezza di termini
candidati per un vocabolario controllato, estratta dalle fonti in sola lettura di
`qa-tool/src/corso-llm/`: `struttura_moduli_1-6.md`, `piano_corso_llm.md`,
`inventario_grafico_moduli_1-6.md`, e i 12 file HTML di `lezioni/` (solo testo in
prosa — titoli, paragrafi, didascalie, note; markup e script ignorati).

Istantanea datata al **26 agosto 2026**. Il corso è materiale non definitivo
(`corso-llm/CLAUDE.md` lo segna come in revisione manuale); questa lista riflette il
suo stato a oggi, non si aggiorna da sola.

**Legenda fonti** (codici usati nella colonna Fonte):

| Codice | Unità didattica |
|---|---|
| `00.A` | Lezione 00.A — Funzioni booleane |
| `00-hw` | Lezione 00 — Hardware e Software |
| `A.1`–`A.6` | Modulo 00, Blocco A — La storia come sequenza di problemi irrisolti |
| `B.1`–`B.3` | Modulo 00, Blocco B — I limiti attuali |
| `C.1`–`C.5` | Modulo 00, Blocco C — Perché ci vuole un villaggio |
| `D.1`–`D.2` | Modulo 00, Blocco D — Lo spazio, il corpo, la macchina |
| `1.1`–`1.5` | Modulo 1 — Il testo come dato |
| `2.1`–`2.4` | Modulo 2 — Probabilità e linguaggio |
| `3.1`–`3.5` | Modulo 3 — Parole come punti nello spazio |
| `4.1`–`4.5` | Modulo 4 — Reti neurali |
| `5.1`–`5.6` | Modulo 5 — Il Transformer |
| `6.1`–`6.6` | Modulo 6 — Cosa significa "Large" |

Criterio di inclusione: menzione esplicita con ruolo didattico/concettuale chiaro. I
casi dubbi sono inclusi comunque, con nota di dubbio esplicita.

---

## 1. Concetto

| Nome | Glossa (in questo corso) | Fonte |
|---|---|---|
| Discretizzazione | Trasformazione di un continuo in simboli finiti ricombinabili; tesi d'apertura: nasce con la scrittura/l'alfabeto, non col computer | 1.1; 6.3; `00-hw` |
| Encoding | Corrispondenza tabellare fissa carattere→numero (ASCII/Unicode); il testo è già numeri prima di ogni LLM | 1.1 |
| Tokenizzazione | Segmentazione del testo in token, unità decise statisticamente e non coincidenti con le parole del dizionario | 1.2, 1.3 |
| Token | Unità minima su cui opera un LLM: parola intera, frammento di parola o carattere | 1.2–1.5 |
| Problema del vocabolario | Impossibilità strutturale di un dizionario fisso di "tutte le parole" (neologismi, errori, nomi propri) | 1.3 |
| ID numerico (token ID) | Numero arbitrario assegnato a ogni token; nessuna relazione di vicinanza con token semanticamente affini | 1.4 |
| Sistema formale | Alfabeto finito di simboli e regole finite per combinarli in dimostrazioni; oggetto discreto ed enumerabile | 1.5; A.2, A.6 |
| Numerabilità / insieme numerabile | Proprietà di un insieme elencabile con metodo sistematico (vocabolario di token, sistema formale); si contrappone al continuo dei reali | 1.5; 3.1 |
| Teorema di incompletezza di Gödel | Nessun sistema formale coerente abbastanza potente può dimostrare tutte le proprie verità aritmetiche | A.2; 1.5 |
| Aritmetizzazione | Mossa di Gödel: codificare simboli, formule e dimostrazioni come numeri, per rendere un sistema autoreferenziale | A.2; 1.5 |
| Test di Turing (Imitation Game) | Sostituzione della domanda "può pensare?" con "può ingannare un osservatore abbastanza a lungo?" | A.2 |
| Separabilità lineare | Proprietà di due insiemi di punti divisibili da una retta/iperpiano; XOR non la possiede | A.3; 4.2 |
| Brittleness (fragilità) | Collasso improvviso, non graduale, di un sistema esperto fuori dal proprio dominio ristretto | A.4 |
| Deep learning | Addestramento praticabile di reti profonde, reso possibile da dati e hardware sufficienti (non da un'idea nuova) | A.5 |
| Probabilità (come numero reale) | Prima "crepa nel discreto": gradazione continua fra 0 e 1, non più solo vero/falso | 2.2 |
| Induzione | Generalizzare da casi osservati (conteggio di frequenze) a una regola probabile, non certa | 2.2 |
| Calibrazione | Proprietà per cui, tra le previsioni fatte con una data confidenza, quella percentuale risulta poi effettivamente corretta | B.2; 2.2 |
| N-gramma | Finestra di N parole di contesto usata per contare e prevedere la parola successiva | 2.3 |
| Assunzione di Markov | Ipotesi che il futuro dipenda solo da una finestra recente e finita del passato, non dall'intera storia | 2.3 |
| Sparsità | Assenza, nei dati, di combinazioni specifiche di contesto: la previsione di un n-gramma si azzera, non si indebolisce | 2.4; 3.1 |
| Dipendenze a lungo raggio | Legami grammaticali fra parole lontane nella frase, invisibili per costruzione a una finestra fissa piccola | 2.4; 5.1 |
| Embedding | Rappresentazione di una parola come vettore/punto in uno spazio continuo: vicinanza spaziale = somiglianza semantica | 3.2 (termine fissato qui); passim |
| Ipotesi distribuzionale | "Si conosce una parola dalla compagnia che tiene" (Firth): il significato si ricava dai contesti d'uso, non da un dizionario | 3.3 |
| Aritmetica vettoriale | Operazioni algebriche fra embedding (es. re−uomo+donna=regina) che producono risultati semanticamente coerenti | 3.4 |
| Sillogismo dell'erba | Ragionare per predicato/direzione condivisa invece che per appartenenza di classe (Bateson); modello filosofico dell'aritmetica vettoriale | 3.4 |
| Abduzione | Inferenza alla spiegazione/analogia più plausibile; il tipo di ragionamento dell'aritmetica vettoriale, distinto da induzione e deduzione | 3.4 |
| Qualità primarie e secondarie | Distinzione di Galileo fra ciò che è quantificabile (forma, numero) e ciò che sembra soggettivo/relazionale (colore, significato) | 3.2; 5.4 |
| Polisemia | Una parola, più significati; limite dell'embedding statico che le assegna un solo vettore fisso | 3.5 |
| Embedding statico | Rappresentazione vettoriale fissa di una parola, identica in ogni frase in cui compare | 3.5; superato in 5.4 |
| Embedding contestuale | Rappresentazione ricalcolata a ogni frase tramite attention; risolve la polisemia | 5.4 |
| Collasso contestuale | Lo spostamento/ricalcolo del vettore di una parola verso il baricentro del significato specifico attivato dal contesto | 5.4 |
| Neurone artificiale | Unità che somma ingressi pesati (più bias) e applica una funzione di attivazione continua | 4.1 |
| Funzione di attivazione (sigmoide) | Funzione continua che schiaccia un numero reale in [0,1], sostituendo la soglia netta booleana | 4.1 |
| Bias (del neurone) | Soglia di base sommata nella combinazione lineare pesata del neurone | 4.1 |
| Autopoiesi | Un sistema vivente come rete chiusa di processi che si automantiene, non un "elaboratore" di input in output (Varela/Maturana) | 4.1 |
| Chiusura operazionale | Un sistema è perturbato dall'ambiente ma non "istruito" in modo trasparente da esso | 4.1 |
| Multi-layer perceptron / strato nascosto | Rete con uno o più strati intermedi che ricodifica lo spazio degli ingressi rendendolo separabile | 4.3 |
| Pleroma e creatura | Distinzione di Bateson (via Jung) fra mondo fisico senza informazione e mondo della comunicazione/forma | 4.3 |
| Funzione di perdita (loss) | Numero singolo che misura quanto una rete sbaglia, dati i pesi correnti; l'oggetto da minimizzare | 4.4 |
| Gradiente | Direzione di massima crescita della perdita in un punto dello spazio dei pesi | 4.5 |
| Discesa del gradiente | Procedura iterativa che aggiorna i pesi nella direzione opposta al gradiente per minimizzare la perdita | 4.5 |
| Minimo locale / minimo globale | Punti di una superficie di perdita in cui la discesa può bloccarsi (locale) o la soluzione migliore (globale) | 4.5 |
| Schismogenesi | Ciclo di retroazione continuo che si autoalimenta durante l'interazione stessa (Bateson, *Naven*); contrapposto al backpropagation offline | 4.5 |
| Plasticità sinaptica | Modifica continua e locale delle sinapsi biologiche, contrapposta all'addestramento discreto e globale artificiale | 4.5; C.3 |
| Attention | Meccanismo per cui ogni parola pesa direttamente ogni altra parola della frase; risolve dipendenze lunghe e staticità insieme | 5.1–5.6 |
| Query, Key, Value | I tre ruoli con cui l'attention confronta (query↔key) e combina (value) le parole di una frase | 5.3 |
| Softmax | Trasformazione dei punteggi di compatibilità grezzi in pesi che sommano a 1 | 5.3 |
| Multi-head attention | Più "teste" di attention in parallelo, ciascuna specializzata su un tipo diverso di relazione | 5.5 |
| Codifica di posizione (positional encoding) | Codice sommato all'embedding che rappresenta la posizione della parola nella frase | 5.5 |
| Parallelismo | Possibilità di calcolare simultaneamente tutti i confronti dell'attention, a differenza dell'elaborazione sequenziale | 5.6 |
| Completamento statistico | Stima del token più probabile dato il testo precedente; l'unica cosa che un LLM fa, alla radice | B.1; 2.1 |
| In-context learning | Apprendere un compito nuovo dentro la stessa conversazione, senza aggiornare alcun peso della rete | B.1 |
| Transfer cross-dominio | Un modello addestrato su testo generico risolve compiti di domini specialistici mai visti in addestramento dedicato | B.1 |
| Capacità emergenti | Capacità che appaiono in modo discontinuo sopra una soglia di scala, non gradualmente | B.1; 6.2 |
| Allucinazione | Invenzione fluente di fatti/citazioni inesistenti; comportamento atteso di un sistema senza fonte di verità esterna | B.2 |
| Metacognizione (simulata) | L'espressione di incertezza ("non lo so") è una stringa di testo probabile in certi contesti, non una stima calibrata interna | B.2 |
| Grounding (symbol grounding problem) | Assenza di riferimento dei simboli al mondo extralinguistico; i simboli si agganciano solo ad altri simboli (Harnad) | B.3; C.1 |
| Ragionamento causale (scala di Pearl) | Tre livelli — associazione, intervento, controfattuale; un LLM opera quasi solo al primo | B.3; C.2 |
| Generalizzazione composizionale | Capacità di combinare pezzi noti in configurazioni nuove in modo sistematico; robusta dentro, fragile fuori distribuzione | B.3 |
| Apprendimento continuo (assente) | Impossibilità per un LLM di aggiornare i propri pesi dall'esperienza conversazionale una volta terminato l'addestramento | B.3 |
| Senso e riferimento | Distinzione di Frege fra l'oggetto reale a cui un'espressione punta e il modo in cui è presentato | C.1 |
| Significato come uso | Tesi del secondo Wittgenstein: il significato di una parola è il suo uso in pratiche sociali condivise ("giochi linguistici") | C.1; 3.3 |
| Stanza cinese | Esperimento mentale di Searle: manipolazione sintattica perfetta senza alcun contenuto semantico | C.1 |
| Problema difficile della coscienza | Perché l'elaborazione dell'informazione sia accompagnata da esperienza soggettiva, non solo da funzione (Chalmers) | C.4 |
| Integrated Information Theory (Φ) | Misura quantitativa dell'informazione integrata, proposta come correlato della coscienza (Tononi); intrattabile a scala realistica | C.4 |
| Global Workspace Theory | La coscienza come trasmissione "globale" di un'informazione a più sistemi cognitivi specializzati (Baars/Dehaene) | C.4 |
| Higher-Order Theories | Uno stato mentale è cosciente solo se esiste, nello stesso sistema, una rappresentazione di secondo ordine su di esso | C.4 |
| Spazio come contenitore assoluto | Concezione newtoniana: palcoscenico fisico indipendente da ciò che lo occupa, misurabile in coordinate | D.1 |
| Spazio come forma dell'intuizione | Lo spazio come struttura imposta dalla mente all'esperienza possibile, non scoperta nel mondo (Kant) | D.1 |
| Spazio vissuto (attraverso il corpo) | Lo spazio come relativo a un corpo situato, orientato, che afferra e si muove (Merleau-Ponty) | D.1 |
| Bayesian brain hypothesis | Il cervello come motore inferenziale che costruisce ipotesi percettive più probabili, non riceve immagini passive | D.1 |
| Gap sensorimotor | Assenza, in un LLM (e in parte in un robot), di un corpo che agisce e percepisce nel mondo fisico | D.2 |
| Robotica embodied | Tesi che l'intelligenza richieda corpi situati capaci di agire, non (solo) rappresentazioni simboliche interne (Brooks) | D.2 |
| Metafore concettuali | Strutture del pensiero astratto con origine sensomotoria esplicita ("capire" = "afferrare") (Lakoff/Johnson) | D.2 |
| Funzione booleana | Funzione che lavora su valori vero/falso, costruita da E, O, NON | `00.A` |
| Tavola di verità | Elenco esaustivo di tutte le combinazioni possibili di ingresso/uscita di una funzione booleana | `00.A` |
| Transistor | Interruttore fisico (passa/non passa corrente) alla base di ogni circuito digitale | `00.A`; `00-hw` |
| Gate logico | Realizzazione fisica degli operatori booleani (AND/OR/NOT) tramite gruppi di transistor | `00-hw` |
| Hardware / software | Distinzione fra il fisico che esegue (lento, massa, energia) e le istruzioni eseguite (copiabili a costo zero) | `00-hw` |
| Sistema esperto | Motore di regole se-allora scritte a mano da un esperto umano; funziona in domini chiusi, fragile fuori (MYCIN, XCON) | A.4 |
| Modello di base | Modello pre-addestrato: puro predittore statistico, senza comportamento conversazionale intrinseco | 6.4 |
| Fine-tuning (come concetto) | Adattamento del comportamento di un modello di base con dati più piccoli e curati | 6.4 |
| RLHF (come concetto) | Trasformazione di preferenze/valutazioni umane in segnale di addestramento ulteriore | 6.5 |
| Modello di ricompensa | Modello secondario addestrato a stimare quanto una risposta piacerebbe a un valutatore umano | 6.5 |
| Quantizzazione (come concetto) | Riduzione deliberata della precisione numerica dei pesi per il deployment, dopo un addestramento a precisione continua | 4.4 (annuncio); 6.6 |
| Parametri / scala | I pesi regolabili di un modello; i tre assi (parametri, dati, calcolo) lungo cui si misura la sua grandezza | 6.1 |
| Irragionevole efficacia della matematica | Formula di Wigner sull'inspiegata efficacia della matematica; applicata all'aritmetica vettoriale | 3.4 |
| Veritas filia temporis / error filius temporis | Coppia aforistica (Bacone/Bayle) su verità ed errore come "figli del tempo"; applicata ai dati di addestramento | 6.3 |

---

## 2. Tecnica/Algoritmo

| Nome | Glossa (in questo corso) | Fonte |
|---|---|---|
| ASCII / Unicode | Tabelle di corrispondenza carattere→numero; ASCII limitata all'inglese, Unicode oltre 149.000 simboli | 1.1 |
| BPE — Byte-Pair Encoding | Algoritmo di tokenizzazione a sotto-parole; nel corso è addestrato realmente sul testo del Modulo 00 | 1.2, 1.3 |
| Diagonale di Cantor (argomento diagonale) | Tecnica dimostrativa: genera, cifra per cifra, un numero assente da qualsiasi lista numerabile data | 1.5; 3.1 |
| Word2Vec | Algoritmo (Mikolov et al., 2013) che apprende embedding prevedendo il contesto di una parola | A.5; 3.3 |
| fastText | Modello di embedding reale (addestrato su italiano) usato per i dataset del corso | 3.2 |
| Backpropagation | Algoritmo che calcola il contributo di ogni peso all'errore finale, propagandolo all'indietro strato per strato | A.5; 4.5 |
| Discesa del gradiente (come algoritmo) | Procedura di ottimizzazione iterativa: piccolo passo nella direzione opposta al gradiente, poi ricalcolo | 4.5 |
| Hidden Markov Model | Modello statistico usato per progressi nel riconoscimento vocale, esempio della "rivincita statistica" | A.4 |
| Support Vector Machine | Metodo di classificazione formalizzato da Vladimir Vapnik | A.4 |
| Reti ricorrenti / LSTM | Elaborazione sequenziale con stato che riassume il passato; tentativo pre-Transformer, limitato su distanze lunghe | A.6 |
| Attention (Bahdanau, 2014-2015) | Meccanismo che permette a una rete di consultare selettivamente tutte le parole dell'input, pesate per rilevanza | A.6; 5.1 |
| Softmax (come tecnica) | Normalizzazione dei punteggi di compatibilità in pesi che sommano a 1 | 5.3 |
| Multi-head attention (come tecnica) | Più insiemi paralleli di query/key/value sulla stessa frase | 5.5 |
| Codifica di posizione (come tecnica) | Somma di un codice posizionale all'embedding di ogni parola | 5.5 |
| Fine-tuning (come tecnica) | Addestramento ulteriore su dataset istruzione→risposta curato (Ouyang et al., 2022) | 6.4 |
| RLHF (come tecnica) | Reinforcement Learning from Human Feedback: classifiche umane → modello di ricompensa → ottimizzazione del modello principale | 6.5 |
| Quantizzazione (livelli: FP32, FP16/BF16, INT8, INT4) | Riduzione della precisione numerica dei pesi in gradi decrescenti per il deployment | 6.6 |
| Reliability diagram (diagramma di calibrazione) | Grafico confidenza dichiarata vs. accuratezza reale, usato per misurare la calibrazione | 2.2 |

---

## 3. Teorico/Autore citato

| Nome | Ruolo nel corso | Fonte |
|---|---|---|
| Gottfried Leibniz | *Characteristica Universalis*, il sogno del pensiero come calcolo; anche calcolo infinitesimale (con Newton) | A.1; 3.2 |
| Isaac Newton | Calcolo infinitesimale (con Leibniz); spazio come contenitore assoluto | 3.2; D.1 |
| George Boole | Algebra della logica (*The Laws of Thought*, 1854); origine degli operatori E/O/NON | A.1; `00.A` |
| Gottlob Frege | Riduzione dell'aritmetica alla logica; distinzione senso/riferimento | A.1; C.1 |
| Bertrand Russell | Paradosso che incrina i *Grundgesetze* di Frege; *Principia Mathematica* con Whitehead | A.1 |
| Alfred North Whitehead | Co-autore di *Principia Mathematica* | A.1 |
| Kurt Gödel | Teoremi di incompletezza (1931); aritmetizzazione | A.2; 1.5 |
| Alan Turing | Macchina universale; Test di Turing; risponde all'obiezione gödeliana | A.2 |
| J.R. Lucas | Riformula l'obiezione gödeliana contro il meccanicismo (1961) | A.2 |
| Roger Penrose | Riprende l'argomento di Lucas, collegandolo alla coscienza | A.2 |
| John McCarthy | Conia "intelligenza artificiale"; proposta di Dartmouth (1956) | A.3 |
| Marvin Minsky | Dartmouth; *Perceptrons* (con Papert, 1969) — dimostra il limite di XOR | A.3 |
| Claude Shannon | Co-firmatario della proposta di Dartmouth | A.3 |
| Nathaniel Rochester | Co-firmatario della proposta di Dartmouth | A.3 |
| Frank Rosenblatt | Costruisce il Perceptron (1958) | A.3; 4.2 |
| Seymour Papert | *Perceptrons* con Minsky (1969) | A.3 |
| David Rumelhart | Articolo del 1986 sul backpropagation (con Hinton e Williams) | A.5 |
| Geoffrey Hinton | Backpropagation (1986); deep learning (2006, con Osindero e Teh) | A.5 |
| Ronald Williams | Articolo del 1986 sul backpropagation | A.5 |
| Simon Osindero | Co-autore con Hinton del metodo 2006 per reti profonde | A.5 |
| Yee-Whye Teh | Co-autore con Hinton del metodo 2006 per reti profonde | A.5 |
| Tomas Mikolov | Guida il gruppo che pubblica Word2Vec (2013) | A.5; 3.3 |
| Dzmitry Bahdanau | Introduce il meccanismo di attention nella traduzione automatica (2014-2015) | A.6 |
| John von Neumann | *The Computer and the Brain* (1958); momento di consapevolezza della discretizzazione | 1.1; 6.3; 4.2 |
| Georg Cantor | Argomento diagonale: i numeri reali non sono numerabili | 1.5; 3.1 |
| Vladimir Vapnik | Formalizza le Support Vector Machines | A.4 |
| Noam Chomsky | Critica ai modelli "a stati finiti" del linguaggio (anni '50), imparentata col limite degli n-grammi | 2.4 |
| John Rupert Firth | Ipotesi distribuzionale: "si conosce una parola dalla compagnia che tiene" (1957) | 3.3 |
| Ludwig Wittgenstein (tardo) | Significato come uso, giochi linguistici | C.1; 3.3 |
| Gregory Bateson | Sillogismo dell'erba; pleroma/creatura; schismogenesi (*Naven*, 1936) | 3.4; 4.3; 4.5 |
| Francisco Varela | Autopoiesi e chiusura operazionale (con Maturana) | 4.1 |
| Humberto Maturana | Autopoiesi (con Varela) | 4.1 |
| Warren McCulloch | Primo modello matematico del neurone (1943, con Pitts) | C.3; 4.1 |
| Walter Pitts | Primo modello matematico del neurone (1943, con McCulloch) | C.3; 4.1 |
| Donald Hebb | Regola di rinforzo delle connessioni ("neurons that fire together, wire together", 1949) | C.3; 4.1 |
| David Hubel | Organizzazione gerarchica della corteccia visiva (con Wiesel, anni '60) | C.3 |
| Torsten Wiesel | Organizzazione gerarchica della corteccia visiva (con Hubel) | C.3 |
| Stevan Harnad | Symbol grounding problem (1990) | B.3; C.1 |
| Judea Pearl | Scala causale: associazione, intervento, controfattuale | B.3; C.2 |
| David Hume | La causalità come inferenza abituale, non percezione diretta | C.2 |
| John Searle | Esperimento mentale della stanza cinese (1980) | C.1 |
| David Chalmers | Problema facile / problema difficile della coscienza (1995) | C.4 |
| Giulio Tononi | Integrated Information Theory (Φ) | C.4 |
| Bernard Baars | Global Workspace Theory | C.4 |
| Stanislas Dehaene | Sviluppo della Global Workspace Theory | C.4 |
| Isaac Newton (spazio) | Vedi sopra — spazio come contenitore assoluto | D.1 |
| Immanuel Kant | Spazio come forma dell'intuizione | D.1 |
| Maurice Merleau-Ponty | Spazio vissuto attraverso il corpo | D.1 |
| Rodney Brooks | Robotica embodied: l'intelligenza richiede corpi, non solo simboli (anni '80) | D.2 |
| George Lakoff | Metafore concettuali a origine sensomotoria (con Johnson) | D.2 |
| Mark Johnson | Metafore concettuali a origine sensomotoria (con Lakoff) | D.2 |
| Galileo Galilei | Qualità primarie/secondarie; fondazione della scienza quantificabile | 3.2; 5.4 |
| Eugene Wigner | "Irragionevole efficacia della matematica" | 3.4 |
| Wei et al. (2022) | Conia il termine "capacità emergenti" | B.1; 6.2 |
| Schaeffer, Miranda, Koyejo (2023) | Controargomento: l'emergenza può essere artefatto delle metriche | B.1; 6.2 |
| Suzana Herculano-Houzel | Stima di ~86 miliardi di neuroni nel cervello umano (2009) | 6.1 |
| Brown et al. (2020) | Paper GPT-3, citato per gli ordini di grandezza dei parametri | 6.1 |
| Chowdhery et al. (2022) | Paper PaLM (Google), citato per gli ordini di grandezza | 6.1 |
| Ouyang et al. (2022) | Paper InstructGPT, introduce il fine-tuning verso il comportamento istruito | 6.4 |
| Francis Bacon | "Veritas filia temporis" — la verità è figlia del tempo | 6.3 |
| Pierre Bayle | Contro-tesi "error filius temporis" — anche l'errore è figlio del tempo | 6.3 |
| William Lawvere | Geometria differenziale sintetica: il continuo come primitivo, il discreto come derivato | 6.6 |
| Carl Gustav Jung | Origine della distinzione pleroma/creatura, ripresa da Bateson | 4.3 (*dubbio — citato solo come fonte della distinzione di Bateson, non come autore trattato per sé*) |
| William Blake | Citato da Bateson a sostegno dell'ipotesi che non esista un pleroma puro | 4.3 (*dubbio — menzione di passaggio, nessun contenuto proprio sviluppato*) |
| C.S. Peirce | Nominato nella struttura come parte del "terzo filo" (logica/informazione/biologia della cognizione) insieme a Bateson e Varela | *dubbio — il nome compare solo nell'intestazione del filo trasversale in `struttura_moduli_1-6.md`, mai nel testo in prosa delle lezioni HTML; l'abduzione (concetto storicamente di Peirce) è discussa in 3.4 senza nominarlo* |
| Autori di "Attention Is All You Need" (Vaswani et al., 2017) | Gruppo di ricercatori a Google, architettura Transformer | A.6; 5.6 (*dubbio — mai nominati singolarmente nel testo, solo "un gruppo di ricercatori a Google"*) |
| Edward Adelson | Illusione della scacchiera, citata come prova della percezione costruttiva | D.1 (*dubbio — menzione di passaggio, un solo esempio fra due*) |
| Müller-Lyer | Illusione ottica citata insieme a quella di Adelson | D.1 (*dubbio — menzione di passaggio*) |

---

## 4. Modulo/Unità

**Modulo 00 — Introduzione narrativa**

- Lezione 00.A — Funzioni booleane
- Lezione 00 — Hardware e Software
- Blocco A — La storia come sequenza di problemi irrisolti
  - A.1 Il sogno di Leibniz / Boole / Frege–Russell–*Principia*
  - A.2 Gödel rompe tutto / Turing / Lucas
  - A.3 Dartmouth / il Perceptron / Minsky e Papert
  - A.4 Sistemi esperti / il secondo inverno / la rivincita statistica
  - A.5 Backpropagation / deep learning / Word2Vec
  - A.6 L'attenzione e il salto finale (chiusura del blocco)
- Blocco B — I limiti attuali come mappa del territorio inesplorato
  - B.1 Cosa sanno fare davvero
  - B.2 Cosa simulano di saper fare
  - B.3 Cosa non sanno fare affatto
- Blocco C — Perché ci vuole un villaggio
  - C.1 Il problema del significato
  - C.2 Il problema della causalità
  - C.3 Il problema biologico
  - C.4 Il problema della coscienza
  - C.5 Chiusura del blocco
- Blocco D — Lo spazio, il corpo, la macchina
  - D.1 Cos'è lo spazio? Il corpo come strumento di misura
  - D.2 Chiusura del blocco e del Modulo 00 narrativo

**Modulo 1 — Il testo come dato**: 1.1 encoding · 1.2 tokenizzazione · 1.3 problema del vocabolario · 1.4 dagli ID al punto più discreto · 1.5 Gödel

**Modulo 2 — Probabilità e linguaggio**: 2.1 prevedere la parola successiva · 2.2 unigrammi/bigrammi, induzione, calibrazione · 2.3 n-grammi e assunzione di Markov · 2.4 sparsità e dipendenze lontane

**Modulo 3 — Parole come punti nello spazio**: 3.1 il problema lasciato aperto · 3.2 le parole come vettori (embedding) · 3.3 l'ipotesi distribuzionale · 3.4 l'aritmetica vettoriale · 3.5 polisemia ed embedding statico

**Modulo 4 — Reti neurali**: 4.1 dal neurone biologico al neurone artificiale · 4.2 il perceptron e XOR · 4.3 strati e profondità · 4.4 la funzione di perdita · 4.5 il gradiente e la backpropagation

**Modulo 5 — Il Transformer**: 5.1 il problema che l'attenzione risolve · 5.2 l'idea dell'attention · 5.3 Query, Key, Value · 5.4 embedding contestuale · 5.5 multi-head e posizione · 5.6 parallelismo e scala

**Modulo 6 — Cosa significa "Large"**: 6.1 scala · 6.2 capacità emergenti · 6.3 i dati · 6.4 fine-tuning · 6.5 RLHF · 6.6 quantizzazione (chiusura dell'arco tecnico)

---

## 5. Dataset/Asset concettualmente rilevante

| Nome | Descrizione | Fonte / file |
|---|---|---|
| Vocabolario BPE del corso | 334 simboli (34 caratteri base + 300 unioni apprese), addestrato realmente sul testo del Modulo 00 | 1.2–1.4; `bpe_merges_modulo1.json` |
| Corpus di 46 frasi italiane | Corpus fisso scritto apposta per il predittore n-grammi (34 frasi di training, 12 di test) | 2.1–2.4; `ngram_dati_modulo2.json` |
| Dati di calibrazione (reliability diagram) | 65 previsioni reali raggruppate in 3 bucket di confidenza, misurate sul corpus di 46 frasi | 2.2; `calibrazione_modulo2.json` |
| Embedding fastText di 23 parole italiane | Vettori reali a 300 dimensioni, proiettati in 2D per esplorazione, aritmetica e polisemia | 3.2, 3.4, 3.5, 5.4; `embedding_dati_moduli_3_5.json` |
| Diagonale di Cantor interattiva | Griglia di cifre con costruzione del numero che sfugge a qualunque lista | 1.5; `cantor_diagonale_modulo1.json` |
| Rete XOR addestrata realmente | Multi-layer perceptron addestrato per davvero via backpropagation, 4/4 corretto, confine di decisione curvo | 4.2, 4.3; `xor_rete_modulo4.json` |
| Paesaggio di perdita a due minimi | Superficie di loss con minimo globale e locale, resa come shader GLSL/SDF (unica eccezione al vanilla JS) | 4.4, 4.5; `paesaggio_perdita_modulo4.json` |
| Esempi di neurone singolo | Pesi/ingressi regolabili a slider, variante continua del calcolatore booleano | 4.1; `neurone_esempi_modulo4.json` |
| Dati di attention illustrativi | Pesi scritti a mano per chiarezza pedagogica — esplicitamente *non* output di un vero Transformer | 5.2–5.5; `attention_dati_modulo5.json` |
| Confronto modello di base / fine-tuned | Stesso prompt, due risposte, per illustrare l'effetto di fine-tuning e RLHF | 6.4, 6.5; `base_vs_tuned_modulo6.json` |
| Curva illustrativa delle capacità emergenti | Andamento piatto-poi-salto per un compito tipo (aritmetica a più cifre); esplicitamente non dati misurati da un paper specifico | 6.2; `capacita_emergenti_modulo6.json` |
| Slider di scala logaritmica | Confronto parametri/dati (GPT-3, PaLM) con il cervello umano (~86 miliardi di neuroni) | 6.1; `scala_modulo6.json` |
| Timeline storica alfabeto→corpora LLM | Alfabeto → von Neumann (1958) → digitalizzazione di massa (anni 2000) → corpora di addestramento oggi | 6.3; `timeline_modulo6.json` |
| Livelli di quantizzazione | FP32 → FP16/BF16 → INT8 → INT4, con riferimento a strumenti reali (llama.cpp) | 6.6; `quantizzazione_modulo6.json` |
| Confronto raster/SVG | Slider di zoom fra immagine raster che pixela e forma SVG che resta nitida; anticipa token vs. embedding | 1.4 |
| Calcolatore booleano interattivo | Interruttori A/B che mostrano dal vivo E, O, NON, XOR e F = (A∧B)∨¬A | `00.A` |

---

## 6. FiloTrasversale

| Nome | Descrizione | Punti di innesco principali |
|---|---|---|
| Discreto/continuo | Filo portante del corso: dal computer come interruttori discreti alla domanda finale su cosa sia "primitivo" fra discreto e continuo | 1.1, 1.4, 1.5, 2.2, 2.4→3.1, 3.2, 3.4, 4.4, 4.5, 5.3, 6.3, 6.6 |
| Galileo e le qualità primarie/secondarie (crollo quantistico) | Da "quantificare il significato" (3.2, estensione del programma galileiano) al crollo di quella stessa distinzione con l'embedding contestuale, analogo alla misura quantistica (5.4) | 3.2, 5.4 |
| Logica, informazione e biologia della cognizione | Da induzione (2.2) ad abduzione/sillogismo dell'erba (3.4), autopoiesi (4.1), pleroma/creatura (4.3), schismogenesi e memristor (4.5) | 2.2, 3.4, 4.1, 4.3, 4.5 |

---

## 7. Relazioni osservate

| Sorgente | Relazione | Destinazione | Nota / fonte |
|---|---|---|---|
| Tokenizzazione | è prerequisito di | Embedding | Il Modulo 1 chiude sul problema (ID senza vicinanza) che il Modulo 3 risolve — 1.4→3.1 |
| ID numerico (token ID) | è analogo a | Immagine raster | Insieme fisso, senza nulla "nel mezzo" — 1.4 |
| Embedding | è analogo a | Immagine vettoriale (SVG) | Spazio continuo, ricalcolabile in ogni punto — 1.4 |
| Vocabolario discreto di token | è numerabile, a differenza di | Spazio di embedding a valori reali | Fondamento rigoroso via diagonale di Cantor, non solo analogia — 1.5, 3.1 |
| Sistema formale gödeliano | si applica potenzialmente a | LLM (vocabolario finito, pesi finiti) | Domanda esplicitamente lasciata aperta, non risolta — 1.5 |
| Sparsità (n-grammi) | è spiegata da | Assenza di vicinanza nei simboli discreti | La sparsità del Modulo 2 non è un difetto di quantità ma di rappresentazione — 3.1 |
| Perceptron (a uno strato) | non risolve | XOR | Limite geometrico di separabilità lineare, non correggibile con più addestramento — A.3, 4.2 |
| Multi-layer perceptron | risolve | XOR | Lo strato nascosto ricodifica lo spazio rendendolo separabile — 4.3 |
| Backpropagation | è prerequisito di | Discesa del gradiente (su reti profonde) | L'algoritmo del 1986 rende allenabili le reti a più strati — A.5, 4.5 |
| Attention | risolve | Dipendenze a lungo raggio | Ogni parola raggiunge ogni altra in un passo solo — 5.1 |
| Attention | risolve | Embedding statico / Polisemia | La rappresentazione si ricalcola frase per frase — 5.1, 5.4 |
| Softmax | è analogo a | Probabilità (Modulo 2) | Stessa struttura matematica: pesi che sommano a 1 — 5.3 |
| Aritmetica vettoriale | esemplifica | Sillogismo dell'erba / Abduzione | Ragionamento per predicato condiviso, non deduzione — 3.4 |
| N-grammi (contare per prevedere) | esemplifica | Induzione | Generalizzare da casi osservati senza certezza — 2.2 |
| Calibrazione | si applica a | Probabilità in uscita da un modello | Debito aperto in B.2, saldato in 2.2 — B.2, 2.2 |
| Embedding contestuale | si contrappone a | Embedding statico | Il valore non esiste prima del calcolo nel contesto — 3.5, 5.4 |
| Embedding contestuale | è analogo a | Misura quantistica (crollo della funzione d'onda) | Il vettore assume valore solo al momento del calcolo col contesto — 5.4 |
| Qualità primarie e secondarie (Galileo) | si applica a | Embedding (Modulo 3) | Quantificare il significato, qualità "secondaria" per eccellenza — 3.2 |
| Ipotesi distribuzionale (Firth) | rende operativa | Significato come uso (Wittgenstein) | "Il significato è la distribuzione dei contesti" riscrive in forma calcolabile "il significato è l'uso" — 3.3, C.1 |
| Grounding | si collega a | Gap sensorimotor | Il grounding mancante è, in gran parte, grounding sensorimotorio (Brooks) — B.3, D.2 |
| Ragionamento causale (Pearl) | si collega a | Inferenza causale (Hume) | Anche l'inferenza umana è indiretta: dove sta davvero la differenza? — C.2 |
| Backpropagation | si contrappone a | Schismogenesi / Plasticità sinaptica | Procedura offline, discreta, globale contro feedback continuo e locale — 4.5, C.3 |
| Memristor | esemplifica | Plasticità sinaptica continua e locale | Corrispettivo hardware reale, non speculativo — 4.5 |
| Autopoiesi (Varela) | dà vocabolario preciso a | "I pesi non contengono i dati in modo trasparente" (Blocco B) | 4.1, B.2 |
| Diagonale di Cantor | è fondamento di | Non numerabilità dello spazio di embedding | Non è un'analogia di stile, è la stessa distinzione matematica — 1.5, 3.1 |
| Gödel (teorema di incompletezza) | è prerequisito concettuale di | "Un LLM è un sistema formale gödeliano?" | Domanda piantata in A.2, ripresa con più strumenti in 1.5 | 
| Turing | riformula | Il sogno di Leibniz/Boole/Frege (pensiero come calcolo) | Sostituisce "può pensare?" con "può ingannare?" — A.2 |
| Lucas | riprende contro | Turing (risposta all'obiezione gödeliana) | L'obiezione matematica torna più aggressiva — A.2 |
| Penrose | riprende | Lucas (argomento gödeliano) | Collegato esplicitamente alla coscienza — A.2 |
| Stanza cinese (Searle) | esemplifica critica a | Sistema puramente simbolico / Grounding | Manipolazione sintattica senza comprensione — C.1 |
| Firth | è analogo a | Wittgenstein (significato come uso) | Stesso principio, reso operativo/misurabile — 3.3 |
| Modulo 00 Blocco A | pianta domande riprese in | Modulo 1 Unità 1.5, Modulo 4 Unità 4.2-4.3 | Gödel→1.5; XOR/profondità→4.2-4.3 — A.2, A.3, A.5 |
| Blocco B (domande aperte) | trova disciplina in | Blocco C (i quattro nodi) | Ogni domanda di B indica una tradizione di ricerca in C — B.1-B.3, C.1-C.4 |
| Blocco C, Nodo 1 (grounding) | è raccordo diretto a | Blocco D (corpo e spazio) | Il grounding mancante è grounding sensorimotorio — C.1, D.2 |
| Capacità emergenti (Wei et al.) | è messo in discussione da | Schaeffer et al. (2023) | L'emergenza può essere artefatto della metrica, non del modello — B.1, 6.2 |
| Modello di base | è prerequisito di | Fine-tuning | Il fine-tuning parte dal modello di base pre-addestrato — 6.4 |
| Fine-tuning | è prerequisito di | RLHF | L'RLHF agisce su un modello già adattato a seguire istruzioni — 6.4, 6.5 |
| Quantizzazione | si contrappone a | Pesi continui (addestramento) | Ritorno deliberato al discreto per efficienza di deployment — 4.4, 6.6 |
| Von Neumann (1958) | è analogo, nello stesso anno, a | Rosenblatt / Perceptron (1958) | Coincidenza esplicitamente notata nel testo, non causale — 1.1, 4.2 |
| GPU (hardware) | rende possibile | Attention / Transformer (parallelismo) | Il Transformer vince anche perché coincide con la forma di calcolo delle GPU — `00-hw`, A.6, 5.6 |
| Word2Vec | esemplifica | Capacità emergenti (struttura non progettata) | L'aritmetica vettoriale emerge senza essere stata codificata a mano — A.5, B.1 |

---

## Note di revisione

**Casi dubbi segnalati** (vedi anche le note inline nella tabella Teorico/Autore citato):
C.S. Peirce (nominato solo nell'intestazione del filo trasversale nel documento di struttura,
mai nel testo in prosa delle lezioni); gli autori di "Attention Is All You Need" (mai
nominati singolarmente, solo come "gruppo di ricercatori a Google"); Jung e Blake (citati
di passaggio da Bateson, senza contenuto proprio sviluppato); Adelson e Müller-Lyer
(esempi di illusioni ottiche citati in un solo passaggio).

**Punti del corso più eterogenei da modellare** (segnalati per la Fase 2):
il Blocco C (quattro nodi disciplinari molto diversi — filosofia del linguaggio, statistica,
neuroscienze, filosofia della mente — tenuti insieme solo dal fatto di rispondere ciascuno
a una domanda del Blocco B) e il filo "logica, informazione e biologia della cognizione"
(Bateson/Varela/Peirce), che attraversa concetti eterogenei (induzione, abduzione,
autopoiesi, pleroma/creatura, schismogenesi) con un grado di coesione più debole rispetto
al filo discreto/continuo, esplicitamente più centrale e meglio strutturato nelle fonti.
