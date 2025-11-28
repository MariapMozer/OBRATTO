from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from config import templates
from util.auth_decorator import requer_autenticacao
from data.servico import servico_repo
from data.servico.servico_model import Servico

router = APIRouter(prefix="/prestador") # Adicionando o prefixo aqui para consistência
UPlOAD_DIR = "static/uploads/servicos/"

# =============== LISTAR ===================
@router.get("/servicos")
@requer_autenticacao(["prestador"])
def listar_servicos(request: Request):
    # Assumindo que obter_todos() retorna uma lista de objetos Servico
    servicos = servico_repo.obter_todos()
    return templates.TemplateResponse(
        "prestador/servico/listar.html",
        {"request": request, "servicos": servicos}
    )


# =============== NOVO ====================
@router.get("/servicos/novo")
@requer_autenticacao(["prestador"])
def novo_servico(request: Request):
    return templates.TemplateResponse(
        "prestador/servico/novo.html",
        {"request": request}
    )


@router.post("/servicos/novo")
@requer_autenticacao(["prestador"])
def criar_servico(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...)
):
    servico = Servico(nome=nome, descricao=descricao, preco=preco)
    servico_repo.inserir(servico)

    return RedirectResponse(
        url="/prestador/servicos",
        status_code=303
    )


# =============== EDITAR ====================
@router.get("/servicos/{servico_id}")
@requer_autenticacao(["prestador"])
def editar_servico(request: Request, servico_id: int):
    servico = servico_repo.obter_por_id(servico_id)
    return templates.TemplateResponse(
        "prestador/servico/editar.html",
        {"request": request, "servico": servico}
    )


@router.post("/servicos/{servico_id}")
@requer_autenticacao(["prestador"])
def atualizar_servico(
    request: Request,
    servico_id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...)
):
    servico_repo.atualizar(servico_id, nome, descricao, preco)

    return RedirectResponse(
        url="/prestador/servicos",
        status_code=303
    )
