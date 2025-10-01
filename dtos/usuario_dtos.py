from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum

class TipoUsuarioEnum(str, Enum):
    ADM = "adm"
    PRESTADOR = "prestador"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"


class CriarUsuarioDTO(BaseDTO):
    """
    DTO para criação de novo usuário.
    Usado em formulários de registro.
    """

    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr = Field(...)
    senha: str = Field(..., min_length=6, description="Senha do usuário")
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do usuário")
    telefone: str = Field(..., min_length=10)
    cep: str = Field(..., description="CEP")
    logradouro: str = Field(..., description="Logradouro")
    numero: str = Field(..., description="Número")
    complemento: Optional[str] = Field(None, description="Complemento")
    bairro: str = Field(..., description="Bairro")
    cidade: str = Field(..., description="Cidade")
    estado: str = Field(..., description="Estado")

    tipo_usuario: TipoUsuarioEnum = Field(...)
    foto: Optional[str] = Field(None)


    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=100),
        "Nome"
    )
        return validador(v)
    
    @field_validator('email')
    @classmethod
    def validar_email(cls, v: EmailStr) -> EmailStr:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(str(valor), campo, min_chars=5, max_chars=100),
        "E-mail"
    )
        return EmailStr(validador(str(v)))

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=6),
        "Senha"
    )
        return validador(v)

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_documento(cls, v: str) -> str:
        if len(v) <= 14:
            validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf_cnpj(valor),
            "CPF"
        )
        else:
            validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf_cnpj(valor),
            "CNPJ"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_telefone(valor),
        "Telefone"
    )
        return validador(v)


    @field_validator('cep')
    @classmethod
    def validar_cep_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_cep(valor),
        "CEP"
    )
        return validador(v)

    @field_validator('logradouro')
    @classmethod
    def validar_logradouro(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2),
        "Logradouro"
    )
        return validador(v)

    @field_validator('numero')
    @classmethod
    def validar_numero(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=1),
        "Número"
    )
        return validador(v)
    
    @field_validator('complemento')
    @classmethod
    def validar_complemento(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=1, max_chars=100),
        "Complemento"
    )
        return validador(v)

    @field_validator('bairro')
    @classmethod
    def validar_bairro(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2),
        "Bairro"
    )
        return validador(v)

    @field_validator('cidade')
    @classmethod
    def validar_cidade(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2),
        "Cidade"
    )
        return validador(v)

    @field_validator('estado')
    @classmethod
    def validar_estado(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
        lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=2),
        "Estado"
    )
        return validador(v)


class CriarPrestador(CriarUsuarioDTO):
    area_atuacao: Optional[str] = Field(None)
    razao_social: Optional[str] = Field(None)
    descricao_servicos: Optional[str] = Field(None)
    selo_confianca: bool = Field(default=False)

    @field_validator('area_atuacao')
    @classmethod
    def validar_area_atuacao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Área de atuação", max_chars=100)(v)

    @field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)

    @field_validator('descricao_servicos')
    @classmethod
    def validar_descricao_servicos(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Descrição dos serviços", max_chars=500)(v)


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


class CriarFornecedor(CriarUsuarioDTO):
    razao_social: Optional[str] = Field(None, description="Razão Social da empresa")
    selo_confianca: bool = Field(default=False)

    field_validator('razao_social')
    @classmethod
    def validar_razao_social(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Razão Social", max_chars=100)(v)



    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao.silva@email.com",
            "telefone": "(11) 99999-9999",
            "cpf": "123.456.789-01"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarUsuarioDTO(BaseDTO):
    """
    DTO para atualização de dados do usuário.
    Campos opcionais para atualização parcial.
    """

    nome: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nome completo"
    )
    telefone: Optional[str] = Field(
        None,
        description="Telefone"
    )

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Nome"
        )
        return validador(v)

    @field_validator('telefone')
    @classmethod
    def validar_telefone_campo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_telefone(valor),
            "Telefone"
        )
        return validador(v)


# Configurar exemplos JSON nos model_config
CriarUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarUsuarioDTO.criar_exemplo_json()
    }
})
