#!/usr/bin/env python3
"""Genera src/dati.ttl a partire da strutture dati esplicite (Fase 4).

Le decisioni di modellazione (chi è un Teorico, quale relazione mappare su quale
object property, quale dataset è "reale" vs "illustrativo") sono scritte a mano qui
sotto, in Python — questo script si limita a serializzarle in Turtle in modo
meccanico e ripetibile. Vedi docs/decisioni-modellazione.md, sezione Fase 4, per il
razionale di ogni scelta non ovvia.

Aggiornato il 4 settembre 2026 per la nuova struttura in tre Parti
(Fondamenti/Genealogia/Meccanismo) del saggio «Dal bit alle entità semantiche» — vedi
docs/decisioni-modellazione.md, sezione "Aggiornamento post-estrazione".

Uso: .venv/bin/python3 scripts/genera_dati.py > src/dati.ttl
"""

NS = "http://example.org/corso-llm-vocabolario#"

# ---------------------------------------------------------------------------
# Parti, Capitoli e Unità — mappatura dalla struttura reale del saggio
# (~/projects/cartografia-semantica/src/saggio/indice.html), verificata direttamente
# capitolo per capitolo e unità per unità il 4 settembre 2026, non presa dal solo
# resoconto dell'utente. Fondamenti non ha sotto-unità (2 capitoli atomici, che
# restano il bersaglio citabile più fine — vedi ontologia.ttl, :discussoInUnita).
# ---------------------------------------------------------------------------

PARTI = {
    "ParteFondamenti": "Fondamenti",
    "ParteGenealogia": "Genealogia",
    "ParteMeccanismo": "Meccanismo",
}

# capitolo_slug: (numero_capitolo, titolo_capitolo, parte_slug, unità_o_None)
# unità: lista di (slug, "N.M", titolo) — slug Meccanismo invariati dall'esecuzione
# precedente (solo rietichettati/riparentati); slug Genealogia nuovi (Gen11..Gen42,
# rimpiazzano UA1..UD2); Fondamenti nuovi (nessun equivalente precedente, prima
# annegati dentro "Modulo00").
CAPITOLI = {
    "Fondamenti1": ("1", "Funzioni booleane", "ParteFondamenti", None),
    "Fondamenti2": ("2", "Hardware e software", "ParteFondamenti", None),
    "Genealogia1": ("1", "Tre ore di disputa senza esito", "ParteGenealogia", [
        ("Gen11", "1.1", "Dalla characteristica universalis alla pura ideografia"),
        ("Gen12", "1.2", "Gödel, Turing, Lucas"),
        ("Gen13", "1.3", "Il perceptron e la disgiunzione esclusiva (XOR)"),
        ("Gen14", "1.4", "Dai sistemi esperti alle macchine statistiche"),
        ("Gen15", "1.5", "Re, donna, regina"),
        ("Gen16", "1.6", "L'attenzione sostituisce la memoria"),
    ]),
    "Genealogia2": ("2", "Il fenomeno e i suoi limiti", "ParteGenealogia", [
        ("Gen21", "2.1", "Completamento statistico a scala massiva, in-context learning, transfer cross-dominio e altre capacità emergenti"),
        ("Gen22", "2.2", "Interpolazione, pesi statistici, metacognizione"),
        ("Gen23", "2.3", "Grounding, ragionamento causale, generalizzazione composizionale, cortocircuito dell'apprendimento"),
    ]),
    "Genealogia3": ("3", "Perché ci vuole un villaggio", "ParteGenealogia", [
        ("Gen31", "3.1", "Il problema del significato"),
        ("Gen32", "3.2", "Il problema della causalità"),
        ("Gen33", "3.3", "Il problema biologico"),
        ("Gen34", "3.4", "Il problema della coscienza"),
        ("Gen35", "3.5", "Cosa siamo, per contrasto"),
    ]),
    "Genealogia4": ("4", "Lo spazio, il corpo, la macchina", "ParteGenealogia", [
        ("Gen41", "4.1", "Cos'è lo spazio? Il corpo come strumento di misura"),
        ("Gen42", "4.2", "Il corpo mancante"),
    ]),
    "Meccanismo1": ("1", "Il testo come dato", "ParteMeccanismo", [
        ("U11", "1.1", "Encoding"), ("U12", "1.2", "Tokenizzazione"),
        ("U13", "1.3", "Problema del vocabolario"),
        ("U14", "1.4", "Dagli ID al punto più discreto"), ("U15", "1.5", "Gödel"),
    ]),
    "Meccanismo2": ("2", "Probabilità e linguaggio", "ParteMeccanismo", [
        ("U21", "2.1", "Prevedere la parola successiva"),
        ("U22", "2.2", "Unigrammi/bigrammi, induzione, calibrazione"),
        ("U23", "2.3", "N-grammi e assunzione di Markov"),
        ("U24", "2.4", "Sparsità e dipendenze lontane"),
    ]),
    "Meccanismo3": ("3", "Parole come punti nello spazio", "ParteMeccanismo", [
        ("U31", "3.1", "Il problema lasciato aperto"),
        ("U32", "3.2", "Le parole come vettori (embedding)"),
        ("U33", "3.3", "L'ipotesi distribuzionale"),
        ("U34", "3.4", "L'aritmetica vettoriale"),
        ("U35", "3.5", "Polisemia ed embedding statico"),
    ]),
    "Meccanismo4": ("4", "Reti neurali", "ParteMeccanismo", [
        ("U41", "4.1", "Dal neurone biologico al neurone artificiale"),
        ("U42", "4.2", "Il perceptron e XOR"),
        ("U43", "4.3", "Strati e profondità"),
        ("U44", "4.4", "La funzione di perdita"),
        ("U45", "4.5", "Il gradiente e la backpropagation"),
    ]),
    "Meccanismo5": ("5", "Il Transformer", "ParteMeccanismo", [
        ("U51", "5.1", "Il problema che l'attenzione risolve"),
        ("U52", "5.2", "L'idea dell'attention"),
        ("U53", "5.3", "Query, Key, Value"),
        ("U54", "5.4", "Embedding contestuale"),
        ("U55", "5.5", "Multi-head e posizione"),
        ("U56", "5.6", "Parallelismo e scala"),
    ]),
    "Meccanismo6": ("6", "Cosa significa \"Large\"", "ParteMeccanismo", [
        ("U61", "6.1", "Scala"), ("U62", "6.2", "Capacità emergenti"),
        ("U63", "6.3", "I dati"), ("U64", "6.4", "Fine-tuning"),
        ("U65", "6.5", "RLHF"), ("U66", "6.6", "Quantizzazione (chiusura dell'arco tecnico)"),
    ]),
}

