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
# Endereço detalhado
    cep: str
    rua: str
    numero: str
    complemento: str
    bairro: str
    cidade: str
    estado: str
    tipo_usuario: str
    data_cadastro: Optional[str] = None
    foto: Optional[str] = None
    token_redefinicao: Optional[str] = None
    data_token: Optional[str] = None



