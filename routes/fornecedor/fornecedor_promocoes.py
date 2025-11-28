from fastapi import APIRouter, Request, HTTPException
from typing import Optional
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from fastapi.responses import RedirectResponse
from data.produto.produto_repo import obter_produto_por_id, atualizar_produto, obter_produtos
from data.produto.produto_model import Produto

router = APIRouter(prefix="/promocoes")
templates = criar_templates("templates")


# Rota para listar todas promoções
@router.get("/listar")
@requer_autenticacao(["fornecedor"])
async def listar_promocoes(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    
    # Obter todos os produtos
    produtos = obter_produtos()
    
    # Filtrar produtos em promoção do fornecedor
    promocoes = [p for p in produtos if p.em_promocao and p.fornecedor_id == usuario_logado.get("id")]
    
    return templates.TemplateResponse(
        "fornecedor/promocao/promocoes.html", 
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "promocoes": promocoes
        }
    )


# Rota para cadastrar promoção
@router.get("/cadastrar")
@requer_autenticacao(["fornecedor"])
async def cadastrar_promocao(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    
    # Obter produtos do fornecedor
    produtos = obter_produtos()
    
    # Filtrar apenas produtos do fornecedor logado
    produtos_fornecedor = [p for p in produtos if p.fornecedor_id == usuario_logado.get("id")]
    
    return templates.TemplateResponse(
        "fornecedor/promocao/cadastrar_promocoes.html", 
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "produtos": produtos_fornecedor
        }
    )


# Rota para cadastrar promoção
@router.post("/cadastrar")
@requer_autenticacao(["fornecedor"])
async def cadastrar_promocao_post(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    
    dados = await request.form()
    id_produto_raw = dados.get("id_produto")
    if isinstance(id_produto_raw, str):
        id_produto = int(id_produto_raw)
    else:
        id_produto = 0
    
    desconto_raw = dados.get("desconto", "0")
    if isinstance(desconto_raw, str):
        desconto = float(desconto_raw)
    else:
        desconto = 0.0
    
    # Validar desconto
    if desconto < 0 or desconto > 100:
        return RedirectResponse(
            "/fornecedor/promocoes/cadastrar?erro=desconto_invalido",
            status_code=303
        )
    
    produto = obter_produto_por_id(id_produto)
    if produto and produto.fornecedor_id == usuario_logado.get("id"):
        produto.em_promocao = True
        produto.desconto = desconto
        atualizar_produto(produto)
        
        return RedirectResponse(
            f"/fornecedor/promocoes/listar?sucesso=promocao_criada&produto={produto.nome}",
            status_code=303
        )
    else:
        return RedirectResponse(
            "/fornecedor/promocoes/cadastrar?erro=produto_nao_encontrado",
            status_code=303
        )


# Rota para alterar promoção
@router.get("/alterar")
@requer_autenticacao(["fornecedor"])
async def alterar_promocao(request: Request):
    return templates.TemplateResponse(
        "fornecedor/promocoes/alterar.html", {"request": request}
    )


# Rota para alterar promoção
@router.post("/alterar")
@requer_autenticacao(["fornecedor"])
async def alterar_promocao_post(request: Request):
    dados = await request.form()
    id_produto_raw = dados.get("id_produto")
    if isinstance(id_produto_raw, str):
        id_produto = int(id_produto_raw)
    else:
        id_produto = 0
    desconto_raw = dados.get("desconto", "0")
    if isinstance(desconto_raw, str):
        desconto = float(desconto_raw)
    else:
        desconto = 0.0
    produto = obter_produto_por_id(id_produto)
    if produto:
        produto.em_promocao = True
        produto.desconto = desconto
        atualizar_produto(produto)
        mensagem = f"Promoção alterada para o produto {produto.nome}!"
    else:
        mensagem = "Produto não encontrado."
    return templates.TemplateResponse(
        "fornecedor/promocoes/alterar.html",
        {"request": request, "mensagem": mensagem},
    )


@router.post("/excluir")
@requer_autenticacao(["fornecedor"])
async def excluir_promocao_post(request: Request):
    dados = await request.form()
    id_promocao = dados.get("id")
    return RedirectResponse(
        url=f"/fornecedor/promocoes/confirmar_exclusao?id={id_promocao}",
        status_code=303,
    )


# Rota para confirmar exclusão de promoção
@router.get("/confirmar_exclusao")
@requer_autenticacao(["fornecedor"])
async def confirmar_exclusao_promocao(request: Request):
    id_promocao = request.query_params.get("id")
    produto = None
    if id_promocao:
        try:
            produto = obter_produto_por_id(int(id_promocao))
        except Exception:
            produto = None
    return templates.TemplateResponse(
        "fornecedor/promocoes/confirmar_exclusao.html",
        {"request": request, "id": id_promocao, "produto": produto},
    )


# Rota para confirmar exclusão de promoção
@router.post("/confirmar_exclusao")
@requer_autenticacao(["fornecedor"])
async def confirmar_exclusao_promocao_post(request: Request):
    dados = await request.form()
    id_produto_raw = dados.get("id_produto")
    if isinstance(id_produto_raw, str):
        id_produto = int(id_produto_raw)
    else:
        id_produto = 0
    produto = obter_produto_por_id(id_produto)
    if produto:
        produto.em_promocao = False
        produto.desconto = 0.0
        atualizar_produto(produto)
        mensagem = (
            f"Promoção removida do produto {produto.nome}. O preço voltou ao normal."
        )
    else:
        mensagem = "Produto não encontrado."
    return templates.TemplateResponse(
        "fornecedor/promocoes/confirmar_exclusao.html",
        {"request": request, "mensagem": mensagem},
    )
