from datetime import datetime
import sqlite3
from typing import Optional, List
from data.fornecedor.fornecedor_model import Fornecedor
from data.fornecedor.fornecedor_sql import * 
from data.usuario.usuario_repo import inserir_usuario
from utils.db import open_connection

def criar_tabela_fornecedor() -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS fornecedor")
        cursor.execute(CRIAR_TABELA_FORNECEDOR)
        conn.commit()
        return True

def inserir_fornecedor(fornecedor: Fornecedor) -> Optional[int]:
    with open_connection() as conn:
        cursor = conn.cursor()
        id_usuario_gerado = inserir_usuario(fornecedor)

        if id_usuario_gerado:
            cursor.execute(INSERIR_FORNECEDOR, (
                id_usuario_gerado,
                fornecedor.razao_social,
                int(getattr(fornecedor, 'selo_confianca', False))
            ))
            conn.commit()
            return id_usuario_gerado
        return None

def obter_fornecedor() -> List[Fornecedor]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_FORNECEDOR)
        rows = cursor.fetchall()
        fornecedores = []
        for row in rows:
            fornecedores.append(Fornecedor(
                id=row["id"],
                nome=row["nome"],
                email=row["email"],
                senha=None,
                cpf_cnpj=None,
                telefone=None,
                cep="",  # Campo adicionado
                estado=row["estado"],
                cidade=row["cidade"],
                rua=row["rua"],
                numero=row["numero"],
                complemento="",  # Campo adicionado
                bairro=row["bairro"],
                data_cadastro=None,
                razao_social=row["razao_social"],
                selo_confianca=bool(row["selo_confianca"]) if "selo_confianca" in row.keys() else False,
                tipo_usuario=row["tipo_usuario"]
            ))
        return fornecedores

def obter_fornecedor_por_id(fornecedor_id: int) -> Optional[Fornecedor]:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(OBTER_FORNECEDOR_POR_ID, (fornecedor_id,))
        row = cursor.fetchone()
        if row:
            # Converter para dict para permitir uso de .get() e evitar AttributeError
            row = dict(row)
            data_cadastro = row.get("data_cadastro")
            if isinstance(data_cadastro, str):
                try:
                    data_cadastro = datetime.fromisoformat(data_cadastro)
                except Exception:
                    # manter como string se não for ISO
                    pass

            return Fornecedor(
                id=row.get("id"),
                nome=row.get("nome"),
                email=row.get("email"),
                senha=row.get("senha"),
                cpf_cnpj=row.get("cpf_cnpj"),
                telefone=row.get("telefone"),
                cep=row.get("cep", ""),  # Campo adicionado com fallback
                estado=row.get("estado"),
                cidade=row.get("cidade"),
                rua=row.get("rua"),
                numero=row.get("numero"),
                complemento=row.get("complemento", ""),  # Campo adicionado com fallback
                bairro=row.get("bairro"),
                data_cadastro=data_cadastro,
                razao_social=row.get("razao_social"),
                selo_confianca=bool(row.get("selo_confianca", False)),
                tipo_usuario=row.get("tipo_usuario")
            )
        return None
    
def obter_fornecedor_por_pagina(conn, limit: int, offset: int) -> list[Fornecedor]:
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()
    cursor.execute(OBTER_FORNECEDOR_POR_PAGINA,(limit, offset))
    rows = cursor.fetchall()
    # Converter cada row para dict para permitir .get()
    rows = [dict(r) for r in rows]
    return [
        Fornecedor(
            id=row.get("id"),
            nome=row.get("nome"),
            email=row.get("email"),
            senha=row.get("senha"),
            cpf_cnpj=row.get("cpf_cnpj"),
            telefone=row.get("telefone"),
            cep=row.get("cep", ""),  # Campo adicionado com fallback
            estado=row.get("estado"),
            cidade=row.get("cidade"),
            rua=row.get("rua"),
            numero=row.get("numero"),
            complemento=row.get("complemento", ""),  # Campo adicionado com fallback
            bairro=row.get("bairro"),
            data_cadastro=row.get("data_cadastro"),
            razao_social=row.get("razao_social"),
            selo_confianca=bool(row.get("selo_confianca", False)),
            tipo_usuario=row.get("tipo_usuario")
        )
        for row in rows
    ]

def obter_fornecedor_por_email(email: str) -> Optional[Fornecedor]:
    with open_connection() as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(OBTER_FORNECEDOR_POR_EMAIL, (email,))
        row = cursor.fetchone()
        if row:
            row = dict(row)
            data_cadastro = row.get("data_cadastro")
            if isinstance(data_cadastro, str):
                try:
                    data_cadastro = datetime.fromisoformat(data_cadastro)
                except Exception:
                    pass

            return Fornecedor(
                id=row.get("id"),
                nome=row.get("nome"),
                email=row.get("email"),
                senha=row.get("senha"),
                cpf_cnpj=row.get("cpf_cnpj"),
                telefone=row.get("telefone"),
                cep=row.get("cep", ""),  # Campo adicionado com fallback
                estado=row.get("estado"),
                cidade=row.get("cidade"),
                rua=row.get("rua"),
                numero=row.get("numero"),
                complemento=row.get("complemento", ""),  # Campo adicionado com fallback
                bairro=row.get("bairro"),
                data_cadastro=data_cadastro,
                razao_social=row.get("razao_social"),
                selo_confianca=bool(row.get("selo_confianca", False)),
                tipo_usuario=row.get("tipo_usuario")
            )
        return None

def atualizar_fornecedor(fornecedor: Fornecedor) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()

        # Atualiza os dados do usuário (herança)
        cursor.execute("""
            UPDATE usuario
            SET nome = ?, email = ?, senha = ?, cpf_cnpj = ?, telefone = ?,
                data_cadastro = ?, endereco = ?
            WHERE id = ?
        """, (
            fornecedor.nome,
            fornecedor.email,
            fornecedor.senha,
            fornecedor.cpf_cnpj,
            fornecedor.telefone,
            fornecedor.estado,
            fornecedor.cidade,
            fornecedor.rua,
            fornecedor.numero,
            fornecedor.bairro,
            fornecedor.data_cadastro.isoformat() if isinstance(fornecedor.data_cadastro, datetime) else fornecedor.data_cadastro,
            fornecedor.id
        ))

        # Atualiza os dados específicos do fornecedor
        cursor.execute("""
            UPDATE fornecedor
            SET razao_social = ?, selo_confianca = ?
            WHERE id = ?
        """, (
            fornecedor.razao_social,
            int(getattr(fornecedor, 'selo_confianca', False)),
            fornecedor.id
        ))

        conn.commit()
        return cursor.rowcount > 0  # Pode melhorar para checar as duas queries se quiser



def deletar_fornecedor(fornecedor_id: int) -> bool:
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(DELETAR_FORNECEDOR, (fornecedor_id,))
        conn.commit()
        return cursor.rowcount > 0

