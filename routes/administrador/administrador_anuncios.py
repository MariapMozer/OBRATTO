from typing import Optional
from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates")


@router.get("/moderar_anuncios")
@requer_autenticacao(["administrador"])
async def moderar_anuncios(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "administrador/moderar_anuncios.html", {"request": request, "usuario_logado": usuario_logado}
    )


@router.get("/relatorios_anuncios")
@requer_autenticacao(["administrador"])
async def relatorios_anuncios(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "administrador/relatorios_anuncios.html", {"request": request, "usuario_logado": usuario_logado}
    )
