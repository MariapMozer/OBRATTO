from typing import Optional
from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates")


# Rota GET para exibir solicitações recebidas
@router.get("/solicitacoes_recebidas")
@requer_autenticacao(["fornecedor"])
async def solicitacoes_recebidas(
    request: Request, usuario_logado: Optional[dict] = None
):
    return templates.TemplateResponse(
        "fornecedor/orcamentos/recebidas.html", {"request": request}
    )


@router.get("/listar")
@requer_autenticacao(["fornecedor"])
async def listar_solicitacoes(request: Request, usuario_logado: Optional[dict] = None):
    return {"message": "Listar solicitações"}


@router.get("/detalhar")
@requer_autenticacao(["fornecedor"])
async def detalhar_solicitacao(request: Request, usuario_logado: Optional[dict] = None):
    return {"message": "Detalhar solicitação"}


@router.post("/responder")
@requer_autenticacao(["fornecedor"])
async def responder_solicitacao(
    request: Request, usuario_logado: Optional[dict] = None
):
    return {"message": "Responder solicitação"}
