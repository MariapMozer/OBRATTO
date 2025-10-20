from datetime import datetime
from typing import Optional, List
from data.usuario.usuario_model import Usuario
from data.usuario.usuario_sql import *
from utils.db import open_connection


def criar_tabela_usuario() -> bool:
    try:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CRIAR_TABELA_USUARIO)
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de usuário: {e}")
        return False


def inserir_usuario(usuario: Usuario) -> Optional[int]:
    if not usuario.data_cadastro:
        usuario.data_cadastro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_USUARIO, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.cpf_cnpj,
            usuario.telefone,
            usuario.cep,
            usuario.rua,
            usuario.numero,
            usuario.complemento,
            usuario.bairro,
            usuario.cidade,
            usuario.estado,
            usuario.data_cadastro,
            usuario.foto,
            usuario.token_redefinicao,
            usuario.data_token,
            usuario.tipo_usuario
        ))
        conn.commit()
        return cursor.lastrowid

def obter_usuario_por_email(email: str) -> Optional[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                cep=row["cep"],
                rua=row["rua"],
                numero=row["numero"],
                complemento=row["complemento"],
                bairro=row["bairro"],
                cidade=row["cidade"],
                estado=row["estado"],
                data_cadastro=row["data_cadastro"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                tipo_usuario=row["tipo_usuario"]
            )
    return None

def obter_usuario_por_id(id: int) -> Optional[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                cep=row["cep"],
                rua=row["rua"],
                numero=row["numero"],
                complemento=row["complemento"],
                bairro=row["bairro"],
                cidade=row["cidade"],
                estado=row["estado"],
                data_cadastro=row["data_cadastro"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                tipo_usuario=row["tipo_usuario"]
            )
    return None

def obter_usuario_por_token(token: str) -> Optional[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_USUARIO_POR_TOKEN, (token,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                cep=row["cep"],
                rua=row["rua"],
                numero=row["numero"],
                complemento=row["complemento"],
                bairro=row["bairro"],
                cidade=row["cidade"],
                estado=row["estado"],
                data_cadastro=row["data_cadastro"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
                tipo_usuario=row["tipo_usuario"]
            )
    return None


def obter_usuarios_por_pagina (pg_num: int, pg_size:int) -> List[Usuario]:
    try:
        limit = pg_size
        offset = (pg_num - 1) * pg_size
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_USUARIO_POR_PAGINA, (limit, offset))
            rows = cursor.fetchall()
            usuarios = [
                Usuario(
                    id=row["id"],
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    cpf_cnpj=row["cpf_cnpj"],
                    telefone=row["telefone"],
                    cep=row["cep"],
                    rua=row["rua"],
                    numero=row["numero"],
                    complemento=row["complemento"],
                    bairro=row["bairro"],
                    cidade=row["cidade"],
                    estado=row["estado"],
                    data_cadastro=row["data_cadastro"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"],
                    tipo_usuario=row["tipo_usuario"]
                ) for row in rows
            ]
            return usuarios
    except Exception as e:
        print(f"Erro ao obter usuários por página: {e}")
        return []

#def obter_todos_por_perfil():
def obter_todos_por_perfil(tipo_usuario: str) -> List[Usuario]:
    try:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_USUARIOS_POR_PERFIL, (tipo_usuario,))
            rows = cursor.fetchall()
            usuarios = [
                Usuario(
                    id=row["id"],
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"],
                    cpf_cnpj=row["cpf_cnpj"],
                    telefone=row["telefone"],
                    cep=row["cep"],
                    rua=row["rua"],
                    numero=row["numero"],
                    complemento=row["complemento"],
                    bairro=row["bairro"],
                    cidade=row["cidade"],
                    estado=row["estado"],
                    data_cadastro=row["data_cadastro"],
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"],
                    tipo_usuario=row["tipo_usuario"]
                ) for row in rows
            ]
        return usuarios
    except Exception as e:
        print(f"Erro ao obter usuários por perfil: {e}")
        return []
    



def atualizar_usuario(usuario: Usuario) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_USUARIO, (
            usuario.nome,
            usuario.email,
            usuario.senha,
            usuario.cpf_cnpj,
            usuario.telefone,
            usuario.cep,
            usuario.rua,
            usuario.numero,
            usuario.complemento,
            usuario.bairro,
            usuario.cidade,
            usuario.estado,
            usuario.data_cadastro,
            usuario.foto,
            usuario.token_redefinicao,
            usuario.data_token,
            usuario.tipo_usuario,
            usuario.id
        ))
        conn.commit()
        return (cursor.rowcount > 0)

def atualizar_tipo_usuario(usuario_id: int, tipo_usuario: str) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_TIPO_USUARIO,(tipo_usuario, usuario_id))
        conn.commit()
        return (cursor.rowcount > 0)
    
def atualizar_senha_usuario(usuario_id: int, nova_senha: str) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_SENHA_USUARIO, (nova_senha, usuario_id))
        conn.commit()
        return (cursor.rowcount > 0)


def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0

def deletar_usuario(usuario_id: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_USUARIO, (usuario_id,))
        conn.commit()
        return cursor.rowcount > 0