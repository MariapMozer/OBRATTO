# ...existing code...
from pydantic import Field, field_validator
from typing import Optional
from ..base_dto import BaseDTO


class CriarPrestadorDTO(BaseDTO):
    area_atuacao: Optional[str] = Field(None, description="Área de atuação", max_length=100)
    razao_social: Optional[str] = Field(None, description="Razão Social", max_length=100)
    descricao_servicos: Optional[str] = Field(None, description="Descrição dos serviços", max_length=500)
    selo_confianca: bool = Field(default=False, description="Selo de confiança")

    @field_validator("area_atuacao")
    @classmethod
    def validar_area_atuacao(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 100:
            raise ValueError("Área de atuação deve ter no máximo 100 caracteres.")
        return v

    @field_validator("razao_social")
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 100:
            raise ValueError("Razão Social deve ter no máximo 100 caracteres.")
        return v

    @field_validator("descricao_servicos")
    @classmethod
    def validar_descricao_servicos(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 500:
            raise ValueError("Descrição dos serviços deve ter no máximo 500 caracteres.")
        return v

    @staticmethod
    def criar_exemplo_json(**overrides) -> dict:
        exemplo = {
            "area_atuacao": "Manutenção",
            "razao_social": "Prestadora de Serviços Ltda",
            "descricao_servicos": "Oferecemos serviços de manutenção residencial e comercial.",
            "selo_confianca": True
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarPrestadorDTO(BaseDTO):
    area_atuacao: Optional[str] = Field(None, description="Área de atuação", max_length=100)
    razao_social: Optional[str] = Field(None, description="Razão Social", max_length=100)
    descricao_servicos: Optional[str] = Field(None, description="Descrição dos serviços", max_length=500)
    selo_confianca: Optional[bool] = Field(None, description="Selo de confiança")

    @field_validator("area_atuacao")
    @classmethod
    def validar_area_atuacao(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 100:
            raise ValueError("Área de atuação deve ter no máximo 100 caracteres.")
        return v

    @field_validator("razao_social")
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 100:
            raise ValueError("Razão Social deve ter no máximo 100 caracteres.")
        return v

    @field_validator("descricao_servicos")
    @classmethod
    def validar_descricao_servicos(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 500:
            raise ValueError("Descrição dos serviços deve ter no máximo 500 caracteres.")
        return v

    @staticmethod
    def criar_exemplo_json(**overrides) -> dict:
        exemplo = {
            "area_atuacao": "Instalação elétrica",
            "razao_social": "Eletricista Exemplo ME",
            "descricao_servicos": "Instalação e reparos elétricos residenciais.",
            "selo_confianca": False
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON para documentação
CriarPrestadorDTO.model_config.update({
    "json_schema_extra": {"example": CriarPrestadorDTO.criar_exemplo_json()}
})
AtualizarPrestadorDTO.model_config.update({
    "json_schema_extra": {"example": AtualizarPrestadorDTO.criar_exemplo_json()}
})
