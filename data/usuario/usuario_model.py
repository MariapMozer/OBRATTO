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

    @classmethod
    def from_row(cls, row) -> "Usuario":
        """
        Cria uma instância de Usuario a partir de uma row do banco de dados.

        Args:
            row: Row do SQLite (dict-like object)

        Returns:
            Instância de Usuario
        """
        return cls(
            id=row["id"],
            nome=row["nome"],
            email=row["email"],
            senha=row["senha"],
            cpf_cnpj=row["cpf_cnpj"],
            telefone=row["telefone"],
            cep=row["cep"],
            rua=row["rua"],
            numero=row["numero"],
            complemento=row["complemento"],
            bairro=row["bairro"],
            cidade=row["cidade"],
            estado=row["estado"],
            data_cadastro=row["data_cadastro"],
            foto=row["foto"],
            token_redefinicao=row["token_redefinicao"],
            data_token=row["data_token"],
            tipo_usuario=row["tipo_usuario"],
        )



