# carrossel-inema

[![carrossel-inema](guia/assets/banner-es.jpg)](https://inematds.github.io/carrossel-inema/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

carrossel-inema es una skill (un conjunto de instrucciones y scripts) para Claude Code que crea carruseles para Instagram y TikTok; las mismas imágenes sirven para Facebook. Es para quienes quieren publicar con frecuencia sin abrir un programa de diseño. Le das el tema y entrega la portada, de 5 a 10 diapositivas con una idea cada una, la diapositiva final con «comenta PALABRA» y 3 stories, todo en el tamaño adecuado. Antes de mostrarlo, comprueba si algún texto quedó cortado o demasiado pequeño. Para usarla, necesitas un ordenador Linux o Mac (en Windows, mediante WSL, el Linux que funciona dentro de Windows) con Node.js, Python y Claude Code; para la portada con ilustración, Codex con la sesión iniciada en tu cuenta de ChatGPT. Los textos se generan en portugués de forma predeterminada; el idioma se cambia en PERFIL.md.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/carrossel-inema/guia/es/**

## Qué genera

| Elemento | Tamaño | Para qué sirve |
|---|---|---|
| Portada | 1080×1350 | captar la atención: número + tema por su nombre + título de hasta 4 líneas |
| 5 a 10 diapositivas | 1080×1350 | una idea por diapositiva, número grande, fragmento clave en negrita, dato con fuente |
| Cierre | 1080×1350 | «Comenta PALABRA» con la palabra destacada |
| 3 stories | 1080×1920 | llevar a la publicación, invitar a responder, repetir la palabra |
| `relatorio.json` | — | qué se redujo, qué no cupo, imagen rota |

## Instalar (una vez)

Necesitas Linux o Mac con Node.js 18+, Python 3 y Chromium (sirve el de Playwright). Para la portada con ilustración: Codex CLI con la sesión iniciada en tu cuenta de ChatGPT (suscripción, sin clave de API).

```bash
git clone https://github.com/inematds/carrossel-inema ~/projetos/carrossel-inema
cd ~/projetos/carrossel-inema
bash setup.sh                     # tem que terminar em SELFTEST PASS
mkdir -p ~/.claude/skills
ln -s "$PWD" ~/.claude/skills/carrossel-inema   # liga a skill no Claude Code
```

Si no tienes Chromium en el equipo: `npx playwright install chromium` (o, en Mac, `export CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"`).

**Cambia la marca:** `PERFIL.md` viene con la marca de INEMA (@inema.tds, Nei Maldaner, hashtags). Edítalo antes del primer carrusel.

## Usar

En Claude Code: **«haz un carrusel sobre <tema>»** o **«¿cuál debería ser el próximo carrusel?»**. La skill sigue `SKILL.md` y lee `PERFIL.md` (marca, tono, reglas aprendidas).

A mano:

```bash
node scripts/render.mjs exemplos/teste/roteiro.json /tmp/teste   # genera las 11 imágenes
python3 scripts/checa.py /tmp/teste exemplos/teste/roteiro.json  # comprueba
python3 scripts/capa.py meu/roteiro.json --estilo 3d --cena "..." # portada con ilustración de Codex
```

## El proceso, de principio a fin

🧠 sesión con Nei · ⚙️ script · 🤖 Codex/`claude -p` (suscripción)

| # | Paso | Comando / qué ocurre | Quién |
|---|---|---|---|
| 1 | Tema | Nei da el tema o la skill propone 3 (lo que funcionó, lo que está en tendencia, lo que preguntan) | 🧠 |
| 2 | Palabra + guía gratis | una palabra para el comentario y la página de inema.club que ofrece | 🧠 |
| 3 | Guion | `roteiro.json` (portada, 5–10 diapositivas, cierre, 3 stories); 3 opciones de portada para que Nei elija | 🧠 |
| 4 | Portada | `python3 scripts/capa.py <roteiro.json> --estilo … --cena …` → `capa.png` con el título dibujado; comprobar el texto | 🤖 |
| 5 | Renderizado | `node scripts/render.mjs <roteiro.json> <pasta>/slides` | ⚙️ |
| 6 | Revisión | `python3 scripts/checa.py <pasta>/slides` (0 errores) + revisar la lámina de conjunto | ⚙️ + 🧠 |
| 7 | Aprobación | Nei aprueba; cada corrección se convierte en una regla en `PERFIL.md` | 🧠 |
| 8 | Publicar | `scripts/publicar.sh <slides> <legenda.txt>` (borrador) · `AO_VIVO=1 …` (en directo) → Metricool inematds (Instagram + TikTok; Facebook manualmente) | 🤖 |

## Archivos

| Ruta | Qué es |
|---|---|
| `SKILL.md` | paso a paso que sigue Claude |
| `PERFIL.md` | marca, tono, hashtags, últimas portadas y reglas aprendidas |
| `scripts/render.mjs` | guion → PNGs (reduce el tamaño de letra hasta el 30% si hace falta y lo anota) |
| `scripts/checa.py` | filtro: tamaños, texto desbordado, letra pequeña, palabra, exageraciones, número sin fuente |
| `scripts/capa.py` | portada con Codex image_gen (suscripción) |
| `scripts/publicar.sh` | programa publicaciones en Metricool (borrador de forma predeterminada; aún no se ha probado) |
| `templates/base.css` | aspecto visual (colores, fuentes, medidas) |
| `exemplos/teste/` | guion de ejemplo usado en la prueba automática |

## Límites

- **`publicar.sh` está configurado para la cuenta de INEMA** (repo `inematds/carrossel-inema`, conector `metricool-inematds`, marca `inema.tds`). Para la tuya: `export REPO=voce/repo CONECTOR=<conector do Metricool> MARCA=<marca>` antes de ejecutarlo (sirve tanto para el borrador como para `AO_VIVO=1`); necesitas tener la sesión iniciada en `gh` y Metricool conectado a Claude Code (MCP).
- **`publicar.sh` aún no se ha probado.** No se ha comprobado el formato de carrusel con varias imágenes ni el de story en Metricool; la primera vez debe usarse como borrador, con Nei revisando el planificador.
- Las stories en Metricool dependen de que la cuenta de Instagram sea profesional.
- Fuentes Sora e Inter: licencia SIL Open Font License, incluidas en `assets/fonts/`.

Licencia del código: MIT.