#!/usr/bin/env node
// cattura.js — cattura gli screenshot dell'harness di regressione visiva.
//
// Uso:
//   node cattura.js --baseline     scrive in baseline/
//   node cattura.js                scrive in attuale/
//   node cattura.js --solo=id1,id2 limita ai bersagli con quegli id (debug)
//
// Avvia da solo un piccolo server statico (Node puro, nessuna dipendenza)
// con radice il repository, su una porta libera scelta dal sistema
// operativo (mai 8777, che e' occupata da altro), lo spegne alla fine.
// Pilota Chrome di sistema via playwright-core (channel:'chrome') — non
// scarica binari di browser.
//
// Vedi README.md per i requisiti di determinismo e perche' esistono le
// scelte qui sotto (congelamento CSS, stub di setInterval, attesa di
// assestamento per il widget canvas di meccanismo-4).

import { chromium } from 'playwright-core';
import http from 'node:http';
import fs from 'node:fs';
import fsp from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { bersagli, VIEWPORTS } from './bersagli.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(__dirname, '..', '..'); // verify -> design-system -> radice repo

// Raccolto durante la cattura, scritto a fine esecuzione (vedi README).
const ANIMAZIONI_INFINITE = [];

// Bersagli in cui qualche `.reveal` non si e' rivelato nemmeno dopo lo scorrimento.
const REVEAL_NASCOSTI = [];

// Bersagli il cui disegno non si e' fermato entro il tempo massimo.
const DISEGNO_INSTABILE = [];

// ---------------------------------------------------------------------
// Server statico minimale
// ---------------------------------------------------------------------

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.webp': 'image/webp',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.otf': 'font/otf',
  '.txt': 'text/plain; charset=utf-8',
  '.ico': 'image/x-icon',
};

function startServer() {
  return new Promise((resolve, reject) => {
    const server = http.createServer((req, res) => {
      try {
        const urlPath = decodeURIComponent(req.url.split('?')[0].split('#')[0]);
        const filePath = path.normalize(path.join(REPO_ROOT, urlPath));
        if (!filePath.startsWith(REPO_ROOT)) {
          res.writeHead(403);
          res.end('Fuori dalla radice del repository');
          return;
        }
        fs.stat(filePath, (err, stats) => {
          if (err) {
            res.writeHead(404);
            res.end(`Non trovato: ${urlPath}`);
            return;
          }
          const risolto = stats.isDirectory() ? path.join(filePath, 'index.html') : filePath;
          fs.readFile(risolto, (err2, dati) => {
            if (err2) {
              res.writeHead(404);
              res.end(`Non trovato: ${urlPath}`);
              return;
            }
            const ext = path.extname(risolto).toLowerCase();
            res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' });
            res.end(dati);
          });
        });
      } catch (e) {
        res.writeHead(500);
        res.end(String(e));
      }
    });
    server.on('error', reject);
    // porta 0 = scelta dal sistema operativo, garantita libera; evita 8777
    // (occupata) senza dover indovinare o cercare porte a mano.
    server.listen(0, '127.0.0.1', () => resolve({ server, port: server.address().port }));
  });
}

// ---------------------------------------------------------------------
// Determinismo: CSS di congelamento + stub dei timer periodici
// ---------------------------------------------------------------------

