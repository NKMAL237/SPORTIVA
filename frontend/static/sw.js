/**
 * SPORTIVA Service Worker v4 — Full Offline Support
 * 
 * Strategy:
 *  - Static assets  : Cache-First (CSS, JS, fonts, vendor libs)
 *  - HTML pages     : Network-First with full offline fallback + cache
 *  - POST requests  : Background Sync queue (IndexedDB) for offline form submissions
 *  - Images/Media   : Cache-First (serve stale, refresh in background)
 */

const CACHE_VERSION = 'sportiva-v4';
const OFFLINE_PAGE  = '/offline/';

const STATIC_ASSETS = [
  '/',
  OFFLINE_PAGE,
  '/events/',
  '/sponsorships/',
  '/media-feed/',
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
  '/static/vendor/leaflet/marker-shadow.png',
  // Sport banner SVGs — cached for offline event display
  '/static/images/events/trophy-football.svg',
  '/static/images/events/trophy-basketball.svg',
  '/static/images/events/trophy-athletics.svg',
  '/static/images/events/trophy-tennis.svg',
  '/static/images/events/trophy-volleyball.svg',
  '/static/images/events/trophy-swimming.svg',
  '/static/images/events/trophy-cycling.svg',
  '/static/images/events/trophy-cricket.svg',
  '/static/images/events/trophy-combat.svg',
  '/static/images/events/trophy-generic.svg',
];

// ──────────────────────────────────────────────────────────────────────────────
// INSTALL — pre-cache static shell
// ──────────────────────────────────────────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      console.log('[SW] Pre-caching static assets...');
      // Use addAll with individual catch so one failure doesn't kill the rest
      return Promise.allSettled(
        STATIC_ASSETS.map(url =>
          cache.add(url).catch(err => console.warn('[SW] Failed to cache:', url, err))
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// ──────────────────────────────────────────────────────────────────────────────
// ACTIVATE — clean up old caches
// ──────────────────────────────────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter(key => key !== CACHE_VERSION)
            .map(key => {
              console.log('[SW] Removing old cache:', key);
              return caches.delete(key);
            })
      );
    }).then(() => self.clients.claim())
  );
});

// ──────────────────────────────────────────────────────────────────────────────
// Helper: open the offline queue store in IndexedDB
// ──────────────────────────────────────────────────────────────────────────────
function openQueueDB() {
  return new Promise((resolve, reject) => {
    const req = indexedDB.open('sportiva-offline-queue', 1);
    req.onupgradeneeded = (e) => {
      e.target.result.createObjectStore('requests', { autoIncrement: true });
    };
    req.onsuccess = (e) => resolve(e.target.result);
    req.onerror = (e) => reject(e.target.error);
  });
}

async function enqueueRequest(request) {
  const db = await openQueueDB();
  const body = await request.text();
  const entry = {
    url: request.url,
    method: request.method,
    headers: [...request.headers.entries()],
    body,
    timestamp: Date.now(),
  };
  return new Promise((resolve, reject) => {
    const tx = db.transaction('requests', 'readwrite');
    tx.objectStore('requests').add(entry);
    tx.oncomplete = resolve;
    tx.onerror = (e) => reject(e.target.error);
  });
}

async function flushQueue() {
  const db = await openQueueDB();
  const tx = db.transaction('requests', 'readwrite');
  const store = tx.objectStore('requests');
  const allReq = store.getAll();
  const allKeys = store.getAllKeys();

  return new Promise((resolve) => {
    allReq.onsuccess = async () => {
      allKeys.onsuccess = async () => {
        const entries = allReq.result;
        const keys = allKeys.result;
        for (let i = 0; i < entries.length; i++) {
          const entry = entries[i];
          try {
            await fetch(entry.url, {
              method: entry.method,
              headers: Object.fromEntries(entry.headers),
              body: entry.body,
            });
            // Delete if successful
            db.transaction('requests', 'readwrite').objectStore('requests').delete(keys[i]);
            console.log('[SW] Flushed offline request:', entry.url);
          } catch {
            console.warn('[SW] Still offline, keeping queued request:', entry.url);
          }
        }
        resolve();
      };
    };
  });
}

// ──────────────────────────────────────────────────────────────────────────────
// BACKGROUND SYNC — replay queued form submissions on reconnect
// ──────────────────────────────────────────────────────────────────────────────
self.addEventListener('sync', (event) => {
  if (event.tag === 'sportiva-offline-forms') {
    console.log('[SW] Background sync: flushing offline form queue...');
    event.waitUntil(flushQueue());
  }
});

// ──────────────────────────────────────────────────────────────────────────────
// FETCH — smart routing
// ──────────────────────────────────────────────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests for caching; queue POST forms for offline sync
  if (request.method === 'POST') {
    event.respondWith(
      fetch(request.clone()).catch(async () => {
        // Offline — enqueue the form submission
        await enqueueRequest(request.clone());
        // Register background sync if available
        if (self.registration.sync) {
          self.registration.sync.register('sportiva-offline-forms');
        }
        // Return a synthetic "queued" response
        return new Response(
          JSON.stringify({ queued: true, message: 'Your action has been saved and will be submitted when you are back online.' }),
          { status: 202, headers: { 'Content-Type': 'application/json', 'X-Offline-Queued': '1' } }
        );
      })
    );
    return;
  }

  // Only handle GET requests below
  if (request.method !== 'GET') return;

  // ── Static assets: Cache-First ──
  if (url.pathname.startsWith('/static/') || url.pathname.startsWith('/media/')) {
    event.respondWith(
      caches.match(request).then((cached) => {
        if (cached) {
          // Refresh cache in background (stale-while-revalidate)
          fetch(request).then((fresh) => {
            if (fresh && fresh.status === 200) {
              caches.open(CACHE_VERSION).then(c => c.put(request, fresh));
            }
          }).catch(() => {});
          return cached;
        }
        return fetch(request).then((fresh) => {
          if (fresh && fresh.status === 200) {
            const clone = fresh.clone();
            caches.open(CACHE_VERSION).then(c => c.put(request, clone));
          }
          return fresh;
        }).catch(() => new Response('', { status: 408, statusText: 'Offline' }));
      })
    );
    return;
  }

  // ── HTML navigation: Network-First with cache fallback ──
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request)
        .then((fresh) => {
          if (fresh && fresh.status === 200) {
            const clone = fresh.clone();
            caches.open(CACHE_VERSION).then(c => c.put(request, clone));
          }
          return fresh;
        })
        .catch(async () => {
          const cached = await caches.match(request);
          if (cached) return cached;
          // Try to match the closest parent path
          const pathParts = url.pathname.split('/').filter(Boolean);
          while (pathParts.length > 0) {
            pathParts.pop();
            const parentUrl = '/' + pathParts.join('/') + '/';
            const parentCached = await caches.match(parentUrl);
            if (parentCached) return parentCached;
          }
          return caches.match(OFFLINE_PAGE);
        })
    );
    return;
  }

  // ── Default fallback ──
  event.respondWith(
    caches.match(request).then((cached) =>
      cached || fetch(request).catch(() =>
        new Response('', { status: 408, statusText: 'Offline' })
      )
    )
  );
});

// ──────────────────────────────────────────────────────────────────────────────
// MESSAGE — force update from client
// ──────────────────────────────────────────────────────────────────────────────
self.addEventListener('message', (event) => {
  if (event.data && event.data.action === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
