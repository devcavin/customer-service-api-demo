# customer-service-api-demo
Repository showing a simple notes API using Django and FastAPI for a workshop I did teaching my folks the basics of API. This repository is designed to provide a boilerplate for building basic notes CRUD endpoints with ADD, READ, UPDATE, and DELETE functionalities.


# Backend Directory Structure

```
backend
├── api
│   ├── cli.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── README.md
│   ├── tests
│   │   └── v1
│   │       ├── __init__.py
│   │       ├── test_accounts.py
│   │       ├── test_business.py
│   │       └── test_core.py
│   ├── v1
│   │   ├── account
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   ├── business
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── core
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   └── routes.py
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── utils.py
│   └── VERSION
├── db.sqlite3
├── env.example
├── external
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── models.py
│   ├── static
│   │   └── external
│   │       ├── css
│   │       ├── img
│   │       │   └── logo.png
│   │       └── js
│   ├── tests.py
│   └── views.py
├── files
│   ├── exports
│   ├── media
│   │   └── default
│   │       ├── logo.png
│   │       └── user.png
│   └── static
├── Makefile
├── manage.py
│   └── wsgi.py
├── requirements.txt
├── templates
│   ├── api
│   │   └── v1
│   │       └── email
│   │           ├── message_received_confirmation.html
│   │           └── password_reset_token.html
│   ├── success.html
│   └── user_creation.html
├── users
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── wsgi.py

30 directories, 76 files

```

# Frontend Directory Structure

Typical frontend directory structure using React might look like:

```
frontend
├── index.html
├── css
│   ├── main.css
├── pages
│   │   ├── main.js
├── img
│   ├── logo.png
```


# Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/devcavin/customer-service-api-demo.git
    cd customer-service-api-demo
    ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```bash
    pip install -r requirements.txt
    ```
4. Set up the environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost,

5. Create a superuser account:
   ```bash
   python manage.py createsuperuser
   ```
6. Run the migrations:
   ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7. Start the development server:
   ```bash
   python manage.py runserver 
   python -m python -m fastapi run api 
   ```

Open your browser and navigate to `http://localhost:8000` for FastAPI.
Docsumentation for the API will be available at `http://localhost:8000/docs` and the admin interface at `http://localhost:8000/d/admin`.


# API Documentation
You can access the API documentation for FastAPI at `http://localhost:8001/docs`. This will provide you with an interactive interface to test the API endpoints.




Note: This repository is a boilerplate and does not include any frontend code. You can use any frontend framework of your choice, such as React, Vue.js, or Angular, and integrate it with the backend APIs provided in this repository. It was forked from [https://github.com/Simatwa/django-fastapi-boilerplate](https://github.com/Simatwa/django-fastapi-boilerplate) and modified to suit my needs. Thanks to the original author for creating this boilerplate.
