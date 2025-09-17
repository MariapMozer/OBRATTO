from fastapi import APIRouter, Request, Form, HTTPException
from utils.auth_decorator import requer_autenticacao
from fastapi.templating import Jinja2Templates
from data.mensagem import mensagem_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Listar mensagens recebidas pelo fornecedor
@router.get("/recebidas")
@requer_autenticacao(['fornecedor'])
async def listar_mensagens_recebidas(request: Request, usuario_logado: dict = None):
    mensagens = mensagem_repo.obter_mensagens_recebidas(usuario_logado.id)
    return templates.TemplateResponse(
        "fornecedor/mensagens_recebidas.html",
        {"request": request, "mensagens": mensagens}
    )

# Listar mensagens enviadas pelo fornecedor
@router.get("/enviadas")
@requer_autenticacao(['fornecedor'])
async def listar_mensagens_enviadas(request: Request, usuario_logado: dict = None):
    mensagens = mensagem_repo.obter_mensagens_enviadas(usuario_logado.id)
    return templates.TemplateResponse(
        "fornecedor/mensagens_enviadas.html",
        {"request": request, "mensagens": mensagens}
    )

# Visualizar mensagem específica
@router.get("/{id_mensagem}")
@requer_autenticacao(['fornecedor'])
async def visualizar_mensagem(request: Request, id_mensagem: int, usuario_logado: dict = None):
    mensagem = mensagem_repo.obter_mensagem_por_id(id_mensagem)
    if not mensagem or mensagem.id_destinatario != usuario_logado.id:
        raise HTTPException(status_code=404, detail="Mensagem não encontrada")
    return templates.TemplateResponse(
        "fornecedor/mensagem_detalhe.html",
        {"request": request, "mensagem": mensagem}
    )

# Enviar nova mensagem
@router.post("/enviar")
@requer_autenticacao(['fornecedor'])
async def enviar_mensagem(request: Request, destinatario_id: int = Form(...), conteudo: str = Form(...), usuario_logado: dict = None):
    mensagem_repo.enviar_mensagem(usuario_logado.id, destinatario_id, conteudo)
    return templates.TemplateResponse(
        "fornecedor/mensagem_enviada_sucesso.html",
        {"request": request}
    )
