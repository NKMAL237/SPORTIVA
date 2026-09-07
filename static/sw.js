const CACHE_NAME = 'sportiva-global-v2';

const STATIC_ASSETS = [
  '/',
  '/offline/',
  '/api/sports-news/',
  '/static/css/styles.css',
  '/static/fonts/fonts.css',
  '/static/js/app.js',
  '/static/js/offline-map.js',
  '/static/js/location-modal.js',
  '/static/manifest.json',
  '/static/vendor/tailwind/tailwind.js',
  '/static/vendor/fontawesome/css/all.min.css',
  '/static/vendor/fontawesome/webfonts/fa-solid-900.woff2',
  '/static/vendor/fontawesome/webfonts/fa-regular-400.woff2',
  '/static/vendor/fontawesome/webfonts/fa-brands-400.woff2',
  '/static/vendor/leaflet/leaflet.css',
  '/static/vendor/leaflet/leaflet.js',
  '/static/vendor/leaflet/marker-icon.png',
  '/static/vendor/leaflet/marker-icon-2x.png',
  '/static/vendor/leaflet/marker-shadow.png'
];


// Install Event: Pre-cache static shell & assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Pre-caching static assets for offline usage');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[Service Worker] Some assets failed to pre-cache:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up old caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Network-first for dynamic navigation, Cache-first for static assets
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // Ignore non-GET requests or admin / auth POST requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle Static files (Cache First, falling back to network)
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) {
          return cachedResponse;
        }
        return fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return networkResponse;
        });
      })
    );
    return;
  }

  // Handle Navigation / HTML pages (Network First, falling back to cache & offline page)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const responseClone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, responseClone);
            });
          }
          return networkResponse;
        })
        .catch(async () => {
          const cachedResponse = await caches.match(request);
          if (cachedResponse) {
            return cachedResponse;
          }
          return caches.match('/offline/');
        })
    );
    return;
  }

  // Default fallback for other GET requests
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      return cachedResponse || fetch(request).catch(() => {
        // Return null/empty if resource is unreachable offline
        return new Response('', { status: 408, statusText: 'Offline' });
      });
    })
  );
});
