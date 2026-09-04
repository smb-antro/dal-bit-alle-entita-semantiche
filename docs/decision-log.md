# Decision log — cs-1-cartografia-semantica

## 2026-09-04 — Creazione del repository

Primo caso studio del portfolio, creato come repository indipendente in
`~/projects/cs-1-cartografia-semantica/`. Combina due lavori dichiarati maturi lo
stesso giorno o poco prima:

- `dominio/` — copiato da `~/projects/cartografia-semantica/` (HEAD `bea0aaa`) via
  `git archive`, non `cp`/clone: solo i file tracciati, nessuna storia git preservata,
  nessun file `.git/`. Rimosso manualmente `.claude/worktrees/.gitkeep` dalla copia —
  era tracciato nel sorgente come scaffold per la propria convenzione worktree, ma non
  ha senso qui: `dominio/` non è un repository a sé in questo contesto.
- `ontologia/` — copiato da `~/projects/vocabolario-ontologia-llm/` (HEAD `1765f29`)
  con lo stesso metodo. Nessun file `.claude`/`.git` presente nella copia.
- `assets/` non copiata in nessuno dei due casi: era vuota (ontologia) o assente
  (dominio) su disco in entrambi i sorgenti al momento della copia, verificato prima di
  procedere — nessuna perdita. Se in futuro uno dei due sorgenti accumula contenuto in
  `assets/` prima di una nuova copia, andrà incluso deliberatamente.
- `design-system/` lasciata vuota di proposito: le linee guida sono ancora in test in
  `~/projects/portfolio/site/`, non ancora mature da formalizzare qui.

**Trovato durante la creazione, non toccato**: esiste già `~/projects/laboratorio-precedente/`,
un "laboratorio informale" (si definisce così nel proprio README) con prototipi
precedenti dello stesso concetto — struttura vera dichiarata esplicitamente rimandata a
quando il lavoro fosse più maturo. Fuori scope per questo repository, che è quel
momento di maturità con un'altra struttura; non migrato né toccato.

## 2026-09-04 — Licenza: decisione rimandata a prima della pubblicazione

Discusse quattro alternative (MIT + CC BY 4.0, MIT + CC BY-NC 4.0, Apache 2.0 +
CC BY-SA 4.0, tutti i diritti riservati). L'utente ha scelto di lasciare la decisione
aperta invece di sceglierne una ora, e di documentarla con un file `LICENSE`
placeholder che elenca le quattro opzioni invece di ometterlo — vedi
[`../LICENSE`](../LICENSE) e [next-steps.md](next-steps.md) per la roadmap verso la
pubblicazione. Non riguarda D3.js (BSD) né EB Garamond (OFL), già vendorizzati con
licenza propria.
