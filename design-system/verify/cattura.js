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

    if (bersaglio.assestamento) {
      await attendiAssestamento(page, bersaglio.assestamento);
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

  if (ANIMAZIONI_INFINITE.length) {
    const rapporto = path.join(__dirname, 'animazioni-infinite.json');
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
