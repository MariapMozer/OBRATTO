from dataclasses import dataclass
from typing import Optional
from data.usuario.usuario_model import Usuario



@dataclass
class Prestador(Usuario):
    area_atuacao: Optional[str] = None
    razao_social: Optional[str] = None
    descricao_servicos: Optional[str] = None
    selo_confianca: bool = False

