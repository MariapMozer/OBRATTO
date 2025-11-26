from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()


# Rota para contratações do prestador
@router.get("/minhas/contratacoes")
@requer_autenticacao(["prestador"])
async def prestador_contratacoes(request: Request):
    return templates.TemplateResponse(
        "prestador/contratacoes/minhas_contratacoes.html", {"request": request}
    )


# Rota para visualizar detalhes das contratações
@router.get("/contratacao/detalhes/{id_contratacao}")
@requer_autenticacao(["prestador"])
async def detalhes_contratacao(request: Request, id_contratacao: int):
    return templates.TemplateResponse(
        "prestador/contratacoes/detalhes.html", {"request": request}
    )
