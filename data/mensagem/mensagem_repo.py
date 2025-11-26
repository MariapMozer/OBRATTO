from datetime import datetime
import sqlite3
from typing import Optional, List
from data.mensagem.mensagem_model import Mensagem
from data.mensagem.mensagem_sql import *
from util.db import open_connection

import logging

logger = logging.getLogger(__name__)


def criar_tabela_mensagem() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_MENSAGEM)
        conn.commit()
        return True


def inserir_mensagem(mensagem):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_MENSAGEM,
            (
                mensagem.id_remetente,
                mensagem.id_destinatario,
                mensagem.conteudo,
                mensagem.data_hora.isoformat(),  # use string ISO para evitar warnings
                mensagem.nome_remetente,
                mensagem.nome_destinatario,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_mensagem(usuario_id) -> List[Mensagem]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_MENSAGEM)
        rows = cursor.fetchall()
        mensagens = []
        for row in rows:
            mensagens.append(
                Mensagem(
                    id_mensagem=row["id_mensagem"],
                    id_remetente=row["id_remetente"],
                    id_destinatario=row["id_destinatario"],
                    conteudo=row["conteudo"],
                    data_hora=row["data_hora"],
                    nome_remetente=row["nome_remetente"],
                    nome_destinatario=row["nome_destinatario"],
                )
            )
        return mensagens


def obter_mensagem_por_id(id_mensagem):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mensagem WHERE id_mensagem = ?", (id_mensagem,))
        row = cursor.fetchone()
        logger.debug("Linha obtida do DB: %s", row)
        if row:
            return Mensagem(
                id_mensagem=row[0],
                id_remetente=row[1],
                id_destinatario=row[2],
                conteudo=row[3],
                data_hora=datetime.fromisoformat(row[4]),
                nome_remetente=row[5],
                nome_destinatario=row[6],
            )
        return None


def obter_mensagem_por_pagina(conn, limit: int, offset: int) -> list[Mensagem]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(OBTER_MENSAGEM_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        Mensagem(
            id_mensagem=row["id_mensagem"],
            id_remetente=row["id_remetente"],
            id_destinatario=row["id_destinatario"],
            conteudo=row["conteudo"],
            data_hora=datetime.fromisoformat(row[4]),
            nome_remetente=row["nome_remetente"],
            nome_destinatario=row["nome_destinatario"],
        )
        for row in rows
    ]


def atualizar_mensagem(mensagem: Mensagem) -> bool:
    """
    Atualiza dados da tabela mensagem.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_MENSAGEM,
            (
                mensagem.id_remetente,
                mensagem.id_destinatario,
                mensagem.conteudo,
                mensagem.data_hora,
                mensagem.id_mensagem,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_mensagem(id_mensagem: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_MENSAGEM, (id_mensagem,))
        conn.commit()
        return cursor.rowcount > 0
