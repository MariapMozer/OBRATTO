# routes/prestador/home_routes.py

from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from util.auth_decorator import obter_usuario_logado # Função que obtém o usuário logado
from util.template_util import criar_templates
# Importe aqui as funções/repositórios para buscar os dados (serviços, solicitações, etc.)
# from data.servico import servico_repo
# from data.solicitacao import solicitacao_repo

router = APIRouter(tags=["Prestador"])
templates = criar_templates("templates")

@router.get("/home", response_class=HTMLResponse)
async def get_prestador_home(request: Request):
    """
    Página inicial do prestador.
    Rota: /prestador/home
    """
    # 1. Obter o usuário logado (usando a função que você já tem)
    usuario_logado = obter_usuario_logado(request)
    
    # 2. **IMPORTANTE:** Carregar os dados necessários para o template
    # O template que padronizamos (prestador_home_padronizado.html) precisa destas variáveis:
    
    # **Exemplo de Carregamento de Dados (Você deve implementar isso):**
    # total_servicos = servico_repo.contar_servicos_por_prestador(usuario_logado.id)
    # total_solicitacoes = solicitacao_repo.contar_solicitacoes_por_prestador(usuario_logado.id)
    # total_contratacoes = solicitacao_repo.contar_contratacoes_por_prestador(usuario_logado.id)
    # avaliacao_media = avaliacao_repo.obter_media_por_prestador(usuario_logado.id)
    # servicos = servico_repo.obter_ultimos_servicos(usuario_logado.id, limite=3)
    # solicitacoes_recentes = solicitacao_repo.obter_solicitacoes_recentes(usuario_logado.id, limite=5)

    # **Variáveis de Exemplo (Substitua pelas suas variáveis reais):**
    context = {
        "request": request,
        "usuario_logado": usuario_logado,
        "total_servicos": 10, # Substitua pela contagem real
        "total_solicitacoes": 5, # Substitua pela contagem real
        "total_contratacoes": 2, # Substitua pela contagem real
        "avaliacao_media": "4.5", # Substitua pela média real
        "servicos": [], # Substitua pela lista real de serviços
        "solicitacoes_recentes": [], # Substitua pela lista real de solicitações
    }
    
    # 3. Renderizar o template
    return templates.TemplateResponse(
        "prestador/home.html", # Certifique-se de que este é o nome correto do seu template
        context
    )
