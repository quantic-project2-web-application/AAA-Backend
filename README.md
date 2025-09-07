### AAA-Backend
# Restaurant API (Flask + PostgresSQL)

## Download and Install
- python (https://www.python.org/)
- postgresql (https://www.postgresql.org/download/)
## Run
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- cp .env-example .env   # set DATABASE_URI/SECRET_KEY
# Database setup
- CREATE ROLE cafe_admin WITH LOGIN PASSWORD 'root1234';
- CREATE DATABASE cafefausse_db OWNER <your-username>;
- GRANT ALL PRIVILEGES ON DATABASE cafefausse_db TO <your-username>;
# DB
- flask db init && flask db migrate -m "initial" && flask db upgrade
- flask run --debug

## Tech
- Flask app-factory + Blueprints
- SQLAlchemy + Flask-SQLAlchemy
- PostgresQL 
- Flask-Migrate (Alembic)
- Marshmallow (validation)
- Flask-CORS (frontend integration)

## Postman Collection

A Postman collection is included in the project root:

Cafe Fausse.postman_collection.json


Import it into Postman to test all API endpoints quickly.