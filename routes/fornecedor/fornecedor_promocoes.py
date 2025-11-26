from fastapi import APIRouter, Request
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from fastapi.responses import RedirectResponse
from data.produto.produto_repo import obter_produto_por_id, atualizar_produto
from data.produto.produto_model import Produto

router = APIRouter()
templates = criar_templates("templates")


# Rota para listar todas promoções
@router.get("/listar")
@requer_autenticacao(["fornecedor"])
async def listar_promocoes(request: Request):
    return templates.TemplateResponse(
        "fornecedor/promocao/promocoes.html", {"request": request}
    )


# Rota para cadastrar promoção
@router.get("/cadastrar")
@requer_autenticacao(["fornecedor"])
async def cadastrar_promocao(request: Request):
    return templates.TemplateResponse(
        "fornecedor/promocoes/cadastrar.html", {"request": request}
    )


# Rota para cadastrar promoção
@router.post("/cadastrar")
@requer_autenticacao(["fornecedor"])
async def cadastrar_promocao_post(request: Request):
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
        mensagem = f"Promoção cadastrada para o produto {produto.nome}!"
    else:
        mensagem = "Produto não encontrado."
    return templates.TemplateResponse(
        "fornecedor/promocoes/cadastrar.html",
        {"request": request, "mensagem": mensagem},
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
