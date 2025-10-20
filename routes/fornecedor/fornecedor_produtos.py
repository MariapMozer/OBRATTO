from typing import Optional
from fastapi import APIRouter, Request, Form, UploadFile, File, Query, status
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from util.flash_messages import informar_sucesso, informar_erro
import os

from data.produto.produto_model import Produto
from data.produto import produto_repo
from dtos.produto.produto_dto import CriarProdutoDTO, AlterarProdutoDTO

router = APIRouter()
templates = criar_templates("templates")


## Página inicial do fornecedor, exibe lista de produtos cadastrados
@router.get("/")
@requer_autenticacao(["fornecedor"])
async def home_adm(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    produtos = produto_repo.obter_produtos_por_fornecedor(
        usuario_logado["id"], limit=10, offset=0
    )
    return templates.TemplateResponse(
        "fornecedor/home_fornecedor.html", {"request": request, "produtos": produtos}
    )


@router.get("/buscar")
@requer_autenticacao(["fornecedor"])
async def buscar_produto(
    request: Request,
    id: str = Query("", description="ID do produto"),
    nome: str = Query("", description="Nome do produto"),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    produtos = []

    # Converter ID para int se não estiver vazio
    produto_id = None
    if id and id.strip():
        try:
            produto_id = int(id)
        except ValueError:
            produto_id = None

    if produto_id is not None:
        produto = produto_repo.obter_produto_por_id(produto_id)
        if produto and produto.fornecedor_id == usuario_logado["id"]:
            produtos = [produto]
    elif nome and nome.strip():
        # Buscar apenas produtos do fornecedor logado
        todos_produtos = produto_repo.obter_produtos_por_fornecedor(
            usuario_logado["id"], limit=100, offset=0
        )
        produtos = [p for p in todos_produtos if nome.lower() in p.nome.lower()]

    return templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos}
    )


@router.get("/listar")
@requer_autenticacao(["fornecedor"])
async def listar_produtos(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    produtos = produto_repo.obter_produtos_por_fornecedor(
        usuario_logado["id"], limit=10, offset=0
    )
    response = templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", {"request": request, "produtos": produtos}
    )
    return response


@router.get("/inserir")
@requer_autenticacao(["fornecedor"])
async def mostrar_formulario_produto(request: Request):
    response = templates.TemplateResponse(
        "fornecedor/produtos/cadastrar_produtos.html", {"request": request}
    )
    return response


@router.post("/inserir")
@requer_autenticacao(["fornecedor"])
async def cadastrar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None

    try:
        # Validar com DTO
        dto = CriarProdutoDTO(
            nome=nome, descricao=descricao, preco=preco, quantidade=quantidade
        )

        # Upload de foto
        import secrets

        tipos_permitidos = [
            "image/jpeg",
            "image/png",
            "image/jpg",
            "image/webp",
            "image/avif",
        ]
        pasta_fotos = "static/uploads/produtos_fornecedor"
        os.makedirs(pasta_fotos, exist_ok=True)
        caminho_foto = None

        if foto and foto.filename:
            if foto.content_type not in tipos_permitidos:
                informar_erro(
                    request, "Tipo de arquivo de foto inválido. Use JPG, PNG ou WEBP."
                )
                return templates.TemplateResponse(
                    "fornecedor/produtos/cadastrar_produtos.html",
                    {
                        "request": request,
                        "dados": {"nome": nome, "descricao": descricao},
                    },
                )

            extensao = foto.filename.split(".")[-1]
            nome_arquivo = (
                f"{dto.nome.replace(' ', '_')}_{secrets.token_hex(8)}.{extensao}"
            )
            caminho_arquivo = os.path.join(pasta_fotos, nome_arquivo)
            conteudo = await foto.read()
            with open(caminho_arquivo, "wb") as f:
                f.write(conteudo)
            caminho_foto = f"/static/uploads/produtos_fornecedor/{nome_arquivo}"

        # Criar produto
        produto = Produto(
            id=None,
            nome=dto.nome,
            descricao=dto.descricao,
            preco=dto.preco,
            quantidade=dto.quantidade,
            foto=caminho_foto,
            fornecedor_id=usuario_logado["id"],
        )

        # Inserir no banco
        produto_repo.inserir_produto(produto)

        # Flash message e redirect
        informar_sucesso(request, f"Produto '{dto.nome}' cadastrado com sucesso!")
        return RedirectResponse(
            "/fornecedor/produtos/listar", status_code=status.HTTP_303_SEE_OTHER
        )

    except ValidationError as e:
        erros = [erro["msg"] for erro in e.errors()]
        informar_erro(request, " | ".join(erros))
        return templates.TemplateResponse(
            "fornecedor/produtos/cadastrar_produtos.html",
            {"request": request, "dados": {"nome": nome, "descricao": descricao}},
        )
    except Exception as e:
        informar_erro(request, f"Erro ao cadastrar produto: {str(e)}")
        return templates.TemplateResponse(
            "fornecedor/produtos/cadastrar_produtos.html",
            {"request": request, "dados": {"nome": nome, "descricao": descricao}},
        )


