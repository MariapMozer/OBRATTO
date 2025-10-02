from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
from .base_dto import BaseDTO
from .usuario_dto import AtualizarUsuarioDTO, CriarUsuarioDTO

class CriarFornecedor(CriarUsuarioDTO):
    razao_social: Optional[str] = Field(None, description="Razão Social da empresa")
    selo_confianca: bool = Field(default=False)

    field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)


    @classmethod
    def criar_exemplo_fornecedor_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "razao_social": "Fornecedor de Materiais Ltda"
        }
        exemplo.update(overrides)
        return exemplo
    
class AtualizarFornecedorDTO(AtualizarUsuarioDTO):

    razao_social: Optional[str] = Field(None, description="Razão Social da empresa")
    selo_confianca: Optional[bool] = Field(None, description="Selo de confiança")

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)
    
CriarFornecedor.model_config.update({
    "json_schema_extra": {
        "example": CriarFornecedor.criar_exemplo_fornecedor_json()
    }
})