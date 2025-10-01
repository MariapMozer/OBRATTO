from fastapi import APIRouter, Request, Form, UploadFile, File
from utils.auth_decorator import requer_autenticacao
from fastapi.templating import Jinja2Templates

from data.produto.produto_model import Produto
from data.produto import produto_repo

router = APIRouter()
templates = Jinja2Templates(directory="templates")


## Página inicial do fornecedor, exibe lista de produtos cadastrados
@router.get("/")
@requer_autenticacao(['fornecedor'])
async def home_adm(request: Request, usuario_logado: dict = None):
    produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
    return templates.TemplateResponse(
        "fornecedor/home_fornecedor.html", 
        {"request": request, 
        "produtos": produtos})

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
    return templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", 
        {"request": request, 
         "produtos": produtos})

@router.get("/listar")
@requer_autenticacao(['fornecedor'])
async def listar_produtos(request: Request, usuario_logado: dict = None):
    produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
    response = templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", 
        {"request": request, 
         "produtos": produtos})
    return response

@router.get("/inserir")
@requer_autenticacao(['fornecedor'])
async def mostrar_formulario_produto(request: Request):
    response = templates.TemplateResponse(
        "fornecedor/produtos/cadastrar_produtos.html", 
        {"request": request})
    return response

@router.post("/inserir")
@requer_autenticacao(['fornecedor'])
async def cadastrar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade: int = Form(...),
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    print(f"DEBUG: Iniciando cadastro de produto")
    print(f"DEBUG: Nome: {nome}, Preço: {preco}, Quantidade: {quantidade}")
    print(f"DEBUG: Usuario logado ID: {usuario_logado['id']}")
    
    import os
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    pasta_fotos = "static/uploads/produtos_fornecedor"
    os.makedirs(pasta_fotos, exist_ok=True)
    caminho_foto = None
    if foto and foto.filename:
        print(f"DEBUG: Processando foto: {foto.filename}")
        print(f"DEBUG: Content type: {foto.content_type}")
        if foto.content_type not in tipos_permitidos:
            print(f"DEBUG: Tipo de arquivo inválido: {foto.content_type}")
            return templates.TemplateResponse(
                "fornecedor/produtos/cadastrar_produtos.html",
                {"request": request, "erro": "Tipo de arquivo de foto inválido."}
            )
        print(f"DEBUG: Tipo de arquivo válido, processando...")
        import secrets
        extensao = foto.filename.split(".")[-1]
        print(f"DEBUG: Extensão extraída: {extensao}")
        nome_arquivo = f"{nome.replace(' ', '_')}_{secrets.token_hex(8)}.{extensao}"
        print(f"DEBUG: Nome do arquivo: {nome_arquivo}")
        caminho_arquivo = os.path.join(pasta_fotos, nome_arquivo)
        print(f"DEBUG: Caminho completo: {caminho_arquivo}")
        
        try:
            conteudo = await foto.read()
            print(f"DEBUG: Conteúdo lido, tamanho: {len(conteudo)} bytes")
            with open(caminho_arquivo, "wb") as f:
                f.write(conteudo)
            print(f"DEBUG: Arquivo salvo com sucesso")
            caminho_foto = f"/static/uploads/produtos_fornecedor/{nome_arquivo}"
            print(f"DEBUG: Foto salva em: {caminho_foto}")
        except Exception as e:
            print(f"DEBUG: Erro ao salvar foto: {e}")
            import traceback
            traceback.print_exc()
            return templates.TemplateResponse(
                "fornecedor/produtos/cadastrar_produtos.html",
                {"request": request, "erro": f"Erro ao salvar foto: {e}"}
            )
    
    print(f"DEBUG: Processamento de foto concluído. Caminho: {caminho_foto}")
    print(f"DEBUG: Criando objeto Produto...")
    
    produto = Produto(
        id=None, 
        nome=nome, 
        descricao=descricao, 
        preco=preco, 
        quantidade=quantidade, 
        foto=caminho_foto,
        fornecedor_id=usuario_logado['id']
    )
    print(f"DEBUG: Produto criado: {produto}")
    
    try:
        print(f"DEBUG: Chamando produto_repo.inserir_produto...")
        produto_repo.inserir_produto(produto)
        print(f"DEBUG: Produto inserido com sucesso")
    except Exception as e:
        print(f"DEBUG: Erro ao inserir produto: {e}")
        import traceback
        traceback.print_exc()
        return templates.TemplateResponse(
            "fornecedor/produtos/cadastrar_produtos.html",
            {"request": request, "erro": f"Erro ao cadastrar produto: {e}"}
        )
    
    print(f"DEBUG: Buscando produtos do fornecedor...")
    produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
    print(f"DEBUG: Encontrados {len(produtos)} produtos")
    response = templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", 
        {"request": request, 
         "produtos": produtos, 
         "mensagem": "Produto inserido com sucesso"})
    print(f"DEBUG: Retornando resposta...")
    return response