@router.get("/atualizar/{id}")
@requer_autenticacao(["fornecedor"])
async def mostrar_formulario_atualizar_produto(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado["id"]:
        response = templates.TemplateResponse(
            "fornecedor/produtos/alterar_produtos.html",
            {"request": request, "produto": produto},
        )
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(
            usuario_logado["id"], limit=10, offset=0
        )
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html",
            {
                "request": request,
                "produtos": produtos,
                "mensagem": "Produto não encontrado ou acesso negado",
            },
        )
    return response


@router.post("/atualizar/{id}")
@requer_autenticacao(["fornecedor"])
async def atualizar_produto(
    request: Request,
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    foto: UploadFile = File(None),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    produto = produto_repo.obter_produto_por_id(id)
    if not produto or produto.fornecedor_id != usuario_logado["id"]:
        produtos = produto_repo.obter_produtos_por_fornecedor(
            usuario_logado["id"], limit=10, offset=0
        )
        return templates.TemplateResponse(
            "fornecedor/produtos/produtos.html",
            {
                "request": request,
                "produtos": produtos,
                "mensagem": "Produto não encontrado ou acesso negado",
            },
        )
    caminho_foto = produto.foto
    import os

    if foto and foto.filename:
        # Apaga a foto antiga se existir
        if caminho_foto:
            apagar_arquivo_imagem(caminho_foto)

        pasta_fotos = "static/uploads/produtos_fornecedor"
        os.makedirs(pasta_fotos, exist_ok=True)
        import secrets

        extensao = foto.filename.split(".")[-1]
        nome_arquivo = f"{nome.replace(' ', '_')}_{secrets.token_hex(8)}.{extensao}"
        caminho_arquivo = os.path.join(pasta_fotos, nome_arquivo)
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)
        caminho_foto = f"/static/uploads/produtos_fornecedor/{nome_arquivo}"
    produto_atualizado = Produto(
        id=id,
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade=quantidade,
        foto=caminho_foto,
        fornecedor_id=usuario_logado["id"],
    )
    produto_repo.atualizar_produto(produto_atualizado)
    produtos = produto_repo.obter_produtos_por_fornecedor(
        usuario_logado["id"], limit=10, offset=0
    )
    response = templates.TemplateResponse(
        "fornecedor/produtos/produtos.html",
        {
            "request": request,
            "produtos": produtos,
            "mensagem": "Produto atualizado com sucesso",
        },
    )
    return response


@router.get("/excluir/{id}")
@requer_autenticacao(["fornecedor"])
async def excluir_produto_get(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado["id"]:
        # Apagar a imagem do sistema de arquivos
        if produto.foto:
            apagar_arquivo_imagem(produto.foto)

        # Apagar produto do banco
        produto_repo.deletar_produto(id)

        # Flash message e redirect
        informar_sucesso(request, f"Produto '{produto.nome}' excluído com sucesso!")
        return RedirectResponse(
            "/fornecedor/produtos/listar", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        informar_erro(request, "Produto não encontrado ou acesso negado")
        return RedirectResponse(
            "/fornecedor/produtos/listar", status_code=status.HTTP_303_SEE_OTHER
        )


@router.post("/excluir/{id}")
@requer_autenticacao(["fornecedor"])
async def excluir_produto(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado["id"]:
        # Apagar a imagem do sistema de arquivos
        if produto.foto:
            apagar_arquivo_imagem(produto.foto)

        # Apagar produto do banco
        produto_repo.deletar_produto(id)

        # Flash message e redirect
        informar_sucesso(request, f"Produto '{produto.nome}' excluído com sucesso!")
        return RedirectResponse(
            "/fornecedor/produtos/listar", status_code=status.HTTP_303_SEE_OTHER
        )
    else:
        informar_erro(request, "Produto não encontrado ou acesso negado")
        return RedirectResponse(
            "/fornecedor/produtos/listar", status_code=status.HTTP_303_SEE_OTHER
        )


@router.get("/confi_exclusao/{id}")
@requer_autenticacao(["fornecedor"])
async def confi_exclusao_produto(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado["id"]:
        return templates.TemplateResponse(
            "fornecedor/produtos/excluir_produtos.html",
            {"request": request, "produto": produto},
        )
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(
            usuario_logado["id"], limit=10, offset=0
        )
        return templates.TemplateResponse(
            "fornecedor/produtos/produtos.html",
            {
                "request": request,
                "produtos": produtos,
                "mensagem": "Produto não encontrado ou acesso negado",
            },
        )


def apagar_arquivo_imagem(caminho_foto: str):
    """Remove o arquivo de imagem do sistema de arquivos se existir"""
    if caminho_foto:
        # Remover a barra inicial para construir o caminho correto
        if caminho_foto.startswith("/"):
            caminho_foto = caminho_foto[1:]

        caminho_completo = os.path.join(os.getcwd(), caminho_foto)

        try:
            if os.path.exists(caminho_completo):
                os.remove(caminho_completo)
                print(f"Imagem removida: {caminho_completo}")
            else:
                print(f"Arquivo não encontrado: {caminho_completo}")
        except Exception as e:
            print(f"Erro ao remover imagem {caminho_completo}: {e}")
