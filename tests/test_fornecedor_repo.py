from datetime import datetime
import sqlite3
from data.fornecedor.fornecedor_repo import (
    criar_tabela_fornecedor,
    inserir_fornecedor,
    obter_fornecedor,
    obter_fornecedor_por_id,
    atualizar_fornecedor,
    deletar_fornecedor,
    obter_fornecedor_por_pagina
)
from data.fornecedor.fornecedor_model import Fornecedor
from data.usuario.usuario_repo import criar_tabela_usuario


class TestFornecedorRepo:
    def test_criar_tabela_fornecedor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        # Act
        resultado = criar_tabela_fornecedor()
        # Assert
        assert resultado is True, "A criação da tabela fornecedor deveria retornar True"

    def test_inserir_fornecedor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@email.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="27999999999",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="fornecedor",
            data_cadastro=datetime.now().isoformat(),
            razao_social="Fornecedor Ltda"
        )
        # Act
        id_inserido = inserir_fornecedor(fornecedor)
        # Assert
        assert id_inserido is not None
        fornecedor_db = obter_fornecedor_por_id(id_inserido)
        assert fornecedor_db is not None, "O fornecedor inserido não deveria ser None"
        assert fornecedor_db.nome == "Fornecedor Teste", "O nome do fornecedor inserido não confere"
        assert fornecedor_db.email == "fornecedor@email.com"

    def test_obter_fornecedor(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        
        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@email.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="27999999999",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="fornecedor",
            data_cadastro=datetime.now().isoformat(),
            razao_social="Fornecedor Ltda"
        )
        inserir_fornecedor(fornecedor)

        fornecedores = obter_fornecedor()

        assert len(fornecedores) > 0, "Deveria haver pelo menos um fornecedor"


    def test_obter_fornecedor_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()      
        criar_tabela_fornecedor()
        
        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@email.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="27999999999",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="fornecedor",
            data_cadastro=datetime.now().isoformat(),
            razao_social="Fornecedor Ltda"
        )
        #Act
        id_inserido = inserir_fornecedor(fornecedor)
        assert id_inserido is not None
        fornecedor_bd = obter_fornecedor_por_id(id_inserido)

        # Assert
        assert fornecedor_bd is not None, "Deveria retornar um fornecedor"
        assert fornecedor_bd.id == id_inserido, "ID do fornecedor retornado deve ser igual ao inserido"
        assert fornecedor_bd.nome == "Fornecedor Teste"
        assert fornecedor_bd.email == "fornecedor@email.com"
        assert fornecedor_bd.tipo_usuario == "fornecedor"
        assert fornecedor_bd.razao_social == "Fornecedor Ltda"

    def test_obter_fornecedor_por_pagina(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_fornecedor()

        for i in range(15):
            fornecedor = Fornecedor(
                id=0,
                nome="Fornecedor Teste",
                email="fornecedor@email.com",
                senha="senha123",
                cpf_cnpj="12345678900",
                telefone="27999999999",
                cep="88888-888",
                rua="Rua Teste",
                numero="123",
                complemento="",
                bairro="Bairro Teste",
                cidade="Cidade Teste",
                estado="ES",
                tipo_usuario="fornecedor",
                data_cadastro=datetime.now().isoformat(),
                razao_social="Fornecedor Ltda"
            )
            inserir_fornecedor(fornecedor)
        with sqlite3.connect(test_db) as conn:
            fornecedor_pagina_1 = obter_fornecedor_por_pagina(conn, limit=10, offset=0)
            fornecedor_pagina_2 = obter_fornecedor_por_pagina(conn,limit=10,offset=10)
            fornecedor_pagina_3 = obter_fornecedor_por_pagina(conn,limit=10, offset=20)
        # Assert
        assert len(fornecedor_pagina_1) == 10, "A primeira página deveria conter 10 fornecedores"
        assert len(fornecedor_pagina_2) == 5, "A segunda página deveria conter os 5 fornecedor restantes"
        assert len(fornecedor_pagina_3) == 0, "A terceira página não deveria conter nenhum fornecedor"
        # Opcional
        ids_pagina_1 = {f.id for f in fornecedor_pagina_1}
        ids_pagina_2 = {f.id for f in fornecedor_pagina_2}
        assert ids_pagina_1.isdisjoint(ids_pagina_2), "Os fornecedores da página 1 não devem se repetir na página 2"

    def test_atualizar_fornecedor(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_fornecedor()

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@email.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="27999999999",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="fornecedor",
            data_cadastro=datetime.now().isoformat(),
            razao_social="Fornecedor Ltda"
        )

        id_inserido = inserir_fornecedor(fornecedor)
        assert id_inserido is not None
        fornecedor_db = obter_fornecedor_por_id(id_inserido)
        assert fornecedor_db is not None

        fornecedor_db.nome = "Fornecedor Atualizado"
        fornecedor_db.razao_social = "Razão Atualizada"

        # Act
        resultado = atualizar_fornecedor(fornecedor_db)

        # Assert
        assert resultado is True, "A atualização do fornecedor deveria retornar True"

        atualizado = obter_fornecedor_por_id(id_inserido)
        assert atualizado is not None
        assert atualizado.nome == "Fornecedor Atualizado"
        assert atualizado.razao_social == "Razão Atualizada"


    def test_deletar_fornecedor(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@email.com",
            senha="senha123",
            cpf_cnpj="12345678900",
            telefone="27999999999",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="fornecedor",
            data_cadastro=datetime.now().isoformat(),
            razao_social="Fornecedor Ltda"
        )
        id_inserido = inserir_fornecedor(fornecedor)
        assert id_inserido is not None

        fornecedor_bd = obter_fornecedor_por_id(id_inserido)
        assert fornecedor_bd is not None

        resultado = deletar_fornecedor(id_inserido)
        assert resultado is True

        fornecedor_apos = obter_fornecedor_por_id(id_inserido)
        assert fornecedor_apos is None

