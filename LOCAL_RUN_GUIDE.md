# Local Run & Offline Guide for Sportiva CM

Sportiva CM is fully configured to operate **100% locally and offline** without requiring an active internet connection. All CSS frameworks (Tailwind), icons (FontAwesome), interactive maps (Leaflet + markers), and fonts (Outfit & Plus Jakarta Sans) are bundled and served directly by the local server and cached by the PWA Service Worker.

---

## Step 1: Open the project folder
Open the project directory in your terminal or VS Code terminal:
```bash
cd "C:\Users\NK-MAL\Documents\SPORTIVA CM"
```

## Step 2: Activate the virtual environment
```bash
.venv\Scripts\activate
```

## Step 3: Apply migrations
```bash
python manage.py migrate
```

## Step 4: Seed sample data (Clubs, Events, Marketplace, Sponsorships)
```bash
python manage.py seed_data
```

## Step 5: Start the local server
```bash
python manage.py runserver
```

## Step 6: Open the website
Visit:
```text
http://127.0.0.1:8000/
```

---

## ⚡ Offline Local Features & Capabilities

1. **Local Vendor Assets (No CDN Dependencies)**:
   - **Tailwind CSS engine**: Local `static/vendor/tailwind/tailwind.js`
   - **Font Awesome 6**: Local `static/vendor/fontawesome/` (CSS + WOFF2 fonts)
   - **Leaflet Maps**: Local `static/vendor/leaflet/` (CSS + JS + local Retina markers)
   - **Custom Typography**: Local `static/fonts/` (Outfit & Plus Jakarta Sans WOFF2 fonts)
2. **PWA Service Worker & Caching**:
   - `sw.js` automatically pre-caches all static assets and visited pages in browser `CacheStorage`.
   - Dynamic caching enables ultra-fast navigation (0ms network latency).
3. **Resilient Map Engine (`offline-map.js`)**:
   - Leaflet maps use local markers and an offline tactical radar coordinate grid for Cameroon regions (Centre, Littoral, West, North, South-West) if tile servers are unreachable.
4. **Live Offline Status Indicator**:
   - Automatically detects network status and shows a discreet badge when operating offline.
5. **Standalone PWA Installable**:
   - Configured with `manifest.json` for desktop or mobile standalone install.

---

## 🧪 How to Demonstrate Offline Mode During Defense

1. Start the server with `python manage.py runserver` and open `http://127.0.0.1:8000/`.
2. Turn off Wi-Fi on your laptop (or open Chrome DevTools > Network tab > select **"Offline"**).
3. Navigate across the entire platform:
   - **Dashboard**: Full Cameroon color scheme and stats.
   - **Clubs & Organizations**: Interactive local sports directory and hub map.
   - **Events**: Tournaments, marathons, and match locations.
   - **Marketplace**: Sporting equipment, jerseys, and contact details.
   - **Sponsorships**: Funding campaigns, pledge counters, and local progress tracking.
   - **User Management & Auth**: Role-based access control and athlete profiles.

---

## Default Accounts
- **Admin**: `camer_admin` / `Admin237!`
- **Organization**: `douala_fc` / `Admin237!`
- **Coach / Trainer**: `coach_samuel` / `Admin237!`
- **Athlete**: `rigobert_song` / `Admin237!`
- **Sponsor**: `mtn_cameroun` / `Admin237!`

## Automated Tests
Run the test suite to verify full integrity:
```bash
python manage.py test
```
