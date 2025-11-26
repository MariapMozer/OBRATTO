from pydantic import EmailStr, Field, field_validator, model_validator
from typing import Optional
from .base_dto import BaseDTO
from util.validacoes_dto import (
    VALIDADOR_NOME,
    VALIDADOR_TELEFONE,
    VALIDADOR_CEP,
    VALIDADOR_ESTADO,
    VALIDADOR_CIDADE,
    VALIDADOR_BAIRRO,
    VALIDADOR_COMPLEMENTO,
    VALIDADOR_NUMERO,
    VALIDADOR_SENHA_FORTE,
    validar_senhas_coincidem,
    validar_cpf_cnpj, # Importamos a função de validação de CPF/CNPJ
)


# class TipoUsuarioEnum(str, Enum):
#     # ADM = "adm"
#     PRESTADOR = "prestador"
#     CLIENTE = "cliente"
#     FORNECEDOR = "fornecedor"
 
class CriarUsuarioDTO(BaseDTO):
    nome: str = Field(..., description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email do usuário")
    senha: str = Field(..., description="Senha do usuário")
    confirmar_senha: str = Field(..., description="Confirmação da senha")
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do usuário")
    telefone: str = Field(..., description="Telefone de contato")
    cep: Optional[str] = Field(None, description="CEP do endereço")
    estado: str = Field(..., description="Estado (UF)")
    cidade: str = Field(..., description="Cidade")
    rua: str = Field(..., description="Rua")
    numero: str = Field(..., description="Número do endereço")
    complemento: Optional[str] = Field(None, description="Complemento do endereço")
    bairro: str = Field(..., description="Bairro")
    tipo_usuario: str = Field(..., description="Tipo de usuário (cliente, prestador, fornecedor)")

    # =================================================================
    # VALIDAÇÕES DE CAMPO (FIELD_VALIDATORS)
    # =================================================================

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, v: str) -> str:
        return VALIDADOR_NOME(v)

    @field_validator("senha")
    @classmethod
    def validar_senha_field(cls, v: str) -> str:
        # Usamos o validador de senha forte
        return VALIDADOR_SENHA_FORTE(v)

    @field_validator("cpf_cnpj")
    @classmethod
    def validar_cpf_cnpj_field(cls, v: str) -> str:
        # **CORREÇÃO CRÍTICA**: Chamamos a função de validação de CPF/CNPJ
        # que deve ser corrigida para incluir o cálculo do dígito verificador.
        # Assumindo que a função 'validar_cpf_cnpj' será corrigida no arquivo 'validacoes_dto.py'
        return validar_cpf_cnpj(v, campo="CPF/CNPJ")

    @field_validator("telefone")
    @classmethod
    def validar_telefone_field(cls, v: str) -> str:
        return VALIDADOR_TELEFONE(v)

    @field_validator("cep")
    @classmethod
    def validar_cep_field(cls, v: Optional[str]) -> Optional[str]:
        return VALIDADOR_CEP(v)

    @field_validator("estado")
    @classmethod
    def validar_estado_field(cls, v: str) -> str:
        return VALIDADOR_ESTADO(v)

    @field_validator("cidade")
    @classmethod
    def validar_cidade_field(cls, v: str) -> str:
        return VALIDADOR_CIDADE(v)

    @field_validator("bairro")
    @classmethod
    def validar_bairro_field(cls, v: str) -> str:
        return VALIDADOR_BAIRRO(v)

    @field_validator("complemento")
    @classmethod
    def validar_complemento_field(cls, v: Optional[str]) -> Optional[str]:
        return VALIDADOR_COMPLEMENTO(v)

    @field_validator("numero")
    @classmethod
    def validar_numero_field(cls, v: str) -> str:
        return VALIDADOR_NUMERO(v)

    # =================================================================
    # VALIDAÇÕES DE MODELO (MODEL_VALIDATORS)
    # =================================================================

    @model_validator(mode="after")
    def validar_senhas(self) -> "CriarUsuarioDTO":
        # **CORREÇÃO CRÍTICA**: Validação para garantir que as senhas coincidam
        validar_senhas_coincidem(self.senha, self.confirmar_senha)
        return self

    # Exemplo de dados para documentação da API (mantido por completude)
    @classmethod
    def criar_exemplo_usuario_json(cls, **overrides) -> dict:
        exemplo = {
            "nome": "João da Silva",
            "email": "joao.silva@exemplo.com",
            "senha": "SenhaForte123!",
            "confirmar_senha": "SenhaForte123!",
            "cpf_cnpj": "12345678901",
            "telefone": "11987654321",
            "cep": "01001000",
            "estado": "SP",
            "cidade": "São Paulo",
            "rua": "Rua Exemplo",
            "numero": "100",
            "complemento": "Apto 1",
            "bairro": "Centro",
            "tipo_usuario": "cliente",
        }
        exemplo.update(overrides)
        return exemplo


CriarUsuarioDTO.model_config.update(
    {"json_schema_extra": {"example": CriarUsuarioDTO.criar_exemplo_usuario_json()}}
)
