
from fastapi import APIRouter, Request, Form, Depends, File, UploadFile
from fastapi.templating import Jinja2Templates
from data.administrador import administrador_repo
from utils.auth_decorator import requer_autenticacao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

administrador_usuarios = APIRouter()

# Rota para exibir o formulário de cadastro do administrador
@router.get("/cadastro")
@requer_autenticacao(['administrador'])
async def exibir_cadastro_administrador(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/moderar_adm/cadastrar_adm.html", {"request": request})

# Rota para cadastrar um novo administrador
@router.post("/cadastro")
@requer_autenticacao(['administrador'])
async def cadastrar_administrador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    novo_adm = {
        "nome": nome,
        "email": email,
        "senha": senha 
    }
    administrador_repo.criar_administrador(novo_adm)
    return templates.TemplateResponse("administrador/moderar_adm/cadastrar_adm.html", {"request": request})


@router.get("/home")
@requer_autenticacao(['administrador'])
async def get_home_adm(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/home_adm.html", {"request": request})


@router.get("/lista")
@requer_autenticacao(['administrador'])
async def get_lista_adm(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/moderar_adm/lista_adm.html", {"request": request})


@router.post("/editar_administrador")
@requer_autenticacao(['administrador'])
async def post_editar_adm(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: dict = None
):
    adm_atualizado = {
        "nome": nome,
        "email": email,
        "senha": senha 
    }
    administrador_repo.atualizar_administrador(id, adm_atualizado)
    return templates.TemplateResponse("administrador/moderar_adm/editar_adm.html", {"request": request})

@router.post("/excluir_administrador")
@requer_autenticacao(['administrador'])
async def post_excluir_adm(request: Request, id: int = Form(...), usuario_logado: dict = None):
    administrador_repo.remover_administrador_por_id(id)
    return templates.TemplateResponse("administrador/moderar_adm/remover_adm.html", {"request": request})

# buscar administrador por id
@router.get("/id/{id}")
async def get_administrador(request: Request, id: int):
    administrador = administrador_repo.obter_administrador_por_id(id)
    return templates.TemplateResponse("administrador.html", {"request": request, "administrador": administrador})

# Moderar prestadores
@router.get("/listar_prestador")
@requer_autenticacao(['administrador'])
async def get_listar_prestador(request: Request, usuario_logado: dict = None):
    prestadores = administrador_repo.listar_prestadores()
    return templates.TemplateResponse("administrador/listar_prestador.html", {"request": request, "prestadores": prestadores})


@router.post("/editar_prestador")
@requer_autenticacao(['administrador'])
async def post_editar_prestador(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: dict = None
):
    prestador_atualizado = {
        "nome": nome,
        "email": email
    }
    administrador_repo.atualizar_prestador(id, prestador_atualizado)
    return templates.TemplateResponse("administrador/listar_prestador.html", {"request": request})

@router.post("/excluir_prestador")
@requer_autenticacao(['administrador'])
async def post_excluir_prestador(request: Request, id: int = Form(...), usuario_logado: dict = None):
    administrador_repo.remover_prestador_por_id(id)
    return templates.TemplateResponse("administrador/listar_prestador.html", {"request": request})

# Rota dinâmica para buscar prestador por id
@router.get("/prestador/{id}")
@requer_autenticacao(['administrador'])
async def get_prestador_por_id(request: Request, id: int, usuario_logado: dict = None):
    prestador = administrador_repo.obter_prestador_por_id(id)
    return templates.TemplateResponse("administrador/detalhes_prestador.html", {"request": request, "prestador": prestador})

# Moderar Fornecedores
@router.get("/listar_fornecedor")
@requer_autenticacao(['administrador'])
async def get_listar_fornecedor(request: Request, usuario_logado: dict = None):
    fornecedores = administrador_repo.listar_fornecedores()
    return templates.TemplateResponse("administrador/listar_fornecedor.html", {"request": request, "fornecedores": fornecedores})

@router.post("/editar_fornecedor")
@requer_autenticacao(['administrador'])
async def post_editar_fornecedor(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: dict = None
):
    fornecedor_atualizado = {
        "nome": nome,
        "email": email
    }
    administrador_repo.atualizar_fornecedor(id, fornecedor_atualizado)
    return templates.TemplateResponse("administrador/listar_fornecedor.html", {"request": request})

@router.post("/excluir_fornecedor")
@requer_autenticacao(['administrador'])
async def post_excluir_fornecedor(request: Request, id: int = Form(...), usuario_logado: dict = None):
    administrador_repo.remover_fornecedor_por_id(id)
    return templates.TemplateResponse("administrador/listar_fornecedor.html", {"request": request})

# Rota dinâmica para buscar fornecedor por id

@router.get("/fornecedor/{id}")
@requer_autenticacao(['administrador'])
async def get_fornecedor_por_id(request: Request, id: int, usuario_logado: dict = None):
    fornecedor = administrador_repo.obter_fornecedor_por_id(id)
    return templates.TemplateResponse("administrador/detalhes_fornecedor.html", {"request": request, "fornecedor": fornecedor})

# Moderar Clientes

@router.get("/listar_cliente")
@requer_autenticacao(['administrador'])
async def get_listar_cliente(request: Request, usuario_logado: dict = None):
    clientes = administrador_repo.listar_clientes()
    return templates.TemplateResponse("administrador/listar_cliente.html", {"request": request, "clientes": clientes})

@router.post("/editar_cliente")
@requer_autenticacao(['administrador'])
async def post_editar_cliente(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: dict = None
):
    cliente_atualizado = {
        "nome": nome,
        "email": email
    }
    administrador_repo.atualizar_cliente(id, cliente_atualizado)
    return templates.TemplateResponse("administrador/listar_cliente.html", {"request": request})

@router.post("/excluir_cliente")
@requer_autenticacao(['administrador'])
async def post_excluir_cliente(request: Request, id: int = Form(...), usuario_logado: dict = None):
    administrador_repo.remover_cliente_por_id(id)
    return templates.TemplateResponse("administrador/listar_cliente.html", {"request": request})

# Rota dinâmica para buscar cliente por id
@router.get("/cliente/{id}")
@requer_autenticacao(['administrador'])
async def get_cliente_por_id(request: Request, id: int, usuario_logado: dict = None):
    cliente = administrador_repo.obter_cliente_por_id(id)
    return templates.TemplateResponse("administrador/detalhes_cliente.html", {"request": request, "cliente": cliente})