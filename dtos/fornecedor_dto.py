from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import *
from enum import Enum
from datetime import date
from .usuario.usuario_dto import AtualizarUsuarioDTO, CriarUsuarioDTO


class CriarFornecedorDTO(CriarUsuarioDTO):
    razao_social: Optional[str] = Field(
        None, description="Razão Social da empresa", max_length=100
    )
    selo_confianca: bool = Field(default=False)

    # Validador desabilitado temporariamente para evitar recursão
    # @field_validator('razao_social')
    # @classmethod
    # def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
    #     return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)

    @classmethod
    def criar_exemplo_fornecedor_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "razao_social": "Fornecedor de Materiais Ltda",
            "selo_confianca": False,
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarFornecedorDTO(AtualizarUsuarioDTO):

    razao_social: Optional[str] = Field(None, description="Razão Social da empresa")
    selo_confianca: Optional[bool] = Field(None, description="Selo de confiança")

    @field_validator("razao_social")
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Razão Social",
        )(v)


CriarFornecedorDTO.model_config.update(
    {
        "json_schema_extra": {
            "example": CriarFornecedorDTO.criar_exemplo_fornecedor_json()
        }
    }
)


class ProdutoDTO(BaseDTO):
    pass


class PromocaoDTO(BaseDTO):
    pass
