from pydantic import EmailStr, Field, field_validator
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_obrigatorio


class LoginDTO(BaseDTO):
    email: str
    senha: str

    @field_validator('email')
    def validar_email(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo E-mail é obrigatório.")
        try:
            EmailStr.validate(v)
        except ValueError:
            raise ValueError("Endereço de e-mail em formato inválido.")

    @field_validator('senha')
    def validar_senha(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("O campo Senha é obrigatório.")
        if len(v.strip()) < 6:
            raise ValueError("A senha deve ter pelo menos 6 caracteres.")
        return v.strip()

# DTO para login de Cliente
class LoginClienteDTO(LoginDTO):
    """DTO para login de Cliente"""
    pass


# DTO para login de Prestador
class LoginPrestadorDTO(LoginDTO):
    """DTO para login de Prestador"""
    pass


# DTO para login de Fornecedor
class LoginFornecedorDTO(LoginDTO):
    """DTO para login de Fornecedor"""
    pass


