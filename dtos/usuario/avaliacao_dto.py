from pydantic import Field, field_validator
from typing import Optional
from datetime import date
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_opcional


class CriarAvaliacaoDTO(BaseDTO):
    nota: int = Field(..., ge=0, le=5, description="Nota da avaliação (0 a 5)")
    data_avaliacao: date = Field(default_factory=date.today, description="Data da avaliação")
    descricao: Optional[str] = Field(None, min_length=5, max_length=500, description="Descrição da avaliação")
    nome_avaliador: str = Field(..., min_length=3, max_length=100, description="Nome de quem avaliou")
    nome_avaliado: str = Field(..., min_length=3, max_length=100, description="Nome de quem foi avaliado")

    @field_validator('nota')
    @classmethod
    def validar_nota(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 0 or v > 5):
            raise ValueError("A nota deve estar entre 0 e 5.")
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição da avaliação"
        )(v)

    @field_validator('nome_avaliador')
    @classmethod
    def validar_nome_avaliador(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome do avaliador"
        )(v)
    
    @field_validator('nome_avaliado')
    @classmethod
    def validar_nome_avaliado(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome do avaliado"
        )(v)

    @classmethod
    def criar_exemplo_avaliacao_json(cls, **overrides) -> dict:
        exemplo = {
            "nota": 5,
            "data_avaliacao": str(date.today()),
            "descricao": "Excelente serviço, recomendo!",
            "nome_avaliador": "Maria Souza",
            "nome_avaliado": "João Silva"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarAvaliacaoDTO(BaseDTO):
    nota: Optional[int] = Field(None, ge=0, le=5, description="Nota da avaliação (0 a 5)")
    data_avaliacao: Optional[date] = Field(None, description="Data da avaliação")
    descricao: Optional[str] = Field(None, min_length=5, max_length=500, description="Descrição da avaliação")
    nome_avaliador: Optional[str] = Field(None, min_length=3, max_length=100, description="Nome de quem avaliou")
    nome_avaliado: Optional[str] = Field(None, min_length=3, max_length=100, description="Nome de quem foi avaliado")

    @field_validator('nota')
    @classmethod
    def validar_nota(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and (v < 0 or v > 5):
            raise ValueError("A nota deve estar entre 0 e 5.")
        return v

    @field_validator('descricao')
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição da avaliação"
        )(v)

    @field_validator('nome_avaliador')
    @classmethod
    def validar_nome_avaliador(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome do avaliador"
        )(v)
    
    @field_validator('nome_avaliado')
    @classmethod
    def validar_nome_avaliado(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Nome do avaliado"
        )(v)


# Configuração de exemplo para Swagger
CriarAvaliacaoDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarAvaliacaoDTO.criar_exemplo_avaliacao_json()
    }
})
