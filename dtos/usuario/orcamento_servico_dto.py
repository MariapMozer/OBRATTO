from pydantic import Field, field_validator
from typing import Optional
from datetime import date
from ..base_dto import BaseDTO
from utils.validacoes_dto import validar_texto_opcional


class CriarOrcamentoServicoDTO(BaseDTO):
    id_orcamento: int = Field(..., description="ID do orçamento principal ao qual este serviço pertence")
    id_servico: int = Field(..., description="ID do serviço que está sendo orçado")
    id_prestador: int = Field(..., description="ID do prestador que oferece o serviço")
    id_cliente: int = Field(..., description="ID do cliente que solicitou o orçamento do serviço")
    valor_estimado: float = Field(..., gt=0, description="Valor estimado para o serviço")
    prazo_entrega: date = Field(..., description="Prazo de entrega para o serviço")
    status: str = Field("pendente", description="Status inicial do orçamento do serviço (ex: pendente, aprovado, rejeitado)")
    descricao: str = Field(..., min_length=10, max_length=500, description="Descrição detalhada do serviço orçado")
    titulo_servico: str = Field(..., min_length=3, max_length=100, description="Título do serviço orçado")

    # 🔹 Validadores

    @field_validator("valor_estimado")
    @classmethod
    def validar_valor_estimado(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("O valor estimado deve ser maior que zero.")
        return v

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, v: str) -> str:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição do serviço"
        )(v)

    @field_validator("titulo_servico")
    @classmethod
    def validar_titulo_servico(cls, v: str) -> str:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Título do serviço"
        )(v)

    @field_validator("prazo_entrega")
    @classmethod
    def validar_prazo_entrega(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("O prazo de entrega não pode ser anterior à data de hoje.")
        return v
    
    @field_validator("status")
    @classmethod
    def validar_status(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Status do orçamento"
        )(v)

    # 🔹 Exemplo para documentação
    @classmethod
    def criar_exemplo_orcamento_json(cls, **overrides) -> dict:
        exemplo = {
            "id_orcamento": 1,
            "id_servico": 10,
            "id_prestador": 5,
            "id_cliente": 3,
            "valor_estimado": 350.0,
            "prazo_entrega": str(date.today()),
            "status": "pendente",
            "descricao": "Serviço detalhado de manutenção residencial.",
            "titulo_servico": "Manutenção residencial",
            "nome_prestador": "Carlos Pereira",
            "nome_cliente": "Ana Souza"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarOrcamentoServicoDTO(BaseDTO):
    valor_estimado: Optional[float] = Field(None, gt=0, description="Novo valor estimado para o serviço")
    prazo_entrega: Optional[date] = Field(None, description="Novo prazo de entrega para o serviço")
    status: Optional[str] = Field(None, description="Novo status do orçamento do serviço")
    descricao: Optional[str] = Field(None, min_length=10, max_length=500, description="Nova descrição detalhada do serviço orçado")
    titulo_servico: Optional[str] = Field(None, min_length=3, max_length=100, description="Novo título do serviço")
    nome_prestador: Optional[str] = Field(None, description="Novo nome do prestador")
    nome_cliente: Optional[str] = Field(None, description="Novo nome do cliente")

    @field_validator("valor_estimado")
    @classmethod
    def validar_valor_estimado(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("O valor estimado deve ser maior que zero.")
        return v

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Descrição do serviço"
        )(v)

    @field_validator("titulo_servico")
    @classmethod
    def validar_titulo_servico(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=100),
            "Título do serviço"
        )(v)

    @field_validator("status")
    @classmethod
    def validar_status(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=50),
            "Status do orçamento"
        )(v)

    @field_validator("nome_prestador")
    @classmethod
    def validar_nome_prestador(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=150),
            "Nome do prestador"
        )(v)

    @field_validator("nome_cliente")
    @classmethod
    def validar_nome_cliente(cls, v: Optional[str]) -> Optional[str]:
        return cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=150),
            "Nome do cliente"
        )(v)

    @field_validator("prazo_entrega")
    @classmethod
    def validar_prazo_entrega(cls, v: Optional[date]) -> Optional[date]:
        if v is not None and v < date.today():
            raise ValueError("O prazo de entrega não pode ser anterior à data de hoje.")
        return v


# 🔹 Configuração de exemplo para Swagger
CriarOrcamentoServicoDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarOrcamentoServicoDTO.criar_exemplo_orcamento_json()
    }
})
