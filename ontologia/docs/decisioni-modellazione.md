# Decisioni di modellazione

Questo è il deliverable primario del progetto, non un'appendice tecnica. Il vocabolario
controllato e la micro-ontologia (`src/*.ttl`) e la struttura di consultazione
(`output/`) dimostrano che so costruire un modello formale e derivarne un'architettura
di consultazione. Quello che li distingue da un esercizio di sintassi è qui: dove il
modello ha dovuto scegliere fra due strade entrambe difendibili, perché ho preso quella
che ho preso, e che cosa quella scelta ha lasciato fuori. Ogni sezione segue lo stesso
schema — la scelta, l'alternativa scartata, il costo accettato.

Il dominio è il saggio interattivo "Dal bit alle entità semantiche"
(`~/projects/cartografia-semantica/src/saggio/`, sola lettura, non modificato — nato
come corso "Come funzionano i LLM" dentro `qa-tool/`, estratto ed evoluto in saggio il
2 settembre 2026). Le decisioni di **avvio** del progetto — perché questo dominio, la
verifica dei tre vincoli (diritti, nessun dato di terzi, complessità sufficiente), il
bootstrap del repository — sono in `docs/decision-log.md`, che tiene la cronologia dei
fatti; questo documento tiene invece le decisioni di modellazione vere e proprie,
organizzate per argomento, non per data. La sezione finale, "Aggiornamento
post-estrazione", raccoglie le decisioni prese quando il dominio è cambiato sotto al
modello già costruito.

## 1. Che cos'è un termine del vocabolario, e cosa non lo è

Il primo problema di ogni vocabolario controllato non è come organizzare i termini, ma
decidere cosa è un termine. Il corso nomina concetti, tecniche, persone, unità
didattiche, dataset — solo la prima categoria è finita dentro `skos:Concept`.

**I teorici citati non sono skos:Concept.** Il corso cita 61 persone, da Leibniz a
Lawvere. SKOS è un vocabolario di *termini/soggetti*, non di *entità nominate*: un
teorico non è un concetto che si "comprende" nel senso in cui si comprende l'embedding
o la calibrazione, è un riferimento, un agente. Mescolare i due tipi avrebbe fatto
usare `skos:broader` indifferentemente sia per gerarchie concettuali
(Embedding→Embedding contestuale) sia per relazioni di attribuzione
(Bateson→pleroma/creatura), perdendo la distinzione fra le due cose. I teorici sono
diventati individui OWL di una classe `Teorico` a sé (§3), collegati ai concetti da
proprietà tipizzate come `teorizzatoDa`. Costo accettato: chi legge solo
`vocabolario.ttl` non vede un solo nome proprio — li vede solo nella struttura di
consultazione finale, che unisce i due livelli.

**Moduli e unità non sono skos:Concept**, per la stessa ragione: "Modulo 3" o "Unità
B.2" non sono termini del dominio, sono la struttura organizzativa del corpus sorgente.
In Fase 2 ho introdotto solo una property-ponte leggera (`:fonte`, stringa) invece di
anticipare già lì una gerarchia Modulo→Unità in OWL — la avrei dovuta rifare se lo
schema OWL fosse risultato diverso da come l'avrei abbozzato a quel punto, ancora prima
di progettare le classi (§3).

**Otto doppioni concetto/tecnica sono stati fusi in un solo nodo.** L'estrazione dei
termini grezzi aveva prodotto, per otto voci (Attention, Softmax, Multi-head attention,
Codifica di posizione, Fine-tuning, RLHF, Quantizzazione, Discesa del gradiente), due
righe separate — una come "concetto", una come "tecnica" — perché il corso ne parla sia
come idea sia come procedura. Ho unificato ciascuna coppia in un solo `skos:Concept`
con uno `scopeNote` capace di coprire entrambi gli aspetti, invece di creare coppie
parallele (`:Attention` + `:AttentionComeTecnica`): la distinzione concetto/tecnica non
è una proprietà del *termine*, è un aspetto descrittivo, e moltiplicare i nodi avrebbe
raddoppiato la manutenzione (due prefLabel, due fonti da tenere sincronizzate) senza
un guadagno reale di espressività. Chi cerca "qual è la differenza fra l'Attention come
idea e come algoritmo?" non trova un confronto esplicito — deve dedurlo dallo
scopeNote unico. La stessa disciplina "un solo nodo per termine" è tenuta anche in
Fase 3: quando la micro-ontologia distingue davvero le tecniche (§3), lo fa con un
**tipo aggiuntivo** sullo stesso nodo (`rdf:type :Tecnica`), non con un nodo duplicato.

