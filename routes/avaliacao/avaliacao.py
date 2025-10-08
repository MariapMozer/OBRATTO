from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from datetime import datetime
from typing import Optional
from data.avaliacao import avaliacao_repo
from data.avaliacao.avaliacao_model import Avaliacao
from config import templates

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])

#  Listar todas as avaliações
@router.get("/")
def listar_avaliacoes(request: Request):
    avaliacoes = avaliacao_repo.obter_todos()
    return templates.TemplateResponse(
        "avaliacao/listar.html",
        {"request": request, "avaliacoes": avaliacoes}
    )

#  Ver uma avaliação específica
@router.get("/{id_avaliacao}")
def obter_avaliacao(id_avaliacao: int, request: Request):
    avaliacao = avaliacao_repo.obter_avaliacao_por_id(id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return templates.TemplateResponse(
        "avaliacao/detalhes.html",
        {"request": request, "avaliacao": avaliacao}
    )

# Formulário para criar uma nova avaliação
@router.get("/nova")
def nova_avaliacao(request: Request):
    return templates.TemplateResponse("avaliacao/nova.html", {"request": request})

# Criar uma avaliação
@router.post("/nova")
def criar_avaliacao(
    request: Request,
    id_avaliador: int = Form(...),
    id_avaliado: int = Form(...),
    nota: float = Form(...),
    descricao: str = Form(...)
):
    nova = Avaliacao(
        id_avaliacao=0,
        id_avaliador=id_avaliador,
        id_avaliado=id_avaliado,
        nota=nota,
        data_avaliacao=datetime.now(),
        descricao=descricao
    )
    id_nova = avaliacao_repo.inserir_avaliacao(nova)
    if not id_nova:
        raise HTTPException(status_code=500, detail="Erro ao criar avaliação")
    return RedirectResponse(url="/avaliacoes", status_code=303)

# Formulário para editar uma avaliação
@router.get("/editar/{id_avaliacao}")
def editar_avaliacao_form(id_avaliacao: int, request: Request):
    avaliacao = avaliacao_repo.obter_avaliacao_por_id(id_avaliacao)
    if not avaliacao:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return templates.TemplateResponse(
        "avaliacao/editar.html",
        {"request": request, "avaliacao": avaliacao}
    )

# Atualizar uma avaliação
@router.post("/editar/{id_avaliacao}")
def atualizar_avaliacao(
    id_avaliacao: int,
    id_avaliador: int = Form(...),
    id_avaliado: int = Form(...),
    nota: float = Form(...),
    descricao: str = Form(...)
):
    existente = avaliacao_repo.obter_avaliacao_por_id(id_avaliacao)
    if not existente:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")

    atualizada = Avaliacao(
        id_avaliacao=id_avaliacao,
        id_avaliador=id_avaliador,
        id_avaliado=id_avaliado,
        nota=nota,
        data_avaliacao=datetime.now(),
        descricao=descricao
    )

    sucesso = avaliacao_repo.atualizar_avaliacao(atualizada)
    if not sucesso:
        raise HTTPException(status_code=500, detail="Erro ao atualizar avaliação")
    return RedirectResponse(url="/avaliacao", status_code=303)

# Excluir uma avaliação
@router.post("/excluir/{id_avaliacao}")
def excluir_avaliacao(id_avaliacao: int):
    sucesso = avaliacao_repo.deletar_avaliacao(id_avaliacao)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    return RedirectResponse(url="/avaliacao", status_code=303)

# 🔹 8. (Opcional) Obter avaliações de um prestador/fornecedor específico
@router.get("/avaliado/{id_avaliado}")
def obter_avaliacoes_por_avaliado(id_avaliado: int, request: Request):
    todas = avaliacao_repo.obter_todos()
    filtradas = [a for a in todas if a.id_avaliado == id_avaliado]
    return templates.TemplateResponse(
        "avaliacao/listar.html",
        {"request": request, "avaliacoes": filtradas}
    )

@router.get("/media/{id_avaliado}")
def media_avaliacoes(id_avaliado: int):
    todas = avaliacao_repo.obter_todos()
    notas = [a.nota for a in todas if a.id_avaliado == id_avaliado]
    if not notas:
        return {"media": 0.0}
    return {"media": sum(notas) / len(notas)}
