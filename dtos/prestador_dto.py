from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
from .base_dto import BaseDTO
from .usuario_dto import AtualizarUsuarioDTO, CriarUsuarioDTO

class CriarPrestadorDTO(CriarUsuarioDTO):
    area_atuacao: Optional[str] = Field(None)
    razao_social: Optional[str] = Field(None)
    descricao_servicos: Optional[str] = Field(None)
    selo_confianca: bool = Field(default=False)

    @field_validator('area_atuacao')
    @classmethod
    def validar_area_atuacao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Área de atuação", max_chars=100)(v)

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)

    @field_validator('descricao_servicos')
    @classmethod
    def validar_descricao_servicos(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Descrição dos serviços", max_chars=500)(v)


    @classmethod
    def criar_exemplo_prestador_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "area_atuacao": "Manutenção",
            "razao_social": "Prestadora de Serviços Ltda",
            "descricao_servicos": "Oferecemos serviços de manutenção residencial e comercial.",
        }
        exemplo.update(overrides)
        return exemplo
    
class AtualizarPrestadorDTO(AtualizarUsuarioDTO):

    area_atuacao: Optional[str] = Field(None, description="Área de atuação")
    razao_social: Optional[str] = Field(None, description="Razão Social")
    descricao_servicos: Optional[str] = Field(None, description="Descrição dos serviços")
    selo_confianca: Optional[bool] = Field(None, description="Selo de confiança")

    @field_validator('area_atuacao')
    @classmethod
    def validar_area_atuacao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Área de atuação", max_chars=100)(v)

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)

    @field_validator('descricao_servicos')
    @classmethod
    def validar_descricao_servicos(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Descrição dos serviços", max_chars=500)(v)

    
CriarPrestadorDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarPrestadorDTO.criar_exemplo_prestador_json()
    }
})