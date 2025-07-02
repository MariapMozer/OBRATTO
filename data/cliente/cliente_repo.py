from datetime import datetime, date
import sqlite3
from typing import Optional, List
from data.cliente.cliente_model import Cliente
from data.cliente.cliente_sql import *
from data.usuario.usuario_repo import inserir_usuario, atualizar_usuario, deletar_usuario
from utils.db import open_connection

def criar_tabela_cliente() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS cliente")
        cursor.execute(CRIAR_TABELA_CLIENTE)
        conn.commit()
        return True

def inserir_cliente(cliente: Cliente) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        id_usuario_gerado = inserir_usuario(cliente)
        if id_usuario_gerado:
            data_nascimento_str = cliente.data_nascimento.isoformat()
            cursor.execute(INSERIR_CLIENTE, (
                id_usuario_gerado,
                cliente.genero,
                data_nascimento_str
            ))
            conn.commit()
            return id_usuario_gerado
        return None

def obter_cliente() -> List[Cliente]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_CLIENTE)
        rows = cursor.fetchall()
        clientes = []
        for row in rows:
            clientes.append(Cliente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=None,
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                data_cadastro=datetime.fromisoformat(row["data_cadastro"]),
                endereco=row["endereco"],
                tipo_usuario=row["tipo_usuario"],
                genero=row["genero"],
                data_nascimento=date.fromisoformat(row["data_nascimento"])
            ))
        return clientes

def obter_cliente_por_id(cliente_id: int) -> Optional[Cliente]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_CLIENTE_POR_ID, (cliente_id,))
        row = cursor.fetchone()
        if row:
            return Cliente(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=row["senha"],
                cpf_cnpj=row["cpf_cnpj"],
                telefone=row["telefone"],
                data_cadastro=datetime.fromisoformat(row["data_cadastro"]),
                endereco=row["endereco"],
                tipo_usuario=row["tipo_usuario"],
                genero=row["genero"],
                data_nascimento=date.fromisoformat(row["data_nascimento"])
            )
        return None
    
def obter_cliente_por_pagina(conn, limit: int, offset: int) -> list[Cliente]:
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute(OBTER_CLIENTE_POR_PAGINA,(limit, offset))
    rows = cursor.fetchall()
    return [
        Cliente(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf_cnpj=row["cpf_cnpj"],
            telefone=row["telefone"],
            data_cadastro=row["data_cadastro"],
            endereco=row["endereco"],
            genero=row["genero"],
            data_nascimento=row["data_nascimento"],
            tipo_usuario=row["tipo_usuario"]
        )
        for row in rows
    ]

def atualizar_cliente(cliente: Cliente) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        sucesso_usuario = atualizar_usuario(cliente)
        data_nascimento_str = cliente.data_nascimento.isoformat()
        cursor.execute(ATUALIZAR_CLIENTE, (
            cliente.genero,
            data_nascimento_str,
            cliente.id
        ))
        conn.commit()
        return sucesso_usuario or cursor.rowcount > 0

def deletar_cliente(cliente_id: int) -> bool:
    return deletar_usuario(cliente_id)