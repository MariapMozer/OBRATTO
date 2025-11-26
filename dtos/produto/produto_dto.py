from pydantic import Field, field_validator
from typing import Optional
from ..base_dto import BaseDTO
from util.validacoes_dto import validar_texto_obrigatorio


class ProdutoValidationMixin:
    """
    Mixin contendo validadores compartilhados para DTOs de Produto.
    Evita duplicação de código de validação entre DTOs de criação e alteração.
    """

    @staticmethod
    def _validar_nome(v: str) -> str:
        """Valida o nome do produto"""
        return validar_texto_obrigatorio(
            v, "Nome do produto", min_chars=3, max_chars=100
        )

    @staticmethod
    def _validar_descricao(v: str) -> str:
        """Valida a descrição do produto"""
        return validar_texto_obrigatorio(v, "Descrição", min_chars=10, max_chars=500)

    @staticmethod
    def _validar_preco(v: float) -> float:
        """Valida o preço do produto"""
        if v <= 0:
            raise ValueError("Preço deve ser maior que zero")
        if v > 1000000:
            raise ValueError("Preço não pode exceder R$ 1.000.000,00")
        return v

    @staticmethod
    def _validar_quantidade(v: int) -> int:
        """Valida a quantidade do produto"""
        if v < 0:
            raise ValueError("Quantidade não pode ser negativa")
        if v > 100000:
            raise ValueError("Quantidade não pode exceder 100.000 unidades")
        return v


class CriarProdutoDTO(BaseDTO, ProdutoValidationMixin):
    """
    DTO para criação de novo produto.
    Usado em formulários de cadastro de produtos.
    """

    nome: str = Field(..., description="Nome do produto")
    descricao: str = Field(..., description="Descrição do produto")
    preco: float = Field(..., gt=0, description="Preço do produto")
    quantidade: int = Field(..., ge=0, description="Quantidade em estoque")
    foto: Optional[str] = Field(None, description="Caminho da foto do produto")
    em_promocao: bool = Field(default=False, description="Produto em promoção")
    desconto: float = Field(
        default=0.0, ge=0, le=100, description="Percentual de desconto"
    )

    @field_validator("nome")
    @classmethod
    def validar_nome_produto(cls, v: str) -> str:
        return cls._validar_nome(v)

    @field_validator("descricao")
    @classmethod
    def validar_descricao_produto(cls, v: str) -> str:
        return cls._validar_descricao(v)

    @field_validator("preco")
    @classmethod
    def validar_preco_produto(cls, v: float) -> float:
        return cls._validar_preco(v)

    @field_validator("quantidade")
    @classmethod
    def validar_quantidade_produto(cls, v: int) -> int:
        return cls._validar_quantidade(v)


class AlterarProdutoDTO(BaseDTO, ProdutoValidationMixin):
    """
    DTO para alteração de produto existente.
    Todos os campos são opcionais.
    """

    nome: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Nome do produto"
    )
    descricao: Optional[str] = Field(
        None, min_length=10, max_length=500, description="Descrição do produto"
    )
    preco: Optional[float] = Field(None, gt=0, description="Preço do produto")
    quantidade: Optional[int] = Field(None, ge=0, description="Quantidade em estoque")
    foto: Optional[str] = Field(None, description="Caminho da foto do produto")
    em_promocao: Optional[bool] = Field(None, description="Produto em promoção")
    desconto: Optional[float] = Field(
        None, ge=0, le=100, description="Percentual de desconto"
    )

    @field_validator("nome")
    @classmethod
    def validar_nome_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return cls._validar_nome(v)
        return v

    @field_validator("descricao")
    @classmethod
    def validar_descricao_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return cls._validar_descricao(v)
        return v

    @field_validator("preco")
    @classmethod
    def validar_preco_alterar(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            return cls._validar_preco(v)
        return v

    @field_validator("quantidade")
    @classmethod
    def validar_quantidade_alterar(cls, v: Optional[int]) -> Optional[int]:
        if v is not None:
            return cls._validar_quantidade(v)
        return v


class ExcluirProdutoDTO(BaseDTO):
    """
    DTO para exclusão de produto.
    """

    id: int = Field(..., gt=0, description="ID do produto a ser excluído")

    @field_validator("id")
    @classmethod
    def validar_id_produto(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ID do produto deve ser maior que zero")
        return v
