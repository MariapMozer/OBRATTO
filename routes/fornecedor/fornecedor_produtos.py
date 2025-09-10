from fastapi import APIRouter, Request, Form, UploadFile, File
from utils.auth_decorator import requer_autenticacao
from fastapi.templating import Jinja2Templates

from data.produto.produto_model import Produto
from data.produto import produto_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


# Rota home do fornecedor
@router.get("/")
@requer_autenticacao(['fornecedor'])
async def home_adm(request: Request):
    produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
    return templates.TemplateResponse("fornecedor/home_teste.html", {"request": request, "produtos": produtos})


@router.get("/buscar")
@requer_autenticacao(['fornecedor'])
async def buscar_produto(request: Request, id: int = None, nome: str = None):
    produtos = []
    if id is not None:
        produto = produto_repo.obter_produto_por_id(id)
        if produto:
            produtos = [produto]
    elif nome:
        produtos = produto_repo.obter_produto_por_nome(nome)
    return templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos})

@router.get("/listar")
@requer_autenticacao(['fornecedor'])
async def listar_produtos(request: Request):
    produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
    response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos})
    return response

@router.get("/inserir")
@requer_autenticacao(['fornecedor'])
async def mostrar_formulario_produto(request: Request):
    response = templates.TemplateResponse("fornecedor/produtos/cadastrar_produtos.html", {"request": request})
    return response

@router.post("/inserir")
@requer_autenticacao(['fornecedor'])
async def cadastrar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    foto: UploadFile = File(...)
):
    import os
    pasta_fotos = "uploads/produtos/"
    os.makedirs(pasta_fotos, exist_ok=True)
    caminho_foto = None
    if foto:
        extensao = foto.filename.split(".")[-1]
        nome_arquivo = f"{nome.replace(' ', '_')}_{foto.filename}"
        caminho_foto = os.path.join(pasta_fotos, nome_arquivo)
        with open(caminho_foto, "wb") as buffer:
            buffer.write(await foto.read())
    produto = Produto(id=None, nome=nome, descricao=descricao, preco=preco, quantidade=quantidade, foto=caminho_foto)
    produto_repo.inserir_produto(produto)
    produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
    response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto inserido com sucesso"})
    return response

@router.get("/atualizar/{id}")
@requer_autenticacao(['fornecedor'])
async def mostrar_formulario_atualizar_produto(request: Request, id: int):
    produto = produto_repo.obter_produto_por_id(id)
    if produto:
        response = templates.TemplateResponse("fornecedor/produtos/alterar_produtos.html", {"request": request, "produto": produto})
    else:
        produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
        response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto não encontrado"})
    return response

@router.post("/atualizar/{id}")
@requer_autenticacao(['fornecedor'])
async def atualizar_produto(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    foto: UploadFile = File(None)
):
    import os
    produto = produto_repo.obter_produto_por_id(id)
    caminho_foto = produto.foto if produto else None
    if foto and foto.filename:
        # Apaga a foto antiga se existir
        if caminho_foto and os.path.exists(caminho_foto):
            try:
                os.remove(caminho_foto)
            except Exception:
                pass
        pasta_fotos = "uploads/produtos/"
        os.makedirs(pasta_fotos, exist_ok=True)
        nome_arquivo = f"{nome.replace(' ', '_')}_{foto.filename}"
        caminho_foto = os.path.join(pasta_fotos, nome_arquivo)
        with open(caminho_foto, "wb") as buffer:
            buffer.write(await foto.read())
    produto_atualizado = Produto(
        id=id,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        foto=caminho_foto
    )
    produto_repo.atualizar_produto(produto_atualizado)
    produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
    response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto atualizado com sucesso"})
    return response


@router.get("/excluir/{id}")
@requer_autenticacao(['fornecedor'])
async def excluir_produto_get(request: Request, id: int):
    produto = produto_repo.obter_produto_por_id(id)
    if produto:
        produto_repo.deletar_produto(id)
        produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
        response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto excluído com sucesso"})
    else:
        produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
        response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto não encontrado"})
    return response


@router.post("/excluir/{id}")
@requer_autenticacao(['fornecedor'])
async def excluir_produto(request: Request, id: int):
    produto = produto_repo.obter_produto_por_id(id)
    if produto:
        produto_repo.deletar_produto(id)
        produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
        response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto excluído com sucesso"})
    else:
        produtos = produto_repo.obter_produto_por_pagina(limit=10, offset=0)
        response = templates.TemplateResponse("fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos, "mensagem": "Produto não encontrado"})
    return response


@router.get("/confi_exclusao/{id}")
@requer_autenticacao(['fornecedor'])
async def confi_exclusao_produto(request: Request, id: int):
    produto = produto_repo.obter_produto_por_id(id)
    return templates.TemplateResponse("fornecedor/produtos/excluir_produtos.html", {"request": request, "produto": produto})
