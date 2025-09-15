
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
@requer_autenticacao(['fornecedor'])
async def mostrar_formulario_pagamento(
    request: Request,
    plano_id: int = None,
    tipo_pagamento: str = "plano",
    usuario_logado: dict = None
):
    # Apenas fornecedor autenticado
    fornecedor_id = usuario_logado.id
    plano = plano_repo.obter_plano_por_id(plano_id)
    cartoes = cartao_repo.obter_cartoes_fornecedor(fornecedor_id)
    return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
        "request": request,
        "plano": plano,
        "id_fornecedor": fornecedor_id,
        "tipo_operacao": "Nova Assinatura",
        "cartoes": cartoes
    })

# Processar pagamento
@router.post("/processar_pagamento")
@requer_autenticacao(['fornecedor'])
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
    usuario_logado: dict = None
):
    fornecedor_id = usuario_logado.id
    plano = plano_repo.obter_plano_por_id(plano_id)
    if not plano:
        cartoes = cartao_repo.obter_cartoes_fornecedor(fornecedor_id)
        return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
            "request": request, "mensagem": "Plano não encontrado.", "cartoes": cartoes
        })
    cartoes = cartao_repo.obter_cartoes_fornecedor(fornecedor_id)
    cartao_usado = None
    if cartao_salvo:
        try:
            cartao_usado = cartao_repo.obter_cartao_por_id(int(cartao_salvo))
            if not cartao_usado or cartao_usado.id_fornecedor != fornecedor_id:
                return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
                    "request": request, "plano": plano, "id_fornecedor": fornecedor_id,
                    "tipo_operacao": tipo_operacao, "cartoes": cartoes,
                    "mensagem": "Cartão selecionado não é válido."
                })
        except ValueError:
            return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
                "request": request, "plano": plano, "id_fornecedor": fornecedor_id,
                "tipo_operacao": tipo_operacao, "cartoes": cartoes,
                "mensagem": "Cartão selecionado não é válido."
            })
    else:
        if metodo_pagamento == "cartao":
            if not numero_cartao or not validade or not cvv or not nome_cartao:
                return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
                    "request": request, "plano": plano, "id_fornecedor": fornecedor_id,
                    "tipo_operacao": tipo_operacao, "cartoes": cartoes,
                    "mensagem": "Todos os campos do cartão são obrigatórios."
                })
            if salvar_cartao == "true":
                try:
                    mes_vencimento, ano_vencimento = validade.split('/')
                    cartao_repo.criar_cartao_from_form(
                        id_fornecedor=fornecedor_id,
                        numero_cartao=numero_cartao.replace(' ', ''),
                        nome_titular=nome_cartao,
                        mes_vencimento=mes_vencimento,
                        ano_vencimento=ano_vencimento,
                        apelido=f"Cartão •••• {numero_cartao.replace(' ', '')[-4:]}",
                        principal=False
                    )
                except Exception as e:
                    print(f"Erro ao salvar cartão: {e}")
    from datetime import datetime
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(fornecedor_id)
    if assinatura_ativa:
        return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
            "request": request, "plano": plano, "id_fornecedor": fornecedor_id,
            "tipo_operacao": tipo_operacao, "mensagem": "Você já possui uma assinatura ativa."
        })
    nova_inscricao = InscricaoPlano(
        id_inscricao_plano=0,
        id_fornecedor=fornecedor_id,
        id_prestador=None,
        id_plano=plano_id
    )
    inscricao_id = inscricao_plano_repo.inserir_inscricao_plano(nova_inscricao)
    reference = f"assinatura_plano_{plano_id}_fornecedor_{fornecedor_id}"
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
        external_reference=reference
    )
    pagamento_inserido = pagamento_repo.inserir_pagamento(pagamento)
    if pagamento_inserido:
        return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
            "request": request,
            "plano": plano,
            "tipo_operacao": tipo_operacao,
            "metodo_pagamento": metodo_pagamento,
            "mensagem": f"{tipo_operacao} processada com sucesso! Pagamento via {metodo_pagamento.upper()} aprovado."
        })
    return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
        "request": request,
        "tipo_operacao": tipo_operacao,
        "mensagem": "Acesso permitido apenas para fornecedores."
    })

