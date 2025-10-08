from datetime import datetime
from pydantic import Field, field_validator
from typing import Optional
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_opcional


class CriarServicoDTO(BaseDTO):
    id_servico: int = Field(..., description="ID do serviço")
    id_prestador: int = Field(..., description="ID do prestador que oferece o serviço")
    titulo: str = Field(..., min_length=3, max_length=100)
    descricao: str = Field(..., min_length=10, max_length=500)
    categoria: str = Field(..., min_length=3, max_length=50)
    valor_base: float = Field(..., gt=0)
    nome_prestador: Optional[str] = Field(None, description="Nome do prestador")


    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Título"
        )(v)
    
    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição do serviço"
        )(v)

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Categoria"
        )(v)
    
    @field_validator('valor_base')
    @classmethod
    def validar_valor_base(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("O valor base deve ser maior que zero.")
        return v

    @classmethod
    def criar_exemplo_servico_json(cls, **overrides) -> dict:
        exemplo = {
            "titulo": "Serviço de Manutenção",
            "descricao": "Serviço completo de manutenção residencial.",
            "categoria": "Manutenção",
            "valor_base": 150.00
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarServicoDTO(BaseDTO):
    titulo: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, min_length=10, max_length=1500)
    categoria: Optional[str] = Field(None, min_length=3, max_length=50)
    valor_base: Optional[float] = Field(None, gt=0)

    @field_validator('titulo')
    @classmethod
    def validar_titulo(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Título"
        )(v)
    
    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=1500),
            "Descrição do serviço"
        )(v)

    @field_validator('categoria')
    @classmethod
    def validar_categoria(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Categoria"
        )(v)
    
    @field_validator('valor_base')
    @classmethod
    def validar_valor_base(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("O valor base deve ser maior que zero.")
        return v


CriarServicoDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarServicoDTO.criar_exemplo_servico_json()
    }
})
