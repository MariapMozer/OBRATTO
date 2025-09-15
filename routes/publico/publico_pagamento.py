
# from fastapi import APIRouter, Request, Form, Response
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import RedirectResponse, JSONResponse
# from data.plano.plano_model import Plano
# from data.plano import plano_repo
# from data.inscricaoplano.inscricao_plano_model import InscricaoPlano
# from data.inscricaoplano import inscricao_plano_repo
# from data.pagamento.pagamento_model import Pagamento
# from data.pagamento.pagamento_repo import PagamentoRepository
# from data.cartao.cartao_model import CartaoCredito
# from data.cartao.cartao_repo import CartaoRepository
# from utils.mercadopago_config import mp_config

# pagamento_repo = PagamentoRepository()
# cartao_repo = CartaoRepository()
# mercadopago_config = mp_config
# router = APIRouter()
# templates = Jinja2Templates(directory="templates")

# # Alias para compatibilidade: redireciona /fornecedor/planos/cartoes para /publico/pagamento/cartoes
# @router.get("/fornecedor/planos/cartoes")
# async def alias_cartoes(request: Request, id_fornecedor: int = None, id_prestador: int = None, id_cliente: int = None):
#     # Redireciona para rota oficial
#     url = f"/publico/pagamento/cartoes?id_fornecedor={id_fornecedor}" if id_fornecedor else "/publico/pagamento/cartoes"
#     return RedirectResponse(url=url, status_code=307)

# @router.get("/formulario")
# async def mostrar_formulario_pagamento(
#     request: Request,
#     plano_id: int = None,
#     id_fornecedor: int = None,
#     id_prestador: int = None,
#     id_cliente: int = None,
#     tipo_pagamento: str = "plano"
# ):
#     # Detecta tipo de usuário pelo ID informado
#     if id_fornecedor is not None:
#         plano = plano_repo.obter_plano_por_id(plano_id)
#         cartoes = cartao_repo.obter_cartoes_fornecedor(id_fornecedor)
#         return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#             "request": request,
#             "plano": plano,
#             "id_fornecedor": id_fornecedor,
#             "tipo_operacao": "Nova Assinatura",
#             "cartoes": cartoes
#         })
#     elif id_prestador is not None:
#         # Futuro: lógica para prestador
#         plano = None  # TODO: buscar plano do prestador
#         cartoes = None  # TODO: buscar cartões do prestador
#         return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#             "request": request,
#             "plano": plano,
#             "id_prestador": id_prestador,
#             "tipo_operacao": "Nova Assinatura",
#             "cartoes": cartoes
#         })
#     elif id_cliente is not None:
#         # Futuro: lógica para cliente
#         servico = None  # TODO: buscar serviço do prestador
#         return templates.TemplateResponse("publico/pagamento/dados_pagamento_cliente.html", {
#             "request": request,
#             "servico": servico,
#             "id_cliente": id_cliente
#         })
#     # Se não for nenhum dos casos acima
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário ou pagamento não suportado."
#     })

