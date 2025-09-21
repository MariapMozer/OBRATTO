import os
from fastapi import APIRouter, Request, Form, HTTPException, UploadFile, status
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
@router.get("/editar")
@requer_autenticacao(["prestador"])
async def editar_perfil_prestador(request: Request):
    return templates.TemplateResponse("prestador/perfil/editar.html", {"request": request})

# Rota para processar o formulário de edição
@router.post("/editar")
@requer_autenticacao(["prestador"])
async def processar_edicao_perfil_prestador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    endereco: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None)
):
    return templates.TemplateResponse("prestador/perfil/editar.html", {"request": request})

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
    endereco: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None)
    ):
    return templates.TemplateResponse("prestador/perfil/excluir.html", {"request": request})



