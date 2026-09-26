# SPORTIVA CM
## Project Requirements and Specifications Document

**Version:** 1.0  
**Date:** 7 September 2026  
**Project status:** MVP / academic demonstration release  
**Primary deployment context:** Cameroon-focused sports community platform with international expansion capability

---

## 1. Document Purpose

This document defines the requirements, scope, architecture, interfaces, data structures, quality attributes, security expectations, and acceptance criteria for SPORTIVA CM.

The specification is based on the current Django implementation and the project documentation. Requirements marked **Implemented** describe behavior already represented in the codebase. Requirements marked **Planned** or **Production hardening** identify capabilities that should be completed before a public production deployment.

## 2. Product Overview

SPORTIVA CM is a web-based sports promotion and community platform. It brings athletes, clubs, academies, coaches, sponsors, event organizers, marketplace sellers, and fans into one digital environment.

The platform is intended to:

- promote sports events and tournaments;
- improve the visibility of athletes and sports organizations;
- provide profiles and achievement records for athletes;
- support social sports content and community interaction;
- connect sponsors with athletes, organizations, and campaigns;
- provide sports equipment listings and seller contact;
- support direct communication between platform users;
- provide a responsive, installable, and partially offline web experience.

## 3. Scope

### 3.1 In scope

- User registration, authentication, profiles, roles, and permissions.
- Athlete exploits, endorsements, merit scoring, and profile discovery.
- Organization and club profiles.
- Sports events, registrations, capacity handling, simulated payment status, and invoices.
- Social media posts, comments, likes, shorts, and feed filtering.
- Sports equipment marketplace listings.
- Sponsorship profiles, campaigns, pledges, proposals, and contracts.
- One-to-one direct messaging with optional file attachments.
- Sports news presentation and a JSON sports-news endpoint.
- Responsive web interface, PWA manifest, service worker, and offline fallback.
- English, French, Spanish, German, Arabic, and Portuguese language configuration.
- Django administration and local seed data.

### 3.2 Out of scope for the current MVP

- Real payment processing or financial settlement.
- Marketplace cart, checkout, delivery, or order management.
- Native Android or iOS applications.
- Guaranteed offline creation and synchronization of new records.
- Production-grade external sports-news ingestion.
- Formal electronic signatures with legal identity verification.
- Advanced analytics, automated moderation, and abuse-reporting workflows.

## 4. Stakeholders and User Roles

| Stakeholder / role | Primary needs |
|---|---|
| Athlete | Build a public sports profile, record achievements, publish content, join events, and obtain sponsorship. |
| Coach / trainer | Discover athletes, validate achievements, and communicate with the community. |
| Organization / club / academy | Promote the organization, publish events, manage sports activity, and discover talent. |
| Sponsor / business partner | Present a sponsor profile, create or support campaigns, and establish partnerships. |
| Event organizer | Create events, manage registrations, and validate or cancel attendance records. |
| Fan / supporter / visitor | Browse sports content, events, organizations, athletes, products, and campaigns. |
| Marketplace seller | Publish sports products and receive buyer enquiries through WhatsApp. |
| Manager | Support athlete or organization administration; currently represented through organization-level access patterns. |
| Administrator / staff | Manage users, content, verification states, permissions, and platform data. |

The implemented user model includes athlete, coach, organization, sponsor, manager, and fan-oriented role values. Organization, club, academy, and manager behavior may share the same organization-level access path and should be refined if separate permissions are required.

## 5. Assumptions and Constraints

- The current development database is SQLite.
- The application is deployed locally using Django's development server.
- Uploaded media is stored in the local `media/` directory.
- The application uses UTC as its server time zone.
- A network connection is required for uncached pages, external resources, and normal server operations.
- Payment, messaging, and news capabilities are implemented as application features rather than integrated external service products.
- A production deployment must replace development defaults with environment-specific configuration.

## 6. Functional Requirements

