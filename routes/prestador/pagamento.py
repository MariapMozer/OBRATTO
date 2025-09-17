
from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from data.plano import plano_repo
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano import inscricao_plano_repo
from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from data.cartao.cartao_model import CartaoCredito
from data.cartao.cartao_repo import CartaoRepository
from utils.mercadopago_config import mp_config
from utils.auth_decorator import requer_autenticacao

pagamento_repo = PagamentoRepository()
cartao_repo = CartaoRepository()
mercadopago_config = mp_config
router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/formulario")
@requer_autenticacao(['prestador'])
async def mostrar_formulario_pagamento(
    request: Request,
    plano_id: int = None,
    tipo_pagamento: str = "plano",
    usuario_logado: dict = None
):
    # Apenas prestador autenticado
    prestador_id = usuario_logado.id
    plano = plano_repo.obter_plano_por_id(plano_id)
    cartoes = cartao_repo.obter_cartoes_prestador(prestador_id)
    return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
        "request": request,
        "plano": plano,
        "id_fornecedor": fornecedor_id,
        "tipo_operacao": "Nova Assinatura",
        "cartoes": cartoes
    })
