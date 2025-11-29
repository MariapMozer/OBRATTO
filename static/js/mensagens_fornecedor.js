/**
 * Script para a página de Mensagens do Fornecedor
 * Inclui funcionalidades de filtro, ações e interatividade
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeMessagePage();
});

/**
 * Inicializa a página de mensagens
 */
function initializeMessagePage() {
    setupMessageItemClickHandlers();
    setupActionButtons();
    setupFilterButton();
    setupModal();
}

/**
 * Setup dos cliques em itens de mensagem
 */
function setupMessageItemClickHandlers() {
    const messageItems = document.querySelectorAll('.mensagem-item');
    
    messageItems.forEach(item => {
        item.addEventListener('click', function(e) {
            // Não abrir se clicou nos botões de ação
            if (e.target.closest('.mensagem-actions')) {
                return;
            }
            
            const msgId = this.getAttribute('data-msg-id');
            if (msgId) {
                // Abrir a conversa/mensagem
                openMessage(msgId);
            }
        });
    });
}

/**
 * Setup dos botões de ação (favoritar, arquivar, deletar)
 */
function setupActionButtons() {
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.btn-action');
        if (!btn) return;

        const msgItem = btn.closest('.mensagem-item');
        const msgId = msgItem.getAttribute('data-msg-id');

        if (btn.querySelector('.bi-star')) {
            // Favoritar
            handleFavorite(btn, msgId);
        } else if (btn.querySelector('.bi-archive')) {
            // Arquivar
            handleArchive(msgItem, msgId);
        } else if (btn.querySelector('.bi-trash')) {
            // Deletar
            handleDelete(msgItem, msgId);
        }
    });
}

/**
 * Marca uma mensagem como favorita
 */
function handleFavorite(btn, msgId) {
    btn.classList.toggle('active');
    const icon = btn.querySelector('i');
    
    if (btn.classList.contains('active')) {
        icon.classList.remove('bi-star');
        icon.classList.add('bi-star-fill');
        showToast('Adicionado aos favoritos', 'success');
    } else {
        icon.classList.remove('bi-star-fill');
        icon.classList.add('bi-star');
        showToast('Removido dos favoritos', 'info');
    }
}

/**
 * Arquiva uma mensagem
 */
function handleArchive(msgItem, msgId) {
    // Transição suave
    msgItem.style.opacity = '0.5';
    msgItem.style.transform = 'translateX(20px)';
    
    setTimeout(() => {
        msgItem.style.display = 'none';
        showToast('Mensagem arquivada', 'success');
    }, 300);
}

/**
 * Deleta uma mensagem
 */
function handleDelete(msgItem, msgId) {
    if (confirm('Tem certeza que deseja deletar esta mensagem?')) {
        msgItem.style.opacity = '0';
        msgItem.style.transform = 'translateX(-100%)';
        
        setTimeout(() => {
            msgItem.remove();
            showToast('Mensagem deletada', 'success');
            
            // Verifica se não há mais mensagens
            checkEmptyList();
        }, 300);
    }
}

/**
 * Verifica se a lista está vazia
 */
