"""
Rotas de catálogo de serviços
"""
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from data.fornecedor import fornecedor_repo
from data.fornecedor.fornecedor_model import Fornecedor
from data.prestador import prestador_repo
from data.prestador.prestador_model import Prestador
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.mensagem.mensagem_model import Mensagem
from data.mensagem import mensagem_repo
from dtos.cliente.cliente_dto import CriarClienteDTO
from dtos.fornecedor.fornecedor_dto import CriarFornecedorDTO
from dtos.prestador.prestador_dto import CriarPrestadorDTO
from util.auth_decorator import obter_usuario_logado, requer_autenticacao
from util.flash_messages import informar_sucesso
from util.security import criar_hash_senha, gerar_token_redefinicao, verificar_senha
from util.template_util import criar_templates
import os
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Serviços"])
templates = criar_templates("templates")

@router.get("/servicos/aluguel-maquinario")
async def exibir_aluguel_maquinario(request: Request):
    """Página em construção - Aluguel de Maquinário"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Aluguel de Maquinário",
            "descricao": "Plataforma de aluguel de equipamentos e máquinas para construção civil: betoneiras, andaimes, compactadores, etc.",
            "icone": "bi-truck",
        },
    )


@router.get("/servicos/reformas")
async def exibir_reformas(request: Request):
    """Página em construção - Reformas"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Reformas",
            "descricao": "Sistema de orçamentos e contratação de serviços de reformas residenciais e comerciais completas.",
            "icone": "bi-hammer",
        },
    )


@router.get("/servicos/para-casa")
async def exibir_para_casa(request: Request):
    """Página em construção - Para a Casa"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Para a Casa",
            "descricao": "Serviços domésticos e manutenção residencial: chaveiro, jardinagem, limpeza, pequenos reparos.",
            "icone": "bi-house-heart",
        },
    )


@router.get("/servicos/construcao")
async def exibir_construcao(request: Request):
    """Página em construção - Construção"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Construção",
            "descricao": "Gestão de projetos de construção civil: orçamentos, cronogramas, acompanhamento de obras.",
            "icone": "bi-building",
        },
    )


@router.get("/servicos/fornecedores")
async def exibir_fornecedores(request: Request):
    """Página em construção - Fornecedores"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Fornecedores",
            "descricao": "Catálogo de materiais de construção e fornecedores parceiros com cotações online.",
            "icone": "bi-shop",
        },
    )


@router.get("/servicos/outros-servicos")
async def exibir_outros_servicos(request: Request):
    """Página em construção - Outros Serviços"""
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/em_construcao.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "titulo": "Outros Serviços",
            "descricao": "Serviços especializados diversos: paisagismo, automação residencial, energia solar, etc.",
            "icone": "bi-grid-3x3-gap",
        },
    )


# -----------------------------------------------------
