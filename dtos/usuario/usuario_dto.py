from pydantic import EmailStr, Field, field_validator, model_validator
from typing import Optional
from ..base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
import re


class TipoUsuarioEnum(str, Enum):
    ADMINISTRADOR = "administrador"
    PRESTADOR = "prestador"
    CLIENTE = "cliente"
    FORNECEDOR = "fornecedor"

# Conversão
    @classmethod
    def from_string(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise ValueError('Tipo de usuário inválido')
        value_clean = value.strip().lower()
        try:
            return cls(value_clean)
        except ValueError:
            raise ValueError('Tipo de usuário inválido')


class CriarUsuarioDTO(BaseDTO):

    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description ="Nome completo do usuário"
    )
    email: EmailStr = Field(
        ...,
        description ="Email do usuário"
    )
    confirmar_senha: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description ="Confirmação da senha do usuário"
    )
    senha: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description ="Senha do usuário"
    )
    cpf_cnpj: str = Field(
        ...,
        description ="CPF ou CNPJ do usuário"
    )
    telefone: str = Field(
        ...,
        min_length=10,
        description ="Telefone com DDD"
    )
    cep: str = Field(
        ...,
        description ="CEP do usuário"
    )
    rua: str = Field(
        ...,
        description ="Rua do usuário"
    )
    numero: str = Field(
        ...,
        description ="Número da residência do usuário"
    )
    complemento: Optional[str] = Field(
        None,
        description ="Complemento do endereço do usuário"
    )
    bairro: str = Field(
        ...,
        description ="Bairro do usuário"
    )
    cidade: str = Field(
        ...,
        description ="Cidade do usuário"
    )
    estado: str = Field(
        ...,
        description ="Estado do usuário"
    )
    tipo_usuario: TipoUsuarioEnum

    # Funções locais para validar CPF e CNPJ (dígitos verificadores)
    @staticmethod
    def _calcular_digito_cpf(digs: str) -> int:
        soma = sum(int(digs[i]) * (len(digs) + 1 - i) for i in range(len(digs)))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    @staticmethod
    def validar_cpf(num: str) -> str:
        num = re.sub(r'[^0-9]', '', num or '')
        if len(num) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        # impedir CPFs com todos os dígitos iguais
        if num == num[0] * 11:
            raise ValueError('CPF inválido')
        dig1 = CriarUsuarioDTO._calcular_digito_cpf(num[:9])
        dig2 = CriarUsuarioDTO._calcular_digito_cpf(num[:9] + str(dig1))
        if int(num[9]) != dig1 or int(num[10]) != dig2:
            raise ValueError('CPF inválido')
        return num

    @staticmethod
    def validar_cnpj(num: str) -> str:
        num = re.sub(r'[^0-9]', '', num or '')
        if len(num) != 14:
            raise ValueError('CNPJ deve conter 14 dígitos')
        # cálculo dos dígitos verificadores
        def calc(digs, pesos):
            s = sum(int(digs[i]) * pesos[i] for i in range(len(digs)))
            r = s % 11
            return '0' if r < 2 else str(11 - r)

        pesos1 = [5,4,3,2,9,8,7,6,5,4,3,2]
        pesos2 = [6] + pesos1
        d1 = calc(num[:12], pesos1)
        d2 = calc(num[:12] + d1, pesos2)
        if num[12] != d1 or num[13] != d2:
            raise ValueError('CNPJ inválido')
        return num

    @classmethod
    def validar_cpf_cnpj_local(cls, valor: str) -> str:
        if not valor:
            raise ValueError('CPF/CNPJ é obrigatório')
        cleaned = re.sub(r'[^0-9]', '', valor)
        if len(cleaned) == 11:
            return cls.validar_cpf(cleaned)
        if len(cleaned) == 14:
            return cls.validar_cnpj(cleaned)
        raise ValueError('CPF deve ter 11 dígitos ou CNPJ 14 dígitos')

   
    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100),
            "Nome"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(
                valor, min_chars=8, obrigatorio=True),
            "Senha"
        )
        return validador(v)

    @field_validator('confirmar_senha')
    @classmethod
    def validar_confirmar_senha(cls, v, info):
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senhas_coincidem(
                valor, info.data.get('senha'), campo),
            "Confirmar Senha"
        )
        return validador(v)

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_cpf_cnpj_criar(cls, v: str) -> str:
        return cls.validar_cpf_cnpj_local(v)

    @field_validator('telefone') 
    @classmethod
    def validar_telefone_criar(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
           lambda valor, campo: validar_telefone(valor),
              "Telefone"
        )
        return validador(v)

    @field_validator('cep')
    @classmethod
    def validar_cep_criar(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cep(valor),
            "CEP"
        )
        return validador(v)

    @field_validator('estado')
    @classmethod
    def validar_estado_criar(cls, v: str) -> str:
        return validar_estado_brasileiro(v)

    @field_validator('tipo_usuario', mode='before')
    @classmethod
    def validar_tipo_usuario_criar(cls, value):
        
        if value is None:
            raise ValueError('Tipo de usuário é obrigatório')
        try:
            return TipoUsuarioEnum.from_string(value)
        except ValueError:
            raise


    @classmethod
    def criar_exemplo_usuario_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva",
            "email": "joao.silva@email.com",
            "senha": "senhaSegura123",
            "confirmar_senha": "senhaSegura123",
            "cpf_cnpj": "111.444.777-35",
            "telefone": "(11) 99999-9999",
            "cep": "12345-678",
            "rua": "Rua Exemplo",
            "numero": "123",    
            "complemento": "Apto 45",
            "bairro": "Bairro Exemplo",
            "cidade": "Cidade Exemplo",
            "estado": "SP",
            "tipo_usuario": "cliente",
        }

        exemplo.update(overrides)
        return exemplo



class AtualizarUsuarioDTO(BaseDTO):

    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome completo")
    email: Optional[EmailStr] = Field(None, description="E-mail do usuário")
    senha: Optional[str] = Field(None, min_length=8, description="Senha do usuário")
    confirmar_senha: Optional[str] = Field(None, description="Confirmação da nova senha")
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
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError('Senha deve ter no mínimo 8 caracteres')
        if not any(c.isdigit() for c in v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v, info):
        # Se nenhuma senha foi informada, aceitar None
        if v is None:
            return v
        if 'senha' in info.data and info.data.get('senha') is not None and v != info.data['senha']:
            raise ValueError('As senhas não coincidem')
        return v

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_documento(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        # Usar a validação local completa (CPF/CNPJ) implementada em CriarUsuarioDTO
        try:
            return CriarUsuarioDTO.validar_cpf_cnpj_local(v)
        except ValueError as e:
            raise ValueError(str(e))

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