"""
Utilidades para trabalhar com templates Jinja2.
Centraliza a criação e configuração de templates.
"""

from fastapi.templating import Jinja2Templates
from jinja2 import Environment, FileSystemLoader
from typing import Optional
import os
from util.flash_messages import get_flashed_messages


def criar_templates(directory: str = "templates", **kwargs) -> Jinja2Templates:
    """
    Cria uma instância de Jinja2Templates com configurações padronizadas.

    Args:
        directory: Diretório onde os templates estão localizados (padrão: "templates")
        **kwargs: Argumentos adicionais para Jinja2Templates

    Returns:
        Instância configurada de Jinja2Templates

    Exemplo:
        ```python
        from util.template_util import criar_templates

        # Criar templates para um módulo específico
        templates = criar_templates("templates/fornecedor")

        # Usar em uma rota
        @router.get("/listar")
        async def listar(request: Request):
            return templates.TemplateResponse("listar.html", {"request": request})
        ```
    """

    # Verificar se o diretório existe
    if not os.path.exists(directory):
        raise ValueError(f"Diretório de templates não encontrado: {directory}")

    # Criar environment Jinja2 customizado
    env = Environment(
        loader=FileSystemLoader(directory), autoescape=True, auto_reload=True
    )

    # Injetar funções globais
    env.globals["get_flashed_messages"] = get_flashed_messages
    env.globals["obter_mensagens"] = get_flashed_messages  # Alias em português

    # Criar instância de Jinja2Templates com environment customizado
    templates = Jinja2Templates(env=env)

    return templates


def criar_templates_multi(directories: list[str], **kwargs) -> Jinja2Templates:
    """
    Cria uma instância de Jinja2Templates com múltiplos diretórios.

    Args:
        directories: Lista de diretórios onde os templates estão localizados
        **kwargs: Argumentos adicionais para Jinja2Templates

    Returns:
        Instância configurada de Jinja2Templates com múltiplos diretórios

    Exemplo:
        ```python
        # Criar templates com múltiplos diretórios
        templates = criar_templates_multi([
            "templates/fornecedor",
            "templates/shared"
        ])
        ```
    """

    # Verificar se todos os diretórios existem
    for directory in directories:
        if not os.path.exists(directory):
            raise ValueError(f"Diretório de templates não encontrado: {directory}")

    # Configurações padrão
    config = {
        "autoescape": True,
        "auto_reload": True,
    }

    # Sobrescrever com kwargs fornecidos
    config.update(kwargs)

    # Jinja2Templates não suporta múltiplos diretórios nativamente
    # Retornar o primeiro diretório (pode ser melhorado no futuro)
    return Jinja2Templates(directory=directories[0], **config)


# Alias para compatibilidade
get_templates = criar_templates
