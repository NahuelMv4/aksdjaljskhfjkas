from sqlalchemy import select
from src.core.database import db
from src.core.models.tipo_personal import TipoPersonal

def create_tipo_personal(**kwargs):
  tipo_personal = TipoPersonal(**kwargs)
  db.session.add(tipo_personal)
  db.session.commit()
  return tipo_personal

def list_tipo_personal():
  stmt = select(TipoPersonal)
  return db.session.execute(stmt).scalars().all()