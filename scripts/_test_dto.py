import sys
from pathlib import Path

# garantir que a raiz do projeto está no path para imports relativos
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root))

from dtos.usuario_dto import CriarUsuarioDTO

ex = CriarUsuarioDTO(**CriarUsuarioDTO.criar_exemplo_usuario_json())
print('DTO criado:', ex)
