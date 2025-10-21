"""
Rotas de cadastro de prestador, cliente e fornecedor
"""
import logging
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Form, Request, status, UploadFile, File
from fastapi.responses import RedirectResponse
from pydantic import ValidationError

from data.cliente import cliente_repo
from data.cliente.cliente_model import Cliente
from data.fornecedor import fornecedor_repo
from data.fornecedor.fornecedor_model import Fornecedor
from data.prestador import prestador_repo
from data.prestador.prestador_model import Prestador
from data.usuario import usuario_repo
from data.usuario.usuario_model import Usuario
from data.mensagem.mensagem_model import Mensagem
from data.mensagem import mensagem_repo
from dtos.cliente.cliente_dto import CriarClienteDTO
from dtos.fornecedor.fornecedor_dto import CriarFornecedorDTO
from dtos.prestador.prestador_dto import CriarPrestadorDTO
from util.auth_decorator import obter_usuario_logado, requer_autenticacao, aplicar_rate_limit_cadastro
from util.flash_messages import informar_sucesso
from util.security import criar_hash_senha, gerar_token_redefinicao, verificar_senha
from util.template_util import criar_templates
import os
import uuid

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Cadastros"])
templates = criar_templates("templates")

@router.get("/cadastro/prestador")
async def exibir_cadastro_prestador(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/prestador/prestador_cadastro.html", {"request": request, "dados": None, "usuario_logado": usuario_logado}
    )


# Rota para processar o formulário de cadastro
@router.post("/cadastro/prestador")
@aplicar_rate_limit_cadastro()
async def processar_cadastro_prestador(
    request: Request,
    nomeCompleto: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(),
    bairro: str = Form(...),
    senha: str = Form(...),
    cep: str = Form(...),
    confirmarSenha: str = Form(...),
    documento: str = Form(...),
    area_atuacao: str = Form(...),
    razao_social: Optional[str] = Form(None),
    descricao_servicos: Optional[str] = Form(None),
):
    # Criar dicionário com dados do formulário (para preservar)
    dados_formulario = {
        "nome": nomeCompleto,
        "email": email,
        "telefone": telefone,
        "estado": estado,
        "cidade": cidade,
        "rua": rua,
        "numero": numero,
        "complemento": complemento,
        "bairro": bairro,
        "cpf_cnpj": documento,
        "area_atuacao": area_atuacao,
        "razao_social": razao_social,
        "descricao_servicos": descricao_servicos,
    }

    try:
        # Validar dados com Pydantic
        dados_dto = CriarPrestadorDTO(
            nome=nomeCompleto,
            email=email,
            telefone=telefone,
            estado=estado,
            cidade=cidade,
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cep=cep,
            senha=senha,
            confirmar_senha=confirmarSenha,
            cpf_cnpj=documento,
            area_atuacao=area_atuacao,
            razao_social=razao_social,
            descricao_servicos=descricao_servicos,
            tipo_usuario="prestador",
        )

        # Verificar se email já existe APÓS a validação do DTO
        if prestador_repo.obter_prestador_por_email(dados_dto.email):
            return templates.TemplateResponse(
                "publico/prestador/prestador_cadastro.html",
                {
                    "request": request,
                    "erro": "Email já cadastrado",
                    "dados": dados_formulario,
                },
            )

        # Criar hash da senha
        senha_hash = criar_hash_senha(dados_dto.senha)

        # Criar objeto Prestador
        prestador = Prestador(
            id=0,  # O ID será gerado pelo banco de dados
            nome=dados_dto.nome,
            email=dados_dto.email,
            senha=senha_hash,
            cpf_cnpj=dados_dto.cpf_cnpj,
            telefone=dados_dto.telefone,
            cep=dados_dto.cep,
            estado=dados_dto.estado,
            cidade=dados_dto.cidade,
            rua=dados_dto.rua,
            numero=dados_dto.numero,
            complemento=dados_dto.complemento or "",
            bairro=dados_dto.bairro,
            tipo_usuario=dados_dto.tipo_usuario,
            data_cadastro=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            foto=None,  # Assumindo que não há upload de foto para prestador neste momento
            token_redefinicao=None,
            data_token=None,
            area_atuacao=dados_dto.area_atuacao,
            razao_social=dados_dto.razao_social,
            descricao_servicos=dados_dto.descricao_servicos,
        )

        # Inserir no banco de dados
        prestador_id = prestador_repo.inserir_prestador(prestador)
        if not prestador_id:
            return templates.TemplateResponse(
                "publico/prestador/prestador_cadastro.html",
                {
                    "request": request,
                    "erro": "Erro ao cadastrar prestador. Tente novamente.",
                    "dados": dados_formulario,
                },
            )

        # Sucesso - Redirecionar com mensagem flash
        informar_sucesso(
            request,
            f"Cadastro de prestador realizado com sucesso! Bem-vindo(a), {nomeCompleto}!",
        )
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            loc_tuple = erro.get("loc")
            campo = str(loc_tuple[0]) if loc_tuple and len(loc_tuple) > 0 else "campo"
            mensagem = erro.get("msg", "")
            campo_str = (
                str(campo).capitalize() if isinstance(campo, (str, int)) else "campo"
            )
            erros.append(f"{campo_str}: {mensagem}")

        erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro de prestador: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse(
            "publico/prestador/prestador_cadastro.html",
            {
                "request": request,
                "erro": erro_msg,
                "dados": dados_formulario,  # Preservar dados digitados
            },
        )

    except Exception as e:
        # logger.error(f"Erro ao processar cadastro de prestador: {e}")

        return templates.TemplateResponse(
            "publico/prestador/prestador_cadastro.html",
            {
                "request": request,
                "erro": "Erro ao processar cadastro. Tente novamente.",
                "dados": dados_formulario,
            },
        )


