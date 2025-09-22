from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from data.fornecedor import fornecedor_repo
from data.fornecedor import fornecedor_sql
from data.fornecedor.fornecedor_model import Fornecedor
from data.prestador import prestador_repo
from data.prestador.prestador_model import Prestador
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.mensagem.mensagem_model import Mensagem
from data.mensagem import mensagem_repo
# from utils.security import verificar_autenticacao
import os
import uuid

from utils.security import criar_hash_senha, gerar_token_redefinicao, verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("publico/home.html", {"request": request})


@router.get("/escolha_cadastro")
async def mostrar_escolha_cadastro(request: Request):
    return templates.TemplateResponse("publico/login_cadastro/escolha_cadastro.html", {"request": request})

#--------------CADASTRO-----------------------------

# Cadastro do prestador
@router.get("/cadastro/prestador")
async def exibir_cadastro_prestador(request: Request):
    return templates.TemplateResponse("publico/prestador/prestador_cadastro.html", {"request": request})

# Rota para processar o formulário de cadastro
@router.post("/cadastro/prestador")
async def processar_cadastro_prestador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None)
):

    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "publico/prestador/prestador_cadastro.html",
            {"request": request, "erro": "As senhas não coincidem."}
        )
    # Verificar se email já existe
    if prestador_repo.obter_prestador_por_email(email):
        return templates.TemplateResponse(
            "publico/prestador/prestador_cadastro.html",
            {"request": request, "erro": "Email já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)
    
    prestador = Prestador(
        id=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        cpf_cnpj=cpf_cnpj,
        telefone=telefone,
        estado=estado,
        cidade=cidade,
        rua=rua,
        numero=numero,
        bairro=bairro,
        tipo_usuario="Prestador",
        data_cadastro=datetime.now(), 
        foto=None,        
        token_redefinicao=None,
        data_token=None,
        area_atuacao=area_atuacao,
        razao_social=razao_social,
        descricao_servicos=descricao_servicos
    )
    prestador_id = prestador_repo.inserir_prestador(prestador)
    if prestador_id:
        return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/cadastro/prestador")


# Rota para cadastro de cliente
@router.get("/cadastro/cliente")
async def get_page(request: Request):
    return templates.TemplateResponse("publico/login_cadastro/cadastro.html", {"request": request})


# Rota para processar o formulário de cadastro
@router.post("/cadastro/cliente")
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    foto: str = Form(None),
    genero: str = Form(...),
    data_nascimento: str = Form(...)):


    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "publico/cliente/cadastro_cliente.html",
            {"request": request, "erro": "As senhas não coincidem."}
        )
    # Verificar se email já existe
    if cliente_repo.obter_cliente_por_email(email):
        return templates.TemplateResponse(
            "publico/cliente/cadastro_cliente.html",
            {"request": request, "erro": "Email já cadastrado"}
        )

    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)
    
    cliente = Cliente(
        id=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        cpf_cnpj=cpf_cnpj,
        telefone=telefone,
        estado=estado,
        cidade=cidade,
        rua=rua,
        numero=numero,
        bairro=bairro,
        tipo_usuario="Cliente",
        data_cadastro=None, 
        foto=foto,
        token_redefinicao=None,
        data_token=None,
        genero=genero,
        data_nascimento=data_nascimento
    )

    cliente_id = cliente_repo.inserir_cliente(cliente)
    if cliente_id:
        return RedirectResponse("/login", status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/cadastro/cliente")


# Rota para cadastro de fornecedor
@router.get("/cadastro/fornecedor")
async def exibir_cadastro_fornecedor(request: Request):
    return templates.TemplateResponse("publico/fornecedor2/cadastro_fornecedor.html", {"request": request})

# Cadastro de fornecedor (POST)

@router.post("/cadastro/fornecedor")
async def processar_cadastro_fornecedor(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    razao_social: Optional[str] = Form(None)
   
):

    if senha != confirmar_senha:
        return templates.TemplateResponse(
            "publico/fornecedor2/cadastro_fornecedor.html",
            {"request": request, "erro": "As senhas não coincidem."}
        )
    # Verificar se email já existe
    if fornecedor_repo.obter_fornecedor_por_email(email):
        return templates.TemplateResponse(
            "publico/fornecedor2/cadastro_fornecedor.html",
            {"request": request, "erro": "Email já cadastrado"}
        )
    
    # Criar hash da senha
    senha_hash = criar_hash_senha(senha)
    

    # Garante que razao_social nunca seja None ou string vazia
    razao_social_final = razao_social if razao_social and razao_social.strip() else nome

    fornecedor = Fornecedor(
        id=0,
        nome=nome,
        email=email,
        senha=senha_hash,
        cpf_cnpj=cpf_cnpj,
        telefone=telefone,
        estado=estado,
        cidade=cidade,
        rua=rua,
        numero=numero,
        bairro=bairro,
        tipo_usuario="Fornecedor",
        data_cadastro=datetime.now(), 
        foto=None,        
        token_redefinicao=None,
        data_token=None,
        razao_social=razao_social_final,
    )

    fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)
    if not fornecedor_id:
        return templates.TemplateResponse(
            "publico/fornecedor2/cadastro_fornecedor.html",
            {"request": request, "erro": "Erro ao cadastrar fornecedor."}
        )

       
    
   
