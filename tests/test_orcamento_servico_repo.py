import sqlite3
import uuid
from data.servico.servico_model import Servico
from data.servico.servico_repo import criar_tabela_servico, inserir_servico
from data.usuario.usuario_model import Usuario
from utils.db import open_connection
import pytest
from datetime import datetime, date
from data.usuario.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.cliente.cliente_model import Cliente
from data.cliente.cliente_repo import criar_tabela_cliente, inserir_cliente
from data.prestador.prestador_model import Prestador
from data.prestador.prestador_repo import criar_tabela_prestador, inserir_prestador
from data.orcamentoservico.orcamento_servico_model import OrcamentoServico
from data.orcamentoservico.orcamento_servico_repo import (
    criar_tabela_orcamento_servico,
    inserir_orcamento_servico,
    obter_orcamento_servico,
    obter_orcamento_servico_por_id,
    atualizar_orcamento_servico,
    deletar_orcamento_servico,
    obter_orcamento_servico_por_pagina
)
class TestOrcamentoServicoRepo:

    def test_criar_tabela_orcamento_servico(self,test_db):
        #Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        #Act
        resultado = criar_tabela_orcamento_servico()
        #Assert
        assert resultado is True

    def inserir_orcamento_para_teste(self, email_cliente, cpf_cliente, email_prestador, cpf_prestador) -> int:
        #Arrange
        cliente = Cliente(
            id=0,
            nome="Cliente Teste",
            email=email_cliente,
            senha="123",
            cpf_cnpj=cpf_cliente,
            telefone="11999999999",
            data_cadastro=datetime.now().isoformat(),
            cep="12345-678",
            rua="Rua Cliente",
            numero="123",
            complemento="",
            bairro="Centro",
            cidade="São Paulo",
            estado="SP",
            tipo_usuario="cliente",
            genero="Masculino",
            data_nascimento=date(1990, 1, 1)
        )
        id_cliente = inserir_cliente(cliente)
        assert id_cliente is not None

        prestador = Prestador(
            id=0,
            nome="Prestador Teste",
            email=email_prestador,
            senha="123",
            cpf_cnpj=cpf_prestador,
            telefone="21999999999",
            data_cadastro=datetime.now().isoformat(),
            cep="98765-432",
            rua="Rua Prestador",
            numero="456",
            complemento="",
            bairro="Vila Nova",
            cidade="Rio de Janeiro",
            estado="RJ",
            tipo_usuario="prestador",
            area_atuacao="Jardinagem",
            razao_social=None,
            descricao_servicos="Serviços de jardinagem"
        )
        id_prestador = inserir_prestador(prestador)
        assert id_prestador is not None

        assert id_cliente is not None

        orcamento = OrcamentoServico(
            id_orcamento=0,
            id_servico=1,
            id_prestador=id_prestador,
            id_cliente=id_cliente,
            valor_estimado=150.0,
            data_solicitacao=date.today(),
            prazo_entrega=date.today(),
            status="Pendente",
            descricao="Orçamento para jardinagem",
        )

        criar_tabela_servico()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço de Jardinagem",
            descricao="Cuidar do jardim",
            categoria="Jardinagem",
            valor_base=100.0
        )
        id_servico = inserir_servico(servico)
        # Act
        id_orcamento = inserir_orcamento_servico(orcamento)
        # Assert
        assert id_orcamento is not None
        return id_orcamento

    def test_inserir_orcamento_servico(self, test_db, email_unico, cpf_unico):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        criar_tabela_orcamento_servico()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"
        # Act
        id_orcamento = self.inserir_orcamento_para_teste(email_unico, cpf_unico, email_prestador, cpf_prestador)
        orcamento_db = obter_orcamento_servico_por_id(id_orcamento)
        # Assert
        assert orcamento_db is not None
        assert orcamento_db.id_orcamento == id_orcamento

    def test_obter_orcamento_servico(self, test_db, email_unico, cpf_unico):
        # Arrange
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DROP TABLE IF EXISTS orcamento_servico")
            cursor.execute("DROP TABLE IF EXISTS prestador")
            cursor.execute("DROP TABLE IF EXISTS cliente")
            cursor.execute("DROP TABLE IF EXISTS usuario")

        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        criar_tabela_orcamento_servico()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"
        # Act
        id_orcamento = self.inserir_orcamento_para_teste(email_unico, cpf_unico, email_prestador, cpf_prestador)
        orcamentos = obter_orcamento_servico()
        # Assert
        assert any(o.id_orcamento == id_orcamento for o in orcamentos)

    def test_obter_orcamento_por_id(self, test_db, email_unico, cpf_unico):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        criar_tabela_orcamento_servico()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"
        # Act
        id_orcamento = self.inserir_orcamento_para_teste(email_unico, cpf_unico, email_prestador, cpf_prestador)
        orcamento = obter_orcamento_servico_por_id(id_orcamento)
        # Assert
        assert orcamento is not None
        assert isinstance(orcamento.descricao, str)

    def test_obter_orcamento_servico_por_pagina(self, test_db, email_unico, cpf_unico):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_orcamento_servico()
        criar_tabela_servico()
        criar_tabela_cliente()
        criar_tabela_prestador()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"

        prestador = Prestador(
            id=0,
            nome="Prestador Teste",
            email=email_prestador,
            senha="123",
            cpf_cnpj=cpf_prestador,
            telefone="27999999999",
            tipo_usuario="prestador",
            data_cadastro=datetime.now().isoformat(),
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES",
            area_atuacao="Geral",
            razao_social=None,
            descricao_servicos="Serviços gerais"
        )

        cliente = Cliente(
            id=0,
            nome="Cliente Teste",
            email=email_unico,
            senha="456",
            cpf_cnpj=cpf_unico,
            telefone="27988888888",
            tipo_usuario="cliente",
            data_cadastro=datetime.now().isoformat(),
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES",
            genero="Masculino",
            data_nascimento=date(1990, 1, 1)
        )

        id_prestador = inserir_prestador(prestador)
        id_cliente = inserir_cliente(cliente)

        assert id_prestador is not None
        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço de Jardinagem",
            descricao="Cuidar do jardim",
            categoria="Jardinagem",
            valor_base=100.0
        )
        id_servico = inserir_servico(servico)

        assert id_prestador is not None
        assert id_cliente is not None
        assert id_servico is not None
        for i in range(15):
            orcamento_servico = OrcamentoServico(
                id_orcamento=0,
                id_servico=id_servico,
                id_prestador=id_prestador,
                id_cliente=id_cliente,
                valor_estimado=150.0,
                data_solicitacao=date.today(),
                prazo_entrega=date.today(),
                status="Pendente",
                descricao="Orçamento para serviço de jardinagem")

            inserir_orcamento_servico(orcamento_servico)
        with sqlite3.connect(test_db) as conn:
            orcamento_servico_pagina_1 = obter_orcamento_servico_por_pagina(conn, limit=10, offset=0)
            orcamento_servico_pagina_2 = obter_orcamento_servico_por_pagina(conn,limit=10,offset=10)
            orcamento_servico_pagina_3 = obter_orcamento_servico_por_pagina(conn,limit=10, offset=20)
        # Assert
        assert len(orcamento_servico_pagina_1) == 10, "A primeira página deveria conter 10 orçamentos de serviços"
        assert len(orcamento_servico_pagina_2) == 5, "A segunda página deveria conter os 5 orçamentos de serviços restantes"
        assert len(orcamento_servico_pagina_3) == 0, "A terceira página não deveria conter nenhum orçamento de serviço"
        # Opcional
        ids_pagina_1 = {os.id_orcamento for os in orcamento_servico_pagina_1}
        ids_pagina_2 = {os.id_orcamento for os in orcamento_servico_pagina_2}
        assert ids_pagina_1.isdisjoint(ids_pagina_2), "Os orcamento_servicoes da página 1 não devem se repetir na página 2"

    def test_atualizar_orcamento_servico(self, test_db, email_unico, cpf_unico):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        criar_tabela_orcamento_servico()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"
        # Act
        id_orcamento = self.inserir_orcamento_para_teste(email_unico, cpf_unico, email_prestador, cpf_prestador)
        orcamento = obter_orcamento_servico_por_id(id_orcamento)
        assert orcamento is not None
        orcamento.status = "Concluído"
        resultado = atualizar_orcamento_servico(orcamento)
        # Assert
        assert resultado is True

    def test_deletar_orcamento_servico(self, test_db, email_unico, cpf_unico):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_cliente()
        criar_tabela_prestador()
        criar_tabela_orcamento_servico()

        email_prestador = f"prestador_{uuid.uuid4().hex[:8]}@teste.com"
        cpf_prestador = f"{uuid.uuid4().int % 100000000000000:014d}"
        # Act
        id_orcamento = self.inserir_orcamento_para_teste(email_unico, cpf_unico, email_prestador, cpf_prestador)
        resultado = deletar_orcamento_servico(id_orcamento)
        # Assert
        assert resultado is True