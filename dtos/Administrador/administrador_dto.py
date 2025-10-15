from pydantic import EmailStr, Field, field_validator, model_validator
from typing import Optional
from ..base_dto import BaseDTO
from ..usuario.usuario_dto import CriarUsuarioDTO, AtualizarUsuarioDTO
from utils.validacoes_dto import *


class CriarAdministradorDTO(CriarUsuarioDTO):
    pass


class AtualizarAdministradorDTO(AtualizarUsuarioDTO):
    pass


class EditarPerfilAdministradorDTO(BaseDTO):
   
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo")
    email: EmailStr = Field(..., description="E-mail")
    senha_atual: str = Field(..., description="Senha atual para confirmar alteração")
    senha_nova: Optional[str] = Field(None, min_length=8, description="Nova senha (opcional)")
    confirmar_senha_nova: Optional[str] = Field(None, description="Confirmação da nova senha")
    telefone: Optional[str] = Field(None, description="Telefone de contato")
    foto: Optional[str] = Field(None, description="URL da foto de perfil")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        return validar_texto_obrigatorio(v, "Nome", min_chars=2, max_chars=100)

    @field_validator('senha_nova')
    @classmethod
    def validar_senha_nova(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return validar_senha(v, min_chars=8, obrigatorio=False)

    @model_validator(mode='after')
    def verificar_senha_nova(cls, model):
        senha_nova = getattr(model, 'senha_nova', None)
        confirmar = getattr(model, 'confirmar_senha_nova', None)
        
        if senha_nova and not confirmar:
            raise ValueError('Confirmação da nova senha é obrigatória')
        
        if senha_nova and confirmar:
            validar_senhas_coincidem(senha_nova, confirmar)
        
        return model

    @field_validator('telefone')
    @classmethod
    def validar_telefone(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(validar_telefone, "Telefone")(v)


class ModerarUsuarioDTO(BaseDTO):

    nome: Optional[str] = Field(None, min_length=2, max_length=100, description="Nome do usuário")
    email: Optional[EmailStr] = Field(None, description="E-mail do usuário")
    ativo: Optional[bool] = Field(None, description="Status ativo/inativo do usuário")
    bloqueado: Optional[bool] = Field(None, description="Usuário bloqueado")
    motivo_bloqueio: Optional[str] = Field(None, max_length=500, description="Motivo do bloqueio")

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=2, max_chars=100),
            "Nome"
        )(v)

    @field_validator('motivo_bloqueio')
    @classmethod
    def validar_motivo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Motivo do bloqueio"
        )(v)


class AprovarSeloDTO(BaseDTO):

    id_usuario: int = Field(..., gt=0, description="ID do usuário (prestador ou fornecedor)")
    tipo_usuario: str = Field(..., description="Tipo: 'prestador' ou 'fornecedor'")
    aprovar: bool = Field(default=True, description="True para aprovar, False para rejeitar")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações sobre a aprovação/rejeição")

    @field_validator('tipo_usuario')
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        tipos_validos = ['prestador', 'fornecedor']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo de usuário deve ser: {", ".join(tipos_validos)}')
        return v.lower()

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Observações"
        )(v)


class ExcluirUsuarioDTO(BaseDTO):

    id_usuario: int = Field(..., gt=0, description="ID do usuário a ser excluído")
    tipo_usuario: str = Field(..., description="Tipo: 'prestador', 'fornecedor', 'cliente' ou 'administrador'")
    confirmar_exclusao: bool = Field(..., description="Confirmação obrigatória de exclusão")
    motivo: Optional[str] = Field(None, max_length=500, description="Motivo da exclusão")

    @field_validator('tipo_usuario')
    @classmethod
    def validar_tipo(cls, v: str) -> str:
        tipos_validos = ['prestador', 'fornecedor', 'cliente', 'administrador']
        if v.lower() not in tipos_validos:
            raise ValueError(f'Tipo de usuário deve ser: {", ".join(tipos_validos)}')
        return v.lower()

    @model_validator(mode='after')
    def verificar_confirmacao(cls, model):
        if not getattr(model, 'confirmar_exclusao', False):
            raise ValueError('A exclusão deve ser confirmada explicitamente')
        return model

    @field_validator('motivo')
    @classmethod
    def validar_motivo(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Motivo da exclusão"
        )(v)


# Configurar exemplos JSON nos model_config
CriarAdministradorDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarAdministradorDTO.criar_exemplo_json()
    }
})