from pydantic import EmailStr, Field, field_validator
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_obrigatorio


class LoginDTO(BaseDTO):
    
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(...,description="Senha do usuário")


    @field_validator("email")
    @classmethod
    def validar_email(cls, email):
        if not email:
           raise ValueError("O campo email é obrigatório.")
        if '@' not in email or '.' not in email:
           raise ValueError("O campo email deve ser um email válido.")
        return email
   
# Mudança no código de senha para torná-lo mais específico e direto, sem depender de funções externas. 

    # @field_validator("senha")
    # @classmethod
    # def validar_senha(cls, senha):
    #    if not senha:
    #        raise ValueError("O campo senha é obrigatório.")
    #    if len(senha) < 8:
    #        raise ValueError("O campo senha deve ter pelo menos 8 caracteres.")
    #    return senha


    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha):
        if not senha or not senha.strip():
            raise ValueError("O campo senha é obrigatório.")
        return senha

# MUdança de classmethod para staticmethod, pois não utiliza a classe diretamente e nem precisa acessar atributos da classe.
    @staticmethod
    def criar_exemplo_login_json(**overrides) -> dict:
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
