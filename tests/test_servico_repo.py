import sqlite3
from data.servico.servico_repo import (
    criar_tabela_servico,
    inserir_servico,
    obter_servico,      
    obter_servico_por_id,
    atualizar_servico,
    deletar_servico,
    obter_servico_por_pagina
)
from data.servico.servico_model import Servico
from data.usuario.usuario_model import Usuario
from data.usuario.usuario_repo import criar_tabela_usuario, inserir_usuario
from data.prestador.prestador_repo import criar_tabela_prestador, inserir_prestador
from data.prestador.prestador_model import Prestador
from datetime import datetime


class TestServicoRepo:

    
    def criar_usuario_prestador(self):
        criar_tabela_usuario()
        criar_tabela_prestador()

        usuario = Usuario(
            id=0,
            nome="Prestador Teste",
            email="teste@teste.com",
            senha="123456",
            cpf_cnpj="12345678900",
            telefone="999999999",
            endereco="Rua Exemplo, 123",
            tipo_usuario="prestador", 
            data_cadastro=datetime.now().isoformat()
        )

        id_usuario = inserir_usuario(usuario)

        prestador = Prestador(
            id=id_usuario, 
            nome=usuario.nome,
            email=usuario.email,
            senha=usuario.senha,
            cpf_cnpj=usuario.cpf_cnpj,
            telefone=usuario.telefone,
            data_cadastro=usuario.data_cadastro,
            endereco=usuario.endereco,
            tipo_usuario=usuario.tipo_usuario,
            area_atuacao="TI",
            tipo_pessoa="Física",
            razao_social=None,
            descricao_servicos=None
        )
        id_prestador = inserir_prestador(prestador)

        return id_prestador

    def test_criar_tabela_servico(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        resultado = criar_tabela_servico()
        assert resultado is True, "A criação da tabela servico deveria retornar True"
    
    def test_inserir_servico(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        criar_tabela_servico()
        id_prestador = self.criar_usuario_prestador()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço Teste",
            descricao="Descrição do serviço",
            categoria="TI",
            valor_base=150.0
        )

        id_inserido = inserir_servico(servico)
        servico_db = obter_servico_por_id(id_inserido)

        print("ID inserido:", id_inserido)
        print("ID prestador usado:", id_prestador)

        assert servico_db is not None
        assert servico_db.titulo == "Serviço Teste"
        assert servico_db.valor_base == 150.0

    def test_obter_servico(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        criar_tabela_servico()
        id_prestador = self.criar_usuario_prestador()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço Lista",
            descricao="Descrição listagem",
            categoria="Design",
            valor_base=200.0
        )
        inserir_servico(servico)

        lista = obter_servico()
        assert len(lista) > 0
        assert any(s.titulo == "Serviço Lista" for s in lista)

    def test_obter_servico_por_id(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        criar_tabela_servico()
        id_prestador = self.criar_usuario_prestador()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço Único",
            descricao="Busca única",
            categoria="Marketing",
            valor_base=120.0
        )
        id_inserido = inserir_servico(servico)
        resultado = obter_servico_por_id(id_inserido)

        assert resultado is not None
        assert resultado.titulo == "Serviço Único"
        assert resultado.valor_base == 120.0

    def test_obter_servico_por_pagina(self, test_db):
        # Arrange
        criar_tabela_usuario()
        criar_tabela_servico()
        criar_tabela_prestador()
        id_prestador = self.criar_usuario_prestador()

        for i in range(15):
            servico = Servico(
                id_servico=0,
                id_prestador=id_prestador,
                titulo="Serviço Único",
                descricao="Busca única",
                categoria="Marketing",
                valor_base=120.0
            )
            inserir_servico(servico)

        with sqlite3.connect(test_db) as conn:
            servico_pagina_1 = obter_servico_por_pagina(conn, limit=10, offset=0)
            servico_pagina_2 = obter_servico_por_pagina(conn,limit=10,offset=10)
            servico_pagina_3 = obter_servico_por_pagina(conn,limit=10, offset=20)

        # Assert
        assert len(servico_pagina_1) == 10, "A primeira página deveria conter 10 serviços"
        assert len(servico_pagina_2) == 5, "A segunda página deveria conter os 5 serviços restantes"
        assert len(servico_pagina_3) == 0, "A terceira página não deveria conter nenhum serviço"
        # Opcional
        ids_pagina_1 = {s.id_servico for s in servico_pagina_1}
        ids_pagina_2 = {s.id_servico for s in servico_pagina_2}
        assert ids_pagina_1.isdisjoint(ids_pagina_2), "Os serviços da página 1 não devem se repetir na página 2"
        assert id_prestador is not None

    def test_atualizar_servico(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        criar_tabela_servico()
        id_prestador = self.criar_usuario_prestador()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço Antigo",
            descricao="Descrição antiga",
            categoria="TI",
            valor_base=100.0
        )
        id_servico = inserir_servico(servico)

        servico_atualizado = Servico(
            id_servico=id_servico,
            id_prestador=id_prestador,
            titulo="Serviço Novo",
            descricao="Nova descrição",
            categoria="TI",
            valor_base=300.0
        )

        resultado = atualizar_servico(servico_atualizado)
        assert resultado is True

        atualizado = obter_servico_por_id(id_servico)
        assert atualizado.titulo == "Serviço Novo"
        assert atualizado.valor_base == 300.0

    def test_deletar_servico(self, test_db):
        criar_tabela_usuario()
        criar_tabela_prestador()
        criar_tabela_servico()
        id_prestador = self.criar_usuario_prestador()

        servico = Servico(
            id_servico=0,
            id_prestador=id_prestador,
            titulo="Serviço Deletável",
            descricao="Descrição",
            categoria="TI",
            valor_base=90.0
        )
        id_servico = inserir_servico(servico)

        resultado = deletar_servico(id_servico)
        assert resultado is True

        apagado = obter_servico_por_id(id_servico)
        assert apagado is None