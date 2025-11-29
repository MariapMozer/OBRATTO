from typing import Optional
from asyncio import open_connection
import os
from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from data.usuario.usuario_sql import ATUALIZAR_FOTO
from util.auth_decorator import requer_autenticacao
from util.template_util import criar_templates
from data.fornecedor.fornecedor_model import Fornecedor
from data.fornecedor import fornecedor_repo
from util.security import criar_hash_senha
from data.usuario import usuario_repo
from data.usuario.usuario_repo import atualizar_foto
from data.avaliacao import avaliacao_repo
from datetime import datetime
from util.logger_config import logger

router = APIRouter()
templates = criar_templates("templates")


@router.get("/home")
@requer_autenticacao(["fornecedor"])
async def home_fornecedor(request: Request, usuario_logado: Optional[dict] = None):
    """Página inicial do fornecedor"""
    assert usuario_logado is not None
    
    # Obter estatísticas para dashboard
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    
    return templates.TemplateResponse(
        "fornecedor/home_fornecedor.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
            "fornecedor": fornecedor,
        }
    )


@router.get("/cadastro")
@requer_autenticacao(["administrador"])
async def formulario_cadastro_fornecedor(request: Request, usuario_logado: Optional[dict] = None):
    """Formulário para cadastrar novo fornecedor (apenas administrador)"""
    assert usuario_logado is not None
    
    return templates.TemplateResponse(
        "fornecedor/cadastro_fornecedor.html",
        {
            "request": request,
            "usuario_logado": usuario_logado,
        }
    )


