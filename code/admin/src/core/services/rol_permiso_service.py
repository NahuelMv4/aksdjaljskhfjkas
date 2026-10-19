from src.core.database import db
from src.core.models.rol import Rol
from src.core.models.permiso import Permiso
from typing import List
from sqlalchemy import select

def create_rol(**kwargs):
  rol = Rol(**kwargs)
  db.session.add(rol)
  db.session.commit()
  return rol

def create_permiso(**kwargs):
  permiso = Permiso(**kwargs)
  db.session.add(permiso)
  db.session.commit()
  return permiso

def asignar_permisos_a_rol(rol: Rol, permisos: List[Permiso]):
  rol.permisos.extend(permisos)
  db.session.commit()
  return rol

def list_permisos():
  stmt = select(Permiso)
  return db.session.execute(stmt).scalars().all()

def list_roles():
  stmt = select(Rol)
  return db.session.execute(stmt).scalars().all()