function checkEmptyList() {
    const msgList = document.querySelector('.mensagens-list');
    if (msgList && msgList.children.length === 0) {
        const tabContent = msgList.closest('.tab-pane');
        if (tabContent) {
            msgList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-state-icon">
                        <i class="bi bi-inbox"></i>
                    </div>
                    <h5>Nenhuma mensagem</h5>
                    <p>Todas as mensagens foram deletadas ou arquivadas.</p>
                </div>
            `;
        }
    }
}

/**
 * Abre uma mensagem/conversa
 */
function openMessage(msgId) {
    console.log('Abrindo mensagem:', msgId);
    // Aqui você pode fazer redirecionamento ou abrir um modal
    // window.location.href = `/fornecedor/mensagens/${msgId}`;
    showToast('Funcionalidade em desenvolvimento', 'info');
}

/**
 * Setup do botão de filtro
 */
function setupFilterButton() {
    const btnFiltro = document.getElementById('btnFiltro');
    if (btnFiltro) {
        btnFiltro.addEventListener('click', function() {
            showFilterMenu();
        });
    }
}

/**
 * Mostra menu de filtros
 */
function showFilterMenu() {
    // Aqui você pode implementar um dropdown de filtros
    console.log('Mostrando menu de filtros');
    showToast('Menu de filtros em desenvolvimento', 'info');
}

/**
 * Setup da modal de nova conversa
 */
function setupModal() {
    const searchInput = document.getElementById('destinatario');
    const searchList = document.getElementById('destinatarioList');
    const modal = document.getElementById('novaConversaModal');
    const form = modal.querySelector('form');

    if (searchInput) {
        // Buscar destinatários enquanto digita
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            
            if (query.length < 2) {
                searchList.style.display = 'none';
                return;
            }
            
            searchDestinatariu(query);
        });
    }

    if (form) {
        form.addEventListener('submit', handleModalSubmit);
    }

    // Limpar modal ao fechar
    const modalElement = new bootstrap.Modal(modal);
    modal.addEventListener('hidden.bs.modal', function() {
        form.reset();
        searchList.style.display = 'none';
    });
}

/**
 * Busca destinatários (simulado)
 */
function searchDestinatariu(query) {
    const searchList = document.getElementById('destinatarioList');
    const searchInput = document.getElementById('destinatario');
    
    // Simulando resultados de busca
    // Em produção, isso seria uma chamada AJAX
    const resultados = [
        { id: 1, nome: 'João Silva', email: 'joao@email.com' },
        { id: 2, nome: 'Maria Santos', email: 'maria@email.com' },
        { id: 3, nome: 'Pedro Costa', email: 'pedro@email.com' },
    ].filter(u => 
        u.nome.toLowerCase().includes(query.toLowerCase()) ||
        u.email.toLowerCase().includes(query.toLowerCase())
    );

    if (resultados.length > 0) {
        searchList.innerHTML = resultados.map(u => `
            <button type="button" class="list-group-item list-group-item-action" 
                    data-user-id="${u.id}" data-user-name="${u.nome}">
                <div class="d-flex align-items-center">
                    <i class="bi bi-person-circle me-2"></i>
                    <div>
                        <div class="fw-bold">${u.nome}</div>
                        <small class="text-muted">${u.email}</small>
                    </div>
                </div>
            </button>
        `).join('');
        
        searchList.style.display = 'block';
        
        // Setup cliques em resultados
        searchList.querySelectorAll('.list-group-item').forEach(btn => {
            btn.addEventListener('click', function() {
                searchInput.value = this.getAttribute('data-user-name');
                searchInput.setAttribute('data-user-id', this.getAttribute('data-user-id'));
                searchList.style.display = 'none';
                searchInput.focus();
            });
        });
    } else {
        searchList.innerHTML = `
            <div class="list-group-item text-muted text-center py-3">
                Nenhum usuário encontrado
            </div>
        `;
        searchList.style.display = 'block';
    }
}

/**
 * Submissão do formulário da modal
 */
function handleModalSubmit(e) {
    e.preventDefault();
    
    const destinatario = document.getElementById('destinatario');
    const conteudo = document.getElementById('conteudo');
    const userId = destinatario.getAttribute('data-user-id');
    
    if (!userId) {
        showToast('Selecione um destinatário válido', 'warning');
        return;
    }
    
    if (!conteudo.value.trim()) {
        showToast('Digite uma mensagem', 'warning');
        return;
    }
    
    // Desabilitar botão de envio
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i> Enviando...';
    
    // Simular envio
    setTimeout(() => {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
        
        // Fechar modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('novaConversaModal'));
        modal.hide();
        
        showToast('Mensagem enviada com sucesso!', 'success');
    }, 1000);
}

/**
 * Mostra um toast/notificação
 */
function showToast(message, type = 'info') {
    // Criar container de toast se não existir
    let toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toastContainer';
        toastContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 400px;
        `;
        document.body.appendChild(toastContainer);
    }

    // Criar elemento toast
    const toastEl = document.createElement('div');
    const alertClass = `alert-${type === 'success' ? 'success' : type === 'danger' ? 'danger' : type === 'warning' ? 'warning' : 'info'}`;
    const icon = type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle';
    
    toastEl.innerHTML = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" style="margin-bottom: 0; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <i class="bi bi-${icon} me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toastEl);

    // Auto remover após 5 segundos
    setTimeout(() => {
        toastEl.style.opacity = '0';
        toastEl.style.transform = 'translateY(-20px)';
        toastEl.style.transition = 'all 0.3s ease';
        
        setTimeout(() => {
            toastEl.remove();
        }, 300);
    }, 5000);
}

/**
 * Utilitários
 */

// Formatar data relativa (ex: "há 2 horas")
function formatDateRelative(date) {
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Agora';
    if (diffMins < 60) return `há ${diffMins}m`;
    
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `há ${diffHours}h`;
    
    const diffDays = Math.floor(diffHours / 24);
    if (diffDays < 7) return `há ${diffDays}d`;
    
    return date.toLocaleDateString('pt-BR');
}

// Export para uso global se necessário
window.mensagensApp = {
    showToast,
    formatDateRelative,
    openMessage
};