**I casi dubbi restano fuori.** Nell'estrazione iniziale, alcuni nomi (C.S. Peirce, gli
autori di *Attention Is All You Need*, Jung, Blake, Adelson, Müller-Lyer) erano stati
segnalati come menzioni troppo marginali per un nodo proprio — o perché comparivano
solo nell'intestazione di un raggruppamento tematico e mai nel testo delle lezioni, o
perché citati di sfuggita da un altro autore. Nessuno di questi è diventato un nodo,
né come `skos:Concept` né, più tardi, come individuo `Teorico`: restano visibili solo
indirettamente, dentro lo scopeNote del concetto a cui sono associati (es. "Pleroma e
creatura" nomina Bateson via Jung, ma Jung non ha una pagina propria).

## 2. La disciplina della gerarchia

Un vocabolario controllato vale quanto la disciplina con cui distingue "è un tipo di"
da "è collegato a". Ho tenuto tre regole ferme in tutte le 111 voci.

**`skos:broader`/`narrower` modella solo genere-specie o parte-tutto — mai
prerequisito, causa, o uso.** Anche quando l'ordine con cui il corso presenta due
concetti renderebbe tentante annidarli. Esempi accettati, perché genuinamente is-a o
parte-tutto: `Embedding` → `Embedding statico`/`Embedding contestuale` (sono tipi di
embedding); `Attention` → `Query/Key/Value`, `Softmax`, `Multi-head attention`,
`Codifica di posizione`, `Parallelismo` (sono componenti del meccanismo, non fasi
esterne ad esso); `Teorema di incompletezza di Gödel` → `Aritmetizzazione` (la mossa
tecnica è parte della dimostrazione); `Autopoiesi` → `Chiusura operazionale` (proprietà
costitutiva, non prerequisito esterno); `RLHF` → `Modello di ricompensa` (componente
strutturale); `Funzione di perdita` → `Gradiente`, `Minimo locale/globale` (proprietà
matematiche intrinseche della funzione stessa, non concetti che la usano).

Esempi **scartati** deliberatamente, perché la relazione reale non è is-a: `Discesa
del gradiente` non è narrower di `Gradiente` — la discesa *usa* il gradiente, non ne è
un tipo (tenuti come fratelli sotto lo stesso genitore tematico). `Reliability
diagram` non è narrower di `Calibrazione` — è uno strumento di misura *per* la
calibrazione, non un tipo di calibrazione (stessa scelta per `Tavola di verità` sotto
`Funzione booleana`, e per `Gate logico` sotto `Transistor`, dove per di più la
direzione meronomica sarebbe stata invertita rispetto a quella intuitiva — un gate è
*composto da* transistor, non il contrario). Il costo di questa disciplina è una
gerarchia più piatta di quanto un lettore abituato a tassonomie profonde potrebbe
aspettarsi — un guadagno, non una perdita: una gerarchia artificialmente profonda
avrebbe comunicato relazioni che il corso non sostiene.

**Solo `skos:broader` è asserito, mai `skos:narrower`.** Sono l'una l'inversa
dell'altra per definizione SKOS; mantenerle entrambe a mano avrebbe voluto dire tenere
sincronizzate due copie della stessa informazione, con un rischio concreto di
disallineamento silenzioso via via che il file cresceva. Qualunque tool SKOS-aware (o
una query SPARQL con proprietà inversa) deriva la direzione mancante.

**Le relazioni tipizzate osservate nel corso (prerequisito-di, analogo-a,
si-contrappone-a, esemplifica, risolve...) non sono confluite in `skos:related`
generico.** `skos:related` è deliberatamente debole in SKOS: comprimerle tutte lì
avrebbe appiattito distinzioni che il corso rende esplicite e utili — "Attention
*risolve* le dipendenze a lungo raggio" dice più di un generico "Attention *è
collegata a* dipendenze a lungo raggio". Restano riservate a object property OWL
tipizzate (§3), applicate agli stessi URI di concetto già definiti — non ha richiesto
una riscrittura del vocabolario, solo un livello aggiunto sopra.

**I tre fili trasversali del corso sono `skos:OrderedCollection`, non
`skos:Concept`.** Un filo (es. discreto/continuo) non è un termine che si definisce, è
un percorso di lettura attraverso concetti definiti altrove — modellarlo come concetto
gli avrebbe dato un posto falso nella gerarchia (non è né più generale né più
specifico di "Embedding", la attraversa trasversalmente). Ordinata, non una collection
semplice, perché il corso presenta i fili come sequenze narrative con un prima e un
dopo. Dichiarato senza nasconderlo, nello scopeNote stesso della collection: il filo
"logica, informazione e biologia della cognizione" (induzione→abduzione→autopoiesi→
pleroma/creatura→schismogenesi) è più debolmente coeso degli altri due — collega
tradizioni diverse (statistica, biologia, cibernetica) più per prossimità pedagogica
nel corso che per una vera parentela concettuale. L'ho mantenuto perché il corso lo
tratta esplicitamente come un filo unico, ma la sua coerenza interna resta più debole
di quella del filo discreto/continuo.

## 3. Dove finisce il vocabolario e comincia l'ontologia

**`:Concetto` coincide con `skos:Concept`** (`owl:equivalentClass`), non è una classe
OWL parallela con propri individui da ricreare: i 111 nodi di Fase 2 diventano
automaticamente istanze di `:Concetto` senza toccare quel file. `:Tecnica` è
sottoclasse di `:Concetto`, non una categoria alternativa — coerente con la scelta del
§1 di non duplicare nodi: i termini già unificati ricevono qui un tipo aggiuntivo (18
individui), non un secondo nodo.

**Ho aggiunto la classe `Unità`, non prevista nel piano approvato**, che elencava solo
`Modulo`. Il corso ha davvero due livelli di struttura (Modulo 3 → Unità 3.4), non
uno: comprimerli in una sola classe avrebbe perso l'informazione di contenimento
(`partOfModulo`, funzionale — un'unità appartiene a esattamente un modulo). Uno
scostamento dal piano dichiarato esplicitamente, non un'aggiunta silenziosa. Ho
lasciato fuori un terzo livello per il "Blocco" (A, B, C, D del Modulo 00): avrebbe
reso lo schema asimmetrico (un livello in più solo per un modulo su sette) per un
guadagno marginale — "tutte le unità del Blocco C" resta comunque ricavabile filtrando
per prefisso del codice unità. Il nome del blocco vive solo in un `rdfs:comment`.

**Le sei object property del piano approvato sono diventate 15 più 2 datatype
property.** Il piano proponeva `prerequisitoDi`, `esemplificaTecnica`, `partOfModulo`,
`discussoIn`, `contrappostoA`, `citaOpera` — scelte prima di vedere le relazioni reali
estratte dal corso. Confrontate con i dati erano insufficienti (mancavano `risolve`,
`analogoA`, `spiegataDa`, `teorizzatoDa`...) e in un caso mal indirizzate
(`esemplificaTecnica` presupponeva che solo le tecniche esemplificassero qualcosa,
mentre anche concetti puramente teorici lo fanno). Non è un ritocco cosmetico dei sei
nomi originali: è uno schema ridisegnato sui dati, con dominio/codominio e
caratteristiche OWL (transitiva, simmetrica, funzionale) assegnate proprietà per
proprietà. Ho comunque scelto di perdere qualcosa per non moltiplicare le proprietà
oltre un certo punto: "rende operativa un'idea" e "dà vocabolario preciso a
un'osservazione" — due formulazioni diverse nel corso — condividono la stessa
struttura logica (una formalizzazione successiva di un'idea preesistente) e sono
confluite in un'unica `rendeOperativo`; e `riprendeArgomentazioneDi` è rimasta solo
Teorico→Teorico, non estesa a Teorico→Concetto, per non aggiungere una proprietà per
sole 2-3 relazioni marginali (Turing/Lucas/Penrose).

**Lo stato epistemico di un dataset è una classe enumerata (`owl:oneOf`), non una
stringa libera** come abbozzato nel piano iniziale. Il corso stesso tratta questa
distinzione — dato reale e verificato algoritmicamente contro dato dichiaratamente
illustrativo — come un'alternativa chiusa e ricorrente, dichiarata esplicitamente nei
metadata di più file `.json` sorgente (i pesi di attention del Modulo 5 sono
etichettati come illustrativi; il BPE e gli embedding fastText, come reali). Una
classe chiusa a due individui (`:Reale`, `:Illustrativo`) rende quella chiusura
verificabile da un reasoner; una stringa libera l'avrebbe solo descritta senza
poterla far rispettare.

**`Concetto`, `Teorico`, `Modulo`, `Unità`, `Dataset`, `FiloTrasversale` sono
dichiarati reciprocamente disgiunti** (`owl:AllDisjointClasses`). Non è burocrazia:
formalizza in un assioma verificabile due decisioni già prese a parole nel §1 — i
teorici non sono concetti, moduli e unità non sono concetti — invece di lasciarle solo
dichiarate in un commento. L'ho verificato con un reasoner OWL-RL reale (`owlrl`), non
solo controllando che il file parsi: la chiusura deduttiva del grafo completo (schema +
dati) passa da 1703 a 3562 triple, l'individuo `Bpe` (tipizzato `:Tecnica`) viene
correttamente inferito anche come `:Concetto` via `rdfs:subClassOf`, e nessuna istanza
risulta inferita come `owl:Nothing` — lo schema è internamente coerente, non solo
sintatticamente valido. Rischio dichiarato: `owl:AllDisjointClasses` è un costrutto
OWL2 relativamente recente; se un altro strumento di validazione lo ignorasse in
silenzio, andrebbe sostituito con 15 coppie esplicite di `owl:disjointWith` — per ora
il reasoner usato lo rispetta correttamente.

## 4. Popolare senza inventare

Popolare un modello con dati reali è dove la tentazione di completare i vuoti con la
propria conoscenza generale è più forte — e dove ho scelto di resisterle con più
disciplina.

**Il popolamento è generato da script, lo schema è scritto a mano.** A differenza del
vocabolario e dell'ontologia (Turtle scritto direttamente, per capire ogni assioma),
`src/dati.ttl` è generato da `scripts/genera_dati.py`. Le decisioni restano mie — chi è
un Teorico, quale relazione osservata diventa quale proprietà OWL, quale dataset è
"reale" — ma sono scritte come strutture dati Python esplicite dentro lo script, non
come Turtle a mano: a questa scala (~200 individui, 259 triple `discussoInUnita`)
trascriverle a mano avrebbe significato ricopiare centinaia di triple strutturalmente
identiche — un lavoro meccanico a rischio di errori di trascrizione più che di
modellazione. È rigenerabile in modo deterministico da un comando singolo.

**Le 111 stringhe `:fonte` scritte in Fase 2 sono state espanse a mano, non con un
parser regex generico.** Avevano formati non uniformi — intervalli con trattino,
gruppi separati da `;` o `,`, annotazioni fra parentesi come `"4.4 (annuncio)"` — e un
parser generico avrebbe rischiato di sbagliare in silenzio proprio su un'eccezione come
questa. 111 righe scritte guardando ciascun valore sono verificabili una per una;
risultato: 0 codici non risolti, 259 triple `discussoInUnita` generate.

**Le citazioni bibliografiche (`citaOpera`) sono popolate solo da fonti già
verificate del progetto** — `termini-grezzi.md` o `qa-tool/docs/decision-log.md`, mai
completate con la mia conoscenza generale di questi lavori, anche quando disponibile e
probabilmente corretta. Dove la fonte dà solo un anno o un descrittore informale (Brown
et al. "paper GPT-3", Cantor, Rosenblatt, Mikolov, Bahdanau), `citaOpera` resta vuoto.
Il punto dell'intero progetto è la tracciabilità al corpus di origine, non
l'accuratezza bibliografica assoluta: integrare da fuori avrebbe messo nel grafo
affermazioni non verificabili contro le fonti dichiarate — esattamente il tipo di
errore che un vocabolario controllato dovrebbe rendere impossibile, non commettere lui
stesso.

**I riferimenti collettivi restano un solo individuo.** "Wei et al. (2022)",
"Schaeffer, Miranda, Koyejo (2023)", "Brown et al. (2020)", "Chowdhery et al. (2022)",
"Ouyang et al. (2022)" sono un solo `Teorico` ciascuno (il gruppo/paper), non scomposti
nei singoli coautori: il corso stesso li cita così, e scomporli avrebbe richiesto
informazioni che il corso non fornisce.

**Un dataset costruito può essere "Reale" se il suo comportamento è verificato,
anche senza provenire da un modello di produzione.** Il "Paesaggio di perdita a due
minimi" (Modulo 4.4/4.5) è una superficie costruita apposta (due gaussiane invertite),
non misurata — ma il comportamento della discesa del gradiente su di essa è stato
verificato numericamente (convergenza corretta da due punti di partenza diversi). Ho
preferito questa lettura di "Reale" — verificato, non fabbricato ad hoc — a
un'improbabile terza categoria "costruito-ma-verificato" che sarebbe servita per un
solo caso su sedici: la classe `StatoEpistemico` resta a due soli valori, con la
distinzione dichiarata nel commento dell'individuo.

**Non tutte le relazioni osservate nel corso sono diventate una tripla — i gap sono
dichiarati, non colmati inventando nodi.** Il destinatario di alcune relazioni non
corrisponde a un nodo esistente nel modello, e forzarlo avrebbe distorto il
vocabolario costruito nei passi precedenti:

- "ID numerico è analogo a immagine raster" / "Embedding è analogo a immagine
  vettoriale" — raster e SVG non sono concetti, sono il dataset illustrativo
  `ConfrontoRasterSvg`.
- "Sistema formale gödeliano si applica potenzialmente a un LLM" — "LLM" come sistema
  complessivo non è un nodo del modello, che descrive i suoi concetti costitutivi, non
  l'oggetto "LLM" nel suo insieme.
- "GPU rende possibile Attention/Transformer" e "Memristor esemplifica plasticità
  sinaptica" — né GPU né Memristor sono mai stati estratti come Concetto/Tecnica a sé;
  comparivano solo dentro queste relazioni. Segnalati come lacune di estrazione, non
  colmati a posteriori.
- "Von Neumann e Rosenblatt, coincidenza di anno (1958)" — dichiaratamente non causale
  nel testo del corso; nessuna delle proprietà Teorico→Teorico definite
  (`riprendeArgomentazioneDi`, pensata per risposte argomentative) si adatta a una
  coincidenza cronologica, e forzarla in una di esse sarebbe stato scorretto.
- "Ragionamento causale (Pearl) si collega a inferenza causale (Hume)" — Hume è un
  Teorico, non un Concetto, e `collegatoA` è scoperto Concetto-Concetto per disegno;
  la connessione resta catturata solo indirettamente (`RagionamentoCausale
  teorizzatoDa Pearl`).
- BPE non ha `teorizzatoDa` verso Sennrich et al.: quel nome compare nello scopeNote
  del vocabolario ma non è mai stato estratto come Teorico — un'incoerenza minore fra
  i due livelli, segnalata qui invece che corretta in silenzio aggiungendo un
  individuo mai passato dal processo di estrazione.

**La validazione corre su due passi tenuti deliberatamente separati.**
`scripts/valida.py` esegue prima una chiusura OWL-RL (`owlrl`) — verifica la
**coerenza logica**, nessuna violazione di disjointness, nessuna istanza
`owl:Nothing` — e poi `pyshacl.validate()` contro `src/shapes.ttl` — verifica la
**forma** dei dati, campi obbligatori, lingua delle etichette, assenza di cicli in
`prerequisitoDi` (una property path SPARQL `prerequisitoDi+` dentro uno shape
`sh:sparql`). Tenerli separati rende leggibile *quale tipo* di problema è emerso,
invece di un unico responso che mescola le due cose. Risultato attuale: 1703 triple
caricate, chiusura OWL-RL a 3562 senza incoerenze, SHACL conforme al primo tentativo.

## 5. Dal grafo alla pagina

La struttura di consultazione non è solo un rendering del grafo: è dove si scopre se
il modello regge all'uso, non solo alla propria coerenza interna.

**Il secondo font previsto per l'apparato non è mai stato specificato** — un vuoto
nella richiesta originale ("EB Garamond per il testo, [...] per l'apparato in
maiuscoletto spaziato"), non una mia dimenticanza. Invece di sceglierne uno
arbitrariamente, ho usato `font-variant-caps: small-caps` sulla stessa famiglia EB
Garamond: usa il taglio small-caps reale del font se il file lo contiene e sintetizza
in modo dignitoso altrimenti, evita di introdurre una seconda famiglia non richiesta e
tiene il sito coerente su un solo font. I file (`EBGaramond-Variable.woff2` e
il corsivo, ~290KB ciascuno) sono scaricati per davvero dal repository ufficiale
Google Fonts, licenza OFL inclusa, e convertiti da TTF a WOFF2 — "self-hosted" nel
vincolo tecnico significa che il sito funziona offline, non che il font sia lo stesso
ma linkato da un CDN a runtime.

**Ho aggiunto una quarta vista (Teorici) non prevista nel piano**, che ne elencava tre
(concetto, modulo, filo trasversale). I 61 teorici esistevano già come dati popolati e
collegati (`teorizzatoDa`, `discussoInUnita`); senza una pagina propria, dati che il
modello già conteneva sarebbero rimasti irraggiungibili con un click — un lettore che
vede "Teorizzato da Bateson" in una pagina Concetto non avrebbe potuto cliccarci sopra.
Non un'estensione di perimetro per il gusto di farla: la verifica d'uso qui sotto
mostra che si è rivelata concretamente utile, non solo giustificabile in astratto.

**Un bug reale è stato trovato durante la verifica, non durante la scrittura**: le
pagine Modulo interrogavano la relazione `discussoInUnita` senza filtrare per tipo —
sia i Concetti sia i Teorici la portano — e le prime versioni generate mostravano nomi
di persone (Cantor, Bateson, Galileo...) dentro la lista "Concetti discussi qui",
linkati verso pagine che non esistevano. Non l'ho trovato rileggendo il codice, ma con
un controllo automatico di tutti i link interni delle 187 pagine generate: 82 link
rotti su 1606, tutti riconducibili a questo unico bug. Corretto separando le due liste
per tipo; rigenerato, 0 link rotti.

**La verifica non si è fermata alla coerenza del grafo — ho eseguito tre compiti di
ricerca reali, in un browser, non solo query SPARQL.** "Trova i prerequisiti per
arrivare a RLHF": funziona, ma mostra un passo alla volta per pagina (Fine-tuning),
mentre la query SPARQL della Fase 4 restituisce l'intera catena transitiva
(Modello di base incluso) in un colpo solo — una differenza dichiarata, non un
difetto: sono due strumenti per due usi diversi, uno sfoglia come un thesaurus, l'altro
interroga come un database. "Trova tutti i concetti del filo discreto/continuo":
nessuna frizione, funziona al primo tentativo. "Trova dove si parla di Bateson": la
vista Teorici mostra insieme i concetti che teorizza e le unità in cui è citato — qui
è dove la scelta del punto precedente si è dimostrata utile su un compito vero, non
solo sensata sulla carta.

**L'accento verde è stato verificato guardando le pagine renderizzate, non leggendo il
CSS.** Il vincolo — riservato a numerazione e rimandi, mai a fondi o titoli — regge su
tutte le pagine controllate: il contatore dei fili trasversali, i codici unità, i link
di cross-reference sono verdi; titoli, sfondi delle card e delle etichette usano solo
un bordo verde, mai un riempimento.

## 6. Limiti noti del modello risultante

Quanto segue non è nascosto altrove nel progetto: è qui, insieme al resto, perché un
documento di decisioni di modellazione che elenca solo i successi non sarebbe onesto.

- **Il namespace era un placeholder** (`http://example.org/corso-llm-vocabolario#`,
  `example.org` è il dominio riservato IANA per la documentazione, non un dominio
  dell'autore): risolto il 15 settembre 2026, prima della pubblicazione, sostituendolo
  con `https://smb-antro.github.io/dal-bit-alle-entita-semantiche/vocabolario#` in
  tutti i `.ttl` e negli script che li generano/interrogano — non un semplice
  trova-e-sostituisci nel testo, ma seguito da una rigenerazione completa (`dati.ttl`,
  le pagine di `output/`, il grafo della Lente semantica) e da una nuova esecuzione di
  reasoner OWL-RL e SHACL, per verificare che il nuovo IRI non alterasse nulla — esito:
  nessuna incoerenza, nessuna differenza nell'output oltre al prefisso stesso (i nomi
  brevi, non l'IRI completo, sono l'unica cosa che compare nelle pagine generate).
- **Alcune relazioni osservate nel corso non sono nel grafo** (§4): GPU, Memristor,
  "immagine raster/SVG" come concetti a sé, la coincidenza Von Neumann/Rosenblatt, il
  legame diretto Pearl-Hume. Nessuno di questi compromette la validità di quanto c'è,
  ma un lettore che cercasse esattamente una di queste relazioni non la troverebbe
  come tripla, solo nel testo del corso.
- **Il filo trasversale "logica, informazione e biologia della cognizione" è più
  debolmente coeso** degli altri due — dichiarato nel suo stesso scopeNote, non
  scoperto ora.
- **`owl:AllDisjointClasses` è verificato con un solo reasoner** (owlrl); un tool di
  validazione diverso potrebbe trattarlo in modo diverso — da riverificare se il
  progetto cambia strumenti.
- **La struttura di consultazione mostra le relazioni un passo alla volta**; per una
  catena transitiva completa serve la query SPARQL, non la sola navigazione — una
  scelta di leggibilità (§5), non un limite tecnico, ma vale la pena che chi consulta
  il sito lo sappia.
- **La verifica d'uso (§5) è stata condotta da me, non da lettori esterni.** Tre
  compiti concreti, non solo coerenza — ma non ancora il test con 2-3 persone terze
  che il piano originale elencava esplicitamente come rimandabile a dopo la prima
  versione. Resta un passo successivo dichiarato, non fatto passare per completo.

## Aggiornamento post-estrazione (4 settembre 2026)

La fonte è stata estratta da `qa-tool/` in un repository proprio,
`~/projects/cartografia-semantica/`, e trasformata da corso a lezioni numerate in saggio
in tre Parti (Fondamenti/Genealogia/Meccanismo, titolo "Dal bit alle entità
semantiche"). Il modello costruito nelle sezioni precedenti non è stato riscritto da
zero: è stato fatto corrispondere alla nuova struttura, con le stesse discipline già
in vigore, non nuove regole inventate per l'occasione.

**Non ho preso il resoconto dell'utente come fonte di verità.** Prima di toccare un
solo file, tre verifiche indipendenti (inventario strutturale del nuovo repository,
audit di ogni riferimento obsoleto nel modello esistente, controllo puntuale delle
citazioni corrette contro il testo attuale) — una fallita per un limite di sessione,
rieseguita a mano con query dirette invece di ritentare lo spawn di un agente. La
verifica ha trovato due discrepanze reali rispetto a quanto descritto inizialmente (il
file compilato non era ancora rinominato, l'appendice viveva solo in un worktree non
unito) — chiarite con l'utente e risolte prima di procedere, non assunte. Ha anche
trovato, per conto suo, un'incoerenza reale nel saggio stesso (la correzione Hebb/Carla
Shatz presente in un capitolo di Genealogia ma non nel passaggio parallelo di
Meccanismo) — segnalata all'utente, non corretta qui: non è un file di questo
repository, e questo progetto legge la fonte, non la modifica.

**Una nuova classe `:Parte`, non un `:Modulo` riciclato.** Il saggio ha ora davvero tre
livelli di struttura (Parte → Capitolo → Unità), non due: `:Modulo` è stata rinominata
`:Capitolo` (stessa semantica, nome più accurato ora che Genealogia e Meccanismo
condividono la stessa struttura — prima "Modulo" andava bene solo per l'area tecnica) e
una nuova `:Parte` aggiunta sopra. La disgiunzione fra i tipi di primo livello (§3) è
passata da 6 a 7 membri.

**I 2 Capitoli di Fondamenti non sono diventati anche `:Unita`.** Il saggio non dà loro
sotto-unità — restano il bersaglio citabile più fine. Dual-tipizzarli avrebbe richiesto
un `:partOfCapitolo` auto-referenziale (un capitolo che fa parte di se stesso), scartato
come soluzione innaturale. Ho invece allargato il range di `:discussoInUnita` all'unione
`owl:unionOf(:Unita :Capitolo)` — verificato con un test isolato via reasoner owlrl,
dati sintetici non nei file reali, *prima* di costruire il resto su quella base: un
concetto collegato sia a un'Unità sia a un Capitolo chiude senza incoerenze.

**La rinumerazione di 111 valori `:fonte` è stata fatta con una funzione scritta e
testata, non con 111 modifiche manuali indipendenti.** Diversamente dalla disciplina
"scritto a mano, verificato a vista" della Fase 2 originale — qui il volume e la
regolarità del compito (uno stesso schema di trasformazione ripetuto identico 111
volte) rendevano una funzione più affidabile di 111 interventi manuali indipendenti,
ciascuno a rischio proprio di errore di trascrizione. La funzione è stata scritta,
il suo output stampato per intero e controllato a campione sui casi più complessi
(intervalli, virgole dentro punto e virgola, annotazioni fra parentesi) *prima* di
essere applicata al file reale — non è un parser generico a cui ho delegato fiducia
alla cieca, è uno strumento verificato una volta e poi applicato in modo deterministico,
la stessa logica del popolamento generato da script (§4), estesa qui alla revisione di
dati già scritti a mano.

**Due gap trovati durante l'esecuzione, non previsti dal piano — corretti quando
scoperti, non nascosti.** `src/shapes.ttl` referenziava ancora `:partOfModulo`/
`:Modulo`: assente dall'elenco file del piano, ha fatto fallire la validazione SHACL
al primo tentativo (47 violazioni) finché non l'ho aggiornato. `scripts/genera_html.py`
assumeva che ogni bersaglio di `discussoInUnita` avesse sempre un genitore Capitolo da
risolvere per costruire il link — falso per i 2 Capitoli di Fondamenti, avrebbe
prodotto link rotti verso una pagina inesistente; isolato in un helper dedicato
(`href_citabile`) e verificato in browser, non solo con il link-checker automatico.
Nessuno dei due era nell'elenco esplicito di file da toccare — la validazione stessa
li ha fatti emergere, che è esattamente il punto di avere una validazione.

**Tre nuovi Teorico, senza nuove relazioni forzate.** Peirce ed Emil Post hanno ora
contenuto reale in Fondamenti (prima Peirce era solo il nome di un'intestazione, un
caso dubbio escluso in Fase 2 per lo stesso motivo — mai contenuto in prosa); Carla
Shatz è nuova, l'autrice reale della frase erroneamente attribuita a Hebb. Ho aggiunto
i tre individui con la loro fonte, ma nessuna relazione `teorizzatoDa` — il testo li
menziona, non attribuisce loro un concetto specifico del modello con la stessa
chiarezza con cui lo fa per, es., Varela e l'autopoiesi. Coerente con la disciplina già
in vigore (§4): un individuo può esistere senza che gli si costruisca attorno una
relazione che il testo non sostiene con la stessa forza.

## In sintesi

Ogni scelta sopra ha una forma ricorrente: preferire una distinzione esplicita a una
comoda semplificazione (teorici/concetti, is-a/uso, reale/illustrativo), e dichiarare
il costo invece di nasconderlo quando la distinzione lascia qualcosa fuori. È lo stesso
principio applicato a livelli diversi — vocabolario, ontologia, dati, pagina — ed è
quello che, più della sintassi Turtle o del CSS, questo progetto vuole dimostrare.
L'aggiornamento del 4 settembre non ha cambiato questo principio, solo l'ha rimesso
alla prova su una fonte che nel frattempo era cambiata sotto i suoi piedi: la
disciplina ha retto senza bisogno di eccezioni.

## Lente semantica (4 settembre 2026)

Una seconda struttura di consultazione, in `lente-semantica/`, accanto a quella per
capitoli di `output/`: non una nuova modellazione, una vista diversa sullo stesso
grafo — un nodo alla volta, con i suoi vicini raggruppati per tipo di relazione e
direzione, invece che sfogliato per area tematica.

**`scripts/genera_grafo.py` elenca esplicitamente le 17 proprietà esposte come archi**,
invece di esportare "ogni tripla il cui oggetto è un URI": la stessa disciplina già
seguita per `:fonte` e per `RELAZIONI_CONCETTO` in `genera_html.py` — una lista
esplicita, verificabile, non un criterio generico che potrebbe includere per sbaglio
triple di bookkeeping (`skos:inScheme`, le liste RDF di `skos:memberList`).

**Il grafo è caricato con `<script src>`, non `fetch()`.** Chrome e Firefox bloccano le
richieste JavaScript a file locali quando una pagina è aperta come `file://` (nessun
server) — un vincolo reale, verificato, non teorico. Un file `.js` caricato con
`<script src>` invece funziona sempre, anche a doppio clic: `genera_grafo.py` scrive
`grafo.js` (`const GRAFO = {...}`), stesso contenuto di un JSON, solo eseguibile invece
che da recuperare via rete. Conseguenza diretta: `output/index.html` si apre
correttamente senza alcun server, coerente col requisito esplicito dell'utente
("l'importante è che sia visualizzabile in browser").

**D3 self-hosted, non vanilla.** Il resto del sito è JavaScript scritto a mano, ma qui
la scelta è stata esplicita e discussa con l'utente: usare D3 (scaricato per davvero,
`output/vendor/d3.v7.min.js`, licenza inclusa — non un link a CDN) per il calcolo degli
archi (`d3.arc()`) e le selezioni DOM, in cambio di un risultato più rifinito e di
meno tempo speso a gestire casi limite geometrici a mano. Il layout radiale stesso
resta calcolato a mano (non `d3-force`): il mockup di riferimento (`mockup/1c-lente.png`)
mostra un ventaglio leggibile per gruppo di relazione, non una nuvola a forze — un
layout deliberato, non quello che D3 produrrebe di default.

**Bug reale trovato in verifica, non nella scrittura**: la sidebar cresceva a
dismisura invece di scorrere al proprio interno, trascinando giù l'intera pagina. Causa
classica di CSS Grid/Flexbox: un elemento con `max-height` dentro un grid item non la
rispetta finché non si dichiara anche `min-height: 0` (il comportamento di default è
"non restringerti mai sotto il contenuto"). Trovato provando l'interazione reale in
browser, non nella sola lettura del codice.

**Verificato funzionalmente, non solo visivamente**: il render iniziale (16 archi per
"Attention", combaciante esattamente col mockup — stessa cifra, stesso tipo "Concetto +
Tecnica"), il click di ricentraggio su un satellite (con aggiornamento di briciola,
hash dell'URL e sidebar), il toggle di 2° grado, e il filtro di ricerca — ciascuno
testato eseguendo l'interazione reale (dispatch di eventi DOM), non solo ispezionando
il markup generato.

**Aperto, non deciso**: se il blocco "Enfatizza/Sacrifica/Risponde a/Nasconde" del
mockup — che qui ho trattato come nota di design per me, non come interfaccia da
riprodurre — debba diventare contenuto scritto da qualche parte (candidato naturale:
questa stessa sezione, che in parte già lo fa). Non ancora una risposta dall'utente su
questo punto.

## Lente semantica — correzioni UX (4 settembre 2026)

Primo giro di uso reale della pagina (non solo la verifica funzionale della sessione
precedente) ha fatto emergere 4 problemi concreti, raccolti dall'utente punto per
punto prima di toccare codice, in un worktree dedicato (`lente-semantica-ux-1af0b5`).

**Centraggio: bug reale, non impressione.** Il `viewBox` dichiarato in
`output/index.html` era `0 0 720 620` (centro vero 360,310), ma `lente.js` disegnava
attorno a `CX=300, CY=300` — 60px a sinistra e 10px sopra il centro reale. Anche
corretto il centraggio, il margine sarebbe rimasto insufficiente: l'etichetta troncata
più lunga (34 caratteri) parte da `R_TESTO=205` e può richiedere fino a ~409px di
raggio nel caso peggiore. Fix: viewBox quadrato `0 0 880 880`, `CX=CY=440` — verificato
non ad occhio ma cliccando programmaticamente tutti i 258 nodi in un browser vero
(`getBBox()` dell'SVG dopo ogni render) e misurando il margine minimo residuo: 60px in
tutte le direzioni per tutti i nodi, incluso "Attention" (16 archi, il caso limite già
usato come riferimento nel mockup). I raggi (`R_ARCO`, `R_NODO`, `R_TESTO`, `R_NODO2`)
non sono stati toccati: erano già tarati e verificati contro il mockup, il problema era
il canvas attorno, non il disegno.

**Sidebar: tendina a due livelli, non un'invenzione nuova.** L'utente ha chiesto di
raggruppare i 258 nodi secondo "la divisione a monte fatta per la mappatura semantica".
Non una nuova classificazione: `kind()` in `scripts/genera_html.py` (root, il
generatore del sito principale) già assegna ogni nodo a Concetto/Teorico/Parte/
Capitolo/Unità/Dataset con un ordine di priorità fisso — `lente.js` ora applica lo
stesso ordine (funzione `gruppoDi`, calcolata lato client dal campo `tipi` già
esportato, senza toccare `genera_grafo.py`). Gruppi ordinati per conteggio decrescente
(Concetto 111, Teorico 64, Unità 47, Dataset 16, Capitolo 12, Parte 3), con "Altro" (5:
FiloTrasversale + StatoEpistemico) sempre in fondo per convenzione anche se
numericamente supera "Parte" — una scelta esplicita dell'utente, non un difetto
dell'ordinamento. Dentro ogni gruppo, alfabetico non per grado: la ricerca di un
termine preciso conta più della sua importanza nel grafo. Markup: `<details>`/
`<summary>` nativi — prima volta nel sito, verificato che non esistesse già un pattern
di accordion altrove da seguire invece. Selezionare un nodo chiude tutti i gruppi tranne
quello del nuovo centro (anche quelli aperti manualmente): il punto della modifica era
eliminare un indice sempre-tutto-visibile, un comportamento cumulativo lo avrebbe
ricreato nel corso di una sessione lunga.

**Contrasti: misurati, non ritoccati a occhio.** Le 4 tinte piene delle categorie di
relazione erano già a norma WCAG (4.5–7.2:1). Le varianti "tenue" usate come
riempimento dei satelliti no: ~1.05–1.17:1 contro lo sfondo, praticamente invisibili —
quasi certamente la causa di "serve più contrasto" segnalata con l'immagine fitta di
connessioni. Corrette a parità di tinta/saturazione ma luminosità alzata (1.8–2.1:1
contro carta, sempre distinguibili dal proprio pieno). Per i 7 nuovi colori di gruppo
nella sidebar, usata la skill `dataviz` (validatore CVD/contrasto eseguibile, non
eyeballing) contro le superfici reali della pagina — palette deliberatamente separata
da quella delle 4 categorie di relazione (due linguaggi cromatici, due significati:
tipo di nodo contro tipo di relazione).

**Relazioni: legenda cliccabile come filtro + glossario, non un secondo indice
completo.** La legenda (4 categorie) è diventata interattiva: cliccare una categoria
attenua i suoi archi/satelliti nel grafo corrente, il filtro persiste cambiando nodo
centrale. Aggiunto un `<details>` "Glossario delle relazioni" separato, di sola
consultazione, con le 18 proprietà raggruppate per categoria. Una seconda tendina
"Relazioni" come punto d'accesso parallelo (equivalente a un secondo indice, non solo
un filtro sul nodo corrente) è stata deliberatamente rimandata: l'utente l'ha chiesta
esplicitamente più avanti, non ora, per non accavallare troppi cambi — e perché
un indice di relazioni tende a voler mostrare tutte le occorrenze di un tipo, in
tensione con la scelta già registrata sopra di non mostrare mai l'insieme dei nodi.

**Etichette sugli archi: un primo tentativo scartato dopo prova reale, non al primo
colpo.** Un primo tentativo aveva aggiunto un'etichetta di testo permanente per ogni
arco (nome della relazione + conteggio), al raggio `R_ARCO+20`. Verificato
programmaticamente su tutti i 258 nodi sembrava a posto (zero sovrapposizioni con i
satelliti), ma l'utente l'ha guardato dal vivo in browser e ha trovato quello che il
controllo automatico non catturava: l'etichetta si sovrapponeva alla propria linea
guida ogni volta che il gruppo aveva un numero **dispari** di voci — non un caso raro,
succede per costruzione matematica (l'angolo medio del gruppo coincide esattamente con
l'angolo della voce centrale quando N è dispari), quindi in circa metà dei gruppi.
Lezione operativa: un controllo di sovrapposizione contro i satelliti non basta a
escludere sovrapposizioni contro le linee guida — vanno controllate esplicitamente,
non assunte innocue perché sottili e traslucide.

Scartato in favore di una soluzione più semplice e priva di geometria condivisa: al
passaggio del mouse su un satellite (non al click), un'unica pillola fissa in alto a
destra nel riquadro del grafo — colore della categoria, testo bianco in maiuscolette,
slug tecnico della relazione + nodo di destinazione (es. "teorizzatoDa · Geoffrey
Hinton"). Non essendo agganciata alla posizione radiale, non condivide più spazio con
nessun'altra linea o etichetta — zero collisioni per costruzione, non per fortuna.
Motivazione aggiuntiva dell'utente: con legenda cliccabile, tooltip sui satelliti e
glossario già presenti, un'etichetta sempre visibile sull'arco era un quarto modo
ridondante di dire la stessa cosa.

**Bug pre-esistente trovato per caso, non nel giro di modifiche originale**: gli archi
colorati risultavano ruotati di 90° rispetto ai satelliti/linee a cui appartengono —
mascherato nella verifica iniziale perché con "Attention" (16 relazioni) il cerchio è
quasi tutto pieno, un anello ruotato resta comunque "adiacente a se stesso" e non salta
all'occhio. Causa: `d3.arc()` misura gli angoli da ore 12 in senso orario, il resto del
codice (satelliti, linee guida) da ore 3 con `Math.cos`/`Math.sin` — stesso numero,
due convenzioni diverse. Confermato con una prova diretta e inequivocabile (un arco di
test con `startAngle=0` si disegna a ore 12, non a ore 3) prima di correggere, non per
deduzione soltanto. Fix: `+Math.PI/2` solo nella chiamata a `arcoGen(...)`. Verificato
sui 258 nodi: l'inizio di ogni primo arco coincide ora esattamente con -90° (ore 12),
zero scarto.

**Larghezza angolare fissa per voce: provata, poi annullata su richiesta esplicita.**
Un'ipotesi intermedia (calibrare l'ampiezza di ogni relazione su "Attention" invece di
dividere sempre l'intero cerchio per il conteggio del nodo corrente) avrebbe evitato
che i nodi con pochissime relazioni producessero un anello quasi completo a ridosso del
cerchio centrale. Provata in isolamento (`lente-semantica/lab/`, vedi sotto) e poi
scartata: l'utente ritiene che il cerchio sempre pieno comunichi meglio, anche a costo
di quell'anello stretto per i nodi più poveri di relazioni — un giudizio di UX, non un
errore da correggere. La divisione resta quindi dinamica per nodo, come in origine.

**Metodo**: da qui in poi, ogni ipotesi di correzione sul grafo è stata prima provata
in `lente-semantica/lab/backpropagation.html` — una pagina isolata sullo stesso nodo
reale ("Backpropagation", 9 relazioni), che riusa i dati veri (`grafo.js`) ma non tocca
`output/` finché il risultato non è confermato. Più economico che iterare sulla pagina
intera, e ha permesso di scartare un'ipotesi (larghezza fissa) senza sporcare la pagina
reale nel frattempo.

**Cerchio centrale: testo rimosso.** Il nome del nodo comparso dentro il cerchio era
ridondante col breadcrumb sopra il grafo (che lo mostra già, per intero) — rimosso, il
cerchio resta come solo elemento visivo di riferimento.
