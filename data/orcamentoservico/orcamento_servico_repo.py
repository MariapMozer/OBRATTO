from typing import List, Optional
from data.orcamentoservico.orcamento_servico_model import OrcamentoServico
from data.orcamentoservico.orcamento_servico_sql import *
from util.db import open_connection
import sqlite3


def criar_tabela_orcamento_servico() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_ORCAMENTO_SERVICO)
        conn.commit()
        return True


def inserir_orcamento_servico(orcamento: OrcamentoServico) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_ORCAMENTO_SERVICO,
            (
                orcamento.id_servico,
                orcamento.id_prestador,
                orcamento.id_cliente,
                orcamento.valor_estimado,
                orcamento.data_solicitacao,
                orcamento.prazo_entrega,
                orcamento.status,
                orcamento.descricao,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_orcamento_servico() -> List[OrcamentoServico]:
    with open_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(OBTER_ORCAMENTO_SERVICO)
        rows = cursor.fetchall()
        orcamentos_servicos = []
        for row in rows:
            orcamentos_servicos.append(
                OrcamentoServico(
                    id_orcamento=row["id_orcamento"],
                    id_servico=row["id_servico"],
                    id_prestador=row["id_prestador"],
                    id_cliente=row["id_cliente"],
                    valor_estimado=row["valor_estimado"],
                    data_solicitacao=row["data_solicitacao"],
                    prazo_entrega=row["prazo_entrega"],
                    status=row["status"],
                    descricao=row["descricao"],
                    nome_prestador=row["nome_prestador"],
                    nome_cliente=row["nome_cliente"],
                    titulo_servico=row["titulo_servico"],
                )
            )
        return orcamentos_servicos


def obter_orcamento_servico_por_id(id_orcamento: int) -> Optional[OrcamentoServico]:
    with open_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(OBTER_ORCAMENTO_SERVICO_POR_ID, (id_orcamento,))
        row = cursor.fetchone()
        if row:
            return OrcamentoServico(
                id_orcamento=row["id_orcamento"],
                id_servico=row["id_servico"],
                id_prestador=row["id_prestador"],
                id_cliente=row["id_cliente"],
                valor_estimado=row["valor_estimado"],
                data_solicitacao=row["data_solicitacao"],
                prazo_entrega=row["prazo_entrega"],
                status=row["status"],
                descricao=row["descricao"],
                nome_prestador=row["nome_prestador"],
                nome_cliente=row["nome_cliente"],
                titulo_servico=row["titulo_servico"],
            )
        return None


def obter_orcamento_servico_por_pagina(
    conn, limit: int, offset: int
) -> list[OrcamentoServico]:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(OBTER_ORCAMENTO_SERVICO_POR_PAGINA, (limit, offset))
    rows = cursor.fetchall()
    return [
        OrcamentoServico(
            id_orcamento=row["id_orcamento"],
            id_servico=row["id_servico"],
            id_prestador=row["id_prestador"],
            id_cliente=row["id_cliente"],
            valor_estimado=row["valor_estimado"],
            data_solicitacao=row["data_solicitacao"],
            prazo_entrega=row["prazo_entrega"],
            status=row["status"],
            descricao=row["descricao"],
            nome_prestador=row["nome_prestador"],
            nome_cliente=row["nome_cliente"],
            titulo_servico=row["titulo_servico"],
        )
        for row in rows
    ]


def atualizar_orcamento_servico(orcamento: OrcamentoServico) -> bool:
    """
    Atualiza dados da tabela orcamentoServico.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_ORCAMENTO_SERVICO,
            (
                orcamento.id_servico,
                orcamento.id_prestador,
                orcamento.id_cliente,
                orcamento.valor_estimado,
                orcamento.data_solicitacao,
                orcamento.prazo_entrega,
                orcamento.status,
                orcamento.descricao,
                orcamento.id_orcamento,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_orcamento_servico(id_orcamento: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ORCAMENTO_SERVICO, (id_orcamento,))
        conn.commit()
        return cursor.rowcount > 0