# # Processar pagamento
# @router.post("/processar_pagamento")
# async def processar_pagamento(
#     request: Request,
#     tipo_usuario: str = Form(...),
#     tipo_operacao: str = Form(...),
#     plano_id: int = Form(None),
#     id_fornecedor: int = Form(None),
#     id_prestador: int = Form(None),
#     id_cliente: int = Form(None),
#     valor: float = Form(...),
#     metodo_pagamento: str = Form(...),
#     cartao_salvo: str = Form(default=""),
#     numero_cartao: str = Form(default=""),
#     validade: str = Form(default=""),
#     cvv: str = Form(default=""),
#     nome_cartao: str = Form(default=""),
#     salvar_cartao: str = Form(default="")
# ):
#     if tipo_usuario == "fornecedor":
#         # Processar pagamento de plano para fornecedor
#         plano = plano_repo.obter_plano_por_id(plano_id)
#         if not plano:
#             cartoes = cartao_repo.obter_cartoes_fornecedor(id_fornecedor)
#             return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#                 "request": request, "mensagem": "Plano não encontrado.", "cartoes": cartoes
#             })
#         # O restante do código só executa se o plano existir
#         cartoes = cartao_repo.obter_cartoes_fornecedor(id_fornecedor)
#         cartao_usado = None
#         if cartao_salvo:
#             try:
#                 cartao_usado = cartao_repo.obter_cartao_por_id(int(cartao_salvo))
#                 if not cartao_usado or cartao_usado.id_fornecedor != id_fornecedor:
#                     return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#                         "request": request, "plano": plano, "id_fornecedor": id_fornecedor,
#                         "tipo_operacao": tipo_operacao, "cartoes": cartoes,
#                         "mensagem": "Cartão selecionado não é válido."
#                     })
#             except ValueError:
#                 return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#                     "request": request, "plano": plano, "id_fornecedor": id_fornecedor,
#                     "tipo_operacao": tipo_operacao, "cartoes": cartoes,
#                     "mensagem": "Cartão selecionado não é válido."
#                 })
#         else:
#             if metodo_pagamento == "cartao":
#                 if not numero_cartao or not validade or not cvv or not nome_cartao:
#                     return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#                         "request": request, "plano": plano, "id_fornecedor": id_fornecedor,
#                         "tipo_operacao": tipo_operacao, "cartoes": cartoes,
#                         "mensagem": "Todos os campos do cartão são obrigatórios."
#                     })
#                 if salvar_cartao == "true":
#                     try:
#                         mes_vencimento, ano_vencimento = validade.split('/')
#                         cartao_repo.criar_cartao_from_form(
#                             id_fornecedor=id_fornecedor,
#                             numero_cartao=numero_cartao.replace(' ', ''),
#                             nome_titular=nome_cartao,
#                             mes_vencimento=mes_vencimento,
#                             ano_vencimento=ano_vencimento,
#                             apelido=f"Cartão •••• {numero_cartao.replace(' ', '')[-4:]}",
#                             principal=False
#                         )
#                     except Exception as e:
#                         print(f"Erro ao salvar cartão: {e}")
#         from datetime import datetime
#         assinatura_ativa = inscricao_plano_repo.obter_assinatura_ativa_por_fornecedor(id_fornecedor)
#         if assinatura_ativa:
#             return templates.TemplateResponse("publico/pagamento/dados_pagamento.html", {
#                 "request": request, "plano": plano, "id_fornecedor": id_fornecedor,
#                 "tipo_operacao": tipo_operacao, "mensagem": "Você já possui uma assinatura ativa."
#             })
#         nova_inscricao = InscricaoPlano(
#             id_inscricao_plano=0,
#             id_fornecedor=id_fornecedor,
#             id_prestador=None,
#             id_plano=plano_id
#         )
#         inscricao_id = inscricao_plano_repo.inserir_inscricao_plano(nova_inscricao)
#         reference = f"assinatura_plano_{plano_id}_fornecedor_{id_fornecedor}"
#         pagamento = Pagamento(
#             id_pagamento=0,
#             plano_id=plano_id,
#             fornecedor_id=id_fornecedor,
#             mp_payment_id=f"{metodo_pagamento}_payment_{inscricao_id}_{int(datetime.now().timestamp())}",
#             mp_preference_id=f"{metodo_pagamento}_pref_{inscricao_id}_{int(datetime.now().timestamp())}",
#             valor=valor,
#             status="aprovado",
#             metodo_pagamento=f"{metodo_pagamento}_simulado",
#             data_criacao=datetime.now().isoformat(),
#             data_aprovacao=datetime.now().isoformat(),
#             external_reference=reference
#         )
#         pagamento_inserido = pagamento_repo.inserir_pagamento(pagamento)
#         if pagamento_inserido:
#             return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
#                 "request": request,
#                 "plano": plano,
#                 "tipo_operacao": tipo_operacao,
#                 "metodo_pagamento": metodo_pagamento,
#                 "mensagem": f"{tipo_operacao} processada com sucesso! Pagamento via {metodo_pagamento.upper()} aprovado."
#             })
#     # Comentado para futura implementação do prestador
#     # if tipo_usuario == "prestador":
#     #     # Processar pagamento de plano para prestador
#     #     # TODO: lógica de pagamento prestador
#     #     return templates.TemplateResponse("prestador/planos e pagamentos/pagamento_sucesso.html", {
#     #         "request": request,
#     #         "mensagem": "Pagamento de plano do prestador processado com sucesso!"
#     #     })
#     # Para cliente (contratação de serviço de prestador)
#     # if tipo_usuario == "cliente":
#     #     # TODO: lógica de contratação de serviço
#     #     return templates.TemplateResponse("cliente/pagamento/pagamento_sucesso.html", {
#     #         "request": request,
#     #         "mensagem": "Pagamento do serviço processado com sucesso!"
#     #     })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "tipo_operacao": tipo_operacao,
#         "mensagem": "Tipo de usuário ou operação não suportada."
#     })

