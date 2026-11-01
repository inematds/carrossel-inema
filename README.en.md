# carrossel-inema

[![carrossel-inema](guia/assets/banner-en.jpg)](https://inematds.github.io/carrossel-inema/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

carrossel-inema is a skill (a set of instructions and scripts) for Claude Code that creates Instagram and TikTok carousels; the same images also work for Facebook. It’s for anyone who wants to post regularly without opening a design program. You provide the topic; it creates the cover, 5 to 10 slides with one idea each, a final slide with “comment WORD,” and 3 stories, all in the right dimensions. Before showing the images, it checks whether any text is cut off or too small. To use it, you need a Linux or Mac computer (on Windows, use WSL, the Linux environment that runs inside Windows) with Node.js, Python, and Claude Code; for an illustrated cover, you need Codex logged into your ChatGPT account. Text is in Portuguese by default; change the language in PERFIL.md.

## 📖 Usage guide

Complete guide (landing page + walkthrough): **https://inematds.github.io/carrossel-inema/guia/en/**

## What it creates

| Item | Size | Purpose |
|---|---|---|
| Cover | 1080×1350 | stop the scroll: number + topic named explicitly + title in up to 4 lines |
| 5 to 10 slides | 1080×1350 | one idea per slide, large number, key excerpt in bold, sourced fact |
| Closing slide | 1080×1350 | “Comment WORD” with the word highlighted |
| 3 stories | 1080×1920 | lead to the post, invite a reply, repeat the word |
| `relatorio.json` | — | what was shrunk, what didn’t fit, broken images |

## Install (once)

You need Linux or Mac with Node.js 18+, Python 3 (with Pillow: `python3 -m pip install pillow`), and Chromium (`npx playwright install chromium`; on Mac, installed Google Chrome works too). For an illustrated cover: Codex CLI logged into your ChatGPT account (subscription, no API key).

```bash
git clone https://github.com/inematds/carrossel-inema ~/projetos/carrossel-inema
cd ~/projetos/carrossel-inema
bash setup.sh                     # must finish with SELFTEST PASS
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/carrossel-inema   # links the skill in Claude Code
```

If Chromium isn’t installed: `npx playwright install chromium` (or, on Mac, `export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`).

**Replace the brand:** `PERFIL.md` comes with the INEMA brand (@inema.tds, Nei Maldaner, hashtags). Edit it before creating your first carousel.

## Use

In Claude Code: **“create a carousel about <topic>”** or **“what should the next carousel be about?”**. The skill follows `SKILL.md` and reads `PERFIL.md` (brand, tone, learned rules).

Manually:

```bash
node scripts/render.mjs exemplos/teste/roteiro.json /tmp/teste   # generates the 11 images
python3 scripts/checa.py /tmp/teste exemplos/teste/roteiro.json  # checks them
python3 scripts/capa.py meu/roteiro.json --estilo 3d --cena "..." # cover with Codex artwork
```

## The process, start to finish

🧠 session with Nei · ⚙️ script · 🤖 Codex/`claude -p` (subscription)

| # | Step | Command / what happens | Who |
|---|---|---|---|
| 1 | Topic | Nei provides the topic, or the skill suggests 3 (what worked, what’s trending, what people ask about) | 🧠 |
| 2 | Word + free guide | a word to comment and the inema.club page it leads to | 🧠 |
| 3 | Script | `roteiro.json` (cover, 5–10 slides, closing slide, 3 stories); 3 cover options for Nei to choose from | 🧠 |
| 4 | Cover | `python3 scripts/capa.py <roteiro.json> --estilo … --cena …` → `capa.png` with the title drawn on it; check the text | 🤖 |
| 5 | Render | `node scripts/render.mjs <roteiro.json> <pasta>/slides` | ⚙️ |
| 6 | Check | `python3 scripts/checa.py <pasta>/slides` (0 errors) + review the contact sheet | ⚙️ + 🧠 |
| 7 | Approval | Nei approves; each correction becomes a rule in `PERFIL.md` | 🧠 |
| 8 | Post | `scripts/publicar.sh <slides> <legenda.txt>` (draft) · `AO_VIVO=1 …` (live) → Metricool inematds (Instagram + TikTok; post to Facebook manually) | 🤖 |

## Files

| Path | What it is |
|---|---|
| `SKILL.md` | step-by-step instructions Claude follows |
| `PERFIL.md` | brand, tone, hashtags, recent covers, and learned rules |
| `scripts/render.mjs` | script → PNGs (shrinks the font to 30% if needed and records it) |
| `scripts/checa.py` | gate: dimensions, overflowing text, small font, word, hype, unsourced number |
| `scripts/capa.py` | cover using Codex image_gen (subscription) |
| `scripts/publicar.sh` | schedules in Metricool (draft by default; not yet tested) |
| `templates/base.css` | visuals (colors, fonts, dimensions) |
| `exemplos/teste/` | example script used in the self-test |

## Limitations

- **`publicar.sh` is configured for the INEMA account** (repo `inematds/carrossel-inema`, connector `metricool-inematds`, brand `inema.tds`). For your account: run `export REPO=you/repo CONECTOR=<Metricool connector> MARCA=<brand>` before running it (applies to both drafts and `AO_VIVO=1`); requires `gh` to be logged in and Metricool connected to Claude Code (MCP).
- **`publicar.sh` only runs on Linux or WSL** (uses Linux `date`); on Mac, post the images manually.
- **`publicar.sh` has not been tested yet.** The Metricool format for carousels with multiple images and for stories has not been verified; the first use should be as a draft, with Nei checking the planner.
- Stories through Metricool require a professional Instagram account.
- Sora and Inter fonts: SIL Open Font License, included in `assets/fonts/`.

Code license: MIT.