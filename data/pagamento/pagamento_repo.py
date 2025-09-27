
"""
Repositório para pagamentos
"""
from typing import List, Optional
from utils.db import open_connection
from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_sql import *
from datetime import datetime

class PagamentoRepository:
    def criar_tabela_pagamento(self):
        """Cria a tabela de pagamentos"""
        with open_connection() as conexao:
            cursor = conexao.cursor()
            cursor.execute(SQL_CRIAR_TABELA_PAGAMENTO)
            conexao.commit()

    def inserir_pagamento(self, pagamento: Pagamento) -> Optional[int]:
        """Insere um novo pagamento"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_INSERIR_PAGAMENTO, (
                    pagamento.plano_id,
                    pagamento.fornecedor_id,
                    pagamento.mp_payment_id,
                    pagamento.mp_preference_id,
                    pagamento.valor,
                    pagamento.status,
                    pagamento.metodo_pagamento,
                    pagamento.data_criacao,
                    pagamento.data_aprovacao,
                    pagamento.external_reference
                ))
                conexao.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao inserir pagamento: {e}")
            return None

    def obter_pagamento_por_id(self, id_pagamento: int) -> Optional[Pagamento]:
        """Obtém um pagamento pelo ID"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTO_POR_ID, (id_pagamento,))
                row = cursor.fetchone()
                
                if row:
                    return Pagamento(
                        id_pagamento=row[0],
                        plano_id=row[1],
                        fornecedor_id=row[2],
                        mp_payment_id=row[3],
                        mp_preference_id=row[4],
                        valor=row[5],
                        status=row[6],
                        metodo_pagamento=row[7],
                        data_criacao=row[8],
                        data_aprovacao=row[9],
                        external_reference=row[10]
                    )
        except Exception as e:
            print(f"Erro ao obter pagamento: {e}")
            return None

    def obter_pagamento_por_mp_id(self, mp_payment_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pelo ID do Mercado Pago"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTO_POR_MP_ID, (mp_payment_id,))
                row = cursor.fetchone()
                
                if row:
                    return Pagamento(
                        id_pagamento=row[0],
                        plano_id=row[1],
                        fornecedor_id=row[2],
                        mp_payment_id=row[3],
                        mp_preference_id=row[4],
                        valor=row[5],
                        status=row[6],
                        metodo_pagamento=row[7],
                        data_criacao=row[8],
                        data_aprovacao=row[9],
                        external_reference=row[10]
                    )
        except Exception as e:
            print(f"Erro ao obter pagamento por MP ID: {e}")
            return None

    def obter_pagamento_por_preference(self, mp_preference_id: str) -> Optional[Pagamento]:
        """Obtém um pagamento pelo ID da preferência do Mercado Pago"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTO_POR_PREFERENCE, (mp_preference_id,))
                row = cursor.fetchone()
                
                if row:
                    return Pagamento(
                        id_pagamento=row[0],
                        plano_id=row[1],
                        fornecedor_id=row[2],
                        mp_payment_id=row[3],
                        mp_preference_id=row[4],
                        valor=row[5],
                        status=row[6],
                        metodo_pagamento=row[7],
                        data_criacao=row[8],
                        data_aprovacao=row[9],
                        external_reference=row[10]
                    )
        except Exception as e:
            print(f"Erro ao obter pagamento por preference: {e}")
            return None

    def atualizar_status_pagamento(self, mp_payment_id: str, status: str, metodo_pagamento: str = None) -> bool:
        """Atualiza o status de um pagamento"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                data_aprovacao = datetime.now().isoformat() if status == "aprovado" else None
                
                cursor.execute(SQL_ATUALIZAR_STATUS_PAGAMENTO, (
                    status, 
                    data_aprovacao, 
                    metodo_pagamento, 
                    mp_payment_id
                ))
                conexao.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar status do pagamento: {e}")
            return False

    def obter_pagamentos_fornecedor(self, fornecedor_id: int) -> List[dict]:
        """Obtém todos os pagamentos de um fornecedor"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTOS_FORNECEDOR, (fornecedor_id,))
                rows = cursor.fetchall()
                
                pagamentos = []
                for row in rows:
                    pagamentos.append({
                        'id_pagamento': row[0],
                        'plano_id': row[1],
                        'fornecedor_id': row[2],
                        'mp_payment_id': row[3],
                        'mp_preference_id': row[4],
                        'valor': row[5],
                        'status': row[6],
                        'metodo_pagamento': row[7],
                        'data_criacao': row[8],
                        'data_aprovacao': row[9],
                        'external_reference': row[10],
                        'nome_plano': row[11] if len(row) > 11 else None
                    })
                
                return pagamentos
        except Exception as e:
            print(f"Erro ao obter pagamentos do fornecedor: {e}")
            return []
        
    def obter_pagamentos_prestador(self, prestador_id: int) -> List[dict]:
        """Obtém todos os pagamentos de um prestador"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTOS_PRESTADOR, (prestador_id,))
                rows = cursor.fetchall()
                
                pagamentos = []
                for row in rows:
                    pagamentos.append({
                        'id_pagamento': row[0],
                        'plano_id': row[1],
                        'prestador_id': row[2],
                        'mp_payment_id': row[3],
                        'mp_preference_id': row[4],
                        'valor': row[5],
                        'status': row[6],
                        'metodo_pagamento': row[7],
                        'data_criacao': row[8],
                        'data_aprovacao': row[9],
                        'external_reference': row[10],
                        'nome_plano': row[11] if len(row) > 11 else None
                    })
                
                return pagamentos
        except Exception as e:
            print(f"Erro ao obter pagamentos do prestador: {e}")
            return []


    def obter_pagamentos_por_status(self, status: str) -> List[dict]:
        """Obtém pagamentos por status"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_OBTER_PAGAMENTOS_POR_STATUS, (status,))
                rows = cursor.fetchall()
                
                pagamentos = []
                for row in rows:
                    pagamentos.append({
                        'id_pagamento': row[0],
                        'plano_id': row[1],
                        'fornecedor_id': row[2],
                        'mp_payment_id': row[3],
                        'mp_preference_id': row[4],
                        'valor': row[5],
                        'status': row[6],
                        'metodo_pagamento': row[7],
                        'data_criacao': row[8],
                        'data_aprovacao': row[9],
                        'external_reference': row[10],
                        'nome_plano': row[11] if len(row) > 11 else None
                    })
                
                return pagamentos
        except Exception as e:
            print(f"Erro ao obter pagamentos por status: {e}")
            return []

    def atualizar_pagamento(self, pagamento: Pagamento) -> bool:
        """Atualiza um pagamento existente"""
        try:
            with open_connection() as conexao:
                cursor = conexao.cursor()
                cursor.execute(SQL_ATUALIZAR_PAGAMENTO, (
                    pagamento.plano_id,
                    pagamento.prestador_id,
                    pagamento.mp_payment_id,
                    pagamento.mp_preference_id,
                    pagamento.valor,
                    pagamento.status,
                    pagamento.metodo_pagamento,
                    pagamento.data_criacao,
                    pagamento.data_aprovacao,
                    pagamento.external_reference,
                    pagamento.id_pagamento
                ))
                conexao.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar pagamento: {e}")
            return False
