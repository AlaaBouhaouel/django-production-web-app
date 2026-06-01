# atast-web-platform

## Problem
Build a structured web application to manage content and user interactions with a stable backend and deployable production setup.

## Solution
Django-based web application implementing:
- server-rendered UI (HTML/CSS)
- backend logic for data handling
- authentication and user flow
- production deployment on Railway

## Architecture
- **Frontend:** Django templates (HTML, CSS)
- **Backend:** Django (views, models, routing)
- **Database:** SQLite (dev) / PostgreSQL-compatible (prod)
- **Deployment:** Railway + Gunicorn + WhiteNoise

## Core Features
- User authentication
- Dynamic page rendering
- Backend-driven content management
- Persistent data storage

## My Contribution
- Built full Django application (models, views, templates)
- Implemented authentication and routing
- Structured backend logic and database models
- Deployed application on Railway

## Results
- Fully functional Django web app
- Production deployment with static handling and server configuration
- End-to-end backend + frontend integration

## Tech Stack
Python · Django · HTML · CSS · Railway · Gunicorn · WhiteNoise

## Links
atast.org
sss.atast.org

## Setup
```bash
python -m venv .venv
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```


