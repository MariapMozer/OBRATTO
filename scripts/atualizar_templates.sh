#!/bin/bash

# Script para atualizar referencias de templates nos arquivos Python

echo "=========================================="
echo "Atualizando referencias de templates..."
echo "=========================================="

# Função para fazer substituição em um arquivo
substituir() {
    local arquivo="$1"
    local antigo="$2"
    local novo="$3"

    if grep -q "$antigo" "$arquivo" 2>/dev/null; then
        # Criar backup
        cp "$arquivo" "$arquivo.backup_reorganizacao" 2>/dev/null

        # Fazer substituição
        sed -i '' "s|$antigo|$novo|g" "$arquivo"
        echo "✓ $arquivo: $antigo -> $novo"
        return 0
    fi
    return 1
}

# Contador
total=0

# Processar todos os arquivos Python em routes
for arquivo in $(find routes -name "*.py" -type f); do
    modificado=0

    # Auth
    substituir "$arquivo" "publico/login_cadastro/login.html" "auth/login.html" && ((modificado++))
    substituir "$arquivo" "publico/login_cadastro/cadastro_sucesso.html" "auth/cadastro_sucesso.html" && ((modificado++))
    substituir "$arquivo" "publico/login_cadastro/recuperar_senha.html" "auth/recuperar_senha.html" && ((modificado++))
    substituir "$arquivo" "publico/login_cadastro/redefinir_senha.html" "auth/redefinir_senha.html" && ((modificado++))

    # Public
    substituir "$arquivo" "publico/home.html" "public/home.html" && ((modificado++))
    substituir "$arquivo" "publico/em_construcao.html" "public/em_construcao.html" && ((modificado++))
    substituir "$arquivo" "publico/fornecedor2/cadastro_fornecedor.html" "public/cadastro/fornecedor.html" && ((modificado++))
    substituir "$arquivo" "publico/fornecedor2/perfil_publico_fornecedor.html" "public/perfil/fornecedor.html" && ((modificado++))
    substituir "$arquivo" "publico/cliente/perfil_publico.html" "public/perfil/cliente.html" && ((modificado++))
    substituir "$arquivo" "publico/prestador/perfil_publico.html" "public/perfil/prestador.html" && ((modificado++))

    # Admin - Base
    substituir "$arquivo" "administrador/home_adm.html" "admin/dashboard.html" && ((modificado++))
    substituir "$arquivo" "administrador/base_admin.html" "base/admin.html" && ((modificado++))
    substituir "$arquivo" "administrador/perfil_editar.html" "admin/perfil_editar.html" && ((modificado++))
    substituir "$arquivo" "administrador/verificacao_usuario.html" "admin/verificacao_usuario.html" && ((modificado++))
    substituir "$arquivo" "administrador/em_construcao.html" "admin/em_construcao.html" && ((modificado++))

    # Admin - Usuários
    substituir "$arquivo" "administrador/listar_cliente.html" "admin/usuarios/clientes/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/listar_fornecedor.html" "admin/usuarios/fornecedores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_fornecedor/listar_fornecedor.html" "admin/usuarios/fornecedores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_fornecedor/moderar_produtos.html" "admin/usuarios/fornecedores/produtos.html" && ((modificado++))
    substituir "$arquivo" "administrador/listar_prestador.html" "admin/usuarios/prestadores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_prestador/listar_prestador.html" "admin/usuarios/prestadores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_prestador/moderar_servicos_prestador.html" "admin/usuarios/prestadores/servicos.html" && ((modificado++))
    substituir "$arquivo" "administrador/lista.html" "admin/usuarios/administradores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_adm/lista_adm.html" "admin/usuarios/administradores/listar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_adm/cadastrar_adm.html" "admin/usuarios/administradores/cadastrar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_adm/editar_adm.html" "admin/usuarios/administradores/editar.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_adm/remover_adm.html" "admin/usuarios/administradores/remover.html" && ((modificado++))

    # Admin - Moderação
    substituir "$arquivo" "administrador/moderar_anuncios.html" "admin/moderacao/anuncios.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_avaliacoes.html" "admin/moderacao/avaliacoes.html" && ((modificado++))
    substituir "$arquivo" "administrador/aprovar_profissionais.html" "admin/moderacao/aprovar_profissionais.html" && ((modificado++))
    substituir "$arquivo" "administrador/avaliar_profissionais.html" "admin/moderacao/avaliar_profissionais.html" && ((modificado++))
    substituir "$arquivo" "administrador/remover_avaliacoes.html" "admin/moderacao/remover_avaliacoes.html" && ((modificado++))
    substituir "$arquivo" "administrador/moderar_chat.html" "admin/moderacao/chat.html" && ((modificado++))

    # Admin - Relatórios
    substituir "$arquivo" "administrador/visualizar_relatorios.html" "admin/relatorios/visualizar.html" && ((modificado++))
    substituir "$arquivo" "administrador/relatorios_anuncios.html" "admin/relatorios/anuncios.html" && ((modificado++))
    substituir "$arquivo" "administrador/exportar_relatorios.html" "admin/relatorios/exportar.html" && ((modificado++))

    # Admin - Configurações
    substituir "$arquivo" "administrador/ajustar_configuracoes.html" "admin/configuracoes/ajustar.html" && ((modificado++))
    substituir "$arquivo" "administrador/configurar_seguranca.html" "admin/configuracoes/seguranca.html" && ((modificado++))

    # Admin - Serviços
    substituir "$arquivo" "administrador/servico/galeria.html" "admin/servicos/galeria.html" && ((modificado++))

    # Fornecedor
    substituir "$arquivo" "fornecedor/home_fornecedor.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/base.html" "base/fornecedor.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/avaliacoes_recebidas.html" "fornecedor/avaliacoes/recebidas.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/mensagens/mensagens_recebidas.html" "fornecedor/mensagens/recebidas.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/orcamentos/orcamento.html" "fornecedor/orcamentos/detalhes.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/orcamentos/responder_orcamentos.html" "fornecedor/orcamentos/responder.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/orcamentos/solicitacoes_recebidas.html" "fornecedor/orcamentos/recebidas.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/listar_planos.html" "fornecedor/planos/listar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/assinar_plano.html" "fornecedor/planos/assinar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/alterar_plano.html" "fornecedor/planos/alterar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/cancelar_plano.html" "fornecedor/planos/cancelar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/confirmacao_cancelamento_plano.html" "fornecedor/planos/confirmar_cancelamento.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/histórico_planos.html" "fornecedor/planos/historico.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/planos/renovar_plano.html" "fornecedor/planos/renovar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/produtos/cadastrar_produtos.html" "fornecedor/produtos/cadastrar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/produtos/alterar_produtos.html" "fornecedor/produtos/alterar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/produtos/excluir_produtos.html" "fornecedor/produtos/excluir.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/promocao/cadastrar_promocoes.html" "fornecedor/promocoes/cadastrar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/promocao/alterar_promocoes.html" "fornecedor/promocoes/alterar.html" && ((modificado++))
    substituir "$arquivo" "fornecedor/promocao/confirmar_exclusao_promocao.html" "fornecedor/promocoes/confirmar_exclusao.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento/dados_pagamento.html" "fornecedor/pagamento/dados.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento/processar_pagamento.html" "fornecedor/pagamento/processar.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento/pagamento_sucesso.html" "fornecedor/pagamento/sucesso.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento/pagamento_erro.html" "fornecedor/pagamento/erro.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento/pagamento_pendente.html" "fornecedor/pagamento/pendente.html" && ((modificado++))

    # Prestador
    substituir "$arquivo" "prestador/prestador_logout.html" "prestador/logout.html" && ((modificado++))
    substituir "$arquivo" "prestador/agenda/agenda.html" "prestador/agenda/calendario.html" && ((modificado++))
    substituir "$arquivo" "prestador/catalogo/catalogo_prestadores.html" "prestador/catalogo/listar.html" && ((modificado++))
    substituir "$arquivo" "prestador/perfil/perfil.html" "prestador/perfil/visualizar.html" && ((modificado++))
    substituir "$arquivo" "prestador/perfil/foto/dados.html" "prestador/perfil/editar_fotos.html" && ((modificado++))
    substituir "$arquivo" "prestador/planos/planos.html" "prestador/planos/listar.html" && ((modificado++))
    substituir "$arquivo" "prestador/servicos/editar_servico.html" "prestador/servicos/editar.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento-prestador/dados_pagamento.html" "prestador/pagamento/dados.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento-prestador/processar_pagamento.html" "prestador/pagamento/processar.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento-prestador/pagamento_sucesso.html" "prestador/pagamento/sucesso.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento-prestador/pagamento_erro.html" "prestador/pagamento/erro.html" && ((modificado++))
    substituir "$arquivo" "publico/pagamento-prestador/pagamento_pendente.html" "prestador/pagamento/pendente.html" && ((modificado++))

    # Cliente
    substituir "$arquivo" "cliente/base.html" "base/cliente.html" && ((modificado++))
    substituir "$arquivo" "cliente/cliente_logout.html" "cliente/logout.html" && ((modificado++))

    # Avaliações
    substituir "$arquivo" "avaliacao/listar.html" "avaliacoes/listar.html" && ((modificado++))
    substituir "$arquivo" "avaliacao/nova.html" "avaliacoes/nova.html" && ((modificado++))
    substituir "$arquivo" "avaliacao/editar.html" "avaliacoes/editar.html" && ((modificado++))
    substituir "$arquivo" "avaliacao/detalhes.html" "avaliacoes/detalhes.html" && ((modificado++))

    if [ $modificado -gt 0 ]; then
        ((total += modificado))
    fi
done

# Processar também util/exception_handlers.py
for arquivo in util/exception_handlers.py util/error_handlers.py; do
    if [ -f "$arquivo" ]; then
        substituir "$arquivo" "errors/404.html" "errors/404.html"
        substituir "$arquivo" "errors/500.html" "errors/500.html"
    fi
done

echo ""
echo "=========================================="
echo "Concluído!"
echo "Total de substituições: $total"
echo "=========================================="
echo ""
echo "Backups criados com extensão .backup_reorganizacao"
