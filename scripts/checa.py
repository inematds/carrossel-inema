#!/usr/bin/env python3
"""Confere um carrossel renderizado antes de mostrar ao Nei.

Uso: python3 scripts/checa.py <pasta-dos-slides> [roteiro.json]
Sai com código 1 se houver ERRO. AVISO não bloqueia.
"""
import json
import re
import struct
import sys
from pathlib import Path

PROIBIDAS = ["revolucion", "incrível", "inacreditável", "insano", "!!", "mude sua vida", "segredo que ninguém"]


def tamanho_png(p: Path):
    with p.open("rb") as f:
        cab = f.read(24)
    if cab[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", cab[16:24])


def amarelado(p: Path):
    """(R+G)/2 - B médio: foto neutra fica de 0 a 10. Sem Pillow, não mede."""
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(p).convert("RGB").resize((108, 135))
    px = list(im.getdata())
    return sum((r + g) / 2 - b for r, g, b in px) / len(px)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pasta = Path(sys.argv[1])
    rel = json.loads((pasta / "relatorio.json").read_text())
    roteiro_p = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(rel["roteiro"])
    roteiro = json.loads(roteiro_p.read_text())
    erros, avisos = [], []

    feed = sorted(p for p in pasta.glob("[0-9][0-9]-*.png"))
    stories = sorted(pasta.glob("story-*.png"))
    if not (pasta / "01-capa.png").exists():
        erros.append("falta a capa (01-capa.png)")
    n_slides = len(roteiro.get("slides", []))
    if not 5 <= n_slides <= 10:
        erros.append(f"{n_slides} slides de conteúdo; o padrão é de 5 a 10")
    if len(stories) != 3:
        avisos.append(f"{len(stories)} stories (o padrão são 3)")

    for p in feed:
        if tamanho_png(p) != (1080, 1350):
            erros.append(f"{p.name}: tamanho {tamanho_png(p)} (esperado 1080x1350)")
    for p in stories:
        if tamanho_png(p) != (1080, 1920):
            erros.append(f"{p.name}: tamanho {tamanho_png(p)} (esperado 1080x1920)")

    for pg in rel["paginas"]:
        for c in pg["caixas"]:
            if c["estourou"]:
                erros.append(f"{pg['nome']}: texto não coube em .{c['classe']} — encurte")
            elif c["escala"] < 0.85:
                avisos.append(f"{pg['nome']}: letra de .{c['classe']} reduzida para {c['px']}px — texto longo")
            if c["px"] < 24:
                erros.append(f"{pg['nome']}: letra {c['px']}px, abaixo do mínimo de leitura no celular")
        for im in pg["imagens"]:
            if not im["ok"]:
                erros.append(f"{pg['nome']}: imagem quebrada {im['src']}")

    capa = roteiro.get("capa", {})
    if not capa.get("imagem"):
        linhas = capa.get("titulo", [])
        if len(linhas) > 4:
            erros.append(f"capa com {len(linhas)} linhas; máximo 4")
        texto_capa = " ".join(linhas)
        if not re.search(r"\d", texto_capa):
            avisos.append("capa sem número (número no título segura o dedo)")
        if roteiro.get("assunto") and roteiro["assunto"].lower() not in texto_capa.lower():
            avisos.append(f"capa não cita o assunto '{roteiro['assunto']}' pelo nome")
    else:
        arte = roteiro_p.parent / capa["imagem"]
        if not arte.exists():
            erros.append(f"capa aponta para {capa['imagem']}, que não existe")
        else:
            am = amarelado(arte)
            if am is None:
                avisos.append("Pillow ausente: não medi se a capa saiu amarelada (python3 -m pip install pillow)")
            elif am is not None and am > 25 and not capa.get("cor_livre"):
                erros.append(f"capa amarelada ({am:.0f}; limite 25): gerar de novo com luz neutra ou marcar capa.cor_livre=true")
            elif am is not None and am > 18:
                avisos.append(f"capa puxando para o amarelo ({am:.0f}; ideal até 18)")
        if not capa.get("texto_conferido"):
            avisos.append("capa com arte gerada: conferir o texto desenhado e marcar capa.texto_conferido=true")

    palavra = (roteiro.get("palavra") or "").strip()
    if not re.fullmatch(r"[A-Za-zÀ-ú0-9]{3,14}", palavra):
        erros.append(f"palavra do comentário '{palavra}' inválida (uma palavra, 3 a 14 letras)")

    tudo = json.dumps(roteiro, ensure_ascii=False).lower()
    for w in PROIBIDAS:
        if w in tudo:
            erros.append(f"palavra de hype proibida: '{w}'")
    for k, s in enumerate(roteiro.get("slides", []), start=2):
        if len(s.get("titulo", "")) > 70:
            avisos.append(f"slide {k}: título com {len(s['titulo'])} caracteres (ideal até 70)")
        if len(s.get("texto", "")) > 260:
            avisos.append(f"slide {k}: texto com {len(s['texto'])} caracteres (ideal até 260)")
        if any(ch.isdigit() for ch in s.get("texto", "") + json.dumps(s.get("dados", []))) and not s.get("fonte"):
            avisos.append(f"slide {k}: tem número mas não tem 'fonte' — confirmar o dado")

    for a in avisos:
        print("AVISO", a)
    for e in erros:
        print("ERRO ", e)
    print(f"{len(feed)} imagens de feed, {len(stories)} stories · {len(erros)} erro(s), {len(avisos)} aviso(s)")
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
