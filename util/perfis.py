"""
Enum centralizado para perfis de usuário do OBRATTO.

FONTE ÚNICA DA VERDADE para perfis no sistema.
SEMPRE use este Enum, NUNCA strings literais em código.
"""
from enum import Enum
from typing import Optional


class Perfil(str, Enum):
    """
    Enum de perfis de usuário do sistema OBRATTO.
    
    Garante consistência em todo o sistema evitando erros de digitação
    e facilitando refatoração.
    """
    
    ADMINISTRADOR = "Administrador"
    CLIENTE = "Cliente"
    FORNECEDOR = "Fornecedor"
    PRESTADOR = "Prestador"
    
    def __str__(self) -> str:
        """Retorna o valor do enum como string"""
        return self.value
    
    @classmethod
    def valores(cls) -> list[str]:
        """Retorna lista de todos os valores de perfis"""
        return [perfil.value for perfil in cls]
    
    @classmethod
    def existe(cls, valor: str) -> bool:
        """Verifica se um valor de perfil é válido"""
        return valor in cls.valores()
    
    @classmethod
    def from_string(cls, valor: str) -> Optional['Perfil']:
        """
        Converte string para Enum Perfil (case-insensitive)
        
        Args:
            valor: String do perfil (ex: "administrador", "Admin", "CLIENTE")
        
        Returns:
            Perfil ou None se não encontrado
        """
        # Normalizar entrada
        valor_normalizado = valor.strip().lower()
        
        # Tentar match exato primeiro
        try:
            return cls(valor)
        except ValueError:
            pass
        
        # Tentar match case-insensitive
        for perfil in cls:
            if perfil.value.lower() == valor_normalizado:
                return perfil
        
        return None
    
    @classmethod
    def validar(cls, valor: str) -> str:
        """
        Valida e retorna o valor, levantando exceção se inválido
        
        Args:
            valor: Valor do perfil a validar
        
        Returns:
            Valor normalizado do perfil
        
        Raises:
            ValueError: Se perfil inválido
        """
        perfil = cls.from_string(valor)
        if not perfil:
            raise ValueError(
                f'Perfil inválido: {valor}. '
                f'Valores permitidos: {", ".join(cls.valores())}'
            )
        return perfil.value
    
    @classmethod
    def perfis_cadastro_publico(cls) -> list[str]:
        """
        Retorna perfis que podem se auto-cadastrar no sistema
        (exclui Administrador que deve ser criado manualmente)
        """
        return [
            cls.CLIENTE.value,
            cls.FORNECEDOR.value,
            cls.PRESTADOR.value
        ]
    
    def normalizado(self) -> str:
        """Retorna perfil em minúsculas para comparações"""
        return self.value.lower()
    
    def __eq__(self, other) -> bool:
        """Permite comparação case-insensitive"""
        if isinstance(other, str):
            return self.value.lower() == other.lower()
        return super().__eq__(other)
