from contextlib import contextmanager
import sqlite3
import sys
import os
from data.usuario.usuario_repo import*
from data.usuario.usuario_model import Usuario

class TestUsuarioRepo:
    def test_criar_tabela_usuario(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela_usuario()
        #Assert
        assert resultado == True,"A criação da tabela deveria retornar True"

    def test_inserir_usuario(self, test_db):
        #Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0,"Usuario Teste", "email", "senha", "12345678901", "99999999999", "88888-888", "Rua Teste", "123", "", "Bairro Teste", "Cidade Teste", "ES", "cliente", "2023-10-01 12:00:00")
        #Act
        id_usuario_inserido = inserir_usuario(usuario_teste)
        #Assert
        assert id_usuario_inserido is not None
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None, "A categoria inserida não deveria ser None"
        assert id_usuario_inserido is not None
        assert usuario_db.id == id_usuario_inserido, "O ID do usuário inserido não confere com o ID retornado"
        assert usuario_db.nome == "Usuario Teste", "O nome do usuário inserido não confere"

    def test_atualizar_usuario(self, test_db):
        #Arrange
        criar_tabela_usuario()
        usuario_teste = Usuario(0,"Usuario Teste", "email", "senha", "12345678901", "99999999999", "88888-888", "Rua Teste", "123", "", "Bairro Teste", "Cidade Teste", "ES", "cliente", "2023-10-01 12:00:00")
        id_usuario_inserido = inserir_usuario(usuario_teste)
        assert id_usuario_inserido is not None
        usuario_inserido = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_inserido is not None
        #Act
        usuario_inserido.nome = "Usuario Atualizado"
        resultado = atualizar_usuario(usuario_inserido)
        #Assert
        assert resultado == True, "A alteração do usuário deveria retornar True"
        assert id_usuario_inserido is not None
        usuario_db = obter_usuario_por_id(id_usuario_inserido)
        assert usuario_db is not None
        assert usuario_db.nome == "Usuario Atualizado", "O nome do usuário alterado não confere"

    def test_obter_usuario_por_email(self, test_db):
            # Arrange
            criar_tabela_usuario()
            email_unico = "email_unico_para_teste@email.com"
            usuario_teste = Usuario(0, "Usuario Unico", email_unico, "senha", "11122233344", "77777777777", "88888-888", "Rua Teste", "123", "", "Bairro Teste", "Cidade Teste", "ES", "cliente", datetime.now().isoformat())
            inserir_usuario(usuario_teste)
            # Act
            usuario_db = obter_usuario_por_email(email_unico)
            # Assert
            assert usuario_db is not None, "Deveria ter encontrado um usuário com o email especificado"
            assert usuario_db.email == email_unico

    def test_obter_usuario_por_id(self, test_db):
        # Arrange
        criar_tabela_usuario()
        email_unico = "id_test@email.com"
        usuario_original = Usuario(
            id=0,
            nome="Usuario ID Test",
            email=email_unico,
            senha="senha_id",
            cpf_cnpj="55544433322",
            telefone="11222334455",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="cliente",
            data_cadastro=datetime.now().isoformat()
        )
        id_inserido = inserir_usuario(usuario_original)
        # Act
        assert id_inserido is not None
        usuario_encontrado = obter_usuario_por_id(id_inserido)
        # Assert
        assert usuario_encontrado is not None, "A busca por ID não deveria retornar None"
        assert id_inserido is not None
        assert usuario_encontrado.id == id_inserido, "O ID do usuário encontrado não corresponde ao ID inserido"
        assert usuario_encontrado.email == email_unico, "O email do usuário encontrado não corresponde ao original"
        assert usuario_encontrado.nome == "Usuario ID Test", "O nome do usuário encontrado não corresponde ao original"

    def test_obter_usuarios_por_pagina(self, test_db):
            # Arrange
            criar_tabela_usuario()
            for i in range(1, 16):
                usuario = Usuario(
                    id=0,
                    nome=f"Usuario {i}",
                    email=f"usuario{i}@email.com",
                    senha="senha",
                    cpf_cnpj=f"000000000{i:02d}",
                    telefone=f"999999999{i:02d}",
                    cep="88888-888",
                    rua=f"Rua {i}",
                    numero="123",
                    complemento="",
                    bairro="Bairro Teste",
                    cidade="Cidade Teste",
                    estado="ES",
                    tipo_usuario="1",
                    data_cadastro=datetime.now().isoformat()
                )
                inserir_usuario(usuario)
            # Act
            pagina_1 = obter_usuarios_por_pagina(pg_num=1, pg_size=5)
            # Assert
            assert len(pagina_1) == 5, "A primeira página deveria ter 5 usuários"
            assert pagina_1[0].nome == "Usuario 1", "O primeiro usuário da página 1 está incorreto"
            assert pagina_1[4].nome == "Usuario 5", "O último usuário da página 1 está incorreto"
            # Act
            pagina_2 = obter_usuarios_por_pagina(pg_num=2, pg_size=5)
            # Assert
            assert len(pagina_2) == 5, "A segunda página deveria ter 5 usuários"
            assert pagina_2[0].nome == "Usuario 6", "O primeiro usuário da página 2 está incorreto"
            assert pagina_2[4].nome == "Usuario 10", "O último usuário da página 2 está incorreto"
            # Act
            pagina_3 = obter_usuarios_por_pagina(pg_num=3, pg_size=5)
            # Assert
            assert len(pagina_3) == 5, "A terceira página deveria ter 5 usuários (os últimos 5)"
            assert pagina_3[0].nome == "Usuario 11", "O primeiro usuário da página 3 está incorreto"
            assert pagina_3[4].nome == "Usuario 15", "O último usuário da página 3 está incorreto"
            # Act
            pagina_4 = obter_usuarios_por_pagina(pg_num=4, pg_size=5)
            # Assert
            assert len(pagina_4) == 0, "A quarta página deveria estar vazia"
            

    def test_atualizar_tipo_usuario(self, test_db):
        criar_tabela_usuario()
        usuario_original = Usuario(
            id=0,
            nome="Usuario de Teste de Tipo",
            email="tipo@teste.com",
            senha="123",
            cpf_cnpj="987654321",
            telefone="555444333",
            cep="88888-888",
            rua="Rua Teste",
            numero="123",
            complemento="",
            bairro="Bairro Teste",
            cidade="Cidade Teste",
            estado="ES",
            tipo_usuario="Cliente",
            data_cadastro=datetime.now().isoformat()
        )
        id_inserido = inserir_usuario(usuario_original)
        assert id_inserido is not None and id_inserido > 0, "Falha ao inserir usuário para o teste."
        novo_tipo = "Administrador"
        #ACT
        resultado_da_atualizacao = atualizar_tipo_usuario(
            usuario_id=id_inserido,
            tipo_usuario=novo_tipo
        )
        # ASSERT 
        assert resultado_da_atualizacao is True, "A função deveria retornar True para uma atualização bem-sucedida."
        usuario_do_banco = obter_usuario_por_id(id_inserido)
        assert usuario_do_banco is not None
        assert usuario_do_banco.tipo_usuario == novo_tipo, \
            f"O tipo do usuário deveria ser '{novo_tipo}', mas foi encontrado '{usuario_do_banco.tipo_usuario}'."

    def test_atualizar_senha_usuario(self, test_db):
            criar_tabela_usuario()
            senha_antiga = "senha123"
            usuario_original = Usuario(
                id=0,
                nome="Usuario Senha Teste",
                email="senha@teste.com",
                senha=senha_antiga,
                cpf_cnpj="192837465",
                telefone="11223344",
                cep="88888-888",
                rua="Rua Teste",
                numero="123",
                complemento="",
                bairro="Bairro Teste",
                cidade="Cidade Teste",
                estado="ES",
                tipo_usuario="Cliente",
                data_cadastro=datetime.now().isoformat()
            )
            id_inserido = inserir_usuario(usuario_original)
            assert id_inserido is not None, "Falha ao inserir usuário de teste."
            #ARRANGE
            nova_senha = "senhaSuperSegura456"
            #ACT 
            resultado = atualizar_senha_usuario(
                usuario_id=id_inserido,
                nova_senha=nova_senha
            )
            #ASSERT 
            assert resultado is True, "A função de atualizar senha deveria retornar True."
            usuario_do_banco = obter_usuario_por_id(id_inserido)
            assert usuario_do_banco is not None
            assert usuario_do_banco.senha == nova_senha, "A senha no banco de dados não foi atualizada corretamente."
            assert usuario_do_banco.senha != senha_antiga, "A senha no banco ainda é a senha antiga."

    def test_deletar_um_usuario(self, test_db):
            criar_tabela_usuario()
            usuario_para_deletar = Usuario(
                id=0,
                nome="Usuario a Ser Deletado",
                email="deletar@teste.com",
                senha="senha_temp",
                cpf_cnpj="000000000",
                telefone="00000000",
                cep="88888-888",
                rua="Rua Teste",
                numero="123",
                complemento="",
                bairro="Bairro Teste",
                cidade="Cidade Teste",
                estado="ES",
                tipo_usuario="Excluido",
                data_cadastro=datetime.now().isoformat()
            )
            id_inserido = inserir_usuario(usuario_para_deletar)
            assert id_inserido is not None, "Falha ao inserir o usuário que seria deletado."
            usuario_existe = obter_usuario_por_id(id_inserido)
            assert usuario_existe is not None, "O usuário não foi encontrado no banco antes de tentar deletar."
            resultado = deletar_usuario(usuario_id=id_inserido)
            assert resultado is True, "A função de deletar deveria retornar True."
            usuario_nao_deve_existir = obter_usuario_por_id(id_inserido)
            assert usuario_nao_deve_existir is None, "O usuário ainda foi encontrado no banco de dados após a deleção."
