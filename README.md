# Text-to-Image Backend (Django)

This is the backend for a **Text-to-Image generator** built with **Django REST Framework**.  
It allows authenticated users to generate images from text prompts using the **ChatGPT RapidAPI** and manage their generated images.

> ⚠️ Currently, this project is primarily a **portfolio project**, but it is structured for future expansion into a SaaS product.

## Features

- User authentication (login/signup/logout)
- Generate images from text prompts via RapidAPI
- Store image metadata and prompt per user
- Retrieve, list, and delete generated images
- Download images with correct file types (PNG/JPG)
- JWT-based authentication for API security

## Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (JSON Web Tokens)
- **API:** RapidAPI (ChatGPT text-to-image)
- **Deployment:** Designed for Render (or any cloud provider)

---

## Getting Started

### 1. Clone the repository

git clone https://github.com/yourusername/text-to-image-backend.git
cd text-to-image-backend

## Getting Started

### 1. Clone the repository

git clone https://github.com/yourusername/text-to-image-backend.git
cd text-to-image-backend

## Setup Virtual Environment

python -m venv .venv
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows

## Install Dependencies

pip install -r requirements.txt

Environment Variables

# Django settings

SECRET_KEY=your_django_secret_key
DEBUG=True

# RapidAPI

RAPIDAPI_KEY=your_rapidapi_key_here

# Database URL (PostgreSQL)

DATABASE_URL=postgres://db_user:db_password@db_host:db_port/db_name

# JWT settings

JWT_SECRET_KEY=your_jwt_secret_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME=3600 # 1 hour

Apply Migrations
python manage.py makemigrations
python manage.py migrate

Run the Development Server
python manage.py runserver

The API will be accessible at http://127.0.0.1:8000/.

API Endpoints
Endpoint Method Description
/api/auth/login/ POST Authenticate a user
/api/auth/register/ POST Register a new user
/api/images/ GET List all generated images for user
/api/images/ POST Generate a new image from prompt
/api/images/<id>/ GET Retrieve single image
details/api/images/<id>/ DELETE Delete an image
/api/images/download/<id>/GET Download the image file

Future Improvements
Turn the project into a SaaS product with subscription tiers
Add billing and payments integration
Include image history dashboard for users
Implement rate limiting to prevent API abuse
Add multi-resolution image generation
Frontend SPA (React/Next.js) to consume the API

Deployment Notes
.env should be configured in the hosting platform (e.g., Render)

DEBUG must be set to False in production
ALLOWED_HOSTS should include the deployed domain

Start command on Render:
gunicorn myproject.wsgi:application

License
This project is for portfolio purposes. You can reuse or extend it under your own terms.

Built with ❤️ by Ohazulike Stanley
