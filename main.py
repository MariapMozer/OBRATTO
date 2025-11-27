import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# --- APP / DB ---
from util.seed import criar_tabelas
from util.db import seed_usuarios_padrao
from util.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)

# --- CONFIG / LOGGER ---
try:
    from util.config import SECRET_KEY, SESSION_MAX_AGE, APP_NAME, VERSION
    from util.logger_config import logger
except ImportError:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não configurada!")
    SESSION_MAX_AGE = 3600
    import logging
    logger = logging.getLogger(__name__)

# --- ROTAS ---

# Público
from routes.publico import router as publico_router
from routes.publico import test_toasts

# Fornecedor
from routes.fornecedor import fornecedor_pagamento
from routes.fornecedor import fornecedor_produtos
from routes.fornecedor import fornecedor_planos
from routes.fornecedor import fornecedor_mensagens
from routes.fornecedor import fornecedor_perfil
from routes.fornecedor import fornecedor_promocoes
from routes.fornecedor import fornecedor_solicitacoes_orcamento

# Administrador
from routes.administrador import administrador_anuncios
from routes.administrador import administrador_usuarios

# Prestador
from routes.prestador import prestador_agenda
from routes.prestador import prestador_catalogo
from routes.prestador import prestador_contratacoes
from routes.prestador import prestador_pagamento
from routes.prestador import prestador_perfil
from routes.prestador import prestador_planos
from routes.prestador import prestador_solicitacoes
from routes.prestador import prestador_servicos
from routes.prestador.prestador_home import router as prestador_home_router

# Cliente
from routes.cliente import cliente_perfil
from routes.cliente import cliente_contratacoes


# ----------------------------------------------------------
# INICIALIZAÇÃO DO BANCO
# ----------------------------------------------------------
criar_tabelas()
seed_usuarios_padrao()

# ----------------------------------------------------------
# CRIAÇÃO DO APP
# ----------------------------------------------------------
app = FastAPI(
    title="Obratto",
    description="Plataforma para gerenciamento de fornecedores, prestadores e clientes.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

logger.info(f"{APP_NAME} v{VERSION} iniciando...")
logger.info("SessionMiddleware configurado")
logger.info("Exception handlers registrados")

# ----------------------------------------------------------
# MIDDLEWARE
# ----------------------------------------------------------
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=SESSION_MAX_AGE,
    same_site="lax",
    https_only=False,
)

# ----------------------------------------------------------
# EXCEPTION HANDLERS
# ----------------------------------------------------------
@app.exception_handler(StarletteHTTPException)
async def _http_exception_handler(request: Request, exc: StarletteHTTPException):
    return await http_exception_handler(request, exc)

@app.exception_handler(RequestValidationError)
async def _validation_exception_handler(request: Request, exc: RequestValidationError):
    return await validation_exception_handler(request, exc)

@app.exception_handler(Exception)
async def _generic_exception_handler(request: Request, exc: Exception):
    return await generic_exception_handler(request, exc)


# ----------------------------------------------------------
# ROTAS - PÚBLICO
# ----------------------------------------------------------
app.include_router(publico_router)
app.include_router(test_toasts.router)

# ----------------------------------------------------------
# ROTAS - FORNECEDOR
# ----------------------------------------------------------
app.include_router(fornecedor_promocoes.router, prefix="/fornecedor")
app.include_router(fornecedor_perfil.router, prefix="/fornecedor")
app.include_router(fornecedor_solicitacoes_orcamento.router, prefix="/fornecedor")
app.include_router(fornecedor_produtos.router, prefix="/fornecedor")
app.include_router(fornecedor_planos.router, prefix="/fornecedor")
app.include_router(fornecedor_pagamento.router, prefix="/fornecedor")
app.include_router(fornecedor_mensagens.router, prefix="/fornecedor")

# ----------------------------------------------------------
# ROTAS - ADMINISTRADOR
# ----------------------------------------------------------
app.include_router(administrador_usuarios.router, prefix="/administrador")
app.include_router(administrador_anuncios.router, prefix="/administrador")

# ----------------------------------------------------------
# ROTAS - PRESTADOR
# ----------------------------------------------------------
app.include_router(prestador_perfil.router, prefix="/prestador")
app.include_router(prestador_agenda.router, prefix="/prestador")
app.include_router(prestador_planos.router, prefix="/prestador")
app.include_router(prestador_solicitacoes.router, prefix="/prestador")
app.include_router(prestador_servicos.router, prefix="/prestador")
app.include_router(prestador_contratacoes.router, prefix="/prestador")
app.include_router(prestador_pagamento.router, prefix="/prestador")
app.include_router(prestador_catalogo.router, prefix="/prestador")
app.include_router(prestador_home_router, prefix="/prestador")  # CORRETO!

# ----------------------------------------------------------
# ROTAS - CLIENTE
# ----------------------------------------------------------
app.include_router(cliente_perfil.router, prefix="/cliente")
app.include_router(cliente_contratacoes.router, prefix="/cliente")


# ----------------------------------------------------------
# RUN
# ----------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