# # Callback de sucesso do Mercado Pago
# @router.get("/sucesso")
# async def pagamento_sucesso(request: Request, payment_id: str = None, status: str = None, external_reference: str = None):
#     if payment_id:
#         payment_info = mp_config.get_payment_info(payment_id)
#         if payment_info.get("status") == "approved":
#             pagamento_repo.atualizar_status_pagamento(
#                 mp_payment_id=payment_id,
#                 status="aprovado",
#                 metodo_pagamento=payment_info.get("payment_method_id")
#             )
#             return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
#                 "request": request, "payment_info": payment_info, "mensagem": "Pagamento aprovado com sucesso! Seu plano está ativo."
#             })
#     return templates.TemplateResponse("publico/pagamento/pagamento_sucesso.html", {
#         "request": request, "mensagem": "Pagamento processado com sucesso!"
#     })

# # Callback de falha do Mercado Pago
# @router.get("/falha")
# async def pagamento_falha(request: Request):
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request, "mensagem": "Pagamento rejeitado ou cancelado. Tente novamente."
#     })

# # Callback de pagamento pendente
# @router.get("/pendente")
# async def pagamento_pendente(request: Request):
#     return templates.TemplateResponse("publico/pagamento/pagamento_pendente.html", {
#         "request": request, "mensagem": "Pagamento pendente de aprovação. Aguarde a confirmação."
#     })


# # ===== ROTAS DE GERENCIAMENTO DE CARTÕES =====


# # Exemplo de função para buscar id do usuário logado (pode ser adaptada para seu sistema de autenticação)
# def get_current_user_id(request):
#     # Tente buscar de sessão
#     id_fornecedor = request.session.get("id_fornecedor")
#     id_prestador = request.session.get("id_prestador")
#     id_cliente = request.session.get("id_cliente")
#     # Tente buscar de contexto global, cookies, headers, etc (adapte conforme seu sistema)
#     # Exemplo: id_fornecedor = request.cookies.get("id_fornecedor")
#     # Se não encontrar, retorna None
#     return id_fornecedor, id_prestador, id_cliente

# @router.get("/cartoes")
# async def listar_cartoes(request: Request, id_fornecedor: int = None, id_prestador: int = None, id_cliente: int = None):
#     # Tenta identificar o usuário pela URL, sessão ou contexto global
#     id_fornecedor = id_fornecedor or request.session.get("id_fornecedor")
#     id_prestador = id_prestador or request.session.get("id_prestador")
#     id_cliente = id_cliente or request.session.get("id_cliente")
#     # Se ainda não encontrou, tenta buscar pelo contexto global
#     if not (id_fornecedor or id_prestador or id_cliente):
#         id_fornecedor, id_prestador, id_cliente = get_current_user_id(request)

#     if id_fornecedor:
#         cartoes = cartao_repo.obter_cartoes_fornecedor(id_fornecedor)
#         return templates.TemplateResponse("publico/pagamento/meus_cartoes.html", {
#             "request": request,
#             "cartoes": cartoes,
#             "id_fornecedor": id_fornecedor
#         })
#     elif id_prestador:
#         cartoes = cartao_repo.obter_cartoes_prestador(id_prestador)
#         return templates.TemplateResponse("publico/pagamento/meus_cartoes.html", {
#             "request": request,
#             "cartoes": cartoes,
#             "id_prestador": id_prestador
#         })
#     elif id_cliente:
#         cartoes = cartao_repo.obter_cartoes_cliente(id_cliente)
#         return templates.TemplateResponse("publico/pagamento/meus_cartoes.html", {
#             "request": request,
#             "cartoes": cartoes,
#             "id_cliente": id_cliente
#         })
#     else:
#         # Nenhum usuário identificado
#         return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#             "request": request,
#             "mensagem": "Usuário não identificado. Faça login para visualizar seus cartões."
#         })

