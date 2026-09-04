# vocabolario-ontologia-llm

Repository indipendente dentro `~/projects/`.

## Obiettivo

Portfolio: vocabolario controllato (SKOS) e micro-ontologia (OWL) sul saggio interattivo
"Dal bit alle entità semantiche" (`~/projects/cartografia-semantica/src/saggio/`, ex
corso "Come funzionano i LLM"), con una struttura di consultazione HTML derivata dal
modello e un documento delle decisioni di modellazione come deliverable primario — non
un'appendice.

## Fonte del dominio

`~/projects/cartografia-semantica/src/saggio/` è **sola lettura**: mai modificato da
questo progetto. Il saggio era dichiarato "non definitivo" nel suo repository fino al
4 settembre 2026 (revisione manuale dell'autore in corso), poi dichiarato definitivo in
quella data — il vocabolario riflette lo stato del saggio alla data di aggiornamento più
recente dichiarata in `docs/decision-log.md`, non un testo che si aggiorna da solo.

## Struttura

```
docs/          decision-log.md, next-steps.md, snapshot.md
src/           .ttl (Turtle) e script di modellazione/validazione
assets/        esclusa da git — binari pesanti/rigenerabili
output/        pagine HTML della struttura di consultazione, tracciate normalmente
```

## Vincoli tecnici

- Nessun build tooling. HTML/CSS vanilla. Font self-hosted OFL (EB Garamond + maiuscoletto
  spaziato per l'apparato). Accento verde solo su numerazione/rimandi.
- RDF in Turtle, scritto/generato a mano o da script — mai da GUI.
- Validazione/query da riga di comando (rdflib, pySHACL) in un venv isolato
  (`requirements.txt`).

## Regole operative

- Commit solo su richiesta esplicita dell'utente.
- Un worktree aggiuntivo alla volta, sempre in `.claude/worktrees/`.
- Regole generali di `~/projects/`: vedi `../CLAUDE.md` e `../memoria/`.
