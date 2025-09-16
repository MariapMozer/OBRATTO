let tipoSelecionado = null;

document.addEventListener('DOMContentLoaded', function() {
    const tipoCards = document.querySelectorAll('.tipo-card');
    const btnContinuar = document.getElementById('btnContinuar');
    
    tipoCards.forEach(card => {
        card.addEventListener('click', function() {
            selecionarTipo(this);
        });
        
        card.addEventListener('mouseenter', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'translateY(-3px)';
            }
        });
        
        card.addEventListener('mouseleave', function() {
            if (!this.classList.contains('selected')) {
                this.style.transform = 'translateY(0)';
            }
        });
    });
    
    btnContinuar.addEventListener('click', function() {
        if (tipoSelecionado) {
            continuarCadastro();
        }
    });
    
    setTimeout(() => {
        document.querySelector('.selecao-container').classList.add('fade-in-up');
    }, 100);
});

function selecionarTipo(cardElement) {
    document.querySelectorAll('.tipo-card').forEach(card => {
        card.classList.remove('selected');
    });
    
    cardElement.classList.add('selected');
    
    tipoSelecionado = cardElement.getAttribute('data-tipo');
    
    const btnContinuar = document.getElementById('btnContinuar');
    btnContinuar.disabled = false;
    
    cardElement.style.transform = 'translateY(-5px) scale(1.02)';
    setTimeout(() => {
        cardElement.style.transform = 'translateY(-3px) scale(1)';
    }, 200);
    
    mostrarFeedbackSelecao(tipoSelecionado);
}

function mostrarFeedbackSelecao(tipo) {
    const tipoNomes = {
        'cliente': 'Cliente',
        'fornecedor': 'Fornecedor', 
        'prestador': 'Prestador de Serviços',
        'administrador': 'Administrador'
    };
    
    const feedback = document.createElement('div');
    feedback.className = 'feedback-selecao';
    feedback.innerHTML = `
        <i class="bi bi-check-circle-fill"></i>
        ${tipoNomes[tipo]} selecionado!
    `;
    
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #171370 0%, #E8894B 100%);
        color: white;
        padding: 12px 20px;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        box-shadow: 0 8px 20px rgba(23, 19, 112, 0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    
    document.body.appendChild(feedback);
    
    setTimeout(() => {
        feedback.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            document.body.removeChild(feedback);
        }, 300);
    }, 2000);
}

function continuarCadastro() {
    if (!tipoSelecionado) {
        alert('Por favor, selecione um tipo de usuário.');
        return;
    }
    
    const btnContinuar = document.getElementById('btnContinuar');
    const textoOriginal = btnContinuar.innerHTML;
    btnContinuar.innerHTML = '<i class="bi bi-hourglass-split"></i> Carregando...';
    btnContinuar.disabled = true;
    
    setTimeout(() => {
        const urlsCadastro = {
            'cliente': '/cadastro/cliente',
            'fornecedor': '/cadastro/fornecedor',
            'prestador': '/cadastro/prestador',
            'administrador': '/cadastro/administrador'
        };
        
        window.location.href = urlsCadastro[tipoSelecionado];
    }, 1500);
}

document.addEventListener('keydown', function(e) {
    const tipoCards = document.querySelectorAll('.tipo-card');
    const btnContinuar = document.getElementById('btnContinuar');
    
    if (e.key === 'ArrowRight' || e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'ArrowDown') {
        e.preventDefault();
        
        let currentIndex = -1;
        tipoCards.forEach((card, index) => {
            if (card.classList.contains('selected')) {
                currentIndex = index;
            }
        });
        
        let nextIndex;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
            nextIndex = (currentIndex + 1) % tipoCards.length;
        } else {
            nextIndex = currentIndex === -1 ? 0 : (currentIndex - 1 + tipoCards.length) % tipoCards.length;
        }
        
        selecionarTipo(tipoCards[nextIndex]);
        tipoCards[nextIndex].focus();
    }
    
    if (e.key === 'Enter' && tipoSelecionado && !btnContinuar.disabled) {
        continuarCadastro();
    }
});

document.addEventListener('DOMContentLoaded', function() {
    const tipoCards = document.querySelectorAll('.tipo-card');
    
    tipoCards.forEach((card, index) => {
        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Selecionar tipo de usuário: ${card.querySelector('h3').textContent}`);
        
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                selecionarTipo(this);
            }
        });
    });
});

const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .tipo-card:focus {
        outline: 2px solid #E8894B;
        outline-offset: 2px;
    }
`;
document.head.appendChild(style);

