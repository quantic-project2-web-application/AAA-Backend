import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")  # Flask CLI also auto-loads .env/.flaskenv when python-dotenv installed

class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    # Choose the URL matching your installed driver:
    # psycopg2:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URI",
        "postgresql+psycopg2://cafe_admin:root1234@localhost:5432/cafefausse_db"
    )

    # or psycopg (psycopg3):
    # "postgresql+psycopg://restaurant:restaurant@localhost:5432/restaurant_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROPAGATE_EXCEPTIONS = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True

class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI", "sqlite:///:memory:")

class ProductionConfig(BaseConfig):
    DEBUG = False
