#!/usr/bin/env python3
"""
Script de Migração de Schema - Projeto OBRATTO

Adiciona colunas faltantes nas tabelas existentes.

TODO ALUNOS: Entender migração de banco de dados
- Por que schemas mudam durante o desenvolvimento?
- Como adicionar colunas sem perder dados?
- Por que não dropar e recriar em produção?

Uso: python scripts/migrar_schema.py
"""

import sys
import os

# Adicionar o diretório pai ao sys.path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)
sys.path.insert(0, projeto_dir)

from util.db import open_connection

def verificar_coluna_existe(cursor, tabela: str, coluna: str) -> bool:
    """Verifica se uma coluna existe em uma tabela"""
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = cursor.fetchall()
    nomes_colunas = [col[1] for col in colunas]
    return coluna in nomes_colunas

def migrar_schema():
    """Adiciona colunas faltantes"""
    print("\n🔧 Migrando schema do banco de dados...\n")

    migracoes = []

    with open_connection() as conn:
        cursor = conn.cursor()

        # Migração 1: Adicionar selo_confianca em prestador
        if not verificar_coluna_existe(cursor, "prestador", "selo_confianca"):
            cursor.execute("ALTER TABLE prestador ADD COLUMN selo_confianca INTEGER DEFAULT 0")
            migracoes.append("✅ Coluna 'selo_confianca' adicionada em 'prestador'")

        # Migração 2: Adicionar selo_confianca em fornecedor (se necessário)
        try:
            if not verificar_coluna_existe(cursor, "fornecedor", "selo_confianca"):
                cursor.execute("ALTER TABLE fornecedor ADD COLUMN selo_confianca INTEGER DEFAULT 0")
                migracoes.append("✅ Coluna 'selo_confianca' adicionada em 'fornecedor'")
        except:
            pass  # Tabela pode não ter essa coluna no modelo

        conn.commit()

    if migracoes:
        print("Migrações aplicadas:")
        for msg in migracoes:
            print(f"  {msg}")
    else:
        print("ℹ️  Nenhuma migração necessária - schema está atualizado")

    print("\n✨ Schema atualizado com sucesso!\n")

if __name__ == "__main__":
    migrar_schema()