### 6.1 Core and home dashboard

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-CORE-01 | The system shall provide a home dashboard for public and authenticated users. | Must | Implemented |
| FR-CORE-02 | The dashboard shall present platform statistics including athletes, organizations, events, and sponsors where data is available. | Must | Implemented |
| FR-CORE-03 | The dashboard shall display posts, shorts, upcoming events, athlete rankings, and sponsor information. | Must | Implemented |
| FR-CORE-04 | The system shall provide a sports-news JSON endpoint for dashboard consumption. | Should | Implemented |
| FR-CORE-05 | The system shall provide an offline fallback page. | Must | Implemented |
| FR-CORE-06 | The system should personalize feed ordering using the authenticated user's favorite sports. | Should | Implemented |

### 6.2 Accounts, authentication, and profiles

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-ACC-01 | A visitor shall be able to create an account with username, email, password, role, name, location, and sports information. | Must | Implemented |
| FR-ACC-02 | The system shall authenticate users using Django session authentication. | Must | Implemented |
| FR-ACC-03 | A user shall be able to view and edit their profile, biography, avatar, country, city, sports, and social contact information. | Must | Implemented |
| FR-ACC-04 | The system shall support profile search, filtering, sorting, and public profile viewing. | Must | Implemented |
| FR-ACC-05 | A user shall be able to follow and unfollow another user. Duplicate follow relationships shall be prevented. | Should | Implemented |
| FR-ACC-06 | An athlete shall be able to create and edit exploit records with achievement details and optional proof media or links. | Must | Implemented |
| FR-ACC-07 | Authorized users shall be able to verify or reject athlete exploits. | Must | Implemented |
| FR-ACC-08 | A user shall be able to endorse an athlete for a skill or capability. | Should | Implemented |
| FR-ACC-09 | The system shall calculate and display an athlete Sportiva Score and tier using achievements and community signals. | Should | Implemented |
| FR-ACC-10 | Staff and administrators shall be able to manage user access and custom tab permissions. | Must | Implemented |

### 6.3 Organizations and clubs

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-ORG-01 | An authorized user shall be able to create or manage an organization profile. | Must | Implemented |
| FR-ORG-02 | An organization profile shall support name, type, sport, description, address, country, city, contact details, website, logo, and verification state. | Must | Implemented |
| FR-ORG-03 | Visitors shall be able to browse and filter organizations by text, country, city, and sport. | Must | Implemented |
| FR-ORG-04 | An organization page shall show relevant published events. | Should | Implemented |
| FR-ORG-05 | Staff shall be able to administer organization records and verification information. | Should | Implemented |

### 6.4 Events and registrations

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-EVT-01 | An authorized organizer shall be able to create an event with title, sport, category, organizer, location, dates, capacity, fee, currency, banner, and contact information. | Must | Implemented |
| FR-EVT-02 | Visitors shall be able to browse and filter events by search text, country, city, sport, and category. | Must | Implemented |
| FR-EVT-03 | An authenticated user shall be able to register for an event. | Must | Implemented |
| FR-EVT-04 | The system shall prevent duplicate registration by the same user for the same event. | Must | Implemented |
| FR-EVT-05 | The system shall reject new registrations when event capacity has been reached. | Must | Implemented |
| FR-EVT-06 | The system shall record registration payment method and payment status. | Should | Implemented; payment is simulated |
| FR-EVT-07 | The system shall provide a downloadable invoice or entry-pass PDF for an eligible registration. | Should | Implemented |
| FR-EVT-08 | The organizer or authorized staff shall be able to validate or cancel a registration. | Must | Implemented |
| FR-EVT-09 | The system should support event contact through normalized WhatsApp links. | Should | Implemented |
| FR-EVT-10 | The platform shall integrate a real payment provider before accepting production payments. | Must for production | Planned |

