"""
Módulo de rotas públicas da aplicação OBRATTO.

Este módulo consolida todas as rotas públicas em submódulos organizados:
- home_routes: Página inicial e navegação principal
- auth_routes: Login, logout e recuperação de senha
- cadastro_routes: Cadastro de prestador, cliente e fornecedor
- perfil_routes: Perfis públicos de usuários
- mensagem_routes: Sistema de mensagens
- servico_routes: Catálogo de serviços

Uso no main.py:
    from routes.publico import router as publico_router
    app.include_router(publico_router)
"""
from fastapi import APIRouter

# Importar todos os subrouters
from . import (
    home_routes,
    auth_routes,
    cadastro_routes,
    perfil_routes,
    mensagem_routes,
    servico_routes,
)

# Router principal que consolida todos os subrouters
router = APIRouter()

# Incluir todos os subrouters
router.include_router(home_routes.router, tags=["Home"])
router.include_router(auth_routes.router, tags=["Autenticação"])
router.include_router(cadastro_routes.router, tags=["Cadastros"])
router.include_router(perfil_routes.router, tags=["Perfis Públicos"])
router.include_router(mensagem_routes.router, tags=["Mensagens"])
router.include_router(servico_routes.router, tags=["Serviços"])
