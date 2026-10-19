from os import environ
from datetime import timedelta

class Config:
  TESTING = False
  FLASK_SECRET_KEY = "secret_key"
  FLASK_SESSION_TYPE = "filesystem"
  PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  
  SESSION_COOKIE_HTTPONLY = True                 
  SESSION_COOKIE_SAMESITE = "Lax"               
  SESSION_COOKIE_SECURE = False 

class ProductionConfig(Config):
  SQLALCHEMY_ENGINES = {
    "default": environ.get("DATABASE_URL")
  }

class DevelopmentConfig(Config):
  SECRET_KEY = "dev-secret_key"
  DB_USER = environ.get("DB_USER") or "postgres"
  DB_PASSWORD = environ.get("DB_PASSWORD") or "postgres"
  DB_HOST = environ.get("DB_HOST") or "localhost"
  DB_PORT = environ.get("DB_PORT") or "5432"
  DB_NAME = environ.get("DB_NAME") or "grupo32"
  DB_SCHEME = "postgresql+psycopg"
  SQLALCHEMY_ENGINES = {
    "default": f"{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
  }

class TestingConfig(Config):
  TESTING = True

config = {
  "development": DevelopmentConfig,
  "production": ProductionConfig,
  "testing": TestingConfig
}