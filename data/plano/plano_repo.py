from typing import Optional, List
from data.plano.plano_model import Plano
from data.plano.plano_model import Plano
from data.plano.plano_sql import *
from util.db import open_connection


def criar_tabela_plano() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_PLANO)
        conn.commit()
        return True


def inserir_plano(plano: Plano) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_PLANO,
            (
                plano.nome_plano,
                plano.valor_mensal,
                plano.limite_servico,
                plano.tipo_plano,
                plano.descricao,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_todos_os_planos() -> List[Plano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_OS_PLANOS)
        rows = cursor.fetchall()
        anuncio = []
        for row in rows:
            anuncio.append(
                Plano(
                    id_plano=row["id_plano"],
                    nome_plano=row["nome_plano"],
                    valor_mensal=row["valor_mensal"],
                    limite_servico=row["limite_servico"],
                    tipo_plano=row["tipo_plano"],
                    descricao=row["descricao"],
                )
            )
        return anuncio


def obter_plano_por_nome(plano_nome: str) -> Optional[Plano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PLANO_POR_NOME, (plano_nome,))
        row = cursor.fetchone()
        if row:
            return Plano(
                id_plano=row["id_plano"],
                nome_plano=row["nome_plano"],
                valor_mensal=row["valor_mensal"],
                limite_servico=row["limite_servico"],
                tipo_plano=row["tipo_plano"],
                descricao=row["descricao"],
            )
        return None  # Corrigido


def obter_plano_por_id(plano_id: int) -> Optional[Plano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PLANO_POR_ID, (plano_id,))
        row = cursor.fetchone()
        if row:
            return Plano(
                id_plano=row["id_plano"],
                nome_plano=row["nome_plano"],
                valor_mensal=row["valor_mensal"],
                limite_servico=row["limite_servico"],
                tipo_plano=row["tipo_plano"],
                descricao=row["descricao"],
            )
        return None


class PlanoRepository:
    def obter_plano_por_id(self, plano_id: int) -> Optional[Plano]:
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(OBTER_PLANO_POR_ID, (plano_id,))
            row = cursor.fetchone()
            if row:
                return Plano(
                    id_plano=row["id_plano"],
                    nome_plano=row["nome_plano"],
                    valor_mensal=row["valor_mensal"],
                    limite_servico=row["limite_servico"],
                    tipo_plano=row["tipo_plano"],
                    descricao=row["descricao"],
                )
            return None  # Corrigido


def obter_plano_por_pagina(pagina: int, tamanho_pagina: int) -> List[Plano]:
    offset = (pagina - 1) * tamanho_pagina
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_PLANO_POR_PAGINA, (tamanho_pagina, offset))
        rows = cursor.fetchall()
        return [
            Plano(
                id_plano=row["id_plano"],
                nome_plano=row["nome_plano"],
                valor_mensal=row["valor_mensal"],
                limite_servico=row["limite_servico"],
                tipo_plano=row["tipo_plano"],
                descricao=row["descricao"],
            )
            for row in rows
        ]


def atualizar_plano_por_id(plano: Plano):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_PLANO_POR_ID,
            (
                plano.nome_plano,
                plano.valor_mensal,
                plano.limite_servico,
                plano.tipo_plano,
                plano.descricao,
                plano.id_plano,
            ),
        )
        conn.commit()
        return cursor.rowcount > 0


def deletar_plano(id_plano: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_PLANO, (id_plano,))
        conn.commit()
        return cursor.rowcount > 0
