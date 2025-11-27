#!/usr/bin/env python3
"""
Script para reorganizar a estrutura de templates do projeto OBRATTO
"""
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Diretório base do projeto
BASE_DIR = Path("/Volumes/Externo/Ifes/PI/OBRATTO")
TEMPLATES_DIR = BASE_DIR / "templates"

# Mapeamento completo: origem -> destino
# Formato: "caminho/relativo/antigo.html": "caminho/relativo/novo.html"
FILE_MAPPINGS: Dict[str, str] = {
    # === AUTH (login/cadastro) ===
    "publico/login_cadastro/login.html": "auth/login.html",
    "publico/login_cadastro/cadastro_sucesso.html": "auth/cadastro_sucesso.html",
    "publico/login_cadastro/recuperar_senha.html": "auth/recuperar_senha.html",
    "publico/login_cadastro/redefinir_senha.html": "auth/redefinir_senha.html",

    # === PUBLIC ===
    "publico/home.html": "public/home.html",
    "publico/em_construcao.html": "public/em_construcao.html",

    # PUBLIC - Cadastros
    "publico/fornecedor2/cadastro_fornecedor.html": "public/cadastro/fornecedor.html",
    "publico/cadastro_cliente.html": "public/cadastro/cliente.html",  # se existir
    "publico/cadastro_prestador.html": "public/cadastro/prestador.html",  # se existir

    # PUBLIC - Perfis Públicos
    "publico/cliente/perfil_publico.html": "public/perfil/cliente.html",
    "publico/fornecedor2/perfil_publico_fornecedor.html": "public/perfil/fornecedor.html",
    "publico/prestador/perfil_publico.html": "public/perfil/prestador.html",

    # === COMPONENTS ===
    "components/toast-handler.html": "components/toast-handler.html",  # mantém

    # === ERRORS ===
    "errors/404.html": "errors/404.html",  # mantém
    "errors/500.html": "errors/500.html",  # mantém

    # === ADMIN ===
    "administrador/home_adm.html": "admin/dashboard.html",
    "administrador/base_admin.html": "base/admin.html",
    "administrador/perfil_editar.html": "admin/perfil_editar.html",
    "administrador/verificacao_usuario.html": "admin/verificacao_usuario.html",
    "administrador/em_construcao.html": "admin/em_construcao.html",

    # ADMIN - Usuários
    "administrador/listar_cliente.html": "admin/usuarios/clientes/listar.html",
    "administrador/listar_fornecedor.html": "admin/usuarios/fornecedores/listar.html",
    "administrador/moderar_fornecedor/listar_fornecedor.html": "admin/usuarios/fornecedores/listar.html",
    "administrador/moderar_fornecedor/moderar_produtos.html": "admin/usuarios/fornecedores/produtos.html",
    "administrador/listar_prestador.html": "admin/usuarios/prestadores/listar.html",
    "administrador/moderar_prestador/listar_prestador.html": "admin/usuarios/prestadores/listar.html",
    "administrador/moderar_prestador/moderar_servicos_prestador.html": "admin/usuarios/prestadores/servicos.html",
    "administrador/lista.html": "admin/usuarios/administradores/listar.html",
    "administrador/moderar_adm/lista_adm.html": "admin/usuarios/administradores/listar.html",
    "administrador/moderar_adm/cadastrar_adm.html": "admin/usuarios/administradores/cadastrar.html",
    "administrador/moderar_adm/editar_adm.html": "admin/usuarios/administradores/editar.html",
    "administrador/moderar_adm/remover_adm.html": "admin/usuarios/administradores/remover.html",

    # ADMIN - Moderação
    "administrador/moderar_anuncios.html": "admin/moderacao/anuncios.html",
    "administrador/moderar_avaliacoes.html": "admin/moderacao/avaliacoes.html",
    "administrador/aprovar_profissionais.html": "admin/moderacao/aprovar_profissionais.html",
    "administrador/avaliar_profissionais.html": "admin/moderacao/avaliar_profissionais.html",
    "administrador/remover_avaliacoes.html": "admin/moderacao/remover_avaliacoes.html",
    "administrador/moderar_chat.html": "admin/moderacao/chat.html",

    # ADMIN - Relatórios
    "administrador/visualizar_relatorios.html": "admin/relatorios/visualizar.html",
    "administrador/relatorios_anuncios.html": "admin/relatorios/anuncios.html",
    "administrador/exportar_relatorios.html": "admin/relatorios/exportar.html",

    # ADMIN - Configurações
    "administrador/ajustar_configuracoes.html": "admin/configuracoes/ajustar.html",
    "administrador/configurar_seguranca.html": "admin/configuracoes/seguranca.html",

    # ADMIN - Serviços
    "administrador/servico/galeria.html": "admin/servicos/galeria.html",

    # === FORNECEDOR ===
    "fornecedor/home_fornecedor.html" # manter temporariamente
    "fornecedor/perfil.html": "fornecedor/perfil.html",
    "fornecedor/conta.html": "fornecedor/conta.html",
    "fornecedor/base.html": "base/fornecedor.html",

    # FORNECEDOR - Avaliações
    "fornecedor/avaliacoes_recebidas.html": "fornecedor/avaliacoes/recebidas.html",

    # FORNECEDOR - Mensagens
    "fornecedor/mensagens/mensagens_recebidas.html": "fornecedor/mensagens/recebidas.html",

    # FORNECEDOR - Orçamentos
    "fornecedor/orcamentos/orcamento.html": "fornecedor/orcamentos/detalhes.html",
    "fornecedor/orcamentos/responder_orcamentos.html": "fornecedor/orcamentos/responder.html",
    "fornecedor/orcamentos/solicitacoes_recebidas.html": "fornecedor/orcamentos/recebidas.html",

    # FORNECEDOR - Planos
    "fornecedor/planos/listar_planos.html": "fornecedor/planos/listar.html",
    "fornecedor/planos/assinar_plano.html": "fornecedor/planos/assinar.html",
    "fornecedor/planos/alterar_plano.html": "fornecedor/planos/alterar.html",
    "fornecedor/planos/cancelar_plano.html": "fornecedor/planos/cancelar.html",
    "fornecedor/planos/confirmacao_cancelamento_plano.html": "fornecedor/planos/confirmar_cancelamento.html",
    "fornecedor/planos/minha_assinatura.html": "fornecedor/planos/minha_assinatura.html",
    "fornecedor/planos/histórico_planos.html": "fornecedor/planos/historico.html",
    "fornecedor/planos/renovar_plano.html": "fornecedor/planos/renovar.html",

    # FORNECEDOR - Produtos
    "fornecedor/produtos/cadastrar_produtos.html": "fornecedor/produtos/cadastrar.html",
    "fornecedor/produtos/alterar_produtos.html": "fornecedor/produtos/alterar.html",
    "fornecedor/produtos/excluir_produtos.html": "fornecedor/produtos/excluir.html",

    # FORNECEDOR - Promoções
    "fornecedor/promocao/cadastrar_promocoes.html": "fornecedor/promocoes/cadastrar.html",
    "fornecedor/promocao/alterar_promocoes.html": "fornecedor/promocoes/alterar.html",
    "fornecedor/promocao/confirmar_exclusao_promocao.html": "fornecedor/promocoes/confirmar_exclusao.html",

    # FORNECEDOR - Pagamento (de publico/pagamento)
    "publico/pagamento/dados_pagamento.html": "fornecedor/pagamento/dados.html",
    "publico/pagamento/processar_pagamento.html": "fornecedor/pagamento/processar.html",
    "publico/pagamento/pagamento_sucesso.html": "fornecedor/pagamento/sucesso.html",
    "publico/pagamento/pagamento_erro.html": "fornecedor/pagamento/erro.html",
    "publico/pagamento/pagamento_pendente.html": "fornecedor/pagamento/pendente.html",

    # === PRESTADOR ===
    "prestador/home.html": "prestador/home.html",
    "prestador/prestador_logout.html": "prestador/logout.html",

    # PRESTADOR - Agenda
    "prestador/agenda/agenda.html": "prestador/agenda/calendario.html",
    "prestador/agenda/detalhes.html": "prestador/agenda/detalhes.html",

    # PRESTADOR - Catálogo
    "prestador/catalogo/catalogo_prestadores.html": "prestador/catalogo/listar.html",

    # PRESTADOR - Perfil
    "prestador/perfil/painel.html": "prestador/perfil/painel.html",
    "prestador/perfil/perfil.html": "prestador/perfil/visualizar.html",
    "prestador/perfil/editar_dados.html": "prestador/perfil/editar_dados.html",
    "prestador/perfil/foto/dados.html": "prestador/perfil/editar_fotos.html",
    "prestador/perfil/excluir.html": "prestador/perfil/excluir.html",

    # PRESTADOR - Planos
    "prestador/planos/planos.html": "prestador/planos/listar.html",
    "prestador/planos/meu_plano.html": "prestador/planos/meu_plano.html",
    "prestador/planos/assinar.html": "prestador/planos/assinar.html",
    "prestador/planos/editar.html": "prestador/planos/editar.html",
    "prestador/planos/cancelar.html": "prestador/planos/cancelar.html",
    "prestador/planos/renovar.html": "prestador/planos/renovar.html",
    "prestador/planos/confirmar_assinatura.html": "prestador/planos/confirmar_assinatura.html",
    "prestador/planos/confirmar_cancelamento.html": "prestador/planos/confirmar_cancelamento.html",

    # PRESTADOR - Serviços
    "prestador/servicos/buscar.html": "prestador/servicos/buscar.html",
    "prestador/servicos/novo.html": "prestador/servicos/novo.html",
    "prestador/servicos/editar_servico.html": "prestador/servicos/editar.html",
    "prestador/servicos/detalhes.html": "prestador/servicos/detalhes.html",
    "prestador/servicos/excluir.html": "prestador/servicos/excluir.html",
    "prestador/servicos/status.html": "prestador/servicos/status.html",

    # PRESTADOR - Solicitações
    "prestador/solicitacoes/detalhes.html": "prestador/solicitacoes/detalhes.html",

    # PRESTADOR - Pagamento (de publico/pagamento-prestador)
    "publico/pagamento-prestador/dados_pagamento.html": "prestador/pagamento/dados.html",
    "publico/pagamento-prestador/processar_pagamento.html": "prestador/pagamento/processar.html",
    "publico/pagamento-prestador/pagamento_sucesso.html": "prestador/pagamento/sucesso.html",
    "publico/pagamento-prestador/pagamento_erro.html": "prestador/pagamento/erro.html",
    "publico/pagamento-prestador/pagamento_pendente.html": "prestador/pagamento/pendente.html",

    # === CLIENTE ===
    "cliente/home.html": "cliente/home.html",
    "cliente/cliente_logout.html": "cliente/logout.html",
    "cliente/confirmacao.html": "cliente/confirmacao.html",
    "cliente/em_construcao.html": "cliente/em_construcao.html",
    "cliente/login.html": "cliente/login.html",  # verificar se existe
    "cliente/solicitar_orcamento.html": "cliente/solicitar_orcamento.html",
    "cliente/base.html": "base/cliente.html",

    # CLIENTE - Perfil
    "cliente/perfil/editar_fotos.html": "cliente/perfil/editar_fotos.html",

    # === AVALIAÇÕES ===
    "avaliacao/listar.html": "avaliacoes/listar.html",
    "avaliacao/nova.html": "avaliacoes/nova.html",
    "avaliacao/editar.html": "avaliacoes/editar.html",
    "avaliacao/detalhes.html": "avaliacoes/detalhes.html",
}