@router.get("/atualizar")
@requer_autenticacao(['fornecedor'])
async def mostrar_formulario_atualizar_produto(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado['id']:
        response = templates.TemplateResponse(
            "fornecedor/produtos/alterar_produtos.html", 
            {"request": request, 
             "produto": produto})
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
             "produtos": produtos, 
             "mensagem": "Produto não encontrado ou acesso negado"})
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
    foto: UploadFile = File(None),
    usuario_logado: dict = None
):
    produto = produto_repo.obter_produto_por_id(id)
    if not produto or produto.fornecedor_id != usuario_logado['id']:
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        return templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
             "produtos": produtos, 
             "mensagem": "Produto não encontrado ou acesso negado"})
    caminho_foto = produto.foto
    import os
    if foto and foto.filename:
        # Apaga a foto antiga se existir
        if caminho_foto and os.path.exists(caminho_foto):
            try:
                os.remove(caminho_foto)
            except Exception:
                pass
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
        fornecedor_id=usuario_logado['id']
    )
    produto_repo.atualizar_produto(produto_atualizado)
    produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
    response = templates.TemplateResponse(
        "fornecedor/produtos/produtos.html", 
        {"request": request, 
         "produtos": produtos, 
         "mensagem": "Produto atualizado com sucesso"})
    return response

@router.get("/excluir/{id}")
@requer_autenticacao(['fornecedor'])
async def excluir_produto_get(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado['id']:
        produto_repo.deletar_produto(id)
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
            "produtos": produtos, 
            "mensagem": "Produto excluído com sucesso"})
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
             "produtos": produtos, 
             "mensagem": "Produto não encontrado ou acesso negado"})
    return response

@router.post("/excluir/{id}")
@requer_autenticacao(['fornecedor'])
async def excluir_produto(request: Request, id: int, usuario_logado: dict = None):
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado['id']:
        produto_repo.deletar_produto(id)
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
            "produtos": produtos, 
            "mensagem": "Produto excluído com sucesso"})
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        response = templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
             "produtos": produtos, 
             "mensagem": "Produto não encontrado ou acesso negado"})
    return response

@router.get("/confi_exclusao/{id}")
@requer_autenticacao(['fornecedor'])
async def confi_exclusao_produto(request: Request, id: int,  usuario_logado: dict = None):
    produto = produto_repo.obter_produto_por_id(id)
    if produto and produto.fornecedor_id == usuario_logado['id']:
        return templates.TemplateResponse(
            "fornecedor/produtos/excluir_produtos.html", 
            {"request": request, 
             "produto": produto})
    else:
        produtos = produto_repo.obter_produtos_por_fornecedor(usuario_logado['id'], limit=10, offset=0)
        return templates.TemplateResponse(
            "fornecedor/produtos/produtos.html", 
            {"request": request, 
             "produtos": produtos,
               "mensagem": "Produto não encontrado ou acesso negado"})
