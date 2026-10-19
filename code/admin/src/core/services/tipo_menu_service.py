from sqlalchemy import select
from src.core.database import db
from src.core.models.tipo_menu import TipoMenu

def create_tipo_menu(**kwargs):
  tipo_menu = TipoMenu(**kwargs)
  db.session.add(tipo_menu)
  db.session.commit()
  return tipo_menu

def list_tipo_menu():
  stmt = select(TipoMenu)
  return db.session.execute(stmt).scalars().all()