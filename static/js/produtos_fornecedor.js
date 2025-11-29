/**
 * Script para a página de Produtos do Fornecedor
 * Inclui funcionalidades de filtro, busca e visualização
 */

document.addEventListener('DOMContentLoaded', function() {
    initializeProductsPage();
});

/**
 * Inicializa a página de produtos
 */
function initializeProductsPage() {
    setupSearchInput();
    setupSortSelect();
}

/**
 * Setup do input de busca
 */
function setupSearchInput() {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(filterProducts, 300));
    }
}

/**
 * Setup do select de ordenação
 */
function setupSortSelect() {
    const sortSelect = document.getElementById('sortSelect');
    if (sortSelect) {
        sortSelect.addEventListener('change', filterProducts);
    }
}

/**
 * Filtra e ordena os produtos
 */
function filterProducts() {
    const searchInput = document.getElementById('searchInput');
    const sortSelect = document.getElementById('sortSelect');
    const productGrid = document.getElementById('productsGrid');

    if (!productGrid) return;

    const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
    const sortValue = sortSelect ? sortSelect.value : 'name-asc';
    
    let items = Array.from(productGrid.querySelectorAll('.product-item'));

    // Filtrar por busca
    items = items.filter(item => {
        const productName = item.getAttribute('data-product-name').toLowerCase();
        return productName.includes(searchTerm);
    });

    // Ordenar
    items.sort((a, b) => {
        const nameA = a.getAttribute('data-product-name');
        const nameB = b.getAttribute('data-product-name');
        const priceA = parseFloat(a.getAttribute('data-product-price')) || 0;
        const priceB = parseFloat(b.getAttribute('data-product-price')) || 0;

        switch (sortValue) {
            case 'name-asc':
                return nameA.localeCompare(nameB);
            case 'name-desc':
                return nameB.localeCompare(nameA);
            case 'price-asc':
                return priceA - priceB;
            case 'price-desc':
                return priceB - priceA;
            case 'newest':
                return 0; // Mantém ordem original
            default:
                return 0;
        }
    });

    // Remover todos os itens
    items.forEach(item => item.remove());

    // Re-adicionar itens ordenados
    if (items.length > 0) {
        items.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.05}s`;
            productGrid.appendChild(item);
        });
    } else {
        // Mostrar mensagem de nenhum resultado
        showNoResults();
    }
}

/**
 * Mostra mensagem de nenhum resultado
 */
function showNoResults() {
    const productGrid = document.getElementById('productsGrid');
    if (!productGrid) return;

    const noResults = document.createElement('div');
    noResults.className = 'col-12';
    noResults.innerHTML = `
        <div class="empty-state" style="margin-top: 2rem;">
            <div class="empty-state-icon">
                <i class="bi bi-search"></i>
            </div>
            <h5>Nenhum produto encontrado</h5>
            <p>Tente refinar sua busca ou limpar os filtros.</p>
        </div>
    `;
    productGrid.appendChild(noResults);
}

/**
 * Muda a visualização entre grade e lista
 */
function changeView(view) {
    const productGrid = document.getElementById('productsGrid');
    if (!productGrid) return;

    if (view === 'list') {
        productGrid.classList.add('list-view');
    } else {
        productGrid.classList.remove('list-view');
    }

    // Salvar preferência no localStorage
    localStorage.setItem('productView', view);
}

/**
 * Carrega a visualização salva
 */
function loadSavedView() {
    const savedView = localStorage.getItem('productView') || 'grid';
    
    if (savedView === 'list') {
        document.getElementById('viewList').checked = true;
        changeView('list');
    } else {
        document.getElementById('viewGrid').checked = true;
        changeView('grid');
    }
}

/**
 * Debounce function para melhorar performance
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func(...args), delay);
    };
}

/**
 * Funções auxiliares
 */

// Formatar preço em Reais
function formatPrice(price) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(price);
}

// Truncar texto
function truncateText(text, maxLength) {
    if (text.length > maxLength) {
        return text.substring(0, maxLength) + '...';
    }
    return text;
}

// Carregar view ao inicializar
if (document.readyState !== 'loading') {
    loadSavedView();
} else {
    document.addEventListener('DOMContentLoaded', loadSavedView);
}

// Export para uso global
window.productsApp = {
    filterProducts,
    changeView,
    formatPrice,
    truncateText
};
