document.addEventListener("DOMContentLoaded", function() {
    const carousels = document.querySelectorAll('.carousel');

    carousels.forEach(carousel => {
        // Inicializa o carrossel sem autoplay
        const carouselInstance = new bootstrap.Carousel(carousel, {
            interval: false, // nunca girar sozinho
            ride: false
        });

        // Garante que ele esteja pausado imediatamente
        carouselInstance.pause();
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const carousels = document.querySelectorAll('.carousel');
    const cardsPerSlide = 3; // quantos cards aparecem por slide

    carousels.forEach(carousel => {
        const totalCards = carousel.querySelectorAll('.carousel-item').length;

        if (totalCards > cardsPerSlide) {
            // Mais que 3 cards â†’ inicializa carrossel manual
            const carouselInstance = new bootstrap.Carousel(carousel, {
                interval: false,
                ride: false
            });
            carouselInstance.pause();

            // garante que as setas estejam visÃ­veis
            const prev = carousel.querySelector('.carousel-control-prev');
            const next = carousel.querySelector('.carousel-control-next');
            if(prev) prev.style.display = 'flex';
            if(next) next.style.display = 'flex';

        } else {
            // 3 ou menos cards â†’ mantÃ©m estÃ¡tico
            const prev = carousel.querySelector('.carousel-control-prev');
            const next = carousel.querySelector('.carousel-control-next');
            if(prev) prev.style.display = 'none';
            if(next) next.style.display = 'none';

            // garante que todos os cards fiquem visÃ­veis
            const cards = carousel.querySelectorAll('.carousel-item');
            cards.forEach(card => {
                card.classList.add('active');
                card.style.display = 'block';
            });
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        new bootstrap.Carousel(carousel, { interval: false });
    });
});
