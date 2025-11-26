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

    @classmethod
    def from_row(cls, row) -> "Produto":
        """
        Cria uma instância de Produto a partir de uma row do banco de dados.
        Suporta tanto acesso por índice quanto por nome de coluna.

        Args:
            row: Row do SQLite (pode ser tuple ou dict-like)

        Returns:
            Instância de Produto
        """
        # Verificar se é acesso por índice (tuple) ou por nome (Row)
        if isinstance(row, (tuple, list)):
            return cls(
                id=row[0],
                nome=row[1],
                descricao=row[2],
                preco=row[3],
                quantidade=row[4],
                em_promocao=bool(row[5]),
                desconto=row[6],
                foto=row[7] if len(row) > 7 else None,
                fornecedor_id=row[8] if len(row) > 8 else None,
            )
        else:
            # Acesso por nome de coluna
            return cls(
                id=row["id"],
                nome=row["nome"],
                descricao=row["descricao"],
                preco=row["preco"],
                quantidade=row["quantidade"],
                em_promocao=bool(row["em_promocao"]),
                desconto=row["desconto"],
                foto=row["foto"] if "foto" in row.keys() else None,
                fornecedor_id=row["fornecedor_id"] if "fornecedor_id" in row.keys() else None,
            )