#---------------------------------------------------------------------

#--------------LOGIN/LOGOUT-----------------------------

@router.get("/login")
async def mostrar_login(request: Request):
    return templates.TemplateResponse("publico/login_cadastro/login.html", {"request": request})

@router.post("/login")
async def processar_login(request: Request, email: str = Form(...), senha: str = Form(...)):
    if not email or not senha:
        return templates.TemplateResponse("publico/login_cadastro/login.html", {"request": request, "erro": "Preencha todos os campos."}, status_code=status.HTTP_400_BAD_REQUEST)

    usuario = usuario_repo.obter_usuario_por_email(email)
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse("publico/login_cadastro/login.html", {"request": request, "erro": "Email ou senha inválidos"}, status_code=status.HTTP_401_UNAUTHORIZED)

    # Cria sessão completa
    usuario_dict = {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": getattr(usuario, "perfil", getattr(usuario, "tipo_usuario", "cliente")),
        "foto": getattr(usuario, "foto", None)
    }
    request.session["usuario"] = usuario_dict

    # Redireciona conforme perfil
    perfil = usuario_dict["perfil"].lower()
    if perfil == "admin" or perfil == "administrador":
        return RedirectResponse("/admin", status_code=status.HTTP_303_SEE_OTHER)
    elif perfil == "fornecedor":
        return RedirectResponse("/fornecedor", status_code=status.HTTP_303_SEE_OTHER)
    elif perfil == "cliente":
        return RedirectResponse("/cliente", status_code=status.HTTP_303_SEE_OTHER)
    elif perfil == "prestador":
        return RedirectResponse("/prestador", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
    

@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

#-----------------------------------------------------

#--------------RECUPERAR SENHA-----------------------------

@router.get("/recuperar-senha")
async def recuperar_senha_get(request: Request):
    return templates.TemplateResponse("publico/login_cadastro/recuperar_senha.html", {"request": request})


@router.post("/recuperar-senha")
async def recuperar_senha_post(request: Request, email: str = Form(...)):
    usuario = usuario_repo.obter_usuario_por_email(email)
    if usuario:
        # Gera token e salva no usuário
        token = gerar_token_redefinicao()
        usuario.token_redefinicao = token
        usuario_repo.atualizar_usuario(usuario)
        # Aqui você enviaria o e-mail real. Exemplo:
        link = f"http://localhost:8000/publico/resetar-senha?token={token}"
        mensagem = f"Enviamos um link de recuperação para o e-mail: {email}. (Simulação: {link})"
    else:
        mensagem = "E-mail não encontrado."
    return templates.TemplateResponse("publico/recuperar_senha.html", {"request": request, "mensagem": mensagem})


@router.get("/resetar-senha")
async def resetar_senha_get(request: Request, token: str):
    return templates.TemplateResponse("publico/login_cadastro/redefinir_senha.html", {"request": request, "token": token})

@router.post("/resetar-senha")
async def resetar_senha_post(request: Request, token: str = Form(...), nova_senha: str = Form(...)):
    usuario = usuario_repo.obter_usuario_por_token(token)
    if usuario:
        usuario.senha = criar_hash_senha(nova_senha)
        usuario.token_redefinicao = None
        usuario_repo.atualizar_usuario(usuario)
        mensagem = "Senha redefinida com sucesso! Faça login."
        return RedirectResponse("/publico/login_cadastro/login.html", status_code=303)
    else:
        mensagem = "Token inválido ou expirado."
        return templates.TemplateResponse("publico/login_cadastro/redefinir_senha.html", {"request": request, 
        "mensagem": mensagem, "token": token})

#-----------------------------------------------------

# Rota para perfil público do prestador
@router.get("/prestador/perfil_publico")
async def exibir_perfil_publico(request: Request):
    return templates.TemplateResponse("publico/prestador/perfil_publico.html", {"request": request})

# Rota para perfil público do cliente
@router.get("/cliente/perfil_publico")
async def exibir_perfil_publico(request: Request):
    return templates.TemplateResponse("publico/cliente/perfil_publico.html", {"request": request})

# Rota para perfil público do fornecedor
@router.get("/fornecedor/perfil_publico")
async def exibir_perfil_publico(request: Request):
    return templates.TemplateResponse("publico/perfil_publico_fornecedor.html", {"request": request})

#-----------------------------------------------------
#----------------- MENSAGEM --------------------------

# # ROTAS PRINCIPAIS 
# @router.get("/mensagens")
# async def exibir_caixa_mensagens(request: Request):
#     """Exibe a caixa de mensagens principal do usuário"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter todas as mensagens do usuário (enviadas e recebidas)
#     todas_mensagens = mensagem_repo.obter_mensagem()
    
#     # Filtrar mensagens do usuário atual
#     mensagens_usuario = [
#         msg for msg in todas_mensagens 
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]
    
