#!/usr/bin/env python3
"""
Script de Limpeza do Banco de Dados - Projeto OBRATTO

Este script REMOVE TODOS OS DADOS do banco de dados, mantendo apenas a estrutura das tabelas.

TODO ALUNOS: Entender importância de scripts de limpeza
- Útil para reset completo do ambiente de desenvolvimento
- NUNCA use em produção!
- Sempre faça backup antes de usar

Uso: python scripts/limpar_banco.py

⚠️  ATENÇÃO: Este script é DESTRUTIVO! Use com cuidado!
"""

import sys
import os

# Adicionar o diretório pai ao sys.path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)
sys.path.insert(0, projeto_dir)

from util.db import open_connection

# ==============================================================================
# CONFIGURAÇÕES
# ==============================================================================

EMOJI_ALERTA = "⚠️"
EMOJI_SUCESSO = "✅"
EMOJI_INFO = "ℹ️"
EMOJI_ERRO = "❌"


def print_header(titulo: str):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f"  {titulo}")
    print("=" * 80)


def print_alerta(mensagem: str):
    """Imprime mensagem de alerta"""
    print(f"{EMOJI_ALERTA} {mensagem}")


def print_sucesso(mensagem: str):
    """Imprime mensagem de sucesso"""
    print(f"{EMOJI_SUCESSO} {mensagem}")


def print_info(mensagem: str):
    """Imprime mensagem informativa"""
    print(f"{EMOJI_INFO} {mensagem}")


def print_erro(mensagem: str):
    """Imprime mensagem de erro"""
    print(f"{EMOJI_ERRO} {mensagem}")


def confirmar_acao() -> bool:
    """
    Solicita confirmação do usuário antes de prosseguir

    TODO ALUNOS: Observe:
    - Sempre pedir confirmação para ações destrutivas
    - Usar input() para interação com usuário
    - Validar entrada do usuário
    """
    print(f"\n{EMOJI_ALERTA} {EMOJI_ALERTA} {EMOJI_ALERTA} ATENÇÃO {EMOJI_ALERTA} {EMOJI_ALERTA} {EMOJI_ALERTA}")
    print("\nEsta ação irá APAGAR TODOS OS DADOS do banco de dados!")
    print("As tabelas serão mantidas, mas todos os registros serão removidos.")
    print("\nEsta ação NÃO PODE SER DESFEITA!")

    resposta = input("\nDeseja continuar? Digite 'SIM' para confirmar: ")

    return resposta.strip().upper() == "SIM"


def limpar_tabelas():
    """
    Remove todos os dados das tabelas, respeitando a ordem de dependências

    TODO ALUNOS: Observe a ordem de exclusão:
    1. Tabelas com chaves estrangeiras PRIMEIRO
    2. Tabelas referenciadas POR ÚLTIMO
    3. Por que essa ordem é necessária? (Integridade referencial)
    """
    print_header("LIMPANDO BANCO DE DADOS")

    # Ordem de exclusão (respeitando dependências - chaves estrangeiras)
    tabelas_ordem = [
        # 1. Tabelas que dependem de múltiplas outras (mais dependências)
        "orcamento_servico",
        "inscricao_plano",
        "avaliacao",
        "mensagem",
        "notificacao",
        "orcamento",

        # 2. Tabelas que dependem de usuários específicos
        "produto",  # depende de fornecedor
        "servico",  # depende de prestador
        "anuncio",

        # 3. Tabelas de tipos de usuários
        "administrador",
        "cliente",
        "prestador",
        "fornecedor",

        # 4. Tabelas independentes ou com poucas dependências
        "plano",

        # 5. Tabela base (por último, pois outros dependem dela)
        "usuario",
    ]

    total_registros_removidos = 0

    try:
        with open_connection() as conn:
            cursor = conn.cursor()

            for tabela in tabelas_ordem:
                try:
                    # Conta registros antes de excluir
                    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                    count_antes = cursor.fetchone()
                    if count_antes:
                        count = count_antes[0]
                    else:
                        count = 0

                    if count > 0:
                        # Exclui todos os registros
                        cursor.execute(f"DELETE FROM {tabela}")
                        conn.commit()

                        total_registros_removidos += count
                        print_sucesso(f"Tabela '{tabela}' limpa ({count} registros removidos)")
                    else:
                        print_info(f"Tabela '{tabela}' já está vazia")

                except Exception as e:
                    print_alerta(f"Aviso ao limpar '{tabela}': {e}")
                    # Continua mesmo se houver erro em uma tabela
                    continue

        return total_registros_removidos

    except Exception as e:
        print_erro(f"Erro ao limpar banco de dados: {e}")
        import traceback
        print(traceback.format_exc())
        return -1


def main():
    """
    Função principal
    """
    print("\n")
    print("=" * 80)
    print("  🗑️  LIMPEZA DO BANCO DE DADOS - PROJETO OBRATTO")
    print("=" * 80)

    # Solicita confirmação
    if not confirmar_acao():
        print(f"\n{EMOJI_INFO} Operação cancelada pelo usuário.")
        print("Nenhum dado foi removido.\n")
        return 0

    # Executa limpeza
    print("\n")
    total_removidos = limpar_tabelas()

    if total_removidos >= 0:
        print_header("RESUMO DA LIMPEZA")
        print(f"\n{EMOJI_SUCESSO} Limpeza concluída com sucesso!")
        print(f"\n  📊 Total de registros removidos: {total_removidos}")
        print("\n  ℹ️  As tabelas foram mantidas (apenas dados removidos)")
        print("\n  📝 Próximos passos:")
        print("    ➜ Para popular novamente: python scripts/popular_banco.py")
        print("    ➜ Ou crie dados manualmente via interface web\n")
    else:
        print_erro("\nErro durante a limpeza do banco.")
        return 1

    print("=" * 80)
    print("  ✨ BANCO DE DADOS LIMPO!")
    print("=" * 80)
    print()

    return 0


if __name__ == "__main__":
    exit(main())
