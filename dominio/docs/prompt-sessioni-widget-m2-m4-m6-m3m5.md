# Prompt per sessioni separate — widget Moduli 2, 4, 6, 3/5

Scritti il 2026-07-06 per l'esaurirsi dei limiti di sessione/contesto nella sessione che
ha completato il Modulo 1 (`lezione_01_testo_come_dato.html`, vedi decision-log). Ognuno
di questi prompt è pensato per essere incollato in una **sessione/chat separata**, in
modalità piano, per completare il rispettivo modulo in poche iterazioni.

Tutti e quattro assumono il worktree già esistente
`qa-tool/.claude/worktrees/corso-llm-moduli-1-6/`
(branch `corso-llm-moduli-1-6`) — da non ricreare.

---

## Prompt 1 — Modulo 2

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md
per lo stato del progetto (corso "Come funzionano gli LLM", Modulo 1 già completo).

Compito: costruire src/corso-llm/lezioni/lezione_02_probabilita.html (Modulo 2 —
Probabilità e linguaggio), usando come modello diretto lezione_01_testo_come_dato.html
già completato (stessa shell CSS/JS, navigazione a due livelli livello-modulo +
livello-sezione, stesso metodo di embedding dati incorporati via placeholder).

Contenuti (unità 2.1-2.4): vedi src/corso-llm/struttura_moduli_1-6.md, sezione Modulo 2,
per il dettaglio completo di ciascuna unità incluse le note sul filo discreto/continuo
e sul "terzo filo" (induzione, calibrazione).

Dati già pronti in src/corso-llm/lezioni/: ngram_dati_modulo2.json (corpus scritto apposta,
tabelle di conteggio a finestra 1/2/3, tre prefissi dimostrativi già scelti e verificati)
e calibrazione_modulo2.json (reliability diagram misurato realmente).

Componenti da costruire (vedi src/corso-llm/inventario_grafico_moduli_1-6.md, sezione
Modulo 2): predittore n-grammi interattivo con slider di contesto e barre di probabilità;
diagramma di calibrazione per 2.2; piccolo contenuto statico per le dipendenze lontane
in 2.4 (non serve dataset).

Metodo: scrivi prima l'unità 2.1 da sola, copiala su Desktop per farla verificare
dall'utente (il server di anteprima integrato ha un limite di sandbox noto — nega
l'accesso a getcwd() — non perderci tempo), attendi conferma, poi procedi con 2.2-2.4.
Prima di consegnare qualunque HTML, verifica SEMPRE la sintassi JS con un motore reale
(osascript -l JavaScript su macOS, via new Function(codice_estratto)), non solo il
bilanciamento dei tag HTML — un doppio backslash in una stringa ha bloccato l'intero
script in M1 e i soli controlli HTML non l'avevano preso. Documenta in decision-log.md
e next-steps.md, poi commit. Non toccare src/corso-agenti/ né src/capstone-qualitativo/.
```

---

## Prompt 2 — Modulo 4

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md.

Compito: costruire src/corso-llm/lezioni/lezione_04_reti_neurali.html (Modulo 4 — Reti
neurali), usando come modello lezione_01_testo_come_dato.html già completato (stessa
shell, stesso metodo di verifica).

Contenuti (unità 4.1-4.5): vedi struttura_moduli_1-6.md, sezione Modulo 4 — include
Bateson/pleroma-creatura (4.3), Varela/autopoiesi (4.1), schismogenesi vs backprop e
memristor (4.5): sono contenuto testuale/concettuale, NON richiedono widget dedicati.

Dati già pronti in src/corso-llm/lezioni/: xor_rete_modulo4.json (rete addestrata, 4/4
corretto, griglia 100x100 per il confine di decisione), paesaggio_perdita_modulo4.json
(formula a due minimi, gradiente, traiettorie verificate), neurone_esempi_modulo4.json.

ATTENZIONE — punto più a rischio del modulo: la superficie di perdita (4.4/4.5) va resa
con uno SHADER GLSL/SDF (WebGL), non Canvas/SVG come il resto del sito — decisione già
presa in sessione precedente, non rivederla, ma è la prima volta che si esce dal vanilla
JS. Consiglio: costruisci prima 4.1 (neurone, sliders) e 4.2/4.3 (XOR, griglia già pronta,
disegnabile anche solo con SVG/Canvas) — componenti a basso rischio con pattern già
consolidati — e lascia lo shader per ultimo. Se lo shader richiede più iterazioni di
quelle disponibili in questa sessione, è accettabile consegnare 4.1-4.3 completi e
lasciare 4.4/4.5 con un fallback temporaneo (contorno/heatmap su Canvas) esplicitamente
segnalato come provvisorio in decision-log, invece di bloccare tutto il modulo.

Metodo: primo campione (4.1) verificato dall'utente su Desktop prima di procedere.
Verifica SEMPRE la sintassi JS con motore reale (osascript -l JavaScript, new
Function(codice)) prima di consegnare — vedi decision-log per il bug reale già trovato
in M1. Documenta e committa. Non toccare src/corso-agenti/ né src/capstone-qualitativo/.
```

---

## Prompt 3 — Modulo 6

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md.

Compito: costruire src/corso-llm/lezioni/lezione_06_large.html (Modulo 6 — Cosa
significa "Large"), usando come modello lezione_01_testo_come_dato.html già completato.

Contenuti (unità 6.1-6.6): vedi struttura_moduli_1-6.md, sezione Modulo 6 — include la
chiusura del filo discreto/continuo (6.6, quantizzazione) e la domanda finale
deliberatamente irrisolta (continuo primitivo vs discreto primitivo).

