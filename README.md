# Library Management REST API

Django + Django REST Framework + MySQL based API to manage books, members, issue/return and fines.

## Tech Stack
Python, Django, DRF, MySQL, JWT (SimpleJWT), Swagger (drf-spectacular)

## Features
- JWT authentication
- Search and filter books, pagination
- Issue/return using transaction.atomic
- Automatic fine (Rs 5 per late day)
- Raw SQL reports: overdue books, popular books, top members
- Swagger docs at /api/docs/

## Setup
1. `python -m venv venv` and activate it
2. `pip install -r requirements.txt`
3. Create MySQL database: `CREATE DATABASE library;`
4. Create a `.env` file with DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
7. `python manage.py runserver`

## Endpoints
- POST /api/token/
- GET/POST /api/books/, /api/members/, /api/issues/
- POST /api/issues/{id}/return/
- GET /api/reports/overdue/, /popular-books/, /top-members/