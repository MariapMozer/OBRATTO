from pydantic import EmailStr, Field, field_validator
from .base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_obrigatorio


class LoginDTO(BaseDTO):
    
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=8, description="Senha do usuário")

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=8),
            "Senha"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_login_json(cls, **overrides) -> dict:
        exemplo = {
            "email": "joao.silva@email.com",
            "senha": "senhaSegura123"
        }
        exemplo.update(overrides)
        return exemplo


# Configurar exemplos JSON nos model_config
LoginDTO.model_config.update({
    "json_schema_extra": {
        "example": LoginDTO.criar_exemplo_login_json()
    }
})