// animation-duration/transition-duration a 0 invece di animation:none —
// none farebbe ricadere l'elemento sullo stile non animato della cascata
// (rischioso per animazioni che partono da opacity:0 con fill-mode
// forwards: animation:none le lascerebbe invisibili). Con duration:0 il
// motore delle animazioni gira comunque e rispetta il fill-mode, solo
// senza il tempo di mezzo — l'aspetto finale e' quello autentico, solo
// istantaneo.
const CSS_CONGELAMENTO = `
  *, *::before, *::after {
    animation-duration: 0s !important;
    animation-delay: 0s !important;
    transition-duration: 0s !important;
    transition-delay: 0s !important;
    scroll-behavior: auto !important;
  }

  /* I blocchi .reveal arrivano allo stato finale per dichiarazione, non per
     transizione. Non e' solo velocita': un translateY(0) resta pur sempre una
     trasformazione, che promuove l'elemento a livello compositato e ne cambia
     la rasterizzazione del testo a seconda che il browser lo ri-unisca o no
     prima dello scatto. Il cancello di qualita' l'ha fatto emergere subito
     dopo l'introduzione dello scorrimento: differenze di pochi pixel sui
     bordi, con delta fino a 74, su pagine visivamente identiche. Togliendo la
     trasformazione la rasterizzazione e' una sola. */
  .reveal{ opacity: 1 !important; transform: none !important; }
`;

// Unico setInterval trovato nel repo (fondamenti-2-hardware-software.html)
// e' un orologio testuale che sale da 0.0s a 2.6s e ricomincia, all'infinito
// — non converge mai da solo, quindi non basta "aspettare abbastanza" come
// per il canvas di meccanismo-4. Se scattassimo lo screenshot a un istante
// qualunque leggeremmo un valore diverso a ogni cattura. Bloccare
// window.setInterval prima che qualunque script di pagina giri lascia il
// testo al valore iniziale renderizzato staticamente nell'HTML.
// setTimeout NON e' toccato: e' usato solo per animare l'accensione della
// "ladder" dopo un click sull'interruttore, un'interazione che questo
// harness non simula — bloccarlo comunque non farebbe differenza, ma
// lasciarlo intatto e' piu' fedele al comportamento reale della pagina.
async function scriptIniziale() {
  window.setInterval = () => 0;
}

// ---------------------------------------------------------------------
// Interazioni con nome, referenziate da bersagli.js
// ---------------------------------------------------------------------

const INTERAZIONI = {
  // Apre la "tenda" laterale dei concetti: cerca la funzione apriTenda nel
  // JS dei capitoli — si attiva cliccando un <button class="termine-concetto">.
  async 'apri-tenda'(page) {
    await page.click('.termine-concetto');
    await page.waitForSelector('#tenda-concetto.visibile', { timeout: 5000 });
  },

  // Apre il primo <details> ancora chiuso cliccando il suo <summary> —
  // stato nativo del browser, non simulato via attributo `open`.
  async 'apri-details'(page) {
    const summary = page.locator('details:not([open]) > summary').first();
    await summary.click();
  },

  // Tab reale (non .focus() programmatico, che in Chromium non sempre fa
  // scattare :focus-visible sugli stessi elementi) finche' l'elemento
  // attivo non e' genuinamente visibile DENTRO al viewport — l'ordine di
  // tabulazione e' deterministico a parita' di DOM, quindi il numero di Tab
  // necessari e' stabile fra le due catture del cancello di qualita'.
  // Nota scoperta durante lo sviluppo: i primi elementi nell'ordine di
  // tabulazione di ogni pagina del saggio sono i controlli della tenda dei
  // concetti (`.tenda-chiudi`, il link "Apri nella Lente semantica"), che
  // esistono sempre nel DOM ma sono spostati fuori dal viewport via CSS
  // quando la tenda e' chiusa — getBoundingClientRect() li riporta con
  // width/height > 0 (non sono display:none), quindi un controllo di sola
  // dimensione ci sarebbe atterrato sopra un pulsante invisibile all'occhio.
  async 'focus-visible'(page) {
    for (let i = 0; i < 20; i++) {
      await page.keyboard.press('Tab');
      const visibile = await page.evaluate(() => {
        const el = document.activeElement;
        if (!el || el === document.body) return false;
        const r = el.getBoundingClientRect();
        const s = getComputedStyle(el);
        const dentroViewport = r.right > 0 && r.bottom > 0 && r.left < window.innerWidth && r.top < window.innerHeight;
        return r.width > 0 && r.height > 0 && dentroViewport && s.visibility !== 'hidden' && s.display !== 'none';
      });
      if (visibile) return;
    }
    throw new Error('focus-visible: nessun elemento visibile nel viewport raggiunto in 20 Tab');
  },

  // Attiva il 2° grado nella Lente semantica (bottone #btn-grado-2, vedi
  // lente.js: impostaGrado(true)).
  async 'lente-grado2'(page) {
    await page.click('#btn-grado-2');
    await page.waitForFunction(() => document.getElementById('btn-grado-2').classList.contains('attivo'));
  },
};

