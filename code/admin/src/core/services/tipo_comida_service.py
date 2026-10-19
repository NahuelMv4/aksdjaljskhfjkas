from src.core.database import db
from src.core.models.tipo_comida import TipoComida

def create_tipo_comida(**kwargs):
  tipo_comida = TipoComida(**kwargs)
  db.session.add(tipo_comida)
  db.session.commit()
  return tipo_comida