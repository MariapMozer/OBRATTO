from typing import Optional
from asyncio import open_connection
import os
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from data.usuario.usuario_sql import ATUALIZAR_FOTO
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from data.fornecedor.fornecedor_model import Fornecedor
from data.fornecedor import fornecedor_repo
from util.security import criar_hash_senha
from data.usuario import usuario_repo
from data.avaliacao import avaliacao_repo
from datetime import datetime

router = APIRouter()
templates = criar_templates("templates")


@router.get("/perfil")
@requer_autenticacao(["fornecedor"])
async def visualizar_perfil_fornecedor(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return templates.TemplateResponse(
        "fornecedor/perfil.html", {"request": request, "fornecedor": fornecedor}
    )


# 2. Editar/atualizar perfil do fornecedor
@router.post("/perfil/editar")
@requer_autenticacao(["fornecedor"])
async def editar_perfil_fornecedor(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    razao_social: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor.nome = nome
    fornecedor.email = email
    fornecedor.telefone = telefone
    fornecedor.razao_social = razao_social
    fornecedor_repo.atualizar_fornecedor(fornecedor)
    mensagem = "Perfil atualizado com sucesso."
    return templates.TemplateResponse(
        "fornecedor/perfil.html",
        {"request": request, "fornecedor": fornecedor, "mensagem": mensagem},
    )


# 3. Alterar senha do fornecedor

from util.security import verificar_senha, criar_hash_senha


@router.post("/perfil/alterar-senha")
@requer_autenticacao(["fornecedor"])
async def alterar_senha_fornecedor(
    request: Request,
    id: int,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    from data.usuario import usuario_repo

    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    # Verifica se a senha atual está correta (usando hash)
    if not verificar_senha(senha_atual, fornecedor.senha):
        from fastapi import status
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            f"/fornecedor/perfil/?erro=senha_incorreta",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    # Atualiza a senha com hash
    nova_senha_hash = criar_hash_senha(nova_senha)
    usuario_repo.atualizar_senha_usuario(usuario_logado["id"], nova_senha_hash)
    from fastapi import status
    from fastapi.responses import RedirectResponse

    return RedirectResponse(
        f"/fornecedor/perfil/?msg=senha_alterada", status_code=status.HTTP_303_SEE_OTHER
    )


# 4. Upload/atualização de foto de perfil
@router.post("/perfil/foto")
@requer_autenticacao(["fornecedor"])
async def upload_foto_perfil(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            "/fornecedor/perfil/?erro=tipo_invalido", status_code=303
        )

    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/fornecedores"
    os.makedirs(upload_dir, exist_ok=True)

    # Gerar nome único para o arquivo
    import secrets

    extensao = foto.filename.split(".")[-1] if foto.filename else "jpg"
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # Atualizar caminho no banco (usar caminho relativo)
        caminho_relativo = f"/static/uploads/fornecedores/{nome_arquivo}"
        atualizar_foto(usuario_logado["id"], caminho_relativo)

        # Atualizar sessão (se aplicável)
        usuario_logado["foto"] = caminho_relativo
        from util.auth_decorator import criar_sessao

        criar_sessao(request, usuario_logado)

    except Exception as e:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            "/fornecedor/perfil/?erro=upload_falhou", status_code=303
        )

    from fastapi.responses import RedirectResponse

    return RedirectResponse("/fornecedor/perfil/?foto_sucesso=1", status_code=303)


# 13. Deletar conta do fornecedor
@router.post("/perfil/excluir")
@requer_autenticacao(["fornecedor"])
async def deletar_conta_fornecedor(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor_repo.deletar_fornecedor(usuario_logado["id"])
    from fastapi import status
    from fastapi.responses import RedirectResponse

    return RedirectResponse(
        "/fornecedor/cadastro?msg=conta_excluida", status_code=status.HTTP_303_SEE_OTHER
    )


# Visualizar perfil do fornecedor
@router.get("/conta")
@requer_autenticacao(["fornecedor"])
async def visualizar_conta(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    return templates.TemplateResponse(
        "fornecedor/conta.html", {"request": request, "fornecedor": fornecedor}
    )


# Visualizar avaliações recebidas pelo fornecedor
@router.get("/avaliacoes")
@requer_autenticacao(["fornecedor"])
async def visualizar_avaliacoes_recebidas(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    # obter todas as avaliações e filtrar pelas que foram feitas para o fornecedor logado
    todas = avaliacao_repo.obter_todos()
    avaliacoes = [a for a in todas if getattr(a, 'id_avaliado', None) == usuario_logado['id']]
    return templates.TemplateResponse(
        "fornecedor/avaliacoes/recebidas.html",
        {"request": request, "avaliacoes": avaliacoes, "usuario_logado": usuario_logado},
    )


# atualizar foto de perfil


def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    from util.db import open_connection

    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0