### 6.5 Media feed and community interaction

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-MEDIA-01 | An authenticated user shall be able to publish text, image, video, short/reel, or article content. | Must | Implemented |
| FR-MEDIA-02 | A post shall support optional sport, location, hashtags, and media metadata. | Should | Implemented |
| FR-MEDIA-03 | Users shall be able to browse For You, Following, Shorts, and Trending feed views where available. | Must | Implemented |
| FR-MEDIA-04 | Users shall be able to filter media content by sport and hashtag. | Should | Implemented |
| FR-MEDIA-05 | An authenticated user shall be able to like or unlike a post. Duplicate likes shall be prevented. | Must | Implemented |
| FR-MEDIA-06 | Users shall be able to comment on posts. | Must | Implemented |
| FR-MEDIA-07 | The system should record post view counts. | Could | Partially implemented |
| FR-MEDIA-08 | Staff should be able to moderate inappropriate or reported content. | Should | Planned |

### 6.6 Marketplace

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-MKT-01 | An authenticated seller shall be able to publish a sports product listing. | Must | Implemented |
| FR-MKT-02 | A product listing shall support seller, category, title, description, price, currency, condition, location, image, availability, and contact information. | Must | Implemented |
| FR-MKT-03 | Visitors shall be able to browse and filter product listings. | Must | Implemented |
| FR-MKT-04 | A buyer shall be able to contact a seller through a generated WhatsApp link. | Should | Implemented |
| FR-MKT-05 | The system should support cart, checkout, orders, delivery, and payment in a future release. | Could | Planned |

### 6.7 Sponsorships and partnerships

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-SPN-01 | A sponsor shall be able to create and maintain a sponsor company profile. | Must | Implemented |
| FR-SPN-02 | An authorized creator shall be able to create a sponsorship campaign with target amount, deadline, location, banner, and contact details. | Must | Implemented |
| FR-SPN-03 | Users shall be able to browse sponsors, campaigns, and active contracts. | Must | Implemented |
| FR-SPN-04 | An authenticated user shall be able to make a campaign pledge with amount, message, and anonymous option. | Must | Implemented; record only |
| FR-SPN-05 | The system shall display campaign funding progress. | Must | Implemented |
| FR-SPN-06 | Users shall be able to send sponsorship proposals to relevant athletes, organizations, sponsors, or events. | Must | Implemented |
| FR-SPN-07 | A proposal recipient shall be able to accept or decline a proposal. | Must | Implemented |
| FR-SPN-08 | Accepting a proposal shall create an active sponsorship contract. | Must | Implemented |
| FR-SPN-09 | Sponsorship participants shall be able to use direct chat and WhatsApp contact. | Should | Implemented |
| FR-SPN-10 | The platform shall integrate payment processing and financial reconciliation before real sponsorship funds are accepted. | Must for production | Planned |
| FR-SPN-11 | The system should support formal electronic signatures and contract audit history. | Could | Planned |

### 6.8 Direct messaging

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-CHAT-01 | An authenticated user shall be able to start a one-to-one conversation with another user. | Must | Implemented |
| FR-CHAT-02 | A conversation shall contain participants and timestamped messages. | Must | Implemented |
| FR-CHAT-03 | A message shall support text and optional file attachment. | Should | Implemented |
| FR-CHAT-04 | Users shall only be able to view conversations in which they participate. | Must | Implemented |
| FR-CHAT-05 | The system shall display unread message counts and allow incoming messages to be marked as read. | Should | Implemented |
| FR-CHAT-06 | The system should provide real-time delivery and notifications in a future release. | Could | Planned |

### 6.9 Internationalization and offline web application

| ID | Requirement | Priority | Status |
|---|---|---:|---|
| FR-PWA-01 | The application shall provide a web app manifest for installable PWA behavior. | Should | Implemented |
| FR-PWA-02 | A service worker shall cache selected static assets and previously visited GET pages. | Should | Implemented |
| FR-PWA-03 | The application shall show an offline fallback when a requested page is unavailable. | Must | Implemented |
| FR-PWA-04 | The interface shall support configured English, French, Spanish, German, Arabic, and Portuguese languages. | Should | Configured; translation completeness varies |
| FR-PWA-05 | Offline mode should synchronize newly created records after reconnection. | Could | Planned |

