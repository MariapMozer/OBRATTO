document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.search-input');
    const filterSelect = document.querySelector('.filter-select');
    const prestadorCardsContainer = document.getElementById('prestador-cards');
    const fornecedorCardsContainer = document.getElementById('fornecedor-cards');

    // Função de filtro e busca (simulada)
    function filterAndSearch() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterValue = filterSelect.value;

        // Simulação de dados (substituir por chamada real à API)
        const allCards = [
            ...prestadorCardsContainer.querySelectorAll('.service-card'),
            ...fornecedorCardsContainer.querySelectorAll('.service-card')
        ];

        allCards.forEach(card => {
            const isPrestador = card.closest('#prestador-cards') !== null;
            const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
            const cardSubtitle = card.querySelector('.card-subtitle').textContent.toLowerCase();
            
            const matchesSearch = cardTitle.includes(searchTerm) || cardSubtitle.includes(searchTerm);
            
            let matchesFilter = true;
            if (filterValue === 'prestador' && !isPrestador) {
                matchesFilter = false;
            } else if (filterValue === 'fornecedor' && isPrestador) {
                matchesFilter = false;
            }

            if (matchesSearch && matchesFilter) {
                card.style.display = 'flex';
            } else {
                card.style.display = 'none';
            }
        });

        // Lógica para mostrar/esconder as seções inteiras
        const prestadorSection = prestadorCardsContainer.closest('.container').querySelector('h2:first-of-type');
        const fornecedorSection = fornecedorCardsContainer.closest('.container').querySelector('h2:nth-of-type(2)');

        if (filterValue === 'prestador') {
            prestadorCardsContainer.style.display = 'grid';
            fornecedorCardsContainer.style.display = 'none';
            prestadorSection.style.display = 'block';
            fornecedorSection.style.display = 'none';
        } else if (filterValue === 'fornecedor') {
            prestadorCardsContainer.style.display = 'none';
            fornecedorCardsContainer.style.display = 'grid';
            prestadorSection.style.display = 'none';
            fornecedorSection.style.display = 'block';
        } else { // 'all'
            prestadorCardsContainer.style.display = 'grid';
            fornecedorCardsContainer.style.display = 'grid';
            prestadorSection.style.display = 'block';
            fornecedorSection.style.display = 'block';
        }
    }

    searchInput.addEventListener('input', filterAndSearch);
    filterSelect.addEventListener('change', filterAndSearch);

    // Inicializa o filtro para garantir que todos estejam visíveis no carregamento
    filterAndSearch();
});