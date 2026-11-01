#!/usr/bin/env bash
# Instala o carrossel-inema e roda o autoteste. Tem que terminar em "SELFTEST PASS".
set -euo pipefail
cd "$(dirname "$0")"

falha() { echo "SELFTEST FAIL: $*"; exit 1; }

command -v node >/dev/null || falha "Node.js não encontrado (precisa da versão 18 ou mais nova)"
command -v python3 >/dev/null || falha "python3 não encontrado"
command -v ffmpeg >/dev/null || echo "aviso: ffmpeg ausente (só faz falta para ajustar a capa gerada)"

# playwright-core não baixa navegador; usa o Chromium que já existe na máquina
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install --silent --no-audit --no-fund >/dev/null

for f in Sora.ttf Inter-400.ttf Inter-500.ttf Inter-700.ttf; do
  [ -s "assets/fonts/$f" ] || falha "fonte assets/fonts/$f ausente"
done

SAIDA="$(mktemp -d /tmp/carrossel-selftest.XXXX)"
node scripts/render.mjs exemplos/teste/roteiro.json "$SAIDA" >/dev/null || falha "render falhou (Chromium? defina CHROME=/caminho)"
python3 scripts/checa.py "$SAIDA" exemplos/teste/roteiro.json || falha "checagem acusou erro em $SAIDA"
n=$(ls "$SAIDA"/*.png | wc -l)
[ "$n" -eq 11 ] || falha "esperava 11 imagens (capa + 6 + fecho + 3 stories), saiu $n"
echo "imagens de teste: $SAIDA"
echo "SELFTEST PASS"
