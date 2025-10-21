"""
Rotas de perfis públicos
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

router = APIRouter(tags=["Perfis Públicos"])
templates = criar_templates("templates")

@router.get("/prestador/perfil_publico")
async def exibir_perfil_publico_prestador(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "public/perfil/prestador.html", {"request": request, "usuario_logado": usuario_logado}
    )


# Rota para perfil público do cliente
@router.get("/cliente/perfil_publico")
async def exibir_perfil_publico_cliente(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "public/perfil/cliente.html", {"request": request, "usuario_logado": usuario_logado}
    )


# Rota para perfil público do fornecedor
@router.get("/fornecedor/perfil_publico")
async def exibir_perfil_publico_fornecedor(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "public/perfil/fornecedor.html", {"request": request, "usuario_logado": usuario_logado}
    )


# -----------------------------------------------------
# ----------------- MENSAGEM --------------------------


# ROTAS PRINCIPAIS

# ============================================================================
# TODO ALUNO: REVISAR CÓDIGO COMENTADO - MENSAGENS
# ============================================================================
#
# PROBLEMA IDENTIFICADO: 25 linhas de código comentadas (linhas 825-849)
#
# O QUE FAZER:
# 1. ANALISE o código comentado abaixo
# 2. DECIDA se ele deve ser:
#    a) REMOVIDO (se não for mais necessário)
#    b) IMPLEMENTADO (se for necessário mas incompleto)
#    c) MOVIDO (se pertence a outro módulo)
#
# ANÁLISE INICIAL:
# - Parece ser uma rota GET /mensagens para exibir caixa de mensagens
# - NÃO usa @requer_autenticacao() (possível problema de segurança!)
# - Usa obter_usuario_logado() manualmente
# - Há uma função similar em linha 852: exibir_conversa()
#
# PERGUNTAS PARA VOCÊ:
# 1. Esta rota é necessária? Já existe implementação similar?
# 2. Se for necessária, por que está comentada?
# 3. A autenticação está correta?
# 4. A função organizar_conversas_por_contato() existe?
#
# AÇÃO RECOMENDADA:
# - Se for implementar: use @requer_autenticacao() e teste
# - Se for remover: delete todo o código comentado
# - Se não souber: consulte o professor
# ============================================================================

# @router.get("/mensagens")
# async def exibir_caixa_mensagens(request: Request):
#     """Exibe a caixa de mensagens principal do usuário"""
#     usuario = obter_usuario_logado(request)
#     if not usuario:
#         return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

#     # Obter todas as mensagens do usuário (enviadas e recebidas)
#     todas_mensagens = mensagem_repo.obter_mensagem()

#     # Filtrar mensagens do usuário atual
#     mensagens_usuario = [
#         msg for msg in todas_mensagens
#         if msg.id_remetente == usuario["id"] or msg.id_destinatario == usuario["id"]
#     ]

#     # Organizar conversas por contato
#     conversas = organizar_conversas_por_contato(mensagens_usuario, usuario["id"])

#     return templates.TemplateResponse("publico/mensagens/mensagens.html", {
#         "request": request,
#         "usuario": usuario,
#         "conversas": conversas,
#         "mensagens": mensagens_usuario
#     })