#     # Organizar conversas por contato
#     conversas = organizar_conversas_por_contato(mensagens_usuario, usuario["id"])
    
#     # Contar mensagens não lidas
#     mensagens_nao_lidas = contar_mensagens_nao_lidas(usuario["id"])
    
#     return templates.TemplateResponse("mensagens/caixa_mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "conversas": conversas,
#         "mensagens_nao_lidas": mensagens_nao_lidas
#     })

# @router.get("/mensagens/conversa/{contato_id}")
# async def exibir_conversa(request: Request, contato_id: int):
#     """Exibe uma conversa específica entre o usuário logado e um contato"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter dados do contato
#     contato = obter_dados_usuario_por_id(contato_id)
#     if not contato:
#         return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter mensagens da conversa
#     todas_mensagens = mensagem_repo.obter_mensagem()
#     mensagens_conversa = [
#         msg for msg in todas_mensagens 
#         if (msg.id_remetente == usuario["id"] and msg.id_destinatario == contato_id) or
#            (msg.id_remetente == contato_id and msg.id_destinatario == usuario["id"])
#     ]
    
#     # Ordenar por data
#     mensagens_conversa.sort(key=lambda x: x.data_hora)
    
#     return templates.TemplateResponse("mensagens/conversa.html", {
#         "request": request,
#         "usuario": usuario,
#         "contato": contato,
#         "mensagens": mensagens_conversa
#     })

# @router.get("/mensagens/nova")
# async def exibir_nova_mensagem(request: Request):
#     """Exibe formulário para nova mensagem"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter usuários disponíveis baseado no tipo do usuário logado
#     usuarios_disponiveis = obter_usuarios_disponiveis_por_tipo(usuario["perfil"], usuario["id"])
    
