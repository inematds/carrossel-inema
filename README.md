# carrossel-inema

**Carrossel de Instagram, Facebook e TikTok pronto em minutos, no padrão INEMA.** Você diz o tema; o Claude Code escreve o roteiro, o Codex desenha a capa, um navegador sem janela transforma tudo em imagens 1080×1350 (feed) e 1080×1920 (stories), o próprio sistema confere se nada estourou e só posta depois do seu "aprovado".

🇧🇷 Português · [🇺🇸 English](README.en.md) · [🇪🇸 Español](README.es.md) · Guia: https://inematds.github.io/carrossel-inema/guia/

## O que sai

| Peça | Tamanho | Para quê |
|---|---|---|
| Capa | 1080×1350 | segurar o dedo: número + assunto pelo nome + título em até 4 linhas |
| 5 a 10 slides | 1080×1350 | uma ideia por slide, número grande, trecho-chave em negrito, dado com fonte |
| Fecho | 1080×1350 | "Comenta PALAVRA" com a palavra em destaque |
| 3 stories | 1080×1920 | levar ao post, puxar resposta, repetir a palavra |
| `relatorio.json` | — | o que encolheu, o que não coube, imagem quebrada |

## Instalar (uma vez)

Precisa de Linux ou Mac com Node.js 18+, Python 3 e um Chromium (o do Playwright serve). Para a capa com arte: Codex CLI logado na sua conta ChatGPT (assinatura, sem chave de API).

```bash
git clone https://github.com/inematds/carrossel-inema ~/projetos/carrossel-inema
cd ~/projetos/carrossel-inema
bash setup.sh                     # tem que terminar em SELFTEST PASS
ln -s "$PWD" ~/.claude/skills/carrossel-inema   # liga a skill no Claude Code
```

Se o Chromium não for achado: `CHROME=/caminho/do/chrome bash setup.sh`.

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
| 8 | Postar | `scripts/publicar.sh <slides> <legenda.txt>` (rascunho) · `AO_VIVO=1 …` (ao vivo) → Metricool inematds (IG + TikTok) | 🤖 |

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

- **`publicar.sh` ainda não foi testado.** O formato de carrossel com várias imagens e de story no Metricool não foi conferido; o primeiro uso deve ser como rascunho, com o Nei olhando o planner.
- Stories pelo Metricool dependem da conta Instagram ser profissional.
- Fontes Sora e Inter: licença SIL Open Font License, incluídas em `assets/fonts/`.

Licença do código: MIT.
