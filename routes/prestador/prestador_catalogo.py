from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()


# rota catálogo de prestadores
@router.get("/catalogo", name="catalogo_prestadores")
async def catalogo_prestadores(request: Request):
    return templates.TemplateResponse(
        "prestador/catalogo/catalogo_prestadores.html", {"request": request}
    )