# Rota para cadastro de cliente
@router.get("/cadastro/cliente")
async def get_page(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/login_cadastro/cadastro.html", {"request": request, "dados": None, "usuario_logado": usuario_logado}
    )


# Rota para processar o formulário de cadastro
@router.post("/cadastro/cliente")
@aplicar_rate_limit_cadastro()
async def post_cadastro(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    telefone: str = Form(...),
    cep: str = Form(""),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    complemento: str = Form(""),
    bairro: str = Form(...),
    foto: str = Form(None),
    genero: str = Form(...),
    data_nascimento: str = Form(...),
):

    # Criar dicionário com dados do formulário (para preservar)
    dados_formulario = {
        "nome": nome,
        "email": email,
        "cpf_cnpj": cpf_cnpj,
        "telefone": telefone,
        "estado": estado,
        "cidade": cidade,
        "rua": rua,
        "numero": numero,
        "bairro": bairro,
        "genero": genero,
        "data_nascimento": data_nascimento,
    }

    try:
        # Convert data_nascimento string to date if provided
        from datetime import date as date_class

        data_nasc_obj: Optional[date_class] = None
        if data_nascimento and data_nascimento.strip():
            try:
                data_nasc_obj = date_class.fromisoformat(data_nascimento)
            except ValueError:
                pass

        # Validar dados com Pydantic
        dados_dto = CriarClienteDTO(
            nome=nome,
            email=email,
            telefone=telefone,
            cep=cep or "",
            estado=estado,
            cidade=cidade,
            rua=rua,
            numero=numero,
            complemento=complemento or "",
            bairro=bairro,
            senha=senha,
            confirmar_senha=confirmar_senha,
            cpf_cnpj=cpf_cnpj,
            tipo_usuario="cliente",
            genero=genero,
            data_nascimento=data_nasc_obj,
        )

        # Verificar se email já existe APÓS a validação do DTO
        if cliente_repo.obter_cliente_por_email(dados_dto.email):
            return templates.TemplateResponse(
                "publico/cliente/cadastro_cliente.html",
                {
                    "request": request,
                    "erro": "Email já cadastrado",
                    "dados": dados_formulario,
                },
            )

        # Criar hash da senha
        senha_hash = criar_hash_senha(dados_dto.senha)

        # Criar objeto Cliente
        cliente = Cliente(
            id=0,
            nome=nome,
            email=email,
            senha=senha_hash,
            cpf_cnpj=cpf_cnpj,
            telefone=telefone,
            cep=cep or "",
            complemento=complemento or "",
            estado=estado,
            cidade=cidade,
            rua=rua,
            numero=numero,
            bairro=bairro,
            tipo_usuario="Cliente",
            data_cadastro=None,
            foto=foto,
            token_redefinicao=None,
            data_token=None,
            genero=genero,
            data_nascimento=data_nasc_obj,
        )

        # Inserir no banco de dados
        cliente_id = cliente_repo.inserir_cliente(cliente)
        if not cliente_id:
            return templates.TemplateResponse(
                "publico/cliente/cadastro_cliente.html",
                {
                    "request": request,
                    "erro": "Erro ao cadastrar cliente. Tente novamente.",
                    "dados": dados_formulario,
                },
            )

        # Sucesso - Redirecionar com mensagem flash
        informar_sucesso(
            request, f"Cadastro de cliente realizado com sucesso! Bem-vindo(a), {nome}!"
        )
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            loc_tuple = erro.get("loc")
            campo = str(loc_tuple[0]) if loc_tuple and len(loc_tuple) > 0 else "campo"
            mensagem = erro.get("msg", "")
            campo_str = (
                str(campo).capitalize() if isinstance(campo, (str, int)) else "campo"
            )
            erros.append(f"{campo_str}: {mensagem}")

        erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro de prestador: {erro_msg}")

        # Retornar template com dados preservados e erro
        return templates.TemplateResponse(
            "publico/cliente/cadastro_cliente.html",
            {
                "request": request,
                "erro": erro_msg,
                "dados": dados_formulario,  # Preservar dados digitados
            },
        )

    except Exception as e:
        # logger.error(f"Erro ao processar cadastro de prestador: {e}")

        return templates.TemplateResponse(
            "publico/cliente/cadastro_cliente.html",
            {
                "request": request,
                "erro": "Erro ao processar cadastro. Tente novamente.",
                "dados": dados_formulario,
            },
        )