# codice completo ("Parte · N.M", o "Parte · N" per Fondamenti) -> slug. Per
# Fondamenti il codice risolve direttamente al Capitolo (nessuna Unità propria).
CODE_TO_SLUG = {}
for cap_slug, (cap_num, _, parte_slug, unita) in CAPITOLI.items():
    parte_label = PARTI[parte_slug]
    if unita is None:
        CODE_TO_SLUG[f"{parte_label} · {cap_num}"] = cap_slug
    else:
        for u_slug, u_code, _ in unita:
            CODE_TO_SLUG[f"{parte_label} · {u_code}"] = u_slug

# ---------------------------------------------------------------------------
# Espansione dei valori :fonte (riscritti a mano in vocabolario.ttl il 4 settembre
# 2026 secondo la tabella di mappatura in docs/decisioni-modellazione.md) in liste
# di codici unità. Ogni lista qui sotto è stata derivata dalla precedente
# (Fase 4 originale) applicando la stessa tabella di rinomina, poi riverificata
# contro i nuovi valori di vocabolario.ttl — non un parser generico rieseguito
# alla cieca (vedi decisioni-modellazione.md, Fase 4 #2 e Aggiornamento
# post-estrazione).
# ---------------------------------------------------------------------------

FONTE_ESPANSA = {
    "Discretizzazione": ["Meccanismo · 1.1", "Meccanismo · 6.3", "Fondamenti · 2"],
    "Encoding": ["Meccanismo · 1.1"], "AsciiUnicode": ["Meccanismo · 1.1"],
    "Tokenizzazione": ["Meccanismo · 1.2", "Meccanismo · 1.3"],
    "Bpe": ["Meccanismo · 1.2", "Meccanismo · 1.3"],
    "Token": ["Meccanismo · 1.2", "Meccanismo · 1.3", "Meccanismo · 1.4", "Meccanismo · 1.5"],
    "TokenId": ["Meccanismo · 1.4"], "ProblemaDelVocabolario": ["Meccanismo · 1.3"],
    "FondamentiLogicoMatematici": ["Genealogia · 1.1", "Genealogia · 1.2", "Meccanismo · 1.5"],
    "SistemaFormale": ["Meccanismo · 1.5", "Genealogia · 1.2", "Genealogia · 1.6"],
    "Numerabilita": ["Meccanismo · 1.5", "Meccanismo · 3.1"],
    "TeoremaIncompletezzaGodel": ["Genealogia · 1.2", "Meccanismo · 1.5"],
    "Aritmetizzazione": ["Genealogia · 1.2", "Meccanismo · 1.5"],
    "TestDiTuring": ["Genealogia · 1.2"],
    "DiagonaleDiCantor": ["Meccanismo · 1.5", "Meccanismo · 3.1"],
    "StoriaIntelligenzaArtificiale": [f"Genealogia · 1.{i}" for i in range(1, 7)],
    "SistemaEsperto": ["Genealogia · 1.4"], "Brittleness": ["Genealogia · 1.4"],
    "DeepLearning": ["Genealogia · 1.5"],
    "HiddenMarkovModel": ["Genealogia · 1.4"], "SupportVectorMachine": ["Genealogia · 1.4"],
    "RetiRicorrentiLstm": ["Genealogia · 1.6"],
    "ProbabilitaEPrevisioneLinguistica": [f"Meccanismo · 2.{i}" for i in range(1, 5)],
    "ProbabilitaComeNumeroReale": ["Meccanismo · 2.2"], "Induzione": ["Meccanismo · 2.2"],
    "Calibrazione": ["Genealogia · 2.2", "Meccanismo · 2.2"], "ReliabilityDiagram": ["Meccanismo · 2.2"],
    "Ngramma": ["Meccanismo · 2.3"], "AssunzioneDiMarkov": ["Meccanismo · 2.3"],
    "Sparsita": ["Meccanismo · 2.4", "Meccanismo · 3.1"],
    "DipendenzeLungoRaggio": ["Meccanismo · 2.4", "Meccanismo · 5.1"],
    "CompletamentoStatistico": ["Genealogia · 2.1", "Meccanismo · 2.1"],
    "SpazioSemanticoEEmbedding": [f"Meccanismo · 3.{i}" for i in range(1, 6)],
    "Embedding": ["Meccanismo · 3.2"], "EmbeddingStatico": ["Meccanismo · 3.5"],
    "EmbeddingContestuale": ["Meccanismo · 5.4"], "CollassoContestuale": ["Meccanismo · 5.4"],
    "IpotesiDistribuzionale": ["Meccanismo · 3.3"], "AritmeticaVettoriale": ["Meccanismo · 3.4"],
    "SillogismoDellErba": ["Meccanismo · 3.4"], "Abduzione": ["Meccanismo · 3.4"],
    "QualitaPrimarieSecondarie": ["Meccanismo · 3.2", "Meccanismo · 5.4"], "Polisemia": ["Meccanismo · 3.5"],
    "IrragionevoleEfficaciaMatematica": ["Meccanismo · 3.4"],
    "Word2Vec": ["Genealogia · 1.5", "Meccanismo · 3.3"], "FastText": ["Meccanismo · 3.2"],
    "ReteNeuraleEApprendimento": [f"Meccanismo · 4.{i}" for i in range(1, 6)],
    "NeuroneArtificiale": ["Meccanismo · 4.1"], "FunzioneAttivazione": ["Meccanismo · 4.1"],
    "Bias": ["Meccanismo · 4.1"],
    "SeparabilitaLineare": ["Genealogia · 1.3", "Meccanismo · 4.2"], "MultiLayerPerceptron": ["Meccanismo · 4.3"],
    "Backpropagation": ["Genealogia · 1.5", "Meccanismo · 4.5"], "FunzionePerdita": ["Meccanismo · 4.4"],
    "Gradiente": ["Meccanismo · 4.5"], "MinimoLocaleGlobale": ["Meccanismo · 4.5"],
    "DiscesaDelGradiente": ["Meccanismo · 4.5"],
    "BiologiaCognizioneETeoriaSistemi": ["Meccanismo · 4.1", "Meccanismo · 4.3", "Meccanismo · 4.5"],
    "Autopoiesi": ["Meccanismo · 4.1"], "ChiusuraOperazionale": ["Meccanismo · 4.1"],
    "PleromaCreatura": ["Meccanismo · 4.3"],
    "Schismogenesi": ["Meccanismo · 4.5"], "PlasticitaSinaptica": ["Meccanismo · 4.5", "Genealogia · 3.3"],
    "TransformerEAttenzione": [f"Meccanismo · 5.{i}" for i in range(1, 7)],
    "Attention": [f"Meccanismo · 5.{i}" for i in range(1, 7)],
    "QueryKeyValue": ["Meccanismo · 5.3"], "Softmax": ["Meccanismo · 5.3"],
    "MultiHeadAttention": ["Meccanismo · 5.5"], "CodificaPosizione": ["Meccanismo · 5.5"],
    "Parallelismo": ["Meccanismo · 5.6"],
    "CapacitaELimitiDeiLlm": ["Genealogia · 2.1", "Genealogia · 2.2", "Genealogia · 2.3"],
    "InContextLearning": ["Genealogia · 2.1"], "TransferCrossDominio": ["Genealogia · 2.1"],
    "CapacitaEmergenti": ["Genealogia · 2.1", "Meccanismo · 6.2"], "Allucinazione": ["Genealogia · 2.2"],
    "MetacognizioneSimulata": ["Genealogia · 2.2"], "Grounding": ["Genealogia · 2.3", "Genealogia · 3.1"],
    "RagionamentoCausale": ["Genealogia · 2.3", "Genealogia · 3.2"],
    "GeneralizzazioneComposizionale": ["Genealogia · 2.3"],
    "ApprendimentoContinuoAssente": ["Genealogia · 2.3"],
    "FilosofiaLinguaggioEMente": ["Genealogia · 3.1", "Genealogia · 3.4"],
    "SensoRiferimento": ["Genealogia · 3.1"], "SignificatoComeUso": ["Genealogia · 3.1", "Meccanismo · 3.3"],
    "StanzaCinese": ["Genealogia · 3.1"], "ProblemaDifficileCoscienza": ["Genealogia · 3.4"],
    "IntegratedInformationTheory": ["Genealogia · 3.4"], "GlobalWorkspaceTheory": ["Genealogia · 3.4"],
    "HigherOrderTheories": ["Genealogia · 3.4"],
    "FilosofiaSpazioECorpo": ["Genealogia · 4.1", "Genealogia · 4.2"],
    "SpazioContenitoreAssoluto": ["Genealogia · 4.1"], "SpazioFormaIntuizione": ["Genealogia · 4.1"],
    "SpazioVissuto": ["Genealogia · 4.1"], "BayesianBrain": ["Genealogia · 4.1"],
    "GapSensorimotor": ["Genealogia · 4.2"], "RoboticaEmbodied": ["Genealogia · 4.2"],
    "MetaforeConcettuali": ["Genealogia · 4.2"],
    "HardwareEFondamentaComputazionali": ["Fondamenti · 1", "Fondamenti · 2"],
    "FunzioneBooleana": ["Fondamenti · 1"], "TavolaVerita": ["Fondamenti · 1"],
    "Transistor": ["Fondamenti · 1", "Fondamenti · 2"], "GateLogico": ["Fondamenti · 2"],
    "HardwareSoftware": ["Fondamenti · 2"],
    "AddestramentoEScala": ["Meccanismo · 6.1", "Meccanismo · 6.4", "Meccanismo · 6.5", "Meccanismo · 6.6"],
    "ModelloDiBase": ["Meccanismo · 6.4"], "FineTuning": ["Meccanismo · 6.4"], "Rlhf": ["Meccanismo · 6.5"],
    "ModelloDiRicompensa": ["Meccanismo · 6.5"],
    "Quantizzazione": ["Meccanismo · 4.4", "Meccanismo · 6.6"], "ParametriScala": ["Meccanismo · 6.1"],
    "RiflessioniEpistemologicheTrasversali": ["Meccanismo · 6.3"], "VeritasFiliaTemporis": ["Meccanismo · 6.3"],
}

