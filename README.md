# 🏆 SPORTIVA CM 2.0 — Global Sports Talent, Scouting & Sponsorship Platform

SPORTIVA CM 2.0 is a modern, high-performance sports management and talent marketplace platform. It empowers athletes, clubs, academies, scouts, brands, and fans to discover sports talent, coordinate international tournaments, manage crowdfunding and sponsorship contracts, and communicate seamlessly in real time.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Python 3.11, 3.12, 3.13, 3.14 supported)
- **Virtual Environment**

### 2. Environment Setup
```powershell
# Clone or navigate to the project directory
cd "c:\Users\NK-MAL\Documents\SPORTIVA CM 2.0"

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install all required dependencies
pip install -r requirements.txt
```

### 3. Database Initialization & Seeding
```powershell
# Run system pre-flight check
python manage.py check

# Apply all database migrations
python manage.py migrate

# Seed the database with comprehensive global demo data
python manage.py seed_data
```

### 4. Run Development Server
```powershell
python manage.py runserver
```

Open your browser and navigate to: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Accounts & Credentials

> 📖 **Full User Access Guide**: A complete list of all 16 registered users across all personas (Athletes, Sponsors, Clubs, Coaches, Admins) is available in **[`USERS_CREDENTIALS.md`](USERS_CREDENTIALS.md)**.

The seed command automatically provisions pre-configured personas with verified records, exploits, contracts, and media:

| Role | Username | Password | Notes & Profile Focus |
| :--- | :--- | :--- | :--- |
| **Superuser / Admin** | `sportiva_admin` | `Admin2026!` | Full administrative access at `/admin/` |
| **Elite Athlete (Track & Field)** | `marcus_bolt` | `Pass2026!` | 100m Gold Medalist, verified exploits, campaign creator |
| **Pro Athlete (Tennis)** | `elena_rodriguez` | `Pass2026!` | WTA top 40 pro, training shorts on media feed |
| **Athlete (Football)** | `samuel_etame` | `Pass2026!` | Top youth goalscorer, rising star forward |
| **Corporate Sponsor** | `apex_nutrition` | `Pass2026!` | Sports nutrition partner with active sponsorship budget |
| **Corporate Sponsor** | `stride_footwear` | `Pass2026!` | Performance footwear brand with signed athlete contracts |
| **Sports Academy / Club** | `olympic_academy` | `Pass2026!` | Verified sports academy hosting international events |
| **Sports Fan / Supporter** | `lucas_fan` | `Pass2026!` | Active subscriber & crowdfunding backer |

---

## 🏛️ Project Architecture & Layout

The project enforces a clean separation of concerns with a dedicated `frontend/` directory for all client presentation assets and modular backend Django apps:

```text
sportiva_cm/
│
├── 🎨 frontend/                          # Client-side presentation layer
│   ├── static/                           # Static assets
│   │   ├── css/styles.css                # Tailwind & custom responsive styling
│   │   ├── js/                           # DOM scripts & dynamic interactions
│   │   ├── images/                       # UI icons, placeholders, site logos
│   │   ├── vendor/                       # FontAwesome, Leaflet, Tailwind
│   │   ├── manifest.json                 # Progressive Web App (PWA) manifest
│   │   └── sw.js                         # PWA Service Worker (offline cache)
│   └── templates/                        # Server-rendered HTML templates
│       ├── base.html                     # Core skeleton layout
│       ├── navbar.html                   # Role-based navigation header
│       ├── footer.html                   # Multi-language footer
│       ├── accounts/                     # Profiles, login, registration, exploits
│       ├── chat/                         # Direct messaging inbox & threads
│       ├── core/                         # Home landing, search & feed
│       ├── events/                       # Tournaments, registrations & tickets
│       ├── marketplace/                  # Gear e-commerce & listings
│       ├── media_feed/                   # Social cards, video clips & shorts
│       ├── organizations/                # Clubs & sports academies
│       └── sponsorships/                 # Brand deals, campaigns & proposals
│
├── ⚙️ BACKEND APPLICATIONS                # Domain logic, models, controllers & APIs
│   ├── sportiva_cm/                      # Core Django project config (settings, URLs, ASGI/WSGI)
│   ├── accounts/                         # Custom User, roles, exploits, endorsements
│   ├── chat/                             # Direct messaging and communication
│   ├── core/                             # Landing page, public search, PWA APIs, seed commands
│   ├── events/                           # Tournaments, registration, invoice generator
│   ├── marketplace/                      # Gear listings, orders, and sports equipment
│   ├── media_feed/                       # Social feed, video shorts, likes & comments
│   ├── organizations/                    # Sports clubs, academies & rosters
│   └── sponsorships/                     # Crowdfunding, sponsorship proposals & contracts
│
└── 📁 ROOT & SYSTEM FILES
    ├── manage.py                         # Django administrative CLI
    ├── requirements.txt                  # Python dependencies
    ├── db.sqlite3                        # SQLite development database
    ├── media/                            # User-uploaded files (avatars, attachments)
    ├── locale/                           # Multi-language translations (EN, FR, ES, DE, AR, PT)
    ├── .env.example                      # Environment variables template
    └── PROJECT_STRUCTURE.md              # Detailed developer architectural map
```

---

## 🧪 Testing & Verification

Run the Django verification check and test suite:
```powershell
# System check
python manage.py check

# Run tests
python manage.py test
```

---

## 🌍 Internationalization (i18n)

SPORTIVA CM supports multi-language operation out of the box:
- English (`en`)
- Français (`fr`)
- Español (`es`)
- Deutsch (`de`)
- العربية (`ar`)
- Português (`pt`)