# # Mostrar formulário para adicionar cartão
# @router.get("/cartoes/adicionar")
# async def mostrar_adicionar_cartao(request: Request, tipo_usuario: str, id_fornecedor: int = None, id_prestador: int = None, id_cliente: int = None):
#     if tipo_usuario == "fornecedor":
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "id_fornecedor": id_fornecedor
#         })
#     # Comentado para futura implementação do prestador
#     # if tipo_usuario == "prestador":
#     #     return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#     #         "request": request,
#     #         "id_prestador": id_prestador
#     #     })
#     # Para cliente
#     # if tipo_usuario == "cliente":
#     #     return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#     #         "request": request,
#     #         "id_cliente": id_cliente
#     #     })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Processar adição de cartão
# @router.post("/cartoes/adicionar")
# async def adicionar_cartao(
#     request: Request,
#     tipo_usuario: str = Form(...),
#     id_fornecedor: int = Form(None),
#     id_prestador: int = Form(None),
#     id_cliente: int = Form(None),
#     numero_cartao: str = Form(...),
#     nome_titular: str = Form(...),
#     mes_vencimento: str = Form(...),
#     ano_vencimento: str = Form(...),
#     apelido: str = Form(...),
#     principal: str = Form(None)
# ):
#     try:
#         if tipo_usuario == "fornecedor":
#             resultado = cartao_repo.criar_cartao_from_form(
#                 id_fornecedor=id_fornecedor,
#                 numero_cartao=numero_cartao,
#                 nome_titular=nome_titular,
#                 mes_vencimento=mes_vencimento,
#                 ano_vencimento=ano_vencimento,
#                 apelido=apelido,
#                 principal=(principal == "true")
#             )
#             if resultado:
#                 return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#             else:
#                 return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#                     "request": request,
#                     "id_fornecedor": id_fornecedor,
#                     "mensagem": "Erro ao salvar o cartão. Tente novamente."
#                 })
#         # Comentado para futura implementação do prestador
#         # if tipo_usuario == "prestador":
#         #     resultado = cartao_repo.criar_cartao_from_form_prestador(...)
#         #     ...
#         # if tipo_usuario == "cliente":
#         #     resultado = cartao_repo.criar_cartao_from_form_cliente(...)
#         #     ...
#     except Exception as e:
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "id_fornecedor": id_fornecedor,
#             "mensagem": f"Erro ao processar cartão: {str(e)}"
#         })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Mostrar formulário para editar cartão

