# Script para criar um administrador padrão no banco, conforme padrão sugerido.
import sys
import os

# Adicionar o diretório pai ao sys.path para imports
script_dir = os.path.dirname(os.path.abspath(__file__))
projeto_dir = os.path.dirname(script_dir)
sys.path.insert(0, projeto_dir)

from utils.security import criar_hash_senha
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.administrador import administrador_repo
from data.administrador.administrador_model import Administrador
from datetime import datetime
from utils.seed import criar_tabelas


def criar_admin_padrao():
    # Verifica se já existe admin
    admins = usuario_repo.obter_todos_por_perfil("Administrador")
    if not admins:
        senha_hash = criar_hash_senha("admin123")
        admin_usuario = Usuario(
            id=None,
            nome="Administrador",
            email="admin@admin.com",
            senha=senha_hash,
            cpf_cnpj="00000000000",
            telefone="(00) 00000-0000",
            endereco="Sistema",
            tipo_usuario="Administrador",
            data_cadastro=datetime.now()
        )
        id_usuario = usuario_repo.inserir_usuario(admin_usuario)
        if id_usuario:
            administrador = Administrador(id=None, id_usuario=id_usuario)
            administrador_repo.inserir_administrador(administrador)
            print("Admin criado: admin@admin.com / admin123")
        else:
            print("Erro ao criar usuário administrador.")
    else:
        print("Já existe administrador cadastrado.")


criar_tabelas()
criar_admin_padrao()