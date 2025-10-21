/**
 * Service Worker - OBRATTO
 * Implementa cache offline e estratégias de caching para PWA
 */

const CACHE_NAME = 'obratto-cache-v1';
const RUNTIME_CACHE = 'obratto-runtime-v1';

// Recursos críticos para cache na instalação
const PRECACHE_URLS = [
    '/static/css/components.min.css',
    '/static/css/components.css',
    '/static/css/toasts.css',
    '/static/js/lazy-load.js',
    '/static/js/toasts.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css'
];

// Instalação do Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando...');

    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Pre-caching recursos críticos');
                return cache.addAll(PRECACHE_URLS);
            })
            .then(() => self.skipWaiting())
    );
});

// Ativação do Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Ativando...');

    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    // Limpar caches antigos
                    if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                        console.log('[Service Worker] Removendo cache antigo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Interceptação de requisições
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Ignorar requisições cross-origin (exceto CDNs conhecidos)
    const isLocalOrigin = url.origin === location.origin;
    const isCDN = url.hostname.includes('jsdelivr.net') || url.hostname.includes('cdn.');

    if (!isLocalOrigin && !isCDN) {
        return;
    }

    // Ignorar requisições POST/PUT/DELETE
    if (request.method !== 'GET') {
        return;
    }

    // Estratégia de cache baseada no tipo de recurso
    if (isStaticAsset(request)) {
        // Cache First para assets estáticos
        event.respondWith(cacheFirst(request));
    } else if (isAPIRequest(url)) {
        // Network First para API
        event.respondWith(networkFirst(request));
    } else {
        // Network First com fallback para HTML
        event.respondWith(networkFirstWithFallback(request));
    }
});

/**
 * Verifica se a requisição é de um asset estático
 */
function isStaticAsset(request) {
    const destination = request.destination;
    return destination === 'style' ||
           destination === 'script' ||
           destination === 'image' ||
           destination === 'font';
}

/**
 * Verifica se é requisição de API
 */
function isAPIRequest(url) {
    return url.pathname.startsWith('/api/');
}

/**
 * Estratégia: Cache First
 * Usa cache se disponível, busca na rede caso contrário
 */
async function cacheFirst(request) {
    const cachedResponse = await caches.match(request);

    if (cachedResponse) {
        console.log('[Service Worker] Cache hit:', request.url);
        return cachedResponse;
    }

    console.log('[Service Worker] Cache miss, buscando na rede:', request.url);

    try {
        const networkResponse = await fetch(request);

        // Clonar a resposta antes de cachear
        const responseToCache = networkResponse.clone();

        // Cachear apenas respostas bem-sucedidas
        if (networkResponse.ok) {
            const cache = await caches.open(RUNTIME_CACHE);
            cache.put(request, responseToCache);
        }

        return networkResponse;
    } catch (error) {
        console.error('[Service Worker] Erro ao buscar na rede:', error);

        // Fallback para imagem placeholder se disponível
        if (request.destination === 'image') {
            return caches.match('/static/img/placeholder.png');
        }

        throw error;
    }
}

/**
 * Estratégia: Network First
 * Prioriza rede, usa cache como fallback
 */
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);

        // Cachear resposta se bem-sucedida
        if (networkResponse.ok) {
            const cache = await caches.open(RUNTIME_CACHE);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('[Service Worker] Rede indisponível, usando cache:', request.url);

        const cachedResponse = await caches.match(request);

        if (cachedResponse) {
            return cachedResponse;
        }

        throw error;
    }
}

/**
 * Estratégia: Network First com Fallback
 * Para páginas HTML
 */
async function networkFirstWithFallback(request) {
    try {
        const networkResponse = await fetch(request);

        // Cachear resposta HTML se bem-sucedida
        if (networkResponse.ok && networkResponse.headers.get('content-type')?.includes('text/html')) {
            const cache = await caches.open(RUNTIME_CACHE);
            cache.put(request, networkResponse.clone());
        }

        return networkResponse;
    } catch (error) {
        console.log('[Service Worker] Rede indisponível:', request.url);

        // Tentar cache primeiro
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }

        // Fallback para página offline se disponível
        const offlinePage = await caches.match('/offline.html');
        if (offlinePage) {
            return offlinePage;
        }

        throw error;
    }
}

// Background Sync para requisições falhadas (opcional)
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-messages') {
        console.log('[Service Worker] Sincronizando mensagens pendentes...');
        event.waitUntil(syncPendingMessages());
    }
});

async function syncPendingMessages() {
    // Implementar lógica de sincronização
    // Por exemplo, enviar mensagens que falharam quando offline
    console.log('[Service Worker] Sincronização de mensagens completa');
}

// Notificações Push (opcional para futuras funcionalidades)
self.addEventListener('push', (event) => {
    console.log('[Service Worker] Push recebido:', event);

    const options = {
        body: event.data ? event.data.text() : 'Nova notificação',
        icon: '/static/img/logo.png',
        badge: '/static/img/badge.png',
        vibrate: [200, 100, 200]
    };

    event.waitUntil(
        self.registration.showNotification('Obratto', options)
    );
});

// Clique em notificação
self.addEventListener('notificationclick', (event) => {
    console.log('[Service Worker] Notificação clicada:', event);

    event.notification.close();

    event.waitUntil(
        clients.openWindow('/')
    );
});

console.log('[Service Worker] Registrado com sucesso!');
