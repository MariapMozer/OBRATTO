#!/usr/bin/env python3
"""
Script de Geração de Fotos de Teste - Projeto OBRATTO

Gera fotos placeholder para usuários e produtos usando PIL/Pillow.

TODO ALUNOS: Entender geração programática de imagens
- Como criar imagens com PIL/Pillow
- Dimensões adequadas para fotos de perfil e produtos
- Por que usar placeholders em desenvolvimento

Uso: python scripts/gerar_fotos_teste.py
"""

import os
import sys
from pathlib import Path
from typing import Union

# Adicionar o diretório pai ao sys.path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)
sys.path.insert(0, projeto_dir)

try:
    from PIL import Image, ImageDraw, ImageFont
    from PIL.ImageFont import FreeTypeFont, ImageFont as ImageFontBase
except ImportError:
    print("❌ Pillow não está instalado!")
    print("   Execute: pip install Pillow")
    sys.exit(1)


# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================

DIRETORIO_USUARIOS = Path("static/uploads/teste/usuarios")
DIRETORIO_PRODUTOS = Path("static/uploads/teste/produtos")

# Dimensões
TAMANHO_AVATAR = (400, 400)
TAMANHO_PRODUTO = (600, 400)

# Cores para avatares (Nome -> Cor de fundo)
CORES_AVATAR = {
    "Admin Principal": "#3498db",
    "Maria Administradora": "#e74c3c",
    "João Moderador": "#2ecc71",
    "Maria Silva": "#9b59b6",
    "João Santos": "#f39c12",
    "Ana Paula Costa": "#1abc9c",
    "Carlos Eduardo Lima": "#34495e",
    "Fernanda Oliveira": "#e67e22",
    "Pedro Eletricista": "#3498db",
    "Carla Encanadora": "#1abc9c",
    "Ricardo Pintor": "#e74c3c",
    "Julia Jardineira": "#2ecc71",
    "Marcos Pedreiro": "#95a5a6",
    "Casa das Tintas": "#e74c3c",
    "Materiais Hidráulicos Silva": "#3498db",
    "Elétrica Total": "#f39c12",
    "Jardinagem Verde Vida": "#27ae60",
    "Construção Forte": "#7f8c8d",
}

# Cores para produtos (Categoria -> Cor)
CORES_PRODUTO = {
    "tinta": "#e74c3c",
    "verniz": "#8e44ad",
    "registro": "#3498db",
    "caixa": "#1abc9c",
    "tubo": "#95a5a6",
    "disjuntor": "#f39c12",
    "tomada": "#e67e22",
    "fio": "#34495e",
    "substrato": "#27ae60",
    "grama": "#2ecc71",
    "kit": "#16a085",
    "cimento": "#7f8c8d",
    "areia": "#d4ac6e",
    "tijolo": "#c0392b",
}


