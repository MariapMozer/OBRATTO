#!/usr/bin/env python3
"""
Script para minificar o CSS de componentes
Uso: python scripts/minify_css.py
"""

import re
from pathlib import Path

def minify_css(css_content):
    """
    Minifica CSS removendo comentários, espaços em branco desnecessários
    e quebras de linha.
    """
    # Remover comentários /* ... */
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

    # Remover espaços em branco múltiplos
    css_content = re.sub(r'\s+', ' ', css_content)

    # Remover espaços ao redor de { } : ; , >
    css_content = re.sub(r'\s*([{};:,>])\s*', r'\1', css_content)

    # Remover espaço antes de !important
    css_content = re.sub(r'\s*!important', '!important', css_content)

    # Remover último ;  antes de }
    css_content = re.sub(r';}', '}', css_content)

    # Remover espaços ao redor de operadores em calc()
    css_content = re.sub(r'calc\s*\(\s*', 'calc(', css_content)

    return css_content.strip()


def main():
    # Caminhos
    project_root = Path(__file__).parent.parent
    css_file = project_root / 'static' / 'css' / 'components.css'
    min_file = project_root / 'static' / 'css' / 'components.min.css'

    print(f"📦 Minificando CSS...")
    print(f"   Origem: {css_file}")
    print(f"   Destino: {min_file}")

    # Ler arquivo original
    if not css_file.exists():
        print(f"❌ Erro: Arquivo {css_file} não encontrado!")
        return 1

    with open(css_file, 'r', encoding='utf-8') as f:
        original_content = f.read()

    original_size = len(original_content)

    # Minificar
    minified_content = minify_css(original_content)
    minified_size = len(minified_content)

    # Calcular redução
    reduction = ((original_size - minified_size) / original_size) * 100

    # Adicionar header
    header = f"""/*! Components CSS - Obratto | Minified | {minified_size} bytes | Reduction: {reduction:.1f}% */
"""
    final_content = header + minified_content

    # Escrever arquivo minificado
    with open(min_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"✅ Minificação completa!")
    print(f"   Tamanho original: {original_size:,} bytes")
    print(f"   Tamanho minificado: {minified_size:,} bytes")
    print(f"   Redução: {reduction:.1f}%")

    return 0


if __name__ == '__main__':
    exit(main())
