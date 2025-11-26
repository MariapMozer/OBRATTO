from contextlib import contextmanager
import sqlite3
import sys
import os
from datetime import datetime

import pytest
from data.administrador.administrador_repo import*
from data.administrador.administrador_model import Administrador
from data.usuario.usuario_model import Usuario
from data.usuario.usuario_repo import criar_tabela_usuario, inserir_usuario, obter_usuario_por_id

class TestAdministradorRepo:

    def test_criar_tabela_administrador(self, test_db):
        #Arrange
        #Act
        resultado = criar_tabela_administrador()
        #Assert
        assert resultado == True,"A criação da tabela deveria retornar True"

    def test_inserir_administrador(self, test_db):
            # Arrange
            criar_tabela_usuario()
            criar_tabela_administrador()
            usuario_base = Usuario(
                id=0,
                nome="Admin Chefe",
                email="chefe@obratto.com",
                senha="senha_chefe",
                cpf_cnpj="10101010101",
                telefone="28999998888",
                data_cadastro=datetime.now().isoformat(),
                tipo_usuario="Administrador",
                cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
            )
            id_usuario_criado = inserir_usuario(usuario_base)
            assert id_usuario_criado is not None, "Falha ao criar o usuário base."

            assert id_usuario_criado is not None
            admin_para_inserir = Administrador(id=0, id_usuario=id_usuario_criado)
            #Act 
            #Assert
            id_admin_inserido = inserir_administrador(admin_para_inserir)
            assert id_admin_inserido is not None and id_admin_inserido > 0
            with pytest.raises(sqlite3.IntegrityError) as e:
                inserir_administrador(admin_para_inserir)
            assert "UNIQUE constraint failed" in str(e.value)
    
    def test_obter_todos_administradores(self, test_db):
            #Arrange
            criar_tabela_usuario()
            criar_tabela_administrador()

            usuario1 = Usuario(id=0, nome="Ana (Admin)", email="ana@teste.com", senha="123", cpf_cnpj="111", telefone="111", data_cadastro=datetime.now().isoformat(), tipo_usuario="Administrador",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")
            usuario2 = Usuario(id=0, nome="Beto (Cliente)", email="beto@teste.com", senha="123", cpf_cnpj="222", telefone="222", data_cadastro=datetime.now().isoformat(), tipo_usuario="Cliente",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")
            usuario3 = Usuario(id=0, nome="Carla (Admin)", email="carla@teste.com", senha="123", cpf_cnpj="333", telefone="333", data_cadastro=datetime.now().isoformat(), tipo_usuario="Administrador",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")

            id_ana = inserir_usuario(usuario1)
            id_beto = inserir_usuario(usuario2)
            id_carla = inserir_usuario(usuario3)

            assert id_ana is not None
            assert id_carla is not None
            inserir_administrador(Administrador(id=0, id_usuario=id_ana))
            inserir_administrador(Administrador(id=0, id_usuario=id_carla))
            #Act
            lista_de_admins = obter_todos_administradores()
            #Assert
            assert len(lista_de_admins) == 2
            assert lista_de_admins[0].nome == "Ana (Admin)"
            assert lista_de_admins[1].nome == "Carla (Admin)"
            assert isinstance(lista_de_admins[0], Usuario) 

    def test_obter_administrador_por_id(self, test_db):
        #Arrange
            criar_tabela_usuario()
            criar_tabela_administrador()

            email_unico = "id_admin@teste.com"
            usuario_base = Usuario(
                id=0, nome="Admin Por ID", email=email_unico, senha="456",
                cpf_cnpj="444", telefone="444", data_cadastro=datetime.now().isoformat(), tipo_usuario="Administrador",
                cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES"
            )
            id_usuario = inserir_usuario(usuario_base)
            assert id_usuario is not None
            id_admin = inserir_administrador(Administrador(id=0, id_usuario=id_usuario))
            assert id_admin is not None, "Falha ao inserir na tabela admin para o teste."
            #Act
            usuario_encontrado = obter_administrador_por_id(id_admin)
            #Assert
            assert usuario_encontrado is not None
            assert isinstance(usuario_encontrado, Usuario)
            assert usuario_encontrado.id == id_usuario
            assert usuario_encontrado.email == email_unico
            assert usuario_encontrado.nome == "Admin Por ID"

    def test_transferir_privilegio_admin_sem_getter(self, test_db):
            #Arrange
            criar_tabela_usuario()
            criar_tabela_administrador()

            ana = Usuario(id=0, nome="Ana", email="ana@teste.com", senha="123", cpf_cnpj="111", telefone="111", data_cadastro=datetime.now().isoformat(), tipo_usuario="Administrador",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")
            beto = Usuario(id=0, nome="Beto", email="beto@teste.com", senha="456", cpf_cnpj="222", telefone="222", data_cadastro=datetime.now().isoformat(), tipo_usuario="Cliente",
            cep="88888-888", rua="Rua Teste", numero="123", complemento="", bairro="Centro", cidade="Vitória", estado="ES")
            id_ana = inserir_usuario(ana)
            id_beto = inserir_usuario(beto)

            assert id_ana is not None
            assert id_beto is not None
            admin_original = Administrador(id=0, id_usuario=id_ana)
            id_admin_a_ser_atualizado = inserir_administrador(admin_original)
            assert id_admin_a_ser_atualizado is not None, "Falha ao criar o admin original."
            #Act
            admin_com_privilegio_transferido = Administrador(id=id_admin_a_ser_atualizado, id_usuario=id_beto)
            resultado = atualizar_administrador(admin_com_privilegio_transferido)
            #Assert
            assert resultado is True, "A função de atualizar deveria retornar True."
            try:
                inserir_administrador(Administrador(id=0, id_usuario=id_ana))
            except Exception as exc:
                assert False, f"Não deveria falhar ao reinserir Ana como admin. Erro: {exc}"
            with pytest.raises(sqlite3.IntegrityError) as exc_info:
                inserir_administrador(Administrador(id=0, id_usuario=id_beto))

            assert "UNIQUE constraint failed" in str(exc_info.value)

    def test_deletar_administrador(self, test_db):
            #Arrange
            criar_tabela_usuario()
            criar_tabela_administrador()

            usuario = Usuario(
                id=0, nome="Admin a ser Removido", email="remover@teste.com",
                senha="123", cpf_cnpj="333", telefone="333",
                data_cadastro=datetime.now().isoformat(), tipo_usuario="Administrador",
                cep="88888-888", rua="Rua Teste", numero="123", complemento="",
                bairro="Centro", cidade="Vitória", estado="ES"
            )
            id_usuario = inserir_usuario(usuario)
            assert id_usuario is not None

            admin_para_deletar = Administrador(id=0, id_usuario=id_usuario)
            id_admin_criado = inserir_administrador(admin_para_deletar)
            
            assert id_admin_criado is not None, "Falha ao criar o administrador para o teste."
            #Act
            resultado_delecao = deletar_administrador(administrador_id=id_admin_criado)
            #Assert
            assert resultado_delecao is True, "A função de deletar deveria retornar True."
            try:
                assert id_usuario is not None
                novo_id_admin = inserir_administrador(Administrador(id=0, id_usuario=id_usuario))
                assert novo_id_admin is not None and novo_id_admin > id_admin_criado
            except Exception as exc:
                assert False, f"A reinserção do administrador deveria ter sucesso, mas falhou. Erro: {exc}"

    