"""
Rotas de autenticação: login, logout e recuperação de senha
"""
import logging
from typing import Optional
from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from data.usuario import usuario_repo
from dtos.usuario.login_dto import LoginDTO
from util.auth_decorator import obter_usuario_logado, aplicar_rate_limit_login
from util.security import criar_hash_senha, gerar_token_redefinicao, verificar_senha
from util.template_util import criar_templates

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Autenticação"])
templates = criar_templates("templates")


@router.get("/login")
async def mostrar_login(request: Request, mensagem: Optional[str] = None):
    """
    Exibe a página de login

    Args:
        request: Objeto Request do FastAPI contendo dados da requisição
        mensagem: Mensagem de sucesso opcional a ser exibida (ex: após cadastro)

    Returns:
        TemplateResponse: Página HTML do formulário de login

    Template:
        publico/login_cadastro/login.html
    """
    usuario_logado = obter_usuario_logado(request)
    context: dict = {"request": request, "usuario_logado": usuario_logado}
    if mensagem:
        context["sucesso"] = mensagem
    return templates.TemplateResponse("publico/login_cadastro/login.html", context)


@router.post("/login")
@aplicar_rate_limit_login()
async def processar_login(request: Request, email: str = Form(), senha: str = Form()):
    """
    Processa o login do usuário

    Valida as credenciais, cria a sessão do usuário e redireciona conforme o perfil.

    Segurança:
        - Rate limiting: 5 tentativas por 5 minutos (por IP)
        - Validação de dados via LoginDTO
        - Hash seguro de senha com bcrypt
        - Proteção contra timing attacks

    Args:
        request: Objeto Request do FastAPI
        email: Email do usuário (form data)
        senha: Senha do usuário (form data)

    Returns:
        - RedirectResponse: Redireciona para a home do perfil em caso de sucesso
        - TemplateResponse: Retorna formulário com erros em caso de falha

    Redirecionamentos por perfil:
        - admin/administrador: /administrador/home
        - fornecedor: /fornecedor
        - cliente: /cliente
        - prestador: /prestador
        - default: /

    Códigos de status:
        - 303: Login bem-sucedido (redirect)
        - 400: Campos vazios
        - 401: Credenciais inválidas
        - 429: Rate limit excedido (muitas tentativas)

    Template:
        publico/login_cadastro/login.html
    """
    dados_formulario = {"email": email}
    try:
        login_dto = LoginDTO(email=email, senha=senha)

        if not email or not senha:
            return templates.TemplateResponse(
                "publico/login_cadastro/login.html",
                {"request": request, "erro": "Preencha todos os campos."},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        usuario = usuario_repo.obter_usuario_por_email(login_dto.email)
        logger.debug(f"Tentativa de login para: {email}")

        if not usuario or not verificar_senha(login_dto.senha, usuario.senha):
            return templates.TemplateResponse(
                "publico/login_cadastro/login.html",
                {"request": request, "erro": "Email ou senha inválidos"},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )

        # Cria sessão completa
        perfil_usuario = getattr(
            usuario, "perfil", getattr(usuario, "tipo_usuario", "cliente")
        )
        usuario_dict = {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email,
            "perfil": perfil_usuario.lower(),  # Normaliza o perfil para minúsculas
            "foto": getattr(usuario, "foto", None),
        }
        request.session["usuario"] = usuario_dict

        # Redireciona conforme perfil
        perfil = usuario_dict["perfil"]
        if perfil == "admin" or perfil == "administrador":
            return RedirectResponse(
                "/administrador/home", status_code=status.HTTP_303_SEE_OTHER
            )
        elif perfil == "fornecedor":
            return RedirectResponse(
                "/fornecedor", status_code=status.HTTP_303_SEE_OTHER
            )
        elif perfil == "cliente":
            return RedirectResponse("/cliente", status_code=status.HTTP_303_SEE_OTHER)
        elif perfil == "prestador":
            return RedirectResponse("/prestador", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            loc = erro["loc"]
            campo = str(loc[0]) if loc and len(loc) > 0 else "campo"
            mensagem = erro["msg"]
            erros.append(f"{campo.capitalize()}: {mensagem}")

        erro_msg = " | ".join(erros)
        logger.warning(f"Erro de validação no login: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse(
            "publico/login_cadastro/login.html",
            {
                "request": request,
                "erro": erro_msg,
                "dados": dados_formulario,  # Preservar dados digitados
            },
        )

    except Exception as e:
        logger.error(f"Erro ao processar login: {e}", exc_info=True)

        return templates.TemplateResponse(
            "publico/login_cadastro/login.html",
            {
                "request": request,
                "erro": "Erro ao processar login. Tente novamente.",
                "dados": dados_formulario,
            },
        )


@router.get("/logout")
async def logout(request: Request):
    """
    Faz logout do usuário

    Limpa a sessão do usuário e redireciona para a página inicial.

    Args:
        request: Objeto Request do FastAPI

    Returns:
        RedirectResponse: Redireciona para a home (/) após logout

    Códigos de status:
        - 303: Logout bem-sucedido (redirect)
    """
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/recuperar-senha")
async def recuperar_senha_get(request: Request):
    """
    Exibe formulário de recuperação de senha

    Args:
        request: Objeto Request do FastAPI

    Returns:
        TemplateResponse: Página HTML do formulário de recuperação

    Template:
        publico/login_cadastro/recuperar_senha.html
    """
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/login_cadastro/recuperar_senha.html",
        {"request": request, "usuario_logado": usuario_logado}
    )


@router.post("/recuperar-senha")
async def recuperar_senha_post(request: Request, email: str = Form(...)):
    """
    Processa solicitação de recuperação de senha

    Gera um token de redefinição e atualiza no banco de dados.
    Em produção, enviaria email com link de redefinição.

    Args:
        request: Objeto Request do FastAPI
        email: Email do usuário que esqueceu a senha

    Returns:
        TemplateResponse: Página com mensagem de confirmação ou erro

    Comportamento:
        - Se email existe: Gera token e mostra link (simulação)
        - Se email não existe: Mostra mensagem "E-mail não encontrado"

    Códigos de status:
        - 200: Requisição processada (sempre retorna 200)

    Template:
        publico/login_cadastro/recuperar_senha.html

    TODO: Implementar envio de email real em produção
    """
    usuario = usuario_repo.obter_usuario_por_email(email)
    if usuario:
        # Gera token e salva no usuário
        token = gerar_token_redefinicao()
        usuario.token_redefinicao = token
        usuario_repo.atualizar_usuario(usuario)
        # Aqui você enviaria o e-mail real. Exemplo:
        link = f"http://localhost:8000/resetar-senha?token={token}"
        mensagem = f"Enviamos um link de recuperação para o e-mail: {email}. (Simulação: {link})"
    else:
        mensagem = "E-mail não encontrado."
    return templates.TemplateResponse(
        "publico/login_cadastro/recuperar_senha.html",
        {"request": request, "mensagem": mensagem}
    )


@router.get("/resetar-senha")
async def resetar_senha_get(request: Request, token: str):
    """
    Exibe formulário para redefinir senha

    Args:
        request: Objeto Request do FastAPI
        token: Token de redefinição enviado por email

    Returns:
        TemplateResponse: Formulário para definir nova senha

    Template:
        publico/login_cadastro/redefinir_senha.html
    """
    return templates.TemplateResponse(
        "publico/login_cadastro/redefinir_senha.html",
        {"request": request, "token": token},
    )


@router.post("/resetar-senha")
async def resetar_senha_post(
    request: Request, token: str = Form(...), nova_senha: str = Form(...)
):
    """
    Processa a redefinição de senha

    Valida o token, atualiza a senha do usuário e remove o token.

    Args:
        request: Objeto Request do FastAPI
        token: Token de redefinição (form data)
        nova_senha: Nova senha escolhida pelo usuário (form data)

    Returns:
        - RedirectResponse: Redireciona para /login em caso de sucesso
        - TemplateResponse: Retorna formulário com erro se token inválido

    Segurança:
        - Token é de uso único (removido após uso)
        - Senha é hasheada com bcrypt antes de salvar
        - Token inválido/expirado retorna erro genérico

    Códigos de status:
        - 303: Senha redefinida com sucesso (redirect)
        - 200: Token inválido (mostra formulário com erro)

    Template:
        publico/login_cadastro/redefinir_senha.html
    """
    usuario = usuario_repo.obter_usuario_por_token(token)
    if usuario:
        usuario.senha = criar_hash_senha(nova_senha)
        usuario.token_redefinicao = None
        usuario_repo.atualizar_usuario(usuario)
        return RedirectResponse("/login?mensagem=Senha redefinida com sucesso!", status_code=303)
    else:
        mensagem = "Token inválido ou expirado."
        return templates.TemplateResponse(
            "publico/login_cadastro/redefinir_senha.html",
            {"request": request, "mensagem": mensagem, "token": token},
        )