# ---------------------------------------------------------------------------
# Teorici. name -> (slug, commento/ruolo nel corso, fonte[list codici],
# citaOpera-o-None). citaOpera valorizzato SOLO quando la fonte dà esplicitamente
# un titolo/venue, mai integrato con conoscenza generale esterna al corpus (vedi
# decisioni-modellazione.md, Fase 4 #3). Codici fonte aggiornati alla nuova
# numerazione il 4 settembre 2026. Peirce, Post e Shatz aggiunti in questo
# aggiornamento (prima Peirce era solo un'intestazione — caso dubbio escluso in
# Fase 2 — mai contenuto reale; Post e Shatz non esistevano affatto nell'estrazione
# originale): nessuna relazione teorizzatoDa forzata per i tre, il testo non la
# sostiene esplicitamente oltre alla menzione — vedi decisioni-modellazione.md.
# ---------------------------------------------------------------------------

TEORICI = [
    ("Leibniz", "Gottfried Leibniz", "Characteristica Universalis, il sogno del pensiero come calcolo; anche calcolo infinitesimale (con Newton).", ["Genealogia · 1.1", "Meccanismo · 3.2"], None),
    ("Newton", "Isaac Newton", "Calcolo infinitesimale (con Leibniz); spazio come contenitore assoluto.", ["Meccanismo · 3.2", "Genealogia · 4.1"], None),
    ("Boole", "George Boole", "Algebra della logica; origine degli operatori E/O/NON.", ["Genealogia · 1.1", "Fondamenti · 1"], "The Laws of Thought, 1854"),
    ("Frege", "Gottlob Frege", "Riduzione dell'aritmetica alla logica; distinzione senso/riferimento.", ["Genealogia · 1.1", "Genealogia · 3.1"], None),
    ("Russell", "Bertrand Russell", "Paradosso che incrina i Grundgesetze di Frege; Principia Mathematica con Whitehead.", ["Genealogia · 1.1"], "Principia Mathematica (con Alfred North Whitehead)"),
    ("Whitehead", "Alfred North Whitehead", "Co-autore di Principia Mathematica.", ["Genealogia · 1.1"], "Principia Mathematica (con Bertrand Russell)"),
    ("Godel", "Kurt Gödel", "Teoremi di incompletezza (1931); aritmetizzazione.", ["Genealogia · 1.2", "Meccanismo · 1.5"], None),
    ("Turing", "Alan Turing", "Macchina universale; Test di Turing; risponde all'obiezione gödeliana.", ["Genealogia · 1.2"], None),
    ("Lucas", "J.R. Lucas", "Riformula l'obiezione gödeliana contro il meccanicismo (1961).", ["Genealogia · 1.2"], None),
    ("Penrose", "Roger Penrose", "Riprende l'argomento di Lucas, collegandolo alla coscienza.", ["Genealogia · 1.2"], None),
    ("McCarthy", "John McCarthy", "Conia \"intelligenza artificiale\"; proposta di Dartmouth (1956).", ["Genealogia · 1.3"], None),
    ("Minsky", "Marvin Minsky", "Dartmouth; Perceptrons (con Papert, 1969) — dimostra il limite di XOR.", ["Genealogia · 1.3"], "Perceptrons, 1969 (con Seymour Papert)"),
    ("Shannon", "Claude Shannon", "Co-firmatario della proposta di Dartmouth.", ["Genealogia · 1.3"], None),
    ("Rochester", "Nathaniel Rochester", "Co-firmatario della proposta di Dartmouth.", ["Genealogia · 1.3"], None),
    ("Rosenblatt", "Frank Rosenblatt", "Costruisce il Perceptron (1958).", ["Genealogia · 1.3", "Meccanismo · 4.2"], None),
    ("Papert", "Seymour Papert", "Perceptrons con Minsky (1969).", ["Genealogia · 1.3"], "Perceptrons, 1969 (con Marvin Minsky)"),
    ("Rumelhart", "David Rumelhart", "Articolo del 1986 sul backpropagation (con Hinton e Williams).", ["Genealogia · 1.5"], None),
    ("Hinton", "Geoffrey Hinton", "Backpropagation (1986); deep learning (2006, con Osindero e Teh).", ["Genealogia · 1.5"], None),
    ("Williams", "Ronald Williams", "Articolo del 1986 sul backpropagation.", ["Genealogia · 1.5"], None),
    ("Osindero", "Simon Osindero", "Co-autore con Hinton del metodo 2006 per reti profonde.", ["Genealogia · 1.5"], None),
    ("Teh", "Yee-Whye Teh", "Co-autore con Hinton del metodo 2006 per reti profonde.", ["Genealogia · 1.5"], None),
    ("Mikolov", "Tomas Mikolov", "Guida il gruppo che pubblica Word2Vec (2013).", ["Genealogia · 1.5", "Meccanismo · 3.3"], None),
    ("Bahdanau", "Dzmitry Bahdanau", "Introduce il meccanismo di attention nella traduzione automatica (2014-2015).", ["Genealogia · 1.6"], None),
    ("VonNeumann", "John von Neumann", "The Computer and the Brain (1958); momento di consapevolezza della discretizzazione.", ["Meccanismo · 1.1", "Meccanismo · 6.3", "Meccanismo · 4.2"], "The Computer and the Brain, 1958"),
    ("Cantor", "Georg Cantor", "Argomento diagonale: i numeri reali non sono numerabili.", ["Meccanismo · 1.5", "Meccanismo · 3.1"], None),
    ("Vapnik", "Vladimir Vapnik", "Formalizza le Support Vector Machines.", ["Genealogia · 1.4"], None),
    ("Chomsky", "Noam Chomsky", "Critica ai modelli \"a stati finiti\" del linguaggio (anni '50).", ["Meccanismo · 2.4"], None),
    ("Firth", "John Rupert Firth", "Ipotesi distribuzionale: \"si conosce una parola dalla compagnia che tiene\" (1957).", ["Meccanismo · 3.3"], None),
    ("Wittgenstein", "Ludwig Wittgenstein (tardo)", "Significato come uso, giochi linguistici.", ["Genealogia · 3.1", "Meccanismo · 3.3"], None),
    ("Bateson", "Gregory Bateson", "Sillogismo dell'erba; pleroma/creatura; schismogenesi.", ["Meccanismo · 3.4", "Meccanismo · 4.3", "Meccanismo · 4.5"], "Naven, 1936"),
    ("Varela", "Francisco Varela", "Autopoiesi e chiusura operazionale (con Maturana).", ["Meccanismo · 4.1"], None),
    ("Maturana", "Humberto Maturana", "Autopoiesi (con Varela).", ["Meccanismo · 4.1"], None),
    ("McCulloch", "Warren McCulloch", "Primo modello matematico del neurone (1943, con Pitts); neurofisiologo.", ["Genealogia · 3.3", "Meccanismo · 4.1"], None),
    ("Pitts", "Walter Pitts", "Primo modello matematico del neurone (1943, con McCulloch); logico.", ["Genealogia · 3.3", "Meccanismo · 4.1"], None),
    ("Hebb", "Donald Hebb", "Regola di rinforzo delle connessioni (1949), nella sua forma originale tecnica — non lo slogan con cui è oggi ricordato (vedi Shatz).", ["Genealogia · 3.3", "Meccanismo · 4.1"], None),
    ("Hubel", "David Hubel", "Organizzazione gerarchica della corteccia visiva (con Wiesel).", ["Genealogia · 3.3"], None),
    ("Wiesel", "Torsten Wiesel", "Organizzazione gerarchica della corteccia visiva (con Hubel).", ["Genealogia · 3.3"], None),
    ("Harnad", "Stevan Harnad", "Symbol grounding problem (1990).", ["Genealogia · 2.3", "Genealogia · 3.1"], None),
    ("Pearl", "Judea Pearl", "Scala causale: associazione, intervento, controfattuale.", ["Genealogia · 2.3", "Genealogia · 3.2"], None),
    ("Hume", "David Hume", "La causalità come inferenza abituale, non percezione diretta.", ["Genealogia · 3.2"], None),
    ("Searle", "John Searle", "Esperimento mentale della stanza cinese (1980).", ["Genealogia · 3.1"], None),
    ("Chalmers", "David Chalmers", "Problema facile / problema difficile della coscienza (1995).", ["Genealogia · 3.4"], None),
    ("Tononi", "Giulio Tononi", "Integrated Information Theory (Φ).", ["Genealogia · 3.4"], None),
    ("Baars", "Bernard Baars", "Global Workspace Theory.", ["Genealogia · 3.4"], None),
    ("Dehaene", "Stanislas Dehaene", "Sviluppo della Global Workspace Theory.", ["Genealogia · 3.4"], None),
    ("Kant", "Immanuel Kant", "Spazio come forma dell'intuizione.", ["Genealogia · 4.1"], None),
    ("MerleauPonty", "Maurice Merleau-Ponty", "Spazio vissuto attraverso il corpo.", ["Genealogia · 4.1"], None),
    ("Brooks", "Rodney Brooks", "Robotica embodied: l'intelligenza richiede corpi, non solo simboli.", ["Genealogia · 4.2"], None),
    ("Lakoff", "George Lakoff", "Metafore concettuali a origine sensomotoria (con Johnson).", ["Genealogia · 4.2"], None),
    ("Johnson", "Mark Johnson", "Metafore concettuali a origine sensomotoria (con Lakoff).", ["Genealogia · 4.2"], None),
    ("GalileoGalilei", "Galileo Galilei", "Qualità primarie/secondarie; fondazione della scienza quantificabile.", ["Meccanismo · 3.2", "Meccanismo · 5.4"], None),
    ("Wigner", "Eugene Wigner", "\"Irragionevole efficacia della matematica\".", ["Meccanismo · 3.4"], None),
    ("WeiEtAl2022", "Wei et al. (2022)", "Conia il termine \"capacità emergenti\".", ["Genealogia · 2.1", "Meccanismo · 6.2"], "TMLR, 2022, arXiv:2206.07682"),
    ("SchaefferEtAl2023", "Schaeffer, Miranda, Koyejo (2023)", "Controargomento: l'emergenza può essere artefatto delle metriche.", ["Genealogia · 2.1", "Meccanismo · 6.2"], None),
    ("HerculanoHouzel", "Suzana Herculano-Houzel", "Stima di ~86 miliardi di neuroni nel cervello umano (2009).", ["Meccanismo · 6.1"], "Frontiers in Human Neuroscience, 2009"),
    ("BrownEtAl2020", "Brown et al. (2020)", "Paper GPT-3, citato per gli ordini di grandezza dei parametri.", ["Meccanismo · 6.1"], None),
    ("ChowdheryEtAl2022", "Chowdhery et al. (2022)", "Paper PaLM (Google), citato per gli ordini di grandezza.", ["Meccanismo · 6.1"], None),
    ("OuyangEtAl2022", "Ouyang et al. (2022)", "Introduce il fine-tuning verso il comportamento istruito.", ["Meccanismo · 6.4"], "InstructGPT, 2022"),
    ("Bacon", "Francis Bacon", "\"Veritas filia temporis\" — la verità è figlia del tempo.", ["Meccanismo · 6.3"], "Veritas filia temporis"),
    ("Bayle", "Pierre Bayle", "Contro-tesi \"error filius temporis\".", ["Meccanismo · 6.3"], "Error filius temporis"),
    ("Lawvere", "William Lawvere", "Geometria differenziale sintetica: il continuo come primitivo.", ["Meccanismo · 6.6"], None),
    # --- Aggiunti il 4 settembre 2026 ---
    ("Peirce", "Charles Sanders Peirce", "Abbozza una versione della tavola di verità già tra il 1883 e il 1902, in manoscritti rimasti inediti per decenni.", ["Fondamenti · 1"], None),
    ("Post", "Emil Post", "Usa la tavola di verità (1921, indipendentemente da Wittgenstein) per dimostrare che E, O e NON bastano a costruire qualsiasi funzione booleana.", ["Fondamenti · 1"], None),
    ("Shatz", "Carla Shatz", "Conia decenni dopo lo slogan «neurons that fire together, wire together», spesso attribuito per errore direttamente a Hebb (1949) — nessuna data/opera specifica data dal testo.", ["Genealogia · 3.3"], None),
]

