# Changelog

## 1.0.0 — 01/11/2026
- Render HTML → PNG (capa, 5–10 slides, fecho, 3 stories) com Chromium sem janela; fontes Sora e Inter embutidas.
- Encolhe a letra até 30% quando o texto não cabe e anota no `relatorio.json`.
- `checa.py`: tamanhos, texto estourado, letra < 24 px, imagem quebrada, palavra do comentário, hype, número sem fonte, capa sem número.
- `capa.py`: capa com título desenhado pelo Codex image_gen (assinatura).
- `publicar.sh`: carrossel + stories no Metricool inematds; rascunho por padrão. **Ainda não testado.**
- `checa.py` mede o amarelado da capa ((R+G)/2−B): aviso acima de 18, erro acima de 25. Estilos da capa com luz neutra.
- Autoteste `setup.sh` → `SELFTEST PASS`.