# Rota para cadastro de fornecedor
@router.get("/cadastro/fornecedor")
async def exibir_cadastro_fornecedor(request: Request):
    usuario_logado = obter_usuario_logado(request)
    return templates.TemplateResponse(
        "publico/fornecedor2/cadastro_fornecedor.html", {"request": request, "usuario_logado": usuario_logado}
    )


# Cadastro de fornecedor (POST)
@router.post("/cadastro/fornecedor")
@aplicar_rate_limit_cadastro()
async def processar_cadastro_fornecedor(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    cpf_cnpj: str = Form(...),
    razao_social: Optional[str] = Form(None),
    complemento: Optional[str] = Form(None),
    cep: Optional[str] = Form(None),
    foto: UploadFile = File(None),
):
    # Preservar dados do formulário (exceto senhas por segurança)
    dados_formulario = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "estado": estado,
        "cidade": cidade,
        "rua": rua,
        "numero": numero,
        "bairro": bairro,
        "cpf_cnpj": cpf_cnpj,
        "razao_social": razao_social,
        "complemento": complemento,
        "cep": cep,
    }

    try:
        # Log: valor bruto recebido para diagnóstico (usar INFO para garantir visibilidade nos logs)
        logger.info(f"[DEBUG-INFO] raw cpf_cnpj recebido (form): {repr(cpf_cnpj)}")

        # Validar dados com Pydantic DTO
        fornecedor_dto = CriarFornecedorDTO(
            nome=nome,
            email=email,
            telefone=telefone,
            estado=estado,
            cidade=cidade,
            rua=rua,
            numero=numero,
            bairro=bairro,
            senha=senha,
            confirmar_senha=confirmar_senha,
            cpf_cnpj=cpf_cnpj,
            razao_social=razao_social,
            complemento=complemento or "",
            cep=cep or "",
            tipo_usuario="fornecedor",
        )

        # Log: valor depois da validação (limpo) — usar INFO para visibilidade
        logger.info(
            f"[DEBUG-INFO] fornecedor_dto.cpf_cnpj (após validação): {repr(getattr(fornecedor_dto, 'cpf_cnpj', None))}"
        )

        # Verificar se todos os campos obrigatórios foram preenchidos (usar valores validados pelo DTO)
        if (
            not fornecedor_dto.nome
            or not fornecedor_dto.email
            or not fornecedor_dto.senha
            or not fornecedor_dto.confirmar_senha
            or not fornecedor_dto.cpf_cnpj
        ):
            return templates.TemplateResponse(
                "publico/fornecedor2/cadastro_fornecedor.html",
                {
                    "request": request,
                    "erro": "Preencha todos os campos.",
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Verificar se senhas coincidem (usar valores do DTO)
        if fornecedor_dto.senha != fornecedor_dto.confirmar_senha:
            return templates.TemplateResponse(
                "publico/fornecedor2/cadastro_fornecedor.html",
                {
                    "request": request,
                    "erro": "As senhas não coincidem.",
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Verificar se email já existe (usar email validado pelo DTO)
        if fornecedor_repo.obter_fornecedor_por_email(fornecedor_dto.email):
            return templates.TemplateResponse(
                "publico/fornecedor2/cadastro_fornecedor.html",
                {
                    "request": request,
                    "erro": "Email já cadastrado. Tente fazer login ou use outro email.",
                    "dados": dados_formulario,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        # Criar hash da senha (usar senha validada)
        senha_hash = criar_hash_senha(fornecedor_dto.senha)

        # Garante que razao_social nunca seja None ou string vazia (usar DTO)
        razao_social_value = getattr(fornecedor_dto, "razao_social", None)
        razao_social_final = (
            razao_social_value
            if razao_social_value and razao_social_value.strip()
            else fornecedor_dto.nome
        )

        # Lógica de upload de foto
        caminho_foto = None
        if foto and foto.filename:
            tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
            if foto.content_type not in tipos_permitidos:
                return templates.TemplateResponse(
                    "publico/fornecedor2/cadastro_fornecedor.html",
                    {
                        "request": request,
                        "erro": "Tipo de arquivo de foto inválido. Use apenas JPG, JPEG ou PNG.",
                        "dados": dados_formulario,
                    },
                )
            upload_dir = "static/uploads/fornecedores"
            os.makedirs(upload_dir, exist_ok=True)
            import secrets

            extensao = foto.filename.split(".")[-1]
            nome_arquivo = f"{fornecedor_dto.email}_{secrets.token_hex(8)}.{extensao}"
            caminho_arquivo = os.path.join(upload_dir, nome_arquivo)
            conteudo = await foto.read()
            with open(caminho_arquivo, "wb") as f:
                f.write(conteudo)
            caminho_foto = f"/static/uploads/fornecedores/{nome_arquivo}"

        # Criar objeto Fornecedor
        fornecedor = Fornecedor(
            id=0,
            nome=fornecedor_dto.nome,
            email=fornecedor_dto.email,
            senha=senha_hash,
            cpf_cnpj=fornecedor_dto.cpf_cnpj,
            telefone=fornecedor_dto.telefone,
            cep=getattr(fornecedor_dto, "cep", "") or "",
            estado=fornecedor_dto.estado,
            cidade=fornecedor_dto.cidade,
            rua=fornecedor_dto.rua,
            numero=fornecedor_dto.numero,
            complemento=getattr(fornecedor_dto, "complemento", None) or "",
            bairro=fornecedor_dto.bairro,
            tipo_usuario="Fornecedor",
            data_cadastro=datetime.now().isoformat(),
            foto=caminho_foto,
            token_redefinicao=None,
            data_token=None,
            razao_social=razao_social_final,
        )

        # Inserir no banco de dados
        fornecedor_id = fornecedor_repo.inserir_fornecedor(fornecedor)
        if not fornecedor_id:
            return templates.TemplateResponse(
                "publico/fornecedor2/cadastro_fornecedor.html",
                {
                    "request": request,
                    "erro": "Erro ao cadastrar fornecedor. Tente novamente.",
                    "dados": dados_formulario,
                },
            )

        # Cadastro realizado com sucesso - redirecionar para login
        logger.info(f"Fornecedor cadastrado com sucesso: {fornecedor_dto.email}")
        return RedirectResponse(
            url="/login?mensagem=Cadastro realizado com sucesso! Faça seu login.",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        campos_erro: dict[str, list[str]] = {}
        # Log completo para debug (usar WARNING para visibilidade)
        logger.warning(f"[DEBUG-WARN] ValidationError.errors(): {e.errors()}")
        for erro in e.errors():
            # loc pode ser ('field',) ou ('field', 0, ...); pegamos o primeiro elemento
            loc = erro.get("loc")
            campo = str(loc[0]) if loc and len(loc) > 0 else "campo"
            mensagem = erro.get("msg")
            campo_str = str(campo) if not isinstance(campo, str) else campo
            texto = f"{campo_str.capitalize()}: {mensagem}"
            erros.append(texto)
            # acumular por campo
            if isinstance(mensagem, str):
                campos_erro.setdefault(campo, []).append(mensagem)

        erro_msg = " | ".join(erros)
        logger.warning(f"Erro de validação no cadastro de fornecedor: {erro_msg}")

        # Retornar template com dados preservados e detalhes por campo
        return templates.TemplateResponse(
            "publico/fornecedor2/cadastro_fornecedor.html",
            {
                "request": request,
                "erro": erro_msg,
                "erros_list": erros,
                "campos_erro": campos_erro,
                "dados": dados_formulario,  # Preservar dados digitados
            },
        )

    except Exception as e:
        logger.error(f"Erro ao processar cadastro de fornecedor: {e}")

        return templates.TemplateResponse(
            "publico/fornecedor2/cadastro_fornecedor.html",
            {
                "request": request,
                "erro": "Erro ao processar cadastro. Tente novamente.",
                "dados": dados_formulario,
            },
        )


# ---------------------------------------------------------------------
