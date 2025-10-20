from typing import Optional
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from utils.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/moderar_anuncios")
@requer_autenticacao(['administrador'])
async def moderar_anuncios(request: Request, usuario_logado: Optional[dict] = None):
	return templates.TemplateResponse("administrador/moderar_anuncios.html", {"request": request})
