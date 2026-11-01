# carrossel-inema

[![carrossel-inema](guia/assets/banner-en.jpg)](https://inematds.github.io/carrossel-inema/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

carrossel-inema is a skill (a set of instructions and scripts) for Claude Code that creates Instagram and TikTok carousels; the same images also work for Facebook. It’s for anyone who wants to post regularly without opening a design program. You provide the topic; it delivers the cover, 5 to 10 slides with one idea each, a final slide with “comment KEYWORD,” and 3 stories, all at the right size. Before showing them, it checks whether any text is cut off or too small. To use it, you need a Linux or Mac computer (on Windows, use WSL, the Linux environment that runs inside Windows) with Node.js, Python, and Claude Code; for an illustrated cover, you need Codex signed in to your ChatGPT account. Text is in Portuguese by default; change the language in PERFIL.md.

## 📖 User guide

Complete guide (landing page + step-by-step instructions): **https://inematds.github.io/carrossel-inema/guia/en/**

## What it produces

| Item | Size | Purpose |
|---|---|---|
| Cover | 1080×1350 | stop the scroll: number + topic named explicitly + title in up to 4 lines |
| 5 to 10 slides | 1080×1350 | one idea per slide, large number, key excerpt in bold, sourced data |
| Closing slide | 1080×1350 | “Comment KEYWORD” with the keyword highlighted |
| 3 stories | 1080×1920 | direct people to the post, invite a response, repeat the keyword |
| `relatorio.json` | — | what was shrunk, what didn’t fit, broken images |

## Install (once)

Requires Linux or Mac with Node.js 18+, Python 3, and Chromium (Playwright’s version works). For illustrated covers: Codex CLI signed in to your ChatGPT account (subscription, no API key).

```bash
git clone https://github.com/inematds/carrossel-inema ~/projetos/carrossel-inema
cd ~/projetos/carrossel-inema
bash setup.sh                     # must finish with SELFTEST PASS
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/carrossel-inema   # links the skill in Claude Code
```

No Chromium on your machine? Run `npx playwright install chromium` (or, on Mac, `export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`).

**Change the branding:** `PERFIL.md` comes with INEMA branding (@inema.tds, Nei Maldaner, hashtags). Edit it before your first carousel.

## Use

In Claude Code: **“make a carousel about <topic>”** or **“what should the next carousel be?”** The skill follows `SKILL.md` and reads `PERFIL.md` (branding, tone, rules learned).

Manually:

```bash
node scripts/render.mjs exemplos/teste/roteiro.json /tmp/teste   # generates 11 images
python3 scripts/checa.py /tmp/teste exemplos/teste/roteiro.json  # checks them
python3 scripts/capa.py meu/roteiro.json --estilo 3d --cena "..." # cover with Codex artwork
```

## The process, from start to finish

🧠 session with Nei · ⚙️ script · 🤖 Codex/`claude -p` (subscription)

| # | Step | Command / what happens | Who |
|---|---|---|---|
| 1 | Topic | Nei provides the topic, or the skill suggests 3 (what worked, what’s trending, what people ask about) | 🧠 |
| 2 | Keyword + free guide | a keyword for the comment and the inema.club page it leads to | 🧠 |
| 3 | Script | `roteiro.json` (cover, 5–10 slides, closing slide, 3 stories); 3 cover options for Nei to choose from | 🧠 |
| 4 | Cover | `python3 scripts/capa.py <roteiro.json> --estilo … --cena …` → `capa.png` with the title rendered; check the text | 🤖 |
| 5 | Render | `node scripts/render.mjs <roteiro.json> <pasta>/slides` | ⚙️ |
| 6 | Check | `python3 scripts/checa.py <pasta>/slides` (0 errors) + review the contact sheet | ⚙️ + 🧠 |
| 7 | Approval | Nei approves; each correction becomes a rule in `PERFIL.md` | 🧠 |
| 8 | Post | `scripts/publicar.sh <slides> <legenda.txt>` (draft) · `AO_VIVO=1 …` (live) → Metricool inematds (Instagram + TikTok; Facebook manually) | 🤖 |

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | step-by-step instructions Claude follows |
| `PERFIL.md` | branding, tone, hashtags, recent covers, and rules learned |
| `scripts/render.mjs` | script → PNGs (shrinks the font to 30% if needed and records it) |
| `scripts/checa.py` | gate: dimensions, overflowing text, small type, keyword, hype, numbers without sources |
| `scripts/capa.py` | cover via Codex image_gen (subscription) |
| `scripts/publicar.sh` | schedules in Metricool (draft by default; not yet tested) |
| `templates/base.css` | visual style (colors, fonts, dimensions) |
| `exemplos/teste/` | sample script used in the self-test |

Code license: MIT.

## Limitations

- **`publicar.sh` is configured for the INEMA account** (repo `inematds/carrossel-inema`, connector `metricool-inematds`, brand `inema.tds`). For your account: run `export REPO=you/repo CONECTOR=<Metricool connector> MARCA=<brand>` first (applies to both drafts and `AO_VIVO=1`); requires `gh` to be logged in and Metricool connected to Claude Code (MCP).
- **`publicar.sh` has not been tested yet.** The carousel format with multiple images and the story format in Metricool haven’t been checked; the first use should be as a draft, with Nei reviewing the planner.
- Stories through Metricool require a professional Instagram account.
- Sora and Inter fonts: SIL Open Font License, included in `assets/fonts/`.