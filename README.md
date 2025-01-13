# Company Management System

A Company Management System built with Django that encompasses various features for managing companies, departments, employees, and projects.

## Features

- User authentication and authorization
- Company, Department, Employee, and Project management
- Performance reviews with state transitions
- RESTful API endpoints

## Installation

1. Clone the repository:
    sh
    git clone <repository-url>
    cd <repository-directory>
    

2. Create and activate a virtual environment:
    sh
    python -m venv env
    source env/bin/activate  # On Windows use `env\Scripts\activate`
    

3. Install the dependencies:
    sh
    pip install -r requirements.txt
    

4. Apply the migrations:
    sh
    python manage.py migrate
    

5. Create a superuser:
    sh
    python manage.py createsuperuser
    

6. Run the development server:
    sh
    python manage.py runserver
    

## API Endpoints

The API endpoints are available under the /apis/ path. The following endpoints are provided:

- /apis/companies/ - List and retrieve companies
- /apis/departments/ - List and retrieve departments
- /apis/employees/ - List, create, retrieve, update, and delete employees
- /apis/projects/ - List, create, retrieve, update, and delete projects
- /apis/register/ - Register a new user
- /apis/login/ - Login a user
- /apis/performance-reviews/ - List, create, retrieve, update, and delete performance reviews

## Admin Panel

Access the admin panel at /admin/ to manage the models through the Django admin interface.