"""
Rotas de mensagens
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

router = APIRouter(tags=["Mensagens"])
templates = criar_templates("templates")

@router.get("/mensagens/conversa/{contato_id}")
@requer_autenticacao()
async def exibir_conversa(request: Request, contato_id: int, usuario_logado: Optional[dict] = None):
    """Exibe uma conversa específica entre o usuário logado e um contato"""
    assert usuario_logado is not None

    # Obter dados do contato
    contato = obter_dados_usuario_por_id(contato_id)
    if not contato:
        return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)

    # Obter mensagens da conversa
    todas_mensagens = mensagem_repo.obter_mensagem(usuario_logado["id"])
    mensagens_conversa = [
        msg
        for msg in todas_mensagens
        if (msg.id_remetente == usuario_logado["id"] and msg.id_destinatario == contato_id)
        or (msg.id_remetente == contato_id and msg.id_destinatario == usuario_logado["id"])
    ]

    # Ordenar por data
    mensagens_conversa.sort(key=lambda x: x.data_hora)

    return templates.TemplateResponse(
        "publico/mensagens/mensagens.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "contato": contato,
            "mensagens": mensagens_conversa,
        },
    )


@router.get("/mensagens/nova")
@requer_autenticacao()
async def exibir_nova_mensagem(request: Request, usuario_logado: Optional[dict] = None):
    """Exibe formulário para nova mensagem"""
    assert usuario_logado is not None

    # Obter usuários disponíveis baseado no tipo do usuário logado
    usuarios_disponiveis = obter_usuarios_disponiveis_por_tipo(
        usuario_logado["perfil"], usuario_logado["id"]
    )

    return templates.TemplateResponse(
        "publico/mensagens/mensagens.html",
        {
            "request": request,
            "usuario": usuario_logado,
            "usuarios_disponiveis": usuarios_disponiveis,
        },
    )


@router.post("/mensagens/enviar")
@requer_autenticacao()
async def processar_envio_mensagem(
    request: Request, destinatario_id: int = Form(...), conteudo: str = Form(...), usuario_logado: Optional[dict] = None
):
    """Processa o envio de uma nova mensagem"""
    assert usuario_logado is not None

    try:
        # Validar destinatário
        destinatario = obter_dados_usuario_por_id(destinatario_id)
        if not destinatario:
            return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)

        # Criar mensagem
        mensagem = Mensagem(
            id_mensagem=0,  # Será gerado automaticamente
            id_remetente=usuario_logado["id"],
            id_destinatario=destinatario_id,
            conteudo=conteudo,
            data_hora=datetime.now(),
            nome_remetente=usuario_logado["nome"],
            nome_destinatario=destinatario.nome,
        )

        # Inserir mensagem no banco
        mensagem_repo.inserir_mensagem(mensagem)

        return RedirectResponse(
            f"/mensagens/conversa/{destinatario_id}",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except Exception as e:
        return RedirectResponse("/mensagens", status_code=status.HTTP_303_SEE_OTHER)


# -----------------------------------------------------
