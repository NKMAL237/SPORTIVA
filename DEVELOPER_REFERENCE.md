# SPORTIVA CM 2.0 — Developer Capability Reference

> **What this file is.** A single, self-contained reference describing everything the SPORTIVA platform does, from a developer's point of view. It is written so that a developer who has never seen the codebase can (1) understand immediately what the application is and does, and (2) perform analysis on it — data model, business rules, permission matrix, state machines, and full HTTP surface — without opening the code.
>
> Companion documents: `PROJECT_ANALYSIS_UML.md` (UML diagrams & architecture analysis), `GUIDE_POST_AND_DELETE.md` (end-user guide).

---

## Table of Contents

1. [Application Overview](#1-application-overview)
2. [Tech Stack & Architecture](#2-tech-stack--architecture)
3. [Setup, Run, Test, Seed](#3-setup-run-test-seed)
4. [Roles & Capability Matrix](#4-roles--capability-matrix)
5. [Module-by-Module Capabilities](#5-module-by-module-capabilities)
6. [Complete HTTP Route Reference](#6-complete-http-route-reference)
7. [Data Model Reference](#7-data-model-reference)
8. [State Machines](#8-state-machines)
9. [Business Rules & Invariants](#9-business-rules--invariants)
10. [Scoring Engine](#10-scoring-engine)
11. [Permissions & Tab System](#11-permissions--tab-system)
12. [Offline-First / PWA Architecture](#12-offline-first--pwa-architecture)
13. [Analysis Notes: Design Decisions & Limitations](#13-analysis-notes-design-decisions--limitations)
14. [Test Inventory](#14-test-inventory)

---

## 1. Application Overview

**SPORTIVA CM 2.0** is a Django server-rendered web platform that connects five kinds of sports actors — **athletes, clubs/academies (organizations), coaches/trainers, sponsors, and fans (visitors)** — in one "global sports ecosystem". It is an offline-first Progressive Web App (PWA) designed for markets with unreliable connectivity.

In one sentence: *athletes build a verified merit profile and score, organizations run tournaments with paid registrations and PDF invoices, everyone trades gear in a marketplace, sponsors fund athletes through proposals/contracts and crowdfunding pledges, and all of it works from a cached, queue-based offline layer.*

### Functional pillars

| Pillar | Module(s) | What it does |
|---|---|---|
| Identity & merit | `accounts` | Registration/login, roles, profiles, follows, athlete "exploits" with third-party verification, endorsements, a global **Sportiva Score** and tier system |
| Tournaments | `events` + `organizations` | Organizations publish events (geo-located, capacity-limited, paid or free); users register & "pay"; branded PDF invoices/tickets; organizer check-in; cancellation with refund status; sport-matched trophy imagery |
| Social feed | `media_feed` + `core` | Instagram-style feed: posts, photos, video links, shorts/reels, hashtags, likes, comments, per-user personalization tabs (For You / Following / Shorts / Trending) |
| Commerce | `marketplace` | Classified listings for sports gear with condition grades, geo-location, WhatsApp contact |
| Sponsorship economy | `sponsorships` | Sponsor directory & profiles, bidirectional sponsorship proposals that auto-convert into digital contracts on acceptance, athlete crowdfunding campaigns with pledges |
| Messaging | `chat` | Server-rendered 1-on-1 direct messages with file attachments, read receipts, unread counts |
| Platform shell | `core` | Home hub, offline page, service worker, web app manifest, curated sports-news feed |

---

## 2. Tech Stack & Architecture

| Layer | Technology |
|---|---|
| Framework | Django 6.0.7 (server-side rendered; **no ASGI/channels** — plain WSGI) |
| Database | SQLite (`db.sqlite3`) |
| Auth | Custom user model `accounts.User` (`AUTH_USER_MODEL`), session-based, 5 roles |
| Templates | Django Template Language; Tailwind CSS via **vendored Play CDN runtime** (`frontend/static/vendor/tailwind/`) — no build step; FontAwesome + Leaflet vendored locally; crispy-forms/tailwind pack |
| i18n | `LocaleMiddleware`, 6 languages (en, fr, es, de, ar, pt), `LOCALE_PATHS=locale`, `/i18n/` set-language URL |
| PWA | Hand-written service worker (`frontend/static/sw.js`, cache `sportiva-v5`) + manifest |
| PDF | reportlab (`events/services/invoice_generator.py`) |
| Installed-but-unused | `djangorestframework`, `django_filters` — present in `INSTALLED_APPS`, **no API views exist**; news is a hardcoded feed served as JSON |

### Repository layout

```
sportiva_cm/          # project package: settings.py, urls.py (root URLconf)
accounts/             # users, roles, follows, exploits, endorsements, score, tab perms
core/                 # home hub, offline page, sw.js/manifest serving, news API
events/               # events, registrations, payments(sim), invoices, validation
media_feed/           # posts, likes, comments
marketplace/          # product listings
organizations/        # club/academy profiles + SportsCategory lookup
sponsorships/         # sponsors, proposals→contracts, campaigns, pledges
chat/                 # conversations & messages (only app with app_name='chat')
frontend/templates/   # all DTL templates (APP_DIRS off; DIRS points here)
frontend/static/      # css/js/images/vendor; sw.js lives here
media/                # user uploads (avatars, posts, invoices, ...)
locale/               # translation catalogs
```

### Request pipeline (analysis view)

```
Browser → (Service Worker intercepts: cache / offline queue)
        → Django (LocaleMiddleware → auth/session → tab_required guard)
        → View (decorators: login_required, tab_required, owner/staff in-view checks)
        → ORM (SQLite; score via annotate() to avoid N+1)
        → DTL template (context processor injects allowed_tabs)
```

**Every page** gets `allowed_tabs` from `accounts.context_processors.tab_access`; the navbar/mobile bar render only permitted tabs — this is the role-based UI gate.

---

## 3. Setup, Run, Test, Seed

```bash
# Windows venv (as configured in this repo)
.venv\Scripts\activate

# Install deps
pip install -r requirements.txt        # Django 6.0.7, reportlab, crispy-forms, pillow, python-dotenv

# Database (dev uses committed sqlite; create fresh if missing)
python manage.py migrate

# Seed the full demo dataset: 16 users (5 roles), 5 orgs, 10+ events,
# posts, sponsors, campaigns, exploits (passwords reset to documented demo values)
python manage.py seed_data

# Run
python manage.py runserver

# Verify
python manage.py check
python manage.py test                  # 27 tests across 6 test cases (see §14)
```

Demo access (see `USERS_CREDENTIALS.md` — do **not** commit that file): superuser `sportiva_admin` / `Admin2026!`; all other personas `Pass2026!`.

Environment: python-dotenv if `.env` present; dev defaults are permissive (insecure `SECRET_KEY`, `DEBUG=True`, `ALLOWED_HOSTS=*`) — **harden before any real deployment**.

---

## 4. Roles & Capability Matrix

Roles live on `User.role` (`accounts/models.py`): `ATHLETE`, `ORGANIZATION`, `TRAINER`, `SPONSOR`, `VISITOR`.

| Capability | Guest | Athlete | Organization | Trainer | Sponsor | Visitor | Staff/Admin |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Browse feed, events, marketplace, orgs, sponsorships | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Register / log in | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Create posts, like, comment, follow | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Chat (direct messages) | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Publish events | | | ✓ | | | | ✓ |
| Register & "pay" for events | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Validate event check-ins, issue invoices | | | ✓ (own events) | | | | ✓ |
| Sell products on marketplace | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Submit exploits for verification | | ✓ | | | | | ✓ |
| **Verify/reject exploits** (score gate) | | | ✓ | ✓ | ✓ | | ✓ |
| Endorse athletes | | | ✓ | ✓ | ✓ | | ✓ |
| Sponsor profile + send proposals | | | | | ✓ | | ✓ |
| Launch crowdfunding campaigns | | ✓ | | | | | ✓ |
| Pledge to campaigns | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Manage user tab permissions (`/accounts/users/`) | | | | | | | ✓ |

Staff/superusers bypass all tab restrictions and pass every owner/staff check (they can delete/verify anything).

---

## 5. Module-by-Module Capabilities

### 5.1 `accounts` — identity, merit & reputation

- **Register** (`/accounts/register/`): manual POST parsing — required fields, password match, ≥8 chars, unique username/email; auto-login after creation. Role chosen at registration drives the default tab set.
- **Login/logout** (`/accounts/login/`, `/accounts/logout/`): `next` redirect is sanitized with `url_has_allowed_host_and_scheme` (open-redirect guard).
- **Profiles**: own dashboard (`/accounts/profile/`); any public profile (`/accounts/profile/<username>/`) showing verified exploits, endorsements, score/tier, recent posts, event attendance, follow button. Pending exploits are visible **only** to owner or ORGANIZATION/TRAINER/SPONSOR/staff.
- **Profiles directory** (`/profiles/`): filters — search text, role, country, sport (matched on `favorite_sports` JSON), sort; top-5 athlete leaderboard via the SQL score annotation.
- **Follows** (`/accounts/follow/<id>/`): toggle POST; unique per (follower, followed) pair.
- **Exploits** (`/accounts/exploits/…`): athletes log achievements (title, category MEDAL/RECORD/TITLE/MVP/MATCH_WIN/CAPTAINCY/OTHER, competition, date, description, proof image/link). Status flow `PENDING → VERIFIED | REJECTED`. Editing resets to PENDING. Verification is restricted to ORGANIZATION/TRAINER/SPONSOR/staff and **never the athlete themselves**; verified exploits grant `score_points` (default 35) into the Sportiva Score. Deletion is owner-or-staff with a confirmation page warning about score recalculation.
- **Endorsements** (`/accounts/athletes/<id>/endorse|unendorse/`): `update_or_create` on (athlete, endorser, skill) — re-endorsing the same skill updates the comment; unique constraint enforces it. Any endorser can retract their own endorsement.
- **Score & tier**: computed property + SQL twin (see §10); tiers Legendary/Elite/Pro/Rising Star.
- **User management** (`/accounts/users/`, staff): per-user override of role, active/verified flags, and the full tab-permission dict from checkbox POSTs.

### 5.2 `core` — platform shell

- **Home** (`/`): the hub. Shorts carousel (top-10 `is_short` posts), personalized feed (posts matching viewer `favorite_sports` first), composer, sports-discipline chips (filter feed by sport), top-5 athletes, 4 upcoming events (with sport trophy thumbnails), 4 sponsors, 6 curated news items, platform stats.
- **Offline page** (`/offline/`): branded fallback for navigation requests when uncached.
- **PWA endpoints**: `/sw.js` and `/manifest.json` served via `django.contrib.staticfiles.finders` with inline fallback content.
- **News API** (`/api/sports-news/`): 12 hardcoded curated articles as JSON (`status/online/count/articles/last_updated`) — designed for Service Worker caching; **not** a live news service.

### 5.3 `events` — tournaments, registration & payments

- **Event lifecycle**: create (any logged-in user; `EventForm` with Tailwind widgets), published listing (`/events/`, guests allowed), detail page with geo-location popup, WhatsApp/email organizer, registration.
- **Registration & payment** (`/events/<pk>/register-payment/`, alias `rsvp`): blocks duplicate active registrations; capacity is re-checked inside `transaction.atomic()` with `Event.objects.select_for_update()` to prevent overselling; re-registering over a CANCELLED row reuses it in place. **Payment is simulated** — `payment_method` taken from POST, amount = event `fee_amount`; `FREE` events skip money. Generates `INV-<year>-<hex>` invoice number and a **branded PDF entry ticket/invoice** (reportlab) stored on the registration.
- **Invoice download** (`/events/registration/<pk>/invoice/`): regenerates the PDF on every request; owner, event organizer, or staff only.
- **Organizer check-in** (`/events/registration/<pk>/validate/`): VALIDATE → `organizer_validated=True`, status CONFIRMED; CANCEL → status CANCELLED. Organizer or staff only.
- **Cancellation** (`/events/registration/<pk>/cancel/`): registrant or staff; sets `status=CANCELLED`, `payment_status=REFUNDED`, audit note.
- **Event deletion**: organizer or staff; GET confirmation page, POST deletes.
- **Imagery**: `Event.SPORT_IMAGE_MAP` keyword-matches the sport name to one of 10 trophy SVGs (`trophy_image_key`, fallback `generic`) shown on cards and badges; events also support uploaded banners, venue coordinates (Leaflet map popup), capacity and `entry_fee` text + `fee_amount`/`currency`.

### 5.4 `media_feed` — social layer

- **Feed** (`/media-feed/`, guests allowed): four tabs — *For You* (personalized by favorite sports), *Following*, *Shorts*, *Trending* (sorted by like count); filters by sport and by `#tag`; top-10 shorts rail; create button.
- **Post types**: TEXT / IMAGE / VIDEO / SHORT / ARTICLE with optional uploaded image, video file (shorts/reels), YouTube/TikTok-style `video_url`, space-separated `#hashtags`, country/city geo-label with map popup.
- **Interactions**: like toggle (`get_or_create` + delete), comments (500 chars), follow shortcut on every card.
- **Deletion**: post delete is author-or-staff with a summary confirmation page (author, date, likes, comments, content preview) warning that likes/comments cascade; comments delete instantly via per-comment trash (author-or-staff). Posts have **no edit view** — users delete and recreate.
- **Counters**: `views_count`, `like_count()`, `comment_count()`.

### 5.5 `marketplace` — classifieds

- List (`/marketplace/`, guests): search + country/city/category/condition filters; available items only.
- Sell (`/marketplace/sell/`): title, category, description, price + currency, condition (NEW / LIKE_NEW / GOOD / FAIR), image, WhatsApp number, geo-coordinates.
- Detail: formatted price, seller card, **Direct Chat with Seller** (chat integration), prefilled **WhatsApp deep link** (`wa.me/<digits>?text=…`), location map popup when coordinates set.
- Delete: seller-or-staff with confirmation page.

### 5.6 `organizations` — clubs & academies

- Directory (`/organizations/`, guests) + detail page showing the org's published events (up to 6) and contact channels.
- One profile per user enforced (`organization_create` redirects to the existing profile); GET pre-fills country/city/phone/email from the user account. `OrganizationProfileForm` covers name, sports category, address, coordinates, logo, contacts, website.
- `is_verified` badge (admin-editable); `SportsCategory` is the shared sport lookup imported by `events` and `media_feed`.

### 5.7 `sponsorships` — the funding economy

- **Sponsor directory** (`/sponsorships/`): three tabs — sponsors, campaigns, contracts; search across sponsors & campaigns; current user's latest 5 sent/received proposals.
- **Sponsor profiles** (`/sponsorships/sponsors/<pk>/`): company card with industry, budget range, supported sports, offer/requirements; `sponsor_profile_edit` acts as create-or-edit (`get_or_create`, defaults company name to username). `brand_image_key` keyword-matches industry to a brand-art key.
- **Proposals** (`/sponsorships/proposals/send/`): bidirectional — ATHLETE_TO_SPONSOR, SPONSOR_TO_ATHLETE, EVENT_SPONSORSHIP; GET pre-targets via `sponsor_id`/`athlete_id`/`event_id`; amount is free text (e.g. "$5,000 / 2,500,000 FCFA").
- **Proposal response** (`…/respond/`): recipient-only; **ACCEPT auto-creates an ACTIVE `SponsorshipContract`** (`SPT-CTR-<year>-<hex>`, 365-day term, terms synthesized from deliverables + perks; athlete set only when the recipient is an ATHLETE). DECLINE sets DECLINED.
- **Withdrawal** (`…/withdraw/`): sender-or-staff, PENDING only → DECLINED with withdrawal note.
- **Crowdfunding campaigns** (`/sponsorships/campaigns/…`): create (category TRAVEL/EQUIPMENT/TRAINING/VENUE/MEDICAL/OTHER, target, deadline, banner, WhatsApp); detail shows `progress_percent()` capped at 100%; **pledge** (any logged-in user, min 1, optional message, anonymous flag) recalculates `raised_amount` as the pledge sum; delete pledge/campaign recalculates (creator-or-staff).

### 5.8 `chat` — direct messaging

- Inbox (`/chat/`, login required): split-screen conversation list + thread; POSTing `content` and/or `attachment` creates a message then PRG-redirects; opening a thread marks the other party's messages read.
- `start_direct_chat` (`/chat/start/<user_id>/`): finds an existing 1-on-1 by chained participant filters or creates one; self-chat blocked; two URL aliases.
- Access control: conversations are fetched guarded by `participants=request.user` → 404 for outsiders.
- **Server-rendered only — no polling, no websockets.** `unread_count_for(user)` exists for badges; messages have `is_read` flags and file attachments.

---

## 6. Complete HTTP Route Reference

Method legend: **G** GET, **P** POST. Auth: 🔓 public · 🔒 login · 👑 staff/owner gate (checked in view). All paths below the module prefix; root URLconf mounts modules at the paths shown.

### Root (`sportiva_cm/urls.py`)

| Path | Target |
|---|---|
| `/i18n/` | django set-language |
| `/admin/` | Django admin |
| `/` | core.urls |
| `/accounts/` | accounts.urls (mounted twice: bare + namespace `accounts:` — both resolve) |
| `/profiles/` | `profiles_list` |
| `/organizations/` | organizations.urls |
| `/events/` | events.urls |
| `/media-feed/` | media_feed.urls |
| `/marketplace/` | marketplace.urls |
| `/sponsorships/` | sponsorships.urls |
| `/chat/` | chat.urls (only namespaced app: use `chat:chat_inbox` etc. in templates) |

### `accounts` — prefix `/accounts/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `register/` | register | 🔓 | G,P | create account + auto-login |
| `login/` | login | 🔓 | G,P | session login (safe `next`) |
| `logout/` | logout | 🔓 | G/P | logout → home |
| `profile/` | profile | 🔒 | G | own dashboard |
| `profile/edit/` | profile_edit | 🔒 | G,P | edit profile |
| `profile/<username>/` | user_detail | 🔓 | G | public profile |
| `profile/<username>/view/` | profile_detail | 🔓 | G | alias of user_detail |
| `follow/<user_id>/` | toggle_follow | 🔒 | P | follow/unfollow toggle |
| `exploits/add/` | add_exploit | 🔒 | G,P | log achievement |
| `exploits/<id>/edit/` | edit_exploit | 🔒 👑 | G,P | edit (resets to PENDING) |
| `exploits/<id>/delete/` | delete_exploit | 🔒 👑 | G,P | confirm + delete |
| `exploits/<id>/verify/` | verify_exploit | 🔒 (role gate) | G,P | verify / reject |
| `athletes/<id>/endorse/` | endorse_athlete | 🔒 | P | add/update endorsement |
| `athletes/<id>/unendorse/` | remove_endorsement | 🔒 | P | retract own endorsement |
| `users/` | user_management | 🔒 staff tab | G | tab-permission dashboard |
| `users/<id>/update-tabs/` | user_update_tabs | 🔒 staff tab | P | apply overrides |

### `core` — prefix `/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | home | 🔓 | G | hub page |
| `offline/` | offline_view | 🔓 | G | offline fallback page |
| `sw.js` | service_worker | 🔓 | G | service worker JS |
| `manifest.json` | manifest | 🔓 | G | PWA manifest |
| `api/sports-news/` | sports_news_api | 🔓 | G | curated news JSON |

### `events` — prefix `/events/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | events_list | 🔓 (tab) | G | event listing |
| `create/` | event_create | 🔒 | G,P | publish event |
| `<pk>/` | event_detail | 🔓 | G | detail + register CTA |
| `<pk>/register-payment/` | event_register_payment | 🔒 | G,P | register + simulated payment + PDF invoice |
| `<pk>/rsvp/` | event_rsvp | 🔒 | G,P | alias of register-payment |
| `<pk>/delete/` | delete_event | 🔒 👑 (organizer/staff) | G,P | confirm + delete |
| `registration/<pk>/invoice/` | download_invoice_pdf | 🔒 👑 | G | regenerate/serve PDF |
| `registration/<pk>/validate/` | validate_registration | 🔒 👑 (organizer/staff) | G,P | check-in validate/cancel |
| `registration/<pk>/cancel/` | cancel_registration | 🔒 👑 (registrant/staff) | G,P | cancel + REFUNDED |

### `media_feed` — prefix `/media-feed/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | media_feed_list | 🔓 (tab) | G | feed (tabs/filters) |
| `create/` | post_create | 🔒 | G,P | publish post |
| `<pk>/` | post_detail | 🔓 | G,P | detail + comment (POST authed) |
| `<pk>/like/` | post_like | 🔒 | G,P | like/unlike toggle |
| `<pk>/delete/` | post_delete | 🔒 👑 (author/staff) | G,P | confirm + delete |
| `comments/<pk>/delete/` | comment_delete | 🔒 👑 (author/staff) | P | delete comment |

### `marketplace` — prefix `/marketplace/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | marketplace_list | 🔓 (tab) | G | listings + filters |
| `<pk>/` | product_detail | 🔓 | G | detail (404 if unavailable) |
| `sell/` | product_create | 🔒 | G,P | create listing |
| `<pk>/delete/` | product_delete | 🔒 👑 (seller/staff) | G,P | confirm + delete |

### `organizations` — prefix `/organizations/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | organizations_list | 🔓 (tab) | G | directory |
| `create/` | organization_create | 🔒 | G,P | create profile (one per user) |
| `<pk>/` | organization_detail | 🔓 | G | profile + events |

### `sponsorships` — prefix `/sponsorships/`

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | sponsorships_list | 🔓 (tab) | G | sponsors/campaigns/contracts tabs |
| `campaigns/create/` | campaign_create | 🔒 | G,P | launch campaign |
| `campaigns/<pk>/` | campaign_detail | 🔓 | G,P | detail + pledge (POST authed) |
| `campaigns/<pk>/delete/` | delete_campaign | 🔒 👑 (creator/staff) | G,P | confirm + delete |
| `sponsors/<pk>/` | sponsor_detail | 🔓 | G | sponsor card |
| `sponsors/edit/` | sponsor_profile_edit | 🔒 | G,P | create-or-edit own sponsor profile |
| `proposals/send/` | send_proposal | 🔒 | G,P | send proposal (3 directions) |
| `proposals/<pk>/respond/` | respond_proposal | 🔒 👑 (recipient/staff) | G,P | accept→contract / decline |
| `proposals/<pk>/withdraw/` | withdraw_proposal | 🔒 👑 (sender/staff) | G,P | confirm + withdraw (PENDING only) |
| `pledges/<pk>/delete/` | delete_pledge | 🔒 👑 (pledgor/staff) | G,P | confirm + delete (recalculates raised) |

### `chat` — prefix `/chat/` (namespace `chat`)

| Route | Name | Auth | Methods | Purpose |
|---|---|---|---|---|
| `` | chat:chat_inbox | 🔒 | G,P | inbox + send |
| `<conversation_id>/` | chat:chat_conversation | 🔒 | G,P | thread + send |
| `start/<user_id>/` | chat:start_direct_chat | 🔒 | G | open/create 1-on-1 |
| `start-chat/<user_id>/` | chat:chat_start | 🔒 | G | alias |

---

## 7. Data Model Reference

22 models across 8 apps. Relations: `──▶` FK, `⇢` OneToOne, `◆◆` M2M.

### accounts

**User** (extends `AbstractUser`; `AUTH_USER_MODEL`)
`role`(choices ATHLETE/ORGANIZATION/TRAINER/SPONSOR/VISITOR, default ATHLETE) · `phone_number` · `country`/`city` (defaults 'Global'/'Global City') · `bio` · `avatar` ImageField `avatars/` · `favorite_sports` JSONField list · social handles: `telegram/instagram/twitter/linkedin/tiktok/youtube` · `is_verified` · `custom_allowed_tabs` JSONField dict
Class data: `ALL_TABS` (9 entries), `DEFAULT_ROLE_TABS` per role. Methods: `get_allowed_tabs()`, `has_tab_access(tab)`, `clean_phone_for_whatsapp()`, `clean_social_link(network)`, `social_links`, `sportiva_score` (property), `sportiva_tier`, `is_followed_by(user)`.
Helpers: `sportiva_score_annotation()` — SQL twin of the score via correlated Subqueries (no fan-out); list views annotate, then the property reads `_sportiva_score`.

**Follow** ──▶ User ×2 (`follower`, `followed_user`); `unique_together(follower, followed_user)`.

**AthleteExploit** ──▶ User (`athlete`, related `exploits`); `title`, `category`(TITLE/MEDAL/MVP/RECORD/MATCH_WIN/CAPTAINCY/OTHER), `competition_name`, `date_achieved`, `description`, `proof_image` `exploits/`, `proof_link`; verification: `status`(PENDING/VERIFIED/REJECTED), `validated_by` ──▶ User SET_NULL, `validation_notes`, `score_points` PosInt default **35**.

**AthleteEndorsement** ──▶ User (`athlete`, `endorsed_by`); `skill_or_merit`, `comment`; `unique_together(athlete, endorsed_by, skill_or_merit)`.

### core
No models.

### events

**EventCategory** — `name` unique, `icon_class`.

**Event** ──▶ User (`organizer`, CASCADE) · ──▶ OrganizationProfile (SET_NULL) · ──▶ EventCategory · ──▶ SportsCategory; `country`/`city` · `venue_name` · `latitude`/`longitude` (Float, default 3.8864/11.5367 ≈ Yaoundé) · `start_date`/`end_date` · `description` · `banner` `events/` · `contact_whatsapp` · `entry_fee` text (default 'Free') · `fee_amount` PosInt 0 · `currency` default 'USD' · `max_participants` default 50 · `is_published`.
Class attr `SPORT_IMAGE_MAP`; methods `trophy_image_key`, `clean_whatsapp()`, `confirmed_participants_count()` (COMPLETED|FREE payments), `spots_remaining()`, `is_sold_out()`.

**EventRegistration** ──▶ Event (CASCADE, related `registrations`) · ──▶ User (CASCADE, related `event_registrations`); `registration_code` unique uuid4 · `team_or_club_name` · `status`(CONFIRMED/PENDING_VALIDATION/CANCELLED) · `payment_status`(COMPLETED/FREE/PENDING/REFUNDED) · `payment_method` default 'CARD' · `amount_paid`/`currency` · `invoice_number` unique · `invoice_pdf` FileField `invoices/` · `organizer_validated` bool default True · `organizer_validation_notes` · `registered_at`; `unique_together(event, user)`. Alias `EventAttendance = EventRegistration`.

### media_feed

**Post** ──▶ User (`author`) · ──▶ SportsCategory (SET_NULL null); `post_type`(TEXT/IMAGE/VIDEO/SHORT/ARTICLE) · `is_short` · `title` · `content` · `image` `media_feed/` · `video_file` `media_feed/shorts/` · `video_url` · `hashtags` (space-separated `#tags`) · `country`/`city` · `views_count` · `is_published`; methods `like_count()`, `comment_count()`, `is_liked_by(user)`, `hashtag_list()`.

**Comment** ──▶ Post (CASCADE) · ──▶ User; `content` ≤500.

**Like** ──▶ Post · ──▶ User; `unique_together(post, user)`.

### marketplace

**ProductCategory** — `name` unique, `icon_class`.

**Product** ──▶ User (`seller`) · ──▶ ProductCategory; `title`, `description`, `price` PosInt, `currency` default 'USD', `condition`(NEW/LIKE_NEW/GOOD/FAIR), `country`/`city`, `latitude`/`longitude`, `image` `marketplace/`, `whatsapp_number`, `is_available` default True; methods `clean_whatsapp()`, `price_formatted()`.

### organizations

**SportsCategory** — `name` unique, `icon_class`, `description` (shared lookup for events + feed).

**OrganizationProfile** ⇢ User (SET_NULL null, related `organization_profile`) · ──▶ SportsCategory; `name`, `country`/`city`, `address`, `lat`/`lng`, `description`, `logo` `organizations/`, phone/whatsapp/email/website, `is_verified`; method `clean_whatsapp()`.

### sponsorships

**SponsorProfile** ⇢ User (CASCADE, related `sponsor_profile`); `company_name`, `brand_tagline`, `industry`, `annual_budget_range`, `sports_supported` JSONField, `what_we_offer`, `requirements_criteria`, `website`, `country`/`city`, `address`, `lat`/`lng`, `logo` `sponsors/logos/`, `contact_email`, `whatsapp_number`, `is_verified` default True; `brand_image_key` property.

**SponsorshipRequest** ──▶ User (`sender`) · ──▶ User (`recipient_sponsor`, null) · ──▶ User (`recipient_athlete`, null) · ──▶ Event (SET_NULL null); `title`, `proposal_type`(ATHLETE_TO_SPONSOR/SPONSOR_TO_ATHLETE/EVENT_SPONSORSHIP), `amount` (free text), `deliverables_description`, `perks_offered`, `status`(PENDING/ACCEPTED/DECLINED/CONVERTED_TO_CONTRACT — note: converted status exists in choices but acceptance currently sets ACCEPTED), `response_message`.

**SponsorshipContract** ──▶ User (`sponsor`) · ──▶ User (`athlete`, null) · ──▶ Event (SET_NULL null); `contract_number` unique (`SPT-CTR-…`), `title`, `financial_value`, `terms_and_conditions`, `start_date`, `end_date`, `status`(DRAFT/ACTIVE/COMPLETED/TERMINATED), `sponsor_signed`/`beneficiary_signed` default True, `signed_at`.

**Campaign** ──▶ User (`creator`, CASCADE); `title`, `category`(TRAVEL/EQUIPMENT/TRAINING/VENUE/MEDICAL/OTHER), `description`, `target_amount`, `raised_amount`, `country`/`city`, `lat`/`lng`, `deadline`, `banner` `sponsorships/`, `whatsapp_number`, `is_active`; `progress_percent()` capped 100.

**Pledge** ──▶ Campaign (CASCADE) · ──▶ User (`sponsor`); `amount`, `message`, `is_anonymous`.

### chat

**Conversation** ◆◆ User (`participants`) · `subject` · `created_at`/`updated_at`; methods `get_other_participant(current_user)`, `latest_message()`, `unread_count_for(user)`.

**ChatMessage** ──▶ Conversation (CASCADE) · ──▶ User (`sender`); `content`, `attachment` `chat_attachments/`, `is_read`.

### Unique constraints (analysis-critical)

`Follow(follower, followed_user)` · `AthleteEndorsement(athlete, endorsed_by, skill_or_merit)` · `Like(post, user)` · `EventRegistration(event, user)` · `EventCategory.name` · `SportsCategory.name` · `OrganizationProfile` one-per-user (enforced in view) · `SponsorProfile` one-per-user (OneToOne) · unique invoice/registration/contract numbers.

---

## 8. State Machines

### AthleteExploit.status
```
            ┌──────────── edit ────────────┐
            ▼                              │
[PENDING] ──verify──▶ [VERIFIED]   [REJECTED]
   ▲                  (grants score_points)  ▲
   └──────────────── verify ─────────────────┘
   • editing any exploit resets it to PENDING
   • athlete cannot verify own exploit (role + non-self gate)
   • delete removes its points (score recalculates)
```

### EventRegistration (status × payment_status)
```
register-payment        cancel_registration          organizer validate
──────────────▶ CONFIRMED ──────────────▶ CANCELLED ───────────▶ (stays CANCELLED)
                payment: COMPLETED│FREE    payment: REFUNDED
PENDING_VALIDATION ──organizer VALIDATE──▶ CONFIRMED
• duplicate active registration blocked
• capacity enforced with select_for_update inside transaction.atomic()
• re-register reuses the CANCELLED row in place
```

### SponsorshipRequest.status
```
send ──▶ [PENDING] ──recipient ACCEPT──▶ [ACCEPTED] + auto-create ACTIVE SponsorshipContract
   ▲            └──recipient DECLINE──▶ [DECLINED]
   └──────── sender withdraw (PENDING only) ────────▶ DECLINED (withdrawal note)
```

---

## 9. Business Rules & Invariants

1. **Ownership gates** — every destructive action checks owner-or-staff in the view (posts, comments, products, events, exploits, campaigns, pledges, proposals). Staff/superuser passes all.
2. **Tab guard** — `@tab_required(tab)` on tabbed modules: guests get `DEFAULT_GUEST_TABS` (home, events, organizations, media_feed, marketplace, sponsorships); authenticated users without the tab are bounced home with an error; the navbar renders only `allowed_tabs` from the context processor.
3. **No oversell** — event registration re-checks capacity with row locking (`select_for_update`) inside an atomic block.
4. **One profile per user** — organizations (view-enforced) and sponsor profiles (OneToOne + get_or_create).
5. **No self-dealing** — athletes can't verify their own exploits; users can't chat with themselves; endorsement unique per (athlete, endorser, skill).
6. **Open-redirect guards** — login `next` validated with `url_has_allowed_host_and_scheme`; post-action redirects prefer explicit `next` POST field → safe fallback chain.
7. **Simulated money** — no real payment gateway; `payment_method` + amount recorded, `FREE` events skip payment; refunds are a status flip, no ledger.
8. **Score integrity** — score reads only VERIFIED exploits and non-CANCELLED registrations; list views must use `sportiva_score_annotation()` (correlated subqueries) to avoid multi-valued join fan-out.
9. **Cascade deletes** — deleting a post removes its likes/comments; deleting a campaign/pledge recalculates `raised_amount` from surviving pledges.
10. **PWA queue honesty** — offline POSTs are queued with full headers+body in IndexedDB and replayed on sync; the UI distinguishes document navigations (branded HTML 202) from XHR (JSON 202).

---

## 10. Scoring Engine

```
Sportiva Score = 50                                            (base)
               + Σ score_points of VERIFIED exploits           (default 35 each)
               + 5  × follower count
               + 10 × endorsement count
               + 15 × event registrations (excluding CANCELLED)
```

- `User.sportiva_score` (property) computes it in Python; `sportiva_score_annotation()` computes the identical value in SQL via correlated `Subquery`s so leaderboards don't fan out multi-valued relations (each component is a separate subquery, then summed).
- Tiers: **Legendary** ≥500 · **Elite** ≥250 · **Pro** ≥120 · **Rising Star** <120 (each tier dict carries `name/badge/color/bar_width` for UI).

---

## 11. Permissions & Tab System

`User.ALL_TABS` (9): home, profiles, events, organizations, media_feed, marketplace, sponsorships, chat, user_management.

| Tab | Guest | ATHLETE | ORGANIZATION | TRAINER | SPONSOR | VISITOR | Staff |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| home | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| profiles | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| events | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| organizations | ✓ | | ✓ | ✓ | ✓ | | ✓ |
| media_feed | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| marketplace | ✓ | ✓ | ✓ | ✓ | | ✓ | ✓ |
| sponsorships | ✓ | ✓ | ✓ | | ✓ | | ✓ |
| chat | | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| user_management | | | | | | | ✓ |

Resolution order in `get_allowed_tabs()`: staff/superuser → all tabs → per-role `DEFAULT_ROLE_TABS` → `custom_allowed_tabs` dict overrides (admin-editable per user at `/accounts/users/`).

---

## 12. Offline-First / PWA Architecture

`frontend/static/sw.js` (cache `sportiva-v5`) + `frontend/static/js/app.js` + `frontend/templates/core/offline.html`.

| Request type | Strategy |
|---|---|
| `/static/`, `/media/` GET | Cache-first + stale-while-revalidate |
| Navigation (HTML) | Network-first → cache → parent-path walk → `/offline/` |
| Document-mode POST (offline) | Queue to IndexedDB `sportiva-offline-queue`; respond 202 with self-contained branded "Action Saved Offline" HTML page |
| XHR/fetch POST (offline) | Queue; respond 202 JSON `{queued: true}` |
| Reconnect | Background Sync (`sportiva-offline-forms`) replays queue; `SYNC_COMPLETE` postMessage → toast "Offline actions synced" |

- Precached shell: home, offline page, key module index pages, CSS/JS/fonts/vendor (Tailwind, FontAwesome, Leaflet), 10 event trophy SVGs.
- Message banners auto-dismiss (5 s) via `app.js`.
- News API (`/api/sports-news/`) is cache-friendly JSON for the offline shell.
- Login works offline **once pages are cached** — session auth is cookie-based, so any cached authenticated page remains usable; mutations queue as above.

---

## 13. Analysis Notes: Design Decisions & Limitations

**Deliberate choices**
- **Monolith, server-rendered** — one deployable, SQLite, template-driven; matches an offline-first, low-infrastructure target.
- **Score as annotation + property pair** — single source of truth, two execution paths (Python vs SQL) kept identical by construction.
- **Contracts materialize from accepted proposals** — no separate contract-creation flow; acceptance is the signing event (both `*_signed` default True).
- **Simulated payments** — appropriate for a demo/academic capstone; the seam for a real gateway is `event_register_payment`.

**Known limitations (analysis findings)**
- `djangorestframework` + `django_filters` installed but unused — no REST API; the only JSON endpoint is the hardcoded news feed.
- Chat has **no realtime transport** (no websockets/long-polling); unread badges are computed on page load.
- News is a hardcoded constant (`BUILT_IN_NEWS`, 12 items) — no external API calls by design (offline-first rule).
- i18n: interface strings are translated, but **seed content is English-only** (≈1/6 of content localized).
- Payment simulation means no idempotency keys/webhooks; capacity locking mitigates race conditions but SQLite serializes writers anyway.
- `SponsorshipRequest.CONVERTED_TO_CONTRACT` status exists in choices but acceptance currently sets `ACCEPTED`.
- Dev settings are permissive (hardcoded dev `SECRET_KEY`, `DEBUG=True`, `ALLOWED_HOSTS=*`) — harden before deployment.

**Extension points**
- Real payment provider inside `event_register_payment` (keep the `select_for_update` seam).
- REST API via the already-installed DRF (serializers would map 1:1 onto §7 models).
- Realtime chat: swap `chat_inbox_view` PRG for an ASGI layer; models already carry `is_read`/unread counts.
- Sport imagery is data-driven (`SPORT_IMAGE_MAP` / `brand_image_key`) — add SVGs + keywords to extend.

---

## 14. Test Inventory

27 tests, 6 TestCase classes (all use Django test client):

| App | Class | Tests |
|---|---|---|
| accounts | `AccountsUnitTests` (4) | custom user creation & roles · register GET · login success · login GET |
| events | `EventsUnitTests` (4) | event creation (+whatsapp cleanup) · list view · detail view · rsvp POST creates registration |
| media_feed | `MediaFeedFlowTests` (6) | list loads · detail loads · create requires login · create POST · like toggle · comment add |
| marketplace | `MarketplaceFlowTests` (4) | list loads · detail loads · create requires login · create POST |
| organizations | `OrganizationsUnitTests` (4) | profile creation · list view · detail view · create requires login |
| sponsorships | `SponsorshipFlowTests` (5) | list loads · campaign detail loads · create requires login · create POST · pledge POST |
| core, chat | — | placeholder files, no tests yet (natural next coverage: offline endpoints, chat access guard, exploit verification gate) |

Run: `python manage.py test` → baseline **27 passed, 0 failures**.

---

*SPORTIVA CM 2.0 — Global Sports Network. Generated as the developer capability reference; pair with `PROJECT_ANALYSIS_UML.md` for diagrams and `GUIDE_POST_AND_DELETE.md` for end-user flows.*
