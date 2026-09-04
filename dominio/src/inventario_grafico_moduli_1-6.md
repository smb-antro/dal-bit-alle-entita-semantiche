# Moduli 1-6 — Inventario grafico definitivo

**Stato**: inventario concettuale dei componenti interattivi/grafici, concordato in
conversazione. Definisce *cosa* serve e *perché*, non ancora il codice. Riferimento:
`struttura_moduli_1-6.md` per i contenuti testuali che questi componenti illustrano.

**Principio guida, validato in conversazione**: un componente interattivo *centrale*
per modulo, riusato/arricchito lungo le sue unità — non un widget per unità. Accanto,
piccoli diagrammi di supporto (statici o quasi) per punti specifici che non
giustificano un widget a sé. Non tutto il contenuto aggiunto nelle fasi di revisione
richiede grafica dedicata (es. pleroma/creatura, Varela, calibrazione come concetto
restano testuali).

**Stack di default**: vanilla HTML/CSS/JS, coerente col resto del sito (nessuna
libreria, come già stabilito per il Modulo 00). Un'unica eccezione dichiarata: la
superficie di perdita del Modulo 4.5 userà GLSL/shader con tecnica SDF (Signed
Distance Function, stile Shadertoy) — coerente in modo quasi programmatico col
contenuto insegnato (una superficie continua vera, non un grafico discreto), ma prima
incursione fuori dal vanilla JS. Da tenere presente per l'implementazione: richiede
WebGL, non solo Canvas 2D/SVG.

---

## Modulo 1 — Il testo come dato

- **Componente centrale**: playground del tokenizzatore. L'utente digita testo
  libero; il widget si arricchisce lungo le unità — 1.1 mostra i codici carattere,
  1.2/1.3 la segmentazione in token (confronto naive-a-spazi vs sotto-parole reale),
  1.4 gli ID numerici accanto a ogni token.
- **Piccolo, per 1.4**: comparazione raster/SVG — uno slider di zoom che mostra da un
  lato un'immagine raster che pixela, dall'altro una forma SVG che resta nitida.
  Rinforza l'analogia in modo viscerale.
- **Piccolo, per 1.5**: la diagonale di Cantor — griglia di cifre con la diagonale
  evidenziata e un pulsante che genera, cifra per cifra, il numero che sfugge alla
  lista. Diagramma classico, a basso rischio di ambiguità.

## Modulo 2 — Probabilità e linguaggio

- **Componente centrale**: predittore n-grammi su un piccolo corpus fisso — l'utente
  digita l'inizio di una frase, vede le parole candidate con barre di probabilità
  calcolate dai conteggi reali. Slider per la finestra di contesto (1/2/3 parole),
  mostra dove la previsione si rompe (zero occorrenze).
- **Piccolo, per 2.4**: diagramma non interattivo per illustrare le dipendenze
  lontane che nessuna finestra piccola può coprire.
- **Piccolo, per 2.2**: diagramma di calibrazione (reliability diagram — confidenza
  dichiarata sull'asse x, accuratezza reale sull'asse y, diagonale di riferimento).
  Pochi punti, anche cliccabili, non un widget a sé.

## Modulo 3 — Parole come punti nello spazio

- **Dataset già pronto**: `lezioni/embedding_dati_moduli_3_5.json` — 23 parole,
  vettori reali (fastText italiano), tre modalità di coordinate (esplorazione,
  aritmetica, polisemia) con assi costruiti su misura per ciascuna. Nessuna modifica
  da questa revisione.
- **Componente centrale**: mappa navigabile dello spazio degli embedding, riusata e
  riconfigurata lungo le unità (esplorazione libera in 3.1/3.2; motore
  dell'aritmetica vettoriale in 3.4, con possibilità di provare altre combinazioni e
  vedere anche i fallimenti; punto polisemico fermo tra due gruppi in 3.5).

## Modulo 4 — Reti neurali

- **Tre componenti eterogenei**, non un solo widget riusato:
  - (a) un neurone con pesi regolabili a slider e output live (variante continua del
    calcolatore booleano di `lezione_00a`);
  - (b) i 4 punti di XOR su un piano, dove l'utente prova a tracciare una riga retta
    che li separi e fallisce, prima di vedere come uno strato in più curva lo spazio
    e risolve il problema (4.2/4.3);
  - (c) un paesaggio di perdita (collina/valle) con una pallina che scende passo
    passo (4.4/4.5) — **reso con shader GLSL/SDF**, non Canvas/SVG classico
    (decisione esplicita, vedi sopra).
- **Piccolo, opzionale, "se c'è tempo"**: schema a due pannelli per 4.5 — loop
  continuo del termostato/feedback omeostatico vs ciclo discreto
  addestra-poi-congela del backpropagation. Utile ma non prioritario.
- **Nessuna grafica dedicata**: pleroma/creatura (4.3), Varela/autopoiesi (4.1),
  schismogenesi come concetto teorico (4.5) — restano testuali/concettuali.

## Modulo 5 — Il Transformer

- **Componente centrale**: frase cliccabile — selezionare una parola mostra le
  connessioni pesate verso le altre (spessore/opacità proporzionale al peso di
  attention). Riusato per 5.1-5.4, incluso il caso di una parola polisemica in due
  frasi diverse con pesi diversi.
- **Idea ambiziosa mantenuta**: collegamento con la mappa di Modulo 3 — la parola che
  "si muove" nello stesso spazio da statica a contestuale. Da specificare quando si
  arriverà all'implementazione (candidato per un prototipo con Fable).
- **Piccolo, per 5.5**: interruttore multi-testa (2-3 pattern di attention alternativi
  sulla stessa frase) e una piccola animazione separata per la codifica di posizione.

## Modulo 6 — Cosa significa "Large"

- **6.1**: slider esplorabile su scala logaritmica per la dimensione dei modelli.
- **6.2**: grafico annotato per le capacità emergenti, deliberatamente poco
  interattivo per non dare falsa certezza a un fenomeno ancora dibattuto.
- **Piccolo, per 6.3**: timeline semplice per l'arco storico (alfabeto → von Neumann
  1958 → digitalizzazione di massa anni 2000 → corpora di addestramento LLM oggi) —
  coerente con lo stile timeline già usato nel Blocco A narrativo, basso rischio di
  introdurre uno stile nuovo.
- **6.4/6.5**: semplice toggle prima/dopo per fine-tuning/RLHF.
- **6.6**: una barra continua che si "spacca" in blocchi discreti quando si attiva la
  quantizzazione — eco diretta agli interruttori del Modulo 0.

---

## Decisioni aperte per la fase di implementazione

- Specifica concreta del widget M3↔M5 (interazioni, transizioni tra modalità di
  Modulo 3, come il collegamento con Modulo 5 condivide dati/stato) — da fissare
  prima di un primo prototipo con Fable.
- Come impostare l'infrastruttura WebGL/GLSL per il componente shader di 4.5,
  mantenendo coerenza col resto del sito (vanilla JS altrove).
- Dataset/contenuti concreti per i componenti di M1, M2, M4 (M6 è perlopiù
  esplorativo/illustrativo, meno dipendente da dati reali).
