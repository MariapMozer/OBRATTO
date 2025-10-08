from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date


class TipoUsuarioEnum(str, Enum):
    #ADM = "adm"
    PRESTADOR = "prestador"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"


class CriarUsuarioDTO(BaseDTO):
    """
    DTO para criação de novo usuário.
    Usado em formulários de registro.
    
    NOTA: Validadores customizados temporariamente desabilitados para evitar recursão.
    A validação básica do Pydantic ainda funciona através dos Field constraints.
    """

    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    senha: str = Field(..., min_length=8, description="Senha do usuário")
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do usuário")
    telefone: str = Field(..., min_length=10)
    cep: str = Field(..., description="CEP")
    rua: str = Field(..., description="Rua/Logradouro", min_length=2)
    numero: str = Field(..., description="Número", min_length=1)
    complemento: Optional[str] = Field(None, description="Complemento", max_length=100)
    bairro: str = Field(..., description="Bairro", min_length=2)
    cidade: str = Field(..., description="Cidade", min_length=2)
    estado: str = Field(..., description="Estado", min_length=2, max_length=2)
    tipo_usuario: TipoUsuarioEnum = Field(...)
    foto: Optional[str] = Field(None)


    # VALIDADORES DESABILITADOS TEMPORARIAMENTE - CAUSANDO RECURSÃO
    # Pydantic faz validação básica através dos Field constraints

    @classmethod
    def criar_exemplo_usuario_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao.silva@email.com",
            "senha": "senhaSegura123",
            "cpf_cnpj": "123.456.789-01",
            "telefone": "(11) 99999-9999",
            "cep": "12345-678",
            "rua": "Rua Exemplo",
            "numero": "123",    
            "complemento": "Apto 45",
            "bairro": "Bairro Exemplo",
            "cidade": "Cidade Exemplo",
            "estado": "EX",
        }

        exemplo.update(overrides)
        return exemplo



class AtualizarUsuarioDTO(BaseDTO):

    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo")
    email: Optional[EmailStr] = Field(None, description="E-mail do usuário")
    senha: Optional[str] = Field(None, min_length=8, description="Senha do usuário")
    cpf_cnpj: Optional[str] = Field(None, description="CPF ou CNPJ do usuário")
    telefone: Optional[str] = Field(None, min_length=10, description="Telefone")
    cep: Optional[str] = Field(None, description="CEP")
    rua: Optional[str] = Field(None, description="Rua/Logradouro")
    numero: Optional[str] = Field(None, description="Número")
    complemento: Optional[str] = Field(None, description="Complemento")
    bairro: Optional[str] = Field(None, description="Bairro")
    cidade: Optional[str] = Field(None, description="Cidade")
    estado: Optional[str] = Field(None, description="Estado")
    tipo_usuario: Optional[TipoUsuarioEnum] = Field(None, description="Tipo de usuário")
    foto: Optional[str] = Field(None, description="Foto do usuário")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=100),
            "Nome"
        )(v)

    @field_validator('email')
    @classmethod
    def validar_email(cls, v: Optional[EmailStr]) -> Optional[EmailStr]:
        if not v:
            return v
        cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(str(valor), campo, min_chars=5, max_chars=100),
            "E-mail"
        )(str(v))
        return v  # Retorna o EmailStr original

    @field_validator('senha')
    @classmethod
    def validar_senha_forte(cls, v):
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v, info):
        if 'senha' in info.data and v != info.data['senha']:
            raise ValueError('As senhas não coincidem')
        return v

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_documento(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        tipo = "CPF" if len(v) <= 14 else "CNPJ"
        return cls.validar_campo_wrapper(validar_cpf_cnpj, tipo)(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_telefone, "Telefone")(v)

    @field_validator('cep')
    @classmethod
    def validar_cep(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_cep, "CEP")(v)

    @field_validator('rua')
    @classmethod
    def validar_rua_atualizar(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_obrigatorio, "Rua", min_chars=2)(v)

    @field_validator('numero')
    @classmethod
    def validar_numero(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_obrigatorio, "Número", min_chars=1)(v)

    @field_validator('complemento')
    @classmethod
    def validar_complemento(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_opcional, "Complemento", max_chars=100)(v)

    @field_validator('bairro')
    @classmethod
    def validar_bairro(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_obrigatorio, "Bairro", min_chars=2)(v)

    @field_validator('cidade')
    @classmethod
    def validar_cidade(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_obrigatorio, "Cidade", min_chars=2)(v)

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_texto_obrigatorio, "Estado", min_chars=2, max_chars=2)(v)
    


# Configurar exemplos JSON nos model_config
CriarUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarUsuarioDTO.criar_exemplo_usuario_json()
    }
})