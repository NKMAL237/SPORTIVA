# Local Run & Offline Guide for SPORTIVA

SPORTIVA is fully configured to operate **100% locally and offline** without requiring an active internet connection. All CSS frameworks (Tailwind), icons (FontAwesome), interactive maps (Leaflet + markers), and fonts are bundled and served directly by the local server — and pre-cached by the PWA Service Worker for instant offline access.

---

## Step 1: Open the project folder

Open the project directory in your terminal or VS Code terminal:
```powershell
cd "C:\Users\NK-MAL\Documents\SPORTIVA CM 2.0"
```

## Step 2: Activate the virtual environment
```powershell
.venv\Scripts\activate
```
You will see `(.venv)` at the start of your terminal prompt.

## Step 3: Apply database migrations
```powershell
python manage.py migrate
```

## Step 4: Seed sample data (Athletes, Clubs, Events, Marketplace, Sponsorships)
```powershell
python manage.py seed_data
```
> ⚠️ Only run this **once**. Running it multiple times may create duplicate data.

## Step 5: Start the local server
```powershell
python manage.py runserver
```

## Step 6: Open the website
Visit in **Google Chrome** (recommended for PWA/offline):
```
http://127.0.0.1:8000/
```

---

## ⚡ Offline & Online Mode

SPORTIVA has a **Facebook-style dual mode**:

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Online** | Wi-Fi / Ethernet connected | Full features + live sports news refresh |
| **Offline** | Wi-Fi disabled or DevTools "Offline" | All cached pages load instantly |
| **Reconnect** | Going back online | Green "Back Online" toast + news auto-refresh |

### How the Service Worker caches content:
- **Static assets** (CSS, JS, fonts, icons, maps): Cached on first install → served instantly offline
- **Visited pages**: Network-first, cached as a fallback → available offline after first visit
- **Sports News API** (`/api/sports-news/`): Pre-cached + stored in `localStorage` for offline reading
- **New content**: When back online, new SW version triggers a silent update banner

---

## 📡 Global Sports News (New!)

The right sidebar of the home page includes a **live sports news ticker**:
- **Online**: Fetches fresh articles from `/api/sports-news/` automatically when reconnected
- **Offline**: Serves the last-cached batch of 12 curated news articles (Football, Basketball, Athletics, Tennis, Swimming, Rugby, Cycling, Cricket, Combat Sports)
- **Server-side fallback**: The top 6 articles are always rendered server-side for true offline support

---

## 🧪 How to Demonstrate Offline Mode

1. Start the server with `python manage.py runserver` and open `http://127.0.0.1:8000/`
2. Browse several pages (Home, Events, Organizations, Profiles) to pre-cache them
3. Turn off Wi-Fi OR open Chrome DevTools > **Network** tab > select **"Offline"**
4. Navigate across the entire platform:
   - **Dashboard**: Full stats, news ticker (cached), athlete leaderboard
   - **Clubs & Organizations**: Sports directory and hub map (offline Leaflet maps)
   - **Events**: Tournaments with GPS venue coordinates
   - **Marketplace**: Equipment and sporting goods listings
   - **Sponsorships**: Funding campaigns and sponsor profiles
   - **Athlete Profiles**: Exploits, tier badges, and merit scores
5. Observe the **amber offline badge** at the bottom of the screen
6. Turn Wi-Fi back on to see the **green "Back Online" notification** and news refresh

---

## 🏆 Default Accounts

| Role | Username | Password |
|------|----------|----------|
| **Admin** | `camer_admin` | `Admin237!` |
| **Club / Organization** | `douala_fc` | `Admin237!` |
| **Coach / Trainer** | `coach_samuel` | `Admin237!` |
| **Athlete** | `rigobert_song` | `Admin237!` |
| **Sponsor** | `mtn_cameroun` | `Admin237!` |

---

## 📋 Automated Tests
Run the full test suite (27 tests) to verify system integrity:
```powershell
python manage.py test --verbosity=1
```
Expected result: `Ran 27 tests in XX.XXXs — OK`

---

## 📖 Full User Guide
For a complete step-by-step guide to every feature (with screenshot placeholders for Word document):
```
SPORTIVA_USER_GUIDE.md
```

---

## 🔧 Offline Assets Included

| Asset | Location | Size |
|-------|----------|------|
| Tailwind CSS engine | `static/vendor/tailwind/tailwind.js` | Bundled |
| Font Awesome 6 icons | `static/vendor/fontawesome/` | CSS + WOFF2 |
| Leaflet Maps | `static/vendor/leaflet/` | CSS + JS + markers |
| Custom Fonts | `static/fonts/` | Outfit & Plus Jakarta Sans WOFF2 |
| Service Worker | `static/sw.js` | Caches all above + pages |
| PWA Manifest | `static/manifest.json` | Installable standalone app |

---

## 🌐 Key URLs

| Purpose | URL |
|---------|-----|
| Home Dashboard | `http://127.0.0.1:8000/` |
| Sports Feed | `http://127.0.0.1:8000/media-feed/` |
| Events | `http://127.0.0.1:8000/events/` |
| Sponsorships | `http://127.0.0.1:8000/sponsorships/` |
| Marketplace | `http://127.0.0.1:8000/marketplace/` |
| Sports News API | `http://127.0.0.1:8000/api/sports-news/` |
| Offline Test Page | `http://127.0.0.1:8000/offline/` |
| Admin Panel | `http://127.0.0.1:8000/admin/` |
