from typing import Optional
from fastapi import APIRouter, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from data.plano.plano_repo import PlanoRepository
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
#from data.inscricaoplano.inscricao_plano_repo import InscricaoPlanoRepository
from data.pagamento.pagamento_model import Pagamento
from data.pagamento.pagamento_repo import PagamentoRepository
from data.cartao.cartao_model import CartaoCredito
from data.cartao.cartao_repo import CartaoRepository
from utils.mercadopago_config import mp_config
from utils.auth_decorator import requer_autenticacao
from services.mercadopago_service import MercadoPagoService
from services.payment_service import PaymentService
from datetime import datetime

pagamento_repo = PagamentoRepository()
cartao_repo = CartaoRepository()
#inscricao_plano_repo = InscricaoPlanoRepository()
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
    usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    assert plano_id is not None
    plano = plano_repo.obter_plano_por_id(plano_id)
    cartoes = cartao_repo.obter_cartoes_por_prestador(prestador_id)
    return templates.TemplateResponse("publico/pagamento-prestador/dados_pagamento.html", {
        "request": request,
        "plano": plano,
        "id_prestador": prestador_id,
        "tipo_operacao": "Nova Assinatura",
        "cartoes": cartoes
    })

@router.get("/prestador/pagamento")
async def exibir_pagamento(request: Request):
    return templates.TemplateResponse(
        "publico/pagamento-prestador/dados_pagamento.html",
        {"request": request}
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
    usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    
    new_card_data = None
    if not cartao_salvo and metodo_pagamento == "cartao":
        if not numero_cartao or not validade or not cvv or not nome_cartao:
            cartoes = cartao_repo.obter_cartoes_por_prestador(prestador_id)
            plano = plano_repo.obter_plano_por_id(plano_id)
            return templates.TemplateResponse("publico/pagamento-prestador/dados_pagamento.html", {
                "request": request, "plano": plano, "id_prestador": prestador_id,
                "tipo_operacao": tipo_operacao, "cartoes": cartoes,
                "mensagem": "Todos os campos do cartão são obrigatórios."
            })
        new_card_data = {
            "numero_cartao": numero_cartao,
            "validade": validade,
            "cvv": cvv,
            "nome_cartao": nome_cartao,
            "salvar_cartao": salvar_cartao
        }

    result = await payment_service.process_plan_payment(
        prestador_id=prestador_id,
        plano_id=plano_id,
        valor=valor,
        metodo_pagamento=metodo_pagamento,
        cartao_salvo_id=int(cartao_salvo) if cartao_salvo else None,
        new_card_data=new_card_data
    )

    if result["success"]:
        if result["status"] == "approved":
            return templates.TemplateResponse("publico/pagamento-prestador/pagamento_sucesso.html", {
                "request": request,
                "plano": plano_repo.obter_plano_por_id(plano_id),
                "tipo_operacao": tipo_operacao,
                "metodo_pagamento": metodo_pagamento,
                "mensagem": f"{tipo_operacao} processada com sucesso! Pagamento via {metodo_pagamento.upper()} aprovado."
            })
        elif result["status"] == "pending":
            return templates.TemplateResponse("publico/pagamento-prestador/pagamento_pendente.html", {
                "request": request,
                "plano": plano_repo.obter_plano_por_id(plano_id),
                "tipo_operacao": tipo_operacao,
                "metodo_pagamento": metodo_pagamento,
                "mensagem": f"{tipo_operacao} processada. Pagamento via {metodo_pagamento.upper()} pendente."
            })
        else:
            return templates.TemplateResponse("publico/pagamento-prestador/pagamento_erro.html", {
                "request": request,
                "tipo_operacao": tipo_operacao,
                "mensagem": f"Pagamento via {metodo_pagamento.upper()} {result['status']}."
            })
    else:
        cartoes = cartao_repo.obter_cartoes_por_prestador(prestador_id)
        plano = plano_repo.obter_plano_por_id(plano_id)
        return templates.TemplateResponse("publico/pagamento-prestador/dados_pagamento.html", {
            "request": request, "plano": plano, "id_prestador": prestador_id,
            "tipo_operacao": tipo_operacao, "cartoes": cartoes,
            "mensagem": result["message"]
        })


# ===== ROTAS DE CARTÃO =====

@router.get("/cartoes")
@requer_autenticacao(["prestador"])
async def listar_cartoes(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    cartoes = cartao_repo.obter_cartoes_por_prestador(prestador_id)
    return templates.TemplateResponse("publico/pagamento-prestador/meus_cartoes.html", {
        "request": request,
        "cartoes": cartoes,
        "id_prestador": prestador_id
    })

@router.get("/cartoes/adicionar")
@requer_autenticacao(["prestador"])
async def mostrar_adicionar_cartao(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
        "request": request,
        "id_prestador": prestador_id
    })

@router.post("/cartoes/adicionar")
@requer_autenticacao(["prestador"])
async def adicionar_cartao(
    request: Request,
    numero_cartao: str = Form(...),
    nome_titular: str = Form(...),
    mes_vencimento: str = Form(...),
    ano_vencimento: str = Form(...),
    apelido: str = Form(...),
    principal: str = Form(None),
    usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    try:
        resultado = payment_service.add_card(
            prestador_id=prestador_id,
            numero_cartao=numero_cartao,
            nome_titular=nome_titular,
            mes_vencimento=mes_vencimento,
            ano_vencimento=ano_vencimento,
            apelido=apelido,
            principal=(principal == "true")
        )
        if resultado:
            return RedirectResponse(url="/prestador/pagamento/cartoes", status_code=303)
        else:
            return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
                "request": request,
                "id_prestador": prestador_id,
                "mensagem": "Erro ao salvar o cartão. Tente novamente."
            })
    except Exception as e:
        return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
            "request": request,
            "id_prestador": prestador_id,
            "mensagem": f"Erro ao processar cartão: {str(e)}"
        })

