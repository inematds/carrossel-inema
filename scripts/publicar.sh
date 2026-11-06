#!/usr/bin/env bash
# Publica um carrossel aprovado no Metricool da conta inematds ("metritds": Instagram + TikTok inema.tds).
# Só rodar depois do OK do Nei para AQUELE carrossel.
# uso: scripts/publicar.sh <pasta-dos-slides> <legenda.txt> ["AAAA-MM-DD HH:MM" Brasília, padrão agora + 10 min]
#   As imagens sobem para a release "carrossel-<nome-da-pasta>" do repo público (o Metricool precisa de URL pública).
#   Padrão = RASCUNHO (não vai ao ar). Para publicar de verdade: AO_VIVO=1.
#   REPO=<dono/repo> troca o repo que hospeda (padrão inematds/carrossel-inema). MARCA=<label> (padrão inema.tds).
#   CONECTOR=<nome do servidor MCP do Metricool no seu Claude Code> (padrão metricool-inematds, a conta do INEMA).
#   SEM_STORIES=1 não agenda os stories.
#   Para a SUA conta: gh logado com escrita num repo público seu (REPO=voce/repo), Metricool ligado ao Claude Code
#   como conector MCP (nome em CONECTOR) e a marca do Metricool em MARCA.
set -uo pipefail
date -d "today" >/dev/null 2>&1 || { echo "publicar.sh usa o date do Linux: rode no Linux ou no WSL (no Mac, poste as imagens à mão)"; exit 2; }
export PATH="$HOME/.local/bin:$HOME/.npm-global/bin:$PATH"
PASTA="$(realpath "$1")"; TXT="$(realpath "$2")"; QUANDO_IN="${3:-}"
REPO="${REPO:-inematds/carrossel-inema}"
CON="${CONECTOR:-metricool-inematds}"
[ -s "$TXT" ] || { echo "falta a legenda"; exit 2; }
LIMPO="$(mktemp --suffix=.txt)"; python3 $HOME/projetos/metricool-inematds/sem_links.py "$TXT" "$LIMPO" || exit 2; TXT="$LIMPO"   # sem link no Metricool (Nei, 05/11/2026)
[ -s "$PASTA/01-capa.png" ] || { echo "falta $PASTA/01-capa.png"; exit 2; }
python3 "$(dirname "$0")/checa.py" "$PASTA" || { echo "checagem com erro: não publico"; exit 2; }

if [ -n "$QUANDO_IN" ]; then ALVO=$(TZ=America/Sao_Paulo date -d "$QUANDO_IN" +%s); else ALVO=$(( $(date +%s) + 600 )); fi
[ "$ALVO" -lt $(( $(date +%s) + 300 )) ] && ALVO=$(( $(date +%s) + 600 ))
H_BR=$(TZ=America/Sao_Paulo date -d "@$ALVO" +%H)
[ "$H_BR" -ge 21 ] && echo "aviso: entre 21h e 23h59 o Metricool grava 1 h depois; conferir no planner"
QUANDO_UTC=$(date -u -d "@$ALVO" +%Y-%m-%dT%H:%M:00)

TAG="carrossel-$(basename "$PASTA")"
gh release view "$TAG" -R "$REPO" >/dev/null 2>&1 || \
  gh release create "$TAG" -R "$REPO" --title "Carrossel $(basename "$PASTA")" --notes "Imagens usadas pelo Metricool." >/dev/null
FEED=$(ls "$PASTA"/[0-9][0-9]-*.png | sort)
STORIES=$(ls "$PASTA"/story-*.png 2>/dev/null | sort)
gh release upload "$TAG" $FEED $STORIES -R "$REPO" --clobber || { echo "Falhou: upload na release"; exit 1; }
URL="https://github.com/$REPO/releases/download/$TAG"
MEDIA=$(for f in $FEED; do printf '"%s/%s",' "$URL" "$(basename "$f")"; done | sed 's/,$//')
ST=$(for f in $STORIES; do printf '"%s/%s",' "$URL" "$(basename "$f")"; done | sed 's/,$//')
RASC=$([ -n "${AO_VIVO:-}" ] && echo false || echo true)

PEDIDO="Use só as ferramentas do servidor MCP $CON.
1) getBrandSettings: blogId da marca com label exatamente \"${MARCA:-inema.tds}\" e quais destas redes estão conectadas: instagram, tiktok.
2) createScheduledPost UMA vez (carrossel) com as redes conectadas:
   date = ${QUANDO_UTC}Z ; publicationDate = {dateTime: \"${QUANDO_UTC}\", timezone: \"UTC\"}
   media = [$MEDIA] (nesta ordem) ; text = conteúdo exato do arquivo $TXT (leia com Read)
   draft = $RASC ; autoPublish = true
   instagramData = {type: \"POST\", isAiGenerated: false}
   tiktokData = {privacyOption: \"PUBLIC_TO_EVERYONE\", title: primeira linha do texto (até 90 caracteres), isAigc: false}
$( [ -z "${SEM_STORIES:-}" ] && [ -n "$ST" ] && echo "3) Para cada imagem de [$ST], na ordem, um createScheduledPost só no instagram, instagramData = {type: \"STORY\"}, mesmo draft, 2 minutos depois do anterior (o primeiro 15 min depois do carrossel), text vazio." )
Responda APENAS uma linha JSON, sem crase: {\"ok\":true|false,\"posts\":N,\"redes\":[...],\"planner\":[...],\"erro\":\"\"}"
OUT=$(printf '%s' "$PEDIDO" | timeout 600 env -u ANTHROPIC_API_KEY claude -p \
      --allowedTools "mcp__${CON}__getBrandSettings mcp__${CON}__createScheduledPost Read" 2>&1)
echo "$OUT" | tail -3
echo "$OUT" | grep -q '"ok":true' && echo "Terminei: carrossel $([ "$RASC" = true ] && echo 'agendado como RASCUNHO' || echo 'agendado') para $(TZ=America/Sao_Paulo date -d "@$ALVO" '+%d/%m %H:%M')" \
  || { echo "Falhou: Metricool não agendou"; exit 1; }
