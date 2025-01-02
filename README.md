# Project-management - Django Project API

## Overview
A Django-based API project that provides functionality for managing users, projects, tasks, and comments, along with JWT-based authentication.

---

## Features
- User registration and authentication.
- CRUD operations for projects, tasks, and comments.
- Token-based authentication with refresh support.
- Well designed database schema for project management application .

---

## Installation

### Prerequisites
- Python 3.9+
- pip
- SQLite (default)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

2. Create a virtual environment and activate it:
   ```bash  
   python -m venv venv
   source venv/bin/activate  
   # On Windows: venv\Scripts\activate
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
4. Run migrations:
   ```bash
   python manage.py migrate
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
6. Start the development server
   ```bash
   python manage.py runserver

## Endpoints
- POST api/users/register/ - Register a new user.
- POST api/users/login/ - Login and retrieve tokens.
- GET api/projects/ - List all projects.

## For detailed API documentation, see API Documentation.


## Deployment
To deploy, consider using tools like Docker, Gunicorn, or AWS. Refer to the Django deployment documentation for best practices.