## 7. Business Rules

1. Usernames and email addresses shall follow the uniqueness rules enforced by the custom user model.
2. Only authenticated users may perform protected creation, editing, registration, messaging, or sponsorship actions.
3. Staff and superusers receive administrative access; other roles receive only their permitted tabs and actions.
4. An athlete exploit must be reviewed by an authorized verifier before it contributes to verified achievement scoring.
5. A user cannot register for the same event more than once.
6. An event cannot accept registrations beyond its configured capacity.
7. A post cannot receive more than one like from the same user.
8. A follow relationship between two users cannot be duplicated.
9. Chat participants may access only their own conversations.
10. A sponsorship proposal may create a contract only after acceptance by the relevant recipient.
11. Pledges and sponsorship amounts are records in the database; they do not represent completed financial transactions in the MVP.
12. WhatsApp contact URLs shall use normalized phone numbers where a valid number is available.

## 8. Data Requirements

### 8.1 Principal entities

- **User:** authentication identity, role, location, sports, profile, verification, and permissions.
- **Follow:** directed user-to-user relationship.
- **AthleteExploit:** athlete achievement, points, proof, and verification state.
- **AthleteEndorsement:** skill endorsement from one user to an athlete.
- **SportsCategory:** shared sport classification.
- **OrganizationProfile:** club, academy, training center, or organization information.
- **EventCategory:** event classification.
- **Event:** tournament or sports activity managed by an organizer.
- **EventRegistration:** user attendance request, payment status, and validation state.
- **Post:** text or media publication by a user.
- **Comment:** response attached to a post.
- **Like:** unique user-post reaction.
- **ProductCategory:** marketplace classification.
- **Product:** sports equipment or merchandise listing.
- **SponsorProfile:** sponsor or business identity.
- **Campaign:** sponsorship fundraising target.
- **Pledge:** user contribution record associated with a campaign.
- **SponsorshipRequest:** partnership proposal and response state.
- **SponsorshipContract:** accepted sponsorship relationship.
- **Conversation:** private participant group for messaging.
- **ChatMessage:** message, sender, attachment, and read state.

### 8.2 Data integrity

- Foreign-key relationships shall preserve ownership and association between records.
- Unique constraints shall prevent duplicate follows, likes, and event registrations.
- Deletion behavior shall be explicitly defined for dependent records before production deployment.
- User-uploaded content shall be validated for file type, size, and storage safety before production deployment.
- Monetary values shall use explicit decimal precision and currency codes for production financial workflows.

## 9. External and User Interfaces

### 9.1 Main web routes

| Area | Representative routes |
|---|---|
| Home | `/` |
| Authentication | `/accounts/register/`, `/accounts/login/`, `/accounts/logout/` |
| Profiles | `/accounts/profile/`, `/accounts/profile/<username>/`, `/profiles/` |
| Organizations | `/organizations/` |
| Events | `/events/`, `/events/create/`, `/events/<id>/`, registration and invoice routes |
| Media | `/media-feed/`, `/media-feed/create/`, `/media-feed/<id>/` |
| Marketplace | `/marketplace/`, `/marketplace/sell/`, `/marketplace/<id>/` |
| Sponsorships | `/sponsorships/` and campaign, sponsor, proposal, and contract routes |
| Chat | `/chat/`, `/chat/<conversation_id>/` |
| API | `/api/sports-news/` |
| Administration | `/admin/` |
| Internationalization | `/i18n/` |
| Offline/PWA | `/offline/`, `/sw.js`, `/manifest.json` |

### 9.2 Interface requirements

