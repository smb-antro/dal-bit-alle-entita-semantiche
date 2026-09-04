# Snapshot — cartografia-semantica

Estratto da `qa-tool/` il 2 settembre 2026 (storia git preservata via `git filter-repo`,
vedi decision-log). "Dal bit alle entità semantiche" — saggio interattivo sui modelli
linguistici, in tre Parti (Fondamenti, Genealogia, Meccanismo) più una Presentazione.

```
cartografia-semantica/
├── .claude/worktrees/
├── CLAUDE.md
├── README.md
├── .gitignore                     assets/ + .DS_Store
├── docs/
│   ├── decision-log.md
│   ├── next-steps.md
│   ├── snapshot.md                questo file
│   ├── editorial-guidelines.md    regole di revisione estratte dal lavoro editoriale
│   ├── prompt-sessioni-widget-m2-m4-m6-m3m5.md
│   └── prompt-sessioni-revisione-traduzione-tema.md
├── src/
│   ├── build_output.py            compila saggio/ in output/dal-bit-alle-entita-semantiche_it.html
│   ├── piano_corso_llm.md
│   ├── struttura_moduli_1-6.md
│   ├── inventario_grafico_moduli_1-6.md
│   ├── blocco_a_unita_3-4-5-6_contenuti.md
│   └── saggio/
│       ├── presentazione.html, indice.html
│       ├── fondamenti-1-funzioni-booleane.html, fondamenti-2-hardware-software.html
│       ├── genealogia-1-disputa.html … genealogia-4-corpo.html
│       ├── meccanismo-1-testo-come-dato.html … meccanismo-6-large.html
│       └── *.json, immagini_modulo1/     dataset reali e asset per i widget
├── output/
│   └── dal-bit-alle-entita-semantiche_it.html  file unico autocontenuto, indice + saggio compilato
└── assets/                         PDF di revisione, export design — NON tracciati da git
```

## Stato

Fasi 1-2 (contenuto completo, compilazione, verifica) concluse. Revisione manuale
dell'utente in corso — non riprendere di iniziativa. Aperto: pagina "Lente semantica"
interattiva (da costruire dopo l'aggiornamento dell'ontologia, vedi next-steps).
