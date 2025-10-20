import sqlite3
from typing import Optional, List
from data.administrador.administrador_model import Administrador
from data.administrador.administrador_sql import *
from data.usuario.usuario_model import Usuario
from utils.db import open_connection


def criar_tabela_administrador() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Administrador")
        cursor.execute(CRIAR_TABELA_ADMINISTRADOR)
        conn.commit()
        return True


def inserir_administrador(administrador: Administrador) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(INSERIR_ADMINISTRADOR, (administrador.id_usuario,))
        conn.commit()
        return cursor.lastrowid


def obter_todos_administradores() -> List[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_ADMINISTRADORES)
        rows = cursor.fetchall()
        return [
            Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                cep=row.get("cep", ""),
                rua=row.get("rua", ""),
                numero=row.get("numero", ""),
                complemento=row.get("complemento", ""),
                bairro=row.get("bairro", ""),
                cidade=row.get("cidade", ""),
                estado=row.get("estado", ""),
                tipo_usuario=row["tipo_usuario"],
                data_cadastro=row["data_cadastro"]
            ) for row in rows
        ]

def obter_administrador_por_id(administrador_id: int) -> Optional[Usuario]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ADMINISTRADOR_POR_ID, (administrador_id,))
        row = cursor.fetchone()
        if row:
            return Usuario(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                cep=row.get("cep", ""),
                rua=row.get("rua", ""),
                numero=row.get("numero", ""),
                complemento=row.get("complemento", ""),
                bairro=row.get("bairro", ""),
                cidade=row.get("cidade", ""),
                estado=row.get("estado", ""),
                tipo_usuario=row["tipo_usuario"],
                data_cadastro=row["data_cadastro"]
            )
    return None


def atualizar_administrador(administrador: Administrador) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_ADMINISTRADOR, (
            administrador.id_usuario,
            administrador.id
        ))
        conn.commit()
        return cursor.rowcount > 0


def deletar_administrador(administrador_id: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ADMINISTRADOR, (administrador_id,))
        conn.commit()
        return cursor.rowcount > 0


