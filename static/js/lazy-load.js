/**
 * Lazy Loading Module - OBRATTO
 * Otimiza carregamento de imagens e componentes pesados
 */

(function() {
    'use strict';

    /**
     * Lazy Loading de Imagens
     * Usa Intersection Observer para carregar imagens quando entrarem no viewport
     */
    function initLazyImages() {
        const lazyImages = document.querySelectorAll('img[data-src], img[loading="lazy"]');

        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;

                        // Carregar imagem se tiver data-src
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }

                        // Adicionar classe de carregado
                        img.classList.add('lazy-loaded');

                        // Parar de observar esta imagem
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px', // Começa a carregar 50px antes de entrar no viewport
                threshold: 0.01
            });

            lazyImages.forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback para navegadores sem suporte
            lazyImages.forEach(img => {
                if (img.dataset.src) {
                    img.src = img.dataset.src;
                }
            });
        }
    }

    /**
     * Lazy Loading de Componentes Pesados
     * Carrega componentes sob demanda (chat, timeline, tabelas grandes)
     */
    function initLazyComponents() {
        const lazyComponents = document.querySelectorAll('[data-lazy-component]');

        if (!lazyComponents.length) return;

        const componentObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    const componentType = element.dataset.lazyComponent;

                    loadComponent(element, componentType);
                    observer.unobserve(element);
                }
            });
        }, {
            rootMargin: '100px 0px',
            threshold: 0.01
        });

        lazyComponents.forEach(component => {
            componentObserver.observe(component);
        });
    }

    /**
     * Carrega um componente específico
     */
    function loadComponent(element, componentType) {
        const loadingHTML = `
            <div class="text-center py-4">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                    <span class="visually-hidden">Carregando...</span>
                </div>
                <p class="text-muted small mt-2">Carregando componente...</p>
            </div>
        `;

        element.innerHTML = loadingHTML;

        // Simular carregamento (substituir com fetch real se necessário)
        setTimeout(() => {
            element.classList.add('component-loaded');
            element.removeAttribute('data-lazy-component');

            // Disparar evento customizado para notificar que o componente foi carregado
            const event = new CustomEvent('componentLoaded', {
                detail: { componentType, element }
            });
            document.dispatchEvent(event);
        }, 100);
    }

    /**
     * Lazy Loading de Background Images (CSS)
     */
    function initLazyBackgrounds() {
        const lazyBackgrounds = document.querySelectorAll('[data-bg]');

        if (!lazyBackgrounds.length) return;

        const bgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    element.style.backgroundImage = `url('${element.dataset.bg}')`;
                    element.removeAttribute('data-bg');
                    observer.unobserve(element);
                }
            });
        }, {
            rootMargin: '50px 0px'
        });

        lazyBackgrounds.forEach(bg => {
            bgObserver.observe(bg);
        });
    }

    /**
     * Lazy Loading de Iframes (vídeos, mapas)
     */
    function initLazyIframes() {
        const lazyIframes = document.querySelectorAll('iframe[data-src]');

        if (!lazyIframes.length) return;

        const iframeObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const iframe = entry.target;
                    iframe.src = iframe.dataset.src;
                    iframe.removeAttribute('data-src');
                    observer.unobserve(iframe);
                }
            });
        }, {
            rootMargin: '100px 0px'
        });

        lazyIframes.forEach(iframe => {
            iframeObserver.observe(iframe);
        });
    }

    /**
     * Preload de recursos críticos
     */
    function preloadCriticalResources() {
        // Preload de fontes críticas
        const criticalFonts = [
            '/static/webfonts/bootstrap-icons.woff2'
        ];

        criticalFonts.forEach(fontUrl => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = 'font';
            link.type = 'font/woff2';
            link.crossOrigin = 'anonymous';
            link.href = fontUrl;
            document.head.appendChild(link);
        });
    }

    /**
     * Debounce helper para otimizar eventos de scroll/resize
     */
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Inicialização
     */
    function init() {
        // Verificar se document está pronto
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        // Inicializar todos os lazy loaders
        initLazyImages();
        initLazyComponents();
        initLazyBackgrounds();
        initLazyIframes();
        preloadCriticalResources();

        // Re-observar novos elementos adicionados dinamicamente
        const observer = new MutationObserver(debounce(() => {
            initLazyImages();
            initLazyComponents();
            initLazyBackgrounds();
            initLazyIframes();
        }, 300));

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        console.log('✅ Lazy loading inicializado');
    }

    // Inicializar
    init();

    // Expor API pública
    window.LazyLoad = {
        refresh: function() {
            initLazyImages();
            initLazyComponents();
            initLazyBackgrounds();
            initLazyIframes();
        }
    };
})();
