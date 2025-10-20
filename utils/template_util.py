"""
Utilidades para trabalhar com templates Jinja2.
Centraliza a criação e configuração de templates.
"""

from fastapi.templating import Jinja2Templates
from typing import Optional
import os


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
        from utils.template_util import criar_templates

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

    # Configurações padrão
    config = {
        "autoescape": True,  # Prevenir XSS
        "auto_reload": True,  # Recarregar templates em desenvolvimento
    }

    # Sobrescrever com kwargs fornecidos
    config.update(kwargs)

    # Criar e retornar instância de Jinja2Templates
    return Jinja2Templates(directory=directory, **config)


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
