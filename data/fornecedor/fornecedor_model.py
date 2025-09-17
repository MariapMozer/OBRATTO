from dataclasses import dataclass
from typing import Optional
from data.usuario.usuario_model import Usuario


from typing import Optional


@dataclass
class Fornecedor(Usuario):
    razao_social: Optional[str] = None
    selo_confianca: bool = False

