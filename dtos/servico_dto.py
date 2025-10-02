from pydantic import EmailStr, Field, field_validator
from typing import Optional
from .base_dto import BaseDTO
from utils.validacoes_dto import *
from enum import Enum
from datetime import date
from .base_dto import BaseDTO
from dataclasses import dataclass
from typing import Optional


class CriarServico(BaseDTO):
    titulo: Optional[str] = Field(None)
    descricao: Optional[str] = Field(None)
    categoria: Optional[str] = Field(None)
    valor_base: Optional[float] = Field(None)
    nome_prestador: Optional[str] = Field(None)

