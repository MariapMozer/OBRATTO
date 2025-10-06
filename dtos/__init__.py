# Base
from .base_dto import BaseDTO

# DTOs de Usuário
from .usuario_dto import (
    CriarUsuarioDTO,
    AtualizarUsuarioDTO
)

# DTOs de Autenticação
from .login_dto import LoginDTO

# DTOs de Cliente
from .cliente_dto import (
    CriarClienteDTO,
    AtualizarClienteDTO
)

# DTOs de Prestador  
from .prestador_dto import (
    CriarPrestadorDTO,
    AtualizarPrestadorDTO
)

# DTOs de Fornecedor
from .fornecedor_dto import (
    CriarFornecedorDTO,
    AtualizarFornecedorDTO
)

__all__ = [
    # Base
    'BaseDTO',

    # Usuário
    'CriarUsuarioDTO',
    'AtualizarUsuarioDTO',
    'LoginDTO',

    # Cliente
    'CriarClienteDTO',
    'AtualizarClienteDTO',

    # Prestador
    'CriarPrestadorDTO',
    'AtualizarPrestadorDTO',

    # Fornecedor
    'CriarFornecedorDTO',
    'AtualizarFornecedorDTO',
]