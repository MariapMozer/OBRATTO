from datetime import datetime
from typing import Optional, List
from data.avaliacao.avaliacao_model import Avaliacao
from data.avaliacao.avaliacao_sql import *
from util.db import open_connection


def criar_tabela_avaliacao() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS avaliacao")
        cursor.execute(CRIAR_TABELA_AVALIACAO)
        conn.commit()
        return True


def inserir_avaliacao(avaliacao: Avaliacao) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_AVALIACAO,
            (
                avaliacao.id_avaliador,
                avaliacao.id_avaliado,
                avaliacao.nota,
                avaliacao.data_avaliacao,
                avaliacao.descricao,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_todos() -> List[Avaliacao]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS)
        rows = cursor.fetchall()
        avaliacoes = []
        for row in rows:
            avaliacoes.append(
                Avaliacao(
                    id_avaliacao=row["id_avaliacao"],
                    id_avaliador=row["id_avaliador"],
                    id_avaliado=row["id_avaliado"],
                    nota=row["nota"],
                    data_avaliacao=row["data_avaliacao"],
                    descricao=row["descricao"],
                    nome_avaliador=row["nome_avaliador"],
                    nome_avaliado=row["nome_avaliado"],
                )
            )
        return avaliacoes


def obter_avaliacao_por_id(id_avaliacao: int) -> Optional[Avaliacao]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_AVALIACAO_POR_ID, (id_avaliacao,))
        row = cursor.fetchone()
        if row:
            return Avaliacao(
                id_avaliacao=row["id_avaliacao"],
                id_avaliador=row["id_avaliador"],
                id_avaliado=row["id_avaliado"],
                nota=row["nota"],
                data_avaliacao=row["data_avaliacao"],
                descricao=row["descricao"],
            )
        return None


def obter_avaliacao_por_pagina(conn, limit: int, offset: int) -> list[Avaliacao]:
    cursor = conn.cursor()
    cursor.execute(OBTER_AVALIACAO_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        Avaliacao(
            id_avaliacao=row[0],
            id_avaliador=row[1],
            id_avaliado=row[2],
            nota=row[3],
            data_avaliacao=datetime.fromisoformat(row[4]),
            descricao=row[5],
        )
        for row in rows
    ]


def atualizar_avaliacao(avaliacao: Avaliacao) -> bool:
    """
    Atualiza dados da tabela avaliacao.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_AVALIACAO,
            (
                avaliacao.id_avaliador,
                avaliacao.id_avaliado,
                avaliacao.nota,
                avaliacao.data_avaliacao,
                avaliacao.descricao,
                avaliacao.id_avaliacao,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_avaliacao(id_avaliacao: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_AVALIACAO, (id_avaliacao,))
        conn.commit()
        return cursor.rowcount > 0
