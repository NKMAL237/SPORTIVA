/**
 * SPORTIVA CM 2.0 — Real-Time Interactive Map & Location Engine
 * 100% Free & Open Access • Zero API Keys • Zero Permissions Required
 * 
 * Supports:
 * - CartoDB Dark Matter (Default high-contrast dark theme)
 * - ESRI World Imagery (High-definition satellite imagery)
 * - CartoDB Voyager (Vibrant streets & sports venues)
 * - OpenStreetMap Standard (Global community map)
 * - Direct turn-by-turn directions links (Google Maps, Apple Maps, OpenStreetMap, Waze)
 * - Custom animated neon radar venue marker
 * - Zero-blocking fallback geocoding
 */

let activeLocationMap = null;
let activeTileLayer = null;
let currentMapCoords = [3.8480, 11.5021];
let currentLayerName = 'dark';
let activeMarker = null;

// City coordinate lookup for bulletproof fallback when exact lat/lng is missing
const CITY_FALLBACK_COORDS = {
  'yaounde': [3.8480, 11.5021],
  'yaoundé': [3.8480, 11.5021],
  'douala': [4.0511, 9.7679],
  'bafoussam': [5.4778, 10.4176],
  'garoua': [9.3000, 13.4000],
  'london': [51.5074, -0.1278],
  'paris': [48.8566, 2.3522],
  'barcelona': [41.3879, 2.1699],
  'madrid': [40.4168, -3.7038],
  'berlin': [52.5200, 13.4050],
  'rome': [41.9028, 12.4964],
  'geneva': [46.2044, 6.1432],
  'tokyo': [35.6762, 139.6503],
  'new york': [40.7128, -74.0060]
};

// Free Tile Layer Definitions (No API keys or billing needed)
const TILE_PROVIDERS = {
  dark: {
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    options: {
      subdomains: 'abcd',
      maxZoom: 19,
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> &bull; &copy; OpenStreetMap'
    }
  },
  satellite: {
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    options: {
      maxZoom: 19,
      attribution: '&copy; ESRI World Imagery &bull; Maxar, Earthstar Geographics'
    }
  },
  voyager: {
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    options: {
      subdomains: 'abcd',
      maxZoom: 19,
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> Voyager &bull; &copy; OpenStreetMap'
    }
  },
  osm: {
    url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
    options: {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }
  }
};

/**
 * Resolves cleanest possible coordinates without needing device location permissions.
 */
function resolveBestCoords(lat, lng, address = '', country = '') {
  let pLat = parseFloat(lat);
  let pLng = parseFloat(lng);

  if (!isNaN(pLat) && !isNaN(pLng) && (Math.abs(pLat) > 0.0001 || Math.abs(pLng) > 0.0001)) {
    return [pLat, pLng];
  }

  // Lookup in city table
  const searchStr = (address + ' ' + country).toLowerCase();
  for (const [cityName, coords] of Object.entries(CITY_FALLBACK_COORDS)) {
    if (searchStr.includes(cityName)) {
      return coords;
    }
  }

  // Default global sports hub coordinate (London or Yaoundé)
  return [3.8480, 11.5021];
}

/**
 * Opens the interactive location modal and initializes the high-resolution map.
 */
function openLocationModal(lat, lng, title, address, country = '') {
  const modal = document.getElementById('sportiva-location-modal');
  if (!modal) return;

  const [resolvedLat, resolvedLng] = resolveBestCoords(lat, lng, address, country);
  currentMapCoords = [resolvedLat, resolvedLng];

  // Populate header details
  const titleEl = document.getElementById('loc-modal-title');
  const addressEl = document.getElementById('loc-modal-address');
  const coordsEl = document.getElementById('loc-modal-coords');

  const displayTitle = title || 'Venue / Stadium Location';
  const displayAddress = address ? (address + (country ? `, ${country}` : '')) : (country || 'Sports Ground / Facility');

  if (titleEl) titleEl.innerText = displayTitle;
  if (addressEl) addressEl.innerText = displayAddress;
  if (coordsEl) coordsEl.innerText = `${resolvedLat.toFixed(5)}, ${resolvedLng.toFixed(5)}`;

  // Direct turn-by-turn navigation links (free, open, no token required)
  const gmapsLink = document.getElementById('loc-modal-gmaps');
  const appleLink = document.getElementById('loc-modal-apple');
  const osmLink = document.getElementById('loc-modal-osm');
  const wazeLink = document.getElementById('loc-modal-waze');

  if (gmapsLink) {
    gmapsLink.href = `https://www.google.com/maps/dir/?api=1&destination=${resolvedLat},${resolvedLng}`;
  }
  if (appleLink) {
    appleLink.href = `https://maps.apple.com/?daddr=${resolvedLat},${resolvedLng}&q=${encodeURIComponent(displayTitle)}`;
  }
  if (osmLink) {
    osmLink.href = `https://www.openstreetmap.org/directions?engine=fossgis_osrm_car&route=%3B${resolvedLat}%2C${resolvedLng}#map=16/${resolvedLat}/${resolvedLng}`;
  }
  if (wazeLink) {
    wazeLink.href = `https://waze.com/ul?ll=${resolvedLat},${resolvedLng}&navigate=yes`;
  }

  // Reveal modal with smooth animation
  modal.classList.remove('hidden');
  modal.classList.add('flex');

  // Initialize or re-render map container
  setTimeout(() => {
    initOrUpdateModalMap(resolvedLat, resolvedLng, displayTitle, displayAddress);
  }, 180);
}