def criar_diretorios():
    """Cria toda a estrutura de diretórios necessária"""
    print("Criando estrutura de diretórios...")

    diretorios = [
        "base",
        "components",
        "errors",
        "auth",
        "public/cadastro",
        "public/perfil",
        "admin/usuarios/clientes",
        "admin/usuarios/fornecedores",
        "admin/usuarios/prestadores",
        "admin/usuarios/administradores",
        "admin/moderacao",
        "admin/relatorios",
        "admin/configuracoes",
        "admin/servicos",
        "fornecedor/avaliacoes",
        "fornecedor/mensagens",
        "fornecedor/orcamentos",
        "fornecedor/planos",
        "fornecedor/produtos",
        "fornecedor/promocoes",
        "fornecedor/pagamento",
        "prestador/agenda",
        "prestador/catalogo",
        "prestador/contratacoes",
        "prestador/perfil",
        "prestador/planos",
        "prestador/servicos",
        "prestador/solicitacoes",
        "prestador/pagamento",
        "cliente/perfil",
        "cliente/contratacoes",
        "avaliacoes",
    ]

    for dir_path in diretorios:
        full_path = TEMPLATES_DIR / dir_path
        full_path.mkdir(parents=True, exist_ok=True)

    print(f"✓ Criados {len(diretorios)} diretórios")


