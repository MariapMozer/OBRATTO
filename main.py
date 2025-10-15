import os
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from routes.publico import publico_routes
from routes.fornecedor import fornecedor_pagamento
from routes.fornecedor import fornecedor_produtos
from routes.fornecedor import fornecedor_planos
from routes.fornecedor import fornecedor_mensagens
from routes.fornecedor import fornecedor_perfil
from routes.fornecedor import fornecedor_promocoes
from routes.fornecedor import fornecedor_solicitacoes_orcamento
from routes.administrador import administrador_anuncios
from routes.administrador import administrador_usuarios
from routes import prestador
from routes.prestador import prestador_agenda, prestador_catalogo, prestador_contratacoes, prestador_pagamento, prestador_perfil
from routes.prestador import prestador_planos
from routes.prestador import prestador_solicitacoes
from routes.prestador import prestador_servicos
from routes.cliente import cliente_perfil
from routes.cliente import cliente_contratacoes
from utils.seed import criar_tabelas


criar_tabelas()

app = FastAPI(
    title="Obratto",
    description="Plataforma para gerenciamento de produtos de fornecedores e serviços de prestadores.",
    version="1.0.0",
    # lifespan=lifespan
)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar middleware de sessão
SECRET_KEY = os.getenv("SECRET_KEY", "sua-chave-secreta-aqui")
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,  # 1 hora
    same_site="lax",
    https_only=False  # True em produção com HTTPS
)

# PÚBLICO
app.include_router(publico_routes.router)

# FORNECEDOR
app.include_router(fornecedor_promocoes.router, prefix="/fornecedor/promocao")
app.include_router(fornecedor_perfil.router, prefix="/fornecedor")
app.include_router(fornecedor_solicitacoes_orcamento.router, prefix="/fornecedor")
app.include_router(fornecedor_produtos.router, prefix="/fornecedor/produtos")
app.include_router(fornecedor_produtos.router, prefix="/fornecedor")
app.include_router(fornecedor_planos.router, prefix="/fornecedor/planos")
app.include_router(fornecedor_pagamento.router, prefix="/fornecedor/pagamento")
app.include_router(fornecedor_mensagens.router, prefix="/fornecedor/mensagens")

# ADMINISTRADOR
app.include_router(administrador_usuarios.router, prefix="/administrador")
app.include_router(administrador_anuncios.router, prefix="/administrador")

# PRESTADOR
app.include_router(prestador_perfil.router, prefix="/prestador")
app.include_router(prestador_agenda.router, prefix="/prestador")
app.include_router(prestador_planos.router, prefix="/prestador")
app.include_router(prestador_solicitacoes.router, prefix="/prestador")   
app.include_router(prestador_servicos.router, prefix="/prestador")
app.include_router(prestador_contratacoes.router, prefix="/prestador")
app.include_router(prestador_pagamento.router, prefix="/prestador" )
app.include_router(prestador_catalogo.router, prefix="/prestador")


# CLIENTE
app.include_router(cliente_perfil.router, prefix="/cliente")
app.include_router(cliente_contratacoes.router, prefix="/cliente")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