@router.get("/cartoes/editar/{id_cartao}")
@requer_autenticacao(["prestador"])
async def mostrar_editar_cartao(request: Request, id_cartao: int, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    cartao = cartao_repo.obter_cartao_por_id(id_cartao)
    if not cartao or cartao.id_fornecedor != prestador_id:
        return RedirectResponse(url="/prestador/pagamento/cartoes", status_code=303)
    return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
        "request": request,
        "cartao": cartao,
        "id_prestador": prestador_id
    })

@router.post("/cartoes/editar/{id_cartao}")
@requer_autenticacao(["prestador"])
async def editar_cartao(
    request: Request,
    id_cartao: int,
    nome_titular: str = Form(...),
    apelido: str = Form(...),
    principal: str = Form(None),
    usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    try:
        resultado = payment_service.update_card(
            id_cartao=id_cartao,
            prestador_id=prestador_id,
            nome_titular=nome_titular,
            apelido=apelido,
            principal=(principal == "true")
        )
        if resultado:
            return RedirectResponse(url="/prestador/pagamento/cartoes", status_code=303)
        else:
            cartao = cartao_repo.obter_cartao_por_id(id_cartao)
            return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
                "request": request,
                "cartao": cartao,
                "id_prestador": prestador_id,
                "mensagem": "Erro ao atualizar o cartão. Tente novamente."
            })
    except Exception as e:
        cartao = cartao_repo.obter_cartao_por_id(id_cartao)
        return templates.TemplateResponse("publico/pagamento-prestador/adicionar_cartao.html", {
            "request": request,
            "cartao": cartao if 'cartao' in locals() else None,
            "id_prestador": prestador_id,
            "mensagem": f"Erro ao processar alterações: {str(e)}"
        })

@router.get("/cartoes/excluir/{id_cartao}")
@requer_autenticacao(["prestador"])
async def mostrar_confirmar_exclusao(request: Request, id_cartao: int, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    cartao = cartao_repo.obter_cartao_por_id(id_cartao)
    if not cartao or cartao.id_fornecedor != prestador_id:
        return RedirectResponse(url="/prestador/pagamento/cartoes", status_code=303)
    return templates.TemplateResponse("publico/pagamento-prestador/confirmar_exclusao_cartao.html", {
        "request": request,
        "cartao": cartao
    })

@router.post("/cartoes/excluir/{id_cartao}")
@requer_autenticacao(["prestador"])
async def excluir_cartao(request: Request, id_cartao: int, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]
    try:
        resultado = payment_service.delete_card(id_cartao, prestador_id)
        if resultado:
            return RedirectResponse(url="/prestador/pagamento/cartoes", status_code=303)
        else:
            cartao = cartao_repo.obter_cartao_por_id(id_cartao)
            return templates.TemplateResponse("publico/pagamento-prestador/confirmar_exclusao_cartao.html", {
                "request": request,
                "cartao": cartao,
                "mensagem": "Erro ao excluir o cartão. Tente novamente."
            })
    except Exception as e:
        cartao = cartao_repo.obter_cartao_por_id(id_cartao)
        return templates.TemplateResponse("publico/pagamento-prestador/confirmar_exclusao_cartao.html", {
            "request": request,
            "cartao": cartao if 'cartao' in locals() else None,
            "mensagem": f"Erro ao processar exclusão: {str(e)}"
        })

@router.post("/cartoes/definir_principal")
@requer_autenticacao(["prestador"])
async def definir_cartao_principal(request: Request, usuario_logado: Optional[dict] = None):
    form = await request.form()
    id_cartao_raw = form.get("id_cartao")
    assert usuario_logado is not None
    prestador_id = usuario_logado["id"]

    if isinstance(id_cartao_raw, str):
        id_cartao = int(id_cartao_raw)
    else:
        id_cartao = 0
    resultado = payment_service.set_main_card(id_cartao, prestador_id)
    if resultado:
        return RedirectResponse(url=f"/prestador/pagamento/cartoes", status_code=303)
    else:
        return RedirectResponse(url=f"/prestador/pagamento/cartoes", status_code=303)

# ===== ROTAS DE WEBHOOK =====
@router.post("/webhooks/mercadopago")
async def mercadopago_webhook(request: Request):
    notification_data = await request.json()
    result = await payment_service.handle_mercadopago_webhook(notification_data)
    if result["success"]:
        return JSONResponse(content={"message": result["message"]}, status_code=200)
    else:
        return JSONResponse(content={"message": result["message"]}, status_code=400)

