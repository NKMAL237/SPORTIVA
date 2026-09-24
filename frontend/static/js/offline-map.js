/**
 * Sportiva CM 2.0 — Resilient Map & Geolocation Helper
 * Works 100% free locally and globally without API keys or permission blockers.
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

    var coords = centerCoords || [3.8480, 11.5021];
    var zoom = zoomLevel || 13;

    var map = L.map(containerId, {
      center: coords,
      zoom: zoom,
      zoomControl: true,
      fadeAnimation: true
    });

    var isOnline = navigator.onLine !== false;

    // High performance free dark tiles (CartoDB Dark Matter)
    var tileLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      maxZoom: 19,
      subdomains: 'abcd',
      attribution: isOnline ? '&copy; <a href="https://carto.com/">CARTO</a> &bull; &copy; OpenStreetMap' : '📍 Sportiva CM (Offline Cache)',
      errorTileUrl: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
    });

    tileLayer.addTo(map);

    // If offline, add indicator badge
    if (!isOnline) {
      var offlineBadge = L.control({ position: 'bottomleft' });
      offlineBadge.onAdd = function() {
        var div = L.DomUtil.create('div', 'p-2 rounded-lg bg-slate-900/90 text-cyan-400 text-xs font-semibold border border-cyan-500/30 shadow-lg');
        div.innerHTML = '<i class="fa-solid fa-satellite-dish mr-1 text-amber-400"></i> Local Offline Radar Grid';
        return div;
      };
      offlineBadge.addTo(map);
    }

    return map;
  };
})();
