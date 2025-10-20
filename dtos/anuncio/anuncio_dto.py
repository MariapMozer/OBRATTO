from pydantic import Field, field_validator
from typing import Optional
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_obrigatorio


class CriarAnuncioDTO(BaseDTO):
    """
    DTO para criação de novo anúncio.
    Usado em formulários de cadastro de anúncios.
    """

    nome_anuncio: str = Field(..., description="Nome do anúncio")
    descricao: str = Field(..., description="Descrição do anúncio")
    preco: float = Field(..., gt=0, description="Preço do anúncio")

    @field_validator('nome_anuncio')
    @classmethod
    def validar_nome_anuncio(cls, v: str) -> str:
        return validar_texto_obrigatorio(v, "Nome do anúncio", min_chars=5, max_chars=150)

    @field_validator('descricao')
    @classmethod
    def validar_descricao_anuncio(cls, v: str) -> str:
        return validar_texto_obrigatorio(v, "Descrição", min_chars=20, max_chars=1000)

    @field_validator('preco')
    @classmethod
    def validar_preco_anuncio(cls, v: float) -> float:
        if v <= 0:
            raise ValueError('Preço deve ser maior que zero')
        if v > 1000000:
            raise ValueError('Preço não pode exceder R$ 1.000.000,00')
        return v


class AlterarAnuncioDTO(BaseDTO):
    """
    DTO para alteração de anúncio existente.
    Todos os campos são opcionais.
    """

    nome_anuncio: Optional[str] = Field(None, min_length=5, max_length=150, description="Nome do anúncio")
    descricao: Optional[str] = Field(None, min_length=20, max_length=1000, description="Descrição do anúncio")
    preco: Optional[float] = Field(None, gt=0, description="Preço do anúncio")

    @field_validator('nome_anuncio')
    @classmethod
    def validar_nome_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_texto_obrigatorio(v, "Nome do anúncio", min_chars=5, max_chars=150)
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_texto_obrigatorio(v, "Descrição", min_chars=20, max_chars=1000)
        return v

    @field_validator('preco')
    @classmethod
    def validar_preco_alterar(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            if v <= 0:
                raise ValueError('Preço deve ser maior que zero')
            if v > 1000000:
                raise ValueError('Preço não pode exceder R$ 1.000.000,00')
        return v


class ExcluirAnuncioDTO(BaseDTO):
    """
    DTO para exclusão de anúncio.
    """

    id_anuncio: int = Field(..., gt=0, description="ID do anúncio a ser excluído")

    @field_validator('id_anuncio')
    @classmethod
    def validar_id_anuncio(cls, v: int) -> int:
        if v <= 0:
            raise ValueError('ID do anúncio deve ser maior que zero')
        return v