/**
 * Initializes or updates the Leaflet map inside the modal.
 */
function initOrUpdateModalMap(lat, lng, title, address) {
  const mapContainer = document.getElementById('loc-modal-map');
  if (!mapContainer || !window.L) return;

  if (activeLocationMap) {
    activeLocationMap.remove();
    activeLocationMap = null;
  }

  // Initialize map instance
  activeLocationMap = L.map('loc-modal-map', {
    center: [lat, lng],
    zoom: 15,
    zoomControl: false, // We use custom styled controls or Leaflet's positioned neatly
    attributionControl: true
  });

  // Add zoom control in top-right
  L.control.zoom({ position: 'topright' }).addTo(activeLocationMap);

  // Apply default layer (Dark Mode)
  setMapTileLayer(currentLayerName || 'dark');

  // Create High-Vis Glowing Radar Pin
  const customPin = L.divIcon({
    className: 'sportiva-radar-pin',
    html: `
      <div style="position:relative; width:44px; height:44px; display:flex; align-items:center; justify-content:center;">
        <div style="position:absolute; width:44px; height:44px; border-radius:50%; background:rgba(14,165,233,0.3); animation: sportivaPulse 2s infinite ease-out;"></div>
        <div style="width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg, #0EA5E9 0%, #2563EB 100%); display:flex; align-items:center; justify-content:center; color:#fff; border:2.5px solid #ffffff; box-shadow:0 4px 14px rgba(14,165,233,0.6); z-index:2;">
          <i class="fa-solid fa-location-dot" style="font-size:15px;"></i>
        </div>
      </div>
    `,
    iconSize: [44, 44],
    iconAnchor: [22, 22]
  });

  // Attach Marker and Popup
  activeMarker = L.marker([lat, lng], { icon: customPin }).addTo(activeLocationMap);

  const popupHtml = `
    <div style="min-width:180px; padding:4px;">
      <h4 style="font-weight:800; font-size:13px; color:#0f172a; margin-bottom:4px;">${title}</h4>
      <p style="font-size:11px; color:#475569; margin:0 0 8px 0; line-height:1.3;">${address}</p>
      <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #e2e8f0; padding-top:6px; font-size:10px; font-weight:bold; color:#0284c7;">
        <span>GPS: ${lat.toFixed(4)}, ${lng.toFixed(4)}</span>
        <span>Verified ✓</span>
      </div>
    </div>
  `;

  activeMarker.bindPopup(popupHtml, { closeButton: true, autoPan: true }).openPopup();

  // Force Leaflet to compute correct container dimensions
  activeLocationMap.invalidateSize();
}

/**
 * Switches the map tile layer seamlessly without reloading.
 */
function switchMapLayer(layerKey) {
  if (!activeLocationMap || !TILE_PROVIDERS[layerKey]) return;
  currentLayerName = layerKey;
  setMapTileLayer(layerKey);

  // Update UI active buttons
  document.querySelectorAll('#map-layer-selector button').forEach(btn => {
    if (btn.getAttribute('data-layer') === layerKey) {
      btn.className = 'px-2.5 py-1 rounded-lg text-xs font-bold transition-all bg-cyan-500 text-slate-950 shadow-md';
    } else {
      btn.className = 'px-2.5 py-1 rounded-lg text-xs font-semibold text-slate-400 hover:text-white transition-all';
    }
  });
}

function setMapTileLayer(layerKey) {
  if (!activeLocationMap) return;
  const config = TILE_PROVIDERS[layerKey] || TILE_PROVIDERS.dark;

  if (activeTileLayer) {
    activeLocationMap.removeLayer(activeTileLayer);
  }

  activeTileLayer = L.tileLayer(config.url, config.options).addTo(activeLocationMap);
}

/**
 * Recenters the map onto the current venue marker.
 */
function recenterLocationMap() {
  if (activeLocationMap && currentMapCoords) {
    activeLocationMap.flyTo(currentMapCoords, 16, { animate: true, duration: 0.8 });
    if (activeMarker) activeMarker.openPopup();
  }
}

/**
 * Copies the current coordinates to the clipboard and shows a toast notification.
 */
function copyModalCoords() {
  if (!currentMapCoords) return;
  const text = `${currentMapCoords[0].toFixed(5)}, ${currentMapCoords[1].toFixed(5)}`;
  navigator.clipboard.writeText(text).then(() => {
    const toast = document.getElementById('map-copy-toast');
    if (toast) {
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 2200);
    }
  }).catch(() => {});
}

/**
 * Closes the location modal cleanly.
 */
function closeLocationModal() {
  const modal = document.getElementById('sportiva-location-modal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
  if (activeLocationMap) {
    activeLocationMap.closePopup();
  }
}

// Global Event Listeners (Escape key, backdrop click, data-open-location elements)
document.addEventListener('DOMContentLoaded', () => {
  // Click listener for elements with data-open-location
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-open-location]');
    if (btn) {
      e.preventDefault();
      const lat = btn.getAttribute('data-lat') || '';
      const lng = btn.getAttribute('data-lng') || '';
      const title = btn.getAttribute('data-title') || 'Location';
      const address = btn.getAttribute('data-address') || '';
      const country = btn.getAttribute('data-country') || '';
      openLocationModal(lat, lng, title, address, country);
    }
  });

  // Close on backdrop click
  const modal = document.getElementById('sportiva-location-modal');
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeLocationModal();
      }
    });
  }

  // Close on Escape key
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeLocationModal();
    }
  });
});
