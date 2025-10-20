import sqlite3
import pytest
import uuid
from datetime import datetime
from data.prestador.prestador_model import Prestador
from data.prestador.prestador_repo import (
    criar_tabela_prestador,
    inserir_prestador,
    obter_prestador,
    obter_prestador_por_id,
    atualizar_prestador,
    deletar_prestador_repo,
    obter_prestador_por_pagina,
)
from data.usuario.usuario_repo import criar_tabela_usuario

@pytest.fixture
def prestador_exemplo(email_unico, cpf_unico):
    return Prestador(
        id=0,
        nome="Prestador Teste",
        email=email_unico,
        senha="senhaSuperForte123",
        cpf_cnpj=cpf_unico,
        telefone="27999887766",
        cep="88888-888",
        rua="Rua Teste",
        numero="123",
        complemento="",
        bairro="Bairro Teste",
        cidade="Cidade Teste",
        estado="ES",
        tipo_usuario="prestador",
        data_cadastro=datetime.now().isoformat(),
        area_atuacao="Tecnologia",
        razao_social="Prestadora de Serviços de Teste Ltda",
        descricao_servicos="Desenvolvimento e testes de software."
    )

class TestPrestadorRepo:

    def test_criar_tabela_prestador(self, test_db):
        # Arrange
        criar_tabela_usuario()
        # Act
        criar_tabela_prestador()
        # Assert
        assert True

    def test_inserir_prestador(self, test_db, prestador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_prestador()
        # Act
        id_inserido = inserir_prestador(prestador_exemplo)
        # Assert
        assert id_inserido is not None
        assert id_inserido > 0
        assert id_inserido is not None
        prestador_db = obter_prestador_por_id(id_inserido)
        assert prestador_db is not None
        assert prestador_db.nome == prestador_exemplo.nome
        assert prestador_db.razao_social == prestador_exemplo.razao_social

    def test_obter_prestador(self, test_db, prestador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_prestador()
        id_inserido = inserir_prestador(prestador_exemplo)
        # Act
        prestadores = obter_prestador()
        # Assert
        assert len(prestadores) == 1
        assert prestadores[0].id == id_inserido
        assert prestadores[0].nome == "Prestador Teste"

    def test_obter_prestador_por_id(self, test_db, prestador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_prestador()
        id_inserido = inserir_prestador(prestador_exemplo)
        # Act
        assert id_inserido is not None
        prestador_db = obter_prestador_por_id(id_inserido)
        # Assert
        assert prestador_db is not None
        assert prestador_db.id == id_inserido
        assert prestador_db.email == prestador_exemplo.email

    def test_obter_prestador_por_pagina(self, test_db):
            # Arrange
            criar_tabela_usuario()
            criar_tabela_prestador()

            for i in range(15):
                email_temp = f"prestador_{i}_{uuid.uuid4().hex[:8]}@teste.com"
                cpf_temp = f"{i:014d}"
                prestador = Prestador(
                    id=0,
                    nome=f"Prestador Teste {i}",
                    email=email_temp,
                    senha="senha123",
                    cpf_cnpj=cpf_temp,
                    telefone="27999999999",
                    cep="88888-888",
                    rua="Rua Teste",
                    numero="123",
                    complemento="",
                    bairro="Bairro Teste",
                    cidade="Cidade Teste",
                    estado="ES",
                    tipo_usuario="prestador",
                    data_cadastro=datetime.now().isoformat(),
                    area_atuacao="Serviços",
                    razao_social="prestador Ltda",
                    descricao_servicos="Prestação de serviços em tecnologia."
                )
                inserir_prestador(prestador)
            with sqlite3.connect(test_db) as conn:
                prestador_pagina_1 = obter_prestador_por_pagina(conn, limit=10, offset=0)
                prestador_pagina_2 = obter_prestador_por_pagina(conn, limit=10, offset=10)
                prestador_pagina_3 = obter_prestador_por_pagina(conn, limit=10, offset=20)
            # Assert
            assert len(prestador_pagina_1) == 10, "A primeira página deveria conter 10 prestadores"
            assert len(prestador_pagina_2) == 5, "A segunda página deveria conter os 5 prestadores restantes"
            assert len(prestador_pagina_3) == 0, "A terceira página não deveria conter nenhum prestador"
            # Opcional
            ids_pagina_1 = {f.id for f in prestador_pagina_1}
            ids_pagina_2 = {f.id for f in prestador_pagina_2}
            assert ids_pagina_1.isdisjoint(ids_pagina_2), "Os prestadores da página 1 não devem se repetir na página 2"


    def test_atualizar_prestador(self, test_db, prestador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_prestador()
        id_inserido = inserir_prestador(prestador_exemplo)
        assert id_inserido is not None

        prestador_para_atualizar = obter_prestador_por_id(id_inserido)
        assert prestador_para_atualizar is not None
        prestador_para_atualizar.nome = "Nome Atualizado"
        prestador_para_atualizar.area_atuacao = "Engenharia"
        prestador_para_atualizar.descricao_servicos = "Serviços de engenharia de software."
        # Act
        sucesso = atualizar_prestador(prestador_para_atualizar)
        assert id_inserido is not None
        prestador_atualizado_db = obter_prestador_por_id(id_inserido)
        # Assert
        assert sucesso is True
        assert prestador_atualizado_db is not None
        assert prestador_atualizado_db.nome == "Nome Atualizado"
        assert prestador_atualizado_db.area_atuacao == "Engenharia"
        assert prestador_atualizado_db.descricao_servicos == "Serviços de engenharia de software."

    def test_deletar_prestador(self, test_db, prestador_exemplo):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_prestador()
        id_inserido = inserir_prestador(prestador_exemplo)
        assert id_inserido is not None

        prestador_db_antes = obter_prestador_por_id(id_inserido)
        assert prestador_db_antes is not None
        # Act
        assert id_inserido is not None
        sucesso = deletar_prestador_repo(id_inserido)
        assert id_inserido is not None
        prestador_db_depois = obter_prestador_por_id(id_inserido)
        # Assert
        assert sucesso is True
        assert prestador_db_depois is None
