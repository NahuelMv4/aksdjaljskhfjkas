from src.core.database import db
from src.core.models.configuracion_sistema import ConfiguracionSistema

def create_configuracion(**kwargs):
  configuracion = ConfiguracionSistema(**kwargs)
  db.session.add(configuracion)
  db.session.commit()
  return configuracion