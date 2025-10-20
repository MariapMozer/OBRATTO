from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from util.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Rota para lista de contratações
@router.get("/contratacoes/")
@requer_autenticacao(["cliente"])
async def cliente_contratacoes(request: Request):
    return templates.TemplateResponse(
        "cliente/contratacoes/minhas_contratacoes.html",
        {
            "request": request,
            "contratacoes": "contratacoes",
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )


# Rota para avaliar contratação
@router.get("/avaliar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def avaliar_contratacao(request: Request, id_contratacao: int):
    return templates.TemplateResponse(
        "cliente/contratacoes/avaliar_contratacao.html",
        {
            "request": request,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )


# Rota para lista de solicitações de contratação
@router.get("/solicitacoes de contratação/")
@requer_autenticacao(["cliente"])
async def cliente_solicitacoes(request: Request):
    return templates.TemplateResponse(
        "cliente/contratacoes/minhas_solicitacoes.html",
        {
            "request": request,
            "solicitacoes": "solicitacoes",
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para cancelar solicitação
@router.get("/cancelar_solicitacao/{id_solicitacao}")
@requer_autenticacao(["cliente"])
async def cancelar_solicitacao(request: Request, id_solicitacao: int):
    return templates.TemplateResponse(
        "cliente/cancelar_solicitacao.html",
        {
            "request": request,
            "id_solicitacao": id_solicitacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para cancelar contratação
@router.get("/cancelar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def cancelar_contratacao(request: Request, id_contratacao: int):
    return templates.TemplateResponse(
        "cliente/contratacoes/cancelar_contratacao.html",
        {
            "request": request,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para pagamento de contratação
@router.get("/pagar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def pagar_contratacao(request: Request, id_contratacao: int):
    return templates.TemplateResponse(
        "cliente/pagar_contratacao.html",
        {
            "request": request,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )
