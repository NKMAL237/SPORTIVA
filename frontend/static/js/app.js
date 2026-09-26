/**
 * SPORTIVA — Global Sports Network
 * Main Client App Script
 * Handles: PWA Service Worker, Online/Offline detection,
 * Live Sports News refresh, and UI micro-animations.
 */

document.addEventListener('DOMContentLoaded', function () {

  // ─── 1. SERVICE WORKER REGISTRATION ───────────────────────────────────────
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js', { scope: '/' })
      .then(function (registration) {
        console.log('[SPORTIVA] Service Worker registered. Scope:', registration.scope);

        // Listen for updates: when a new SW is waiting, show banner
        registration.addEventListener('updatefound', function () {
          const newWorker = registration.installing;
          newWorker.addEventListener('statechange', function () {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              showUpdateBanner();
            }
          });
        });
      })
      .catch(function (error) {
        console.warn('[SPORTIVA] Service Worker registration skipped:', error);
      });

    // If controller changes (new SW activated), reload to apply
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', function () {
      if (!refreshing) {
        refreshing = true;
        window.location.reload();
      }
    });

    // When the SW finishes replaying queued offline form submissions
    navigator.serviceWorker.addEventListener('message', function (event) {
      if (event.data && event.data.action === 'SYNC_COMPLETE') {
        showSyncToast();
      }
    });
  }

  // ─── 2. ONLINE / OFFLINE STATUS INDICATOR ─────────────────────────────────
  var offlineBar = null;

  function createOfflineBar() {
    if (offlineBar) return;
    offlineBar = document.createElement('div');
    offlineBar.id = 'sportiva-offline-bar';
    offlineBar.setAttribute('role', 'status');
    offlineBar.setAttribute('aria-live', 'polite');
    offlineBar.style.cssText = [
      'position:fixed', 'bottom:70px', 'left:50%', 'transform:translateX(-50%)',
      'z-index:9999', 'display:flex', 'align-items:center', 'gap:8px',
      'padding:10px 20px', 'border-radius:99px',
      'background:rgba(120,53,15,0.95)', 'border:1px solid rgba(251,191,36,0.4)',
      'color:#fde68a', 'font-size:12px', 'font-weight:700',
      'box-shadow:0 8px 32px rgba(0,0,0,0.5)', 'backdrop-filter:blur(12px)',
      'transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1)',
      'white-space:nowrap'
    ].join(';');
    offlineBar.innerHTML = '<i class="fa-solid fa-cloud-bolt" style="color:#fbbf24;font-size:14px"></i>' +
      '<span>Offline Mode — Cached content available</span>';
    document.body.appendChild(offlineBar);
  }

  function showOnlineNotification() {
    var toast = document.createElement('div');
    toast.style.cssText = [
      'position:fixed', 'bottom:70px', 'left:50%', 'transform:translateX(-50%) translateY(20px)',
      'z-index:9999', 'display:flex', 'align-items:center', 'gap:8px',
      'padding:10px 20px', 'border-radius:99px',
      'background:rgba(6,78,59,0.95)', 'border:1px solid rgba(52,211,153,0.4)',
      'color:#a7f3d0', 'font-size:12px', 'font-weight:700',
      'box-shadow:0 8px 32px rgba(0,0,0,0.5)', 'backdrop-filter:blur(12px)',
      'opacity:0', 'transition:all 0.5s ease',
      'white-space:nowrap'
    ].join(';');
    toast.innerHTML = '<i class="fa-solid fa-wifi" style="color:#34d399;font-size:14px"></i>' +
      '<span>Back Online — Syncing latest sports news…</span>';
    document.body.appendChild(toast);
    requestAnimationFrame(function () {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });
    setTimeout(function () {
      toast.style.opacity = '0';
      setTimeout(function () { toast.remove(); }, 500);
    }, 4000);

    // Trigger live news refresh
    refreshSportsNews();
  }

  function showSyncToast() {
    var toast = document.createElement('div');
    toast.style.cssText = [
      'position:fixed', 'bottom:70px', 'left:50%', 'transform:translateX(-50%) translateY(20px)',
      'z-index:9999', 'display:flex', 'align-items:center', 'gap:8px',
      'padding:10px 20px', 'border-radius:99px',
      'background:rgba(6,78,59,0.95)', 'border:1px solid rgba(52,211,153,0.4)',
      'color:#a7f3d0', 'font-size:12px', 'font-weight:700',
      'box-shadow:0 8px 32px rgba(0,0,0,0.5)', 'backdrop-filter:blur(12px)',
      'opacity:0', 'transition:all 0.5s ease',
      'white-space:nowrap'
    ].join(';');
    toast.innerHTML = '<i class="fa-solid fa-cloud-arrow-up" style="color:#34d399;font-size:14px"></i>' +
      '<span>Offline actions synced — everything is up to date.</span>';
    document.body.appendChild(toast);
    requestAnimationFrame(function () {
      toast.style.opacity = '1';
      toast.style.transform = 'translateX(-50%) translateY(0)';
    });
    setTimeout(function () {
      toast.style.opacity = '0';
      setTimeout(function () { toast.remove(); }, 500);
    }, 5000);
  }

  function updateNetworkStatus() {
    if (!navigator.onLine) {
      createOfflineBar();
      if (offlineBar) {
        offlineBar.style.opacity = '1';
        offlineBar.style.transform = 'translateX(-50%) scale(1)';
      }
    } else {
      if (offlineBar) {
        offlineBar.style.opacity = '0';
        offlineBar.style.transform = 'translateX(-50%) scale(0.9)';
        setTimeout(function () {
          if (offlineBar) offlineBar.remove();
          offlineBar = null;
        }, 400);
      }
    }
  }

  window.addEventListener('online', function () {
    updateNetworkStatus();
    showOnlineNotification();
  });

  window.addEventListener('offline', function () {
    updateNetworkStatus();
  });

  updateNetworkStatus(); // Initial check

  // ─── 3. LIVE SPORTS NEWS TICKER (ONLINE → refreshes; OFFLINE → stays cached) ─
  var newsContainer = document.getElementById('sportiva-news-ticker');
  var newsLoadingEl = document.getElementById('sportiva-news-loading');

  function refreshSportsNews() {
    if (!newsContainer) return;
    if (!navigator.onLine) return; // Don't fetch if offline

    fetch('/api/sports-news/', {
      headers: { 'X-Requested-With': 'XMLHttpRequest' },
      cache: 'no-cache'
    })
      .then(function (res) {
        if (!res.ok) throw new Error('Network response not ok');
        return res.json();
      })
      .then(function (data) {
        if (data && data.articles && data.articles.length > 0) {
          renderNewsArticles(data.articles);
          if (newsLoadingEl) newsLoadingEl.style.display = 'none';
          // Cache the news data for offline
          localStorage.setItem('sportiva_cached_news', JSON.stringify({
            ts: Date.now(),
            articles: data.articles
          }));
        }
      })
      .catch(function () {
        // Silently fall back to cached news
        loadCachedNews();
      });
  }

  function loadCachedNews() {
    if (!newsContainer) return;
    var cached = localStorage.getItem('sportiva_cached_news');
    if (cached) {
      try {
        var parsed = JSON.parse(cached);
        if (parsed && parsed.articles) {
          renderNewsArticles(parsed.articles);
          if (newsLoadingEl) newsLoadingEl.style.display = 'none';
        }
      } catch (e) { /* ignore */ }
    }
  }

  function renderNewsArticles(articles) {
    if (!newsContainer) return;
    newsContainer.innerHTML = articles.map(function (article) {
      var disciplineColor = getDisciplineColor(article.discipline);
      return [
        '<a href="' + (article.url || '#') + '" target="_blank" rel="noopener"',
        ' class="flex items-start gap-3 p-3 rounded-2xl bg-slate-900/60 hover:bg-slate-800/80',
        ' border border-slate-800 hover:border-slate-700 transition-all duration-200 group">',
        '<div class="w-8 h-8 rounded-lg flex-shrink-0 flex items-center justify-center text-base ' + disciplineColor + '">',
        '<span>' + (article.icon || '⚽') + '</span>',
        '</div>',
        '<div class="flex-1 min-w-0">',
        '<p class="text-xs font-semibold text-slate-100 group-hover:text-cyan-300 leading-snug line-clamp-2">' + escHtml(article.title) + '</p>',
        '<div class="flex items-center gap-2 mt-1">',
        '<span class="text-[10px] font-bold uppercase tracking-wider ' + disciplineColor.replace('bg-', 'text-').split(' ')[0] + '">' + escHtml(article.discipline || 'Sport') + '</span>',
        '<span class="text-[10px] text-slate-500">•</span>',
        '<span class="text-[10px] text-slate-500">' + escHtml(article.source || 'SPORTIVA') + '</span>',
        '</div>',
        '</div>',
        '</a>'
      ].join('');
    }).join('');
  }

  function getDisciplineColor(discipline) {
    var map = {
      'Football': 'bg-emerald-950/80 text-emerald-400',
      'Basketball': 'bg-orange-950/80 text-orange-400',
      'Athletics': 'bg-blue-950/80 text-blue-400',
      'Tennis': 'bg-yellow-950/80 text-yellow-400',
      'Swimming': 'bg-cyan-950/80 text-cyan-400',
      'Rugby': 'bg-rose-950/80 text-rose-400',
      'Cycling': 'bg-purple-950/80 text-purple-400',
      'Combat': 'bg-red-950/80 text-red-400',
      'Cricket': 'bg-lime-950/80 text-lime-400',
    };
    return map[discipline] || 'bg-slate-800/80 text-slate-400';
  }

  function escHtml(str) {
    if (!str) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  // Initial news load: try live first, fall back to cache
  if (newsContainer) {
    if (navigator.onLine) {
      refreshSportsNews();
    } else {
      loadCachedNews();
    }
  }

  // ─── 4. UPDATE BANNER ──────────────────────────────────────────────────────
  function showUpdateBanner() {
    var banner = document.createElement('div');
    banner.style.cssText = [
      'position:fixed', 'top:0', 'left:0', 'right:0', 'z-index:9998',
      'background:linear-gradient(90deg,#0ea5e9,#2563eb)',
      'color:#fff', 'font-size:12px', 'font-weight:700',
      'display:flex', 'align-items:center', 'justify-center', 'gap:12px',
      'padding:10px 16px', 'text-align:center',
      'box-shadow:0 4px 16px rgba(14,165,233,0.4)'
    ].join(';');
    banner.innerHTML = [
      '<i class="fa-solid fa-arrow-rotate-right"></i>',
      '<span>SPORTIVA has been updated!</span>',
      '<button onclick="window.location.reload()" style="',
      'background:rgba(255,255,255,0.2);border:1px solid rgba(255,255,255,0.4);',
      'color:#fff;padding:4px 12px;border-radius:99px;font-size:11px;font-weight:700;cursor:pointer">',
      'Refresh to update</button>'
    ].join('');
    document.body.prepend(banner);
  }

  // ─── 5. SMOOTH SCROLL & MICRO-ANIMATIONS ──────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // Auto-dismiss flash messages after 5 seconds
  setTimeout(function () {
    document.querySelectorAll('.message-banner').forEach(function (el) {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    });
  }, 5000);

});
