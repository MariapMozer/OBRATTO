from typing import List, Optional
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano.inscricao_plano_sql import *
from util.db import open_connection


def criar_tabela_inscricao_plano() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_INSCRICAO_PLANO)
        conn.commit()
        return True


def inserir_inscricao_plano(inscricao_plano: InscricaoPlano) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            INSERIR_INSCRICAO_PLANO,
            (
                inscricao_plano.id_fornecedor,
                inscricao_plano.id_prestador,
                inscricao_plano.id_plano,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def obter_inscricao_plano() -> List[InscricaoPlano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_INSCRICAO_PLANO)
        rows = cursor.fetchall()
        inscricoes = []
        for row in rows:
            inscricoes.append(
                InscricaoPlano(
                    id_inscricao_plano=row["id_inscricao_plano"],
                    id_plano=row["id_plano"],
                    id_fornecedor=row["id_fornecedor"],
                    id_prestador=row["id_prestador"],
                )
            )
        return inscricoes


def obter_inscricao_plano_por_id(id_inscricao: int) -> Optional[InscricaoPlano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_INSCRICAO_PLANO_POR_ID, (id_inscricao,))
        row = cursor.fetchone()
        if row:
            return InscricaoPlano(
                id_inscricao_plano=row["id_inscricao_plano"],
                id_plano=row["id_plano"],
                id_fornecedor=row["id_fornecedor"],
                id_prestador=row["id_prestador"],
            )
        return None


def obter_inscricao_plano_por_pagina(
    pagina: int, tamanho_pagina: int
) -> List[InscricaoPlano]:
    offset = (pagina - 1) * tamanho_pagina
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_INSCRICAO_PLANO_POR_PAGINA, (tamanho_pagina, offset))
        rows = cursor.fetchall()
        return [
            InscricaoPlano(
                id_inscricao_plano=row["id_inscricao_plano"],
                id_plano=row["id_plano"],
                id_fornecedor=row["id_fornecedor"],
                id_prestador=row["id_prestador"],
            )
            for row in rows
        ]


def atualizar_inscricao_plano(inscricao_plano: InscricaoPlano) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            ATUALIZAR_INSCRICAO_PLANO,
            (
                inscricao_plano.id_fornecedor,
                inscricao_plano.id_prestador,
                inscricao_plano.id_plano,
                inscricao_plano.id_inscricao_plano,
            ),
        ),
        conn.commit()
        return cursor.rowcount > 0


def deletar_inscricao_plano(id_inscricao: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_INSCRICAO_PLANO, (id_inscricao,))
        conn.commit()
        return cursor.rowcount > 0


def obter_assinatura_ativa_por_fornecedor(
    id_fornecedor: int,
) -> Optional[InscricaoPlano]:
    """
    Retorna a inscrição ativa do fornecedor, se existir.
    Considera como ativa a inscrição mais recente do fornecedor.
    """
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM inscricao_plano
            WHERE id_fornecedor = ?
            ORDER BY id_inscricao_plano DESC LIMIT 1
        """,
            (id_fornecedor,),
        )
        row = cursor.fetchone()
        if row:
            return InscricaoPlano(
                id_inscricao_plano=row["id_inscricao_plano"],
                id_plano=row["id_plano"],
                id_fornecedor=row["id_fornecedor"],
            )
        return None


def obter_assinatura_ativa_por_prestador(id_prestador: int) -> Optional[InscricaoPlano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute((id_prestador,))
        row = cursor.fetchone()
        if row:
            return InscricaoPlano(
                id_inscricao_plano=row["id_inscricao_plano"],
                id_plano=row["id_plano"],
                id_prestador=row["id_prestador"],
            )
        return None


def obter_inscricao_por_prestador(id_prestador: int) -> Optional[InscricaoPlano]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT * FROM inscricao_plano
            WHERE id_prestador = ? 
            ORDER BY id_inscricao_plano DESC LIMIT 1
        """,
            (id_prestador,),
        )
        row = cursor.fetchone()
        if row:
            return InscricaoPlano(
                id_inscricao_plano=row["id_inscricao_plano"],
                id_plano=row["id_plano"],
                id_fornecedor=row["id_fornecedor"],
                id_prestador=row["id_prestador"],
            )
        return None
