# Seekr

Early-career job & recruiting web app built with **Django** (backend + templates) and **Tailwind CSS**.

## Prerequisites

- Python 3.12+
- Node.js 18+ (optional, only needed to rebuild Tailwind CSS)

## Setup

```bash
# Clone and enter the project
git clone https://github.com/Prithul-the-creator/2340-Project-2.git
cd 2340-Project-2

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows

# Install Python dependencies
pip install -r requirements.txt
```

## Database migrations

```bash
# Create migrations after model changes (if needed)
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Optional: demo data

```bash
python manage.py seed_demo
```

Demo logins:

| Username   | Password      | Role      |
|------------|---------------|-----------|
| `seeker`   | `seeker123`   | Job seeker |
| `recruiter`| `recruiter123`| Recruiter |
| `admin`    | `admin123`    | Admin     |

## Optional: rebuild Tailwind CSS

CSS is already built into `static/css/tailwind.css`. To regenerate after style changes:

```bash
npm install
npm run build:css
# or watch while editing:
npm run watch:css
```

## Tests

```bash
python manage.py test accounts jobs
```

## Project layout

- `accounts/` — auth, profiles, privacy, admin user management
- `jobs/` — jobs, applications, candidates, saved searches, alerts
- `home/` — landing and about pages
- `static/` — Tailwind source and compiled CSS
- `design.md` — Seekr design system notes