// ---------------------------------------------------------------------
// Attese
// ---------------------------------------------------------------------

async function attendiPronta(page) {
  await page.evaluate(() => document.fonts.ready);
}

// Scorre l'intera pagina e torna in cima, per far scattare gli
// IntersectionObserver che rivelano i blocchi `.reveal`.
//
// PERCHE' ESISTE. Senza, l'harness fotografava pagine in cui i `.reveal`
// erano ancora a `opacity: 0` — e i `.reveal` contengono il **64%**
// dell'altezza complessiva delle 14 pagine del saggio. Il confronto a pixel
// vedeva quindi circa un terzo del contenuto, e dichiarava "zero differenze"
// su pagine in gran parte vuote. Trovato il 23 settembre 2026 cambiando il
// font monospaziato: i quattro simboli logici, alti 40px, non comparivano in
// nessuno dei due screenshot perche' stanno dentro un `.reveal`.
//
// Lo spostamento e' l'ultimo `.reveal` dichiarato visibile, non un numero di
// millisecondi: il congelamento delle animazioni rende la transizione
// istantanea, quindi la classe arriva subito dopo l'intersezione.
async function rivelaTutto(page) {
  await page.evaluate(async () => {
    const passo = Math.max(200, Math.floor(window.innerHeight * 0.8));
    const attendiDueFotogrammi = () =>
      new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
    let y = 0;
    // scrollHeight puo' crescere mentre si scorre (contenuto che si rivela)
    while (y < document.documentElement.scrollHeight) {
      window.scrollTo(0, y);
      await attendiDueFotogrammi();
      y += passo;
    }
    window.scrollTo(0, document.documentElement.scrollHeight);
    await attendiDueFotogrammi();
    window.scrollTo(0, 0);
    await attendiDueFotogrammi();
  });

  // Quanti restano nascosti: non un errore di per se' (un `.reveal` dentro un
  // `details` chiuso non si rivela mai), ma va detto invece che taciuto.
  return page.evaluate(() => {
    const tutti = [...document.querySelectorAll('.reveal')];
    return { totale: tutti.length,
             nascosti: tutti.filter((e) => !e.classList.contains('visible')).length };
  });
}

// Aspetta che il textContent di `selettore` smetta di cambiare per almeno
// `stabileMs` — usato per il loop requestAnimationFrame del widget
// "paesaggio di perdita" (meccanismo-4), che non e' un'animazione CSS e
// quindi il congelamento non lo ferma. La fisica e' deterministica (stessa
// posizione iniziale, stesso learning rate, soglia di arresto fissa nel
// codice sorgente) quindi il punto di convergenza e' sempre lo stesso;
// questa funzione aspetta solo che ci si arrivi, senza legare la cattura a
// un numero fisso di millisecondi indovinato a mano.
async function attendiAssestamento(page, selettore, { timeoutMs = 8000, stabileMs = 400, intervalMs = 100 } = {}) {
  const inizio = Date.now();
  let ultimo = null;
  let ultimoCambio = Date.now();
  while (Date.now() - inizio < timeoutMs) {
    const testo = await page.evaluate((sel) => {
      const el = document.querySelector(sel);
      return el ? el.textContent : null;
    }, selettore);
    if (testo !== ultimo) {
      ultimo = testo;
      ultimoCambio = Date.now();
    } else if (Date.now() - ultimoCambio >= stabileMs) {
      return;
    }
    await page.waitForTimeout(intervalMs);
  }
  console.warn(`  attenzione: "${selettore}" non si e' stabilizzato entro ${timeoutMs}ms (ultimo valore: ${JSON.stringify(ultimo)})`);
}

