# Linee guida editoriali — qa-tool

Regole estratte dal lavoro di editing sul corso-llm (Presentazione + refactor sidebar
sui 12 file di `lezioni/`, agosto-settembre 2026). Versione curata a mano di quanto
tracciato nella memoria automatica di Claude Code — va aggiornata manualmente quando
emergono nuove regole, non si sincronizza da sola.

## Scrittura e contenuto

- **Mai il titolo come soggetto grammaticale.** Evitare "«Titolo» è organizzato in tre
  parti" o "Fondamenti parte dalle funzioni booleane...". Riscrivere con soggetto
  neutro: "Il saggio è organizzato in tre parti. La prima... La seconda... La terza e
  ultima...". Attenzione alle collisioni che la riscrittura può introdurre (es. "la
  prima parte parte da..." — risolvere cambiando il verbo, non il soggetto).

- **Un rename di titolo non è mai locale.** Cambiare l'h1 non basta: vanno ricontrollati
  `<title>`, sidebar-title, `indice.html`, e soprattutto le frasi che presuppongono la
  *forma* del vecchio titolo (es. una frase costruita sul fatto che il titolo fosse una
  domanda), non solo il suo testo letterale. Fare uno sweep sistematico (grep su tutto
  `src/corso-llm/`, sia `lezioni/*.html` sia `build_output.py`), non fidarsi della
  memoria.

- **Critica prima di eseguire, sulle riscritture soggettive.** Quando una richiesta di
  riscrittura sembra ridondante con contenuto già esistente, debole, o incoerente con
  scelte fatte altrove, dirlo prima di applicare la modifica — non eseguire e basta, e
  non correggere in silenzio.

- **Citazioni e riferimenti non verificabili restano segnalati come tali.** Attribuzioni
  (es. Bateson) e riferimenti normativi (es. EU AI Act) che non si possono controllare
  contro la fonte originale vanno esplicitamente marcati come da verificare da parte
  dell'utente — mai dati per buoni.

## Refactoring meccanico multi-file

- **Codice morto: cancellare, non disattivare.** Non avvolgere un blocco JS obsoleto in
  wrapper inerti (`<script type="application/json">`, id tipo `unused-...` o
  `DELETE-ME`) come passo intermedio — va rimosso subito. Dopo ogni file toccato, grep
  dei simboli vecchi per confermare zero residui, non solo a fine lavoro.

- **Architettura ambigua → chiedere, non assumere.** Se una modifica strutturale può
  sostituire o affiancare qualcosa di esistente (es. una nuova sidebar rispetto a una
  nav a due livelli), chiedere esplicitamente quale dei due prima di procedere.

- **Refactor ampi e meccanici su molti file → modalità pianifica.** Riduce il rischio di
  applicare un pattern sbagliato N volte prima di accorgersene; verificare poi con un
  campione rappresentativo (incluso almeno un file con widget/script pesanti) invece che
  su tutti i file.

- **Duplicazioni intenzionali vanno tracciate esplicitamente.** Il contenuto della
  Presentazione vive sia in `build_output.py` (`build_intro_and_toc()`) sia in
  `lezioni/presentazione.html`, per scelta esplicita dell'utente — ogni modifica futura
  al testo introduttivo deve aggiornare entrambe le copie.
