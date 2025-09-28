from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Request, status, UploadFile, File
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
from utils.auth_decorator import obter_usuario_logado
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
    razao_social: Optional[str] = Form(None),
    foto: UploadFile = File(None)
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

    # Lógica de upload de foto
    caminho_foto = None
    if foto and foto.filename:
        tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
        if foto.content_type not in tipos_permitidos:
            return templates.TemplateResponse(
                "publico/fornecedor2/cadastro_fornecedor.html",
                {"request": request, "erro": "Tipo de arquivo de foto inválido."}
            )
        upload_dir = "static/uploads/fornecedores"
        os.makedirs(upload_dir, exist_ok=True)
        import secrets
        extensao = foto.filename.split(".")[-1]
        nome_arquivo = f"{email}_{secrets.token_hex(8)}.{extensao}"
        caminho_arquivo = os.path.join(upload_dir, nome_arquivo)
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
        caminho_foto = f"/static/uploads/fornecedores/{nome_arquivo}"

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
        foto=caminho_foto,
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
    print("DEBUG usuario:", usuario)
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


# ROTAS PRINCIPAIS 
@router.get("/mensagens")
async def exibir_caixa_mensagens(request: Request):
    """Exibe a caixa de mensagens principal do usuário"""
    usuario = obter_usuario_logado(request)
    if not usuario:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Obter todas as mensagens do usuário (enviadas e recebidas)
    todas_mensagens = mensagem_repo.obter_mensagem()
    
    # Filtrar mensagens do usuário atual
    mensagens_usuario = [
        msg for msg in todas_mensagens 
        if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
    ]
    
    # Organizar conversas por contato
    conversas = organizar_conversas_por_contato(mensagens_usuario, usuario["id"])
    
    return templates.TemplateResponse("publico/mensagens/mensagens.html", {
        "request": request,
        "usuario": usuario,
        "conversas": conversas,
        "mensagens": mensagens_usuario
    })

@router.get("/mensagens/conversa/{contato_id}")
async def exibir_conversa(request: Request, contato_id: int):
    """Exibe uma conversa específica entre o usuário logado e um contato"""
    usuario = obter_usuario_logado(request)
    if not usuario:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Obter dados do contato
    contato = obter_dados_usuario_por_id(contato_id)
    if not contato:
        return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)
    
    # Obter mensagens da conversa
    todas_mensagens = mensagem_repo.obter_mensagem()
    mensagens_conversa = [
        msg for msg in todas_mensagens 
        if (msg.id_remetente == usuario["id"] and msg.id_destinatario == contato_id) or
           (msg.id_remetente == contato_id and msg.id_destinatario == usuario["id"])
    ]
    
    # Ordenar por data
    mensagens_conversa.sort(key=lambda x: x.data_hora)
    
    return templates.TemplateResponse("publico/mensagens/mensagens.html", {
        "request": request,
        "usuario": usuario,
        "contato": contato,
        "mensagens": mensagens_conversa
    })

@router.get("/mensagens/nova")
async def exibir_nova_mensagem(request: Request):
    """Exibe formulário para nova mensagem"""
    usuario = obter_usuario_logado(request)
    if not usuario:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    # Obter usuários disponíveis baseado no tipo do usuário logado
    usuarios_disponiveis = obter_usuarios_disponiveis_por_tipo(usuario["perfil"], usuario["id"])
    
    return templates.TemplateResponse("publico/mensagens/mensagens.html", {
        "request": request,
        "usuario": usuario,
        "usuarios_disponiveis": usuarios_disponiveis
    })

@router.post("/mensagens/enviar")
async def processar_envio_mensagem(
    request: Request,
    destinatario_id: int = Form(...),
    conteudo: str = Form(...)
):
    """Processa o envio de uma nova mensagem"""
    usuario = obter_usuario_logado(request)
    if not usuario:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    
    try:
        # Validar destinatário
        destinatario = obter_dados_usuario_por_id(destinatario_id)
        if not destinatario:
            return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)
        
        # Criar mensagem
        mensagem = Mensagem(
            id_mensagem=0,  # Será gerado automaticamente
            id_remetente=usuario["id"],
            id_destinatario=destinatario_id,
            conteudo=conteudo,
            data_hora=datetime.now(),
            nome_remetente=usuario["nome"],
            nome_destinatario=destinatario.nome
        )
        
        # Inserir mensagem no banco
        mensagem_repo.inserir_mensagem(mensagem)
        
        return RedirectResponse(
            f"/mensagens/conversa/{destinatario_id}", 
            status_code=status.HTTP_303_SEE_OTHER
        )
        
    except Exception as e:
        return RedirectResponse(
            "/mensagens", 
            status_code=status.HTTP_303_SEE_OTHER
        )

