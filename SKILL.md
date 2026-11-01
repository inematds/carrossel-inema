---
name: carrossel-inema
description: Carrossel de Instagram/Facebook/TikTok no padrão INEMA — escolhe o tema, escreve o roteiro (capa com número + 5–10 slides de uma ideia cada + fecho "comenta PALAVRA" + 3 stories), gera a capa pelo Codex, renderiza 1080x1350 e 1080x1920, confere sozinho, mostra cada imagem ao Nei e só posta no Metricool (metritds) depois do OK. Gatilho: "carrossel", "faz um carrossel sobre X", "qual o próximo carrossel", "slides para o Instagram", "posta o carrossel".
---

# carrossel-inema

Leia `PERFIL.md` antes de tudo, toda vez. Ele tem a marca, as contas, o tom e as **regras aprendidas** (cada correção do Nei vira uma linha lá).

## Os 7 passos (sempre nesta ordem)

### 1. Tema
- Se o Nei já deu o tema, use. Se perguntou "qual o próximo?", proponha 3 temas com o porquê de cada:
  - o que mais funcionou nos nossos posts (pergunte ou leia o relatório do muse-canais, se existir);
  - o que está em alta hoje (radar-pautas, se existir);
  - perguntas que o público repete nos comentários.
- Formatos que seguram o dedo: lista com número ("7 ferramentas…", "5 erros…"), passo a passo, antes × depois.
- Uma ideia por carrossel. Nunca copie texto, imagem ou personagem de outro perfil: só o formato.

### 2. Palavra e guia grátis
- Escolha UMA palavra para o comentário (3 a 14 letras, sem espaço): ex. `AGENTE`, `PROMPT`.
- O guia grátis é a página do INEMA.CLUB sobre o assunto (curso, guia ou projeto que já existe). Confira o link antes.
- Se não existir página, avise o Nei: o lead-comenta cria a página.

### 3. Roteiro (`roteiro.json`)
Crie a pasta `~/projetos/output/carrossel-inema/<AAAA-MM-DD>-<slug>/` e escreva o `roteiro.json` no formato de `exemplos/teste/roteiro.json`:
- **capa.titulo**: 4 linhas curtas, lê como uma frase em voz alta, tem um **número**, cita o **assunto/ferramenta pelo nome** (nunca "sua IA"). `capa.destaque` = a palavra que fica amarela.
- **slides** (5 a 10): `numero`, `titulo` (até ~60 caracteres), `texto` (2–3 frases, até ~240 caracteres, `**negrito**` no trecho-chave), opcional `dados` (até 2 caixas `{valor, rotulo}`), `print` (caminho de print real da ferramenta), `fonte` (obrigatória quando há número).
- **Números só checados hoje**, com fonte. Sem número inventado. Sem hype (ver `regras/texto.md` do inema-design).
- **fecho**: título com pergunta + texto curto; a palavra aparece grande.
- **stories** (3): 1º chama para o post (mostra a capa sozinho), 2º pergunta algo ao público, 3º repete a palavra.

Mostre ao Nei 3 opções de título da capa e o roteiro em texto ANTES de gerar imagem.

### 4. Capa
- Padrão: arte pelo Codex com o título desenhado dentro (`python3 scripts/capa.py <roteiro.json> --estilo foto|3d|ilustracao --cena "..."`).
- Checklist da capa (todas):
  - [ ] lê como título de vídeo, faz sentido em voz alta;
  - [ ] tem número;
  - [ ] cita o assunto/ferramenta pelo nome;
  - [ ] no máximo 4 linhas, letra enorme no celular;
  - [ ] tapando o texto, a imagem sozinha ainda diz o assunto;
  - [ ] logo real do produto, se houver, visível e não coberto;
  - [ ] diferente das últimas capas (cena e estilo) — ver `PERFIL.md › últimas capas`;
  - [ ] **texto desenhado conferido letra por letra** → `capa.texto_conferido: true`.
- Sem arte (pressa ou Codex fora): tirar `capa.imagem`; o render faz a capa tipográfica.

### 5. Render e checagem
```bash
node scripts/render.mjs <pasta>/roteiro.json <pasta>/slides
python3 scripts/checa.py <pasta>/slides <pasta>/roteiro.json
```
- ERRO = corrigir e renderizar de novo. AVISO = olhar e decidir.
- Olhe TODAS as imagens você mesmo (monte uma prancha com ffmpeg `tile`) antes de mostrar: texto cortado, número × rótulo trocados, erro de digitação, nada copiado.

### 6. Aprovação do Nei
Mostre a prancha + a legenda (`<pasta>/legenda.txt`: 1ª linha = gancho, 2–4 linhas, "Comenta PALAVRA", até 5 hashtags). Espere "aprovado"/"posta".
Toda correção que ele fizer: aplique E escreva como regra em `PERFIL.md › Regras aprendidas` (uma linha, com data).

### 7. Postar (só com OK)
```bash
scripts/publicar.sh <pasta>/slides <pasta>/legenda.txt ["AAAA-MM-DD HH:MM"]   # rascunho
AO_VIVO=1 scripts/publicar.sh <pasta>/slides <pasta>/legenda.txt              # ao vivo
```
Instagram + TikTok `inema.tds` pelo Metricool da conta inematds (conector `metricool-inematds`, sem chave de API).
Depois: anote a capa em `PERFIL.md › últimas capas` e registre o post em `<pasta>/publicado.txt`.

## Não fazer
- Postar sem OK. Apagar post no Metricool (só com OK, um por um).
- Usar API paga (ElevenLabs, OpenAI, Blotato…). Arte = Codex pela assinatura; reserva = flux2-klein local.
- Mais de 10 slides; mais de uma ideia por slide; print falso (mock-up).
