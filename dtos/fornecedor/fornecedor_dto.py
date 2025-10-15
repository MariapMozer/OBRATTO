from pydantic import EmailStr, Field, field_validator
from typing import Optional
from ..base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
from ..base_dto import BaseDTO
from ..usuario.usuario_dto import AtualizarUsuarioDTO, CriarUsuarioDTO

class CriarFornecedorDTO(CriarUsuarioDTO):
    razao_social: Optional[str] = Field(None, description="Razão Social da empresa", max_length=100)
    selo_confianca: bool = Field(default=False)

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social_criar(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Razão Social"
        )(v)

    
class AtualizarFornecedorDTO(AtualizarUsuarioDTO):

    razao_social: Optional[str] = Field(None, description="Razão Social da empresa")
    selo_confianca: Optional[bool] = Field(None, description="Selo de confiança")

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Razão Social"
        )(v)

class ProdutoDTO(BaseDTO):
    pass

class PromocaoDTO(BaseDTO):
    pass