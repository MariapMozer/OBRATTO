/**
 * Service Worker Registration - OBRATTO
 * Registra o Service Worker para habilitar cache offline e PWA
 */

(function() {
    'use strict';

    // Verificar suporte a Service Workers
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            registerServiceWorker();
        });
    } else {
        console.log('Service Worker não suportado neste navegador');
    }

    /**
     * Registra o Service Worker
     */
    async function registerServiceWorker() {
        try {
            const registration = await navigator.serviceWorker.register(
                '/static/js/service-worker.js',
                { scope: '/' }
            );

            console.log('✅ Service Worker registrado com sucesso!');
            console.log('Scope:', registration.scope);

            // Verificar atualizações
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                console.log('🔄 Nova versão do Service Worker encontrada');

                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        // Novo Service Worker instalado, mas há um ativo
                        console.log('📦 Nova versão disponível! Recarregue a página para atualizar.');
                        showUpdateNotification();
                    }
                });
            });

            // Verificar atualizações periodicamente
            setInterval(() => {
                registration.update();
            }, 60000); // Verifica a cada 1 minuto

        } catch (error) {
            console.error('❌ Erro ao registrar Service Worker:', error);
        }
    }

    /**
     * Mostra notificação de atualização disponível
     */
    function showUpdateNotification() {
        // Verificar se a função de toast está disponível
        if (typeof window.showToast === 'function') {
            window.showToast(
                'Nova versão disponível! Recarregue a página para atualizar.',
                'info',
                5000
            );
        } else {
            // Fallback: criar banner simples
            const banner = document.createElement('div');
            banner.className = 'update-banner';
            banner.innerHTML = `
                <div style="position: fixed; top: 0; left: 0; right: 0; background: #0d6efd; color: white;
                            padding: 12px 20px; text-align: center; z-index: 9999; box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                    <strong>Nova versão disponível!</strong>
                    <button onclick="location.reload()" style="margin-left: 15px; padding: 4px 12px;
                            background: white; color: #0d6efd; border: none; border-radius: 4px; cursor: pointer;">
                        Atualizar Agora
                    </button>
                    <button onclick="this.parentElement.remove()" style="margin-left: 10px; padding: 4px 12px;
                            background: transparent; color: white; border: 1px solid white; border-radius: 4px; cursor: pointer;">
                        Depois
                    </button>
                </div>
            `;
            document.body.appendChild(banner);
        }
    }

    /**
     * Desregistra o Service Worker (útil para debug)
     */
    window.unregisterServiceWorker = async function() {
        if ('serviceWorker' in navigator) {
            const registrations = await navigator.serviceWorker.getRegistrations();
            for (const registration of registrations) {
                await registration.unregister();
                console.log('Service Worker desregistrado');
            }
        }
    };

    /**
     * Limpa todos os caches (útil para debug)
     */
    window.clearServiceWorkerCache = async function() {
        if ('caches' in window) {
            const cacheNames = await caches.keys();
            for (const cacheName of cacheNames) {
                await caches.delete(cacheName);
                console.log('Cache removido:', cacheName);
            }
            console.log('✅ Todos os caches foram limpos');
        }
    };

    /**
     * Status do Service Worker
     */
    window.serviceWorkerStatus = async function() {
        if ('serviceWorker' in navigator) {
            const registration = await navigator.serviceWorker.getRegistration();

            if (registration) {
                console.log('📊 Status do Service Worker:');
                console.log('- Registrado:', !!registration);
                console.log('- Scope:', registration.scope);
                console.log('- Ativo:', !!registration.active);
                console.log('- Instalando:', !!registration.installing);
                console.log('- Aguardando:', !!registration.waiting);

                // Listar caches
                const cacheNames = await caches.keys();
                console.log('- Caches ativos:', cacheNames.length);
                console.log('- Nomes dos caches:', cacheNames);
            } else {
                console.log('❌ Service Worker não registrado');
            }
        } else {
            console.log('❌ Service Worker não suportado');
        }
    };

    // Detectar quando está offline/online
    window.addEventListener('online', () => {
        console.log('🌐 Conexão restaurada');
        if (typeof window.showToast === 'function') {
            window.showToast('Conexão com a internet restaurada!', 'success', 3000);
        }
    });

    window.addEventListener('offline', () => {
        console.log('📵 Sem conexão');
        if (typeof window.showToast === 'function') {
            window.showToast('Você está offline. Algumas funcionalidades podem estar limitadas.', 'warning', 5000);
        }
    });

    console.log('📱 Service Worker registration script carregado');
})();
