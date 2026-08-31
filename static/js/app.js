/**
 * Sportiva CM — Main Client App Script
 * Offline status banner, Service Worker lifecycle, and UI enhancers.
 */

document.addEventListener('DOMContentLoaded', function() {
  // Service Worker Registration for PWA & Offline Support
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then(function(registration) {
        console.log('Sportiva CM Service Worker registered successfully with scope:', registration.scope);
      })
      .catch(function(error) {
        console.log('Sportiva CM Service Worker registration skipped or failed:', error);
      });
  }

  // Network Offline / Online Toast Indicator
  var indicator = document.getElementById('offline-indicator');
  
  function updateNetworkStatus() {
    if (!navigator.onLine) {
      if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'offline-indicator';
        indicator.className = 'fixed bottom-4 right-4 z-50 flex items-center space-x-2 px-4 py-2.5 rounded-2xl bg-amber-950/90 border border-amber-500/40 text-amber-200 text-xs font-semibold shadow-2xl backdrop-blur-md transition-all duration-300 animate-pulse';
        indicator.innerHTML = '<i class="fa-solid fa-cloud-bolt text-amber-400"></i><span>Offline Mode — Running Locally</span>';
        document.body.appendChild(indicator);
      }
      indicator.classList.remove('hidden');
    } else if (indicator) {
      indicator.classList.add('hidden');
    }
  }

  window.addEventListener('online', function() {
    updateNetworkStatus();
  });

  window.addEventListener('offline', function() {
    updateNetworkStatus();
  });

  // Initial check
  updateNetworkStatus();
});
