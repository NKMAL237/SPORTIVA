# SPORTIVA CM 2.0 — Architecture & Project Structure Guide

Welcome to the **Sportiva CM** codebase. This guide details the complete organization of the project, clearly separating **Frontend** assets and templates from **Backend** business logic, data models, and API endpoints.

---

## 🏛️ High-Level Architectural Overview

Sportiva CM is designed with a clean separation of concerns:
- **`frontend/`**: Holds all user interface presentation layers (HTML templates, Tailwind CSS, JavaScript interactions, PWA assets, and media).
- **Backend Apps (`accounts/`, `chat/`, `events/`, etc.)**: Houses domain-specific data models, REST endpoints, services, signals, and business logic.
- **`sportiva_cm/`**: Central project settings, WSGI/ASGI gateways, and root routing.

```
sportiva_cm/
│
├── 🎨 frontend/                      # ALL FRONTEND ASSETS & UI
│   ├── static/                       # Static assets (CSS, JS, Fonts, Images)
│   └── templates/                    # HTML template hierarchies
│
├── ⚙️ BACKEND APPS                   # BUSINESS LOGIC & DATA MODELS
│   ├── accounts/                     # Users, Profiles, Endorsements
│   ├── chat/                         # Direct Messaging & Real-Time Threads
│   ├── core/                         # Home, Public Feeds, PWA APIs
│   ├── events/                       # Tournaments, Registrations, Invoices
│   ├── marketplace/                  # Gear Listings, E-Commerce, Orders
│   ├── media_feed/                   # Social Feed, Posts, Reels, Likes
│   ├── organizations/                # Sports Clubs, Academies, Rosters
│   ├── sponsorships/                 # Brand Campaigns, Proposals, Contracts
│   └── sportiva_cm/                  # Core Django Config & URL Routing
│
└── 📁 ROOT & SYSTEM FILES
    ├── manage.py                     # Django CLI
    ├── db.sqlite3                    # Local SQLite Database
    ├── media/                        # User-uploaded files (avatars, attachments)
    └── locale/                       # Internationalization & Translations
```

---

## 🎨 1. Frontend Layer (`frontend/`)

Everything related to what the user sees, interacts with, or downloads on the client-side resides inside `frontend/`.

```
frontend/
├── static/                           # Client-side Static Files
│   ├── css/
│   │   └── styles.css                # Tailwind CSS & custom responsive styling
│   ├── js/                           # Interactive scripts & dynamic AJAX
│   ├── images/                       # UI icons, placeholders, site logos
│   ├── fonts/                        # Web typography
│   ├── vendor/                       # Third-party client dependencies
│   ├── manifest.json                 # Progressive Web App (PWA) manifest
│   └── sw.js                         # PWA Service Worker (caching & offline mode)
│
└── templates/                        # Server-Side Rendered HTML Templates
    ├── base.html                     # Core layout skeleton (header, links, footer)
    ├── navbar.html                   # Global navigation bar & role-based tabs
    ├── footer.html                   # Site footer & language switcher
    ├── offline.html                  # Fallback screen when offline (PWA)
    │
    ├── accounts/                     # User & Profile UI
    │   ├── login.html                # User authentication screen
    │   ├── register.html             # Multi-role signup (Athlete, Scout, Club)
    │   ├── profile.html              # Athlete/Scout CV profile view
    │   ├── profile_edit.html         # Edit details, stats, achievements
    │   └── ...
    │
    ├── chat/                         # Direct Messaging UI
    │   ├── inbox.html                # Conversations list & message thread
    │   └── thread.html               # Chat conversation window
    │
    ├── core/                         # Public & Home Screens
    │   ├── home.html                 # Landing page & featured athletes
    │   ├── search.html               # Universal search results
    │   └── ...
    │
    ├── events/                       # Tournaments & Scouting Trials
    │   ├── list.html                 # Event directory with country/sport filters
    │   ├── detail.html               # Event details, capacity indicators
    │   └── create.html               # Event creation form
    │
    ├── marketplace/                  # Sports Equipment & Gear
    │   ├── list.html                 # Product catalog & category filtering
    │   ├── detail.html               # Product detail & purchase options
    │   └── create.html               # List gear for sale
    │
    ├── media_feed/                   # Social Feed
    │   ├── feed.html                 # Video/photo feed & athlete highlights
    │   └── post_detail.html          # Single post with comments
    │
    ├── organizations/                # Clubs & Academies
    │   ├── list.html                 # Directory of clubs and academies
    │   ├── detail.html               # Academy profile, staff & athlete roster
    │   └── create.html               # Register academy/club
    │
    └── sponsorships/                 # Sponsorships & Deals
        ├── list.html                 # Active campaigns & opportunities
        ├── sponsor_detail.html       # Sponsorship campaign overview
        └── proposal_form.html        # Pitch and apply for sponsorship
```

> **Django Configuration Note**:
> In `sportiva_cm/settings.py`, Django knows how to find these files via:
> - `TEMPLATES['DIRS'] = [BASE_DIR / 'frontend' / 'templates']`
> - `STATICFILES_DIRS = [BASE_DIR / 'frontend' / 'static']`

---

## ⚙️ 2. Backend Layer (Domain Applications)

Each domain of Sportiva CM is a dedicated, self-contained Django application:

| Application | Responsibilities & Purpose | Key Files |
| :--- | :--- | :--- |
| **`accounts`** | User models, role types (Athlete, Scout, Club, Brand), endorsements, career exploits, authentication and authorization. | `models.py`, `views.py`, `forms.py`, `urls.py` |
| **`chat`** | One-to-one messaging, thread handling, unread counts, and real-time communication. | `models.py`, `views.py`, `urls.py` |
| **`core`** | Platform landing views, search endpoints, news integration, and PWA utilities. | `views.py`, `urls.py` |
| **`events`** | Scouting events, tournaments, ticketing, capacity enforcement, and PDF invoice generation. | `models.py`, `views.py`, `services/`, `urls.py` |
| **`marketplace`**| Sports gear listings, product categorization, condition ratings, and transaction flow. | `models.py`, `views.py`, `urls.py` |
| **`media_feed`** | Social posts, video clips, scouting highlights, likes, and comment threads. | `models.py`, `views.py`, `urls.py` |
| **`organizations`**| Clubs, training centers, academies, staff allocations, and roster affiliations. | `models.py`, `views.py`, `urls.py` |
| **`sponsorships`** | Brand sponsorships, campaign budgets, applications, contract management. | `models.py`, `views.py`, `urls.py` |
| **`sportiva_cm`** | Project root configuration: `settings.py`, global `urls.py`, `wsgi.py`, and `asgi.py`. | Core configurations |

---

## 🚀 3. How to Run & Develop

1. **Activate Virtual Environment**:
   ```powershell
   .venv\Scripts\activate
   ```

2. **Verify System Health**:
   ```bash
   python manage.py check
   ```

3. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Launch Development Server**:
   ```bash
   python manage.py runserver
   ```

Visit `http://127.0.0.1:8000/` in your browser.

---

## 👥 4. User Accounts & Testing Credentials

For a complete table of all 16 registered users, default passwords, roles, and instructions to test each account type, refer to **[`USERS_CREDENTIALS.md`](USERS_CREDENTIALS.md)**.

