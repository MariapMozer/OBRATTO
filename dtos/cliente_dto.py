from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
from .base_dto import BaseDTO
from .usuario_dto import AtualizarUsuarioDTO, CriarUsuarioDTO

class CriarCliente(CriarUsuarioDTO):
    genero: Optional[str] = Field(None, description="Gênero do cliente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")

    @field_validator('genero')
    @classmethod
    def validar_genero(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Gênero", max_chars=20)(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        return cls.validar_campo_wrapper(validar_data_nascimento, "Data de nascimento")(v)

    @classmethod
    def criar_exemplo_cliente_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "genero": "Feminino",
            "data_nascimento": "1990-01-01"
        }
        exemplo.update(overrides)
        return exemplo
    
class AtualizarClienteDTO(AtualizarUsuarioDTO):

    genero: Optional[str] = Field(None, description="Gênero do cliente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")

    @field_validator('genero')
    @classmethod
    def validar_genero(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Gênero", max_chars=20)(v)

    @field_validator('data_nascimento')
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        return cls.validar_campo_wrapper(validar_data_nascimento, "Data de nascimento")(v)
    
CriarCliente.model_config.update({
    "json_schema_extra": {
        "example": CriarCliente.criar_exemplo_cliente_json()
    }
})