// Impronta di cio' che i widget disegnano: contenuto dei canvas, markup
// generato dentro gli SVG, e testo della pagina. Non e' il pixel esatto dello
// screenshot (troppo costoso da ripetere in polling) ma cattura tutto cio' che
// nel saggio cambia dopo il caricamento.
async function improntaDisegno(page) {
  return page.evaluate(() => {
    const parti = [];
    for (const c of document.querySelectorAll('canvas')) {
      try { parti.push(c.toDataURL()); } catch (e) { parti.push('canvas-non-leggibile'); }
    }
    for (const s of document.querySelectorAll('svg')) parti.push(s.innerHTML);
    parti.push(document.body.innerText);
    const s = parti.join('\u0001');
    let h1 = 0x811c9dc5, h2 = 0;
    for (let i = 0; i < s.length; i++) {
      h1 = (h1 ^ s.charCodeAt(i)) >>> 0;
      h1 = (h1 * 0x01000193) >>> 0;
      h2 = (h2 + s.charCodeAt(i) * (i + 1)) >>> 0;
    }
    return `${s.length}:${h1}:${h2}`;
  });
}

// Aspetta che quell'impronta smetta di cambiare.
//
// PERCHE'. Diversi widget del saggio disegnano con requestAnimationFrame, che
// il congelamento delle animazioni CSS non ferma: tokenizzatore, grafici di
// probabilita', mappa degli embedding, quantizzazione. Finche' i .reveal
// restavano a opacita' zero il loro output non compariva negli screenshot e la
// cosa non si vedeva; rivelandoli, il cancello di qualita' ha iniziato a
// fallire su bersagli diversi a ogni giro. Non e' rumore di rasterizzazione:
// e' disegno non ancora finito.
async function attendiDisegnoStabile(page, { timeoutMs = 9000, stabileMs = 500, intervalMs = 150 } = {}) {
  const inizio = Date.now();
  let ultima = null, ultimoCambio = Date.now();
  while (Date.now() - inizio < timeoutMs) {
    const i = await improntaDisegno(page);
    if (i !== ultima) { ultima = i; ultimoCambio = Date.now(); }
    else if (Date.now() - ultimoCambio >= stabileMs) return true;
    await page.waitForTimeout(intervalMs);
  }
  return false;
}

// ---------------------------------------------------------------------
// Salvataggio di un canvas
// ---------------------------------------------------------------------

async function salvaDataUrl(dataUrl, filePath) {
  const m = /^data:image\/png;base64,(.+)$/.exec(dataUrl);
  if (!m) throw new Error(`data: URL inatteso (non PNG base64): ${dataUrl.slice(0, 40)}…`);
  await fsp.writeFile(filePath, Buffer.from(m[1], 'base64'));
}

// ---------------------------------------------------------------------
// Cattura di un singolo bersaglio × viewport × variante
// ---------------------------------------------------------------------