#     return templates.TemplateResponse("mensagens/nova_mensagem.html", {
#         "request": request,
#         "usuario": usuario,
#         "usuarios_disponiveis": usuarios_disponiveis
#     })

# @router.post("/mensagens/enviar")
# async def processar_envio_mensagem(
#     request: Request,
#     destinatario_id: int = Form(...),
#     conteudo: str = Form(...)
# ):
#     """Processa o envio de uma nova mensagem"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     try:
#         # Validar destinatário
#         destinatario = obter_dados_usuario_por_id(destinatario_id)
#         if not destinatario:
#             raise HTTPException(status_code=400, detail="Destinatário não encontrado")
        
#         # Criar mensagem
#         mensagem = Mensagem(
#             id_mensagem=0,  # Será gerado automaticamente
#             id_remetente=usuario["id"],
#             id_destinatario=destinatario_id,
#             conteudo=conteudo,
#             data_hora=datetime.now(),
#             nome_remetente=usuario["nome"],
#             nome_destinatario=destinatario.nome
#         )
        
#         mensagem_repo.inserir_mensagem(mensagem)
        
#         return RedirectResponse(
#             f"/mensagens/conversa/{destinatario_id}", 
#             status_code=status.HTTP_303_SEE_OTHER
#         )
        
#     except Exception as e:
#         usuarios_disponiveis = obter_usuarios_disponiveis_por_tipo(usuario["perfil"], usuario["id"])
#         return templates.TemplateResponse("mensagens/nova_mensagem.html", {
#             "request": request,
#             "usuario": usuario,
#             "usuarios_disponiveis": usuarios_disponiveis,
#             "erro": f"Erro ao enviar mensagem: {str(e)}"
#         })

# @router.post("/mensagens/responder")
# async def processar_resposta_rapida(
#     request: Request,
#     contato_id: int = Form(...),
#     conteudo: str = Form(...)
# ):
#     """Processa resposta rápida em uma conversa"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     try:
#         # Obter dados do destinatário
#         destinatario = obter_dados_usuario_por_id(contato_id)
#         if not destinatario:
#             raise HTTPException(status_code=400, detail="Destinatário não encontrado")
        
#         # Criar mensagem de resposta
#         mensagem = Mensagem(
#             id_mensagem=0,
#             id_remetente=usuario["id"],
#             id_destinatario=contato_id,
#             conteudo=conteudo,
#             data_hora=datetime.now(),
#             nome_remetente=usuario["nome"],
#             nome_destinatario=destinatario.nome
#         )
        
#         mensagem_repo.inserir_mensagem(mensagem)
        
#         return RedirectResponse(
#             f"/mensagens/conversa/{contato_id}", 
#             status_code=status.HTTP_303_SEE_OTHER
#         )
        
#     except Exception as e:
#         return RedirectResponse(
#             f"/mensagens/conversa/{contato_id}", 
#             status_code=status.HTTP_303_SEE_OTHER
#         )

# #-----------------------------------------------------
# #------------- ROTAS ESPECÍFICAS POR TIPO -----------
# #-----------------------------------------------------

# @router.get("/cliente/mensagens")
# async def mensagens_cliente(request: Request):
#     """Interface de mensagens específica para clientes"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() != "cliente":
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter prestadores e fornecedores disponíveis
#     prestadores = prestador_repo.obter_todos_prestadores() if hasattr(prestador_repo, 'obter_todos_prestadores') else []
#     fornecedores = fornecedor_repo.obter_todos_fornecedores() if hasattr(fornecedor_repo, 'obter_todos_fornecedores') else []
    
#     # Obter conversas do cliente
#     todas_mensagens = mensagem_repo.obter_mensagem()
#     mensagens_cliente = [
#         msg for msg in todas_mensagens 
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]
    
#     conversas = organizar_conversas_por_contato(mensagens_cliente, usuario["id"])
    
#     return templates.TemplateResponse("mensagens/cliente_mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "prestadores": prestadores,
#         "fornecedores": fornecedores,
#         "conversas": conversas
#     })

