# Prompt per sessioni separate — revisione di tono, compilazione, traduzioni, tema

Scritti il 2026-07-07, dopo il completamento del Modulo 6 (vedi decision-log), su richiesta
esplicita dell'utente: rendere il tono del corso più professionale/accademico e meno
pedagogico, poi compilare un file unico autocontenuto (indice + introduzione + tutte le
lezioni, 00a/00b prima dei Blocchi A-D, poi Moduli 1-6) con tema chiaro/scuro, infine
tradurlo in inglese, francese e tedesco. Stesso schema del file gemello
`prompt-sessioni-widget-m2-m4-m6-m3m5.md`: ogni prompt è pensato per una **sessione/chat
separata**, in modalità piano, e va lanciato **nell'ordine indicato** — ogni sessione
dipende dal risultato verificato della precedente.

Tutti assumono il worktree già esistente
`qa-tool/.claude/worktrees/corso-llm-moduli-1-6/`
(branch `corso-llm-moduli-1-6`) — da non ricreare.

## Decisioni già prese, non da riaprire in queste sessioni

- **Ambito della revisione di tono**: l'intero corso, tutti e 12 i file esistenti
  (`lezione_00a_funzioni_booleane.html`, `lezione_00b_hardware_software.html`,
  `lezione_00_blocco_a.html`/`_b`/`_c`/`_d`, `lezione_01_testo_come_dato.html` ...
  `lezione_06_large.html`) — non solo i Moduli 1-6.
- **Widget nelle traduzioni**: per EN/FR/DE si ricostruiscono **dati reali nuovi**
  (tokenizer BPE, corpus n-grammi, vettori embedding, esempio di polisemia), non solo la
  prosa — stesso rigore già documentato nel decision-log per l'italiano (2026-07-06), non
  semplificazioni né dati italiani lasciati sotto una traduzione superficiale.
- **Fable**: nessuna restrizione di quota imposta da questi prompt — usabile liberamente
  dove già previsto (analogamente a M3/M5).
- **Tema chiaro**: la palette esatta è una decisione della sessione esecutiva di Fase 2
  (non pre-decisa qui), ma quella sessione deve comunque proporla all'utente per conferma
  visiva prima di considerarla definitiva — stesso principio di checkpoint già seguito per
  ogni decisione di design in questo progetto.

## Roadmap e dipendenze

> **Nota del 2026-07-07 (revisione del piano in corsa)**: le Fasi 3 (traduzioni EN/FR/DE,
> voci 3-8 sotto) restano previste ma **non sono urgenti** — rimandate al momento in cui il
> resto del progetto (Fase 1 + Fase 2, contenuto italiano completo) sarà terminato e
> verificato. Non lanciare questi prompt finché non richiesto esplicitamente. Al loro posto,
> la sessione odierna dedica un passo alla verifica del funzionamento dei widget di tutti i
> 12 file (ed eventuale correzione), su specifiche che l'utente darà separatamente.

1. **Fase 1** — Revisione di tono, tutto il corso (IT). *Nessuna dipendenza.* — **Completata
   2026-07-07**, verificata meccanicamente su tutti i 12 file, committata.
2. **Fase 2** — Compilazione `output/dal-bit-alle-entita-semantiche_it.html`: indice, introduzione,
   navigazione a tre livelli, tema chiaro/scuro. *Richiede Fase 1 completata.*
3. **Fase 3-EN-a** — Traduzione prosa + corpora linguistici nativi (EN). *Richiede Fase 2.*
   — **Rimandata**, vedi nota sopra.
4. **Fase 3-EN-b** — Ricostruzione dati reali + assemblaggio + verifica →
   `output/dal-bit-alle-entita-semantiche_en.html`. *Richiede Fase 3-EN-a.* — **Rimandata.**
5. **Fase 3-FR-a** — Traduzione prosa + corpora linguistici nativi (FR). *Richiede Fase 2
   (indipendente da EN/DE, può girare in parallelo).* — **Rimandata.**
6. **Fase 3-FR-b** — Ricostruzione dati reali + assemblaggio + verifica →
   `output/dal-bit-alle-entita-semantiche_fr.html`. *Richiede Fase 3-FR-a.* — **Rimandata.**
7. **Fase 3-DE-a** — Traduzione prosa + corpora linguistici nativi (DE). *Richiede Fase 2
   (indipendente da EN/FR, può girare in parallelo).* — **Rimandata.**
