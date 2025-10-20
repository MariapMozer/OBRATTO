from typing import Optional
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from data.servico import servico_repo
from data.servico.servico_model import Servico
from util.auth_decorator import requer_autenticacao
from util.foto_util import (
    salvar_nova_foto,
    obter_foto_principal,
    obter_todas_fotos,
    excluir_foto,
    reordenar_fotos,
)


router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Rota para exibir a galeria
@router.get("/{id}/galeria")
@requer_autenticacao(["admin"])
async def get_galeria(request: Request, id: int, usuario_logado: Optional[dict] = None):
    servico = servico_repo.obter_servico_por_id(id)
    if not servico:
        return RedirectResponse("/admin/servico", status.HTTP_303_SEE_OTHER)

    fotos = obter_todas_fotos(id)  # ← Obtém todas as fotos do produto
    return templates.TemplateResponse(
        "administrador/galeria.html",
        {"request": request, "servico": servico, "fotos": fotos},
    )


# Rota para upload de múltiplas fotos
@router.post("/{id}/galeria/upload")
@requer_autenticacao(["admin"])
async def post_galeria_upload(
    request: Request,
    id: int,
    fotos: list[UploadFile] = File(...),  # ← Recebe múltiplas fotos
    usuario_logado: Optional[dict] = None,
):
    servico = servico_repo.obter_servico_por_id(id)
    if not servico:
        return RedirectResponse("/admin/servico", status.HTTP_303_SEE_OTHER)

    sucesso = 0
    for foto in fotos:
        if foto.filename:
            try:
                # Salvar cada foto como não-principal (será adicionada no final)
                salvar_nova_foto(id, foto.file, como_principal=False)
                sucesso += 1
            except Exception as e:
                print(f"Erro ao salvar foto {foto.filename}: {e}")

    return RedirectResponse(f"/admin/servico/{id}/galeria", status.HTTP_303_SEE_OTHER)


# Rota para excluir foto específica
@router.post("/{id}/galeria/excluir/{numero}")
@requer_autenticacao(["admin"])
async def post_galeria_excluir(
    request: Request,
    id: int,
    numero: int,  # ← Número da foto a ser excluída (001, 002, etc.)
    usuario_logado: Optional[dict] = None,
):
    servico = servico_repo.obter_servico_por_id(id)
    if not servico:
        return RedirectResponse("/admin/servico", status.HTTP_303_SEE_OTHER)

    try:
        excluir_foto(id, numero)  # ← Remove foto e reordena automaticamente
    except Exception as e:
        print(f"Erro ao excluir foto: {e}")

    return RedirectResponse(f"/admin/servico/{id}/galeria", status.HTTP_303_SEE_OTHER)


# Rota para reordenar fotos via drag-and-drop
@router.post("/{id}/galeria/reordenar")
@requer_autenticacao(["admin"])
async def post_galeria_reordenar(
    request: Request,
    id: int,
    nova_ordem: str = Form(...),  # ← Recebe string: "1,3,2,4"
    usuario_logado: Optional[dict] = None,
):
    servico = servico_repo.obter_servico_por_id(id)
    if not servico:
        return RedirectResponse("/admin/servico", status.HTTP_303_SEE_OTHER)

    try:
        # Converter string em lista de inteiros
        ordem_lista = [int(x.strip()) for x in nova_ordem.split(",")]
        reordenar_fotos(id, ordem_lista)  # ← Aplica nova ordem
    except Exception as e:
        print(f"Erro ao reordenar fotos: {e}")

    return RedirectResponse(f"/admin/servico/{id}/galeria", status.HTTP_303_SEE_OTHER)


# # Modificar rota de cadastro para aceitar foto principal
# @router.post("/cadastrar")
# @requer_autenticacao(["admin"])
# async def post_cadastrar(
#     request: Request,
#     titulo: str = Form(...),
#     descricao: str = Form(...),
#     categoria: float = Form(...),
#     valor_base: int = Form(...),
#     nome_prestador: int = Form(...),
#     foto: Optional[UploadFile] = File(None),  # ← Foto opcional no cadastro
#     usuario_logado: Optional[dict] = None
# ):
#     # 1. Criar produto primeiro
#     servico = Servico(
#         id=0, titlo=titulo, descricao=descricao,
#         categoria=categoria, valor_base=valor_base, nome_prestador=nome_prestador,
#     )
#     servico_id = servico_repo.inserir_servico(servico)

#     if servico_id:
#         # 2. Salvar foto se foi enviada
#         if foto and foto.filename:
#             try:
#                 salvar_nova_foto(servico_id, foto.file, como_principal=True)
#             except Exception as e:
#                 print(f"Erro ao salvar foto: {e}")

#         return RedirectResponse("/admin/servico", status.HTTP_303_SEE_OTHER)

#     # Erro ao criar produto...