# @router.get("/prestador/mensagens")
# async def mensagens_prestador(request: Request):
#     """Interface de mensagens específica para prestadores"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() != "prestador":
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter clientes disponíveis
#     clientes = cliente_repo.obter_todos_clientes() if hasattr(cliente_repo, 'obter_todos_clientes') else []
    
#     # Obter conversas do prestador
#     todas_mensagens = mensagem_repo.obter_mensagem()
#     mensagens_prestador = [
#         msg for msg in todas_mensagens 
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]
    
#     conversas = organizar_conversas_por_contato(mensagens_prestador, usuario["id"])
    
#     return templates.TemplateResponse("mensagens/prestador_mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "clientes": clientes,
#         "conversas": conversas
#     })

# @router.get("/fornecedor/mensagens")
# async def mensagens_fornecedor(request: Request):
#     """Interface de mensagens específica para fornecedores"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() != "fornecedor":
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter clientes disponíveis
#     clientes = cliente_repo.obter_todos_clientes() if hasattr(cliente_repo, 'obter_todos_clientes') else []
    
#     # Obter conversas do fornecedor
#     todas_mensagens = mensagem_repo.obter_mensagem()
#     mensagens_fornecedor = [
#         msg for msg in todas_mensagens 
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]
    
#     conversas = organizar_conversas_por_contato(mensagens_fornecedor, usuario["id"])
    
#     return templates.TemplateResponse("mensagens/fornecedor_mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "clientes": clientes,
#         "conversas": conversas
#     })

# @router.get("/admin/mensagens")
# async def mensagens_admin(request: Request):
#     """Interface de mensagens para administradores"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() not in ["admin", "administrador"]:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     # Obter estatísticas
#     try:
#         total_clientes = len(cliente_repo.obter_todos_clientes()) if hasattr(cliente_repo, 'obter_todos_clientes') else 0
#         total_prestadores = len(prestador_repo.obter_todos_prestadores()) if hasattr(prestador_repo, 'obter_todos_prestadores') else 0
#         total_fornecedores = len(fornecedor_repo.obter_todos_fornecedores()) if hasattr(fornecedor_repo, 'obter_todos_fornecedores') else 0
#     except:
#         total_clientes = total_prestadores = total_fornecedores = 0
    
#     # Obter todas as conversas do admin
#     todas_mensagens = mensagem_repo.obter_mensagem()
#     mensagens_admin = [
#         msg for msg in todas_mensagens 
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]
    
#     conversas = organizar_conversas_por_contato(mensagens_admin, usuario["id"])
    
#     return templates.TemplateResponse("mensagens/admin_mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "total_clientes": total_clientes,
#         "total_prestadores": total_prestadores,
#         "total_fornecedores": total_fornecedores,
#         "conversas": conversas
#     })

# @router.get("/admin/mensagens/broadcast")
# async def exibir_broadcast(request: Request):
#     """Interface para envio de mensagens em massa"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() not in ["admin", "administrador"]:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     return templates.TemplateResponse("mensagens/admin_broadcast.html", {
#         "request": request,
#         "usuario": usuario
#     })

# @router.post("/admin/mensagens/broadcast")
# async def processar_broadcast(
#     request: Request,
#     tipo_destinatarios: str = Form(...),
#     conteudo: str = Form(...)
# ):
#     """Processa envio de mensagem em massa"""
#     usuario = verificar_autenticacao(request)
#     if not usuario or usuario["perfil"].lower() not in ["admin", "administrador"]:
#         return RedirectResponse("/entrar", status_code=status.HTTP_303_SEE_OTHER)
    
#     try:
#         destinatarios = []
        
#         # Determinar destinatários baseado na seleção
#         if tipo_destinatarios in ["todos", "clientes"]:
#             try:
#                 clientes = cliente_repo.obter_todos_clientes() if hasattr(cliente_repo, 'obter_todos_clientes') else []
#                 destinatarios.extend(clientes)
#             except:
#                 pass
        