def hex_to_rgb(hex_color: str) -> tuple:
    """Converte cor hexadecimal para RGB"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def obter_iniciais(nome: str) -> str:
    """Obtém as iniciais de um nome (máximo 2 letras)"""
    partes = nome.split()
    if len(partes) >= 2:
        return (partes[0][0] + partes[1][0]).upper()
    return partes[0][:2].upper()


def gerar_avatar(nome: str, cor_hex: str, caminho_saida: Path):
    """
    Gera uma foto de avatar com iniciais

    TODO ALUNOS: Observe:
    - Criação de imagem em memória com PIL
    - Desenho de formas e texto
    - Salvamento em formato JPEG
    """
    # Criar imagem com cor de fundo
    cor_fundo = hex_to_rgb(cor_hex)
    img = Image.new('RGB', TAMANHO_AVATAR, cor_fundo)
    draw = ImageDraw.Draw(img)

    # Obter iniciais
    iniciais = obter_iniciais(nome)

    # Tentar carregar fonte, usar padrão se não conseguir
    fonte: Union[FreeTypeFont, ImageFontBase]
    try:
        # Tamanho da fonte proporcional ao tamanho da imagem
        tamanho_fonte = TAMANHO_AVATAR[0] // 3
        fonte = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", tamanho_fonte)
    except:
        fonte = ImageFont.load_default()

    # Centralizar texto
    bbox = draw.textbbox((0, 0), iniciais, font=fonte)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    posicao = (
        (TAMANHO_AVATAR[0] - text_width) // 2,
        (TAMANHO_AVATAR[1] - text_height) // 2 - 20
    )

    # Desenhar texto em branco
    draw.text(posicao, iniciais, fill='white', font=fonte)

    # Salvar imagem
    img.save(caminho_saida, 'JPEG', quality=85)


def gerar_foto_produto(nome_produto: str, cor_hex: str, caminho_saida: Path):
    """
    Gera uma foto de produto colorida com o nome

    TODO ALUNOS: Observe:
    - Imagens com dimensões diferentes (retangular)
    - Texto multilinhas para nomes longos
    """
    # Criar imagem com cor de fundo
    cor_fundo = hex_to_rgb(cor_hex)
    img = Image.new('RGB', TAMANHO_PRODUTO, cor_fundo)
    draw = ImageDraw.Draw(img)

    # Tentar carregar fonte
    fonte: Union[FreeTypeFont, ImageFontBase]
    try:
        fonte = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        fonte = ImageFont.load_default()

    # Quebrar texto em múltiplas linhas se necessário
    palavras = nome_produto.split()
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + " " + palavra if linha_atual else palavra
        bbox = draw.textbbox((0, 0), teste, font=fonte)
        if bbox[2] - bbox[0] < TAMANHO_PRODUTO[0] - 40:
            linha_atual = teste
        else:
            if linha_atual:
                linhas.append(linha_atual)
            linha_atual = palavra

    if linha_atual:
        linhas.append(linha_atual)

    # Desenhar cada linha centralizada
    y_offset = (TAMANHO_PRODUTO[1] - len(linhas) * 50) // 2

    for i, linha in enumerate(linhas):
        bbox = draw.textbbox((0, 0), linha, font=fonte)
        text_width = bbox[2] - bbox[0]
        x = (TAMANHO_PRODUTO[0] - text_width) // 2
        y = y_offset + i * 50
        draw.text((x, y), linha, fill='white', font=fonte)

    # Salvar imagem
    img.save(caminho_saida, 'JPEG', quality=85)


def gerar_todas_fotos_usuarios():
    """Gera fotos de perfil para todos os usuários"""
    print("\n📸 Gerando fotos de perfil dos usuários...\n")

    usuarios = [
        ("Admin Principal", "admin_principal.jpg"),
        ("Maria Administradora", "maria_admin.jpg"),
        ("João Moderador", "joao_moderador.jpg"),
        ("Maria Silva", "maria_silva.jpg"),
        ("João Santos", "joao_santos.jpg"),
        ("Ana Paula Costa", "ana_costa.jpg"),
        ("Carlos Eduardo Lima", "carlos_lima.jpg"),
        ("Fernanda Oliveira", "fernanda_oliveira.jpg"),
        ("Pedro Eletricista", "pedro_eletricista.jpg"),
        ("Carla Encanadora", "carla_encanadora.jpg"),
        ("Ricardo Pintor", "ricardo_pintor.jpg"),
        ("Julia Jardineira", "julia_jardineira.jpg"),
        ("Marcos Pedreiro", "marcos_pedreiro.jpg"),
        ("Casa das Tintas", "casa_tintas.jpg"),
        ("Materiais Hidráulicos Silva", "materiais_silva.jpg"),
        ("Elétrica Total", "eletrica_total.jpg"),
        ("Jardinagem Verde Vida", "verde_vida.jpg"),
        ("Construção Forte", "construcao_forte.jpg"),
    ]

    for nome, arquivo in usuarios:
        caminho = DIRETORIO_USUARIOS / arquivo
        cor = CORES_AVATAR.get(nome, "#95a5a6")
        gerar_avatar(nome, cor, caminho)
        print(f"✅ {arquivo}")


def gerar_todas_fotos_produtos():
    """Gera fotos para todos os produtos"""
    print("\n📦 Gerando fotos dos produtos...\n")

    produtos = [
        ("Tinta Acrílica Branca 18L", "tinta_acrilica.jpg", "tinta"),
        ("Tinta Látex Amarela 3.6L", "tinta_latex.jpg", "tinta"),
        ("Verniz Marítimo 900ml", "verniz_maritimo.jpg", "verniz"),
        ("Registro de Pressão 1/2", "registro_pressao.jpg", "registro"),
        ("Caixa D'água 1000L", "caixa_dagua.jpg", "caixa"),
        ("Tubo PVC 50mm 6m", "tubo_pvc.jpg", "tubo"),
        ("Disjuntor Bipolar 40A", "disjuntor_bipolar.jpg", "disjuntor"),
        ("Tomada 2P+T 10A Branca", "tomada_branca.jpg", "tomada"),
        ("Fio Flexível 2.5mm 100m", "fio_flexivel.jpg", "fio"),
        ("Substrato Orgânico 15kg", "substrato_organico.jpg", "substrato"),
        ("Grama Esmeralda m²", "grama_esmeralda.jpg", "grama"),
        ("Kit Ferramentas Jardinagem", "kit_ferramentas.jpg", "kit"),
        ("Cimento CP-II 50kg", "cimento_cp2.jpg", "cimento"),
        ("Areia Média m³", "areia_media.jpg", "areia"),
        ("Tijolo Furado 8 Furos", "tijolo_furado.jpg", "tijolo"),
    ]

    for nome, arquivo, categoria in produtos:
        caminho = DIRETORIO_PRODUTOS / arquivo
        cor = CORES_PRODUTO.get(categoria, "#95a5a6")
        gerar_foto_produto(nome, cor, caminho)
        print(f"✅ {arquivo}")


def main():
    """Função principal"""
    print("\n" + "=" * 80)
    print("  📸 GERAÇÃO DE FOTOS DE TESTE - PROJETO OBRATTO")
    print("=" * 80)

    try:
        # Garantir que os diretórios existem
        DIRETORIO_USUARIOS.mkdir(parents=True, exist_ok=True)
        DIRETORIO_PRODUTOS.mkdir(parents=True, exist_ok=True)

        # Gerar fotos
        gerar_todas_fotos_usuarios()
        gerar_todas_fotos_produtos()

        print("\n" + "=" * 80)
        print("  ✨ FOTOS GERADAS COM SUCESSO!")
        print("=" * 80)
        print(f"\n  📁 Fotos de usuários: {DIRETORIO_USUARIOS}")
        print(f"  📁 Fotos de produtos: {DIRETORIO_PRODUTOS}\n")

        return 0

    except Exception as e:
        print(f"\n❌ Erro ao gerar fotos: {e}")
        import traceback
        print(traceback.format_exc())
        return 1


if __name__ == "__main__":
    exit(main())
