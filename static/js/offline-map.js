/**
 * Sportiva CM — Offline-Ready Map & Geolocation Helper
 * Works 100% offline locally without external CDN or tile server dependencies.
 */

(function() {
  // 1. Configure Leaflet default icons to local static files
  if (window.L && window.L.Icon && window.L.Icon.Default) {
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: '/static/vendor/leaflet/marker-icon-2x.png',
      iconUrl: '/static/vendor/leaflet/marker-icon.png',
      shadowUrl: '/static/vendor/leaflet/marker-shadow.png',
    });
  }

  // 2. Global helper to initialize a resilient map
  window.createSportivaMap = function(containerId, centerCoords, zoomLevel) {
    if (!window.L) {
      console.warn("Leaflet is not loaded.");
      return null;
    }

    var mapElement = document.getElementById(containerId);
    if (!mapElement) return null;

    var coords = centerCoords || [5.3696, 12.9231]; // Default to Cameroon center
    var zoom = zoomLevel || 6;

    var map = L.map(containerId, {
      center: coords,
      zoom: zoom,
      zoomControl: true,
      fadeAnimation: true
    });

    // Check if browser is online
    var isOnline = navigator.onLine !== false;

    // Tile layer with graceful offline fallback
    var tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: isOnline ? '&copy; OpenStreetMap contributors • Sportiva CM' : '📍 Sportiva CM Cameroon Sports Map (Offline Mode)',
      errorTileUrl: 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256"><rect width="256" height="256" fill="%230b1329"/><path d="M0,0 L256,256 M256,0 L0,256" stroke="rgba(16,185,129,0.04)" stroke-width="1"/><circle cx="128" cy="128" r="64" stroke="rgba(16,185,129,0.06)" fill="none"/></svg>'
    });

    tileLayer.addTo(map);

    // If offline, add a subtle regional overlay / indicator
    if (!isOnline) {
      var offlineBadge = L.control({ position: 'bottomleft' });
      offlineBadge.onAdd = function() {
        var div = L.DomUtil.create('div', 'p-2 rounded-lg bg-slate-900/90 text-emerald-400 text-xs font-semibold border border-emerald-500/30 shadow-lg');
        div.innerHTML = '<i class="fa-solid fa-satellite-dish mr-1 text-amber-400"></i> Local Cameroon Radar Grid';
        return div;
      };
      offlineBadge.addTo(map);
    }

    return map;
  };
})();
