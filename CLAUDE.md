# cs-1-cartografia-semantica

Repository indipendente dentro `~/projects/`. Primo caso studio del portfolio pubblico
su GitHub — la card è già riservata in `portfolio/site/lab.html`
("Dal bit alle entità semantiche").

## Obiettivo

Mettere insieme due lavori nati indipendenti — un saggio interattivo (`dominio/`) e la
sua formalizzazione semantica in SKOS/OWL (`ontologia/`) — per dimostrare il rapporto
tra un dominio narrativo e la sua cartografia semantica, non presentarli come due tool
scollegati.

## Struttura

- `dominio/` — saggio interattivo "Dal bit alle entità semantiche", copiato da
  `~/projects/cartografia-semantica/` (HEAD `bea0aaa` del 4 settembre 2026) via
  `git archive` — solo file tracciati, nessuna storia git preservata.
- `ontologia/` — vocabolario SKOS + micro-ontologia OWL + "Lente semantica" (grafo
  radiale interattivo), copiato da `~/projects/vocabolario-ontologia-llm/` (HEAD
  `1765f29` del 4 settembre 2026), stesso metodo.
- `design-system/` — linee guida di design e i prototipi che le hanno stabilite, vedi `design-system/README.md`.
- `docs/` — decision-log.md, next-steps.md, snapshot.md di questo repository (distinti
  dai docs/ interni a dominio/ e ontologia/, che restano quelli originali).
- `LICENSE` — placeholder con quattro alternative, decisione rimandata a prima della
  pubblicazione.

## Vincoli tecnici

Ereditati da entrambi i sorgenti: nessun build tooling, HTML/CSS vanilla. Font
self-hosted OFL (EB Garamond) in `ontologia/output/fonts/`. D3 v7 vendorizzato BSD in
`ontologia/lente-semantica/output/vendor/`. RDF in Turtle in `ontologia/src/`.

`dominio/` e `ontologia/` sono **copie sola lettura** del loro stato al 4 settembre
2026 — non sincronizzate automaticamente con i repository sorgente; un aggiornamento
richiede ripetere la copia con `git archive` deliberatamente, non un `cp`/rsync.

**`assets/`**: escluso da git in entrambi i sorgenti (convenzione per binari pesanti)
ed era vuoto o assente su disco in entrambi al momento della copia — nessuna perdita.
Se in futuro uno dei due accumula contenuto in `assets/` prima di una nuova copia, va
incluso deliberatamente: un repo portfolio deve rendere per chi lo clona, in deroga
alla convenzione abituale "assets/ escluso".

## Regole operative

- Commit solo su richiesta esplicita dell'utente — anche il primo, nonostante il
  repository sia nuovo.
- Non toccare `~/projects/cartografia-semantica/` né
  `~/projects/vocabolario-ontologia-llm/` da qui: restano archivio storico
  pre-portfolio, sola lettura.
- Non pushare su GitHub finché non richiesto esplicitamente — vedi `docs/next-steps.md`
  per la licenza (ancora da scegliere, vedi `LICENSE`) e la roadmap prima della
  pubblicazione.
- Rinominare/eliminare solo con `git mv`/`git rm`, mai perdere la storia per comodità
  (vale da quando questo repository comincia ad avere una propria storia).
- Un worktree aggiuntivo alla volta, sempre in `.claude/worktrees/`.
- Regole generali di `~/projects/`: vedi `../CLAUDE.md` e `../memoria/`.
