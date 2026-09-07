/**
 * SPORTIVA — Real-Time Pop-up Localization System
 * Dynamically displays an interactive Leaflet popup map with one-click direct
 * links to Google Maps, Apple Maps, and exact coordinates.
 */

let activeLocationMap = null;

function openLocationModal(lat, lng, title, address, country = '') {
  const modal = document.getElementById('sportiva-location-modal');
  if (!modal) return;

  const titleEl = document.getElementById('loc-modal-title');
  const addressEl = document.getElementById('loc-modal-address');
  const gmapsLink = document.getElementById('loc-modal-gmaps');
  const appleLink = document.getElementById('loc-modal-apple');
  const coordsEl = document.getElementById('loc-modal-coords');

  if (titleEl) titleEl.innerText = title || 'Venue Location';
  if (addressEl) addressEl.innerText = address + (country ? `, ${country}` : '');
  if (coordsEl) coordsEl.innerText = `${parseFloat(lat).toFixed(4)}, ${parseFloat(lng).toFixed(4)}`;

  const cleanLat = parseFloat(lat) || 3.8864;
  const cleanLng = parseFloat(lng) || 11.5367;

  if (gmapsLink) {
    gmapsLink.href = `https://www.google.com/maps/search/?api=1&query=${cleanLat},${cleanLng}`;
  }
  if (appleLink) {
    appleLink.href = `http://maps.apple.com/?q=${encodeURIComponent(title || 'Location')}&ll=${cleanLat},${cleanLng}`;
  }

  modal.classList.remove('hidden');
  modal.classList.add('flex');

  // Initialize or update Leaflet map in modal
  setTimeout(() => {
    const mapContainer = document.getElementById('loc-modal-map');
    if (!mapContainer) return;

    if (activeLocationMap) {
      activeLocationMap.remove();
      activeLocationMap = null;
    }

    activeLocationMap = L.map('loc-modal-map', {
      center: [cleanLat, cleanLng],
      zoom: 14,
      zoomControl: true
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(activeLocationMap);

    const markerIcon = L.divIcon({
      className: 'sportiva-pin',
      html: `
        <div style="background:#0EA5E9; width:36px; height:36px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:white; border:3px solid white; box-shadow:0 0 15px rgba(14,165,233,0.8);">
          <i class="fa-solid fa-location-dot" style="font-size:16px;"></i>
        </div>
      `,
      iconSize: [36, 36],
      iconAnchor: [18, 18]
    });

    const marker = L.marker([cleanLat, cleanLng], { icon: markerIcon }).addTo(activeLocationMap);
    marker.bindPopup(`<b>${title}</b><br/>${address}`).openPopup();

    activeLocationMap.invalidateSize();
  }, 200);
}

function closeLocationModal() {
  const modal = document.getElementById('sportiva-location-modal');
  if (modal) {
    modal.classList.add('hidden');
    modal.classList.remove('flex');
  }
}

// Global click listener for elements with data-open-location
document.addEventListener('DOMContentLoaded', () => {
  document.body.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-open-location]');
    if (btn) {
      e.preventDefault();
      const lat = btn.getAttribute('data-lat') || 3.8864;
      const lng = btn.getAttribute('data-lng') || 11.5367;
      const title = btn.getAttribute('data-title') || 'Location';
      const address = btn.getAttribute('data-address') || '';
      const country = btn.getAttribute('data-country') || '';
      openLocationModal(lat, lng, title, address, country);
    }
  });
});
