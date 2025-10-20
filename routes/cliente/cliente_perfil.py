from typing import Optional
from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import UploadFile, File
import os, secrets
from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from util.auth_decorator import requer_autenticacao
from util.security import criar_hash_senha
from fastapi import status

router = APIRouter()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "static/uploads/cliente"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/")
@requer_autenticacao(["cliente"])
async def get_page(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse("cliente/home.html", {"request": request})


# Visualizar perfil do cliente
@router.get("/perfil")
@requer_autenticacao(["cliente"])
async def exibir_perfil_cliente(request: Request):
    return templates.TemplateResponse(
        "cliente/perfil/perfil.html", {"request": request}
    )


# Editar dados do perfil
@router.get("/editar/dados")
@requer_autenticacao(["cliente"])
async def editar_perfil_cliente(request: Request):
    return templates.TemplateResponse(
        "cliente/perfil/editar_dados.html", {"request": request}
    )


# Rota para processar o formulário de edição de dados do perfil
@router.post("/editar/dados")
@requer_autenticacao(["cliente"])
async def processar_edicao_perfil_cliente(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    cpf_cnpj: str = Form(...),
    genero: str = Form(...),
    data_nascimento: str = Form(...),
    foto: Optional[UploadFile] = File(None),  # ← arquivo enviado
    usuario_logado: Optional[dict] = None,
):
    # ============================================================================
    # TODO ALUNO: IMPLEMENTAR EDIÇÃO DE PERFIL DO CLIENTE
    # ============================================================================
    #
    # Esta função está VAZIA e precisa ser implementada por você!
    #
    # OBJETIVO: Processar o formulário de edição de perfil do cliente
    #
    # PASSOS RECOMENDADOS:
    # 1. Validar os dados recebidos do formulário
    # 2. Verificar se o email já está sendo usado por outro usuário
    # 3. Se uma foto foi enviada, fazer upload e salvar o caminho
    # 4. Atualizar os dados do cliente no banco usando cliente_repo
    # 5. Usar flash messages para informar sucesso/erro (util.flash_messages)
    # 6. Redirecionar para a página de perfil
    #
    # DICAS:
    # - Use try/except para tratar erros
    # - Veja a função alterar_foto() abaixo como exemplo de upload de arquivo
    # - Use logger.info() e logger.error() para registrar eventos
    # - Veja as rotas de cadastro em publico_routes.py como referência
    #
    # EXEMPLO DE ESTRUTURA:
    #   try:
    #       # Validar e processar dados
    #       cliente = cliente_repo.obter_cliente_por_id(usuario_logado["id"])
    #       # Atualizar campos
    #       cliente_repo.atualizar_cliente(cliente)
    #       informar_sucesso(request, "Perfil atualizado com sucesso!")
    #       return RedirectResponse("/cliente/perfil", status.HTTP_303_SEE_OTHER)
    #   except Exception as e:
    #       logger.error(f"Erro ao editar perfil: {e}")
    #       # Retornar template com erro
    # ============================================================================
    pass  # ← REMOVA ESTA LINHA após implementar a função


# Editar foto de perfil
@router.get("/editar/fotos")
@requer_autenticacao(["cliente"])
async def editar_foto_perfil_cliente(
    request: Request, usuario_logado: Optional[dict] = None
):
    return templates.TemplateResponse(
        "cliente/perfil/editar_foto.html",
        {"request": request, "cliente": usuario_logado},
    )


# Rota para processar o formulário de edição de foto
@router.post("/editar/fotos")
@requer_autenticacao(["cliente"])
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),  # ← Recebe arquivo de foto
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse("/perfil?erro=tipo_invalido", status.HTTP_303_SEE_OTHER)

    # 2. Criar diretório se não existir
    upload_dir = "static/uploads/cliente"
    os.makedirs(upload_dir, exist_ok=True)

    # 3. Gerar nome único para evitar conflitos
    import secrets

    extensao = foto.filename.split(".")[-1] if foto.filename else "jpg"
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 4. Salvar arquivo no sistema
    try:
        conteudo = await foto.read()  # ← Lê conteúdo do arquivo
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 5. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/cliente/{nome_arquivo}"
        cliente_repo.atualizar_foto(usuario_logado["id"], caminho_relativo)

        # 6. Atualizar sessão do usuário
        usuario_logado["foto"] = caminho_relativo
        from util.auth_decorator import criar_sessao

        criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse("/perfil?erro=upload_falhou", status.HTTP_303_SEE_OTHER)

    return RedirectResponse("/perfil?foto_sucesso=1", status.HTTP_303_SEE_OTHER)


# Excluir perfil
@router.get("/excluir")
@requer_autenticacao(["cliente"])
async def excluir_perfil_cliente(request: Request):
    return templates.TemplateResponse("cliente/excluir.html", {"request": request})


# Rota para processar a exclusão do perfil
@router.post("/excluir")
@requer_autenticacao(["cliente"])
async def processar_exclusao_perfil_cliente(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    cliente_id = usuario_logado["id"]

    # Excluir cliente no banco
    cliente_repo.deletar_cliente(cliente_id)

    # Redirecionar para logout (encerra sessão)
    return RedirectResponse("/logout", status.HTTP_303_SEE_OTHER)
