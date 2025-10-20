"""
Teste de inscrição de plano
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.plano import plano_repo
from data.inscricaoplano import inscricao_plano_repo
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano

def test_inscricao():
    print("=== Teste de Inscrição de Plano ===")
    
    # Listar planos disponíveis
    planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=10)
    print(f"Planos disponíveis: {len(planos)}")
    
    if not planos:
        print("Nenhum plano encontrado!")
        return
    
    # Testar inscrição
    id_fornecedor = 1
    plano_escolhido = planos[0]
    
    print(f"Testando inscrição do fornecedor {id_fornecedor} no plano {plano_escolhido.nome_plano}")
    
    # Verificar se já tem assinatura
    assinatura_existente = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    print(f"Assinatura existente: {assinatura_existente is not None}")
    
    if assinatura_existente:
        print(f"Plano atual: ID {assinatura_existente.id_plano}")
        # Deletar assinatura existente para teste
        id_inscricao = assinatura_existente.id_inscricao_plano
        assert id_inscricao is not None
        inscricao_plano_repo.deletar_inscricao_plano(id_inscricao)
        print("Assinatura existente removida para teste")
    
    # Criar nova inscrição
    id_plano_escolhido = plano_escolhido.id_plano
    assert id_plano_escolhido is not None
    nova_inscricao = InscricaoPlano(
        id_inscricao_plano=0,
        id_fornecedor=id_fornecedor,
        id_prestador=None,
        id_plano=id_plano_escolhido
    )
    
    try:
        inscricao_id = inscricao_plano_repo.inserir_inscricao_plano(nova_inscricao)
        print(f"Nova inscrição criada com ID: {inscricao_id}")
        
        # Verificar se foi salva
        assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
        if assinatura_ativa:
            print(f"✅ Inscrição salva com sucesso!")
            print(f"   ID Inscrição: {assinatura_ativa.id_inscricao_plano}")
            print(f"   ID Plano: {assinatura_ativa.id_plano}")
            print(f"   ID Fornecedor: {assinatura_ativa.id_fornecedor}")
        else:
            print("❌ Erro: Inscrição não foi encontrada após inserção")
            
    except Exception as e:
        print(f"❌ Erro ao inserir inscrição: {e}")

if __name__ == "__main__":
    test_inscricao()
