import os
from fastapi import APIRouter, File, Request, Form, HTTPException, UploadFile, status
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


# Tudo funcionando corretamente!

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Rota para página inicial do Prestador
@router.get("")
async def home_prestador(request: Request):
    return templates.TemplateResponse("prestador/home.html", {"request": request})

# Rota para painel do Prestador
@router.get("/painel")
@requer_autenticacao(["prestador"])
async def painel_prestador(request: Request):
    return templates.TemplateResponse("prestador/perfil/painel.html", {"request": request})

# Visualizar perfil do fornecedor
@router.get("/perfil")
@requer_autenticacao(["prestador"])
async def exibir_perfil_prestador(request: Request):
    return templates.TemplateResponse("prestador/perfil/perfil.html", {"request": request})

# Editar perfil
@router.get("/editar/dados")
@requer_autenticacao(["prestador"])
async def editar_perfil_prestador(request: Request):
    return templates.TemplateResponse("prestador/perfil/editar_dados.html", {"request": request})

# Rota para processar o formulário de edição
@router.post("/editar/dados")
@requer_autenticacao(["prestador"])
async def processar_edicao_perfil_prestador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None)
):
    return templates.TemplateResponse("prestador/perfil/editar_dados.html", {"request": request})


# Rota para visualizar alteração de foto
@router.get("/perfil/alterar-foto")
@requer_autenticacao(["prestador"])
async def mostrar_alterar_foto(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse("prestador/perfil/foto/dados.html", {"request": request, "usuario": usuario_logado})

# Rota para processar alteração de foto
@router.post("/perfil/alterar-foto")
@requer_autenticacao(["prestador"])
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets
    filename = foto.filename
    if filename:
        extensao = filename.split(".")[-1]
    else:
        extensao = "jpg"
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



# Excluir perfil
@router.get("/excluir")
@requer_autenticacao(["prestador"])
async def excluir_perfil_prestador(request: Request):
    return templates.TemplateResponse("prestador/perfil/excluir.html", {"request": request})

# Rota para processar a exclusão do perfil
@router.post("/excluir")
async def processar_exclusao_perfil_prestador(request: Request, 
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),    
    bairro: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None)
    ):
    return templates.TemplateResponse("prestador/perfil/excluir.html", {"request": request})



