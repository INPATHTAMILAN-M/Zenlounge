# ZenLounge - Django User Management API

## Project Overview
A Django REST framework implementation for user management with JWT authentication and Swagger documentation.

## Installation
1. Create virtual environment: `python3 -m venv venv`
2. Activate environment: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`

## API Documentation
Access Swagger UI at `http://localhost:8000/

## Features
- User registration
- JWT authentication
- Profile management
- Password reset
- Token refresh
