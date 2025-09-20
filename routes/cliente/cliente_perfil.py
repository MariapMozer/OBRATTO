from typing import Optional
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File
import os, secrets
from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from utils.auth_decorator import requer_autenticacao
from utils.security import criar_hash_senha

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_page(request: Request):
    return templates.TemplateResponse("cliente/home.html", { "request": request })

# Visualizar perfil do cliente
@router.get("/perfil")
@requer_autenticacao(["cliente"])
async def exibir_perfil_cliente(request: Request):
    return templates.TemplateResponse("cliente/perfil/perfil.html", {"request": request})

# Editar perfil
@router.get("/editar")
@requer_autenticacao(["cliente"])
async def editar_perfil_cliente(request: Request):
    return templates.TemplateResponse("cliente/perfil/editar.html", {"request": request})


# Rota para processar o formulário de edição
@router.post("/editar")
@requer_autenticacao(["cliente"])
async def processar_edicao_perfil_cliente(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    endereco: str = Form(...),
    genero: str = Form(...),
    data_nascimento: str = Form(...),
    foto: Optional[UploadFile] = File(None),  # ← arquivo enviado
    usuario_logado: dict = None
):
    # Atualizar dados no banco
    cliente = Cliente(
        id=usuario_logado["id"],
        nome=nome,
        email=email,
        senha=criar_hash_senha(senha) if senha else usuario_logado["senha"],
        telefone=telefone,
        cpf_cnpj=cpf_cnpj,
        endereco=endereco,
        genero=genero,
        data_nascimento=data_nascimento,
        foto=usuario_logado.get("foto")
    )

    # Atualizar foto, se houver upload
    if foto:
        tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
        if foto.content_type not in tipos_permitidos:
            return templates.TemplateResponse(
                "cliente/perfil/editar.html",
                {"request": request, "erro": "Tipo de arquivo inválido"}
            )

        upload_dir = "static/uploads/clientes"
        os.makedirs(upload_dir, exist_ok=True)

        extensao = foto.filename.split(".")[-1]
        nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
        caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        cliente.foto = f"/static/uploads/clientes/{nome_arquivo}"

    # Atualizar no banco
    from data.cliente import cliente_repo
    cliente_repo.atualizar(cliente)

    # Atualizar sessão
    usuario_logado.update({"foto": cliente.foto})
    from utils.auth_decorator import criar_sessao
    criar_sessao(request, usuario_logado)

    return RedirectResponse("/perfil", status_code=303)


# Excluir perfil
@router.get("/excluir")
@requer_autenticacao(["cliente"])
async def excluir_perfil_prestador(request: Request):
    return templates.TemplateResponse("cliente/excluir.html", {"request": request})

# Rota para processar a exclusão do perfil
@router.post("/excluir")
@requer_autenticacao(["cliente"])
async def processar_exclusao_perfil_cliente(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    endereco: str = Form(...),
    data_cadastro: str = Form(...),
    genero: str = Form(...),
    data_nascimento: str = Form(...),
    tipo_usuario: str = "cliente",
    foto: Optional[str] = None,
    token_redefinicao: Optional[str] = None,
    data_token: Optional[str] = None
    ):
    return templates.TemplateResponse("cliente/excluir.html", {"request": request})
