
from fastapi import APIRouter, Request, Form
from utils.auth_decorator import requer_autenticacao
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from data.plano.plano_model import Plano
from data.plano import plano_repo
from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
from data.inscricaoplano import inscricao_plano_repo
from data.pagamento.pagamento_repo import PagamentoRepository
from data.cartao.cartao_repo import CartaoRepository
from utils.mercadopago_config import mp_config

# Criar instância dos repositórios
pagamento_repo = PagamentoRepository()
cartao_repo = CartaoRepository()
mercadopago_config = mp_config
router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Alias para compatibilidade: redireciona /fornecedor/planos/cartoes para /publico/pagamento/cartoes
@router.get("/cartoes")
@requer_autenticacao(['fornecedor'])
async def alias_cartoes(request: Request, 
                        id_fornecedor: int = None, 
                        id_prestador: int = None, 
                        id_cliente: int = None):
    url = f"/publico/pagamento/cartoes?id_fornecedor={id_fornecedor}" if id_fornecedor else "/publico/pagamento/cartoes"
    return RedirectResponse(url=url, status_code=307)

# Rota para exibir o plano atual do fornecedor
@router.get("/meu_plano")
@requer_autenticacao(['fornecedor'])
async def mostrar_meu_plano(request: Request, id_fornecedor: int = 1):
    # Aqui você pode buscar os dados do plano do fornecedor se necessário
    return templates.TemplateResponse("fornecedor/planos/minha_assinatura.html", 
                                      {"request": request, 
                                       "id_fornecedor": id_fornecedor})

# Listar planos disponíveis
@router.get("/listar")
@requer_autenticacao(['fornecedor'])
async def listar_planos(request: Request):
    planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=10)
    return templates.TemplateResponse("fornecedor/planos/listar_planos.html", 
                                      {"request": request, 
                                       "planos": planos})

# Mostrar formulário de alteração de plano
@router.get("/alterar")
@requer_autenticacao(['fornecedor'])
async def mostrar_alterar_plano(request: Request, id_fornecedor: int = 1):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    plano_atual = None
    
    if assinatura_ativa:
        plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    
    planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
    return templates.TemplateResponse("fornecedor/planos/alterar_plano.html", {
        "request": request, 
        "planos": planos, 
        "plano_atual": plano_atual, 
        "id_fornecedor": id_fornecedor
    })

# Processar alteração de plano
@router.post("/alterar")
@requer_autenticacao(['fornecedor'])
async def alterar_plano(request: Request, id_plano: int = Form(...)):
    id_fornecedor = 1  # Fixo para o fornecedor logado
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    if not assinatura_ativa:
        planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
        return templates.TemplateResponse("fornecedor/planos/alterar_plano.html", {
            "request": request, 
            "planos": planos, 
            "mensagem": "Você não possui assinatura ativa para alterar."
        })
    
    plano_novo = plano_repo.obter_plano_por_id(id_plano)
    plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    
    if plano_novo:
        # Verificar se há diferença de valor que requer pagamento
        if plano_novo.valor_mensal > plano_atual.valor_mensal:
            # Redirecionar para dados de pagamento se o novo plano é mais caro
            response = RedirectResponse(f"/publico/pagamento/formulario?plano_id={id_plano}&id_fornecedor={id_fornecedor}&tipo=alteracao", status_code=303)
            return response
        else:
            # Atualizar diretamente se o novo plano é igual ou mais barato
            assinatura_ativa.id_plano = id_plano
            inscricao_plano_repo.atualizar_inscricao_plano(assinatura_ativa)
            response = RedirectResponse("/fornecedor/planos/listar", status_code=303)
            return response
    
    planos = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
    return templates.TemplateResponse("fornecedor/planos/alterar_plano.html", {
        "request": request, 
        "planos": planos,
        "mensagem": "Erro ao alterar plano."
    })

# Mostrar confirmação de cancelamento de plano
@router.get("/cancelar")
@requer_autenticacao(['fornecedor'])
async def mostrar_cancelar_plano(request: Request, id_fornecedor: int = 1):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    plano_atual = None
    
    if assinatura_ativa:
        plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    
    return templates.TemplateResponse("fornecedor/planos/cancelar_plano.html", {
        "request": request,
        "plano_atual": plano_atual, 
        "id_fornecedor": id_fornecedor
    })

