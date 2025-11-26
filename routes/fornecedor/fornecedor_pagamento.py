from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse, JSONResponse
from data.plano import plano_repo
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano import inscricao_plano_repo
from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from util.mercadopago_config import mp_config
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from datetime import datetime

pagamento_repo = PagamentoRepository()
mercadopago_config = mp_config
router = APIRouter()
templates = criar_templates("templates")


@router.get("/formulario")
@requer_autenticacao(["fornecedor"])
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
    fornecedor_id = usuario_logado["id"]

    plano = None
    if plano_id is not None:
        plano = plano_repo.obter_plano_por_id(plano_id)

    return templates.TemplateResponse(
        "fornecedor/pagamento/dados.html",
        {
            "request": request,
            "plano": plano,
            "id_fornecedor": fornecedor_id,
            "tipo_operacao": "Nova Assinatura",
        },
    )


@router.post("/processar_pagamento")
@requer_autenticacao(["fornecedor"])
async def processar_pagamento(
    request: Request,
    tipo_operacao: str = Form(...),
    plano_id: int = Form(None),
    valor: float = Form(...),
    metodo_pagamento: str = Form(...),
    numero_cartao: str = Form(default=""),
    validade: str = Form(default=""),
    cvv: str = Form(default=""),
    nome_cartao: str = Form(default=""),
    usuario_logado: Optional[dict] = None,
):
    """
    Processa pagamento SEM armazenar dados de cartão.
    Dados do cartão são usados apenas para processamento via Mercado Pago.
    """
    assert usuario_logado is not None
    fornecedor_id = usuario_logado["id"]

    # Validar plano
    plano = plano_repo.obter_plano_por_id(plano_id)
    if not plano:
        return templates.TemplateResponse(
            "fornecedor/pagamento/dados.html",
            {
                "request": request,
                "mensagem": "Plano não encontrado.",
                "id_fornecedor": fornecedor_id,
            },
        )

    # Validar campos de cartão se for pagamento com cartão
    if metodo_pagamento == "cartao":
        if not numero_cartao or not validade or not cvv or not nome_cartao:
            return templates.TemplateResponse(
                "fornecedor/pagamento/dados.html",
                {
                    "request": request,
                    "plano": plano,
                    "id_fornecedor": fornecedor_id,
                    "tipo_operacao": tipo_operacao,
                    "mensagem": "Todos os campos do cartão são obrigatórios.",
                },
            )

    # Verificar se já tem assinatura ativa
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(
        fornecedor_id
    )
    if assinatura_ativa:
        return templates.TemplateResponse(
            "fornecedor/pagamento/dados.html",
            {
                "request": request,
                "plano": plano,
                "id_fornecedor": fornecedor_id,
                "tipo_operacao": tipo_operacao,
                "mensagem": "Você já possui uma assinatura ativa.",
            },
        )

    # Criar inscrição no plano
    nova_inscricao = InscricaoPlano(
        id_inscricao_plano=0,
        id_fornecedor=fornecedor_id,
        id_prestador=None,
        id_plano=plano_id,
    )
    inscricao_id = inscricao_plano_repo.inserir_inscricao_plano(nova_inscricao)
    reference = f"assinatura_plano_{plano_id}_fornecedor_{fornecedor_id}"

    # TODO: Integrar com Mercado Pago para tokenização
    # Por enquanto, simular pagamento aprovado
    pagamento = Pagamento(
        id_pagamento=0,
        plano_id=plano_id,
        fornecedor_id=fornecedor_id,
        mp_payment_id=f"{metodo_pagamento}_payment_{inscricao_id}_{int(datetime.now().timestamp())}",
        mp_preference_id=f"{metodo_pagamento}_pref_{inscricao_id}_{int(datetime.now().timestamp())}",
        valor=valor,
        status="aprovado",
        metodo_pagamento=f"{metodo_pagamento}_simulado",
        data_criacao=datetime.now().isoformat(),
        data_aprovacao=datetime.now().isoformat(),
        external_reference=reference,
    )

    pagamento_inserido = pagamento_repo.inserir_pagamento(pagamento)
    if pagamento_inserido:
        return templates.TemplateResponse(
            "fornecedor/pagamento/sucesso.html",
            {
                "request": request,
                "plano": plano,
                "tipo_operacao": tipo_operacao,
                "metodo_pagamento": metodo_pagamento,
                "mensagem": f"{tipo_operacao} processada com sucesso! Pagamento via {metodo_pagamento.upper()} aprovado.",
            },
        )

    return templates.TemplateResponse(
        "fornecedor/pagamento/erro.html",
        {
            "request": request,
            "tipo_operacao": tipo_operacao,
            "mensagem": "Erro ao processar pagamento.",
        },
    )


# Callback de sucesso do Mercado Pago
@router.get("/sucesso")
@requer_autenticacao(["fornecedor"])
async def pagamento_sucesso(
    request: Request,
    payment_id: Optional[str] = None,
    status: Optional[str] = None,
    external_reference: Optional[str] = None,
):
    if payment_id:
        payment_info = mp_config.get_payment_info(payment_id)
        if payment_info.get("status") == "approved":
            pagamento_repo.atualizar_status_pagamento(
                mp_payment_id=payment_id,
                status="aprovado",
                metodo_pagamento=payment_info.get("payment_method_id"),
            )
            return templates.TemplateResponse(
                "fornecedor/pagamento/sucesso.html",
                {
                    "request": request,
                    "payment_info": payment_info,
                    "mensagem": "Pagamento aprovado com sucesso! Seu plano está ativo.",
                },
            )
    return templates.TemplateResponse(
        "fornecedor/pagamento/sucesso.html",
        {"request": request, "mensagem": "Pagamento processado com sucesso!"},
    )


# Callback de falha do Mercado Pago
@router.get("/falha")
@requer_autenticacao(["fornecedor"])
async def pagamento_falha(request: Request):
    return templates.TemplateResponse(
        "fornecedor/pagamento/erro.html",
        {
            "request": request,
            "mensagem": "Pagamento rejeitado ou cancelado. Tente novamente.",
        },
    )


# Callback de pagamento pendente
@router.get("/pendente")
@requer_autenticacao(["fornecedor"])
async def pagamento_pendente(request: Request):
    return templates.TemplateResponse(
        "fornecedor/pagamento/pendente.html",
        {
            "request": request,
            "mensagem": "Pagamento pendente de aprovação. Aguarde a confirmação.",
        },
    )
