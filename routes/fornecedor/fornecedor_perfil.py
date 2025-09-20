
from asyncio import open_connection
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from data.usuario.usuario_sql import ATUALIZAR_FOTO
from utils.auth_decorator import requer_autenticacao
from fastapi.templating import Jinja2Templates
from data.fornecedor.fornecedor_model import Fornecedor
from data.fornecedor import fornecedor_repo
from utils.security import criar_hash_senha
from data.usuario import usuario_repo
from data.avaliacao import avaliacao_repo
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/perfil")
@requer_autenticacao(['fornecedor'])
async def visualizar_perfil_fornecedor(request: Request, usuario_logado: dict = None):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return templates.TemplateResponse(
        "fornecedor/perfil.html", 
        {"request": request,
        "fornecedor": fornecedor})

# 2. Editar/atualizar perfil do fornecedor
@router.post("/perfil/editar")
@requer_autenticacao(['fornecedor'])
async def editar_perfil_fornecedor(
    request: Request, 
    nome: str = Form(...), 
    email: str = Form(...), 
    telefone: str = Form(...), 
    endereco: str = Form(...), 
    razao_social: str = Form(...),
    usuario_logado: dict = None):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor.nome = nome
    fornecedor.email = email
    fornecedor.telefone = telefone
    fornecedor.endereco = endereco
    fornecedor.razao_social = razao_social
    fornecedor_repo.atualizar_fornecedor(fornecedor)
    mensagem = "Perfil atualizado com sucesso."
    return templates.TemplateResponse(
        "fornecedor/perfil.html", 
        {"request": request, 
         "fornecedor": fornecedor, 
         "mensagem": mensagem})

# 3. Alterar senha do fornecedor

from utils.security import verificar_senha, criar_hash_senha

@router.post("/perfil/alterar-senha")
@requer_autenticacao(['fornecedor'])
async def alterar_senha_fornecedor(
    request: Request,
    id: int,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    usuario_logado: dict = None
):
    from data.usuario import usuario_repo
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    # Verifica se a senha atual está correta (usando hash)
    if not verificar_senha(senha_atual, fornecedor.senha):
        from fastapi import status
        from fastapi.responses import RedirectResponse
        return RedirectResponse(
            f"/fornecedor/perfil/?erro=senha_incorreta",
            status_code=status.HTTP_303_SEE_OTHER
        )
    # Atualiza a senha com hash
    nova_senha_hash = criar_hash_senha(nova_senha)
    usuario_repo.atualizar_senha_usuario(usuario_logado.id, nova_senha_hash)
    from fastapi import status
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        f"/fornecedor/perfil/?msg=senha_alterada",
        status_code=status.HTTP_303_SEE_OTHER
    )

# 4. Upload/atualização de foto de perfil
@router.post("/perfil/foto")
@requer_autenticacao(['fornecedor'])
async def upload_foto_perfil(
    request: Request,
    foto: UploadFile = File(...), 
    usuario_logado: dict = None
    ):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    # Exemplo simples: salvar arquivo em static/img/fornecedores
    import os
    pasta_destino = "static/img/fornecedores"
    os.makedirs(pasta_destino, exist_ok=True)
    caminho_arquivo = os.path.join(pasta_destino, f"fornecedor_{usuario_logado.id}.jpg")
    with open(caminho_arquivo, "wb") as buffer:
        buffer.write(await foto.read())
    mensagem = "Foto de perfil atualizada com sucesso."
    return templates.TemplateResponse(
        "fornecedor/perfil.html", 
        {"request": request, 
         "fornecedor": fornecedor, 
         "mensagem": mensagem, 
         "foto_path": caminho_arquivo})

# 13. Deletar conta do fornecedor
@router.post("/perfil/excluir")
@requer_autenticacao(['fornecedor'])
async def deletar_conta_fornecedor(request: Request, usuario_logado: dict = None):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor_repo.deletar_fornecedor(usuario_logado.id)
    from fastapi import status
    from fastapi.responses import RedirectResponse
    return RedirectResponse(
        "/fornecedor/cadastro?msg=conta_excluida",
        status_code=status.HTTP_303_SEE_OTHER
    )

# Visualizar perfil do fornecedor
@router.get("/conta")
@requer_autenticacao(['fornecedor'])
async def visualizar_conta(request: Request, usuario_logado: dict = None):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado.id)
    return templates.TemplateResponse(
        "fornecedor/conta.html", 
        {"request": request, 
         "fornecedor": fornecedor})

# Visualizar avaliações recebidas pelo fornecedor
@router.get("/avaliacoes")
@requer_autenticacao(['fornecedor'])
async def visualizar_avaliacoes_recebidas(request: Request, usuario_logado: dict = None):
    avaliacoes = avaliacao_repo.obter_avaliacoes_por_fornecedor(usuario_logado.id)
    return templates.TemplateResponse(
        "fornecedor/avaliacoes_recebidas.html",
        {"request": request, "avaliacoes": avaliacoes}
    )



# atualizar foto de perfil

def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0
