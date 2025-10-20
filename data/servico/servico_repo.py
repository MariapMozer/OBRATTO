import sqlite3
from typing import List, Optional
from data.servico.servico_model import Servico
from data.servico.servico_sql import (
    CRIAR_TABELA_SERVICO,
    INSERIR_SERVICO,
    OBTER_SERVICO,
    OBTER_SERVICO_POR_ID,
    ATUALIZAR_SERVICO,
    DELETAR_SERVICO,
    OBTER_SERVICO_POR_PAGINA,
)
from util.db import open_connection


def criar_tabela_servico() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_SERVICO)
        conn.commit()
        return True


def inserir_servico(servico: Servico) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_SERVICO,
            (
                servico.id_prestador,
                servico.titulo,
                servico.descricao,
                servico.categoria,
                servico.valor_base,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_servico() -> List[Servico]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_SERVICO)
        rows = cursor.fetchall()
        servicos = []
        for row in rows:
            servicos.append(
                Servico(
                    id_servico=row["id_servico"],
                    id_prestador=row["id_prestador"],
                    titulo=row["titulo"],
                    descricao=row["descricao"],
                    categoria=row["categoria"],
                    valor_base=row["valor_base"],
                    nome_prestador=row["nome_prestador"],
                )
            )
        return servicos


def obter_servico_por_id(id_servico: int) -> Optional[Servico]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_SERVICO_POR_ID, (id_servico,))
        row = cursor.fetchone()
        if row:
            return Servico(
                id_servico=row["id_servico"],
                id_prestador=row["id_prestador"],
                titulo=row["titulo"],
                descricao=row["descricao"],
                categoria=row["categoria"],
                valor_base=row["valor_base"],
                nome_prestador=row["nome_prestador"],
            )
        return None


def obter_servico_por_pagina(conn, limit: int, offset: int) -> list[Servico]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(OBTER_SERVICO_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        Servico(
            id_servico=row["id_servico"],
            id_prestador=row["id_prestador"],
            titulo=row["titulo"],
            descricao=row["descricao"],
            categoria=row["categoria"],
            valor_base=row["valor_base"],
            nome_prestador=row["nome_prestador"],
        )
        for row in rows
    ]


def atualizar_servico(servico: Servico) -> bool:
    """
    Atualiza dados da tabela servico.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_SERVICO,
            (
                servico.id_prestador,
                servico.titulo,
                servico.descricao,
                servico.categoria,
                servico.valor_base,
                servico.id_servico,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_servico(id_servico: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_SERVICO, (id_servico,))
        conn.commit()
        return cursor.rowcount > 0