async function catturaBersaglio(browser, baseURL, outDir, bersaglio, vpName, reducedMotion) {
  const viewport = VIEWPORTS[vpName];
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 1,
    reducedMotion: reducedMotion ? 'reduce' : 'no-preference',
  });
  await context.addInitScript(scriptIniziale);
  const page = await context.newPage();
  let scritti = 0;
  const suffisso = reducedMotion ? `${vpName}__reduced-motion` : vpName;
  const etichetta = `${bersaglio.id} · ${suffisso}`;

  try {
    await page.goto(baseURL + bersaglio.url, { waitUntil: 'networkidle' });
    await attendiPronta(page);

    // Nella variante reduced-motion, PRIMA di congelare, si censiscono le
    // animazioni infinite ancora in corso. Scoperta con il cancello di
    // qualita': fondamenti-2 ha tre cursori con `animation: 1.2s infinite
    // blink` che continuano a lampeggiare anche quando l'utente ha chiesto
    // meno animazioni, perche' il blocco @media (prefers-reduced-motion:
    // reduce) delle pagine contiene solo `scroll-behavior: auto`. E' una
    // lacuna di accessibilita' reale, non un difetto dell'harness: viene
    // riportata come elenco, non come differenza di immagine.
    if (reducedMotion) {
      const infinite = await page.evaluate(() =>
        document.getAnimations()
          .filter((a) => a.playState === 'running' && a.effect
                         && a.effect.getTiming().iterations === Infinity)
          .map((a) => a.animationName || 'senza nome'));
      if (infinite.length) {
        ANIMAZIONI_INFINITE.push({ bersaglio: bersaglio.id, animazioni: infinite });
      }
    }

    // Il congelamento si applica a ENTRAMBE le varianti. Non cambia quali
    // regole CSS si applicano (la media query resta attiva e il suo effetto
    // su colori e disposizione e' comunque catturato): azzera solo il tempo,
    // che e' l'unica fonte di non determinismo. Conseguenza dichiarata:
    // l'harness non verifica per immagine che le animazioni si fermino sotto
    // reduced-motion — quello lo dice il censimento qui sopra.
    await page.addStyleTag({ content: CSS_CONGELAMENTO });

    if (bersaglio.interazione) {
      await INTERAZIONI[bersaglio.interazione](page);
    }

    // Prima dell'assestamento: rivelare il contenuto puo' far partire widget
    // che a quel punto devono convergere.
    const rivelati = await rivelaTutto(page);
    if (rivelati.nascosti) {
      REVEAL_NASCOSTI.push(`${etichetta}: ${rivelati.nascosti}/${rivelati.totale}`);
    }

    if (bersaglio.assestamento) {
      await attendiAssestamento(page, bersaglio.assestamento);
    }

    if (!(await attendiDisegnoStabile(page))) {
      DISEGNO_INSTABILE.push(etichetta);
    }

    // Pausa finale prima dello scatto — piu' lunga di quanto sembri
    // necessario di proposito. Scoperta durante lo sviluppo (vedi README,
    // "Determinismo": il cancello di qualita' l'ha fatta emergere): anche
    // dopo che `document.fonts.ready` si risolve, il compositor di Chrome
    // puo' impiegare altri ~100-200ms per finire di rasterizzare il testo
    // appena "swappato" al font definitivo — una corsa invisibile a
    // qualunque promise JS, misurabile solo confrontando due catture a
    // processo Chrome separato (nello stesso processo non si vedeva mai:
    // da qui il valore del cancello di qualita' come richiesto, non di
    // un'esecuzione singola). Sotto ai 200ms, le pagine con titoli grandi
    // (meccanismo-1, meccanismo-5) mostravano differenze reali fra due
    // catture identiche, sempre nella stessa fascia verticale (il primo
    // "tile" di rasterizzazione sotto la piega originale); da 200ms in su,
    // zero differenze su piu' ripetizioni. 300ms lascia un margine di
    // sicurezza deliberato sopra quella soglia misurata.
    await page.waitForTimeout(300);

    if (!bersaglio.soloCanvas) {
      const filePath = path.join(outDir, `${bersaglio.id}__${suffisso}.png`);
      await page.screenshot({ path: filePath, fullPage: true });
      scritti++;
    }

    if (bersaglio.canvas && !reducedMotion) {
      const dataUrl = await page.evaluate((sel) => {
        const el = document.querySelector(sel);
        return el ? el.toDataURL('image/png') : null;
      }, bersaglio.canvas.selettore);
      if (dataUrl) {
        await salvaDataUrl(dataUrl, path.join(outDir, `${bersaglio.id}.png`));
        scritti++;
      } else {
        console.warn(`  attenzione: canvas "${bersaglio.canvas.selettore}" non trovato per ${etichetta}`);
      }
    }

    if (bersaglio.canvasAttr && !reducedMotion) {
      const { selettore, attributo } = bersaglio.canvasAttr;
      const dataUrl = await page.evaluate(
        ({ sel, attr }) => {
          const el = document.querySelector(sel);
          return el ? el.getAttribute(attr) : null;
        },
        { sel: selettore, attr: attributo },
      );
      if (dataUrl) {
        await salvaDataUrl(dataUrl, path.join(outDir, `${bersaglio.id}.png`));
        scritti++;
      } else {
        console.warn(`  attenzione: attributo "${attributo}" su "${selettore}" assente per ${etichetta}`);
      }
    }

    console.log(`  ok  ${etichetta}`);
  } catch (err) {
    console.error(`  ERRORE  ${etichetta}: ${err.message}`);
    throw err;
  } finally {
    await context.close();
  }
  return scritti;
}