#-----------------------------------------------------
#------------- FUNÇÕES AUXILIARES -------------------
#-----------------------------------------------------

def obter_dados_usuario_por_id(usuario_id: int):
    """Obtém dados de um usuário por ID, buscando em todas as tabelas"""
    # Tentar buscar em clientes
    try:
        if hasattr(cliente_repo, 'obter_cliente_por_id'):
            cliente = cliente_repo.obter_cliente_por_id(usuario_id)
            if cliente:
                return cliente
    except:
        pass
    
    # Tentar buscar em prestadores
    try:
        if hasattr(prestador_repo, 'obter_prestador_por_id'):
            prestador = prestador_repo.obter_prestador_por_id(usuario_id)
            if prestador:
                return prestador
    except:
        pass
    
    # Tentar buscar em fornecedores
    try:
        if hasattr(fornecedor_repo, 'obter_fornecedor_por_id'):
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_id)
            if fornecedor:
                return fornecedor
    except:
        pass
    
    # Tentar buscar na tabela geral de usuários
    try:
        if hasattr(usuario_repo, 'obter_usuario_por_id'):
            usuario = usuario_repo.obter_usuario_por_id(usuario_id)
            if usuario:
                return usuario
    except:
        pass
    
    return None

def obter_usuarios_disponiveis_por_tipo(tipo_usuario: str, usuario_id: int):
    """Obtém usuários disponíveis baseado no tipo do usuário logado"""
    usuarios = []
    
    if tipo_usuario.lower() == "cliente":
        # Clientes podem enviar para prestadores e fornecedores
        try:
            if hasattr(prestador_repo, 'obter_todos_prestadores'):
                prestadores = prestador_repo.obter_todos_prestadores()
                for p in prestadores:
                    if p.id != usuario_id:
                        usuarios.append({
                            "id": p.id,
                            "nome": p.nome,
                            "tipo": "prestador",
                            "email": getattr(p, 'email', ''),
                            "area_atuacao": getattr(p, 'area_atuacao', '')
                        })
        except:
            pass
        
        try:
            if hasattr(fornecedor_repo, 'obter_todos_fornecedores'):
                fornecedores = fornecedor_repo.obter_todos_fornecedores()
                for f in fornecedores:
                    if f.id != usuario_id:
                        usuarios.append({
                            "id": f.id,
                            "nome": f.nome,
                            "tipo": "fornecedor",
                            "email": getattr(f, 'email', ''),
                            "razao_social": getattr(f, 'razao_social', '')
                        })
        except:
            pass
    
    elif tipo_usuario.lower() in ["prestador", "fornecedor"]:
        # Prestadores e fornecedores podem enviar para clientes
        try:
            if hasattr(cliente_repo, 'obter_todos_clientes'):
                clientes = cliente_repo.obter_todos_clientes()
                for c in clientes:
                    if c.id != usuario_id:
                        usuarios.append({
                            "id": c.id,
                            "nome": c.nome,
                            "tipo": "cliente",
                            "email": getattr(c, 'email', '')
                        })
        except:
            pass
    
    return usuarios

def organizar_conversas_por_contato(mensagens, usuario_id):
    """Organiza mensagens em conversas por contato"""
    conversas = {}
    
    for msg in mensagens:
        # Determinar o ID do contato (quem não é o usuário atual)
        contato_id = msg.id_destinatario if msg.id_remetente == usuario_id else msg.id_remetente
        contato_nome = msg.nome_destinatario if msg.id_remetente == usuario_id else msg.nome_remetente
        
        if contato_id not in conversas:
            conversas[contato_id] = {
                "contato_id": contato_id,
                "contato_nome": contato_nome,
                "mensagens": [],
                "ultima_mensagem": None
            }
        
        conversas[contato_id]["mensagens"].append(msg)
        
        # Atualizar última mensagem (assumindo que as mensagens estão ordenadas)
        if not conversas[contato_id]["ultima_mensagem"] or msg.data_hora > conversas[contato_id]["ultima_mensagem"].data_hora:
            conversas[contato_id]["ultima_mensagem"] = msg
    
    # Converter para lista e ordenar por última mensagem
    lista_conversas = list(conversas.values())
    lista_conversas.sort(key=lambda x: x["ultima_mensagem"].data_hora if x["ultima_mensagem"] else datetime.min, reverse=True)
    
    return lista_conversas