# Callback de sucesso do Mercado Pago
@router.get("/sucesso")
@requer_autenticacao(['fornecedor'])
async def pagamento_sucesso(
    request: Request, 
    payment_id: str = None, 
    status: str = None, 
    external_reference: str = None):
    if payment_id:
        payment_info = mp_config.get_payment_info(payment_id)
        if payment_info.get("status") == "approved":
            pagamento_repo.atualizar_status_pagamento(
                mp_payment_id=payment_id,
                status="aprovado",
                metodo_pagamento=payment_info.get("payment_method_id")
            )
            return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
                "request": request, 
                "payment_info": payment_info, 
                "mensagem": "Pagamento aprovado com sucesso! Seu plano está ativo."
            })
    return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
        "request": request, 
        "mensagem": "Pagamento processado com sucesso!"
    })

# Callback de falha do Mercado Pago
@router.get("/falha")
@requer_autenticacao(['fornecedor'])
async def pagamento_falha(request: Request):
    return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
        "request": request, "mensagem": "Pagamento rejeitado ou cancelado. Tente novamente."
    })

# Callback de pagamento pendente
@router.get("/pendente")
@requer_autenticacao(['fornecedor'])
async def pagamento_pendente(request: Request):
    return templates.TemplateResponse("publico/pagamento/pagamento_pendente.html", {
        "request": request, "mensagem": "Pagamento pendente de aprovação. Aguarde a confirmação."
    })


# ===== ROTAS DE GERENCIAMENTO DE CARTÕES =====

@router.get("/cartoes")
@requer_autenticacao(['fornecedor'])
async def listar_cartoes(request: Request, usuario_logado: dict = None):
    fornecedor_id = usuario_logado.id
    cartoes = cartao_repo.obter_cartoes_fornecedor(fornecedor_id)
    return templates.TemplateResponse("publico/pagamento/meus_cartoes.html", {
        "request": request,
        "cartoes": cartoes,
        "id_fornecedor": fornecedor_id
    })

# Mostrar formulário para adicionar cartão
@router.get("/cartoes/adicionar")
@requer_autenticacao(['fornecedor'])
async def mostrar_adicionar_cartao(request: Request, usuario_logado: dict = None):
    fornecedor_id = usuario_logado.id
    return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
        "request": request,
        "id_fornecedor": fornecedor_id
    })

# Processar adição de cartão
@router.post("/cartoes/adicionar")
@requer_autenticacao(['fornecedor'])
async def adicionar_cartao(
    request: Request,
    numero_cartao: str = Form(...),
    nome_titular: str = Form(...),
    mes_vencimento: str = Form(...),
    ano_vencimento: str = Form(...),
    apelido: str = Form(...),
    principal: str = Form(None),
    usuario_logado: dict = None
):
    fornecedor_id = usuario_logado.id
    try:
        resultado = cartao_repo.criar_cartao_from_form(
            id_fornecedor=fornecedor_id,
            numero_cartao=numero_cartao,
            nome_titular=nome_titular,
            mes_vencimento=mes_vencimento,
            ano_vencimento=ano_vencimento,
            apelido=apelido,
            principal=(principal == "true")
        )
        if resultado:
            return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
        else:
            return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
                "request": request,
                "id_fornecedor": fornecedor_id,
                "mensagem": "Erro ao salvar o cartão. Tente novamente."
            })
    except Exception as e:
        return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
            "request": request,
            "id_fornecedor": fornecedor_id,
            "mensagem": f"Erro ao processar cartão: {str(e)}"
        })
   

# Mostrar formulário para editar cartão

