# cartografia-semantica

Repository indipendente dentro `~/projects/`. Estratto da `qa-tool/` il 2 settembre 2026
come `corso-llm` (storia git preservata via `git filter-repo` — vedi
`docs/decision-log.md`, voce del 2 settembre), poi rinominato lo stesso giorno per
riflettere il titolo e la natura di saggio interattivo, non più corso. Prima viveva
insieme a due progetti correlati (`corso-agenti`, `capstone-qualitativo`) con cui non
condivide nulla — separazione naturale.

## Struttura

- `src/saggio/` — i 12 file HTML del saggio interattivo "Dal bit alle entità semantiche",
  più `presentazione.html` e `indice.html`. Ogni file è autosufficiente, con una sidebar
  fissa condivisa (indice ad accordion + scroll-spy).
- `src/build_output.py` — compila `saggio/` in `output/dal-bit-alle-entita-semantiche_it.html`, un
  documento unico autocontenuto (sidebar unica, navigazione via `showChapter()`).
- `src/piano_corso_llm.md`, `struttura_moduli_1-6.md`, `inventario_grafico_moduli_1-6.md`,
  `blocco_a_unita_3-4-5-6_contenuti.md` — pianificazione di processo, non contenuto
  pubblicato. Usano ancora terminologia dell'epoca in cui il progetto era concepito come
  "corso" a moduli/blocchi — lasciata intatta deliberatamente: registra la logica reale con
  cui il lavoro è stato costruito, non va riscritta a posteriori.

## Stato

Fasi 1-2 (contenuto completo, compilazione, verifica) concluse — **non definitivo**:
revisione manuale dell'utente in corso, non riprendere di iniziativa. Fase 3 (traduzioni
EN/FR/DE) pianificata ma rimandata su richiesta esplicita, non ancora avviata. Pagina
"Lente semantica" interattiva da costruire dopo l'aggiornamento dell'ontologia (vedi
`docs/next-steps.md`).

## Regole operative

- Commit solo su richiesta esplicita dell'utente.
- `assets/` esclusa in blocco da git — vedi `.gitignore`.
- Un worktree aggiuntivo alla volta, sempre in `.claude/worktrees/`.
- Rinominare/eliminare solo con `git mv`/`git rm`, mai perdere la storia per comodità.
- Regole generali di `~/projects/`: vedi `../CLAUDE.md` e `../memoria/`.
