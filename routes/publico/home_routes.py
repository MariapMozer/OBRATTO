"""
Rotas públicas da home e páginas principais
"""
from fastapi import APIRouter, Request
from util.auth_decorator import obter_usuario_logado
from util.template_util import criar_templates

router = APIRouter(tags=["Home Pública"])
templates = criar_templates("templates")


@router.get("/")
async def get_root(request: Request):
    """Página inicial do site"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "public/home.html",
        {"request": request, "usuario_logado": usuario_logado}
    )


@router.get("/escolha_cadastro")
async def mostrar_escolha_cadastro(request: Request):
    """Página de escolha do tipo de cadastro"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "auth/escolha_cadastro.html",
        {"request": request, "usuario_logado": usuario_logado}
    )
