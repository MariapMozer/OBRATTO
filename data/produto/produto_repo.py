from datetime import datetime
import sqlite3
from typing import Optional, List
from data.produto.produto_model import Produto
from data.produto.produto_sql import (
    CRIAR_TABELA_PRODUTO,
    INSERIR_PRODUTO,
    INSERIR_PRODUTO_SEM_ID,
    OBTER_PRODUTO,
    OBTER_PRODUTO_POR_ID,
    OBTER_PRODUTO_POR_NOME,
    OBTER_PRODUTOS_POR_FORNECEDOR,
    ATUALIZAR_PRODUTO,
    DELETAR_PRODUTO,
    OBTER_PRODUTO_POR_PAGINA,
)
from util.db import open_connection


def criar_tabela_produto():
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_PRODUTO)
        conn.commit()


def inserir_produto(produto: Produto) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        if produto.id is None:
            # Insert without ID (autoincrement)
            params = (
                produto.nome,
                produto.descricao,
                produto.preco,
                produto.quantidade,
                int(produto.em_promocao),
                produto.desconto,
                produto.foto,
                produto.fornecedor_id,
            )
            cursor.execute(INSERIR_PRODUTO_SEM_ID, params)
            conn.commit()
            return cursor.lastrowid
        else:
            # Insert with ID
            cursor.execute(
                INSERIR_PRODUTO,
                (
                    produto.id,
                    produto.nome,
                    produto.descricao,
                    produto.preco,
                    produto.quantidade,
                    int(produto.em_promocao),
                    produto.desconto,
                    produto.foto,
                    produto.fornecedor_id,
                ),
            )
            conn.commit()
            return produto.id


def obter_produto_por_id(id: int) -> Optional[Produto]:
    with open_connection() as conn:
        cursor = conn.execute(OBTER_PRODUTO_POR_ID, (id,))
        row = cursor.fetchone()
        if row:
            return Produto(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                quantidade=row[4],
                em_promocao=bool(row[5]),
                desconto=row[6],
                foto=row[7] if len(row) > 7 else None,
                fornecedor_id=row[8] if len(row) > 8 else None,
            )
        return None


def obter_produto_por_pagina(limit: int, offset: int) -> List[Produto]:
    with open_connection() as conn:
        cursor = conn.execute(OBTER_PRODUTO_POR_PAGINA, (limit, offset))
        return [
            Produto(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                quantidade=row[4],
                em_promocao=bool(row[5]),
                desconto=row[6],
                foto=row[7] if len(row) > 7 else None,
                fornecedor_id=row[8] if len(row) > 8 else None,
            )
            for row in cursor.fetchall()
        ]


def obter_produto_por_nome(nome: str) -> List[Produto]:
    with open_connection() as conn:
        cursor = conn.execute(OBTER_PRODUTO_POR_NOME, (f"%{nome}%",))
        return [
            Produto(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                quantidade=row[4],
                em_promocao=bool(row[5]),
                desconto=row[6],
                foto=row[7] if len(row) > 7 else None,
                fornecedor_id=row[8] if len(row) > 8 else None,
            )
            for row in cursor.fetchall()
        ]


def obter_produtos_por_fornecedor(
    fornecedor_id: int, limit: int = 10, offset: int = 0
) -> List[Produto]:
    with open_connection() as conn:
        cursor = conn.execute(
            OBTER_PRODUTOS_POR_FORNECEDOR, (fornecedor_id, limit, offset)
        )
        return [
            Produto(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                quantidade=row[4],
                em_promocao=bool(row[5]),
                desconto=row[6],
                foto=row[7] if len(row) > 7 else None,
                fornecedor_id=row[8] if len(row) > 8 else None,
            )
            for row in cursor.fetchall()
        ]


def atualizar_produto(produto: Produto):
    with open_connection() as conn:
        conn.execute(
            ATUALIZAR_PRODUTO,
            (
                produto.nome,
                produto.descricao,
                produto.preco,
                produto.quantidade,
                int(produto.em_promocao),
                produto.desconto,
                produto.foto,
                produto.fornecedor_id,
                produto.id,
            ),
        )
        conn.commit()


def deletar_produto(id: int):
    with open_connection() as conn:
        conn.execute(DELETAR_PRODUTO, (id,))
        conn.commit()