@router.get("/cartoes/editar/{id_cartao}")
@requer_autenticacao(['fornecedor'])
async def mostrar_editar_cartao(request: Request, id_cartao: int, usuario_logado: dict = None):
    fornecedor_id = usuario_logado.id
    cartao = cartao_repo.obter_cartao_por_id(id_cartao)
    if not cartao or cartao.id_fornecedor != fornecedor_id:
        return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
    return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
        "request": request,
        "cartao": cartao,
        "id_fornecedor": fornecedor_id
    })

# Processar edição de cartão
@router.post("/cartoes/editar/{id_cartao}")
@requer_autenticacao(['fornecedor'])
async def editar_cartao(
    request: Request,
    id_cartao: int,
    nome_titular: str = Form(...),
    apelido: str = Form(...),
    principal: str = Form(None),
    usuario_logado: dict = None
):
    fornecedor_id = usuario_logado.id
    try:
        cartao = cartao_repo.obter_cartao_por_id(id_cartao)
        if not cartao or cartao.id_fornecedor != fornecedor_id:
            return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
        cartao.nome_titular = nome_titular.strip().upper()
        cartao.apelido = apelido.strip()
        cartao.principal = (principal == "true")
        resultado = cartao_repo.atualizar_cartao(cartao)
        if resultado:
            return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
        else:
            return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
                "request": request,
                "cartao": cartao,
                "id_fornecedor": fornecedor_id,
                "mensagem": "Erro ao atualizar o cartão. Tente novamente."
            })
    except Exception as e:
        return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
            "request": request,
            "cartao": cartao if 'cartao' in locals() else None,
            "id_fornecedor": fornecedor_id,
            "mensagem": f"Erro ao processar alterações: {str(e)}"
        })
    

# Mostrar confirmação de exclusão
@router.get("/cartoes/excluir/{id_cartao}") # Nesse caso é perigoso?
@requer_autenticacao(['fornecedor'])
async def mostrar_confirmar_exclusao(request: Request, id_cartao: int, usuario_logado: dict = None):
    fornecedor_id = usuario_logado.id
    cartao = cartao_repo.obter_cartao_por_id(id_cartao)
    if not cartao or cartao.id_fornecedor != fornecedor_id:
        return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
    return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
        "request": request,
        "cartao": cartao
    })

# Processar exclusão de cartão
@router.post("/cartoes/excluir/{id_cartao}")
@requer_autenticacao(['fornecedor'])
async def excluir_cartao(request: Request, id_cartao: int, usuario_logado: dict = None):
    fornecedor_id = usuario_logado.id
    try:
        cartao = cartao_repo.obter_cartao_por_id(id_cartao)
        if not cartao or cartao.id_fornecedor != fornecedor_id:
            return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
        resultado = cartao_repo.remover_cartao(id_cartao)
        if resultado:
            return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
        else:
            return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
                "request": request,
                "cartao": cartao,
                "mensagem": "Erro ao excluir o cartão. Tente novamente."
            })
    except Exception as e:
        return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
            "request": request,
            "cartao": cartao if 'cartao' in locals() else None,
            "mensagem": f"Erro ao processar exclusão: {str(e)}"
        })
    finally:
        pass

# Definir cartão como principal

@router.post("/cartoes/definir_principal")
@requer_autenticacao(['fornecedor'])
async def definir_cartao_principal(request: Request, usuario_logado: dict = None):
    form = await request.form()
    id_cartao = form.get("id_cartao")
    fornecedor_id = usuario_logado.id

    cartao = cartao_repo.obter_cartao_por_id(int(id_cartao))
    if not cartao or cartao.id_fornecedor != int(fornecedor_id):
        return RedirectResponse(url=f"/publico/pagamento/cartoes?id_fornecedor={fornecedor_id}", 
        status_code=303)
    cartao_repo.definir_todos_nao_principal(int(fornecedor_id))
    cartao.principal = True
    cartao_repo.atualizar_cartao(cartao)
    return RedirectResponse(url=f"/publico/pagamento/cartoes?id_fornecedor={fornecedor_id}", 
    status_code=303)