# ---------------------------------------------------------------------------
# Dataset/Asset. slug -> (label, descrizione, stato ["Reale"|"Illustrativo"],
# dataVerifica-o-None). Data di verifica 2026-07-06 quando qa-tool/decision-log.md
# la documenta esplicitamente per quella sessione; altrimenti None (nessuna data
# inventata) — vedi decisioni-modellazione.md, Fase 4 #4.
# ---------------------------------------------------------------------------

DATASET = [
    ("VocabolarioBpeDelCorso", "Vocabolario BPE del corso", "334 simboli (34 caratteri base + 300 unioni apprese), addestrato realmente sul testo di Genealogia.", "Reale", "2026-07-06"),
    ("Corpus46FrasiItaliane", "Corpus di 46 frasi italiane", "Corpus scritto apposta per il predittore n-grammi (34 training, 12 test).", "Reale", "2026-07-06"),
    ("DatiCalibrazioneReliability", "Dati di calibrazione (reliability diagram)", "65 previsioni reali raggruppate in 3 bucket di confidenza, misurate sul corpus di 46 frasi.", "Reale", "2026-07-06"),
    ("EmbeddingFastTextIt23Parole", "Embedding fastText di 23 parole italiane", "Vettori reali a 300 dimensioni, proiettati in 2D per esplorazione, aritmetica e polisemia.", "Reale", "2026-07-06"),
    ("DiagonaleCantorInterattiva", "Diagonale di Cantor interattiva", "Griglia di cifre con costruzione del numero che sfugge a qualunque lista.", "Reale", "2026-07-06"),
    ("ReteXorAddestrata", "Rete XOR addestrata realmente", "Multi-layer perceptron addestrato via backpropagation, 4/4 corretto, confine di decisione curvo.", "Reale", "2026-07-06"),
    ("PaesaggioPerditaDueMinimi", "Paesaggio di perdita a due minimi", "Superficie di loss (due gaussiane invertite) con minimo globale e locale; discesa del gradiente verificata numericamente. Costruita (non misurata da un modello reale), ma verificata: \"reale\" qui significa verificato algoritmicamente, non proveniente da un training di produzione — nota esplicita per non confondere le due cose.", "Reale", "2026-07-06"),
    ("EsempiNeuroneSingolo", "Esempi di neurone singolo", "Pesi/ingressi regolabili a slider, variante continua del calcolatore booleano. Nessun addestramento o verifica: calcolatore dal vivo.", "Illustrativo", None),
    ("DatiAttentionIllustrativi", "Dati di attention illustrativi", "Pesi scritti a mano per chiarezza pedagogica — esplicitamente non output di un vero Transformer.", "Illustrativo", None),
    ("ConfrontoBaseFineTuned", "Confronto modello di base / fine-tuned", "Prompt/risposta scritti per illustrare l'effetto di fine-tuning e RLHF, non output di un modello reale.", "Illustrativo", None),
    ("CurvaCapacitaEmergentiIllustrativa", "Curva illustrativa delle capacità emergenti", "Andamento piatto-poi-salto per un compito tipo, dichiarato esplicitamente non misurato da un paper specifico.", "Illustrativo", None),
    ("SliderScalaLogaritmica", "Slider di scala logaritmica", "Confronto parametri/dati (GPT-3, PaLM) con il cervello umano, su numeri reali verificati.", "Reale", "2026-07-06"),
    ("TimelineAlfabetoCorporaLlm", "Timeline storica alfabeto→corpora LLM", "Alfabeto, von Neumann 1958, digitalizzazione di massa, corpora di addestramento — date verificate.", "Reale", "2026-07-06"),
    ("LivelliQuantizzazione", "Livelli di quantizzazione", "FP32→FP16/BF16→INT8→INT4, con riferimento a strumenti reali (llama.cpp).", "Reale", "2026-07-06"),
    ("ConfrontoRasterSvg", "Confronto raster/SVG", "Cerchio raster 24×24px generato via Pillow e suo equivalente SVG, stessi colori del design system.", "Reale", "2026-07-06"),
    ("CalcolatoreBooleanoInterattivo", "Calcolatore booleano interattivo", "Interruttori A/B che mostrano dal vivo E, O, NON, XOR e F = (A∧B)∨¬A.", "Reale", None),
]

