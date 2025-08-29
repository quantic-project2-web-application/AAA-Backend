### AAA-Backend
# Restaurant API (Flask + PostgresSQL)

## Run
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- cp .env.example .env   # set DATABASE_URI/SECRET_KEY
- flask db init && flask db migrate -m "initial" && flask db upgrade
- flask run --debug

## Tech
- Flask app-factory + Blueprints
- SQLAlchemy + Flask-SQLAlchemy
- PostgresQL 
- Flask-Migrate (Alembic)
- Marshmallow (validation)
- Flask-CORS (frontend integration)