# @router.get("/cartoes/editar/{id_cartao}")
# async def mostrar_editar_cartao(request: Request, id_cartao: int, id_fornecedor: int = None, id_prestador: int = None, id_cliente: int = None):
#     # Detecta tipo de usuário pelo id recebido
#     if id_fornecedor is not None:
#         cartao = cartao_repo.obter_cartao_por_id(id_cartao)
#         if not cartao or cartao.id_fornecedor != id_fornecedor:
#             return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "cartao": cartao,
#             "id_fornecedor": id_fornecedor
#         })
#     elif id_prestador is not None:
#         # Futuro: lógica para prestador
#         cartao = None  # TODO: buscar cartão do prestador
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "cartao": cartao,
#             "id_prestador": id_prestador
#         })
#     elif id_cliente is not None:
#         # Futuro: lógica para cliente
#         cartao = None  # TODO: buscar cartão do cliente
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "cartao": cartao,
#             "id_cliente": id_cliente
#         })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Processar edição de cartão
# @router.post("/cartoes/editar/{id_cartao}")
# async def editar_cartao(
#     request: Request,
#     id_cartao: int,
#     tipo_usuario: str = Form(...),
#     id_fornecedor: int = Form(None),
#     id_prestador: int = Form(None),
#     id_cliente: int = Form(None),
#     nome_titular: str = Form(...),
#     apelido: str = Form(...),
#     principal: str = Form(None)
# ):
#     try:
#         if tipo_usuario == "fornecedor":
#             cartao = cartao_repo.obter_cartao_por_id(id_cartao)
#             if not cartao or cartao.id_fornecedor != id_fornecedor:
#                 return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#             cartao.nome_titular = nome_titular.strip().upper()
#             cartao.apelido = apelido.strip()
#             cartao.principal = (principal == "true")
#             resultado = cartao_repo.atualizar_cartao(cartao)
#             if resultado:
#                 return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#             else:
#                 return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#                     "request": request,
#                     "cartao": cartao,
#                     "id_fornecedor": id_fornecedor,
#                     "mensagem": "Erro ao atualizar o cartão. Tente novamente."
#                 })
#         # Comentado para futura implementação do prestador
#         # if tipo_usuario == "prestador":
#         #     ...
#         # if tipo_usuario == "cliente":
#         #     ...
#     except Exception as e:
#         return templates.TemplateResponse("publico/pagamento/adicionar_cartao.html", {
#             "request": request,
#             "cartao": cartao if 'cartao' in locals() else None,
#             "id_fornecedor": id_fornecedor,
#             "mensagem": f"Erro ao processar alterações: {str(e)}"
#         })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Mostrar confirmação de exclusão
# @router.get("/cartoes/excluir/{id_cartao}")
# async def mostrar_confirmar_exclusao(request: Request, id_cartao: int, tipo_usuario: str, id_fornecedor: int = None, id_prestador: int = None, id_cliente: int = None):
#     if tipo_usuario == "fornecedor":
#         cartao = cartao_repo.obter_cartao_por_id(id_cartao)
#         if not cartao or cartao.id_fornecedor != id_fornecedor:
#             return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#         return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
#             "request": request,
#             "cartao": cartao
#         })
#     # Comentado para futura implementação do prestador
#     # if tipo_usuario == "prestador":
#     #     ...
#     # if tipo_usuario == "cliente":
#     #     ...
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Processar exclusão de cartão
# @router.post("/cartoes/excluir/{id_cartao}")
# async def excluir_cartao(request: Request, id_cartao: int, tipo_usuario: str = Form(...), id_fornecedor: int = Form(None), id_prestador: int = Form(None), id_cliente: int = Form(None)):
#     try:
#         if tipo_usuario == "fornecedor":
#             cartao = cartao_repo.obter_cartao_por_id(id_cartao)
#             if not cartao or cartao.id_fornecedor != id_fornecedor:
#                 return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#             resultado = cartao_repo.remover_cartao(id_cartao)
#             if resultado:
#                 return RedirectResponse(url="/publico/pagamento/cartoes", status_code=303)
#             else:
#                 return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
#                     "request": request,
#                     "cartao": cartao,
#                     "mensagem": "Erro ao excluir o cartão. Tente novamente."
#                 })
#         # Comentado para futura implementação do prestador
#         # if tipo_usuario == "prestador":
#         #     ...
#         # if tipo_usuario == "cliente":
#         #     ...
#     except Exception as e:
#         return templates.TemplateResponse("publico/pagamento/confirmar_exclusao_cartao.html", {
#             "request": request,
#             "cartao": cartao if 'cartao' in locals() else None,
#             "mensagem": f"Erro ao processar exclusão: {str(e)}"
#         })
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })

# # Definir cartão como principal



# @router.post("/cartoes/definir_principal")
# async def definir_cartao_principal(request: Request):
#     form = await request.form()
#     id_cartao = form.get("id_cartao")
#     id_fornecedor = form.get("id_fornecedor") or request.session.get("id_fornecedor")
#     id_prestador = form.get("id_prestador") or request.session.get("id_prestador")
#     id_cliente = form.get("id_cliente") or request.session.get("id_cliente")

#     if id_fornecedor:
#         cartao = cartao_repo.obter_cartao_por_id(int(id_cartao))
#         if not cartao or cartao.id_fornecedor != int(id_fornecedor):
#             return RedirectResponse(url="/publico/pagamento/cartoes?id_fornecedor={}".format(id_fornecedor), status_code=303)
#         cartao_repo.definir_todos_nao_principal(int(id_fornecedor))
#         cartao.principal = True
#         cartao_repo.atualizar_cartao(cartao)
#         return RedirectResponse(url="/publico/pagamento/cartoes?id_fornecedor={}".format(id_fornecedor), status_code=303)
#     elif id_prestador:
#         # Futuro: lógica para prestador
#         return RedirectResponse(url="/publico/pagamento/cartoes?id_prestador={}".format(id_prestador), status_code=303)
#     elif id_cliente:
#         # Futuro: lógica para cliente
#         return RedirectResponse(url="/publico/pagamento/cartoes?id_cliente={}".format(id_cliente), status_code=303)
#     return templates.TemplateResponse("publico/pagamento/pagamento_erro.html", {
#         "request": request,
#         "mensagem": "Tipo de usuário não suportado."
#     })