@router.post("/cadastro")
@requer_autenticacao(["administrador"])
async def processar_cadastro_fornecedor(
    request: Request,
    nome: str = Form(...),
    razao_social: str = Form(...),
    cpf_cnpj: str = Form(...),
    telefone: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    cidade: str = Form(...),
    estado: str = Form(...),
    cep: str = Form(...),
    complemento: str = Form(None),
    email: str = Form(...),
    senha: str = Form(...),
    confirmar_senha: str = Form(...),
    termos: str = Form(None),
    usuario_logado: Optional[dict] = None,
):
    """Processar cadastro de novo fornecedor"""
    assert usuario_logado is not None
    
    erros = {}
    
    # Validações básicas
    if not nome or len(nome) < 2:
        erros['nome'] = ['Nome deve ter no mínimo 2 caracteres']
    
    if not razao_social or len(razao_social) < 2:
        erros['razao_social'] = ['Razão social deve ter no mínimo 2 caracteres']
    
    if not cpf_cnpj or len(cpf_cnpj.replace('.', '').replace('-', '')) < 11:
        erros['cpf_cnpj'] = ['CPF/CNPJ inválido']
    
    if not telefone or len(telefone.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')) < 10:
        erros['telefone'] = ['Telefone inválido']
    
    if not email or '@' not in email:
        erros['email'] = ['Email inválido']
    
    if not senha or len(senha) < 8:
        erros['senha'] = ['Senha deve ter no mínimo 8 caracteres']
    
    if not confirmar_senha or confirmar_senha != senha:
        erros['confirmar_senha'] = ['As senhas não coincidem']
    
    if not rua or len(rua) < 2:
        erros['rua'] = ['Rua é obrigatória']
    
    if not numero:
        erros['numero'] = ['Número é obrigatório']
    
    if not bairro or len(bairro) < 2:
        erros['bairro'] = ['Bairro é obrigatório']
    
    if not cidade or len(cidade) < 2:
        erros['cidade'] = ['Cidade é obrigatória']
    
    if not cep or len(cep.replace('-', '')) < 8:
        erros['cep'] = ['CEP inválido']
    
    if not estado or len(estado) != 2:
        erros['estado'] = ['Estado é obrigatório']
    
    if not termos:
        erros['termos'] = ['Você deve aceitar os termos de serviço']
    
    # Se houver erros, retornar formulário com erros
    if erros:
        return templates.TemplateResponse(
            "fornecedor/cadastro_fornecedor.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erros": erros,
                "fornecedor": {
                    "nome": nome,
                    "razao_social": razao_social,
                    "cpf_cnpj": cpf_cnpj,
                    "telefone": telefone,
                    "rua": rua,
                    "numero": numero,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "cep": cep,
                    "complemento": complemento,
                    "email": email,
                }
            },
            status_code=400
        )
    
    try:
        # Verificar se email já existe
        user_existente = usuario_repo.obter_usuario_por_email(email)
        if user_existente:
            erros['email'] = ['Email já cadastrado']
            return templates.TemplateResponse(
                "fornecedor/cadastro_fornecedor.html",
                {
                    "request": request,
                    "usuario_logado": usuario_logado,
                    "erros": erros,
                    "fornecedor": {
                        "nome": nome,
                        "razao_social": razao_social,
                        "cpf_cnpj": cpf_cnpj,
                        "telefone": telefone,
                        "rua": rua,
                        "numero": numero,
                        "bairro": bairro,
                        "cidade": cidade,
                        "estado": estado,
                        "cep": cep,
                        "complemento": complemento,
                        "email": email,
                    }
                },
                status_code=400
            )
        
        # Criar novo usuário
        from util.security import criar_hash_senha
        from data.usuario.usuario_model import Usuario
        
        novo_usuario = Usuario(
            id=0,
            nome=nome,
            email=email,
            senha_hash=criar_hash_senha(senha),
            tipo_usuario="fornecedor",
            ativo=True,
            data_criacao=datetime.now(),
            foto=None
        )
        
        usuario_id = usuario_repo.inserir_usuario(novo_usuario)
        
        # Criar fornecedor vinculado
        novo_fornecedor = Fornecedor(
            id=usuario_id,
            razao_social=razao_social,
            selo_confianca=False
        )
        
        fornecedor_repo.inserir_fornecedor(novo_fornecedor)
        
        # Atualizar dados de endereço do usuário
        import sqlite3
        from util.db import open_connection
        
        with open_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE usuario 
                SET cpf_cnpj=?, telefone=?, rua=?, numero=?, bairro=?, cidade=?, estado=?, cep=?, complemento=?
                WHERE id=?
            """, (cpf_cnpj, telefone, rua, numero, bairro, cidade, estado, cep, complemento, usuario_id))
            conn.commit()
        
        # Retornar com mensagem de sucesso
        return templates.TemplateResponse(
            "fornecedor/cadastro_fornecedor.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "sucesso": f"Fornecedor {nome} cadastrado com sucesso! ID: {usuario_id}"
            }
        )
        
    except Exception as e:
        logger.error(f"Erro ao cadastrar fornecedor: {e}")
        return templates.TemplateResponse(
            "fornecedor/cadastro_fornecedor.html",
            {
                "request": request,
                "usuario_logado": usuario_logado,
                "erro": "Erro ao cadastrar fornecedor. Tente novamente.",
                "fornecedor": {
                    "nome": nome,
                    "razao_social": razao_social,
                    "cpf_cnpj": cpf_cnpj,
                    "telefone": telefone,
                    "rua": rua,
                    "numero": numero,
                    "bairro": bairro,
                    "cidade": cidade,
                    "estado": estado,
                    "cep": cep,
                    "complemento": complemento,
                    "email": email,
                }
            },
            status_code=500
        )


@router.get("/perfil")
@requer_autenticacao(["fornecedor"])
async def visualizar_perfil_fornecedor(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    
    # Se fornecedor não existe, criar automaticamente
    if not fornecedor:
        import sqlite3
        from util.db import open_connection
        
        try:
            with open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO fornecedor (id, razao_social, selo_confianca)
                    VALUES (?, ?, 0)
                """, (usuario_logado["id"], usuario_logado.get("nome", "Fornecedor")))
                conn.commit()
            
            # Tentar obter novamente
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
        except Exception as e:
            from util.logger_config import logger
            logger.error(f"Erro ao criar fornecedor: {e}")
            raise HTTPException(status_code=500, detail="Erro ao criar perfil de fornecedor")
    
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    
    return templates.TemplateResponse(
        "fornecedor/perfil.html", {"request": request, "fornecedor": fornecedor}
    )


