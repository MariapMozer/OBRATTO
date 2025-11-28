from typing import Optional
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from data.avaliacao import avaliacao_repo
from data.fornecedor import fornecedor_repo
from datetime import datetime

router = APIRouter()
templates = criar_templates("templates")


@router.get("/avaliacoes/recebidas")
@requer_autenticacao(["fornecedor"])
async def avaliacoes_recebidas(
    request: Request,
    usuario_logado: Optional[dict] = None,
    ordenar: str = "recente",
):
    """
    Página de avaliações recebidas pelo fornecedor
    """
    assert usuario_logado is not None
    
    # Verificar se fornecedor existe
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    # Obter todas as avaliações para este fornecedor (id_avaliado = usuario_logado["id"])
    todas_avaliacoes = avaliacao_repo.obter_todos()
    
    # Filtrar apenas avaliações recebidas por este fornecedor
    avaliacoes = [
        a for a in todas_avaliacoes 
        if a.id_avaliado == usuario_logado["id"]
    ]

    # Ordenação
    if ordenar == "recente":
        avaliacoes.sort(key=lambda x: x.data_avaliacao, reverse=True)
    elif ordenar == "antiga":
        avaliacoes.sort(key=lambda x: x.data_avaliacao)
    elif ordenar == "nota_alta":
        avaliacoes.sort(key=lambda x: x.nota, reverse=True)
    elif ordenar == "nota_baixa":
        avaliacoes.sort(key=lambda x: x.nota)

    # Calcular estatísticas
    media_nota = 0
    nota_maxima = 0
    nota_minima = 5
    
    if avaliacoes:
        media_nota = sum(a.nota for a in avaliacoes) / len(avaliacoes)
        nota_maxima = max(a.nota for a in avaliacoes)
        nota_minima = min(a.nota for a in avaliacoes)

    return templates.TemplateResponse(
        "fornecedor/avaliacoes/recebidas.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "avaliacoes": avaliacoes,
            "media_nota": media_nota,
            "nota_maxima": nota_maxima,
            "nota_minima": nota_minima,
            "now": datetime.now(),
        }
    )


@router.post("/avaliacoes/responder")
@requer_autenticacao(["fornecedor"])
async def responder_avaliacao(
    request: Request,
    id_avaliacao: int = Form(...),
    resposta: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    """
    Responder a uma avaliação recebida
    """
    assert usuario_logado is not None
    
    # Verificar se fornecedor existe
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    # Verificar se a avaliação existe e pertence a este fornecedor
    avaliacao = avaliacao_repo.obter_avaliacao_por_id(id_avaliacao)
    if not avaliacao or avaliacao.id_avaliado != usuario_logado["id"]:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
    
    # Por enquanto, apenas redirecionar de volta (resposta será armazenada em um campo separado)
    # Para implementação futura: salvar a resposta em um banco de dados
    
    return RedirectResponse(
        url="/fornecedor/avaliacoes/recebidas?resposta_enviada=1",
        status_code=303
    )