8. **Fase 3-DE-b** — Ricostruzione dati reali + assemblaggio + verifica →
   `output/dal-bit-alle-entita-semantiche_de.html`. *Richiede Fase 3-DE-a.* — **Rimandata.**

Le sessioni "a" e "b" di ciascuna lingua sono separate perché la "a" produce un artefatto
(il corpus narrativo tradotto) di cui la "b" ha bisogno come dato di ingresso per
riaddestrare il tokenizzatore BPE — non sono la stessa unità di lavoro solo divisa per
comodità, la "b" dipende letteralmente sul testo prodotto dalla "a".

---

## Prompt 1 — Revisione di tono, tutto il corso (IT)

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
in particolare la voce del 2026-07-07 su questa richiesta, che spiega perché l'ambito è
l'intero corso e non solo i moduli tecnici.

Compito: rileggere e riscrivere il REGISTRO della prosa (non la struttura, non i dati, non
i widget) in tutti e 12 i file esistenti di src/corso-llm/lezioni/:
lezione_00a_funzioni_booleane.html, lezione_00b_hardware_software.html,
lezione_00_blocco_a.html, lezione_00_blocco_b.html, lezione_00_blocco_c.html,
lezione_00_blocco_d.html, lezione_01_testo_come_dato.html, lezione_02_probabilita.html,
lezione_03_embedding.html, lezione_04_reti_neurali.html, lezione_05_transformer.html,
lezione_06_large.html — da un registro narrativo/pedagogico a uno più professionale e
accademico.

Cosa cambia e cosa NON cambia — distinzione centrale di questo compito:
- CAMBIA: la prosa dentro i tag <p>, <h1>, <h2>, <blockquote>, <div class="aside"> p,
  <div class="question">. Meno scaffolding didattico esplicito (frasi tipo "Vediamo
  perché", "Bene, ora che abbiamo capito X...", rivolgersi al lettore solo per
  scaffolding retorico non funzionale), più argomentazione diretta, registro da testo
  accademico divulgativo di alto livello (pensa a un saggio, non a un corso interattivo
  per principianti) — ma SENZA perdere: (a) i fatti e le citazioni reali (nomi, anni,
  paper), che restano identici; (b) il registro di domanda aperta esplicito ovunque
  compaia (capacità emergenti in 6.2, la domanda finale discreto/continuo in 6.6, "un LLM è
  un sistema formale nel senso di Gödel?" in 1.5, e altre già presenti) — NON risolvere
  nessuna domanda che il corso lascia deliberatamente aperta, cambiare tono non significa
  cambiare cosa il corso afferma di sapere con certezza; (c) le istruzioni funzionali che
  dicono all'utente di interagire con un widget ("Scriva una frase qui sotto", "Muova lo
  slider") — quelle restano, sono funzionali non stilistiche, vanno solo eventualmente
  irrigidite di registro ("Scriva una frase" invece di "Provi a scrivere, se le va").
- NON CAMBIA: nessun id, nessuna classe CSS, nessun dato JS incorporato, nessuna riga di
  <script>, nessuna struttura HTML (hero/eyebrow/quadro/chiusura restano, sono
  impaginazione non tono), nessun file JSON in lezioni/. Questo è un compito di editing di
  prosa, non di ricostruzione.

Metodo, checkpoint obbligatorio: scegli UN'unità rappresentativa (consiglio l'Unità 1.1 di
lezione_01_testo_come_dato.html, già vista dall'utente più volte come riferimento) e riscrivi
SOLO quella con il nuovo registro. Mostra il prima/dopo (testo, non screenshot) e attendi
conferma esplicita dell'utente sul registro prima di applicarlo a tutti gli altri 11 file —
stesso principio di checkpoint-sul-primo-campione già usato in ogni sessione precedente di
questo progetto. Se il registro non convince, itera sullo stesso campione prima di procedere.

Dopo la conferma: procedi con gli altri 11 file, uno alla volta o a gruppi coerenti (es. il
Modulo 00 narrativo come gruppo, poi i Moduli 1-6). Dopo OGNI file modificato, verifica
meccanicamente che nessuna struttura sia stata alterata per errore: HTML ben formato
(parser Python, tag bilanciati), stesso numero di id presenti prima e dopo la modifica,
sintassi JS invariata con motore reale (osascript -l JavaScript, new Function) — anche se
il JS non dovrebbe essere toccato, la verifica needs a per essere certi che nessuna modifica
alla prosa abbia rotto per errore una stringa JS che la incorpora (es. testi di aside o
domande che compaiono anche come costanti JS in qualche widget — verifica caso per caso).

Documenta in decision-log.md un esempio concreto di prima/dopo (almeno un paragrafo)
per lasciare traccia del registro scelto, poi next-steps.md, poi commit. Non toccare
src/corso-agenti/ né src/capstone-qualitativo/.
```

---

## Prompt 2 — Compilazione file singolo IT + tema chiaro/scuro

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica esplicitamente che la revisione di tono (Fase 1) sia stata completata e
committata prima di iniziare; se non lo è, fermati e segnalalo invece di procedere su
prosa non ancora rivista.

Compito: creare output/dal-bit-alle-entita-semantiche_it.html — un unico file HTML autocontenuto che
fonde, nell'ordine, tutte e 12 le lezioni già riviste (00a, 00b, Blocco A, B, C, D, poi
Moduli 1-6), con un indice iniziale, un'introduzione nuova, navigazione a tre livelli, e
un tema chiaro selezionabile accanto a quello scuro esistente. La cartella output/ esiste
già nello scheletro del progetto per "deliverable finiti, tracciati normalmente" — a
differenza di src/corso-llm/lezioni/, che restano i sorgenti di lavoro (non li spostare,
non li eliminare: il file compilato è un artefatto derivato, le lezioni singole restano).

RISCHIO TECNICO PRINCIPALE, da risolvere con attenzione prima di scrivere codice — ogni
lezione ha oggi il proprio <script> con nomi identici a livello top-level in TUTTI i file
(const UNITS, function setActiveUnit, renderRail, ecc.) e id di sezione che ricominciano
sempre da capo (u1-apertura, u2-apertura...) — concatenare 12 file così com'è produce
SyntaxError da ridichiarazione di const e collisioni di id. Prima di implementare, progetta
esplicitamente come risolverlo, per esempio: (a) UNA sola copia della logica di
navigazione/shell condivisa (già identica byte-per-byte tra i file), scritta una volta sola
nel file compilato; (b) ogni lezione diventa un "capitolo" con id di sezione prefissati dal
proprio slug (es. m1-u1-apertura invece di u1-apertura) per essere univoci nell'intero
documento; (c) la logica e i dati specifici di ciascun widget (BPE, n-grammi, embedding,
XOR, shader, scala, quantizzazione...) vanno namespaced per lezione (es. dentro una IIFE
per capitolo, o funzioni con suffisso _m1/_m2/...), non semplicemente concatenati. Prima di
scrivere tutti i 12 capitoli, fai una prova tecnica con solo le prime 2 lezioni (00a + 00b)
per validare l'approccio di namespacing — verifica con un motore JS reale che il risultato
compili senza errori di ridichiarazione — poi estendi agli altri 10 solo dopo che la prova
funziona.

Navigazione a tre livelli — PROPONI esplicitamente 2 opzioni concrete di architettura
all'utente prima di implementare (non decidere da solo, è una decisione di design, come
tutte quelle di shell/navigazione in questo progetto finora): un possibile schema è un
selettore di capitolo fisso (12 voci) sopra l'attuale coppia topbar-unità/rail-sezioni di
ciascuna lezione, che sostituisce il contenuto di topbar+rail quando si cambia capitolo;
un'alternativa è un indice laterale a scomparsa con tutti e 12 i capitoli e le loro unità
già visibili in gerarchia. Fatti confermare l'opzione prima di costruire tutti i 12
capitoli.

Introduzione nuova (contenuto originale, non trascrizione): scrivi una proposta di
introduzione al corso (indicativamente 300-500 parole — posizione, motivazione, struttura
in moduli, il filo discreto/continuo come chiave di lettura trasversale) e sottoponila
all'utente per conferma prima di considerarla definitiva nel file compilato — è contenuto
autoriale nuovo, non una trascrizione meccanica, stesso principio già seguito per ogni
altro contenuto originale di questo progetto.

Tema chiaro: progetta tu la palette (background, surface, testo, accento — mantenendo lo
stesso ruolo strutturale delle variabili CSS già esistenti, solo con valori diversi),
verificane il contrasto (WCAG AA almeno per testo su sfondo) e proponila all'utente con
uno screenshot/anteprima prima di darla per definitiva. Il toggle chiaro/scuro deve
persistere la scelta (es. localStorage) e applicarsi coerentemente a tutti i 12 capitoli
nello stesso file.

Verifica finale: sintassi JS con motore reale sull'intero file compilato (non capitolo per
capitolo isolato — il rischio è proprio nell'interazione tra capitoli); HTML ben formato;
TUTTI gli id del documento univoci (non solo dentro ciascun capitolo); nessuna classe CSS
orfana; dati di ciascun capitolo ancora coincidenti byte-per-byte con i JSON sorgente
originali (lo spostamento/namespacing non deve aver alterato alcun valore). Copia il file
compilato su Desktop per la verifica visiva dell'utente (stesso limite noto del server di
anteprima, prova comunque .claude/serve_lezioni.py se applicabile alla cartella output/).

Documenta in decision-log.md (in particolare la soluzione tecnica scelta per il
namespacing e l'architettura di navigazione confermata) e next-steps.md, poi commit. Non
toccare src/corso-agenti/ né src/capstone-qualitativo/.
```

---

## Prompt 3 — EN, parte a: traduzione prosa + corpora linguistici nativi

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che output/dal-bit-alle-entita-semantiche_it.html esista e sia già stato verificato/committato
(Fase 2); se non lo è, fermati e segnalalo.

Compito, parte 1 di 2 per la lingua inglese (la parte 2, ricostruzione dati e
assemblaggio, è un prompt separato successivo — qui produci solo testo, non toccare
ancora i widget). Traduci in inglese TUTTA la prosa di output/dal-bit-alle-entita-semantiche_it.html
(introduzione, indice, tutti e 12 i capitoli) — non una traduzione meccanica parola per
parola, ma una resa fedele nello stesso registro professionale/accademico già stabilito in
italiano nella Fase 1; mantieni identici fatti, citazioni, nomi propri, anni, e il registro
di domanda aperta ovunque compaia. Salva il risultato come testo intermedio (non ancora nel
widget finale) in un file di lavoro, es. src/corso-llm/traduzioni/testo_en.md — da rimuovere
a fine lavoro come già fatto per altri file di appoggio in questo progetto, una volta che il
contenuto autorevole vive nell'HTML finale.

Compito aggiuntivo e critico di questa sessione — corpora linguistici nativi, NON tradotti
meccanicamente dall'italiano:
1. Il Modulo 00 narrativo (Blocchi A-D + 00a/00b), tradotto sopra, servirà nella sessione
   successiva come corpus di addestramento per un tokenizzatore BPE inglese — verifica che
   la tua traduzione di questi blocchi sia abbastanza ricca e varia (non serve fare nulla di
   speciale oltre a una buona traduzione, ma tienilo a mente: è testo che verrà davvero
   processato da un algoritmo nella sessione successiva, non solo letto).
2. Scrivi da zero (non tradurre) un nuovo corpus di circa 46 frasi inglesi semplici per il
   predittore n-grammi del Modulo 2 — stesso principio già seguito in italiano
   (docs/decision-log.md, voce Modulo 2): frasi brevi con pattern ripetuti naturali in
   inglese (es. soggetti/verbi che si ripetono in contesti diversi), non una traduzione
   letterale delle 46 frasi italiane esistenti (una traduzione letterale non garantisce che
   emergano gli stessi fenomeni di predizione netta/ambigua/sparsità — quei fenomeni vanno
   ri-osservati sui dati inglesi reali, non presunti). Salva in un file di lavoro separato,
   es. src/corso-llm/traduzioni/corpus_ngram_en.md.
3. Non serve ancora scegliere l'esempio di polisemia per l'inglese in questa sessione (lo
   farai nella sessione successiva, quando avrai accesso ai vettori fastText reali) — ma se
   durante la traduzione ti vengono in mente candidati reali (una parola inglese con due
   significati molto distanti, es. in ambiti diversi come quelli usati per "calcio"), annotali
   in un commento nel file di lavoro per la sessione successiva.

Verifica: rileggi la traduzione confrontandola frase per frase con l'originale italiano per
verificare che nessun fatto/citazione/anno sia stato alterato o perso nella traduzione. Documenta in
decision-log.md e next-steps.md (inclusa la lista dei file di lavoro prodotti, da consumare
nella sessione successiva), poi commit. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```

---

## Prompt 4 — EN, parte b: ricostruzione dati reali + assemblaggio + verifica

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che la traduzione inglese e i corpora linguistici nativi (Fase 3-EN-a) esistano e
siano committati; se non lo sono, fermati e segnalalo.

Compito: ricostruire, con lo STESSO rigore già documentato nel decision-log per l'italiano
(voci del 2026-07-06), tre dataset reali in inglese, poi integrarli nei widget e assemblare
output/dal-bit-alle-entita-semantiche_en.html.

1. **Tokenizzatore BPE (Modulo 1)**: addestra un vero algoritmo Byte-Pair Encoding sul
   corpus del Modulo 00 tradotto in inglese (src/corso-llm/traduzioni/testo_en.md dalla
   sessione precedente) — stessa logica già implementata in italiano, stesso numero
   indicativo di iterazioni (adatta se il corpus inglese ha una dimensione molto diversa).
   Verifica 0 errori di round-trip su tutte le parole uniche del corpus, e verifica il
   comportamento su parole inventate in inglese (l'equivalente di "blorpificazione" — inventa
   2-3 neologismi inglesi plausibili con suffissi reali, es. "-ification", "-ness").
   Salva in src/corso-llm/lezioni/bpe_merges_modulo1_en.json con la stessa struttura del
   file italiano.
2. **Predittore n-grammi (Modulo 2)**: usa il corpus inglese scritto nella sessione
   precedente (src/corso-llm/traduzioni/corpus_ngram_en.md), costruisci le tabelle di
   conteggio a finestra 1/2/3, e SOLO DOPO aver visto le distribuzioni reali scegli tre
   prefissi dimostrativi (previsione netta, distribuzione ambigua, sparsità) — non
   riusare gli stessi prefissi italiani tradotti, potrebbero non produrre lo stesso tipo di
   distribuzione sui dati inglesi. Ricostruisci anche la misura di calibrazione (split
   train/held-out, bucket di confidenza) sul corpus inglese — accetta il risultato reale
   che emerge, anche se il pattern di overconfidence non fosse identico a quello italiano.
   Salva in ngram_dati_modulo2_en.json e calibrazione_modulo2_en.json.
3. **Embedding reali ed esempio di polisemia (Moduli 3/5)**: procurati vettori fastText
   inglesi reali (cc.en.300.vec, stesso metodo di estrazione in streaming già usato per
   l'italiano, senza scaricare l'intero file). Scegli 23 parole inglesi nei 4 gruppi
   tematici analoghi (reale/genere, sportivo, chimico, animali). Cerca e verifica un vero
   esempio di polisemia inglese con due significati distanti (usa gli eventuali candidati
   annotati nella sessione precedente come punto di partenza, ma verifica empiricamente
   con le similarità coseno reali — non forzare un candidato che non regge ai numeri,
   come già successo con "banca" scartata in italiano a favore di "calcio"). Verifica che
   l'aritmetica vettoriale di genere (king-man+woman=queen o equivalente) regga sui vettori
   reali con una distanza ragionevole, riportando il risultato reale anche se non fosse
   pulito quanto il caso italiano. Salva in embedding_dati_moduli_3_5_en.json con la stessa
   struttura/metadata del file italiano (documenta fonte, metodo, risultati di verifica).
4. **Base vs fine-tuned (Modulo 6)**: adatta concettualmente (non traduci meccanicamente)
   la coppia prompt/risposta del Modulo 6 in modo che il fenomeno reale (continuazione di
   pattern superficiale vs esecuzione dell'istruzione, Ouyang et al. 2022) resti illustrato
   fedelmente in inglese. Salva in base_vs_tuned_modulo6_en.json.

Integra tutti questi dati nei widget corrispondenti della versione inglese, seguendo
l'architettura già decisa in Fase 2 (namespacing per capitolo). Assembla
output/dal-bit-alle-entita-semantiche_en.html completo. Verifica meccanica finale identica a quella
usata per il file italiano: sintassi JS reale sull'intero file, HTML ben formato, id
univoci nell'intero documento, nessuna classe orfana, tutti i dati incorporati confrontati
byte-per-byte con i nuovi JSON sorgente inglesi. Copia su Desktop per la verifica
dell'utente.

Documenta ogni risultato di verifica (specialmente i numeri reali che emergono dai dati
inglesi, anche se diversi da quelli italiani) in decision-log.md e next-steps.md, poi
commit. Non toccare src/corso-agenti/ né src/capstone-qualitativo/.
```

---

## Prompt 5 — FR, parte a: traduzione prosa + corpora linguistici nativi

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che output/dal-bit-alle-entita-semantiche_it.html esista e sia già stato verificato/committato
(Fase 2); se non lo è, fermati e segnalalo. Questa sessione è indipendente dal lavoro sulla
versione inglese (può girare prima, dopo, o in parallelo in un'altra sessione).

Compito, parte 1 di 2 per la lingua francese (la parte 2 è un prompt separato successivo).
Traduci in francese TUTTA la prosa di output/dal-bit-alle-entita-semantiche_it.html (introduzione,
indice, tutti e 12 i capitoli), stesso registro professionale/accademico già stabilito in
italiano, stessi fatti/citazioni/nomi/anni identici, stesso registro di domanda aperta
preservato ovunque. Salva il risultato intermedio in
src/corso-llm/traduzioni/testo_fr.md.

Corpora linguistici nativi, NON tradotti meccanicamente dall'italiano:
1. Verifica che la traduzione francese del Modulo 00 narrativo sia una buona base per un
   futuro corpus di addestramento BPE (nessuna azione extra oltre a una buona traduzione).
2. Scrivi da zero (non tradurre) un nuovo corpus di circa 46 frasi francesi semplici per il
   predittore n-grammi del Modulo 2, con pattern ripetuti naturali in francese — stesso
   principio già seguito in italiano e inglese: non una traduzione letterale delle frasi
   esistenti. Salva in src/corso-llm/traduzioni/corpus_ngram_fr.md.
3. Annota eventuali candidati reali per un esempio di polisemia francese (parola con due
   significati distanti, verificabile nella sessione successiva con vettori fastText
   francesi reali).

Verifica: rileggi la traduzione confrontandola frase per frase con l'originale italiano.
Documenta in decision-log.md e next-steps.md, poi commit. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```

---

## Prompt 6 — FR, parte b: ricostruzione dati reali + assemblaggio + verifica

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che la traduzione francese e i corpora nativi (Fase 3-FR-a) esistano e siano
committati; se non lo sono, fermati e segnalalo.

Compito: identico nella struttura al Prompt 4 (EN, parte b), applicato al francese.
Ricostruisci con lo stesso rigore già documentato nel decision-log per l'italiano:

1. Tokenizzatore BPE addestrato sul corpus del Modulo 00 tradotto in francese
   (src/corso-llm/traduzioni/testo_fr.md) — verifica 0 errori di round-trip e
   comportamento su 2-3 neologismi francesi plausibili. Salva in
   bpe_merges_modulo1_fr.json.
2. Predittore n-grammi sul corpus francese nativo (corpus_ngram_fr.md) — tabelle di
   conteggio, tre prefissi dimostrativi scelti dopo aver visto le distribuzioni reali,
   calibrazione ricostruita su split train/held-out francese. Salva in
   ngram_dati_modulo2_fr.json e calibrazione_modulo2_fr.json.
3. Vettori fastText francesi reali (cc.fr.300.vec) per 23 parole nei 4 gruppi tematici;
   esempio di polisemia francese verificato empiricamente con similarità coseno reali;
   aritmetica vettoriale di genere verificata sui vettori reali francesi, riportando il
   risultato reale. Salva in embedding_dati_moduli_3_5_fr.json.
4. Coppia base-vs-fine-tuned adattata concettualmente in francese, fenomeno reale
   preservato. Salva in base_vs_tuned_modulo6_fr.json.

Integra nei widget, assembla output/dal-bit-alle-entita-semantiche_fr.html, con la stessa architettura
di navigazione/namespacing/tema chiaro-scuro già stabilita in Fase 2. Verifica meccanica
finale identica alle sessioni precedenti (sintassi JS reale sull'intero file, HTML ben
formato, id univoci nell'intero documento, nessuna classe orfana, dati confrontati
byte-per-byte con i nuovi JSON sorgente francesi). Copia su Desktop per la verifica
dell'utente.

Documenta in decision-log.md e next-steps.md, poi commit. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```

---

## Prompt 7 — DE, parte a: traduzione prosa + corpora linguistici nativi

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che output/dal-bit-alle-entita-semantiche_it.html esista e sia già stato verificato/committato
(Fase 2); se non lo è, fermati e segnalalo. Questa sessione è indipendente dal lavoro sulle
versioni inglese e francese (può girare prima, dopo, o in parallelo).

Compito, parte 1 di 2 per la lingua tedesca (la parte 2 è un prompt separato successivo).
Traduci in tedesco TUTTA la prosa di output/dal-bit-alle-entita-semantiche_it.html (introduzione,
indice, tutti e 12 i capitoli), stesso registro professionale/accademico già stabilito in
italiano, stessi fatti/citazioni/nomi/anni identici, stesso registro di domanda aperta
preservato ovunque. Salva il risultato intermedio in src/corso-llm/traduzioni/testo_de.md.

Corpora linguistici nativi, NON tradotti meccanicamente dall'italiano:
1. Verifica che la traduzione tedesca del Modulo 00 narrativo sia una buona base per un
   futuro corpus di addestramento BPE (nessuna azione extra oltre a una buona traduzione;
   tieni presente che la morfologia tedesca, con le parole composte, potrebbe produrre un
   comportamento BPE interessante da notare per l'unità 1.3 sul problema del vocabolario —
   annotalo se emerge qualcosa di pedagogicamente rilevante, senza forzarlo).
2. Scrivi da zero (non tradurre) un nuovo corpus di circa 46 frasi tedesche semplici per il
   predittore n-grammi del Modulo 2, con pattern ripetuti naturali in tedesco. Salva in
   src/corso-llm/traduzioni/corpus_ngram_de.md.
3. Annota eventuali candidati reali per un esempio di polisemia tedesca (parola con due
   significati distanti, verificabile nella sessione successiva con vettori fastText
   tedeschi reali).

Verifica: rileggi la traduzione confrontandola frase per frase con l'originale italiano.
Documenta in decision-log.md e next-steps.md, poi commit. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```

---

## Prompt 8 — DE, parte b: ricostruzione dati reali + assemblaggio + verifica

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md —
verifica che la traduzione tedesca e i corpora nativi (Fase 3-DE-a) esistano e siano
committati; se non lo sono, fermati e segnalalo.

Compito: identico nella struttura al Prompt 4 (EN, parte b) e al Prompt 6 (FR, parte b),
applicato al tedesco. Ricostruisci con lo stesso rigore già documentato nel decision-log
per l'italiano:

1. Tokenizzatore BPE addestrato sul corpus del Modulo 00 tradotto in tedesco
   (src/corso-llm/traduzioni/testo_de.md) — verifica 0 errori di round-trip e
   comportamento su 2-3 neologismi tedeschi plausibili. Salva in
   bpe_merges_modulo1_de.json.
2. Predittore n-grammi sul corpus tedesco nativo (corpus_ngram_de.md) — tabelle di
   conteggio, tre prefissi dimostrativi scelti dopo aver visto le distribuzioni reali,
   calibrazione ricostruita su split train/held-out tedesco. Salva in
   ngram_dati_modulo2_de.json e calibrazione_modulo2_de.json.
3. Vettori fastText tedeschi reali (cc.de.300.vec) per 23 parole nei 4 gruppi tematici;
   esempio di polisemia tedesca verificato empiricamente con similarità coseno reali;
   aritmetica vettoriale di genere verificata sui vettori reali tedeschi, riportando il
   risultato reale. Salva in embedding_dati_moduli_3_5_de.json.
4. Coppia base-vs-fine-tuned adattata concettualmente in tedesco, fenomeno reale
   preservato. Salva in base_vs_tuned_modulo6_de.json.

Integra nei widget, assembla output/dal-bit-alle-entita-semantiche_de.html, con la stessa architettura
di navigazione/namespacing/tema chiaro-scuro già stabilita in Fase 2. Verifica meccanica
finale identica alle sessioni precedenti (sintassi JS reale sull'intero file, HTML ben
formato, id univoci nell'intero documento, nessuna classe orfana, dati confrontati
byte-per-byte con i nuovi JSON sorgente tedeschi). Copia su Desktop per la verifica
dell'utente.

Documenta in decision-log.md e next-steps.md, poi commit. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```
