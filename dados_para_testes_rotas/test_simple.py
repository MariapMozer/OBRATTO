"""
Teste simples das funções de plano
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.plano import plano_repo
from data.inscricaoplano import inscricao_plano_repo
from data.pagamento.pagamento_repo import PagamentoRepository

def test_functions():
    print("Testando funções...")
    
    # Testar obter planos
    planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=10)
    print(f"Planos encontrados: {len(planos)}")
    
    for plano in planos:
        print(f"- {plano.nome_plano}: R$ {plano.valor_mensal}")
    
    # Testar obter plano por ID
    if planos:
        id_plano = planos[0].id_plano
        assert id_plano is not None
        primeiro_plano = plano_repo.obter_plano_por_id(id_plano)
        print(f"Primeiro plano: {primeiro_plano.nome_plano if primeiro_plano else 'Não encontrado'}")
    
    print("Testes concluídos!")

if __name__ == "__main__":
    test_functions()
