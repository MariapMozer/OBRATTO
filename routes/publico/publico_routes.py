from fastapi import APIRouter, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.usuario import usuario_repo
from utils.security import criar_hash_senha, gerar_token_redefinicao, verificar_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse("publico/home.html", {"request": request})


@router.get("/escolha_cadastro")
async def mostrar_escolha_cadastro(request: Request):
    return templates.TemplateResponse("publico/escolha_cadastro.html", {"request": request})


@router.get("/entrar")
async def mostrar_login(request: Request):
    return templates.TemplateResponse("publico/login.html", {"request": request})

# Rota POST para processar login

@router.post("/entrar")
async def processar_login(request: Request, email: str = Form(...), senha: str = Form(...)):
    if not email or not senha:
        return templates.TemplateResponse("publico/login.html", {"request": request, "erro": "Preencha todos os campos."}, status_code=status.HTTP_400_BAD_REQUEST)

    usuario = usuario_repo.obter_usuario_por_email(email)
    if not usuario or not verificar_senha(senha, usuario.senha):
        return templates.TemplateResponse("publico/login.html", {"request": request, "erro": "Email ou senha inválidos"}, status_code=status.HTTP_401_UNAUTHORIZED)

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


@router.get("/recuperar-senha")
async def recuperar_senha_get(request: Request):
    return templates.TemplateResponse("publico/recuperar_senha.html", {"request": request})


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
    return templates.TemplateResponse("publico/redefinir_senha.html", {"request": request, "token": token})

@router.post("/resetar-senha")
async def resetar_senha_post(request: Request, token: str = Form(...), nova_senha: str = Form(...)):
    usuario = usuario_repo.obter_usuario_por_token(token)
    if usuario:
        usuario.senha = criar_hash_senha(nova_senha)
        usuario.token_redefinicao = None
        usuario_repo.atualizar_usuario(usuario)
        mensagem = "Senha redefinida com sucesso! Faça login."
        return RedirectResponse("/publico/login", status_code=303)
    else:
        mensagem = "Token inválido ou expirado."
        return templates.TemplateResponse("publico/redefinir_senha.html", {"request": request, "mensagem": mensagem, "token": token})


# @router.get("/cadastro")
# async def exibir_cadastro_fornecedor(request: Request):
#     return templates.TemplateResponse("fornecedor/cadastro_fornecedor.html", {"request": request})

# # Cadastro de fornecedor (POST)

# @router.post("/cadastro")
# async def cadastrar_fornecedor(
#     request: Request,
#     nome: str = Form(...),
#     email: str = Form(...),
#     senha: str = Form(...),
#     cpf_cnpj: str = Form(...),
#     telefone: str = Form(...),
#     endereco: str = Form(...),
#     razao_social: str = Form(...)
# ):
    
#     # Verificar se o email já existe
#     usuario_existente = usuario_repo.obter_usuario_por_email(email)
#     if usuario_existente:
#         from fastapi import status
#         from fastapi.responses import RedirectResponse
#         return RedirectResponse(
#             "/fornecedor/cadastro?erro=email_existe",
#             status_code=status.HTTP_303_SEE_OTHER
#         )
#     # Criar o novo fornecedor
#     senha_hash = criar_hash_senha(senha)
#     novo_fornecedor = Fornecedor(
#         id=0,
#         nome=nome,
#         email=email,
#         senha=senha_hash,
#         cpf_cnpj=cpf_cnpj,
#         telefone=telefone,
#         data_cadastro=datetime.now(),
#         endereco=endereco,
#         tipo_usuario="Fornecedor",
#         razao_social=razao_social
#     )
#     from data.fornecedor import fornecedor_repo
#     id_gerado = fornecedor_repo.inserir_fornecedor(novo_fornecedor)
#     from fastapi import status
#     from fastapi.responses import RedirectResponse
#     if id_gerado:
#         return RedirectResponse(
#             f"/fornecedor/perfil_publico/{id_gerado}",
#             status_code=status.HTTP_303_SEE_OTHER
#         )
#     else:
#         return RedirectResponse(
#             "/fornecedor/cadastro?erro=erro_cadastro",
#             status_code=status.HTTP_303_SEE_OTHER
#         )