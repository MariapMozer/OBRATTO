from typing import Optional
from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from data.orcamento import orcamento_repo
from data.cliente import cliente_repo
import datetime

router = APIRouter()
templates = criar_templates("templates")


# Rota GET para exibir solicitações recebidas
@router.get("/solicitacoes_recebidas")
@requer_autenticacao(["fornecedor"])
async def solicitacoes_recebidas(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    # obter todos os orçamentos e filtrar pelo fornecedor logado
    todos = orcamento_repo.obter_todos_orcamentos()
    solicitacoes = []
    for o in todos:
        if getattr(o, 'id_fornecedor', None) == usuario_logado['id']:
            # Buscar dados do cliente para exibir nome/avatar
            cliente = cliente_repo.obter_cliente_por_id(o.id_cliente)
            solicitacoes.append(
                {
                    'id': o.id,
                    'cliente_id': o.id_cliente,
                    'cliente_nome': cliente.nome if cliente else 'Cliente',
                    'cliente_avatar': getattr(cliente, 'foto', None) if cliente else None,
                    'produto_nome': getattr(o, 'descricao', '')[:50],
                    'mensagem': getattr(o, 'descricao', ''),
                    'data': o.data_solicitacao.strftime('%d/%m/%Y') if hasattr(o, 'data_solicitacao') else '',
                    'conversa_id': None,
                }
            )

    return templates.TemplateResponse(
        "fornecedor/orcamentos/recebidas.html",
        {"request": request, "solicitacoes": solicitacoes, "usuario_logado": usuario_logado},
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
