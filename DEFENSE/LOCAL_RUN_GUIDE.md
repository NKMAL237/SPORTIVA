# Local Run Guide for Sportiva CM

## Step 1: Open the project folder
Open the project directory in your terminal or VS Code terminal.

Example:
```bash
cd "C:\Users\NK-MAL\Documents\SPORTIVA CM"
```

## Step 2: Activate the virtual environment
Windows:
```bash
.venv\Scripts\activate
```

## Step 3: Install required packages
If the environment is not ready, install the dependencies:
```bash
pip install django pillow django-crispy-forms crispy-tailwind djangorestframework django-filter
```

## Step 4: Apply migrations
```bash
python manage.py migrate
```

## Step 5: Seed sample data
```bash
python manage.py seed_data
```

## Step 6: Run the app
```bash
python manage.py runserver
```

## Step 7: Open the website
Visit:
```text
http://127.0.0.1:8000/
```

## Step 8: Use the default admin account
The seed file creates:
- username: camer_admin
- password: Admin237!

## Step 9: Run tests
```bash
python manage.py test
```

## Troubleshooting
- If a module is missing, install it with pip.
- If there is a migration issue, run:
```bash
python manage.py makemigrations
python manage.py migrate
```
- If the app does not open, make sure your virtual environment is active.

## Quick Demo User Flow
1. Open the homepage.
2. Register a user account.
3. Create a club or organization.
4. Create an event.
5. Visit the media feed.
6. Browse the marketplace.
7. Launch or support a sponsorship campaign.

This is the quickest way to demonstrate the platform during your defense.
