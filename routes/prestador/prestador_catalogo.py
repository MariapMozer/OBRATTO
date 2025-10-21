from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from util.auth_decorator import requer_autenticacao, obter_usuario_logado

router = APIRouter()


# rota catálogo de prestadores
@router.get("/catalogo", name="catalogo_prestadores")
async def catalogo_prestadores(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "prestador/catalogo/listar.html", {"request": request, "usuario_logado": usuario_logado}
    )
