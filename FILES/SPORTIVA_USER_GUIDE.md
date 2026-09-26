# SPORTIVA — Global Sports Network
## Complete User Guide & Step-by-Step Manual

**Version 2.0 | September 2026**
**Global Sports Network — Athletes · Clubs · Events · Sponsors**

---

> **How to use this guide:**
> This document covers every feature of SPORTIVA step by step. Follow each section in order for first-time setup, then use individual sections as a reference. Screenshots are indicated with 📸 markers — take a screenshot of your running instance at those points for the final Word document.

---

# TABLE OF CONTENTS

1. [System Overview](#1-system-overview)
2. [First-Time Setup (Local Installation)](#2-first-time-setup)
3. [Starting SPORTIVA (Offline & Online Mode)](#3-starting-sportiva)
4. [Home Dashboard](#4-home-dashboard)
5. [Account Registration & Login](#5-account-registration--login)
6. [Athlete Profile Management](#6-athlete-profile-management)
7. [Exploits & Merit Scoring System](#7-exploits--merit-scoring-system)
8. [Clubs & Organizations](#8-clubs--organizations)
9. [Events & Tournaments](#9-events--tournaments)
10. [Sponsorships System](#10-sponsorships-system)
11. [Sports Feed & Media (Posts & Shorts)](#11-sports-feed--media)
12. [Global Sports News Ticker](#12-global-sports-news-ticker)
13. [Marketplace](#13-marketplace)
14. [Direct Messaging (Chat)](#14-direct-messaging-chat)
15. [Offline Mode & PWA Installation](#15-offline-mode--pwa-installation)
16. [Administration Panel](#16-administration-panel)
17. [Default Accounts Reference](#17-default-accounts-reference)
18. [Troubleshooting](#18-troubleshooting)

---

# 1. SYSTEM OVERVIEW

SPORTIVA is a **global digital sports ecosystem** that connects:

| Role | Description |
|------|-------------|
| 🏃 **Athletes** | Create verified profiles, log exploits, get sponsored |
| 🏟️ **Clubs / Organizations** | Manage rosters, events, recruit talent |
| 🎖️ **Coaches** | Verify athlete performance, manage teams |
| 💼 **Sponsors** | Create profiles, post campaigns, sign digital contracts |
| 📋 **Managers** | Oversee athlete careers and club administration |
| 👥 **Fans** | Follow athletes, watch shorts, browse events |

### Key Features at a Glance
- ✅ **PWA / Offline Mode** — Full functionality without internet (Service Worker caching)
- ✅ **Live Sports News** — Automatically refreshes when online, cached for offline
- ✅ **Sponsorship Contracts** — Digital contracts with PDF generation
- ✅ **Merit Scoring** — Athletes earn verified "Sportiva Points" through exploits
- ✅ **Instagram-Style Feed** — Posts, Reels/Shorts, Stories
- ✅ **Interactive Maps** — Leaflet-powered venue mapping (works offline)
- ✅ **Multi-Language** — English, French, Spanish, German, Arabic, Portuguese
- ✅ **Installable as App** — Install as a standalone desktop/mobile PWA

---

# 2. FIRST-TIME SETUP

## Step 2.1 — Open Project Folder

Open **Windows PowerShell** or the **VS Code Terminal** and navigate to the project:

```powershell
cd "C:\Users\NK-MAL\Documents\SPORTIVA CM 2.0"
```

📸 *Screenshot: Terminal showing the project directory*

## Step 2.2 — Activate the Virtual Environment

```powershell
.venv\Scripts\activate
```

You will see `(.venv)` appear at the start of your terminal prompt, confirming activation.

📸 *Screenshot: Terminal with (.venv) activated*

## Step 2.3 — Apply Database Migrations

This sets up all database tables:

```powershell
python manage.py migrate
```

Expected output: A list of applied migrations ending with `OK`.

📸 *Screenshot: Migration output showing all OK*

## Step 2.4 — Seed Sample Data

Load clubs, athletes, events, sponsors, and marketplace items:

```powershell
python manage.py seed_data
```

> ⚠️ Only run this once. Running it multiple times may create duplicate data.

📸 *Screenshot: Seed data output showing created records*

## Step 2.5 — Run Automated Tests (Optional)

Verify all 27+ tests pass:

```powershell
python manage.py test --verbosity=1
```

Expected: `OK` with all tests passing.

---

# 3. STARTING SPORTIVA

## Step 3.1 — Start the Local Server

```powershell
python manage.py runserver
```

You will see:
```
System check identified no issues (0 silenced).
Django version 6.0.7, using settings 'sportiva_cm.settings'
Starting development server at http://127.0.0.1:8000/
```

📸 *Screenshot: Server running in terminal*

## Step 3.2 — Open in Your Browser

Open **Google Chrome** (recommended for PWA features) and visit:
```
http://127.0.0.1:8000/
```

📸 *Screenshot: SPORTIVA home page loading in browser*

---

## Online Mode vs. Offline Mode

SPORTIVA works like **Facebook**: it serves cached content offline and syncs data when a connection is restored.

| Situation | Behavior |
|-----------|----------|
| **Online (Wi-Fi/Ethernet connected)** | Full functionality + live sports news refresh |
| **Offline (Wi-Fi disabled)** | Cached pages load instantly + amber offline badge appears |
| **Reconnected** | Green "Back Online — Syncing…" notification + news refresh |

### How to Test Offline Mode

1. Open the app and browse several pages (home, events, profiles)
2. **Chrome**: Open DevTools (F12) → **Network** tab → Change "No throttling" to **"Offline"**
3. Navigate the site — cached pages will load perfectly
4. Switch back to "No throttling" to go back online

📸 *Screenshot: Chrome DevTools Network tab in Offline mode*
📸 *Screenshot: Amber offline badge visible on screen*
📸 *Screenshot: Green "Back Online" notification on reconnect*

---

# 4. HOME DASHBOARD

The homepage is divided into three main sections:

## Left Sidebar
- **Your Profile Card** (when logged in) — shows avatar, tier badge, followers, exploits count
- **Sports Disciplines** — filter feed by sport category

## Center Feed
- **Stories & Shorts Carousel** — horizontal scroll of athlete videos/posts
- **Personalized Feed** — posts ranked by your favorite sports
- **Create Post button** — share content directly from home

## Right Sidebar
- **Top Athletes Leaderboard** — ranked by Sportiva Score
- **Upcoming Events** — next 4 tournaments
- **Verified Sponsors** — global sponsor directory
- **🆕 Global Sports News** — live ticker with discipline icons (Football ⚽, Basketball 🏀, Athletics 🏃, Tennis 🎾, Swimming 🏊, Rugby 🏉, Cycling 🚴, Cricket 🏏, Combat 🥊)

📸 *Screenshot: Full home dashboard (left + center + right)*
📸 *Screenshot: Global Sports News section in right sidebar*

### Hero Statistics Bar
At the top you will see four counters:
- **Global Athletes** count
- **Clubs & Academies** count
- **Active Tournaments** count
- **Verified Sponsors** count

---

# 5. ACCOUNT REGISTRATION & LOGIN

## Step 5.1 — Register a New Account

1. Click **"Join as Athlete or Fan"** on the home page OR navigate to `/accounts/register/`
2. Fill in the registration form:

| Field | Required | Notes |
|-------|----------|-------|
| Username | ✅ | Unique, lowercase letters/numbers |
| Email | ✅ | Used for notifications |
| Password | ✅ | Must meet security requirements |
| Role | ✅ | Choose: Athlete / Coach / Club / Sponsor / Manager / Fan |
| Full Name | ✅ | First and Last name |
| Country | ✅ | Used for global search and display |
| City | ✅ | Location for local matching |
| Sport(s) | Optional | Used for personalized feed |

3. Click **"Create My Account"**

📸 *Screenshot: Registration form*

## Step 5.2 — Log In

1. Navigate to `/accounts/login/` or click **"Log In"** in the navbar
2. Enter your **Username** and **Password**
3. Click **"Sign In"**

📸 *Screenshot: Login form*

## Step 5.3 — Change Language

Click the **language globe icon** (🌐) in the navbar to switch between:
🇬🇧 English | 🇫🇷 Français | 🇪🇸 Español | 🇩🇪 Deutsch | 🇸🇦 العربية | 🇧🇷 Português

📸 *Screenshot: Language selector dropdown*

---

# 6. ATHLETE PROFILE MANAGEMENT

## Step 6.1 — View Your Profile

Click your **avatar/username** in the navbar → **"My Profile"** or go to `/accounts/profile/`

Your profile shows:
- Personal info (name, city, country, sport)
- **Sportiva Tier Badge** (🥉 Bronze → 🥈 Silver → 🥇 Gold → 💎 Diamond → 🌟 Legend)
- **Sportiva Score** (points from verified exploits)
- Followers / Following / Exploits count
- Recent posts and exploit history

📸 *Screenshot: Athlete profile page*

## Step 6.2 — Edit Profile

1. On your profile page, click **"Edit Profile"**
2. Update fields: bio, avatar, sport specialization, favorite sports, city, country
3. Click **"Save Changes"**

📸 *Screenshot: Profile edit form*

## Step 6.3 — Follow / Connect with Athletes

1. Visit any athlete's profile from the leaderboard or search
2. Click **"Follow"** button
3. Their posts will appear in your personalized feed

---

# 7. EXPLOITS & MERIT SCORING SYSTEM

This is SPORTIVA's unique differentiation system that objectively ranks athletes.

## Understanding Sportiva Score

| Tier | Score Range | Badge |
|------|------------|-------|
| Bronze | 0 – 499 | 🥉 |
| Silver | 500 – 1,499 | 🥈 |
| Gold | 1,500 – 4,999 | 🥇 |
| Diamond | 5,000 – 14,999 | 💎 |
| Legend | 15,000+ | 🌟 |

## Step 7.1 — Log an Exploit

1. From the home page, click **"Log Exploits & Merits"** OR go to `/accounts/exploits/add/`
2. Fill in the form:

| Field | Description |
|-------|-------------|
| Title | Name of achievement (e.g., "Gold Medal – 100m Sprint") |
| Description | Detailed account of the exploit |
| Date | When the exploit occurred |
| Location | Where it took place |
| Proof URL | Link to video/article for verification |
| Points | Self-reported points (subject to verification) |

3. Click **"Submit Exploit"**

📸 *Screenshot: Add exploit form*

## Step 7.2 — Exploit Verification

Exploits start with status **"Pending"**. They can be verified by:
- ✅ **Club Manager** of the athlete's club
- ✅ **Coach** assigned to the athlete
- ✅ **Event Organizer** of the relevant event
- ✅ **Sponsor** linked by contract
- ✅ **Admin**

Once verified, the exploit's points are added to the athlete's **Sportiva Score**, which updates their tier badge and position on the leaderboard.

📸 *Screenshot: Exploit detail page showing verification status*

## Step 7.3 — Verify an Exploit (For Coaches/Managers)

1. Go to the athlete's profile
2. Click on an exploit marked **"Pending"**
3. Review the evidence (proof URL)
4. Click **"Verify"** or **"Reject"** with a reason

---

# 8. CLUBS & ORGANIZATIONS

## Step 8.1 — Browse Organizations

Navigate to `/organizations/` to see all registered clubs, academies, and sports organizations.

Filter by:
- Sport discipline
- Country / City
- Organization type (Club, Academy, Federation, etc.)

📸 *Screenshot: Organizations list page*

## Step 8.2 — Register Your Club/Organization

1. Register an account with role **"Club / Organization"**
2. Go to `/organizations/register/`
3. Fill in:
   - Organization name
   - Type (Sports Club, Academy, etc.)
   - Primary sport
   - Location (country, city)
   - Contact information
   - Description

📸 *Screenshot: Organization registration form*

## Step 8.3 — Manage Club Roster

From your organization's dashboard:
- **Add Athletes**: Invite athletes by username to join your roster
- **Remove Athletes**: Remove members from the roster
- **Set Coaches**: Assign coach roles to specific members

---

# 9. EVENTS & TOURNAMENTS

## Step 9.1 — Browse Events

Navigate to `/events/` to see all upcoming and past tournaments.

📸 *Screenshot: Events list page with filter options*

## Step 9.2 — View Event Details

Click any event to see:
- Full description and rules
- Date, time, and location
- **Interactive Leaflet Map** (works offline) showing venue location
- Registration status and spots remaining
- Entry fee (if applicable)
- Registered participants

📸 *Screenshot: Event detail page with map*
📸 *Screenshot: Location popup modal with GPS coordinates*

## Step 9.3 — Register for an Event

1. On the event detail page, click **"Register Now"**
2. Confirm your participation
3. Receive a confirmation message

📸 *Screenshot: Event registration confirmation*

## Step 9.4 — Create an Event (Organizers)

1. Navigate to `/events/create/`
2. Fill in:

| Field | Required | Description |
|-------|----------|-------------|
| Title | ✅ | Tournament/event name |
| Sport | ✅ | Select discipline |
| Description | ✅ | Rules, format, prizes |
| Date & Time | ✅ | Start and end |
| City | ✅ | Venue city |
| Country | ✅ | Host country |
| Latitude/Longitude | Optional | For interactive map pin |
| Entry Fee | Optional | Leave blank for free |
| Max Participants | ✅ | Capacity limit |

📸 *Screenshot: Create event form*

---

# 10. SPONSORSHIPS SYSTEM

## Step 10.1 — How Sponsorships Work

```
Sponsor Profile → Sponsorship Campaign → Contract → Athlete/Club
```

1. **Sponsor** creates a profile and defines available sponsorship packages
2. **Athlete/Club** browses campaigns and submits a request
3. **Sponsor** reviews and approves the request
4. A **digital contract** is generated (PDF downloadable)
5. The **athlete is linked** to the sponsor on their profile

## Step 10.2 — Create a Sponsor Profile

1. Register/login with role **"Sponsor"**
2. Navigate to `/sponsorships/sponsor/create/`
3. Fill in:
   - Company name
   - Industry (e.g., Sports Equipment, Financial Services)
   - Logo
   - Description
   - Budget range
   - Preferred sports/disciplines

📸 *Screenshot: Sponsor profile creation form*

## Step 10.3 — Create a Sponsorship Campaign

1. From your sponsor dashboard, click **"New Campaign"**
2. Fill in:
   - Campaign title
   - Target sport(s)
   - Budget offered
   - Target athlete type (individual/club)
   - Duration
   - Terms and conditions

📸 *Screenshot: Create campaign form*

## Step 10.4 — Athlete Applies for Sponsorship

1. Navigate to `/sponsorships/`
2. Browse available campaigns
3. Click **"Apply / Request Sponsorship"**
4. Write a pitch message explaining why you are a good fit
5. Submit the application

📸 *Screenshot: Sponsorship application form*

## Step 10.5 — Sponsor Reviews & Signs Contract

1. Sponsor logs in → Dashboard shows pending applications
2. Click on an application to view the athlete's profile, exploits, and score
3. Click **"Accept & Generate Contract"** OR **"Decline"**
4. A digital contract PDF is auto-generated with both parties' details

📸 *Screenshot: Contract review page*
📸 *Screenshot: Generated PDF contract*

## Step 10.6 — Linked Athletes on Sponsor Profile

After contract signing, the athlete appears as **"Sponsored"** on:
- The athlete's own profile page
- The sponsor's public profile page

---

# 11. SPORTS FEED & MEDIA

## Step 11.1 — Browse the Global Feed

Navigate to `/media-feed/` to see all posts and shorts.

Filter by:
- **All** posts
- **Shorts/Reels** (short videos)
- **By Sport** discipline

📸 *Screenshot: Media feed with posts and shorts*

## Step 11.2 — Create a Post or Short

1. Click **"Create Short / Post"** (home page) or navigate to `/media-feed/create/`
2. Choose type:
   - **Post** — text and image content
   - **Short/Reel** — short video (under 60 seconds)
3. Fill in title, description, attach media
4. Select sport category
5. Click **"Publish"**

📸 *Screenshot: Post creation form*

## Step 11.3 — Like, Comment, and Follow

On any post:
- **Heart ❤️** — Like/unlike a post
- **💬 Comment** — Leave a text comment
- **Follow** the author from their profile

📸 *Screenshot: Post detail with likes and comments*

## Step 11.4 — Stories Carousel

The horizontal stories bar at the top of the home page shows recent shorts from athletes you follow. Click any avatar ring to view that athlete's latest content.

---

# 12. GLOBAL SPORTS NEWS TICKER

The news section is visible in the **right sidebar** of the home page.

## How It Works

| Mode | Behavior |
|------|----------|
| **Online** | Fetches fresh articles from `/api/sports-news/` every time you go online |
| **Offline** | Shows the last-cached batch of articles (stored in localStorage) |
| **First Load** | Server renders 6 articles instantly (always available offline) |

## News Disciplines Covered

⚽ Football | 🏀 Basketball | 🏃 Athletics | 🎾 Tennis | 🏊 Swimming | 🏉 Rugby | 🚴 Cycling | 🏏 Cricket | 🥊 Combat Sports

📸 *Screenshot: News ticker showing sports articles with discipline badges*
📸 *Screenshot: Green LIVE badge on news ticker when online*

---

# 13. MARKETPLACE

## Step 13.1 — Browse the Marketplace

Navigate to `/marketplace/` to view sports equipment and services for sale.

Filter by:
- Category (Equipment, Jerseys, Coaching, etc.)
- Price range
- Sport discipline

📸 *Screenshot: Marketplace listings grid*

## Step 13.2 — List an Item

1. Go to `/marketplace/create/`
2. Fill in:
   - Title
   - Description
   - Category
   - Price
   - Images
   - Contact method

📸 *Screenshot: Create marketplace listing form*

## Step 13.3 — Contact a Seller

1. Click on any listing
2. Click **"Contact Seller"** to start a direct message conversation

---

# 14. DIRECT MESSAGING (CHAT)

## Step 14.1 — Start a Conversation

1. Navigate to any user's profile
2. Click **"Send Message"** OR click **"Chat"** in the navbar
3. Type your message and press Enter or click **"Send"**

📸 *Screenshot: Chat conversation view*

## Step 14.2 — View All Conversations

Navigate to `/chat/` to see all your active conversations, sorted by most recent.

---

# 15. OFFLINE MODE & PWA INSTALLATION

## How Offline Mode Works

SPORTIVA uses a **Progressive Web App (PWA) Service Worker** that:
1. On first visit, **pre-caches** all static assets (CSS, fonts, icons, maps, JS)
2. On subsequent visits, **serves assets from cache** (0ms load time)
3. For pages you've visited, **serves the cached HTML** when offline
4. For the **news API**, caches the last response in both browser cache and localStorage

## Available Offline (No Internet Needed)

✅ Home dashboard with cached stats  
✅ Athlete profiles and leaderboard  
✅ Clubs & organizations directory  
✅ Event listings with interactive maps  
✅ Marketplace listings  
✅ Sports news (last cached batch)  
✅ All static UI (fonts, icons, animations)

## Requires Internet Connection

⚠️ Sending new chat messages  
⚠️ Uploading new posts/media  
⚠️ Real-time sports news refresh  
⚠️ Submitting new applications  

## Step 15.1 — Install as a Desktop App (PWA)

1. Open SPORTIVA in **Google Chrome**
2. Look for the **install icon** (⊕) in the browser address bar
3. Click **"Install SPORTIVA"**
4. SPORTIVA now appears as a standalone app on your desktop

📸 *Screenshot: Chrome install PWA prompt*
📸 *Screenshot: SPORTIVA as standalone desktop app*

## Step 15.2 — Test Offline Mode

1. Start the server: `python manage.py runserver`
2. Open Chrome DevTools: **F12** → **Network** tab
3. Set throttling to **"Offline"**
4. Navigate across the site — all cached pages work
5. The amber badge **"Offline Mode — Cached content available"** will appear at the bottom

📸 *Screenshot: DevTools set to Offline*
📸 *Screenshot: Amber offline badge visible on screen*

## Step 15.3 — Reconnection Behavior

When you switch back online:
1. Green **"Back Online — Syncing latest sports news…"** notification pops up
2. News ticker automatically refreshes with fresh articles
3. Any actions you missed will resume normally

📸 *Screenshot: Green reconnection notification banner*

---

# 16. ADMINISTRATION PANEL

## Access the Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with admin credentials:
   - **Username**: `camer_admin`
   - **Password**: `Admin237!`

📸 *Screenshot: Django admin panel*

## Admin Capabilities

| Section | What You Can Do |
|---------|----------------|
| Users | Create, edit, deactivate any user account |
| Exploits | Verify/reject athlete exploits and award points |
| Events | Create, edit, publish/unpublish events |
| Sponsorships | Manage contracts and campaigns |
| Organizations | Approve/reject club registrations |
| Posts | Moderate feed content, remove flagged posts |
| Marketplace | Remove inappropriate listings |

---

# 17. DEFAULT ACCOUNTS REFERENCE

Use these pre-seeded accounts to test all features:

| Role | Username | Password | Can Do |
|------|----------|----------|--------|
| **Admin** | `camer_admin` | `Admin237!` | Everything |
| **Club/Org** | `douala_fc` | `Admin237!` | Manage club, create events |
| **Coach** | `coach_samuel` | `Admin237!` | Verify exploits, manage athletes |
| **Athlete** | `rigobert_song` | `Admin237!` | Create posts, add exploits |
| **Sponsor** | `mtn_cameroun` | `Admin237!` | Create campaigns, sign contracts |

---

# 18. TROUBLESHOOTING

## "ModuleNotFoundError" when running the server

**Fix:** The virtual environment is not activated. Run:
```powershell
.venv\Scripts\activate
```
Then try again.

## "Table doesn't exist" or database errors

**Fix:** Run migrations:
```powershell
python manage.py migrate
```

## News ticker shows "Loading…" indefinitely

**Fix:** This happens if JavaScript is blocked. Ensure no extensions (ad blockers) are blocking `/api/sports-news/`. If offline, the server-rendered news should appear automatically.

## Pages don't load offline

**Fix:** The Service Worker needs to cache pages first. Visit the pages you want offline **while connected to the internet** at least once. The Service Worker will cache them for future offline use.

## Old cached version shows after an update

**Fix:** The browser may be showing an older cached version. Hard refresh:
```
Ctrl + Shift + R  (Windows/Linux)
Cmd + Shift + R   (Mac)
```
Or open DevTools → Application → Service Workers → Click **"Update"** then **"Skip Waiting"**.

## "NoReverseMatch" error

**Fix:** Make sure migrations have been applied and the server has been restarted:
```powershell
python manage.py migrate
python manage.py runserver
```

## How to reset/clear all data and start fresh

```powershell
del db.sqlite3
python manage.py migrate
python manage.py seed_data
```

---

# QUICK REFERENCE CARD

| Task | URL | Shortcut |
|------|-----|----------|
| Home Dashboard | `/` | Navbar: SPORTIVA logo |
| Sports Feed | `/media-feed/` | Navbar: Feed icon |
| Events | `/events/` | Navbar: Events icon |
| Marketplace | `/marketplace/` | Navbar: Store icon |
| Sponsorships | `/sponsorships/` | Navbar: Handshake icon |
| Chat | `/chat/` | Navbar: Messages icon |
| My Profile | `/accounts/profile/` | Navbar: Avatar |
| Add Exploit | `/accounts/exploits/add/` | Home: "Log Exploits" button |
| Admin | `/admin/` | Direct URL |
| Sports News API | `/api/sports-news/` | JSON endpoint |
| Offline Page | `/offline/` | Auto: when network lost |

---

*SPORTIVA — Empowering Sporting Talent Worldwide*
*© 2026 SPORTIVA Global Network. All rights reserved.*

