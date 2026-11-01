#!/usr/bin/env node
// Carrossel INEMA — roteiro.json → PNGs (feed 1080x1350 + stories 1080x1920) + relatorio.json
// Uso: node scripts/render.mjs <roteiro.json> [pasta-de-saida]
import { chromium } from "playwright-core";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";

const RAIZ = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const [arqRoteiro, saidaArg] = process.argv.slice(2);
if (!arqRoteiro) { console.error("uso: node scripts/render.mjs <roteiro.json> [saida]"); process.exit(2); }
const roteiro = JSON.parse(fs.readFileSync(arqRoteiro, "utf8"));
const pastaRoteiro = path.dirname(path.resolve(arqRoteiro));
const saida = path.resolve(saidaArg || path.join(pastaRoteiro, "slides"));
fs.mkdirSync(saida, { recursive: true });

function acharChrome() {
  if (process.env.CHROME && fs.existsSync(process.env.CHROME)) return process.env.CHROME;
  const base = path.join(os.homedir(), ".cache/ms-playwright");
  const dirs = fs.existsSync(base) ? fs.readdirSync(base).filter(d => /^chromium-\d+$/.test(d)).sort().reverse() : [];
  for (const d of dirs) for (const sub of ["chrome-linux-arm64/chrome", "chrome-linux64/chrome", "chrome-linux/chrome", "chrome-mac/Chromium.app/Contents/MacOS/Chromium", "chrome-mac-arm64/Chromium.app/Contents/MacOS/Chromium"]) {
    const p = path.join(base, d, sub);
    if (fs.existsSync(p)) return p;
  }
  for (const p of ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/google-chrome", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]) if (fs.existsSync(p)) return p;
  throw new Error("Chromium não encontrado: rode `npx playwright install chromium` ou defina CHROME=/caminho/do/chrome");
}

const esc = s => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
// **negrito** no texto vira <b>
const rico = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<b>$1</b>");
const arquivo = p => (p ? pathToFileURL(path.resolve(pastaRoteiro, p)).href : "");
const SETA = `<svg class="seta" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>`;

// fontes embutidas em base64: o Chromium bloqueia fonte por file:// vinda de outra pasta
const css = fs.readFileSync(path.join(RAIZ, "templates/base.css"), "utf8")
  .replace(/url\("\{\{FONTS\}\}\/([\w-]+)\.(woff2|ttf)"\)/g, (_, f, ext) =>
    `url(data:font/${ext};base64,${fs.readFileSync(path.join(RAIZ, "assets/fonts", `${f}.${ext}`)).toString("base64")})`);
const marca = esc(roteiro.marca || "INEMA.CLUB");
const conta = esc(roteiro.conta || "");
const total = (roteiro.slides?.length || 0) + 2;

function topo(i) {
  return `<div class="top"><span class="marca">${marca}</span><span>${i} / ${total}</span></div>`;
}

function capa() {
  const c = roteiro.capa || {};
  if (c.imagem) {
    // arte do Codex já traz o título desenhado; aqui só a etiqueta da marca
    return `<div class="page feed" style="padding:0"><img class="capa-img" src="${arquivo(c.imagem)}">
      ${c.etiqueta === false ? "" : `<div class="capa-tag">${marca}</div>`}</div>`;
  }
  const hl = (c.destaque || "").toUpperCase();
  const linhas = (c.titulo || []).map(l => {
    let h = esc(l.toUpperCase());
    if (hl) h = h.replace(esc(hl), `<span class="hl">${esc(hl)}</span>`);
    return h;
  });
  return `<div class="page feed">${topo(1)}
    <div class="capa-titulo" data-fit>${linhas.join("<br>")} ${SETA}</div>
    <div class="rodape">${conta}</div></div>`;
}

function slide(s, i) {
  const dados = (s.dados || []).slice(0, 2).map(d =>
    `<div class="dado"><div class="v">${esc(d.valor)}</div><div class="r">${esc(d.rotulo)}</div></div>`).join("");
  return `<div class="page feed">${topo(i)}
    <div class="marcadagua">${esc(s.numero ?? i - 1)}</div>
    <div class="corpo">
    <div class="num">${esc(s.numero ?? i - 1)}</div>
    <div class="titulo" data-fit>${rico(s.titulo)}</div>
    <div class="texto" data-fit>${rico(s.texto)}</div>
    ${s.print ? `<div class="print"><img src="${arquivo(s.print)}"></div>` : ""}
    ${s.fonte ? `<div class="fonte">Fonte: ${esc(s.fonte)}</div>` : ""}
    ${dados ? `<div class="dados">${dados}</div>` : ""}</div>
    <div class="rodape"><span>${conta}</span><span class="arraste">arraste ${SETA}</span></div></div>`;
}

function fecho() {
  const f = roteiro.fecho || {};
  return `<div class="page feed">${topo(total)}
    <div class="fecho-titulo" data-fit>${rico(f.titulo || "Quer o passo a passo?")}</div>
    <div class="fecho-texto" data-fit>${rico(f.texto || "Comenta a palavra abaixo que eu te mando o guia grátis.")}</div>
    <div class="palavra">${esc((roteiro.palavra || "GUIA").toUpperCase())}</div>
    <div class="rodape">${marca} ${conta ? "· " + conta : ""}</div></div>`;
}

function story(s, i) {
  const ultimo = i === (roteiro.stories || []).length;
  // o 1º story mostra a capa do post (já renderizada) para levar a pessoa ao carrossel
  const mostraCapa = s.mostrar === "capa" || (s.mostrar === undefined && i === 1);
  const capaPng = pathToFileURL(path.join(saida, "01-capa.png")).href;
  return `<div class="page story"><div class="top"><span class="marca">${marca}</span><span>${i} / ${roteiro.stories.length}</span></div>
    <div class="corpo">
    ${mostraCapa ? `<div class="story-capa"><img src="${capaPng}"></div>` : ""}
    <div class="titulo" data-fit>${rico(s.titulo)}</div>
    <div class="texto" data-fit>${rico(s.texto)}</div>
    ${ultimo ? `<div class="palavra">${esc((roteiro.palavra || "GUIA").toUpperCase())}</div>` : ""}
    </div>
    <div class="rodape"><span>${conta}</span><span class="arraste">${mostraCapa ? "toque no post " + SETA : ""}</span></div></div>`;
}

const paginas = [
  { nome: "01-capa.png", html: capa(), w: 1080, h: 1350 },
  ...(roteiro.slides || []).map((s, k) => ({ nome: `${String(k + 2).padStart(2, "0")}-slide.png`, html: slide(s, k + 2), w: 1080, h: 1350 })),
  { nome: `${String(total).padStart(2, "0")}-fecho.png`, html: fecho(), w: 1080, h: 1350 },
  ...(roteiro.stories || []).map((s, k) => ({ nome: `story-${k + 1}.png`, html: story(s, k + 1), w: 1080, h: 1920 })),
];

const browser = await chromium.launch({ executablePath: acharChrome(), args: ["--no-sandbox", "--allow-file-access-from-files"] });
const relatorio = { roteiro: path.resolve(arqRoteiro), saida, paginas: [] };
try {
  const ctx = await browser.newContext({ deviceScaleFactor: 1 });
  const page = await ctx.newPage();
  for (const p of paginas) {
    await page.setViewportSize({ width: p.w, height: p.h });
    const doc = `<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>${css}</style></head><body>${p.html}</body></html>`;
    const tmp = path.join(saida, ".pagina.html");
    fs.writeFileSync(tmp, doc);
    await page.goto(pathToFileURL(tmp).href);
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.all([...document.images].map(i => (i.complete ? null : i.decode().catch(() => null))));
    });
    // encolhe a letra até caber (no máximo 30%) e anota o que não coube
    const medida = await page.evaluate(() => {
      const caixa = document.querySelector(".page").getBoundingClientRect();
      const out = [];
      for (const el of document.querySelectorAll("[data-fit]")) {
        const base = parseFloat(getComputedStyle(el).fontSize);
        let esc = 1;
        const estoura = () => {
          const r = el.getBoundingClientRect();
          // folga de 15% da letra: a Sora sobe acima da linha e dava falso "não coube"
          const folga = parseFloat(getComputedStyle(el).fontSize) * 0.15;
          return el.scrollHeight > el.clientHeight + folga || el.scrollWidth > el.clientWidth + 2 || r.bottom > caixa.bottom - 40;
        };
        while (estoura() && esc > 0.7) { esc -= 0.04; el.style.fontSize = base * esc + "px"; }
        out.push({ classe: el.className, escala: +esc.toFixed(2), estourou: estoura(), px: Math.round(base * esc),
          sh: el.scrollHeight, ch: el.clientHeight, sw: el.scrollWidth, cw: el.clientWidth, fim: Math.round(el.getBoundingClientRect().bottom) });
      }
      const imgs = [...document.images].map(i => ({ src: i.src.split("/").pop(), ok: i.naturalWidth > 0 }));
      const fontes = [...document.fonts].filter(f => f.status === "loaded").map(f => f.family + " " + f.weight);
      return { caixas: out, imagens: imgs, fontes };
    });
    await page.locator(".page").screenshot({ path: path.join(saida, p.nome) });
    relatorio.paginas.push({ nome: p.nome, largura: p.w, altura: p.h, ...medida });
    console.log("ok", p.nome);
  }
  fs.rmSync(path.join(saida, ".pagina.html"), { force: true });
} finally {
  await browser.close();
}
fs.writeFileSync(path.join(saida, "relatorio.json"), JSON.stringify(relatorio, null, 2));
console.log(`pronto: ${paginas.length} imagens em ${saida}`);