# Processar cancelamento de plano
@router.post("/cancelar")
@requer_autenticacao(['fornecedor'])
async def cancelar_plano(request: Request, id_fornecedor: int = Form(...)):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    if not assinatura_ativa:
        return templates.TemplateResponse("fornecedor/planos/cancelar_plano.html", {
            "request": request, 
            "mensagem": "Você não possui assinatura ativa para cancelar."
        })
    
    plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    return templates.TemplateResponse("fornecedor/planos/confirmacao_cancelamento_plano.html", {
        "request": request, 
        "plano_atual": plano_atual, 
        "id_fornecedor": id_fornecedor
    })

# Confirmar cancelamento de plano
@router.post("/confirmar_cancelamento")
@requer_autenticacao(['fornecedor'])
async def confirmar_cancelamento_plano(request: Request, id_fornecedor: int = Form(...)):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    if not assinatura_ativa:
        return templates.TemplateResponse("fornecedor/planos/cancelar_plano.html", {
            "request": request, 
            "mensagem": "Você não possui assinatura ativa para cancelar."
        })
    
    # Cancelar a assinatura ativa
    inscricao_plano_repo.deletar_inscricao_plano(assinatura_ativa.id_inscricao_plano)
    response = RedirectResponse("/fornecedor/planos/listar", status_code=303)
    return response

# Mostrar formulário de renovação de plano
@router.get("/renovar")
@requer_autenticacao(['fornecedor'])
async def mostrar_renovar_plano(request: Request, id_fornecedor: int = 1):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    plano_atual = None
    
    if assinatura_ativa:
        plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    
    return templates.TemplateResponse("fornecedor/planos/renovar_plano.html", {
        "request": request, 
        "plano_atual": plano_atual, 
        "id_fornecedor": id_fornecedor
    })

# Processar renovação de plano - redirecionar para dados de pagamento
@router.post("/renovar")
@requer_autenticacao(['fornecedor'])
async def renovar_plano(request: Request, id_fornecedor: int = Form(...)):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    if not assinatura_ativa:
        return templates.TemplateResponse("fornecedor/planos/renovar_plano.html", {
            "request": request, 
            "mensagem": "Você não possui assinatura ativa para renovar."
        })
    
    plano_atual = plano_repo.obter_plano_por_id(assinatura_ativa.id_plano)
    if plano_atual:
        # Redirecionar para dados de pagamento
        response = RedirectResponse(f"/publico/pagamento/formulario?plano_id={plano_atual.id_plano}&id_fornecedor={id_fornecedor}&tipo=renovacao", status_code=303)
        return response
    
    return templates.TemplateResponse("fornecedor/planos/renovar_plano.html", {
        "request": request, 
        "mensagem": "Erro ao renovar plano."
    })

# Mostrar formulário de assinatura de plano
@router.get("/assinar")
@requer_autenticacao(['fornecedor'])
async def mostrar_assinar_plano(request: Request):
    planos_disponiveis = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
    return templates.TemplateResponse("fornecedor/planos/assinar_plano.html", {
        "request": request, 
        "planos_disponiveis": planos_disponiveis
    })

# Processar assinatura de plano - redirecionar para dados de pagamento
@router.post("/assinar")
@requer_autenticacao(['fornecedor'])
async def assinar_plano(request: Request, plano_id: int = Form(...), id_fornecedor: int = Form(default=1)):
    assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
    if assinatura_ativa:
        planos_disponiveis = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
        return templates.TemplateResponse("fornecedor/planos/assinar_plano.html", {
            "request": request, 
            "planos_disponiveis": planos_disponiveis,
            "mensagem": "Você já possui uma assinatura ativa. Cancele antes de assinar outro plano."
        })
    
    plano = plano_repo.obter_plano_por_id(plano_id)
    if not plano:
        planos_disponiveis = plano_repo.obter_plano_por_pagina(pagina=1, tamanho_pagina=20)
        return templates.TemplateResponse("fornecedor/planos/assinar_plano.html", {
            "request": request,
            "planos_disponiveis": planos_disponiveis, 
            "mensagem": "Plano não encontrado"
        })
    
    # Redirecionar para dados de pagamento
    response = RedirectResponse(f"/publico/pagamento/formulario?plano_id={plano_id}&id_fornecedor={id_fornecedor}&tipo=assinatura", status_code=303)
    return response


