# Sportiva CM

Sportiva CM is a Django-based sports promotion and community platform designed for Cameroon. It connects athletes, clubs, trainers, sponsors, and sports fans in one digital ecosystem for events, organizations, media updates, marketplace activity, and sponsorship campaigns.

## Project Purpose

The platform aims to:
- promote sports events and tournaments across Cameroon;
- help clubs, training centers, and academies gain visibility;
- connect fans and athletes with local sports communities;
- support buying and selling of sports gear;
- help organizations raise funding through sponsorship campaigns.

## Main Features

- User registration and login with role-based profiles
- Sports organizations and club directory
- Event creation and RSVP registration
- Media feed for news, highlights, and updates
- Community marketplace for sports equipment
- Sponsorship campaigns with pledge support
- WhatsApp contact integration
- Mobile-friendly responsive UI
- Localized Cameroon-focused data and categories

## App Structure

- accounts: authentication, profile, user roles
- organizations: club profiles and sports directory
- events: event management and attendance
- media_feed: posts, likes, comments
- marketplace: selling and buying sports products
- sponsorships: funding campaigns and pledges
- core: home page and shared logic

## Tech Stack

- Python
- Django
- SQLite (development)
- HTML / CSS / JavaScript
- Tailwind CSS
- Django Forms
- Pillow for image handling

## Local Setup

1. Open the project folder.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install django pillow django-crispy-forms crispy-tailwind djangorestframework django-filter
```

5. Apply migrations:

```bash
python manage.py migrate
```

6. Seed sample data:

```bash
python manage.py seed_data
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Open the browser at:

```text
http://127.0.0.1:8000/
```

## Default Admin Account

The seed command creates an administrative account with:

- username: camer_admin
- password: Admin237!

## Testing

Run the project tests with:

```bash
python manage.py test
```

## Project Status

This project is currently in an MVP stage and is suitable for demonstration, defense presentation, and further feature expansion.

## Future Improvements

- stronger production security settings
- environment variables for sensitive config
- better API layer for mobile frontend integration
- more advanced search and filter features
- stronger unit test coverage
- multilingual support (English and French)
- deployment to a real cloud platform

---

This project was developed as a sports promotion application for Cameroon, with the goal of creating a digital platform that supports local sports development, visibility, and community engagement.
