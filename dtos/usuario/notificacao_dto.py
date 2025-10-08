from pydantic import Field, field_validator
from typing import Optional, Literal
from datetime import datetime
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_opcional, validar_texto


class CriarNotificacaoDTO(BaseDTO):
    id_usuario: int = Field(..., description="ID do usuário que receberá a notificação")
    mensagem: str = Field(..., min_length=1, max_length=500, description="Conteúdo da mensagem da notificação")
    tipo_notificacao: Literal["alerta", "aviso", "informativo"] = Field(..., description="Tipo da notificação")
    data_hora: Optional[datetime] = Field(default_factory=datetime.utcnow, description="Data e hora da notificação")
    visualizar: Optional[bool] = Field(default=False, description="Status de visualização da notificação")

    # 🔹 Validadores
    @field_validator("id_usuario")
    @classmethod
    def validar_id_usuario(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("O ID do usuário deve ser maior que zero.")
        return v

    @field_validator("mensagem")
    @classmethod
    def validar_mensagem(cls, v: str) -> str:
        return cls.validar_campo_wrapper(validar_texto, "Mensagem", max_chars=500)(v)

    @field_validator("data_hora")
    @classmethod
    def validar_data_hora(cls, v: datetime) -> datetime:
        if v > datetime.utcnow():
            raise ValueError("A data da notificação não pode ser futura.")
        return v
    
    @classmethod
    def criar_exemplo_notificacao_json(cls, **overrides) -> dict:
        exemplo = {
            "id_usuario": 1,
            "mensagem": "Sua solicitação foi aprovada!",
            "tipo_notificacao": "aviso",
            "data_hora": datetime.utcnow().isoformat(),
            "visualizar": False
        }
        exemplo.update(overrides)
        return exemplo

class AtualizarNotificacaoDTO(BaseDTO):
    mensagem: Optional[str] = Field(None, min_length=1, max_length=500, description="Novo conteúdo da mensagem da notificação")
    tipo_notificacao: Optional[Literal["alerta", "aviso", "informativo"]] = Field(None, description="Novo tipo da notificação")
    visualizar: Optional[bool] = Field(None, description="Status de visualização da notificação")
    data_hora: Optional[datetime] = Field(None, description="Nova data e hora da notificação")

    @field_validator("mensagem")
    @classmethod
    def validar_mensagem(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        return cls.validar_campo_wrapper(validar_texto_opcional, "Mensagem", max_chars=500)(v)

    @field_validator("data_hora")
    @classmethod
    def validar_data_hora(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v > datetime.utcnow():
            raise ValueError("A data da notificação não pode ser futura.")
        return v

# Configuração de exemplo para Swagger
CriarNotificacaoDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarNotificacaoDTO.criar_exemplo_notificacao_json()
    }
})