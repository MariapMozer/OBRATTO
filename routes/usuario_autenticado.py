import os
from fastapi import APIRouter, Request, Form, HTTPException, UploadFile, status, File
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from fastapi.templating import Jinja2Templates
from data.cliente.cliente_model import Cliente
from data.prestador import prestador_repo
from data.prestador.prestador_model import Prestador
from data.usuario import usuario_repo
from utils.auth_decorator import criar_sessao, requer_autenticacao
from utils.security import criar_hash_senha, verificar_senha


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# ------------ Prestador ----------------

# Rota para visualizar alteração de foto
@router.get("/prestador/perfil/alterar-foto")
@requer_autenticacao(["prestador"])
async def alterar_foto(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("prestador/perfil/foto/dados.html", {"request": request, "usuario": usuario_logado})

# Rota para processar alteração de foto
@router.post("/prestador/perfil/alterar-foto")
@requer_autenticacao("prestador")
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...), 
    usuario_logado: dict = None
):
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        usuario_repo.atualizar_foto(usuario_logado['id'], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        from utils.auth_decorator import criar_sessao
        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)


# ------------ Fornecedor ----------------