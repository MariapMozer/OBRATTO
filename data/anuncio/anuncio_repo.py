from typing import Optional, List
from data.anuncio.anuncio_model import Anuncio
from data.fornecedor.fornecedor_model import Fornecedor
from data.anuncio.anuncio_sql import *
from utils.db import open_connection

                        
def criar_tabela_anuncio() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(CRIAR_TABELA_ANUNCIO)
        conn.commit()
        return True


def inserir_anuncio(anuncio: Anuncio) -> Optional[int]:                # Insere dados específicos do anuncio.     
    with open_connection() as conn:                                    # O id_usuario deve existir na tabela usuario.
        cursor = conn.cursor()
        cursor.execute(INSERIR_ANUNCIO, (
            anuncio.id_anuncio,
            anuncio.nome_anuncio,
            anuncio.id_fornecedor,
            anuncio.data_criacao,
            anuncio.descricao,
            anuncio.preco
        ))
        conn.commit()
        return cursor.lastrowid


def obter_todos_anuncios() -> List[Anuncio]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_TODOS_ANUNCIOS)
        rows = cursor.fetchall()
        anuncio = []
        for row in rows:
            anuncio.append(Anuncio(
                id_anuncio=row["id_anuncio"],
                nome_anuncio=row["nome_anuncio"],
                id_fornecedor=row["id_fornecedor"],
                data_criacao=row["data_criacao"],
                descricao=row["descricao"],
                preco=row["preco"]
            ))
        return anuncio


def obter_anuncio_por_nome(anuncio_nome: str) -> Optional[Fornecedor]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ANUNCIO_POR_NOME, (anuncio_nome,))
        row = cursor.fetchone()
        if row:
            return Anuncio(
                 id_anuncio=row["id_anuncio"],
                nome_anuncio=row["nome_anuncio"],
                id_fornecedor=row["id_fornecedor"],
                data_criacao=row["data_criacao"],
                descricao=row["descricao"],
                preco=row["preco"]
            )
        return anuncio_nome
    

def obter_anuncio_por_id(anuncio_id: str) -> Optional[Anuncio]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_ANUNCIO_POR_ID, (anuncio_id,))
        row = cursor.fetchone()
        if row:
            return Anuncio(
                 id_anuncio=row["id_anuncio"],
                nome_anuncio=row["nome_anuncio"],
                id_fornecedor=row["id_fornecedor"],
                data_criacao=row["data_criacao"],
                descricao=row["descricao"],
                preco=row["preco"]
            )
        return anuncio_id


def atualizar_anuncio_por_nome(anuncio: Anuncio):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_ANUNCIO_POR_NOME, (
            anuncio.id_anuncio,
            anuncio.nome_anuncio,
            anuncio.id_fornecedor,
            anuncio.data_criacao,
            anuncio.descricao,
            anuncio.preco
        ))
        conn.commit()
        return cursor.rowcount > 0


def deletar_anuncio(id_anuncio: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_ANUNCIO, (id_anuncio,))
        conn.commit()
        return cursor.rowcount > 0
