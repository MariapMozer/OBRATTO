from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from data.plano.plano_repo import PlanoRepository
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from util.mercadopago_config import mp_config
from util.auth_decorator import requer_autenticacao
from services.mercadopago_service import MercadoPagoService
from services.payment_service import PaymentService
from datetime import datetime

pagamento_repo = PagamentoRepository()
plano_repo = PlanoRepository()
mercadopago_config = mp_config
mercadopago_service = MercadoPagoService()
payment_service = PaymentService()

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ===== ROTAS DE PAGAMENTO =====


@router.get("/formulario")
@requer_autenticacao(["prestador"])
async def mostrar_formulario_pagamento(
    request: Request,
    plano_id: Optional[int] = None,
    tipo_pagamento: str = "plano",
    usuario_logado: Optional[dict] = None,
):
    """
    Mostra formulário de pagamento.
    NOTA: Cartões NÃO são armazenados. Usuário deve digitar dados a cada pagamento.
    """
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    assert plano_id is not None
    plano = plano_repo.obter_plano_por_id(plano_id)
    return templates.TemplateResponse(
        "publico/pagamento-prestador/dados_pagamento.html",
        {
            "request": request,
            "plano": plano,
            "id_prestador": prestador_id,
            "tipo_operacao": "Nova Assinatura",
        },
    )


@router.get("/prestador/pagamento")
async def exibir_pagamento(request: Request):
    return templates.TemplateResponse(
        "publico/pagamento-prestador/dados_pagamento.html", {"request": request}
    )


@router.post("/processar_pagamento")
@requer_autenticacao(["prestador"])
async def processar_pagamento(
    request: Request,
    tipo_operacao: str = Form(...),
    plano_id: int = Form(None),
    valor: float = Form(...),
    metodo_pagamento: str = Form(...),
    cartao_salvo: str = Form(default=""),
    numero_cartao: str = Form(default=""),
    validade: str = Form(default=""),
    cvv: str = Form(default=""),
    nome_cartao: str = Form(default=""),
    salvar_cartao: str = Form(default=""),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]

    new_card_data = None
    if not cartao_salvo and metodo_pagamento == "cartao":
        if not numero_cartao or not validade or not cvv or not nome_cartao:
            plano = plano_repo.obter_plano_por_id(plano_id)
            return templates.TemplateResponse(
                "publico/pagamento-prestador/dados_pagamento.html",
                {
                    "request": request,
                    "plano": plano,
                    "id_prestador": prestador_id,
                    "tipo_operacao": tipo_operacao,
                    "mensagem": "Todos os campos do cartão são obrigatórios.",
                },
            )
        new_card_data = {
            "numero_cartao": numero_cartao,
            "validade": validade,
            "cvv": cvv,
            "nome_cartao": nome_cartao,
            "salvar_cartao": salvar_cartao,
        }

    result = await payment_service.process_plan_payment(
        prestador_id=prestador_id,
        plano_id=plano_id,
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        card_token=None,  # TODO: Implementar tokenização de cartão no frontend
        user_email=usuario_logado.get("email"),
    )

    if result["success"]:
        if result["status"] == "approved":
            return templates.TemplateResponse(
                "publico/pagamento-prestador/pagamento_sucesso.html",
                {
                    "request": request,
                    "plano": plano_repo.obter_plano_por_id(plano_id),
                    "tipo_operacao": tipo_operacao,
                    "metodo_pagamento": metodo_pagamento,
                    "mensagem": f"{tipo_operacao} processada com sucesso! Pagamento via {metodo_pagamento.upper()} aprovado.",
                },
            )
        elif result["status"] == "pending":
            return templates.TemplateResponse(
                "publico/pagamento-prestador/pagamento_pendente.html",
                {
                    "request": request,
                    "plano": plano_repo.obter_plano_por_id(plano_id),
                    "tipo_operacao": tipo_operacao,
                    "metodo_pagamento": metodo_pagamento,
                    "mensagem": f"{tipo_operacao} processada. Pagamento via {metodo_pagamento.upper()} pendente.",
                },
            )
        else:
            return templates.TemplateResponse(
                "publico/pagamento-prestador/pagamento_erro.html",
                {
                    "request": request,
                    "tipo_operacao": tipo_operacao,
                    "mensagem": f"Pagamento via {metodo_pagamento.upper()} {result['status']}.",
                },
            )
    else:
        plano = plano_repo.obter_plano_por_id(plano_id)
        return templates.TemplateResponse(
            "publico/pagamento-prestador/dados_pagamento.html",
            {
                "request": request,
                "plano": plano,
                "id_prestador": prestador_id,
                "tipo_operacao": tipo_operacao,
                "mensagem": result["message"],
            },
        )


# ===== ROTAS DE WEBHOOK =====
@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(request: Request):
    notification_data = await request.json()
    result = await payment_service.handle_mercadopago_webhook(notification_data)
    if result["success"]:
        return JSONResponse(content={"message": result["message"]}, status_code=200)
    else:
        return JSONResponse(content={"message": result["message"]}, status_code=400)
