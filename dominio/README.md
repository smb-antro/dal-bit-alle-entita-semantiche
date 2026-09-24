# cartografia-semantica

"Dal bit alle entità semantiche" — saggio interattivo su come funzionano i modelli
linguistici, dai principi discreti dell'hardware fino allo spazio vettoriale in cui si
rappresenta il significato.

- `src/saggio/` — i file HTML del saggio: Presentazione, Parte I (Fondamenti), Parte II
  (Genealogia), Parte III (Meccanismo). Ogni file è autosufficiente (CSS/JS inline),
  navigabile da una sidebar fissa comune.
- `src/build_output.py` — compila tutti i file di `saggio/` in un unico documento
  autocontenuto, `output/dal-bit-alle-entita-semantiche_it.html`. Dal 23 settembre 2026
  include anche la Lente semantica come capitolo, e la compilazione **fallisce** se nel
  file scritto resta un `href`/`src` che non sia `#` o `data:`. Su come aprirlo offline
  (e perché Safari rifiuta un percorso incollato nella barra degli indirizzi) vedi la
  nota nel [README del repository](../README.md#aprire-il-saggio-compilato).
- `docs/` — decision-log, next-steps, snapshot, linee guida editoriali.
- `assets/` — NON tracciata da git: PDF di revisione, export di design.
- `.claude/worktrees/` — sede obbligatoria dei worktree di sessione.

## Stato attuale

Estratto da `qa-tool/` il 2 settembre 2026, con storia git preservata (`git filter-repo`).
Fasi 1-2 (contenuto completo, compilazione, verifica) concluse — revisione manuale
dell'utente in corso, non riprendere di iniziativa senza indicazione esplicita. Vedi
`docs/next-steps.md`.
