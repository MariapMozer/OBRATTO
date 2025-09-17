from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    senha: str
    cpf_cnpj: str
    telefone: str
    endereco: str
    tipo_usuario: str
    data_cadastro: Optional[str] = None
    foto: str = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None