#         if tipo_destinatarios in ["todos", "prestadores"]:
#             try:
#                 prestadores = prestador_repo.obter_todos_prestadores() if hasattr(prestador_repo, 'obter_todos_prestadores') else []
#                 destinatarios.extend(prestadores)
#             except:
#                 pass
        
#         if tipo_destinatarios in ["todos", "fornecedores"]:
#             try:
#                 fornecedores = fornecedor_repo.obter_todos_fornecedores() if hasattr(fornecedor_repo, 'obter_todos_fornecedores') else []
#                 destinatarios.extend(fornecedores)
#             except:
#                 pass
        
#         # Enviar mensagem para todos os destinatários
#         mensagens_enviadas = 0
#         for destinatario in destinatarios:
#             try:
#                 mensagem = Mensagem(
#                     id_mensagem=0,
#                     id_remetente=usuario["id"],
#                     id_destinatario=destinatario.id,
#                     conteudo=conteudo,
#                     data_hora=datetime.now(),
#                     nome_remetente=usuario["nome"],
#                     nome_destinatario=destinatario.nome
#                 )
#                 mensagem_repo.inserir_mensagem(mensagem)
#                 mensagens_enviadas += 1
#             except Exception as e:
#                 print(f"Erro ao enviar mensagem para {destinatario.nome}: {e}")
#                 continue
        
#         return templates.TemplateResponse("mensagens/admin_broadcast.html", {
#             "request": request,
#             "usuario": usuario,
#             "sucesso": f"Mensagem enviada para {mensagens_enviadas} usuários"
#         })
        
#     except Exception as e:
#         return templates.TemplateResponse("mensagens/admin_broadcast.html", {
#             "request": request,
#             "usuario": usuario,
#             "erro": f"Erro ao enviar mensagens: {str(e)}"
#         })

# #-----------------------------------------------------
# #----------------- ROTAS API/AJAX -------------------
# #-----------------------------------------------------

# @router.get("/api/mensagens/nao-lidas")
# async def contar_nao_lidas(request: Request):
#     """API para contar mensagens não lidas"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return JSONResponse({"erro": "Não autenticado"}, status_code=401)
    
#     try:
#         count = contar_mensagens_nao_lidas(usuario["id"])
#         return JSONResponse({"count": count})
#     except Exception as e:
#         return JSONResponse({"erro": str(e)}, status_code=500)

# @router.delete("/api/mensagens/{mensagem_id}")
# async def excluir_mensagem_api(request: Request, mensagem_id: int):
#     """API para excluir mensagem"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return JSONResponse({"erro": "Não autenticado"}, status_code=401)
    
#     try:
#         mensagem = mensagem_repo.obter_mensagem_por_id(mensagem_id)
#         if not mensagem:
#             return JSONResponse({"erro": "Mensagem não encontrada"}, status_code=404)
        
#         # Verificar permissão
#         if mensagem.id_remetente != usuario["id"] and mensagem.id_destinatario != usuario["id"]:
#             return JSONResponse({"erro": "Sem permissão"}, status_code=403)
        
#         mensagem_repo.deletar_mensagem(mensagem_id)
#         return JSONResponse({"sucesso": True})
#     except Exception as e:
#         return JSONResponse({"erro": str(e)}, status_code=500)

# @router.get("/api/mensagens/buscar")
# async def buscar_mensagens_api(request: Request, termo: str = ""):
#     """API para buscar mensagens"""
#     usuario = verificar_autenticacao(request)
#     if not usuario:
#         return JSONResponse({"erro": "Não autenticado"}, status_code=401)
    
#     try:
#         todas_mensagens = mensagem_repo.obter_mensagem()
        
#         # Filtrar mensagens do usuário que contenham o termo
#         mensagens_filtradas = [
#             msg for msg in todas_mensagens 
#             if (msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]) and
#                termo.lower() in msg.conteudo.lower()
#         ]
        