# ---------------------------------------------------------------------------
# Relazioni fra Concetti (object properties già definite in ontologia.ttl).
# Invariate dalla Fase 4 originale: riferiscono slug di Concetto, non codici
# unità — non toccate dalla rinumerazione. Ogni tripla qui è una decisione di
# mappatura presa a mano dalle ~38 relazioni osservate in Fase 1 — non tutte sono
# state mappate: quelle il cui target non corrisponde a un nodo esistente (es.
# "GPU", "Immagine raster" come concetti a sé) sono elencate come gap dichiarati
# in docs/decisioni-modellazione.md, non forzate qui con un nodo inventato.
# ---------------------------------------------------------------------------

RELAZIONI_CONCETTO = [
    ("Tokenizzazione", "prerequisitoDi", "Embedding"),
    ("Numerabilita", "contrappostoA", "Embedding"),
    ("Sparsita", "spiegataDa", "TokenId"),
    ("MultiLayerPerceptron", "risolve", "SeparabilitaLineare"),
    ("Backpropagation", "prerequisitoDi", "DiscesaDelGradiente"),
    ("Attention", "risolve", "DipendenzeLungoRaggio"),
    ("Attention", "risolve", "EmbeddingStatico"),
    ("Attention", "risolve", "Polisemia"),
    ("Softmax", "analogoA", "ProbabilitaComeNumeroReale"),
    ("AritmeticaVettoriale", "esemplifica", "Abduzione"),
    ("AritmeticaVettoriale", "esemplifica", "SillogismoDellErba"),
    ("Ngramma", "esemplifica", "Induzione"),
    ("EmbeddingContestuale", "contrappostoA", "EmbeddingStatico"),
    ("QualitaPrimarieSecondarie", "analogoA", "EmbeddingContestuale"),
    ("Embedding", "rendeOperativo", "QualitaPrimarieSecondarie"),
    ("IpotesiDistribuzionale", "rendeOperativo", "SignificatoComeUso"),
    ("Grounding", "collegatoA", "GapSensorimotor"),
    ("Backpropagation", "contrappostoA", "Schismogenesi"),
    ("Backpropagation", "contrappostoA", "PlasticitaSinaptica"),
    ("DiagonaleDiCantor", "prerequisitoDi", "Numerabilita"),
    ("SistemaFormale", "prerequisitoDi", "TeoremaIncompletezzaGodel"),
    ("StanzaCinese", "esemplifica", "Grounding"),
    ("ModelloDiBase", "prerequisitoDi", "FineTuning"),
    ("FineTuning", "prerequisitoDi", "Rlhf"),
    ("Quantizzazione", "contrappostoA", "DiscesaDelGradiente"),
    ("Word2Vec", "esemplifica", "CapacitaEmergenti"),
]

