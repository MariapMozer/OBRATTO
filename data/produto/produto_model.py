from dataclasses import dataclass
from typing import Optional
import datetime


@dataclass
class Produto:
    id: Optional[int]
    nome: str
    descricao: str
    preco: float
    quantidade: int
    foto: Optional[str] = None
    em_promocao: bool = False
    desconto: float = 0.0
    fornecedor_id: Optional[int] = None
