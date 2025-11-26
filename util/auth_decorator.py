"""
Decorator para proteger rotas com autenticação e autorização.

Funções principais:
- Verificação de autenticação (usuário logado)
- Verificação de autorização (perfis permitidos)
- Gerenciamento de sessão
"""

from functools import wraps
from typing import List, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import RedirectResponse
from util.logger_config import logger
from util.flash_messages import informar_erro
import asyncio
import inspect


def obter_usuario_logado(request: Request) -> Optional[dict]:
    """
    Obtém os dados do usuário logado da sessão

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Dicionário com dados do usuário ou None se não estiver logado
    """
    if not hasattr(request, "session"):
        return None
    return request.session.get("usuario")


def esta_logado(request: Request) -> bool:
    """
    Verifica se há um usuário logado

    Args:
        request: Objeto Request do FastAPI

    Returns:
        True se há usuário logado, False caso contrário
    """
    return obter_usuario_logado(request) is not None


def criar_sessao(request: Request, usuario: dict) -> None:
    """
    Cria uma sessão para o usuário após login

    Args:
        request: Objeto Request do FastAPI
        usuario: Dicionário com dados do usuário
    """
    if hasattr(request, "session"):
        # Remove senha da sessão por segurança
        usuario_sessao = usuario.copy()
        usuario_sessao.pop("senha", None)
        request.session["usuario"] = usuario_sessao


def destruir_sessao(request: Request) -> None:
    """
    Destrói a sessão do usuário (logout)

    Args:
        request: Objeto Request do FastAPI
    """
    if hasattr(request, "session"):
        request.session.clear()


def requer_autenticacao(perfis_autorizados: Optional[List[str]] = None):
    """
    Decorator para proteger rotas que requerem autenticação e autorização

    Args:
        perfis_autorizados: Lista de perfis autorizados a acessar a rota.
                           Se None, qualquer usuário logado pode acessar.
                           Validação é case-insensitive (admin = Admin = ADMIN)

    Exemplo de uso:
        @router.get("/admin")
        @requer_autenticacao(['Administrador'])
        async def admin_page(request: Request, usuario_logado: dict):
            # usuario_logado é injetado automaticamente
            ...

        @router.get("/perfil")
        @requer_autenticacao()  # Qualquer usuário logado
        async def perfil(request: Request, usuario_logado: dict):
            ...
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontra o objeto Request nos argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break

            if not request:
                logger.error(f"Request object not found in {func.__name__}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found",
                )

            # Verifica se o usuário está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                # Log de acesso negado
                logger.warning(
                    f"Acesso não autenticado bloqueado: {request.url.path} "
                    f"[IP: {request.client.host if request.client else 'unknown'}]"
                )

                # Flash message informativa
                informar_erro(
                    request, "Você precisa estar autenticado para acessar esta página."
                )

                # Redireciona para login preservando destino original
                return RedirectResponse(
                    url=f"/login?redirect={request.url.path}",
                    status_code=status.HTTP_303_SEE_OTHER,
                )

            # Verifica autorização se perfis foram especificados
            if perfis_autorizados:
                perfil_usuario = usuario.get("perfil", "").lower()
                perfis_permitidos_lower = [p.lower() for p in perfis_autorizados]

                if perfil_usuario not in perfis_permitidos_lower:
                    # Log de tentativa de acesso não autorizado
                    logger.warning(
                        f"Acesso não autorizado bloqueado: usuário '{usuario.get('email')}' "
                        f"(perfil: {usuario.get('perfil')}) tentou acessar {request.url.path} "
                        f"[perfis permitidos: {', '.join(perfis_autorizados)}] "
                        f"[IP: {request.client.host if request.client else 'unknown'}]"
                    )

                    # Flash message informativa
                    informar_erro(
                        request, "Você não tem permissão para acessar esta página."
                    )

                    # Redireciona para página inicial do perfil do usuário
                    return RedirectResponse(
                        url=f"/{perfil_usuario}", status_code=status.HTTP_303_SEE_OTHER
                    )

            # Log de acesso bem-sucedido (apenas DEBUG para não poluir logs)
            logger.debug(
                f"Acesso autorizado: {usuario.get('email')} "
                f"({usuario.get('perfil')}) -> {request.url.path}"
            )

            # Adiciona o usuário aos kwargs apenas se a função aceita esse parâmetro
            sig = inspect.signature(func)
            if "usuario_logado" in sig.parameters:
                kwargs["usuario_logado"] = usuario

            # Chama a função original
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return decorator