RELAZIONI_TEORICO = [
    # (concetto, teorico) -> teorizzatoDa
    ("TeoremaIncompletezzaGodel", "Godel"), ("TestDiTuring", "Turing"),
    ("Autopoiesi", "Varela"), ("Autopoiesi", "Maturana"), ("ChiusuraOperazionale", "Varela"),
    ("PleromaCreatura", "Bateson"), ("SillogismoDellErba", "Bateson"), ("Schismogenesi", "Bateson"),
    ("QualitaPrimarieSecondarie", "GalileoGalilei"),
    ("IpotesiDistribuzionale", "Firth"), ("SignificatoComeUso", "Wittgenstein"),
    ("StanzaCinese", "Searle"), ("Grounding", "Harnad"), ("RagionamentoCausale", "Pearl"),
    ("ProblemaDifficileCoscienza", "Chalmers"), ("IntegratedInformationTheory", "Tononi"),
    ("GlobalWorkspaceTheory", "Baars"), ("GlobalWorkspaceTheory", "Dehaene"),
    ("SpazioFormaIntuizione", "Kant"), ("SpazioVissuto", "MerleauPonty"),
    ("SpazioContenitoreAssoluto", "Newton"), ("RoboticaEmbodied", "Brooks"),
    ("MetaforeConcettuali", "Lakoff"), ("MetaforeConcettuali", "Johnson"),
    ("IrragionevoleEfficaciaMatematica", "Wigner"), ("CapacitaEmergenti", "WeiEtAl2022"),
    ("Word2Vec", "Mikolov"), ("Attention", "Bahdanau"), ("FunzioneBooleana", "Boole"),
    ("Backpropagation", "Rumelhart"), ("Backpropagation", "Hinton"), ("Backpropagation", "Williams"),
    ("DeepLearning", "Hinton"), ("DeepLearning", "Osindero"), ("DeepLearning", "Teh"),
    ("SupportVectorMachine", "Vapnik"), ("FineTuning", "OuyangEtAl2022"),
    ("VeritasFiliaTemporis", "Bacon"), ("VeritasFiliaTemporis", "Bayle"),
    ("ParametriScala", "BrownEtAl2020"), ("ParametriScala", "ChowdheryEtAl2022"),
    ("DiagonaleDiCantor", "Cantor"), ("Discretizzazione", "VonNeumann"),
    ("SeparabilitaLineare", "Minsky"), ("SeparabilitaLineare", "Papert"),
    ("NeuroneArtificiale", "McCulloch"), ("NeuroneArtificiale", "Pitts"),
]

