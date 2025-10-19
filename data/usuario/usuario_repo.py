from datetime import datetime
from typing import Optional, List
from data.usuario.usuario_model import Usuario
from data.usuario.usuario_sql import *
from utils.db import open_connection
import logging

logger = logging.getLogger(__name__)


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
        new_id = cursor.lastrowid
        # Após inserir na tabela usuario, garantir existência do registro na tabela específica
        try:
            _criar_registro_tipo_padrao(conn, usuario, new_id)
        except Exception as e:
            # Não falhar a criação do usuário se a criação do registro de tipo falhar; apenas logar
            logger.exception(f"Falha ao criar registro de tipo para usuario id={new_id}: {e}")
        return new_id


def _criar_registro_tipo_padrao(conn, usuario: Usuario, usuario_id: int) -> None:
    """
    Cria um registro padrão nas tabelas de tipo (fornecedor, prestador, cliente, administrador)
    quando possível. Usa valores padrão para campos obrigatórios quando necessário.

    Observação: usamos INSERT OR IGNORE para não duplicar registros caso já existam.
    """
    tipo = (getattr(usuario, 'tipo_usuario', '') or '').lower()
    cur = conn.cursor()
    # Fornecedor
    if tipo == 'fornecedor':
        # razao_social recebe o nome do usuário como fallback
        razao = usuario.nome or ''
        cur.execute("INSERT OR IGNORE INTO fornecedor (id, razao_social, selo_confianca) VALUES (?, ?, ?)", (usuario_id, razao, 0))
    # Prestador
    elif tipo == 'prestador':
        # area_atuacao é NOT NULL na tabela; usar valor padrão vazio
        area = ''
        razao = usuario.nome or ''
        descricao = ''
        cur.execute("INSERT OR IGNORE INTO prestador (id, area_atuacao, razao_social, descricao_servicos, selo_confianca) VALUES (?, ?, ?, ?, ?)", (usuario_id, area, razao, descricao, 0))
    # Cliente
    elif tipo == 'cliente':
        # genero and data_nascimento são NOT NULL; inserir placeholders
        genero = 'N/D'
        data_nasc = '1970-01-01'
        cur.execute("INSERT OR IGNORE INTO cliente (id, genero, data_nascimento) VALUES (?, ?, ?)", (usuario_id, genero, data_nasc))
    # Administrador
    elif tipo == 'administrador' or tipo == 'admin':
        cur.execute("INSERT OR IGNORE INTO administrador (id_usuario) VALUES (?)", (usuario_id,))
    conn.commit()


def backfill_registros_tipo():
    """
    Percorre todos os usuários e garante um registro correspondente na tabela de tipo.
    Use este método para popular as tabelas de tipo para usuários já existentes.
    """
    with open_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nome, tipo_usuario, foto FROM usuario")
        rows = cur.fetchall()
        count = 0
        for r in rows:
            uid = r['id'] if isinstance(r, dict) else r[0]
            tipo = (r['tipo_usuario'] if isinstance(r, dict) else r[2]) or ''
            usuario_obj = Usuario(
                id=uid,
                nome=(r['nome'] if isinstance(r, dict) else r[1]),
                email=None,
                senha=None,
                cpf_cnpj=None,
                telefone=None,
                cep=None,
                rua=None,
                numero=None,
                complemento=None,
                bairro=None,
                cidade=None,
                estado=None,
                data_cadastro=None,
                foto=None,
                token_redefinicao=None,
                data_token=None,
                tipo_usuario=tipo
            )
            try:
                _criar_registro_tipo_padrao(conn, usuario_obj, uid)
                count += 1
            except Exception:
                logger.exception(f"Erro ao backfill usuario id={uid}")
        logger.info(f"Backfill finalizado: processados={len(rows)}, insercoes_tentadas={count}")

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


def obter_usuarios_por_pagina (pg_num: int, pg_size:int) -> List[Usuario]:
    try:
        limit = pg_size
        offset = (pg_num - 1) * pg_size
        conn = open_connection()
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
        conn.close()
        return usuarios
    except Exception as e:
        print(f"Erro ao obter usuários por página: {e}")

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