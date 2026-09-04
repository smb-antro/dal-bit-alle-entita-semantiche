# Next steps — vocabolario-ontologia-llm

- [x] Fase 1 — Estrazione del vocabolario grezzo da `corso-llm` (`docs/termini-grezzi.md`)
- [x] Fase 2 — Vocabolario controllato SKOS (`src/vocabolario.ttl`)
- [x] Fase 3 — Micro-ontologia OWL (`src/ontologia.ttl`)
- [x] Fase 4 — Popolamento e validazione (`src/dati.ttl`, `src/shapes.ttl`, script)
- [x] Fase 5 — Struttura di consultazione HTML (`output/`)
- [x] Fase 6 — Documento delle decisioni di modellazione in forma finale
- [x] Fase 7 — README di presentazione e verifica end-to-end

Tutte le fasi del piano approvato sono complete. Possibili passi successivi, non
richiesti finora (vedi anche "Limiti noti" in `docs/decisioni-modellazione.md`):
verifica d'uso con 2-3 lettori esterni reali (finora solo autoverifica); decidere una
sede di pubblicazione e sostituire il namespace provvisorio; eventuale pagina di
consultazione per i Dataset (non prevista nel piano, i 16 individui esistono solo nel
grafo).

## Aggiornamento post-estrazione (4 settembre 2026)

- [x] Fase A — Schema (`src/ontologia.ttl`): `:Parte`, `:Modulo`→`:Capitolo`
- [x] Fase B — Vocabolario (`src/vocabolario.ttl`): 111 `:fonte` rinumerati
- [x] Fase C — Generatore dati (`scripts/genera_dati.py`): `PARTI`+`CAPITOLI`, 3 nuovi Teorico
- [x] Fase D — Rigenerazione e validazione (`output/`, `scripts/valida.py`)
- [x] Fase E — Prosa e cornice (`README.md`, `CLAUDE.md`, decision-log, decisioni-modellazione)
- [ ] Fase F — Commit (su richiesta esplicita, non compreso nel piano)

Non richiesto finora, segnalato solo per contesto (dipende da questo aggiornamento, non
lo blocca): la Lente Semantica interattiva e il confronto grafo/ontologie
nell'appendice "Dietro i widget" di `cartografia-semantica` — entrambi lavoro futuro in
quel repository, non in questo.

Segnalato all'utente, non azionabile qui: un'incoerenza reale in
`cartografia-semantica/src/saggio/meccanismo-4-reti-neurali.html` (la correzione
Hebb/Carla Shatz non è arrivata lì, a differenza del passaggio parallelo in
Genealogia).

Piano completo: `~/.claude/plans/`.
