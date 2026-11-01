#!/usr/bin/env python3
"""Gera a arte da capa pelo Codex (image_gen, assinatura) com o título desenhado na imagem.

Uso: python3 scripts/capa.py <roteiro.json> [--cena "descrição da cena"] [--estilo foto|3d|ilustracao]
Grava <pasta-do-roteiro>/capa.png (1080x1350) e atualiza capa.imagem no roteiro.
Depois de gerar: CONFERIR o texto desenhado (a IA erra letra) e marcar "texto_conferido": true.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Luz NEUTRA (branco que parece branco); o amarelo INEMA fica só no texto desenhado (regra de 12/10/2026)
ESTILOS = {
    "foto": "fotografia realista com cara de foto de verdade, luz neutra de dia ou de estúdio (branco que parece branco), fundo escuro, profundidade de campo rasa, um assunto grande",
    "3d": "render 3D realista, materiais foscos e metal prateado ou grafite, luz neutra de estúdio, fundo escuro, um assunto grande",
    "ilustracao": "ilustração editorial limpa, traço firme, fundo escuro, cores neutras com um único acento amarelo #FACC15",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("roteiro")
    ap.add_argument("--cena", default="", help="o que aparece na imagem (sem o título)")
    ap.add_argument("--estilo", default="foto", choices=ESTILOS)
    a = ap.parse_args()

    rp = Path(a.roteiro).resolve()
    rot = json.loads(rp.read_text())
    capa = rot.setdefault("capa", {})
    linhas = capa.get("titulo") or []
    if not linhas:
        sys.exit("roteiro sem capa.titulo")
    destaque = (capa.get("destaque") or "").upper()
    cena = a.cena or capa.get("cena") or f"cena que mostra, sem precisar ler, o assunto: {rot.get('assunto', '')}"

    pasta = rp.parent / "capa-codex"
    pasta.mkdir(exist_ok=True)
    titulo = " / ".join(l.upper() for l in linhas)
    pedido = f"""Gere UMA imagem com a ferramenta de geração de imagem (image_gen) e salve nesta pasta como capa.png, formato RETRATO 4:5 (o maior tamanho disponível nessa proporção).

É a capa de um carrossel de Instagram do perfil {rot.get('conta', '')} (marca INEMA.CLUB).
Cena: {cena}.
Estilo: {ESTILOS[a.estilo]}. Nada de luz dourada, tom quente geral ou objetos dourados por toda a cena. Nada de robô de desenho animado: se aparecer robô, é humanoide industrial liso tipo Tesla Optimus, com visor escuro na frente da cabeça.
Título DESENHADO dentro da imagem, em caixa alta, fonte sans geométrica bem pesada, branco, em exatamente estas linhas:
{chr(10).join('  ' + l.upper() for l in linhas)}
{f'A palavra "{destaque}" em amarelo #FACC15 e as outras em branco.' if destaque else ''}
Termine a última linha com uma seta para a direita (→).
O título ocupa a metade de cima ou a metade de baixo, letras enormes (legíveis num celular em miniatura), sem cortar nenhuma letra, com margem de pelo menos 6% das bordas.
Escreva o texto exatamente como acima, com acentos corretos, sem palavras extras, sem logotipo inventado, sem marca d'água.
Não mexa em nenhum outro arquivo da pasta. Ao final, diga o nome do arquivo salvo.
"""
    (pasta / "pedido.txt").write_text(pedido)
    env = dict(os.environ)
    env["PATH"] = f"{Path.home()}/.npm-global/bin:" + env.get("PATH", "")  # CLI novo antes do antigo em /usr/bin
    print("Codex gerando a capa (pode levar alguns minutos)…", flush=True)
    with open(pasta / "codex.log", "w") as lg:
        subprocess.run(["codex", "exec", "--skip-git-repo-check", "--dangerously-bypass-approvals-and-sandbox", "-"],
                       input=pedido, text=True, cwd=pasta, stdout=lg, stderr=subprocess.STDOUT, timeout=1800, env=env)
    gerada = pasta / "capa.png"
    if not gerada.exists():
        cands = sorted(pasta.glob("*.png"), key=lambda p: p.stat().st_mtime)
        if not cands:
            sys.exit(f"Codex não gerou a imagem (veja {pasta / 'codex.log'})")
        gerada = cands[-1]
    final = rp.parent / "capa.png"
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(gerada), "-vf",
                        "scale=1080:1350:force_original_aspect_ratio=increase,crop=1080:1350", str(final)], check=True)
    else:
        shutil.copy(gerada, final)
    capa["imagem"] = "capa.png"
    capa["texto_conferido"] = False
    rp.write_text(json.dumps(rot, ensure_ascii=False, indent=2) + "\n")
    print(f"capa: {final}\nAgora confira o texto desenhado e marque capa.texto_conferido=true no roteiro.")


if __name__ == "__main__":
    main()
