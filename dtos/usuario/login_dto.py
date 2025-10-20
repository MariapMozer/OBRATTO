from pydantic import EmailStr, Field, field_validator
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_obrigatorio
from utils.security import validar_forca_senha


class LoginDTO(BaseDTO):
    """
    DTO para validação de dados de login

    IMPORTANTE: Para login, validamos apenas campos obrigatórios,
    NÃO aplicamos validação de força de senha (isso é só no cadastro).
    """

    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")

    @field_validator('senha')
    @classmethod
    def validar_senha_existe(cls, v: str) -> str:
        """Valida apenas se senha foi fornecida (não valida força)"""
        if not v or not v.strip():
            raise ValueError("Senha é obrigatória")
        return v.strip()

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
