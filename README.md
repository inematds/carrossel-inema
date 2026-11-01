# carrossel-inema

[![carrossel-inema](guia/assets/banner.jpg)](https://inematds.github.io/carrossel-inema/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

O carrossel-inema é uma skill (um conjunto de instruções e scripts) para o Claude Code que faz carrosséis de Instagram e TikTok; as mesmas imagens servem para o Facebook. Serve para quem quer postar com frequência sem abrir programa de design. Você dá o tema; ele entrega a capa, de 5 a 10 slides com uma ideia cada, o slide final com "comenta PALAVRA" e 3 stories, todos no tamanho certo. Antes de mostrar, ele confere se algum texto ficou cortado ou pequeno demais. Para usar, precisa de um computador Linux ou Mac (no Windows, pelo WSL, o Linux que roda dentro do Windows) com Node.js, Python e o Claude Code; para a capa com arte, o Codex logado na sua conta do ChatGPT. Os textos saem em português por padrão; o idioma se troca no PERFIL.md.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/carrossel-inema/guia/**

## O que sai

| Peça | Tamanho | Para quê |
|---|---|---|
| Capa | 1080×1350 | segurar o dedo: número + assunto pelo nome + título em até 4 linhas |
| 5 a 10 slides | 1080×1350 | uma ideia por slide, número grande, trecho-chave em negrito, dado com fonte |
| Fecho | 1080×1350 | "Comenta PALAVRA" com a palavra em destaque |
| 3 stories | 1080×1920 | levar ao post, puxar resposta, repetir a palavra |
| `relatorio.json` | — | o que encolheu, o que não coube, imagem quebrada |

## Instalar (uma vez)

Precisa de Linux ou Mac com Node.js 18+, Python 3 (com Pillow: `python3 -m pip install pillow`) e um Chromium (`npx playwright install chromium`; no Mac, o Google Chrome instalado já serve). Para a capa com arte: Codex CLI logado na sua conta ChatGPT (assinatura, sem chave de API).

```bash
git clone https://github.com/inematds/carrossel-inema ~/projetos/carrossel-inema
cd ~/projetos/carrossel-inema
bash setup.sh                     # tem que terminar em SELFTEST PASS
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/carrossel-inema   # liga a skill no Claude Code
```

Sem Chromium na máquina: `npx playwright install chromium` (ou, no Mac, `export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`).

**Troque a marca:** o `PERFIL.md` vem com a marca do INEMA (@inema.tds, Nei Maldaner, hashtags). Edite antes do primeiro carrossel.

## Usar

No Claude Code: **"faz um carrossel sobre <tema>"** ou **"qual deve ser o próximo carrossel?"**. A skill segue `SKILL.md` e lê `PERFIL.md` (marca, tom, regras aprendidas).

À mão:

```bash
node scripts/render.mjs exemplos/teste/roteiro.json /tmp/teste   # gera as 11 imagens
python3 scripts/checa.py /tmp/teste exemplos/teste/roteiro.json  # confere
python3 scripts/capa.py meu/roteiro.json --estilo 3d --cena "..." # capa com arte do Codex
```

## O processo, do início ao fim

🧠 sessão com o Nei · ⚙️ script · 🤖 Codex/`claude -p` (assinatura)

| # | Passo | Comando / o que acontece | Quem |
|---|---|---|---|
| 1 | Tema | Nei dá o tema, ou a skill propõe 3 (o que funcionou, o que está em alta, o que perguntam) | 🧠 |
| 2 | Palavra + guia grátis | uma palavra para o comentário e a página do inema.club que ela entrega | 🧠 |
| 3 | Roteiro | `roteiro.json` (capa, 5–10 slides, fecho, 3 stories); 3 opções de capa para o Nei escolher | 🧠 |
| 4 | Capa | `python3 scripts/capa.py <roteiro.json> --estilo … --cena …` → `capa.png` com o título desenhado; conferir o texto | 🤖 |
| 5 | Render | `node scripts/render.mjs <roteiro.json> <pasta>/slides` | ⚙️ |
| 6 | Checagem | `python3 scripts/checa.py <pasta>/slides` (0 erro) + olhar a prancha | ⚙️ + 🧠 |
| 7 | Aprovação | Nei aprova; cada correção vira regra no `PERFIL.md` | 🧠 |
| 8 | Postar | `scripts/publicar.sh <slides> <legenda.txt>` (rascunho) · `AO_VIVO=1 …` (ao vivo) → Metricool inematds (Instagram + TikTok; Facebook à mão) | 🤖 |

## Arquivos

| Caminho | O que é |
|---|---|
| `SKILL.md` | passo a passo que o Claude segue |
| `PERFIL.md` | marca, tom, hashtags, últimas capas e regras aprendidas |
| `scripts/render.mjs` | roteiro → PNGs (encolhe a letra até 30% se precisar e anota) |
| `scripts/checa.py` | portão: tamanhos, texto estourado, letra pequena, palavra, hype, número sem fonte |
| `scripts/capa.py` | capa pelo Codex image_gen (assinatura) |
| `scripts/publicar.sh` | agenda no Metricool (rascunho por padrão; ainda não testado) |
| `templates/base.css` | visual (cores, fontes, medidas) |
| `exemplos/teste/` | roteiro de exemplo usado no autoteste |

## Limites

- **`publicar.sh` vem configurado para a conta do INEMA** (repo `inematds/carrossel-inema`, conector `metricool-inematds`, marca `inema.tds`). Para a sua: crie o repositório com `gh repo create carrossel-imagens --public --add-readme`, ligue o Metricool com `claude mcp add --transport http --scope user metricool https://ai.metricool.com/mcp` (e `/mcp` para entrar) e rode `export REPO=voce/carrossel-imagens CONECTOR=metricool MARCA=<marca>` antes de rodar (vale para o rascunho e para o `AO_VIVO=1`); precisa do `gh` logado e do Metricool ligado ao Claude Code (MCP).
- **`publicar.sh` só roda no Linux ou no WSL** (usa o `date` do Linux); no Mac, poste as imagens à mão.
- **`publicar.sh` ainda não foi testado.** O formato de carrossel com várias imagens e de story no Metricool não foi conferido; o primeiro uso deve ser como rascunho, com o Nei olhando o planner.
- Stories pelo Metricool dependem da conta Instagram ser profissional.
- Fontes Sora e Inter: licença SIL Open Font License, incluídas em `assets/fonts/`.

Licença do código: MIT.