- The interface shall be responsive on desktop, tablet, and mobile viewports.
- Navigation shall expose only the tabs permitted for the authenticated user's role.
- Forms shall display validation feedback and preserve user-entered values when validation fails.
- Protected actions shall provide clear success or failure messages.
- Images and media shall have appropriate labels or alternative text where practical.
- Event, campaign, product, and profile pages shall expose relevant contact actions without revealing unnecessary private data.

## 10. Non-Functional Requirements

### 10.1 Performance

- Common list and detail pages should render within an acceptable local development response time under seeded data.
- Database queries should use filtering and pagination patterns appropriate to the expected dataset.
- Static assets should be cached by the service worker where safe.
- Uploaded media should not be loaded at unnecessarily large dimensions in list views.

### 10.2 Availability and resilience

- The application shall provide a useful offline fallback for cached navigation.
- The service worker shall fail gracefully when network resources are unavailable.
- Database migrations shall be repeatable and version controlled.
- Backups shall be defined before production deployment.

### 10.3 Security

- Django CSRF protection, session authentication, password validators, and clickjacking protection shall remain enabled.
- Authorization checks shall be applied server-side to every protected mutation and private resource.
- Production configuration shall use a secret key supplied through environment variables.
- Production shall disable debug mode, restrict allowed hosts, enforce HTTPS, and use secure cookies.
- File uploads shall be restricted by size, type, content inspection, and storage permissions.
- Sensitive personal and financial information shall not be exposed in public list pages or URLs.
- Rate limiting, email verification, password reset, audit logging, and abuse controls should be added before public launch.

### 10.4 Maintainability

- Feature code shall remain separated into Django apps: `accounts`, `organizations`, `events`, `media_feed`, `marketplace`, `sponsorships`, `chat`, and `core`.
- Schema changes shall be delivered through Django migrations.
- Dependencies shall be recorded in a locked or repeatable dependency file before production deployment.
- Automated tests shall cover authentication, authorization, model constraints, critical forms, and high-value workflows.

### 10.5 Accessibility and usability

- The application should support keyboard navigation and visible focus states.
- Form labels, error messages, button names, and image alternatives should be understandable without color alone.
- Layouts shall remain usable on small screens and with long translated strings.
- Language selection should be available from the shared navigation.

## 11. Technical Architecture

### 11.1 Technology stack

- Python and Django.
- SQLite for development.
- Django templates, forms, and server-side views.
- HTML, CSS, JavaScript, Tailwind CSS, local fonts, and vendor assets.
- Django REST Framework and django-filter for API and filtering support.
- Pillow for image handling.
- Crispy Forms with the Tailwind template pack.
- Service worker and web manifest for PWA behavior.

### 11.2 Application structure

- `core`: home dashboard, shared logic, sports-news endpoint, and offline view.
- `accounts`: custom user model, authentication, profiles, follows, exploits, endorsements, and permissions.
- `organizations`: organization profiles and discovery.
- `events`: events, registrations, invoice generation, and event management.
- `media_feed`: posts, comments, likes, shorts, and feed views.
- `marketplace`: sports products and seller contact.
- `sponsorships`: sponsors, campaigns, pledges, proposals, and contracts.
- `chat`: conversations and private messages.
- `sportiva_cm`: project settings, root URLs, WSGI, and ASGI configuration.

### 11.3 Deployment configuration

Development setup:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install django pillow django-crispy-forms crispy-tailwind djangorestframework django-filter
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

The local application is available at `http://127.0.0.1:8000/` after the development server starts.

Production deployment shall additionally define a supported database, web server, static-file pipeline, media storage strategy, HTTPS configuration, secret management, monitoring, backup process, and dependency lock file.

## 12. Verification and Acceptance Criteria

The MVP shall be considered functionally acceptable when the following scenarios succeed:

