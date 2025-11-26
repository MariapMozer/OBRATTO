import sqlite3
from typing import Optional, List
from data.notificacao.notificacao_model import Notificacao
from data.notificacao.notificacao_sql import *
from util.db import open_connection


def criar_tabela_notificacao() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_NOTIFICACAO)
        conn.commit()
        return True


def inserir_notificacao(notificacao: Notificacao) -> Optional[int]:
    """
    Insere uma nova Notificacao no banco.
    O id_usuario deve existir na tabela usuario.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_NOTIFICACAO,
            (
                notificacao.id_usuario,
                notificacao.mensagem,
                notificacao.data_hora,
                notificacao.tipo_notificacao,
                int(notificacao.visualizar),
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_notificacao() -> List[Notificacao]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_NOTIFICACAO)
        rows = cursor.fetchall()
        notificacoes = []
        for row in rows:
            notificacoes.append(
                Notificacao(
                    id_notificacao=row["id_notificacao"],
                    id_usuario=row["id_usuario"],
                    mensagem=row["mensagem"],
                    data_hora=row["data_hora"],
                    tipo_notificacao=row["tipo_notificacao"],
                    visualizar=bool(row["vizualizar"]),
                )
            )
        return notificacoes


def obter_notificacao_por_id(id_notificacao: int) -> Optional[Notificacao]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_NOTIFICACAO_POR_ID, (id_notificacao,))
        row = cursor.fetchone()
        if row:
            return Notificacao(
                id_notificacao=row["id_notificacao"],
                id_usuario=row["id_usuario"],
                mensagem=row["mensagem"],
                data_hora=row["data_hora"],
                tipo_notificacao=row["tipo_notificacao"],
                visualizar=bool(row["vizualizar"]),
            )
        return None


def obter_notificacao_por_pagina(conn, limit: int, offset: int) -> list[Notificacao]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(OBTER_NOTIFICACAO_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        Notificacao(
            id_notificacao=row["id_notificacao"],
            id_usuario=row["id_usuario"],
            mensagem=row["mensagem"],
            data_hora=row["data_hora"],
            tipo_notificacao=row["tipo_notificacao"],
            visualizar=bool(row["vizualizar"]),
        )
        for row in rows
    ]


def atualizar_notificacao(notificacao: Notificacao) -> bool:
    """
    Atualiza dados da tabela notificacao.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_NOTIFICACAO,
            (
                notificacao.id_usuario,
                notificacao.mensagem,
                notificacao.data_hora,
                notificacao.tipo_notificacao,
                int(notificacao.visualizar),
                notificacao.id_notificacao,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar(id_notificacao: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_NOTIFICACAO, (id_notificacao,))
        conn.commit()
        return cursor.rowcount > 0
