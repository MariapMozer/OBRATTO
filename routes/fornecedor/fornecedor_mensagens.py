from typing import Optional
from fastapi import APIRouter, Request, Form, HTTPException
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from data.mensagem import mensagem_repo
from data.usuario import usuario_repo

router = APIRouter(prefix="/mensagens")
templates = criar_templates("templates")


# Listar mensagens recebidas pelo fornecedor
@router.get("/recebidas")
@requer_autenticacao(["fornecedor"])
async def listar_mensagens_recebidas(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    mensagens = mensagem_repo.obter_mensagem(usuario_logado["id"])
    return templates.TemplateResponse(
        "fornecedor/mensagens/recebidas.html",
        {"request": request, "mensagens": mensagens},
    )


# Listar mensagens enviadas pelo fornecedor
@router.get("/enviadas")
@requer_autenticacao(["fornecedor"])
async def listar_mensagens_enviadas(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    # TODO: Implement obter_mensagens_enviadas or filter obter_mensagem results
    mensagens = mensagem_repo.obter_mensagem(usuario_logado["id"])
    return templates.TemplateResponse(
        "fornecedor/mensagens_enviadas.html",
        {"request": request, "mensagens": mensagens},
    )


# Visualizar mensagem específica
@router.get("/{id_mensagem}")
@requer_autenticacao(["fornecedor"])
async def visualizar_mensagem(
    request: Request, id_mensagem: int, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    mensagem = mensagem_repo.obter_mensagem_por_id(id_mensagem)
    if not mensagem or mensagem.id_destinatario != usuario_logado["id"]:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return templates.TemplateResponse(
        "fornecedor/mensagem_detalhe.html", {"request": request, "mensagem": mensagem}
    )


# Enviar nova mensagem
@router.post("/enviar")
@requer_autenticacao(["fornecedor"])
async def enviar_mensagem_fornecedor(
    request: Request,
    destinatario_id: int = Form(...),
    conteudo: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    from data.mensagem.mensagem_model import Mensagem
    from datetime import datetime

    mensagem = Mensagem(
        id_mensagem=0,
        id_remetente=usuario_logado["id"],
        id_destinatario=destinatario_id,
        conteudo=conteudo,
        data_hora=datetime.now(),
        nome_remetente="",
        nome_destinatario="",
    )
    mensagem_repo.inserir_mensagem(mensagem)
    return templates.TemplateResponse(
        "fornecedor/mensagem_enviada_sucesso.html", {"request": request}
    )


# # Chat / Conversação com outro usuário
# @router.get("/chat/{id_usuario}")
# @requer_autenticacao(['fornecedor'])
# async def abrir_chat(request: Request, id_usuario: int, usuario_logado: Optional[dict] = None):
#     """
#     Abre a tela de chat/conversação com um usuário específico.
#     Mostra todo o histórico de mensagens trocadas entre os dois usuários.
#     """
#     # Obter informações do usuário com quem vai conversar
#     outro_usuario = usuario_repo.obter_usuario_por_id(id_usuario)

#     if not outro_usuario:
#         raise HTTPException(status_code=404, detail="Usuário não encontrado")

#     # Obter histórico de mensagens entre os dois usuários
#     # (mensagens enviadas e recebidas entre eles)
#     mensagens = mensagem_repo.obter_conversa_entre_usuarios(
#         usuario_logado['id'],
#         id_usuario
#     )

#     # Marcar mensagens recebidas como lidas
#     mensagem_repo.marcar_mensagens_como_lidas(
#         id_remetente=id_usuario,
#         id_destinatario=usuario_logado['id']
#     )

#     return templates.TemplateResponse(
#         "fornecedor/mensagens/chat.html",
#         {
#             "request": request,
#             "outro_usuario": outro_usuario,
#             "mensagens": mensagens,
#             "usuario_logado": usuario_logado
#         }
#     )

# # Enviar mensagem no chat (AJAX)
# @router.post("/chat/{id_usuario}/enviar")
# @requer_autenticacao(['fornecedor'])
# async def enviar_mensagem_chat(
#     request: Request,
#     id_usuario: int,
#     mensagem: str = Form(...),
#     usuario_logado: Optional[dict] = None
# ):
#     """
#     Envia uma mensagem no chat (usado via AJAX).
#     Retorna JSON com a mensagem criada.
#     """
#     if not mensagem or not mensagem.strip():
#         raise HTTPException(status_code=400, detail="Mensagem vazia")

#     # Criar mensagem
#     id_mensagem = mensagem_repo.enviar_mensagem(
#         id_remetente=usuario_logado['id'],
#         id_destinatario=id_usuario,
#         conteudo=mensagem.strip()
#     )

#     # Retornar JSON com sucesso
#     return {
#         "sucesso": True,
#         "id_mensagem": id_mensagem,
#         "mensagem": "Mensagem enviada com sucesso"
#     }
