// Lente semantica — grafo radiale D3, un nodo alla volta. Nessun fetch: i dati
// sono già in memoria via grafo.js (caricato prima di questo file). Nessuna
// simulazione a forze: il layout è calcolato a mano, per gruppo di relazione,
// come nel mockup (docs in ../mockup/1c-lente.png) — D3 qui serve per
// selezioni/data-join e per il calcolo degli archi (d3.arc()), non per la
// disposizione dei nodi, che è deliberatamente un ventaglio leggibile, non una
// nuvola a forze.

(function () {
    "use strict";

    const NODI_PER_ID = new Map(GRAFO.nodi.map((n) => [n.id, n]));
    const PROPRIETA = GRAFO.proprieta;

    const COLORE_CATEGORIA = {
        gerarchia: "var(--cat-gerarchia)",
        concettuale: "var(--cat-concettuale)",
        attribuzione: "var(--cat-attribuzione)",
        struttura: "var(--cat-struttura)",
    };
    const TENUE_CATEGORIA = {
        gerarchia: "var(--cat-gerarchia-tenue)",
        concettuale: "var(--cat-concettuale-tenue)",
        attribuzione: "var(--cat-attribuzione-tenue)",
        struttura: "var(--cat-struttura-tenue)",
    };
    const ORDINE_CATEGORIE = ["gerarchia", "concettuale", "attribuzione", "struttura"];
    const NOMI_CATEGORIE = {
        gerarchia: "Gerarchia (broader)",
        concettuale: "Relazioni concettuali",
        attribuzione: "Attribuzione a un Teorico",
        struttura: "Struttura del corpus",
    };

    // Classificazione dei nodi per la sidebar — stesso ordine di priorità di
    // kind() in scripts/genera_html.py (root, sito principale): concetto >
    // teorico > parte > capitolo > unita > dataset > altro. Riusa il campo
    // "tipi" già esportato da genera_grafo.py, non richiede una nuova
    // esportazione dai .ttl.
    function gruppoDi(nodo) {
        const t = nodo.tipi;
        if (t.includes("Concetto")) return "Concetto";
        if (t.includes("Teorico")) return "Teorico";
        if (t.includes("Parte")) return "Parte";
        if (t.includes("Capitolo")) return "Capitolo";
        if (t.includes("Unità")) return "Unità";
        if (t.includes("Dataset")) return "Dataset";
        return "Altro"; // FiloTrasversale, StatoEpistemico, e nodi senza tipo
    }
    const COLORE_GRUPPO = {
        Concetto: "var(--grp-concetto)",
        Teorico: "var(--grp-teorico)",
        Unità: "var(--grp-unita)",
        Dataset: "var(--grp-dataset)",
        Capitolo: "var(--grp-capitolo)",
        Parte: "var(--grp-parte)",
        Altro: "var(--grp-altro)",
    };
    // Ordine di visualizzazione dei 7 gruppi: per conteggio decrescente, con
    // "Altro" sempre in fondo indipendentemente dal conteggio. Calcolato una
    // sola volta sull'intero dataset, non ad ogni render della sidebar.
    const ORDINE_GRUPPI = (() => {
        const conteggio = new Map();
        for (const n of GRAFO.nodi) {
            const g = gruppoDi(n);
            conteggio.set(g, (conteggio.get(g) || 0) + 1);
        }
        return Array.from(conteggio.keys()).sort((a, b) => {
            if (a === "Altro") return 1;
            if (b === "Altro") return -1;
            return conteggio.get(b) - conteggio.get(a);
        });
    })();
    const nodoMaxGrado = GRAFO.nodi.reduce((max, n) => (n.grado > max.grado ? n : max), GRAFO.nodi[0]);

    // Indice di adiacenza: per ogni id, la lista di {altro, prop, uscente}.
    const ADIACENZA = new Map();
    function aggiungiAdiacenza(id, voce) {
        if (!ADIACENZA.has(id)) ADIACENZA.set(id, []);
        ADIACENZA.get(id).push(voce);
    }
    for (const a of GRAFO.archi) {
        aggiungiAdiacenza(a.da, { altro: a.a, prop: a.prop, uscente: true });
        aggiungiAdiacenza(a.a, { altro: a.da, prop: a.prop, uscente: false });
    }

    function viciniDi(id) {
        return ADIACENZA.get(id) || [];
    }

    function etichettaRelazione(prop, uscente) {
        const meta = PROPRIETA[prop];
        if (!meta) return prop;
        return uscente ? meta.diretta : meta.inversa;
    }

    function categoriaDi(prop) {
        const meta = PROPRIETA[prop];
        return meta ? meta.categoria : "struttura";
    }

    function tronca(s, n) {
        return s.length > n ? s.slice(0, n - 1) + "…" : s;
    }

    // ------------------------------------------------------------------
    // Sidebar — tendina a due livelli: gruppo di tipo (per conteggio
    // decrescente, "Altro" in fondo), poi dentro ciascuno nodi in ordine
    // alfabetico. Ricostruita per intero ad ogni chiamata (258 nodi in
    // totale: costo trascurabile, nessuna strategia di diffing necessaria).
    // ------------------------------------------------------------------

    const listaNodi = document.getElementById("lista-nodi");
    const campoRicerca = document.getElementById("ricerca");
    let centroCorrente = null;
    let grado2Attivo = false;

    campoRicerca.placeholder = `Cerca fra ${GRAFO.nodi.length} nodi…`;

    function renderSidebar(filtro) {
        const f = (filtro || "").trim().toLowerCase();
        const perGruppo = new Map(ORDINE_GRUPPI.map((g) => [g, []]));
        for (const n of GRAFO.nodi) {
            if (f && !n.label.toLowerCase().includes(f)) continue;
            perGruppo.get(gruppoDi(n)).push(n);
        }
        for (const lista of perGruppo.values()) {
            lista.sort((a, b) => a.label.localeCompare(b.label, "it"));
        }

        const gruppoAttivo = centroCorrente ? gruppoDi(NODI_PER_ID.get(centroCorrente)) : null;
        listaNodi.innerHTML = "";

        for (const g of ORDINE_GRUPPI) {
            const nodiGruppo = perGruppo.get(g);
            if (f && nodiGruppo.length === 0) continue; // niente risultati: nascondi il gruppo intero

            const det = document.createElement("details");
            det.className = "gruppo-nodi";
            det.dataset.gruppo = g;
            det.style.setProperty("--colore-gruppo", COLORE_GRUPPO[g]);
            det.open = f ? true : g === gruppoAttivo;

            const summary = document.createElement("summary");
            const pallino = document.createElement("span");
            pallino.className = "pallino";
            pallino.style.background = COLORE_GRUPPO[g];
            const nome = document.createElement("span");
            nome.className = "nome-gruppo";
            nome.textContent = g;
            const conteggio = document.createElement("span");
            conteggio.className = "conteggio-gruppo";
            conteggio.textContent = nodiGruppo.length;
            summary.append(pallino, nome, conteggio);
            det.appendChild(summary);

            const ul = document.createElement("ul");
            ul.className = "lista-nodi";
            for (const n of nodiGruppo) {
                const li = document.createElement("li");
                li.dataset.id = n.id;
                if (n.id === centroCorrente) li.classList.add("selezionato");
                const nomeNodo = document.createElement("span");
                nomeNodo.className = "nome";
                nomeNodo.textContent = n.label;
                const grado = document.createElement("span");
                grado.className = "grado";
                grado.textContent = n.grado;
                li.append(nomeNodo, grado);
                li.addEventListener("click", () => selezionaNodo(n.id));
                ul.appendChild(li);
            }
            det.appendChild(ul);
            listaNodi.appendChild(det);
        }
    }

    campoRicerca.addEventListener("input", () => renderSidebar(campoRicerca.value));

    // ------------------------------------------------------------------
    // Breadcrumb
    // ------------------------------------------------------------------

    function renderBreadcrumb(id) {
        const nodo = NODI_PER_ID.get(id);
        const el = document.getElementById("breadcrumb-nodo");
        const vicini = viciniDi(id);
        const genitore = vicini.find((v) => v.prop === "broader" && v.uscente);
        let html = "";
        if (genitore) {
            const g = NODI_PER_ID.get(genitore.altro);
            html += `<a href="#${g.id}" class="rimando-genitore">${g.label}</a><span class="sep"> › </span>`;
        }
        html += `<strong>${nodo.label}</strong> · ${nodo.tipi.join(" + ")} · <span class="num">${nodo.grado}</span> archi`;
        el.innerHTML = html;
        el.querySelectorAll("a.rimando-genitore").forEach((a) =>
            a.addEventListener("click", (e) => {
                e.preventDefault();
                selezionaNodo(genitore.altro);
            })
        );
    }

    // ------------------------------------------------------------------
    // Grafo radiale
    // ------------------------------------------------------------------

    const svg = d3.select("#svg-grafo");
    const CX = 440, CY = 440;
    const R_ARCO = 95, R_NODO = 195, R_TESTO = 205, R_NODO2 = 235;
    const GAP = 0.045; // radianti fra un gruppo di relazione e il successivo

    // Etichetta col tipo di relazione + nodo di destinazione: non più un
    // testo permanente sull'arco (si sovrapponeva sempre a una linea guida
    // quando il gruppo ha un numero dispari di voci — succede per
    // costruzione, non un caso raro) ma un'unica pillola fissa in alto a
    // destra, che appare solo al passaggio del mouse su un satellite.
    const badgeRelazione = document.getElementById("badge-relazione");
    function mostraBadgeRelazione(g, altro) {
        badgeRelazione.textContent = `${g.prop} · ${tronca(altro.label, 30)}`;
        badgeRelazione.style.background = COLORE_CATEGORIA[g.categoria];
        badgeRelazione.classList.add("visibile");
    }
    function nascondiBadgeRelazione() {
        badgeRelazione.classList.remove("visibile");
    }

    function costruisciGruppi(id) {
        const vicini = viciniDi(id);
        const chiavi = new Map(); // "prop|uscente" -> {prop, uscente, categoria, voci:[]}
        for (const v of vicini) {
            const chiave = v.prop + "|" + v.uscente;
            if (!chiavi.has(chiave)) {
                chiavi.set(chiave, { prop: v.prop, uscente: v.uscente, categoria: categoriaDi(v.prop), voci: [] });
            }
            chiavi.get(chiave).voci.push(v.altro);
        }
        const gruppi = Array.from(chiavi.values());
        gruppi.sort((a, b) => {
            const ca = ORDINE_CATEGORIE.indexOf(a.categoria), cb = ORDINE_CATEGORIE.indexOf(b.categoria);
            if (ca !== cb) return ca - cb;
            if (a.prop !== b.prop) return a.prop.localeCompare(b.prop);
            return a.uscente === b.uscente ? 0 : a.uscente ? -1 : 1;
        });
        return gruppi;
    }

    function renderGrafo(id) {
        svg.selectAll("*").remove();
        const nodo = NODI_PER_ID.get(id);
        const gruppi = costruisciGruppi(id);
        const totale = gruppi.reduce((s, g) => s + g.voci.length, 0);
        if (totale === 0) {
            svg.append("text").attr("x", CX).attr("y", CY).attr("text-anchor", "middle")
                .text(`«${nodo.label}» non ha vicini nel grafo.`);
            return;
        }

        const gapTotale = GAP * gruppi.length;
        const angoloPerVoce = (2 * Math.PI - gapTotale) / totale;
        let angolo = -Math.PI / 2;

        const arcoGen = d3.arc().innerRadius(R_ARCO - 4).outerRadius(R_ARCO + 4);
        const layer2 = svg.append("g").attr("class", "livello-2");
        const layerArchi = svg.append("g");
        const layerSatelliti = svg.append("g");

        for (const g of gruppi) {
            const spanGruppo = angoloPerVoce * g.voci.length;
            const a0 = angolo, a1 = angolo + spanGruppo;

            // d3.arc() misura gli angoli da ore 12 in senso orario; il resto
            // del codice (satelliti, linee guida) usa Math.cos/sin, che
            // misura da ore 3 — da qui la correzione di +90° (Math.PI/2)
            // solo qui, dove serve tradurre verso la convenzione di d3.
            const arco = layerArchi.append("path")
                .attr("class", "arco-categoria")
                .attr("data-cat", g.categoria)
                .attr("d", arcoGen({ startAngle: a0 + Math.PI / 2, endAngle: a1 + Math.PI / 2 }))
                .attr("transform", `translate(${CX},${CY})`)
                .attr("stroke", COLORE_CATEGORIA[g.categoria]);
            arco.append("title").text(`${etichettaRelazione(g.prop, g.uscente)} (${g.voci.length})`);

            g.voci.forEach((altroId, i) => {
                const aNodo = a0 + angoloPerVoce * (i + 0.5);
                const x = CX + R_NODO * Math.cos(aNodo), y = CY + R_NODO * Math.sin(aNodo);
                const xArco = CX + R_ARCO * Math.cos(aNodo), yArco = CY + R_ARCO * Math.sin(aNodo);
                const xTesto = CX + R_TESTO * Math.cos(aNodo), yTesto = CY + R_TESTO * Math.sin(aNodo);
                const altro = NODI_PER_ID.get(altroId);

                layerSatelliti.append("line").attr("class", "linea-guida")
                    .attr("data-cat", g.categoria)
                    .attr("x1", xArco).attr("y1", yArco).attr("x2", x).attr("y2", y)
                    .attr("stroke", COLORE_CATEGORIA[g.categoria]);

                const grp = layerSatelliti.append("g").attr("class", "satellite")
                    .attr("data-cat", g.categoria)
                    .style("cursor", "pointer")
                    .on("click", () => selezionaNodo(altroId))
                    .on("mouseenter", () => mostraBadgeRelazione(g, altro))
                    .on("mouseleave", () => nascondiBadgeRelazione());
                grp.append("title").text(`${altro.label} — ${etichettaRelazione(g.prop, g.uscente)}`);
                grp.append("circle").attr("cx", x).attr("cy", y).attr("r", 5)
                    .attr("fill", TENUE_CATEGORIA[g.categoria]).attr("stroke", COLORE_CATEGORIA[g.categoria]);

                const gradiTesto = (aNodo * 180) / Math.PI;
                const specchiato = gradiTesto > 90 && gradiTesto < 270;
                grp.append("text")
                    .attr("x", xTesto).attr("y", yTesto)
                    .attr("transform", `rotate(${specchiato ? gradiTesto + 180 : gradiTesto}, ${xTesto}, ${yTesto})`)
                    .attr("text-anchor", specchiato ? "end" : "start")
                    .attr("dominant-baseline", "middle")
                    .attr("fill", "var(--inchiostro)")
                    .text(tronca(altro.label, 34));

                if (grado2Attivo) {
                    const viciniAltro = viciniDi(altroId)
                        .filter((v) => v.altro !== id && !g.voci.includes(v.altro))
                        .slice(0, 5);
                    viciniAltro.forEach((v2, j) => {
                        const spread = 0.11;
                        const a2 = aNodo - spread / 2 + (viciniAltro.length > 1 ? (spread * j) / (viciniAltro.length - 1) : spread / 2);
                        const x2 = CX + R_NODO2 * Math.cos(a2), y2 = CY + R_NODO2 * Math.sin(a2);
                        const n2 = NODI_PER_ID.get(v2.altro);
                        const grp2 = layer2.append("g").attr("class", "satellite-2")
                            .style("cursor", "pointer")
                            .on("click", () => selezionaNodo(v2.altro));
                        grp2.append("title").text(`${n2.label} (2° grado, via ${altro.label})`);
                        grp2.append("line").attr("x1", x).attr("y1", y).attr("x2", x2).attr("y2", y2)
                            .attr("stroke", COLORE_CATEGORIA[categoriaDi(v2.prop)]).attr("stroke-width", 0.75).attr("opacity", 0.35);
                        grp2.append("circle").attr("cx", x2).attr("cy", y2).attr("r", 3)
                            .attr("fill", COLORE_CATEGORIA[categoriaDi(v2.prop)]);
                    });
                }
            });

            angolo = a1 + GAP;
        }

        // Niente più testo dentro il cerchio centrale: il nome del nodo è già
        // nel breadcrumb sopra il grafico — ripeterlo qui era ridondante (e
        // per i nomi lunghi, anche troncato in modo brutto).
        const centro = svg.append("g").attr("class", "nodo-centro");
        centro.append("circle").attr("cx", CX).attr("cy", CY).attr("r", 46);
    }

    // ------------------------------------------------------------------
    // Legenda (filtro cliccabile) e glossario delle relazioni
    // ------------------------------------------------------------------

    const categorieAttive = new Set(ORDINE_CATEGORIE);

    function aggiornaFiltroLegenda() {
        const nascoste = ORDINE_CATEGORIE.filter((c) => !categorieAttive.has(c));
        svg.attr("data-nascondi", nascoste.join(" "));
    }

    function renderLegenda() {
        const el = document.getElementById("legenda");
        el.innerHTML = "";
        for (const cat of ORDINE_CATEGORIE) {
            const btn = document.createElement("button");
            btn.type = "button";
            btn.className = "voce";
            btn.setAttribute("aria-pressed", categorieAttive.has(cat) ? "true" : "false");
            btn.innerHTML = `<span class="pallino" style="background:${COLORE_CATEGORIA[cat]}"></span>${NOMI_CATEGORIE[cat]}`;
            btn.addEventListener("click", () => {
                if (categorieAttive.has(cat)) categorieAttive.delete(cat);
                else categorieAttive.add(cat);
                btn.setAttribute("aria-pressed", categorieAttive.has(cat) ? "true" : "false");
                aggiornaFiltroLegenda();
            });
            el.appendChild(btn);
        }
    }

    function renderGlossario() {
        const el = document.getElementById("glossario-relazioni");
        el.innerHTML = "";
        for (const cat of ORDINE_CATEGORIE) {
            const voci = Object.entries(PROPRIETA).filter(([, meta]) => meta.categoria === cat);
            const box = document.createElement("div");
            box.className = "glossario-categoria";
            const h3 = document.createElement("h3");
            h3.innerHTML = `<span class="pallino" style="background:${COLORE_CATEGORIA[cat]}"></span>${NOMI_CATEGORIE[cat]}`;
            box.appendChild(h3);
            const dl = document.createElement("dl");
            for (const [slug, meta] of voci) {
                const dt = document.createElement("dt");
                dt.textContent = slug;
                const dd = document.createElement("dd");
                dd.textContent = `${meta.diretta} / ${meta.inversa}`;
                dl.append(dt, dd);
            }
            box.appendChild(dl);
            el.appendChild(box);
        }
    }

    // ------------------------------------------------------------------
    // Selezione e avvio
    // ------------------------------------------------------------------

    function selezionaNodo(id) {
        if (!NODI_PER_ID.has(id)) return;
        centroCorrente = id;
        location.hash = id;
        renderBreadcrumb(id);
        renderGrafo(id);
        renderSidebar(campoRicerca.value);
        document.querySelectorAll(".lista-nodi li.selezionato").forEach((el) => el.scrollIntoView({ block: "nearest" }));
    }

    document.getElementById("btn-grado-1").addEventListener("click", () => impostaGrado(false));
    document.getElementById("btn-grado-2").addEventListener("click", () => impostaGrado(true));
    function impostaGrado(due) {
        grado2Attivo = due;
        document.getElementById("btn-grado-1").classList.toggle("attivo", !due);
        document.getElementById("btn-grado-2").classList.toggle("attivo", due);
        if (centroCorrente) renderGrafo(centroCorrente);
    }

    window.addEventListener("hashchange", () => {
        const id = decodeURIComponent(location.hash.slice(1));
        if (id && NODI_PER_ID.has(id) && id !== centroCorrente) selezionaNodo(id);
    });

    renderLegenda();
    renderGlossario();
    aggiornaFiltroLegenda();
    const iniziale = decodeURIComponent(location.hash.slice(1));
    const nodoIniziale = NODI_PER_ID.has(iniziale) ? iniziale : nodoMaxGrado.id;
    selezionaNodo(nodoIniziale);
})();
