from fastapi import APIRouter, Request, Form, Depends, File, UploadFile, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from pydantic import ValidationError
from datetime import datetime
from typing import Optional
import logging

from data.administrador import administrador_repo
from data.administrador.administrador_model import Administrador
from data.fornecedor import fornecedor_repo
from data.prestador import prestador_repo
from data.cliente import cliente_repo
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from dtos.Administrador.administrador_dto import (
    CriarAdministradorDTO,
    AtualizarAdministradorDTO,
)
from util.auth_decorator import requer_autenticacao
from util.security import criar_hash_senha

# Configurar logger
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")
administrador_usuarios = APIRouter()


@router.get("/home")
@requer_autenticacao(["administrador"])
async def get_home_adm(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "administrador/home_adm.html", {"request": request}
    )


# Rota para exibir o formulário de cadastro do administrador
@router.get("/cadastro")
@requer_autenticacao(["administrador"])
async def exibir_cadastro_administrador(
    request: Request, usuario_logado: Optional[dict] = None
):
    return templates.TemplateResponse(
        "administrador/moderar_adm/cadastrar_adm.html", {"request": request}
    )


# Rota para cadastrar um novo administrador
@router.post("/cadastro")
@requer_autenticacao(["administrador"])
async def cadastrar_administrador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    telefone: str = Form(...),
    cep: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    complemento: str = Form(""),
    usuario_logado: Optional[dict] = None,
):
    logger.info(f"Iniciando cadastro de administrador. Email: {email}")

    # Preservar dados do formulário (exceto senhas por segurança)
    dados_formulario = {
        "nome": nome,
        "email": email,
        "cpf_cnpj": cpf_cnpj,
        "telefone": telefone,
        "cep": cep,
        "estado": estado,
        "cidade": cidade,
        "rua": rua,
        "numero": numero,
        "bairro": bairro,
        "complemento": complemento,
    }

    try:
        # Validar dados com Pydantic DTO
        admin_dto = CriarAdministradorDTO(
            nome=nome,
            email=email,
            senha=senha,
            confirmar_senha=confirmar_senha,
            cpf_cnpj=cpf_cnpj,
            telefone=telefone,
            cep=cep,
            estado=estado,
            cidade=cidade,
            rua=rua,
            numero=numero,
            bairro=bairro,
            complemento=complemento or "",
            tipo_usuario="administrador",
        )

        # Verificar se email já existe
        usuario_existente = usuario_repo.obter_usuario_por_email(admin_dto.email)
        logger.info(
            f"Verificação de email: {admin_dto.email} - Existente: {usuario_existente is not None}"
        )

        if usuario_existente:
            logger.warning(f"Email já cadastrado: {admin_dto.email}")
            return templates.TemplateResponse(
                "administrador/moderar_adm/cadastrar_adm.html",
                {
                    "request": request,
                    "erro": "Email já cadastrado no sistema.",
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Criar hash da senha (usar senha validada)
        senha_hash = criar_hash_senha(admin_dto.senha)

        # Criar objeto Usuario
        usuario = Usuario(
            id=0,  # Will be set by database auto-increment
            nome=admin_dto.nome,
            email=admin_dto.email,
            senha=senha_hash,
            cpf_cnpj=admin_dto.cpf_cnpj,
            telefone=admin_dto.telefone,
            cep=admin_dto.cep,
            rua=admin_dto.rua,
            numero=admin_dto.numero,
            complemento=admin_dto.complemento or "",
            bairro=admin_dto.bairro,
            cidade=admin_dto.cidade,
            estado=admin_dto.estado,
            tipo_usuario="Administrador",
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=None,
            token_redefinicao=None,
            data_token=None,
        )

        # Inserir usuário no banco
        id_usuario = usuario_repo.inserir_usuario(usuario)
        logger.info(
            f"Usuário criado com ID: {id_usuario}, tipo_usuario: {usuario.tipo_usuario}"
        )

        if not id_usuario:
            return templates.TemplateResponse(
                "administrador/moderar_adm/cadastrar_adm.html",
                {
                    "request": request,
                    "erro": "Erro ao criar usuário. Tente novamente.",
                    "dados": dados_formulario,
                },
            )

        # Criar registro na tabela administrador
        administrador = Administrador(id=None, id_usuario=id_usuario)
        admin_id = administrador_repo.inserir_administrador(administrador)

        if not admin_id:
            # Se falhar, remover usuário criado (rollback manual)
            usuario_repo.deletar_usuario(id_usuario)
            return templates.TemplateResponse(
                "administrador/moderar_adm/cadastrar_adm.html",
                {
                    "request": request,
                    "erro": "Erro ao criar administrador. Tente novamente.",
                    "dados": dados_formulario,
                },
            )

        # Sucesso - Registrar log
        assert usuario_logado is not None
        logger.info(
            f"Novo administrador criado: {admin_dto.email} por {usuario_logado.get('email', 'desconhecido')}"
        )

        # Redirecionar com mensagem de sucesso
        return templates.TemplateResponse(
            "administrador/moderar_adm/cadastrar_adm.html",
            {
                "request": request,
                "sucesso": f"Administrador {admin_dto.nome} cadastrado com sucesso!",
                "dados": None,  # Limpar formulário
            },
        )

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        campos_erro: dict[str, list[str]] = {}

        for erro in e.errors():
            loc_tuple = erro.get("loc")
            campo = str(loc_tuple[0]) if loc_tuple and len(loc_tuple) > 0 else "campo"
            mensagem = erro.get("msg", "")
            campo_str = (
                str(campo).capitalize() if isinstance(campo, (str, int)) else "campo"
            )
            texto = f"{campo_str}: {mensagem}"
            erros.append(texto)
            campos_erro.setdefault(campo, []).append(mensagem)

        erro_msg = " | ".join(erros)
        logger.warning(f"Erro de validação no cadastro de administrador: {erro_msg}")

        # Retornar template com dados preservados e erros
        return templates.TemplateResponse(
            "administrador/moderar_adm/cadastrar_adm.html",
            {
                "request": request,
                "erro": erro_msg,
                "erros_list": erros,
                "campos_erro": campos_erro,
                "dados": dados_formulario,
            },
        )

    except Exception as e:
        import traceback

        logger.error(f"Erro ao processar cadastro de administrador: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")

        return templates.TemplateResponse(
            "administrador/moderar_adm/cadastrar_adm.html",
            {
                "request": request,
                "erro": "Erro ao processar cadastro. Tente novamente.",
                "dados": dados_formulario,
            },
        )


@router.get("/lista")
@requer_autenticacao(["administrador"])
async def get_lista_adm(request: Request, usuario_logado: Optional[dict] = None):
    return templates.TemplateResponse(
        "administrador/moderar_adm/lista_adm.html", {"request": request}
    )


@router.post("/editar_administrador")
@requer_autenticacao(["administrador"])
async def post_editar_adm(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    # TODO: Implement proper update logic - atualizar_administrador expects Administrador object
    # For now, update via usuario_repo
    usuario = usuario_repo.obter_usuario_por_id(id)
    if usuario:
        usuario.nome = nome
        usuario.email = email
        if senha:
            from util.security import criar_hash_senha

            usuario.senha = criar_hash_senha(senha)
        usuario_repo.atualizar_usuario(usuario)
    return templates.TemplateResponse(
        "administrador/moderar_adm/editar_adm.html", {"request": request}
    )


@router.post("/excluir_administrador")
@requer_autenticacao(["administrador"])
async def post_excluir_adm(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    administrador_repo.deletar_administrador(id)
    return templates.TemplateResponse(
        "administrador/moderar_adm/remover_adm.html", {"request": request}
    )


# buscar administrador por id
@router.get("/id/{id}")
@requer_autenticacao(["administrador"])
async def get_administrador(request: Request, id: int, usuario_logado: Optional[dict] = None):
    administrador = administrador_repo.obter_administrador_por_id(id)
    return templates.TemplateResponse(
        "administrador.html", {"request": request, "administrador": administrador}
    )


# Moderar prestadores
@router.get("/listar_prestador")
@requer_autenticacao(["administrador"])
async def get_listar_prestador(request: Request, usuario_logado: Optional[dict] = None):
    prestadores = prestador_repo.obter_prestador()
    return templates.TemplateResponse(
        "administrador/listar_prestador.html",
        {"request": request, "prestadores": prestadores},
    )


@router.post("/editar_prestador")
@requer_autenticacao(["administrador"])
async def post_editar_prestador(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    # Update via usuario_repo
    usuario = usuario_repo.obter_usuario_por_id(id)
    if usuario:
        usuario.nome = nome
        usuario.email = email
        usuario_repo.atualizar_usuario(usuario)
    return templates.TemplateResponse(
        "administrador/listar_prestador.html", {"request": request}
    )


@router.post("/excluir_prestador")
@requer_autenticacao(["administrador"])
async def post_excluir_prestador(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    prestador_repo.deletar_prestador_repo(id)
    return templates.TemplateResponse(
        "administrador/listar_prestador.html", {"request": request}
    )


# Rota dinâmica para buscar prestador por id
@router.get("/prestador/{id}")
@requer_autenticacao(["administrador"])
async def get_prestador_por_id(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    prestador = prestador_repo.obter_prestador_por_id(id)
    return templates.TemplateResponse(
        "administrador/detalhes_prestador.html",
        {"request": request, "prestador": prestador},
    )


# Moderar Fornecedores
@router.get("/listar_fornecedor")
@requer_autenticacao(["administrador"])
async def get_listar_fornecedor(
    request: Request, usuario_logado: Optional[dict] = None
):
    fornecedores = fornecedor_repo.obter_fornecedor()
    return templates.TemplateResponse(
        "administrador/listar_fornecedor.html",
        {"request": request, "fornecedores": fornecedores},
    )


@router.post("/editar_fornecedor")
@requer_autenticacao(["administrador"])
async def post_editar_fornecedor(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    # Update via usuario_repo
    usuario = usuario_repo.obter_usuario_por_id(id)
    if usuario:
        usuario.nome = nome
        usuario.email = email
        usuario_repo.atualizar_usuario(usuario)
    return templates.TemplateResponse(
        "administrador/listar_fornecedor.html", {"request": request}
    )


@router.post("/excluir_fornecedor")
@requer_autenticacao(["administrador"])
async def post_excluir_fornecedor(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    fornecedor_repo.deletar_fornecedor(id)
    return templates.TemplateResponse(
        "administrador/listar_fornecedor.html", {"request": request}
    )


# Rota dinâmica para buscar fornecedor por id


@router.get("/fornecedor/{id}")
@requer_autenticacao(["administrador"])
async def get_fornecedor_por_id(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(id)
    return templates.TemplateResponse(
        "administrador/detalhes_fornecedor.html",
        {"request": request, "fornecedor": fornecedor},
    )


# Moderar Clientes


@router.get("/listar_cliente")
@requer_autenticacao(["administrador"])
async def get_listar_cliente(request: Request, usuario_logado: Optional[dict] = None):
    clientes = cliente_repo.obter_cliente()
    return templates.TemplateResponse(
        "administrador/listar_cliente.html", {"request": request, "clientes": clientes}
    )


@router.post("/editar_cliente")
@requer_autenticacao(["administrador"])
async def post_editar_cliente(
    request: Request,
    id: int = Form(...),
    nome: str = Form(...),
    email: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    # Update via usuario_repo
    usuario = usuario_repo.obter_usuario_por_id(id)
    if usuario:
        usuario.nome = nome
        usuario.email = email
        usuario_repo.atualizar_usuario(usuario)
    return templates.TemplateResponse(
        "administrador/listar_cliente.html", {"request": request}
    )


@router.post("/excluir_cliente")
@requer_autenticacao(["administrador"])
async def post_excluir_cliente(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    cliente_repo.deletar_cliente(id)
    return templates.TemplateResponse(
        "administrador/listar_cliente.html", {"request": request}
    )


# Rota dinâmica para buscar cliente por id
@router.get("/cliente/{id}")
@requer_autenticacao(["administrador"])
async def get_cliente_por_id(
    request: Request, id: int, usuario_logado: Optional[dict] = None
):
    cliente = cliente_repo.obter_cliente_por_id(id)
    return templates.TemplateResponse(
        "administrador/detalhes_cliente.html", {"request": request, "cliente": cliente}
    )


# Rota para listar todos os usuários aguardando verificação de selo
@router.get("/verificacao_selo")
@requer_autenticacao(["administrador"])
async def listar_usuarios_aguardando_selo(
    request: Request, usuario_logado: Optional[dict] = None
):
    fornecedores = [
        f
        for f in fornecedor_repo.obter_fornecedor()
        if not getattr(f, "selo_confianca", False)
    ]
    prestadores = []
    try:
        prestadores = [
            p
            for p in prestador_repo.obter_prestador()
            if not getattr(p, "selo_confianca", False)
        ]
    except Exception:
        pass

    return templates.TemplateResponse(
        "administrador/verificacao_usuario.html",
        {"request": request, "fornecedores": fornecedores, "prestadores": prestadores},
    )


@router.post("/aprovar_selo_fornecedor")
@requer_autenticacao(["administrador"])
async def aprovar_selo_fornecedor(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(id)
    if fornecedor:
        fornecedor.selo_confianca = True
        fornecedor_repo.atualizar_fornecedor(fornecedor)
    return RedirectResponse("/administrador/verificacao_selo", status_code=303)


# Aprovar selo de confiança para prestador
@router.post("/aprovar_selo_prestador")
@requer_autenticacao(["administrador"])
async def aprovar_selo_prestador(
    request: Request, id: int = Form(...), usuario_logado: Optional[dict] = None
):
    prestador = prestador_repo.obter_prestador_por_id(id)
    if prestador:
        prestador.selo_confianca = True
        prestador_repo.atualizar_prestador(prestador)
    return RedirectResponse("/administrador/verificacao_selo", status_code=303)


# Rota para exibir formulário de edição do próprio perfil do administrador
@router.get("/perfil/editar")
@requer_autenticacao(["administrador"])
async def get_editar_perfil_administrador(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    adm = administrador_repo.obter_administrador_por_id(usuario_logado["id"])
    return templates.TemplateResponse(
        "administrador/perfil_editar.html", {"request": request, "administrador": adm}
    )


# Rota para processar edição do próprio perfil do administrador
@router.post("/perfil/editar")
@requer_autenticacao(["administrador"])
async def post_editar_perfil_administrador(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha_atual: str = Form(...),
    senha_nova: str = Form(None),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    adm = administrador_repo.obter_administrador_por_id(usuario_logado["id"])
    from util.security import verificar_senha, criar_hash_senha

    # Verifica senha atual
    if adm is None:
        return templates.TemplateResponse(
            "administrador/perfil_editar.html",
            {"request": request, "erro": "Administrador não encontrado."},
        )

    if not verificar_senha(senha_atual, adm.senha):
        return templates.TemplateResponse(
            "administrador/perfil_editar.html",
            {
                "request": request,
                "administrador": adm,
                "erro": "Senha atual incorreta.",
            },
        )

    # Atualiza dados básicos via usuario_repo
    adm.nome = nome
    adm.email = email

    # Atualiza senha se fornecida
    if senha_nova and senha_nova.strip():
        adm.senha = criar_hash_senha(senha_nova)

    # Update user via usuario_repo
    usuario_repo.atualizar_usuario(adm)

    # Atualiza sessão
    usuario_logado["nome"] = nome
    usuario_logado["email"] = email
    from util.auth_decorator import criar_sessao

    criar_sessao(request, usuario_logado)
    return templates.TemplateResponse(
        "administrador/perfil_editar.html",
        {
            "request": request,
            "administrador": adm,
            "sucesso": "Perfil atualizado com sucesso!",
        },
    )


# Upload/atualização de foto de perfil do administrador
@router.post("/perfil/foto")
@requer_autenticacao(["administrador"])
async def upload_foto_perfil_administrador(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None,
):
    import os

    assert usuario_logado is not None

    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        return RedirectResponse(
            "/administrador/perfil?erro=tipo_invalido", status_code=303
        )

    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/administradores"
    os.makedirs(upload_dir, exist_ok=True)

    # Gerar nome único para o arquivo
    import secrets

    if foto.filename is None:
        return RedirectResponse(
            "/administrador/perfil?erro=arquivo_invalido", status_code=303
        )

    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # Atualizar caminho no banco (usar caminho relativo)
        caminho_relativo = f"/static/uploads/administradores/{nome_arquivo}"
        if hasattr(administrador_repo, "atualizar_foto"):
            administrador_repo.atualizar_foto(usuario_logado["id"], caminho_relativo)

        # Atualizar sessão (se aplicável)
        if usuario_logado is not None:
            usuario_logado["foto"] = caminho_relativo
            from util.auth_decorator import criar_sessao

            criar_sessao(request, usuario_logado)

    except Exception as e:
        return RedirectResponse(
            "/administrador/perfil?erro=upload_falhou", status_code=303
        )

    return RedirectResponse("/administrador/perfil?foto_sucesso=1", status_code=303)
