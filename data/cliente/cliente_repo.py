from datetime import datetime, date
import sqlite3
from typing import Optional, List
from data.cliente.cliente_model import Cliente
from data.cliente.cliente_sql import *
from data.usuario.usuario_repo import (
    inserir_usuario,
    atualizar_usuario,
    deletar_usuario,
)
from util.db import open_connection


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
            data_nascimento_str = cliente.data_nascimento
            cursor.execute(
                INSERIR_CLIENTE,
                (
                    id_usuario_gerado,
                    cliente.genero,
                    data_nascimento_str,
                ),
            )
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
            clientes.append(
                Cliente(
                    id=row["id"],
                    nome=row["nome"],
                    email=row["email"],
                    senha=row["senha"] if "senha" in row.keys() else "",
                    cpf_cnpj=row["cpf_cnpj"],
                    telefone=row["telefone"],
                    cep=row["cep"] if "cep" in row.keys() else "",
                    complemento=(
                        row["complemento"] if "complemento" in row.keys() else ""
                    ),
                    estado=row["estado"],
                    cidade=row["cidade"],
                    rua=row["rua"],
                    numero=row["numero"],
                    bairro=row["bairro"],
                    data_cadastro=row["data_cadastro"],
                    tipo_usuario=row["tipo_usuario"],
                    genero=row["genero"],
                    data_nascimento=(
                        date.fromisoformat(row["data_nascimento"])
                        if "data_nascimento" in row.keys() and row["data_nascimento"]
                        else None
                    ),
                    foto=row["foto"],
                    token_redefinicao=row["token_redefinicao"],
                    data_token=row["data_token"],
                )
            )
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
                cep=row["cep"] if "cep" in row.keys() else "",
                complemento=row["complemento"] if "complemento" in row.keys() else "",
                estado=row["estado"],
                cidade=row["cidade"],
                rua=row["rua"],
                numero=row["numero"],
                bairro=row["bairro"],
                data_cadastro=row["data_cadastro"],
                genero=row["genero"],
                data_nascimento=(
                    date.fromisoformat(row["data_nascimento"])
                    if "data_nascimento" in row.keys() and row["data_nascimento"]
                    else None
                ),
                tipo_usuario=row["tipo_usuario"],
                foto=row["foto"],
                token_redefinicao=row["token_redefinicao"],
                data_token=row["data_token"],
            )
        return None


def obter_cliente_por_pagina(conn, limit: int, offset: int) -> list[Cliente]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(OBTER_CLIENTE_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        Cliente(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf_cnpj=row["cpf_cnpj"],
            telefone=row["telefone"],
            cep=row["cep"] if "cep" in row.keys() else "",
            complemento=row["complemento"] if "complemento" in row.keys() else "",
            estado=row["estado"],
            cidade=row["cidade"],
            rua=row["rua"],
            numero=row["numero"],
            bairro=row["bairro"],
            data_cadastro=row["data_cadastro"],
            genero=row["genero"],
            data_nascimento=(
                row["data_nascimento"] if "data_nascimento" in row.keys() else None
            ),
            tipo_usuario=row["tipo_usuario"],
            foto=row["foto"],
            token_redefinicao=row["token_redefinicao"],
            data_token=row["data_token"],
        )
        for row in rows
    ]


def obter_cliente_por_email(email: str) -> Optional[Cliente]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuario WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return obter_cliente_por_id(row["id"])
        return None


def atualizar_cliente(cliente: Cliente) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        sucesso_usuario = atualizar_usuario(cliente)
        data_nascimento_str = (
            cliente.data_nascimento.isoformat()
            if cliente.data_nascimento is not None
            else None
        )
        cursor.execute(
            ATUALIZAR_CLIENTE,
            (
                cliente.genero,
                data_nascimento_str,
                cliente.id,
            ),
        )
        conn.commit()
        return sucesso_usuario or cursor.rowcount > 0


def deletar_cliente(cliente_id: int) -> bool:
    return deletar_usuario(cliente_id)


def atualizar_foto(id: int, caminho_foto: str) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE cliente SET foto = ? WHERE id = ?", (caminho_foto, id))
        return cursor.rowcount > 0
