from datetime import datetime
import os
import uuid
from fastapi import APIRouter, File, Request, Form, HTTPException, UploadFile, status
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional, List
from config import templates
from data.servico import servico_repo
from data.servico.servico_model import Servico
from util.auth_decorator import requer_autenticacao
from util.foto_util import obter_foto_principal, salvar_nova_foto

router = APIRouter()
UPLOAD_DIR = "static/uploads"

# Tudo funcionando perfeitamente


# Rota para listar serviços do Prestador
@router.get("/meus/servicos")
@requer_autenticacao(["prestador"])
async def gets(request: Request, usuario_logado: Optional[dict] = None):
    servicos = servico_repo.obter_servico()

    # Adicionar informação de foto para cada produto
    servicos_com_foto = []
    for servico in servicos:
        foto_principal = obter_foto_principal(servico.id_servico)
        servicos_com_foto.append({"servico": servico, "foto_principal": foto_principal})

    return templates.TemplateResponse(
        "prestador/servicos/meus_servicos.html",
        {"request": request, "servicos": servicos_com_foto},
    )


# Rota para cadastrar novo serviço
@router.get("/novo")
@requer_autenticacao(["prestador"])
async def form_novo_servicos(request: Request):
    return templates.TemplateResponse(
        "prestador/servicos/novo_servico.html", {"request": request}
    )


# Rota para processar o formulário de novo serviço
@router.post("/novo")
@requer_autenticacao(["prestador"])
async def processar_novo_servico(
    request: Request,
    id_servico: int = Form(...),
    id_prestador: int = Form(...),
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    valor_base: float = Form(...),
    nome_prestador: str = Form(...),
    foto: UploadFile = File(None),  # << aqui entra a foto
):
    servico = Servico(
        id_servico=0,
        id_prestador=id_prestador,
        titulo=titulo,
        descricao=descricao,
        categoria=categoria,
        valor_base=valor_base,
        nome_prestador=nome_prestador,
    )

    servico_id = servico_repo.inserir_servico(servico)
    if servico_id:
        if foto and foto.filename:
            try:
                # Salvar a foto usando a função de utilidade
                salvar_nova_foto(servico_id, foto.file, como_principal=True)
            except Exception as e:
                print(f"Erro ao salvar foto do serviço {servico_id}: {e}")
                # Tratar erro de upload de foto, mas não impedir o cadastro do serviço
        return RedirectResponse("/meus/servicos", status.HTTP_303_SEE_OTHER)
    else:
        return templates.TemplateResponse(
            "prestador/servicos/.html",
            {"request": request, "erro": "Erro ao cadastrar serviço."},
        )


# Editar serviço
@router.get("/editar/servicos")
@requer_autenticacao(["prestador"])
async def editar_servicos(request: Request, id_servico: int):
    return templates.TemplateResponse(
        "prestador/servicos/editar.html",
        {"request": request, "id_servico": id_servico},
    )


# Rota para processar o formulário de edição do serviço
@router.post("/editar/servicos")
@requer_autenticacao(["prestador"])
async def processar_edicao_servico(
    request: Request,
    id_servico: int = Form(...),
    id_prestador: int = Form(...),
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    valor_base: float = Form(...),
    nome_prestador: str = Form(...),
):
    return templates.TemplateResponse(
        "prestador/servicos/editar.html", {"request": request}
    )


# Detalhes do serviço
@router.get("/detalhes")
@requer_autenticacao(["prestador"])
async def detalhes_servicos(request: Request, id_servico: int):
    return templates.TemplateResponse(
        "prestador/servicos/detalhes.html",
        {"request": request, "id_servico": id_servico},
    )


# Buscar serviço
@router.get("/buscar")
@requer_autenticacao(["prestador"])
async def buscar_servicos(request: Request, id_servico: int):
    return templates.TemplateResponse(
        "prestador/servicos/buscar.html", {"request": request, "id_servico": id_servico}
    )


# status do serviço
@router.get("/status")
@requer_autenticacao(["prestador"])
async def status_servicos(request: Request, id_servico: int):
    return templates.TemplateResponse(
        "prestador/servicos/status.html", {"request": request, "id_servico": id_servico}
    )


# Excluir serviço
@router.get("/servicos/excluir")
@requer_autenticacao(["prestador"])
async def excluir_servico(request: Request, id_servico: int):
    return templates.TemplateResponse(
        "prestador/servicos/excluir.html",
        {"request": request, "id_servico": id_servico},
    )


# Rota para processar a exclusão do serviço
@router.post("/servicos/excluir")
@requer_autenticacao(["prestador"])
async def processar_exclusao_servico(
    request: Request,
    id_servico: int = Form(...),
    id_prestador: int = Form(...),
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    valor_base: float = Form(...),
    nome_prestador: str = Form(...),
):
    return templates.TemplateResponse(
        "prestador/servicos/excluir.html",
        {"request": request, "id_servico": id_servico},
    )


# # Rota POST para cadastrar novo serviço
# @router.post("/servicos/novo")
# async def cadastrar_servico(
#     request: Request,
#     nome: str = Form(...),
#     descricao: str = Form(...),
#     preco: float = Form(...),
# ):
#     try:
#         # Cria o dicionário/objeto de serviço
#         novo_servico = {
#             "nome": nome,
#             "descricao": descricao,
#             "preco": preco,
#         }
#         servico_repo.inserir(novo_servico)
#         return RedirectResponse(
#             url="/servicos",
#             status_code=status.HTTP_303_SEE_OTHER
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Erro ao cadastrar serviço: {str(e)}"
#         )