#         # Converter para formato JSON
#         mensagens_json = []
#         for msg in mensagens_filtradas:
#             mensagens_json.append({
#                 "id": msg.id_mensagem,
#                 "conteudo": msg.conteudo[:100] + "..." if len(msg.conteudo) > 100 else msg.conteudo,
#                 "data_hora": msg.data_hora.isoformat() if isinstance(msg.data_hora, datetime) else str(msg.data_hora),
#                 "nome_remetente": msg.nome_remetente,
#                 "nome_destinatario": msg.nome_destinatario
#             })
        
#         return JSONResponse({"mensagens": mensagens_json})
#     except Exception as e:
#         return JSONResponse({"erro": str(e)}, status_code=500)

# #-----------------------------------------------------
# #------------- FUNÇÕES AUXILIARES -------------------
# #-----------------------------------------------------

# def obter_dados_usuario_por_id(usuario_id: int):
#     """Obtém dados de um usuário por ID, buscando em todas as tabelas"""
#     # Tentar buscar em clientes
#     try:
#         if hasattr(cliente_repo, 'obter_cliente_por_id'):
#             cliente = cliente_repo.obter_cliente_por_id(usuario_id)
#             if cliente:
#                 return cliente
#     except:
#         pass
    
#     # Tentar buscar em prestadores
#     try:
#         if hasattr(prestador_repo, 'obter_prestador_por_id'):
#             prestador = prestador_repo.obter_prestador_por_id(usuario_id)
#             if prestador:
#                 return prestador
#     except:
#         pass
    
#     # Tentar buscar em fornecedores
#     try:
#         if hasattr(fornecedor_repo, 'obter_fornecedor_por_id'):
#             fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_id)
#             if fornecedor:
#                 return fornecedor
#     except:
#         pass
    
#     # Tentar buscar na tabela geral de usuários
#     try:
#         if hasattr(usuario_repo, 'obter_usuario_por_id'):
#             usuario = usuario_repo.obter_usuario_por_id(usuario_id)
#             if usuario:
#                 return usuario
#     except:
#         pass
    
#     return None

# def obter_usuarios_disponiveis_por_tipo(tipo_usuario: str, usuario_id: int) -> List[dict]:
#     """Obtém usuários disponíveis baseado no tipo do usuário logado"""
#     usuarios = []
    
#     if tipo_usuario.lower() == "cliente":
#         # Clientes podem enviar para prestadores e fornecedores
#         try:
#             if hasattr(prestador_repo, 'obter_todos_prestadores'):
#                 prestadores = prestador_repo.obter_todos_prestadores()
#                 for p in prestadores:
#                     if p.id != usuario_id:
#                         usuarios.append({
#                             "id": p.id,
#                             "nome": p.nome,
#                             "tipo": "prestador",
#                             "email": getattr(p, 'email', ''),
#                             "area_atuacao": getattr(p, 'area_atuacao', '')
#                         })
#         except:
#             pass
        
#         try:
#             if hasattr(fornecedor_repo, 'obter_todos_fornecedores'):
#                 fornecedores = fornecedor_repo.obter_todos_fornecedores()
#                 for f in fornecedores:
#                     if f.id != usuario_id:
#                         usuarios.append({
#                             "id": f.id,
#                             "nome": f.nome,
#                             "tipo": "fornecedor",
#                             "email": getattr(f, 'email', ''),
#                             "razao_social": getattr(f, 'razao_social', '')
#                         })
#         except:
#             pass
    
#     elif tipo_usuario.lower() in ["prestador", "fornecedor"]:
#         # Prestadores e fornecedores podem enviar para clientes
#         try:
#             if hasattr(cliente_repo, 'obter_todos_clientes'):
#                 clientes = cliente_repo.obter_todos_clientes()
#                 for c in clientes:
#                     if c.id != usuario_id:
#                         usuarios.append({
#                             "id": c.id,
#                             "nome": c.nome,
#                             "tipo": "cliente",
#                             "email": getattr(c, 'email', '')
#                         })
#         except:
#             pass
    
