import pytest
import sqlite3
from datetime import datetime
from data.produto.produto_model import Produto
from data.produto import produto_repo
from data.produto.produto_repo import atualizar_produto, criar_tabela_produto, deletar_produto, inserir_produto, obter_produto_por_id, obter_produto_por_pagina


@pytest.fixture
def produto_exemplo():
    return Produto(id=1, nome="Produto Teste", descricao="Descrição do produto teste", preco=19.9, quantidade=5)


class TestProdutoRepo:

    def test_criar_tabela_produto(self, test_db):
        criar_tabela_produto()
        assert True

    def test_inserir_produto(self, test_db, produto_exemplo):
        criar_tabela_produto()
        inserir_produto(produto_exemplo)
        produto_bd = obter_produto_por_id(produto_exemplo.id)
        assert produto_bd is not None
        assert produto_bd.nome == produto_exemplo.nome
        assert produto_bd.descricao == produto_exemplo.descricao
        assert produto_bd.preco == produto_exemplo.preco
        assert produto_bd.quantidade == produto_exemplo.quantidade

    def test_obter_produto_por_id(self, test_db, produto_exemplo):
        criar_tabela_produto()
        inserir_produto(produto_exemplo)
        produto = obter_produto_por_id(produto_exemplo.id)
        assert produto is not None
        assert produto.id == produto_exemplo.id
        assert produto.nome == "Produto Teste"

    def test_obter_produto_por_pagina(self, test_db):
        criar_tabela_produto()

        # Insere 5 produtos
        for i in range(5):
            produto = Produto(id=i+1, nome=f"Produto {i+1}", descricao="Desc", preco=10.0*(i+1), quantidade=2*(i+1))
            inserir_produto(produto)
        
        produtos_pagina1 = obter_produto_por_pagina(limit=3, offset=0)
        produtos_pagina2 = obter_produto_por_pagina(limit=3, offset=3)
        assert len(produtos_pagina1) == 3
        assert len(produtos_pagina2) == 2
        assert produtos_pagina1[0].id == 1
        assert produtos_pagina2[0].id == 4

    def test_atualizar_produto(self, test_db, produto_exemplo):
        criar_tabela_produto()
        inserir_produto(produto_exemplo)

        produto_para_atualizar = obter_produto_por_id(produto_exemplo.id)
        assert produto_para_atualizar is not None
        produto_para_atualizar.nome = "Nome Atualizado"
        produto_para_atualizar.preco = 29.9
        produto_para_atualizar.descricao = "Novo"
        produto_para_atualizar.quantidade = 10
        sucesso = atualizar_produto(produto_para_atualizar)
        produto_atualizado_db = obter_produto_por_id(produto_exemplo.id)
        assert sucesso is None or sucesso is True
        assert produto_atualizado_db is not None
        assert produto_atualizado_db.nome == "Nome Atualizado"
        assert produto_atualizado_db.preco == 29.9
        assert produto_atualizado_db.descricao == "Novo"
        assert produto_atualizado_db.quantidade == 10

    def test_deletar_produto(self, test_db, produto_exemplo):
        criar_tabela_produto()
        inserir_produto(produto_exemplo)

        produto_db_antes = obter_produto_por_id(produto_exemplo.id)
        assert produto_db_antes is not None

        deletar_produto(produto_exemplo.id)
        produto_db_depois = obter_produto_por_id(produto_exemplo.id)
        
        assert produto_db_depois is None




