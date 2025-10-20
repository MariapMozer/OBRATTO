from datetime import datetime, date
import sqlite3
from data.cliente.cliente_repo import (
    criar_tabela_cliente,
    inserir_cliente,
    obter_cliente,
    obter_cliente_por_id,
    atualizar_cliente,
    deletar_cliente,
    obter_cliente_por_pagina,
)
from data.cliente.cliente_model import Cliente
from data.usuario.usuario_repo import criar_tabela_usuario

class TestClienteRepo:

    def test_criar_tabela_cliente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        # Act
        resultado = criar_tabela_cliente()
        # Assert
        assert resultado is True, "A criação da tabela cliente deveria retornar True"

    def test_inserir_cliente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_novo = Cliente(
            id=0,
            nome="Maria Silva",
            email="maria.silva@email.com",
            senha="senhaforte123",
            cpf_cnpj="111.222.333-44",
            telefone="27988887777",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="2",
            data_cadastro=datetime.now().isoformat(),
            genero="Feminino",
            data_nascimento=date(1995, 10, 25)
        )
        # Act
        id_inserido = inserir_cliente(cliente_novo)
        # Assert
        assert id_inserido is not None
        cliente_db = obter_cliente_por_id(id_inserido)
        assert cliente_db is not None, "O cliente inserido não deveria ser None"
        assert cliente_db.nome == "Maria Silva"
        assert cliente_db.genero == "Feminino"
        assert cliente_db.data_nascimento == date(1995, 10, 25)

    def test_obter_todos_os_clientes(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_1 = Cliente(id=0, nome="Cliente A", email="a@a.com", senha="123", cpf_cnpj="1", telefone="1", cep="88888-888", rua="Rua A", numero="1", complemento="", bairro="Bairro A", cidade="Cidade A", estado="ES", tipo_usuario="2", data_cadastro=datetime.now().isoformat(), genero="M", data_nascimento=date(2001, 1, 1))
        cliente_2 = Cliente(id=0, nome="Cliente B", email="b@b.com", senha="456", cpf_cnpj="2", telefone="2", cep="88888-888", rua="Rua B", numero="2", complemento="", bairro="Bairro B", cidade="Cidade B", estado="ES", tipo_usuario="2", data_cadastro=datetime.now().isoformat(), genero="F", data_nascimento=date(2002, 2, 2))
        inserir_cliente(cliente_1)
        inserir_cliente(cliente_2)
        # Act
        lista_clientes = obter_cliente()
        # Assert
        assert len(lista_clientes) == 2, "A lista deveria conter dois clientes"
        assert lista_clientes[0].nome == "Cliente A"
        assert lista_clientes[1].nome == "Cliente B"

    def test_obter_cliente_por_pagina(self, test_db):
            # Arrange
            criar_tabela_usuario()
            criar_tabela_cliente()

            for i in range(15):
                cliente = Cliente(
                    id=0,
                    nome="Cliente Teste",
                    email="cliente@email.com",
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
                    tipo_usuario="cliente",
                    data_cadastro=datetime.now().isoformat(),
                    genero="Masculino",
                    data_nascimento=date(1990, 1, 1)
                )
                inserir_cliente(cliente)
            with sqlite3.connect(test_db) as conn:
                cliente_pagina_1 = obter_cliente_por_pagina(conn, limit=10, offset=0)
                cliente_pagina_2 = obter_cliente_por_pagina(conn,limit=10,offset=10)
                cliente_pagina_3 = obter_cliente_por_pagina(conn,limit=10, offset=20)
            # Assert
            assert len(cliente_pagina_1) == 10, "A primeira página deveria conter 10 clientes"
            assert len(cliente_pagina_2) == 5, "A segunda página deveria conter os 5 clientes restantes"
            assert len(cliente_pagina_3) == 0, "A terceira página não deveria conter nenhum cliente"
            # Opcional
            ids_pagina_1 = {f.id for f in cliente_pagina_1}
            ids_pagina_2 = {f.id for f in cliente_pagina_2}
            assert ids_pagina_1.isdisjoint(ids_pagina_2), "Os clientes da página 1 não devem se repetir na página 2"

    def test_atualizar_cliente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_original = Cliente(
            id=0,
            nome="João Santos",
            email="joao.santos@email.com",
            senha="senhaoriginal",
            cpf_cnpj="444.555.666-77",
            telefone="27977776666",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="2",
            data_cadastro=datetime.now().isoformat(),
            genero="Masculino",
            data_nascimento=date(1980, 1, 15)
        )
        id_inserido = inserir_cliente(cliente_original)
        assert id_inserido is not None
        cliente_para_atualizar = obter_cliente_por_id(id_inserido)
        assert cliente_para_atualizar is not None
        cliente_para_atualizar.nome = "João da Silva Santos"
        cliente_para_atualizar.genero = "Outro"
        cliente_para_atualizar.rua = "Endereço Novo"
        cliente_para_atualizar.numero = "100"
        # Act
        resultado = atualizar_cliente(cliente_para_atualizar)
        # Assert
        assert resultado is True, "A atualização deveria retornar True"
        cliente_atualizado_db = obter_cliente_por_id(id_inserido)
        assert cliente_atualizado_db is not None
        assert cliente_atualizado_db.nome == "João da Silva Santos"
        assert cliente_atualizado_db.genero == "Outro"
        assert cliente_atualizado_db.rua == "Endereço Novo"
        assert cliente_atualizado_db.numero == "100"

    def test_deletar_cliente(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        cliente_para_deletar = Cliente(id=0, nome="Cliente Temporário", email="temp@temp.com", senha="123", cpf_cnpj="0", telefone="0", cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Bairro Teste", cidade="Cidade Teste", estado="ES", tipo_usuario="2", data_cadastro=datetime.now().isoformat(), genero="N/A", data_nascimento=date(2000, 1, 1))
        id_inserido = inserir_cliente(cliente_para_deletar)
        assert id_inserido is not None
        assert obter_cliente_por_id(id_inserido) is not None
        # Act
        resultado = deletar_cliente(id_inserido)
        # Assert
        assert resultado is True, "A deleção deveria retornar True"
        assert id_inserido is not None
        cliente_apos_delecao = obter_cliente_por_id(id_inserido)
        assert cliente_apos_delecao is None, "O cliente deveria ser None após a deleção"