# 2. Editar/atualizar perfil do fornecedor
@router.post("/perfil/editar")
@requer_autenticacao(["fornecedor"])
async def editar_perfil_fornecedor(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    estado: str = Form(...),
    cidade: str = Form(...),
    rua: str = Form(...),
    numero: str = Form(...),
    bairro: str = Form(...),
    razao_social: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor.nome = nome
    fornecedor.email = email
    fornecedor.telefone = telefone
    fornecedor.razao_social = razao_social
    fornecedor_repo.atualizar_fornecedor(fornecedor)
    mensagem = "Perfil atualizado com sucesso."
    return templates.TemplateResponse(
        "fornecedor/perfil.html",
        {"request": request, "fornecedor": fornecedor, "mensagem": mensagem},
    )


# 3. Alterar senha do fornecedor

from util.security import verificar_senha, criar_hash_senha


@router.post("/perfil/alterar-senha")
@requer_autenticacao(["fornecedor"])
async def alterar_senha_fornecedor(
    request: Request,
    id: int,
    senha_atual: str = Form(...),
    nova_senha: str = Form(...),
    usuario_logado: Optional[dict] = None,
):
    from data.usuario import usuario_repo

    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    # Verifica se a senha atual está correta (usando hash)
    if not verificar_senha(senha_atual, fornecedor.senha):
        from fastapi import status
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            f"/fornecedor/perfil/?erro=senha_incorreta",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    # Atualiza a senha com hash
    nova_senha_hash = criar_hash_senha(nova_senha)
    usuario_repo.atualizar_senha_usuario(usuario_logado["id"], nova_senha_hash)
    from fastapi import status
    from fastapi.responses import RedirectResponse

    return RedirectResponse(
        f"/fornecedor/perfil/?msg=senha_alterada", status_code=status.HTTP_303_SEE_OTHER
    )


# 4. Upload/atualização de foto de perfil
@router.post("/perfil/foto")
@requer_autenticacao(["fornecedor"])
async def upload_foto_perfil(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: Optional[dict] = None,
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    
    # Se fornecedor não existe, criar automaticamente
    if not fornecedor:
        from util.db import open_connection
        
        try:
            with open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO fornecedor (id, razao_social, selo_confianca)
                    VALUES (?, ?, 0)
                """, (usuario_logado["id"], usuario_logado.get("nome", "Fornecedor")))
                conn.commit()
            
            fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
        except Exception as e:
            from util.logger_config import logger
            logger.error(f"Erro ao criar fornecedor: {e}")
    
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")

    # Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg"]
    if foto.content_type not in tipos_permitidos:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            "/fornecedor/perfil/?erro=tipo_invalido", status_code=303
        )

    # Criar diretório de upload se não existir
    upload_dir = "static/uploads/fornecedores"
    os.makedirs(upload_dir, exist_ok=True)

    # Gerar nome único para o arquivo
    import secrets

    extensao = foto.filename.split(".")[-1] if foto.filename else "jpg"
    nome_arquivo = f"{usuario_logado['id']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # Salvar arquivo
    try:
        conteudo = await foto.read()
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # Atualizar caminho no banco (usar caminho relativo)
        caminho_relativo = f"/static/uploads/fornecedores/{nome_arquivo}"
        atualizar_foto(usuario_logado["id"], caminho_relativo)

        # Atualizar sessão (se aplicável)
        usuario_logado["foto"] = caminho_relativo
        from util.auth_decorator import criar_sessao

        criar_sessao(request, usuario_logado)

    except Exception as e:
        from fastapi.responses import RedirectResponse

        return RedirectResponse(
            "/fornecedor/perfil/?erro=upload_falhou", status_code=303
        )

    from fastapi.responses import RedirectResponse

    return RedirectResponse("/fornecedor/perfil/?foto_sucesso=1", status_code=303)


# 13. Deletar conta do fornecedor
@router.post("/perfil/excluir")
@requer_autenticacao(["fornecedor"])
async def deletar_conta_fornecedor(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    fornecedor_repo.deletar_fornecedor(usuario_logado["id"])
    from fastapi import status
    from fastapi.responses import RedirectResponse

    return RedirectResponse(
        "/fornecedor/cadastro?msg=conta_excluida", status_code=status.HTTP_303_SEE_OTHER
    )


# Visualizar perfil do fornecedor
@router.get("/conta")
@requer_autenticacao(["fornecedor"])
async def visualizar_conta(request: Request, usuario_logado: Optional[dict] = None):
    assert usuario_logado is not None
    fornecedor = fornecedor_repo.obter_fornecedor_por_id(usuario_logado["id"])
    return templates.TemplateResponse(
        "fornecedor/conta.html", {"request": request, "fornecedor": fornecedor}
    )


# Visualizar avaliações recebidas pelo fornecedor
@router.get("/avaliacoes")
@requer_autenticacao(["fornecedor"])
async def visualizar_avaliacoes_recebidas(
    request: Request, usuario_logado: Optional[dict] = None
):
    assert usuario_logado is not None
    # obter todas as avaliações e filtrar pelas que foram feitas para o fornecedor logado
    todas = avaliacao_repo.obter_todos()
    avaliacoes = [a for a in todas if getattr(a, 'id_avaliado', None) == usuario_logado['id']]
    return templates.TemplateResponse(
        "fornecedor/avaliacoes/recebidas.html",
        {"request": request, "avaliacoes": avaliacoes, "usuario_logado": usuario_logado},
    )


# atualizar foto de perfil


def atualizar_foto(id: int, caminho_foto: str) -> bool:
    """Atualiza apenas a foto do usuário"""
    from util.db import open_connection

    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(ATUALIZAR_FOTO, (caminho_foto, id))
        return cursor.rowcount > 0
