from dataclasses import dataclass
from datetime import datetime

@dataclass
class Notificacao:
    id_notificacao: int
    id_usuario: int
    mensagem: str
    data_hora: datetime
    tipo_notificacao: str
    visualizar: bool