#     elif tipo_usuario.lower() in ["admin", "administrador"]:
#         # Admin pode enviar para todos
#         try:
#             if hasattr(cliente_repo, 'obter_todos_clientes'):
#                 clientes = cliente_repo.obter_todos_clientes()
#                 for c in clientes:
#                     usuarios.append({
#                         "id": c.id,
#                         "nome": c.nome,
#                         "tipo": "cliente",
#                         "email": getattr(c, 'email', '')
#                     })
#         except:
#             pass
        
#         try:
#             if hasattr(prestador_repo, 'obter_todos_prestadores'):
#                 prestadores = prestador_repo.obter_todos_prestadores()
#                 for p in prestadores:
#                     usuarios.append({
#                         "id": p.id,
#                         "nome": p.nome,
#                         "tipo": "prestador",
#                         "email": getattr(p, 'email', '')
#                     })
#         except:
#             pass
        
#         try:
#             if hasattr(fornecedor_repo, 'obter_todos_fornecedores'):
#                 fornecedores = fornecedor_repo.obter_todos_fornecedores()
#                 for f in fornecedores:
#                     usuarios.append({
#                         "id": f.id,
#                         "nome": f.nome,
#                         "tipo": "fornecedor",
#                         "email": getattr(f, 'email', '')
#                     })
#         except:
#             pass
    
#     return usuarios

# def organizar_conversas_por_contato(mensagens: List[Mensagem], usuario_id: int) -> List[dict]:
#     """Organiza mensagens em conversas por contato"""
#     conversas_dict = {}
    
#     for mensagem in mensagens:
#         # Determinar o contato (quem não é o usuário atual)
#         if mensagem.id_remetente == usuario_id:
#             contato_id = mensagem.id_destinatario
#             contato_nome = mensagem.nome_destinatario
#         else:
#             contato_id = mensagem.id_remetente
#             contato_nome = mensagem.nome_remetente
        
#         # Se é a primeira mensagem desta conversa ou se é mais recente
#         if (contato_id not in conversas_dict or 
#             mensagem.data_hora > conversas_dict[contato_id]["ultima_mensagem"].data_hora):
            
#             conversas_dict[contato_id] = {
#                 "contato_id": contato_id,
#                 "contato_nome": contato_nome,
#                 "ultima_mensagem": mensagem,
#                 "nao_lida": mensagem.id_destinatario == usuario_id  # Simplificado - você pode implementar um sistema mais robusto
#             }
    
#     # Converter para lista e ordenar por data da última mensagem
#     conversas = list(conversas_dict.values())
#     conversas.sort(key=lambda x: x["ultima_mensagem"].data_hora, reverse=True)
    
#     return conversas

# def contar_mensagens_nao_lidas(usuario_id: int) -> int:
#     """Conta mensagens não lidas do usuário (simplificado)"""
#     # Esta é uma implementação simplificada
#     # Você pode implementar um sistema mais robusto com campo 'lida' na tabela
#     try:
#         todas_mensagens = mensagem_repo.obter_mensagem()
#         # Por enquanto, retorna 0 - você pode implementar a lógica de mensagens não lidas
#         return 0
#     except:
#         return 0

# def formatar_data_mensagem(data: datetime) -> str:
#     """Formata data da mensagem para exibição"""
#     if isinstance(data, str):
#         try:
#             data = datetime.fromisoformat(data)
#         except:
#             return str(data)
    
#     agora = datetime.now()
#     diferenca = agora - data
    
#     if diferenca.days == 0:
#         return data.strftime("%H:%M")
#     elif diferenca.days == 1:
#         return "Ontem"
#     elif diferenca.days < 7:
#         dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
#         return dias_semana[data.weekday()]
#     else:
#         return data.strftime("%d/%m/%Y")

# # Filtros para templates Jinja2
# def registrar_filtros_jinja(templates: Jinja2Templates):
#     """Registra filtros personalizados para os templates"""
#     templates.env.filters['formatar_data'] = formatar_data_mensagem
