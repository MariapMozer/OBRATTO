from typing import Optional
from datetime import datetime
from pydantic import Field, field_validator
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto, validar_texto_opcional


class CriarMensagemDTO(BaseDTO):
    id_remetente: int = Field(..., description="ID do usuário que envia a mensagem")
    id_destinatario: int = Field(..., description="ID do usuário que recebe a mensagem")
    conteudo: str = Field(..., description="Conteúdo da mensagem")
    data_hora: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Data e hora do envio")
    nome_remetente: Optional[str] = Field(None, description="Nome do remetente")
    nome_destinatario: Optional[str] = Field(None, description="Nome do destinatário")

    # 🔹 Validações
    @field_validator("conteudo")
    @classmethod
    def validar_conteudo(cls, v: str) -> str:
        return cls.validar_campo_wrapper(validar_texto, "Conteúdo", max_chars=1000)(v)

    @field_validator("nome_remetente")
    @classmethod
    def validar_nome_remetente(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Nome do remetente", max_chars=150)(v)

    @field_validator("nome_destinatario")
    @classmethod
    def validar_nome_destinatario(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Nome do destinatário", max_chars=150)(v)

    # 🔹 Exemplo para documentação
    @classmethod
    def criar_exemplo_mensagem_json(cls, **overrides) -> dict:
        exemplo = {
            "id_remetente": 1,
            "id_destinatario": 2,
            "conteudo": "Olá, tudo bem?",
            "data_hora": datetime.utcnow().isoformat(),
            "nome_remetente": "João Silva",
            "nome_destinatario": "Maria Souza"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarMensagemDTO(BaseDTO):
    id_remetente: Optional[int] = Field(None, description="ID do usuário que envia a mensagem")
    id_destinatario: Optional[int] = Field(None, description="ID do usuário que recebe a mensagem")
    conteudo: Optional[str] = Field(None, description="Conteúdo da mensagem")
    nome_remetente: Optional[str] = Field(None, description="Nome do remetente")
    nome_destinatario: Optional[str] = Field(None, description="Nome do destinatário")

    @field_validator("conteudo")
    @classmethod
    def validar_conteudo(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Conteúdo", max_chars=1000)(v)

    @field_validator("nome_remetente")
    @classmethod
    def validar_nome_remetente(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Nome do remetente", max_chars=150)(v)

    @field_validator("nome_destinatario")
    @classmethod
    def validar_nome_destinatario(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(validar_texto_opcional, "Nome do destinatário", max_chars=150)(v)


# 🔹 Configura JSON Schema extra
CriarMensagemDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarMensagemDTO.criar_exemplo_mensagem_json()
    }
})