// ---------------------------------------------------------------------
// Programma principale
// ---------------------------------------------------------------------

async function main() {
  const argv = process.argv.slice(2);
  const isBaseline = argv.includes('--baseline');
  const outDirName = isBaseline ? 'baseline' : 'attuale';
  const soloArg = argv.find((a) => a.startsWith('--solo='));
  const solo = soloArg ? new Set(soloArg.slice('--solo='.length).split(',')) : null;

  const outDir = path.join(__dirname, outDirName);
  await fsp.rm(outDir, { recursive: true, force: true });
  await fsp.mkdir(outDir, { recursive: true });

  const { server, port } = await startServer();
  const baseURL = `http://127.0.0.1:${port}`;
  console.log(`Server statico: ${baseURL} (radice: ${REPO_ROOT})`);
  console.log(`Scrivo in: ${outDirName}/\n`);

  const browser = await chromium.launch({ channel: 'chrome' });
  const t0 = Date.now();
  let totale = 0;
  let bersagliUsati = 0;

  try {
    for (const bersaglio of bersagli) {
      if (solo && !solo.has(bersaglio.id)) continue;
      bersagliUsati++;
      const viewportNames = bersaglio.viewports || ['desktop', 'mobile'];
      for (const vpName of viewportNames) {
        totale += await catturaBersaglio(browser, baseURL, outDir, bersaglio, vpName, false);
      }
      if (bersaglio.reducedMotion) {
        totale += await catturaBersaglio(browser, baseURL, outDir, bersaglio, 'desktop', true);
      }
    }
  } finally {
    await browser.close();
    await new Promise((resolve) => server.close(resolve));
  }

  const durata = ((Date.now() - t0) / 1000).toFixed(1);
  console.log(`\nFatto: ${bersagliUsati} bersagli, ${totale} file in ${outDirName}/, ${durata}s`);

  const rapporto = path.join(__dirname, 'animazioni-infinite.json');
  // Si cancella quando non c'e' piu' niente da segnalare: un rapporto
  // rimasto da un giro precedente direbbe il falso, ed e' proprio il genere
  // di bugia che passa inosservata.
  await fsp.rm(rapporto, { force: true });

  if (DISEGNO_INSTABILE.length) {
    console.log(`\nBersagli il cui disegno non si e' fermato entro il tempo massimo:`);
    for (const r of DISEGNO_INSTABILE) console.log(`  ${r}`);
  }

  if (REVEAL_NASCOSTI.length) {
    console.log(`\nBlocchi .reveal rimasti nascosti dopo lo scorrimento:`);
    for (const r of REVEAL_NASCOSTI) console.log(`  ${r}`);
  }

  if (ANIMAZIONI_INFINITE.length) {
    await fsp.writeFile(rapporto, JSON.stringify(ANIMAZIONI_INFINITE, null, 2) + '\n');
    console.log(`\nAnimazioni infinite ancora in corso sotto prefers-reduced-motion:`);
    for (const r of ANIMAZIONI_INFINITE) {
      console.log(`  ${r.bersaglio}: ${r.animazioni.join(', ')}`);
    }
    console.log(`  (elenco anche in ${path.basename(rapporto)})`);
  }
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