MESSO_IN_DISCUSSIONE = [
    ("CapacitaEmergenti", "SchaefferEtAl2023"),
]

RIPRENDE_ARGOMENTAZIONE = [
    ("Lucas", "Turing"),
    ("Penrose", "Lucas"),
]

# Rimandi narrativi Unità -> Unità. Remappati dai vecchi slug (UA2, UB1, UC1...)
# ai nuovi (Gen12, Gen21, Gen31...) secondo la tabella del piano — stesse coppie
# concettuali di prima, stessi target Meccanismo (U15, U42, U45) invariati.
RIMANDA_A = [
    ("Gen12", "U15"), ("Gen13", "U42"), ("Gen15", "U45"),
    ("Gen21", "Gen31"), ("Gen23", "Gen32"), ("Gen23", "Gen34"),
    ("Gen31", "Gen42"),
]


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main():
    out = []
    out.append(f'@prefix : <{NS}> .')
    out.append('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .')
    out.append('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .')
    out.append('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .')
    out.append('')
    out.append('# Popolamento (ABox) — Fase 4, aggiornato il 4 settembre 2026. Generato da')
    out.append('# scripts/genera_dati.py da dati strutturati scritti a mano nello script stesso;')
    out.append('# non modificare a mano questo file, rigenerarlo dallo script. Vedi')
    out.append('# docs/decisioni-modellazione.md per il razionale delle scelte di mappatura.')
    out.append('')

    out.append('#' * 72)
    out.append('# Parti')
    out.append('#' * 72)
    out.append('')
    for parte_slug, parte_label in PARTI.items():
        out.append(f':{parte_slug} a :Parte ;')
        out.append(f'    rdfs:label "{esc(parte_label)}"@it .')
        out.append('')

    out.append('#' * 72)
    out.append('# Capitoli e Unità')
    out.append('#' * 72)
    out.append('')
    for cap_slug, (cap_num, cap_title, parte_slug, unita) in CAPITOLI.items():
        parte_label = PARTI[parte_slug]
        out.append(f':{cap_slug} a :Capitolo ;')
        out.append(f'    rdfs:label "{esc(parte_label)} · {esc(cap_num)} — {esc(cap_title)}"@it ;')
        out.append(f'    :partOfParte :{parte_slug} .')
        out.append('')
        if unita:
            for u_slug, u_code, u_title in unita:
                out.append(f':{u_slug} a :Unita ;')
                out.append(f'    rdfs:label "{esc(parte_label)} · {esc(u_code)} — {esc(u_title)}"@it ;')
                out.append(f'    :partOfCapitolo :{cap_slug} .')
                out.append('')

    out.append('#' * 72)
    out.append('# discussoInUnita — Concetto -> Unita/Capitolo, da :fonte già scritto in Fase 2')
    out.append('#' * 72)
    out.append('')
    for concetto, codici in FONTE_ESPANSA.items():
        slugs = [CODE_TO_SLUG[c] for c in codici if c in CODE_TO_SLUG]
        mancanti = [c for c in codici if c not in CODE_TO_SLUG]
        if mancanti:
            out.append(f'# ATTENZIONE: codici non risolti per {concetto}: {mancanti}')
        if slugs:
            targets = ', '.join(f':{s}' for s in slugs)
            out.append(f':{concetto} :discussoInUnita {targets} .')
    out.append('')

    out.append('#' * 72)
    out.append('# Teorici')
    out.append('#' * 72)
    out.append('')
    for slug, nome, ruolo, codici, opera in TEORICI:
        slugs = [CODE_TO_SLUG[c] for c in codici if c in CODE_TO_SLUG]
        out.append(f':{slug} a :Teorico ;')
        out.append(f'    rdfs:label "{esc(nome)}"@it ;')
        out.append(f'    rdfs:comment "{esc(ruolo)}"@it ;')
        if slugs:
            targets = ', '.join(f':{s}' for s in slugs)
            out.append(f'    :discussoInUnita {targets} ;')
        if opera:
            out.append(f'    :citaOpera "{esc(opera)}" ;')
        out[-1] = out[-1].rstrip(' ;') + ' .'
        out.append('')

    out.append('#' * 72)
    out.append('# Dataset')
    out.append('#' * 72)
    out.append('')
    for slug, label, desc, stato, data in DATASET:
        out.append(f':{slug} a :Dataset ;')
        out.append(f'    rdfs:label "{esc(label)}"@it ;')
        out.append(f'    rdfs:comment "{esc(desc)}"@it ;')
        out.append(f'    :haStatoEpistemico :{stato} ;')
        if data:
            out.append(f'    :dataVerifica "{data}"^^xsd:date ;')
        out[-1] = out[-1].rstrip(' ;') + ' .'
        out.append('')

    out.append('#' * 72)
    out.append('# Relazioni fra Concetti')
    out.append('#' * 72)
    out.append('')
    for s, p, o in RELAZIONI_CONCETTO:
        out.append(f':{s} :{p} :{o} .')
    out.append('')

    out.append('#' * 72)
    out.append('# Relazioni Concetto -> Teorico')
    out.append('#' * 72)
    out.append('')
    for c, t in RELAZIONI_TEORICO:
        out.append(f':{c} :teorizzatoDa :{t} .')
    out.append('')
    for c, t in MESSO_IN_DISCUSSIONE:
        out.append(f':{c} :messoInDiscussioneDa :{t} .')
    out.append('')

    out.append('#' * 72)
    out.append('# Relazioni Teorico -> Teorico')
    out.append('#' * 72)
    out.append('')
    for a, b in RIPRENDE_ARGOMENTAZIONE:
        out.append(f':{a} :riprendeArgomentazioneDi :{b} .')
    out.append('')

    out.append('#' * 72)
    out.append('# Relazioni Unita -> Unita (rimandi narrativi)')
    out.append('#' * 72)
    out.append('')
    for a, b in RIMANDA_A:
        out.append(f':{a} :rimandaA :{b} .')
    out.append('')

    print('\n'.join(out))


if __name__ == '__main__':
    main()
