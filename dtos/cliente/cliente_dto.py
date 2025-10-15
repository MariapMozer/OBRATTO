from pydantic import Field, field_validator
from typing import Optional
from datetime import date
from ..base_dto import BaseDTO


class CriarClienteDTO(BaseDTO):
    genero: Optional[str] = Field(None, description="Gênero do cliente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")

    # Validadores explícitos
    @field_validator("genero")
    @classmethod
    def validar_genero(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 20:
            raise ValueError("Gênero deve ter no máximo 20 caracteres.")
        return v

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        # Aqui você pode adicionar validações extras, ex: não aceitar datas futuras
        if v is not None and v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro.")
        return v

    @staticmethod
    def criar_exemplo_json(**overrides) -> dict:
        exemplo = {
            "genero": "Feminino",
            "data_nascimento": "1990-01-01"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarClienteDTO(BaseDTO):
    genero: Optional[str] = Field(None, description="Gênero do cliente")
    data_nascimento: Optional[date] = Field(None, description="Data de nascimento")

    @field_validator("genero")
    @classmethod
    def validar_genero(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) > 20:
            raise ValueError("Gênero deve ter no máximo 20 caracteres.")
        return v

    @field_validator("data_nascimento")
    @classmethod
    def validar_data_nascimento(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v > date.today():
            raise ValueError("Data de nascimento não pode ser no futuro.")
        return v

    @staticmethod
    def criar_exemplo_json(**overrides) -> dict:
        exemplo = {
            "genero": "Masculino",
            "data_nascimento": "1985-05-20"
        }

# Configurar exemplos JSON para documentação
CriarClienteDTO.model_config.update({
    "json_schema_extra": {"example": CriarClienteDTO.criar_exemplo_json()}
})
