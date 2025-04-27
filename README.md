# Health Information Management System - Backend
This is the Flask-based backend for the CEMA Internship Project Health Information Management System. It provides a RESTful API for managing doctors, clients, health programs, enrollments, and authentication via API keys.

## Tech Stack
###    Language & Framework:
 Python, Flask

###    ORM: 
SQLAlchemy

###    Database Migrations: 
Alembic (Flask-Migrate)

###    Database: 
PostgreSQL

## Authentication & Security:

    APIKey model + api_key_required and super_admin_required decorators

    CORS: Flask-CORS

## Environment Management: 
Pipenv, python-dotenv

## Project Structure
    server/
    ├─ Pipfile, Pipfile.lock         # Python environment definitions
    ├─ .env                          # (ignored) actual environment vars
    ├─ .env.example                  # template for env vars
    ├─ run.py                        # application entrypoint
    ├─ seed.py                       # script to seed initial admin Doctor & APIKey
    ├─ app/                          # application package
    │   ├─ __init__.py               # factory, config loading, extension init, blueprint registration
    │   ├─ config.py                 # Config classes: DevelopmentConfig, TestingConfig, ProductionConfig
    │   ├─ models.py                 # SQLAlchemy models: Doctor, Client, HealthProgram, Enrollment, APIKey
    │   ├─ utils/                    # helper decorators (API key and admin checks)
    │   │   └─ auth.py
    │   └─ routes/                   # modular blueprints for each resource
    │       ├─ __init__.py           # imports and registers blueprints
    │       ├─ auth.py               # `/validate` endpoint for API key checking
    │       ├─ admin.py              # admin-only endpoints
    │       ├─ clients.py            # client CRUD endpoints
    │       ├─ programs.py           # health program CRUD endpoints
    │       └─ enrollments.py        # enrollment endpoints
    └─ migrations/                   # Alembic migration scripts
        ├─ versions/                 # revision files for schema changes

# Setup & Run
## 1. Clone & Install
git clone <backend-repo-url>
cd server
pipenv install
pipenv shell


## 2.Configure .env
DATABASE_URL=postgresql://USER:PASS@localhost/health_db
MAIL_USERNAME=youremail@example.com
MAIL_PASSWORD=yourgmailappassword

## 3.Database Preparation
-Create Postgres role & database (once):
-sudo -u postgres psql
-CREATE USER <yourusername> WITH PASSWORD '<PASSWORD>';
-CREATE DATABASE health_db OWNER <yourusername>;
-ALTER ROLE <yourusername> CREATEDB;
\q
## 4.Configure environment:

cp .env.example .env
### edit .env with actual password and any other secrets

## 5.Seed super-admin
python seed.py       # creates Dr. Admin + API key
## 6. Migrations
export FLASK_APP=run.py
flask db init         # if initializing first time
flask db migrate -m "initial schema"
flask db upgrade
### subsequent changes:
flask db migrate -m "describe change"
flask db upgrade

## 7.Run the Server

python3 run.py
Default: http://localhost:5000

# API Endpoints

| Blueprint    | Endpoint                                   | Method | Description                                    | Auth        |
|--------------|--------------------------------------------|--------|------------------------------------------------|-------------|
| `auth_bp`    | `/api/auth/validate`                       | GET    | Returns doctor info: { id, name, is_admin }    | API Key    |
| `clients_bp` | `/api/clients/register`                    | POST   | Register a new client                          | API Key    |
|              | `/api/clients/`                            | GET    | List all clients                               | API Key    |
|              | `/api/clients/search?q=`                   | GET    | Search clients                                 | API Key    |
|              | `/api/clients/<id>`                        | GET    | Fetch client profile + enrollments             | API Key    |
| `programs_bp`| `/api/programs/`                           | POST   | Create a health program                        | API Key    |
|              | `/api/programs/`                           | GET    | List all health programs                       | API Key    |
|              | `/api/programs/list`                       | GET    | List programs for dropdown                     | API Key    |
| `enroll_bp`  | `/api/enrollments/<client_id>`             | POST   | Enroll client in programs via { program_ids: [] } | API Key  |
| `admin_bp`   | `/api/admin/doctors`                       | POST   | Create a new doctor + email key                | Super Admin|
|              | `/api/admin/doctor`                        | POST   | Update an existing doctor                      | Super Admin|

---

# Authentication

-API Key**: Each Doctor has one or more APIKey records. Include `API-KEY` header in requests.


##     Decorators:

    - @api_key_required: Validates the API key, injects request.doctor.

    - @super_admin_required: Ensures doctor.is_admin == True.

# Migrations & Commit History
    Initial schema → doctors, clients, health_programs, enrollments tables

    Password column dropped → refactor: remove password column from Doctor model

    APIKey model added → feat: introduce APIKey model and api_keys table

    is_admin added → feat: add is_admin field to Doctor model

# Contributing
    Fork & create a feature branch

    Write tests and implement changes

    Commit with feat:, fix:, or chore: prefixes

    Open a PR against main

