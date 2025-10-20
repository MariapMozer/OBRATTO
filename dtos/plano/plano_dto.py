from pydantic import Field, field_validator
from typing import Optional
from enum import Enum
from ..base_dto import BaseDTO
from util.validacoes_dto import validar_texto_obrigatorio


class TipoPlanoEnum(str, Enum):
    """Tipos de plano disponíveis"""

    BASICO = "basico"
    INTERMEDIARIO = "intermediario"
    PREMIUM = "premium"
    EMPRESARIAL = "empresarial"


class CriarPlanoDTO(BaseDTO):
    """
    DTO para criação de novo plano.
    Usado em formulários de cadastro de planos.
    """

    nome_plano: str = Field(..., description="Nome do plano")
    valor_mensal: float = Field(..., gt=0, description="Valor mensal do plano")
    limite_servico: int = Field(..., ge=0, description="Limite de serviços permitidos")
    tipo_plano: str = Field(..., description="Tipo do plano")
    descricao: str = Field(..., description="Descrição do plano")

    @field_validator("nome_plano")
    @classmethod
    def validar_nome_plano(cls, v: str) -> str:
        return validar_texto_obrigatorio(v, "Nome do plano", min_chars=3, max_chars=100)

    @field_validator("descricao")
    @classmethod
    def validar_descricao_plano(cls, v: str) -> str:
        return validar_texto_obrigatorio(v, "Descrição", min_chars=10, max_chars=500)

    @field_validator("valor_mensal")
    @classmethod
    def validar_valor_plano(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Valor mensal deve ser maior que zero")
        if v > 10000:
            raise ValueError("Valor mensal não pode exceder R$ 10.000,00")
        return v

    @field_validator("limite_servico")
    @classmethod
    def validar_limite_servico(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Limite de serviços não pode ser negativo")
        if v > 10000:
            raise ValueError("Limite de serviços não pode exceder 10.000")
        return v

    @field_validator("tipo_plano")
    @classmethod
    def validar_tipo_plano(cls, v: str) -> str:
        tipos_validos = ["basico", "intermediario", "premium", "empresarial"]
        if v.lower() not in tipos_validos:
            raise ValueError(
                f'Tipo de plano deve ser um dos seguintes: {", ".join(tipos_validos)}'
            )
        return v.lower()


class AlterarPlanoDTO(BaseDTO):
    """
    DTO para alteração de plano existente.
    Todos os campos são opcionais.
    """

    nome_plano: Optional[str] = Field(
        None, min_length=3, max_length=100, description="Nome do plano"
    )
    valor_mensal: Optional[float] = Field(
        None, gt=0, description="Valor mensal do plano"
    )
    limite_servico: Optional[int] = Field(
        None, ge=0, description="Limite de serviços permitidos"
    )
    tipo_plano: Optional[str] = Field(None, description="Tipo do plano")
    descricao: Optional[str] = Field(
        None, min_length=10, max_length=500, description="Descrição do plano"
    )

    @field_validator("nome_plano")
    @classmethod
    def validar_nome_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_texto_obrigatorio(
                v, "Nome do plano", min_chars=3, max_chars=100
            )
        return v

    @field_validator("descricao")
    @classmethod
    def validar_descricao_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            return validar_texto_obrigatorio(
                v, "Descrição", min_chars=10, max_chars=500
            )
        return v

    @field_validator("valor_mensal")
    @classmethod
    def validar_valor_alterar(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            if v <= 0:
                raise ValueError("Valor mensal deve ser maior que zero")
            if v > 10000:
                raise ValueError("Valor mensal não pode exceder R$ 10.000,00")
        return v

    @field_validator("tipo_plano")
    @classmethod
    def validar_tipo_alterar(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            tipos_validos = ["basico", "intermediario", "premium", "empresarial"]
            if v.lower() not in tipos_validos:
                raise ValueError(
                    f'Tipo de plano deve ser um dos seguintes: {", ".join(tipos_validos)}'
                )
            return v.lower()
        return v


class ExcluirPlanoDTO(BaseDTO):
    """
    DTO para exclusão de plano.
    """

    id_plano: int = Field(..., gt=0, description="ID do plano a ser excluído")

    @field_validator("id_plano")
    @classmethod
    def validar_id_plano(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("ID do plano deve ser maior que zero")
        return v
