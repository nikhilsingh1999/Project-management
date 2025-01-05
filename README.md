# Project-management - Django backend project API

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
   
4. Don't forgot to add in setting the abstract user
   ```bash
   AUTH_USER_MODEL = 'management.User'
   
5. Run migrations:
   ```bash
   python manage.py migrate
   
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   
7. Start the development server
   ```bash
   python manage.py runserver
   
8. Add your app in installed app settings
   ```bash
   INSTALLED_APPS = [
    'management',
    'rest_framework',
    'rest_framework_simplejwt',]
   
## Endpoints
- POST api/users/register/ - Register a new user.
- POST api/users/login/ - Login and retrieve tokens.
- GET api/projects/ - List all projects.

## For detailed API documentation, see [API Documentation](https://www.postman.com/docking-module-operator-74906578/my-workspace/collection/sgf7ktt/project-management-application?action=share&creator=40727933)



## Deployment
To deploy, consider using tools like Docker, Gunicorn, or AWS. Refer to the Django deployment documentation for best practices.


