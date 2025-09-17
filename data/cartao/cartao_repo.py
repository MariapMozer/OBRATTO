from utils.db import open_connection
from data.cartao.cartao_model import CartaoCredito
from data.cartao import cartao_sql 
from typing import List, Optional
from datetime import datetime
import hashlib

class CartaoRepository:
    """Repository para gerenciamento de cartões de crédito"""

    def definir_todos_nao_principal(self, id_fornecedor: int) -> bool:
        """Define todos os cartões do fornecedor como não principal"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(
                    "UPDATE cartao_credito SET principal = 0, data_atualizacao = ? WHERE id_fornecedor = ?",
                    (datetime.now().isoformat(), id_fornecedor)
                )
                con.commit()
                return True
        except Exception as e:
            print(f"Erro ao definir todos como não principal: {e}")
            return False

    def criar_tabela_cartao(self):
        """Cria a tabela de cartões se não existir"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(cartao_sql.SQL_CRIAR_TABELA_CARTAO)
                con.commit()
            return True
        except Exception as e:
            print(f"Erro ao criar tabela cartao_credito: {e}")
            return False
    
    def criptografar_numero_cartao(self, numero_cartao: str) -> str:
        """Criptografa o número do cartão para armazenamento seguro"""
        # Em produção, use uma biblioteca de criptografia mais robusta
        return hashlib.sha256(numero_cartao.encode()).hexdigest()
    
    def obter_ultimos_4_digitos(self, numero_cartao: str) -> str:
        """Extrai os últimos 4 dígitos do cartão"""
        numero_limpo = numero_cartao.replace(" ", "").replace("-", "")
        return numero_limpo[-4:] if len(numero_limpo) >= 4 else numero_limpo
    
    def detectar_bandeira(self, numero_cartao: str) -> str:
        """Detecta a bandeira do cartão baseado no número"""
        numero_limpo = numero_cartao.replace(" ", "").replace("-", "")
        primeiro_digito = numero_limpo[0] if numero_limpo else ""
        
        if primeiro_digito == "4":
            return "Visa"
        elif primeiro_digito == "5":
            return "Mastercard"
        elif primeiro_digito == "3":
            return "American Express"
        elif primeiro_digito == "6":
            return "Discover"
        else:
            return "Outros"
    
    def inserir_cartao(self, cartao: CartaoCredito) -> Optional[int]:
        """Insere um novo cartão"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                
                # Se é o primeiro cartão ou definido como principal, 
                # remover status principal de outros
                if cartao.principal:
                    cursor.execute(
                        cartao_sql.SQL_REMOVER_PRINCIPAL_OUTROS,
                        (datetime.now().isoformat(), cartao.id_fornecedor, 0)
                    )
                
                cursor.execute(cartao_sql.SQL_INSERIR_CARTAO, (
                    cartao.id_fornecedor,
                    cartao.nome_titular,
                    cartao.numero_cartao_criptografado,
                    cartao.ultimos_4_digitos,
                    cartao.mes_vencimento,
                    cartao.ano_vencimento,
                    cartao.bandeira,
                    cartao.apelido,
                    cartao.principal,
                    cartao.ativo,
                    cartao.data_criacao,
                    cartao.data_atualizacao
                ))
                
                cartao_id = cursor.lastrowid
                con.commit()
                return cartao_id
                
        except Exception as e:
            print(f"Erro ao inserir cartão: {e}")
            return None
    
    def obter_cartoes_fornecedor(self, id_fornecedor: int) -> List[CartaoCredito]:
        """Obtém todos os cartões ativos de um fornecedor"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(cartao_sql.SQL_OBTER_CARTOES_FORNECEDOR, (id_fornecedor,))
                rows = cursor.fetchall()
                
                cartoes = []
                for row in rows:
                    cartao = CartaoCredito(
                        id_cartao=row[0],
                        id_fornecedor=row[1],
                        nome_titular=row[2],
                        numero_cartao_criptografado=row[3],
                        ultimos_4_digitos=row[4],
                        mes_vencimento=row[5],
                        ano_vencimento=row[6],
                        bandeira=row[7],
                        apelido=row[8],
                        principal=bool(row[9]),
                        ativo=bool(row[10]),
                        data_criacao=row[11],
                        data_atualizacao=row[12]
                    )
                    cartoes.append(cartao)
                
                return cartoes
                
        except Exception as e:
            print(f"Erro ao obter cartões: {e}")
            return []
        


    def obter_cartoes_por_prestador(self, id_prestador: int) -> List[CartaoCredito]:
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(cartao_sql.SQL_OBTER_CARTOES_POR_PRESTADOR, (id_prestador,))
                rows = cursor.fetchall()
                
                cartoes = []
                for row in rows:
                    cartao = CartaoCredito(
                        id_cartao=row[0],
                        id_prestador=row[1],
                        nome_titular=row[2],
                        numero_cartao_criptografado=row[3],
                        ultimos_4_digitos=row[4],
                        mes_vencimento=row[5],
                        ano_vencimento=row[6],
                        bandeira=row[7],
                        apelido=row[8],
                        principal=bool(row[9]),
                        ativo=bool(row[10]),
                        data_criacao=row[11],
                        data_atualizacao=row[12]
                    )
                    cartoes.append(cartao)
                
                return cartoes
                
        except Exception as e:
            print(f"Erro ao obter cartões: {e}")
            return []
          
    
    def obter_cartao_por_id(self, id_cartao: int) -> Optional[CartaoCredito]:
        """Obtém um cartão específico por ID"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(cartao_sql.SQL_OBTER_CARTAO_POR_ID, (id_cartao,))
                row = cursor.fetchone()
                
                if row:
                    return CartaoCredito(
                        id_cartao=row[0],
                        id_fornecedor=row[1],
                        nome_titular=row[2],
                        numero_cartao_criptografado=row[3],
                        ultimos_4_digitos=row[4],
                        mes_vencimento=row[5],
                        ano_vencimento=row[6],
                        bandeira=row[7],
                        apelido=row[8],
                        principal=bool(row[9]),
                        ativo=bool(row[10]),
                        data_criacao=row[11],
                        data_atualizacao=row[12]
                    )
                return None
                
        except Exception as e:
            print(f"Erro ao obter cartão: {e}")
            return None
    
    def obter_cartao_principal(self, id_fornecedor: int) -> Optional[CartaoCredito]:
        """Obtém o cartão principal do fornecedor"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(cartao_sql.SQL_OBTER_CARTAO_PRINCIPAL, (id_fornecedor,))
                row = cursor.fetchone()
                
                if row:
                    return CartaoCredito(
                        id_cartao=row[0],
                        id_fornecedor=row[1],
                        nome_titular=row[2],
                        numero_cartao_criptografado=row[3],
                        ultimos_4_digitos=row[4],
                        mes_vencimento=row[5],
                        ano_vencimento=row[6],
                        bandeira=row[7],
                        apelido=row[8],
                        principal=bool(row[9]),
                        ativo=bool(row[10]),
                        data_criacao=row[11],
                        data_atualizacao=row[12]
                    )
                return None
                
        except Exception as e:
            print(f"Erro ao obter cartão principal: {e}")
            return None
    
    def atualizar_cartao(self, cartao: CartaoCredito) -> bool:
        """Atualiza dados do cartão"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                
                # Se está definindo como principal, remover de outros
                if cartao.principal:
                    cursor.execute(
                        cartao_sql.SQL_REMOVER_PRINCIPAL_OUTROS,
                        (datetime.now().isoformat(), cartao.id_fornecedor, cartao.id_cartao)
                    )
                
                cursor.execute(cartao_sql.SQL_ATUALIZAR_CARTAO, (
                    cartao.nome_titular,
                    cartao.apelido,
                    cartao.principal,
                    datetime.now().isoformat(),
                    cartao.id_cartao
                ))
                
                con.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao atualizar cartão: {e}")
            return False
    
    def definir_cartao_principal(self, id_cartao: int, id_fornecedor: int) -> bool:
        """Define um cartão como principal"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                
                # Remover status principal de outros cartões
                cursor.execute(
                    cartao_sql.SQL_REMOVER_PRINCIPAL_OUTROS,
                    (datetime.now().isoformat(), id_fornecedor, id_cartao)
                )
                
                # Definir este cartão como principal
                cursor.execute(
                    cartao_sql.SQL_DEFINIR_PRINCIPAL,
                    (datetime.now().isoformat(), id_cartao)
                )
                
                con.commit()
                return True
                
        except Exception as e:
            print(f"Erro ao definir cartão principal: {e}")
            return False
    
    def excluir_cartao(self, id_cartao: int) -> bool:
        """Exclui (desativa) um cartão"""
        try:
            with open_connection() as con:
                cursor = con.cursor()
                cursor.execute(
                    cartao_sql.SQL_DESATIVAR_CARTAO,
                    (datetime.now().isoformat(), id_cartao)
                )
                con.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            print(f"Erro ao excluir cartão: {e}")
            return False
    
    def criar_cartao_from_form(self, id_fornecedor: int, numero_cartao: str, 
                              nome_titular: str, mes_vencimento: str, 
                              ano_vencimento: str, apelido: str, principal: bool = False) -> Optional[int]:
        """
        Método conveniente para criar cartão a partir dos dados do formulário
        """
        try:
            # Processar dados do cartão
            numero_limpo = numero_cartao.replace(' ', '').replace('-', '')
            
            # Criar objeto cartão
            cartao = CartaoCredito(
                id_cartao=0,  # Será definido pelo banco
                id_fornecedor=id_fornecedor,
                nome_titular=nome_titular.strip().upper(),
                numero_cartao_criptografado=self.criptografar_numero_cartao(numero_limpo),
                ultimos_4_digitos=self.obter_ultimos_4_digitos(numero_limpo),
                mes_vencimento=mes_vencimento,
                ano_vencimento=ano_vencimento,
                bandeira=self.detectar_bandeira(numero_limpo),
                apelido=apelido.strip(),
                principal=principal,
                ativo=True
            )
            
            return self.inserir_cartao(cartao)
            
        except Exception as e:
            print(f"Erro ao criar cartão: {e}")
            return None

# Instância global do repositório
cartao_repo = CartaoRepository()
