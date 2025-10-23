from typing import Optional
from fastapi import APIRouter, Request

from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates

router = APIRouter()
templates = criar_templates("templates")


# Rota para lista de contratações
@router.get("/contratacoes/")
@requer_autenticacao(["cliente"])
async def cliente_contratacoes(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/contratacoes/minhas_contratacoes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "contratacoes": "contratacoes",
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )


# Rota para avaliar contratação
@router.get("/avaliar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def avaliar_contratacao(request: Request, id_contratacao: int, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/contratacoes/avaliar_contratacao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )


# Rota para lista de solicitações de contratação
@router.get("/solicitacoes de contratação/")
@requer_autenticacao(["cliente"])
async def cliente_solicitacoes(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/contratacoes/minhas_solicitacoes.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "solicitacoes": "solicitacoes",
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para cancelar solicitação
@router.get("/cancelar_solicitacao/{id_solicitacao}")
@requer_autenticacao(["cliente"])
async def cancelar_solicitacao(request: Request, id_solicitacao: int, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/cancelar_solicitacao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "id_solicitacao": id_solicitacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para cancelar contratação
@router.get("/cancelar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def cancelar_contratacao(request: Request, id_contratacao: int, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/contratacoes/cancelar_contratacao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "solicitacoes",
        },
    )


# Rota para pagamento de contratação
@router.get("/pagar_contratacao/{id_contratacao}")
@requer_autenticacao(["cliente"])
async def pagar_contratacao(request: Request, id_contratacao: int, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "cliente/pagar_contratacao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "id_contratacao": id_contratacao,
            "id_cliente": "id_cliente_logado",
            "pagina_ativa": "contratacoes",
        },
    )