Dati già pronti in src/corso-llm/lezioni/: scala_modulo6.json (numeri reali con fonti:
86 miliardi di neuroni, GPT-3, PaLM), timeline_modulo6.json (riusa le classi CSS
.timeline/.tl-node/.tl-tag/.tl-date/.tl-title/.tl-desc già in lezione_00_blocco_a.html,
NON inventare nuovo stile), capacita_emergenti_modulo6.json (dati illustrativi dichiarati
come tali), base_vs_tuned_modulo6.json, quantizzazione_modulo6.json.

Componenti (vedi inventario_grafico_moduli_1-6.md, sezione Modulo 6): modulo
deliberatamente più leggero sull'interattività (principio già stabilito: non dare falsa
certezza su fenomeni dibattuti come le capacità emergenti) — slider log-scala (6.1),
grafico annotato poco interattivo (6.2), timeline (6.3), toggle prima/dopo (6.4/6.5),
barra che si spacca in blocchi discreti (6.6).

Metodo: primo campione (6.1) verificato dall'utente su Desktop prima di procedere.
Verifica SEMPRE la sintassi JS con motore reale (osascript -l JavaScript) prima di
consegnare. Documenta e committa. Non toccare src/corso-agenti/ né
src/capstone-qualitativo/.
```

---

## Prompt 4 — Modulo 3/5 (con Fable)

```
Lavora in modalità piano. Worktree già esistente, NON crearne uno nuovo:
qa-tool/.claude/worktrees/corso-llm-moduli-1-6/
(branch corso-llm-moduli-1-6). Leggi prima docs/decision-log.md e docs/next-steps.md
per lo stato del progetto e il metodo già stabilito (vedi in particolare le voci sul
Modulo 1 completato, che fa da modello diretto).

Compito: costruire src/corso-llm/lezioni/lezione_03_embedding.html (Modulo 3 — Parole
come punti nello spazio) e lezione_05_transformer.html (Modulo 5 — Il Transformer),
come DUE FILE SEPARATI E AUTONOMI, entrambi basati sugli stessi dati già pronti e
verificati in src/corso-llm/lezioni/embedding_dati_moduli_3_5.json (23 parole, vettori
reali fastText italiani, tre modalità: esplorazione, aritmetica, polisemia). Decisione
già presa esplicitamente con l'utente: NIENTE vera interazione live tra le due pagine —
il widget di M5 ricrea una propria mini-mappa usando gli stessi dati/assi di M3 per
mostrare la parola polisemica "calcio" che si sposta da statica a contestuale, ma resta
dentro la sua pagina. Non riaprire questa decisione architetturale.

Contenuti: vedi src/corso-llm/struttura_moduli_1-6.md, sezioni Modulo 3 (unità 3.1-3.5:
include Cantor/numerabilità in 3.1, Leibniz e il termine "embedding" in 3.2, Wittgenstein/
ipotesi distribuzionale in 3.3, Bateson/sillogismo dell'erba e Wigner in 3.4, polisemia
in 3.5) e Modulo 5 (unità 5.1-5.6: ponte RNN anonimo in 5.1, QKV in 5.3, il crollo
"quantistico" Galileo/osservatore in 5.4 — cuore concettuale dell'unità, non decorazione
— posizione in 5.5).

Componenti (vedi src/corso-llm/inventario_grafico_moduli_1-6.md, sezioni Modulo 3 e 5):
M3 = mappa navigabile dello spazio embedding, riusata/riconfigurata per esplorazione
(3.1/3.2), aritmetica vettoriale con possibilità di provare altre combinazioni (3.4),
punto polisemico fermo tra due gruppi (3.5). M5 = frase cliccabile con pesi di attention
mostrati come spessore/opacità delle connessioni, multi-head come interruttore 2-3
pattern (5.5), piccola animazione per la codifica di posizione.

Metodo di lavoro, importante — a differenza delle altre sessioni gemelle (M2/M4/M6):
1. La PROGETTAZIONE dei due widget (interazioni esatte, come i tre modi di M3 si
   attivano/transitano, come M5 ricrea la mini-mappa) va fatta in conversazione diretta
   con l'utente, NON delegata. Proponi una specifica concreta, fatti confermare.
2. Solo dopo la conferma della specifica, costruisci un PRIMO PROTOTIPO usando il tool
   Agent con model:"fable" (Claude Fable 5) — è il test hands-on già programmato per
   questo modello su un compito delimitato. Dagli in prompt la specifica confermata, i
   percorsi esatti dei file, e il riferimento a lezione_01_testo_come_dato.html come
   modello di shell/stile/metodo di verifica.
3. Verifica tu stesso il risultato di Fable con lo stesso rigore già stabilito: sintassi
   JS con motore reale (osascript -l JavaScript, new Function(codice) — non solo
   controlli HTML), corrispondenza dati, nessuna classe CSS inventata.
4. Copia su Desktop per la verifica visiva dell'utente (il server di anteprima integrato
   ha un limite di sandbox noto — nega l'accesso a getcwd() — non perderci tempo).
5. Documenta in decision-log.md anche una valutazione esplicita di come si è comportato
   Fable sul compito (qualità del codice, aderenza alla specifica, eventuali problemi) —
   è il primo uso reale di questo modello nel progetto, vale la pena registrarlo.
6. Committa. Non toccare src/corso-agenti/ né src/capstone-qualitativo/.
```
