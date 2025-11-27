from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from util.auth_decorator import requer_autenticacao

router = APIRouter()


# Rota para agenda do prestador
@router.get("/agenda")
@requer_autenticacao(["prestador"])
async def agenda_prestador(request: Request):
    return templates.TemplateResponse(
        "prestador/agenda/agenda.html", {"request": request}
    )