1. A new visitor can register, log in, view a profile, and update profile information.
2. An athlete can submit an exploit and an authorized verifier can approve or reject it.
3. A user can follow another user, endorse an athlete, and see the resulting profile signals.
4. An organization can be discovered through the organization list and associated event information.
5. An organizer can create an event and an authenticated user can register once.
6. Duplicate event registration is rejected and capacity limits are respected.
7. An eligible user can access the generated registration invoice or entry pass.
8. An authenticated user can publish a post, like it, comment on it, and filter feed content.
9. A seller can publish a product and a visitor can reach the seller through WhatsApp contact.
10. A campaign creator can publish a campaign, a user can create a pledge record, and progress is displayed.
11. A sponsorship proposal can be accepted or declined and an accepted proposal produces a contract record.
12. Two users can exchange private messages, including an optional attachment, without exposing the conversation to other users.
13. A user can load previously visited pages when offline and receive the offline fallback for unavailable pages.
14. Staff can access the administration interface and manage relevant records.
15. The automated test suite runs successfully in an environment with all declared dependencies installed.

## 13. Testing Strategy

Testing shall be performed at the following levels:

- **Model tests:** constraints, score calculations, relationships, and state transitions.
- **Form tests:** required fields, validation, file handling, and invalid input behavior.
- **View tests:** authentication, authorization, redirects, filtering, and response content.
- **Workflow tests:** registration, event attendance, sponsorship proposals, contracts, chat privacy, and feed interactions.
- **PWA tests:** manifest availability, service-worker registration, cache behavior, and offline fallback.
- **Security tests:** unauthorized access, object ownership, upload validation, CSRF, and sensitive data exposure.
- **Usability tests:** responsive layouts, language switching, error feedback, and mobile navigation.

Recommended commands:

```powershell
python manage.py check
python manage.py test
```

## 14. Risks and Future Improvements

### 14.1 Current implementation risks

- Development defaults currently allow debug mode and unrestricted hosts unless environment variables override them.
- A fallback development secret key exists and must not be used in production.
- SQLite and local media storage are not suitable for a multi-instance production deployment.
- Payment and pledge values are not connected to a payment provider.
- Offline support is primarily cached-read support; reliable offline writes are not guaranteed.
- The user guide describes some capabilities more broadly than the current implementation proves, especially live external news, full offline writes, and certain social-media features.
- Demo account details must be verified against the current seed command before distribution.

### 14.2 Recommended next releases

1. Add a dependency lock file and environment-specific settings.
2. Harden production security configuration.
3. Add real payment integration with transaction reconciliation.
4. Add notification, email verification, password reset, and moderation workflows.
5. Improve search, pagination, analytics, and administration reporting.
6. Add reliable media processing and secure object storage.
7. Separate organization and manager permissions if business rules require it.
8. Add API endpoints for future mobile clients.
9. Expand automated test coverage and continuous integration.
10. Complete translation catalogs and verify right-to-left layout behavior.

## 15. Traceability Summary

| Capability | Primary Django app(s) | Verification evidence |
|---|---|---|
| Authentication and roles | `accounts` | Registration, login, profile, and permission tests |
| Athlete merit | `accounts` | Exploit, verification, endorsement, and score tests |
| Organizations | `organizations` | Organization form, list, and detail tests |
| Events | `events` | Event, registration, capacity, and invoice tests |
| Social feed | `media_feed`, `core` | Post, like, comment, and feed tests |
| Marketplace | `marketplace` | Product form, listing, and contact tests |
| Sponsorships | `sponsorships` | Campaign, pledge, proposal, and contract tests |
| Messaging | `chat` | Conversation privacy, message, attachment, and unread-state tests |
| PWA/offline | `core`, `static`, `templates` | Manifest, service-worker, cache, and offline browser checks |
| Administration | Django admin and all feature apps | Staff authorization and admin smoke tests |

## 16. Approval and Change Control

Changes to this specification should record:

- the requirement ID affected;
- the reason for the change;
- the implementation or migration impact;
- the test evidence required;
- the approver or project owner;
- the new document version and date.

This document should be updated when a functional requirement changes, a new app or external integration is introduced, a security boundary changes, or a production deployment decision changes.
