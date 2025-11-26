from datetime import datetime, date, timedelta
import pytest
import uuid

from data.usuario.usuario_model import Usuario
from data.usuario.usuario_repo import criar_tabela_usuario, inserir_usuario

from data.fornecedor.fornecedor_model import Fornecedor
from data.fornecedor.fornecedor_repo import criar_tabela_fornecedor, inserir_fornecedor

from data.cliente.cliente_model import Cliente
from data.cliente.cliente_repo import criar_tabela_cliente, inserir_cliente

from data.orcamento.orcamento_model import Orcamento
from data.orcamento.orcamento_repo import (
    criar_tabela_orcamento,
    deletar_orcamento,
    inserir_orcamento,
    obter_orcamento_por_id,
    obter_orcamentos_por_pagina,
    obter_todos_orcamentos,
    atualizar_orcamento_por_id
)


class Test_OrcamentoRepo:
    def test_criar_tabela_orcamento(self, test_db):
        criar_tabela_usuario() 
        criar_tabela_fornecedor()
        criar_tabela_cliente()
        resultado = criar_tabela_orcamento()
        assert resultado is True, "A criação da tabela deveria retornar True"

    def test_inserir_orcamento(self, test_db, email_unico, cpf_unico):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_cliente()
        criar_tabela_orcamento()

        email_fornecedor = f"fornecedor_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_fornecedor = f"{uuid.uuid4().int % 100000000000000:014d}"

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email=email_fornecedor,
            senha="senha123",
            cpf_cnpj=cpf_fornecedor,
            telefone="27999999999",
            data_cadastro=datetime.now().isoformat(),
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Centro",
            cidade="Vitória",
            estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None, "Fornecedor não inserido"

        cliente = Cliente(
            id=0,
            nome="Cliente Teste",
            email=email_unico,
            senha="senha123",
            cpf_cnpj=cpf_unico,
            telefone="27988887777",
            data_cadastro=datetime.now().isoformat(),
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Centro",
            cidade="Vitória",
            estado="ES",
            tipo_usuario="Cliente",
            genero="feminino",
            data_nascimento=date(2000, 1, 1)
        )
        id_cliente = inserir_cliente(cliente)
        assert id_cliente is not None, "Cliente não inserido"

        assert id_fornecedor is not None
        assert id_cliente is not None
        orcamento = Orcamento(
            id=0,
            id_fornecedor=id_fornecedor,
            id_cliente=id_cliente,
            valor_estimado=1500.00,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=7),
            status="Pendente",
            descricao="Serviço de pintura"
)
        id_orcamento = inserir_orcamento(orcamento)
        assert id_orcamento is not None, "Orçamento não foi inserido com sucesso"

    def test_obter_todos_orcamentos(self, test_db):
        criar_tabela_orcamento()

        orc1 = Orcamento(
            id=0,
            id_fornecedor=1,
            id_cliente=3,
            valor_estimado=1000,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=15),
            status="Confirmado",
            descricao="Orçamento 1"
)
        inserir_orcamento(orc1)

        orc2 = Orcamento(
            id=0,
            id_fornecedor=2,
            id_cliente=4,
            valor_estimado=2000,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=45),
            status="Pendente",
            descricao="Orçamento 2"
)
        inserir_orcamento(orc2)

        orcamentos = obter_todos_orcamentos()
        assert isinstance(orcamentos, list)
        assert len(orcamentos) >= 2

    def test_obter_orcamento_por_id(self, test_db, email_unico, cpf_unico):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_cliente()
        criar_tabela_orcamento()

        email_fornecedor = f"fornecedor_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_fornecedor = f"{uuid.uuid4().int % 100000000000000:014d}"

        fornecedor = Fornecedor(
            id=0, nome="Fornecedor", email=email_fornecedor, senha="123", cpf_cnpj=cpf_fornecedor, telefone="111",
            data_cadastro=datetime.now().isoformat(), tipo_usuario="Fornecedor", razao_social="Fornecedor Ltda",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        cliente = Cliente(
            id=0,
            nome="Usuário C",
            email=email_unico,
            senha="123",
            cpf_cnpj=cpf_unico,
            telefone="222",
            data_cadastro=datetime.now().isoformat(),
            tipo_usuario="Cliente",
            genero="Feminino",
            data_nascimento=date(2000, 1, 1),
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_cliente = inserir_cliente(cliente)

        assert id_fornecedor is not None
        assert id_cliente is not None
        orcamento = Orcamento(
            id=0,
            id_fornecedor=id_fornecedor,
            id_cliente=id_cliente,
            valor_estimado=2500.0,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=5),
            status="Em análise",
            descricao="Teste de obter por ID"
        )
        id_orc = inserir_orcamento(orcamento)

        assert id_orc is not None
        orc_db = obter_orcamento_por_id(id_orc)
        assert orc_db is not None
        assert orc_db.id == id_orc
        assert orc_db.descricao == "Teste de obter por ID"
        assert orc_db.status == "Em análise"

    def test_obter_orcamentos_por_pagina(self, test_db):
        criar_tabela_orcamento()

        # Inserir múltiplos orçamentos fictícios
        for i in range(10):
            orc = Orcamento(
                id=0,
                id_fornecedor=1,
                id_cliente=2,
                valor_estimado=1000 + i * 100,
                data_solicitacao=datetime.now(),
                prazo_entrega=datetime.now() + timedelta(days=10 + i),
                status="Status {}".format(i),
                descricao="Descrição {}".format(i)
            )
            inserir_orcamento(orc)

        # Página 1, 5 resultados
        orcs_pagina_1 = obter_orcamentos_por_pagina(1, 5)
        assert len(orcs_pagina_1) == 5
        assert orcs_pagina_1[0].descricao.startswith("Descrição")

        # Página 2, 5 resultados
        orcs_pagina_2 = obter_orcamentos_por_pagina(2, 5)
        assert len(orcs_pagina_2) == 5
        assert orcs_pagina_2[0].descricao != orcs_pagina_1[0].descricao

        # Página 3, deve retornar vazio (só tem 10 registros)
        orcs_pagina_3 = obter_orcamentos_por_pagina(3, 5)
        assert len(orcs_pagina_3) == 0



    def test_atualizar_orcamento_por_id(self, test_db, email_unico, cpf_unico):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_cliente()
        criar_tabela_orcamento()

        email_fornecedor = f"fornecedor_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_fornecedor = f"{uuid.uuid4().int % 100000000000000:014d}"

        fornecedor = Fornecedor(
            id=0, nome="F", email=email_fornecedor, senha="1", cpf_cnpj=cpf_fornecedor, telefone="1",
            data_cadastro=datetime.now().isoformat(), tipo_usuario="Fornecedor", razao_social="F LTDA",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)

        cliente = Cliente(
            id=0,
            nome="C",
            email=email_unico,
            senha="2",
            cpf_cnpj=cpf_unico,
            telefone="2",
            data_cadastro=datetime.now().isoformat(),
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Centro",
            cidade="Vitória",
            estado="ES",
            tipo_usuario="Cliente",
            genero="Feminino",
            data_nascimento=date(2000, 1, 1)
        )
        id_cliente = inserir_cliente(cliente)

        assert id_fornecedor is not None
        assert id_cliente is not None
        orcamento = Orcamento(
            id=0,
            id_fornecedor=id_fornecedor,
            id_cliente=id_cliente,
            valor_estimado=1000,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=3),
            status="Pendente",
            descricao="..."
        )

        id_orcamento = inserir_orcamento(orcamento)

        assert id_orcamento is not None
        orcamento_atualizado = Orcamento(
            id=id_orcamento,
            id_fornecedor=id_fornecedor,
            id_cliente=id_cliente,
            valor_estimado=1200,
            data_solicitacao=orcamento.data_solicitacao,
            prazo_entrega=datetime.now() + timedelta(days=2),
            status="Aprovado",
            descricao="Atualizado"
        )
        
        sucesso = atualizar_orcamento_por_id(orcamento_atualizado)
        assert sucesso is True

        atualizado = obter_orcamento_por_id(id_orcamento)
        assert atualizado is not None
        assert atualizado.valor_estimado == 1200.0
        assert atualizado.status == "Aprovado"
        assert "Atualizado" in atualizado.descricao

    def test_deletar_orcamento(self, test_db):
        criar_tabela_orcamento()

        orcamento = Orcamento(
            id=0,
            id_fornecedor=5,
            id_cliente=6,
            valor_estimado=4000,
            data_solicitacao=datetime.now(),
            prazo_entrega=datetime.now() + timedelta(days=10),
            status="Cancelado",
            descricao="Orçamento a deletar"
        )
        id_orc = inserir_orcamento(orcamento)

        assert id_orc is not None
        sucesso = deletar_orcamento(id_orc)
        assert sucesso is True

        orc_db = obter_orcamento_por_id(id_orc)
        assert orc_db is None


   