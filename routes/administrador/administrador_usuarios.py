
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


@router.get("/moderar_administrador")
@requer_autenticacao(['administrador'])
async def get_moderar_adm(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/moderar_adm/moderar_adm.html", {"request": request})


# Rota para moderar fornecedores
@router.get("/moderar_fornecedor")
@requer_autenticacao(['administrador'])
async def moderar_fornecedor(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("administrador/moderar_fornecedor.html", {"request": request})



# Rota POST para moderar prestadores
@router.post("/moderar_prestador")
@requer_autenticacao(['administrador'])
async def post_moderar_prestador(request: Request, usuario_logado: dict = None):
    # Completar
    return templates.TemplateResponse("administrador/moderar_prestador.html", {"request": request})


# Rota para remover administrador
@router.get("/remover")
async def remover_adm(request: Request):
    return templates.TemplateResponse("administrador/moderar_adm/remover_adm.html", {"request": request})

# Rota para remover um administrador
@router.post("/remover")
@requer_autenticacao(['administrador'])
async def remover_administrador(request: Request, id: int = Form(...), usuario_logado: dict = None):
    administrador_repo.remover_administrador_por_id(id)
    return templates.TemplateResponse("adm/administrador_remover.html", {"request": request})

# Rota dinâmica para buscar administrador por id
@router.get("/id/{id}")
async def get_administrador(request: Request, id: int):
    administrador = administrador_repo.obter_administrador_por_id(id)
    return templates.TemplateResponse("administrador.html", {"request": request, "administrador": administrador})

