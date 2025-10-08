from dataclasses import dataclass
from typing import Optional

@dataclass
class Administrador:
    id_usuario: int
    id: Optional[int] = None 