def mover_arquivos() -> Tuple[List[str], List[str], List[str]]:
    """
    Move os arquivos conforme o mapeamento

    Returns:
        Tuple com (movidos com sucesso, não encontrados, erros)
    """
    print("\nMovendo arquivos...")

    movidos = []
    nao_encontrados = []
    erros = []

    for origem, destino in FILE_MAPPINGS.items():
        caminho_origem = TEMPLATES_DIR / origem
        caminho_destino = TEMPLATES_DIR / destino

        if not caminho_origem.exists():
            nao_encontrados.append(origem)
            continue

        try:
            # Garantir que o diretório de destino existe
            caminho_destino.parent.mkdir(parents=True, exist_ok=True)

            # Mover arquivo
            shutil.copy2(caminho_origem, caminho_destino)
            movidos.append(f"{origem} -> {destino}")

        except Exception as e:
            erros.append(f"{origem}: {str(e)}")

    print(f"✓ {len(movidos)} arquivos movidos")
    if nao_encontrados:
        print(f"⚠ {len(nao_encontrados)} arquivos não encontrados")
    if erros:
        print(f"✗ {len(erros)} erros")

    return movidos, nao_encontrados, erros


def gerar_relatorio(movidos: List[str], nao_encontrados: List[str], erros: List[str]):
    """Gera relatório detalhado da reorganização"""
    relatorio_path = BASE_DIR / "scripts" / "relatorio_reorganizacao.txt"

    with open(relatorio_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("RELATÓRIO DE REORGANIZAÇÃO DE TEMPLATES\n")
        f.write("=" * 80 + "\n\n")

        f.write(f"Total de mapeamentos: {len(FILE_MAPPINGS)}\n")
        f.write(f"Arquivos movidos: {len(movidos)}\n")
        f.write(f"Arquivos não encontrados: {len(nao_encontrados)}\n")
        f.write(f"Erros: {len(erros)}\n\n")

        if movidos:
            f.write("=" * 80 + "\n")
            f.write("ARQUIVOS MOVIDOS COM SUCESSO\n")
            f.write("=" * 80 + "\n")
            for item in sorted(movidos):
                f.write(f"{item}\n")
            f.write("\n")

        if nao_encontrados:
            f.write("=" * 80 + "\n")
            f.write("ARQUIVOS NÃO ENCONTRADOS\n")
            f.write("=" * 80 + "\n")
            for item in sorted(nao_encontrados):
                f.write(f"{item}\n")
            f.write("\n")

        if erros:
            f.write("=" * 80 + "\n")
            f.write("ERROS\n")
            f.write("=" * 80 + "\n")
            for item in sorted(erros):
                f.write(f"{item}\n")
            f.write("\n")

        f.write("=" * 80 + "\n")
        f.write("MAPEAMENTO DE MUDANÇAS PARA ARQUIVOS PYTHON\n")
        f.write("=" * 80 + "\n")
        f.write("Substitua as seguintes referências nos arquivos .py:\n\n")

        for origem, destino in sorted(FILE_MAPPINGS.items()):
            f.write(f'"{origem}" -> "{destino}"\n')

    print(f"\n✓ Relatório gerado: {relatorio_path}")


def main():
    print("=" * 80)
    print("REORGANIZAÇÃO DE TEMPLATES - PROJETO OBRATTO")
    print("=" * 80)

    # Passo 1: Criar diretórios
    criar_diretorios()

    # Passo 2: Mover arquivos
    movidos, nao_encontrados, erros = mover_arquivos()

    # Passo 3: Gerar relatório
    gerar_relatorio(movidos, nao_encontrados, erros)

    print("\n" + "=" * 80)
    print("REORGANIZAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print("\nPRÓXIMOS PASSOS:")
    print("1. Verificar o relatório gerado em scripts/relatorio_reorganizacao.txt")
    print("2. Atualizar as referências nos arquivos Python das rotas")
    print("3. Remover as pastas antigas após confirmar que tudo funciona")
    print("4. Testar a aplicação")


if __name__ == "__main__":
    main()
