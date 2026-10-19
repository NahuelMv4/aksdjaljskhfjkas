from flask_sqlalchemy_lite import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

db = SQLAlchemy()

def init_app(app):
  db.init_app(app)

def reset_db():
  import src.core.models

  print("Reseteando base de datos")
  Base.metadata.drop_all(bind=db.engine)
  Base.metadata.create_all(bind=db.engine)
  print("Listo!")

class Base(DeclarativeBase):
  pass