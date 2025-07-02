import sys
import os
from data.fornecedor.fornecedor_model import *
from data.fornecedor.fornecedor_repo import *
from data.inscricaoplano.inscricao_plano_repo import *
from data.plano.plano_model import Plano
from data.plano.plano_repo import *
from data.prestador.prestador_model import Prestador
from data.prestador.prestador_repo import *
from data.usuario.usuario_repo import *

class Test_InscricaoPlanoRepo:
   
    def test_criar_tabela_inscricao_plano(self, test_db):
        criar_tabela_plano()
        criar_tabela_prestador()
        criar_tabela_fornecedor()
        resultado = criar_tabela_inscricao_plano()
        assert resultado is True, "A criação da tabela deveria retornar True"

    
    def test_inserir_inscricao_plano(self, test_db):
        criar_tabela_plano()
        criar_tabela_prestador()
        criar_tabela_fornecedor()
        criar_tabela_inscricao_plano()

        id_fornecedor = 1
        id_prestador = 2
        id_plano = 3

        inscricao_plano_teste = InscricaoPlano(
            id_fornecedor=id_fornecedor,
            id_prestador=id_prestador,
            id_plano=id_plano
        )

        # Act
        id_inscricao = inserir_inscricao_plano(inscricao_plano_teste)
        assert id_inscricao is not None

        inscricao_plano_db = obter_inscricao_plano_por_id(id_inscricao)
        assert inscricao_plano_db is not None
        assert inscricao_plano_db.id_fornecedor

    def test_obter_inscricao_plano(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_plano()
        criar_tabela_prestador()
        criar_tabela_inscricao_plano()

        fornecedor = Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678000199",
            telefone="27999999999",
            data_cadastro="2023-01-01",
            endereco="Rua dos Fornecedores",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA"
        )
        id_fornecedor = inserir_fornecedor(fornecedor)
        assert id_fornecedor is not None, "Fornecedor não foi inserido"

        plano = Plano(
            nome_plano="Plano Básico",
            valor_mensal="49.90",
            limite_servico=0,
            tipo_plano="Básico",
            descricao="Descrição do plano"
        )
        id_plano = inserir_plano(plano)
        assert id_plano is not None, "Plano não foi inserido"

        id_usuario = inserir_usuario(Usuario(
            id=0,
            nome="Maria Prestadora",
            email="maria@prestadora.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01"
        ))
        assert id_usuario is not None, "Usuário não foi inserido"

        prestador = Prestador(
            id=id_usuario,
            nome="Maria Prestadora",
            email="maria@prestadora.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01",
            area_atuacao="Serviços gerais",
            tipo_pessoa="Física",
            razao_social="",
            descricao_servicos="Serviços de limpeza"
        )

        id_prestador = inserir_prestador(prestador)
        assert id_prestador is not None, "Prestador não foi inserido"

    def test_obter_inscricao_plano_por_id(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_prestador()
        criar_tabela_plano()
        criar_tabela_inscricao_plano()
    
        id_fornecedor = inserir_fornecedor(Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678000199",
            telefone="27999999999",
            data_cadastro="2023-01-01",
            endereco="Rua dos Fornecedores",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA"
        ))
        assert id_fornecedor is not None
        
        id_usuario = inserir_usuario(Usuario(
            id=0,
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01"
        ))
        assert id_usuario is not None
        
        id_prestador = inserir_prestador(Prestador(
            id=id_usuario,  
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01",
            area_atuacao="Serviços gerais",
            tipo_pessoa="Física",
            razao_social="",
            descricao_servicos="Serviços de limpeza"
        ))
        assert id_prestador is not None
        
        id_plano = inserir_plano(Plano(
            nome_plano="Plano Básico",
            valor_mensal=49.90,
            limite_servico=0,
            tipo_plano="Básico",
            descricao="Descrição do plano"
        ))
        assert id_plano is not None
        
        inscricao_teste = InscricaoPlano(
            id_inscricao_plano=None,
            id_fornecedor=id_fornecedor,
            id_prestador=id_prestador,
            id_plano=id_plano
        )
        id_inserido = inserir_inscricao_plano(inscricao_teste)
        assert id_inserido is not None
        
        inscricao_obtida = obter_inscricao_plano_por_id(id_inserido)
        assert inscricao_obtida is not None
        assert inscricao_obtida.id_inscricao_plano == id_inserido
        assert inscricao_obtida.id_fornecedor == inscricao_teste.id_fornecedor
        assert inscricao_obtida.id_prestador == inscricao_teste.id_prestador
        assert inscricao_obtida.id_plano == inscricao_teste.id_plano

    def test_obter_inscricao_plano_por_pagina(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_prestador()
        criar_tabela_plano()
        criar_tabela_inscricao_plano()

        # Inserindo dados de base
        id_fornecedor = inserir_fornecedor(Fornecedor(
            id=0,
            nome="Fornecedor Paginado",
            email="fornecedor@pagina.com",
            senha="senha123",
            cpf_cnpj="12345678000100",
            telefone="27999990000",
            data_cadastro="2023-01-01",
            endereco="Rua Paginada",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA"
        ))

        id_usuario = inserir_usuario(Usuario(
            id=0,
            nome="Prestador Paginado",
            email="prestador@pagina.com",
            senha="senha123",
            cpf_cnpj="11122233300",
            telefone="27988880000",
            endereco="Rua dos Paginadores",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01"
        ))

        id_prestador = inserir_prestador(Prestador(
            id=id_usuario,
            nome="Prestador Paginado",
            email="prestador@pagina.com",
            senha="senha123",
            cpf_cnpj="11122233300",
            telefone="27988880000",
            endereco="Rua dos Paginadores",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01",
            area_atuacao="Serviços",
            tipo_pessoa="Física",
            razao_social="",
            descricao_servicos="Serviços gerais"
        ))

        id_plano = inserir_plano(Plano(
            nome_plano="Plano Paginado",
            valor_mensal=59.90,
            limite_servico=10,
            tipo_plano="Premium",
            descricao="Descrição do plano paginado"
        ))

        # Inserindo várias inscrições
        for i in range(10):
            inserir_inscricao_plano(InscricaoPlano(
                id_inscricao_plano=None,
                id_fornecedor=id_fornecedor,
                id_prestador=id_prestador,
                id_plano=id_plano
            ))

        # Página 1 com tamanho 5
        pagina_1 = obter_inscricao_plano_por_pagina(pagina=1, tamanho_pagina=5)
        assert isinstance(pagina_1, list)
        assert len(pagina_1) == 5

        # Página 2 com tamanho 5
        pagina_2 = obter_inscricao_plano_por_pagina(pagina=2, tamanho_pagina=5)
        assert isinstance(pagina_2, list)
        assert len(pagina_2) == 5

        # Página 3 (deve estar vazia)
        pagina_3 = obter_inscricao_plano_por_pagina(pagina=3, tamanho_pagina=5)
        assert isinstance(pagina_3, list)
        assert len(pagina_3) == 0


    def test_atualizar_inscricao_plano(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_prestador()
        criar_tabela_plano()
        criar_tabela_inscricao_plano()

        id_fornecedor = inserir_fornecedor(Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678000199",
            telefone="27999999999",
            data_cadastro="2023-01-01",
            endereco="Rua dos Fornecedores",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA"
        ))

        id_usuario = inserir_usuario(Usuario(
            id=0,
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01"
        ))

        id_prestador = inserir_prestador(Prestador(
            id=id_usuario, 
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01",
            area_atuacao="Serviços gerais",
            tipo_pessoa="Física",
            razao_social="",
            descricao_servicos="Serviços de limpeza"
        ))

        id_plano = inserir_plano(Plano(
            nome_plano="Plano Básico",
            valor_mensal=49.90,
            limite_servico=0,
            tipo_plano="Básico",
            descricao="Descrição do plano"
        ))

        inscricao_original = InscricaoPlano(
            id_inscricao_plano=None,
            id_fornecedor=id_fornecedor,
            id_prestador=id_prestador,
            id_plano=id_plano
        )
        id_inscricao = inserir_inscricao_plano(inscricao_original)
        assert id_inscricao is not None

        inscricao_atualizada = InscricaoPlano(
            id_inscricao_plano=id_inscricao,
            id_fornecedor=id_fornecedor,
            id_prestador=id_prestador,
            id_plano=id_plano 
        )

        sucesso = atualizar_inscricao_plano(inscricao_atualizada)
        assert sucesso is True

        inscricao_db = obter_inscricao_plano_por_id(id_inscricao)
        assert inscricao_db is not None
        assert inscricao_db.id_plano == inscricao_atualizada.id_plano

    def test_deletar_inscricao_plano(self, test_db):
        criar_tabela_usuario()
        criar_tabela_fornecedor()
        criar_tabela_prestador()
        criar_tabela_plano()
        criar_tabela_inscricao_plano()

        id_fornecedor = inserir_fornecedor(Fornecedor(
            id=0,
            nome="Fornecedor Teste",
            email="fornecedor@teste.com",
            senha="senha123",
            cpf_cnpj="12345678000199",
            telefone="27999999999",
            data_cadastro="2023-01-01",
            endereco="Rua dos Fornecedores",
            tipo_usuario="Fornecedor",
            razao_social="Fornecedor LTDA"
        ))
        id_usuario = inserir_usuario(Usuario(
            id=0,
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01"
        ))
        id_prestador = inserir_prestador(Prestador(
            id=id_usuario, 
            nome="Prestador Teste",
            email="prestador@teste.com",
            senha="senha123",
            cpf_cnpj="11122233344",
            telefone="27988887777",
            endereco="Rua das Prestadoras",
            tipo_usuario="Prestador",
            data_cadastro="2023-01-01",
            area_atuacao="Serviços gerais",
            tipo_pessoa="Física",
            razao_social="",
            descricao_servicos="Serviços de limpeza"
        ))
        id_plano = inserir_plano(Plano(
            nome_plano="Plano Básico",
            valor_mensal=49.90,
            limite_servico=0,
            tipo_plano="Básico",
            descricao="Descrição do plano"
        ))

        inscricao = InscricaoPlano(
            id_inscricao_plano=None,
            id_fornecedor=id_fornecedor,
            id_prestador=id_prestador,
            id_plano=id_plano
        )
        id_inscricao = inserir_inscricao_plano(inscricao)
        assert id_inscricao is not None

        sucesso = deletar_inscricao_plano(id_inscricao)
        assert sucesso is True

        inscricao_db = obter_inscricao_plano_por_id(id_inscricao)
        assert inscricao_db is None


