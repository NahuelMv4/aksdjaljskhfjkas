from src.core.database import db
from src.core.models.sector import Sector
from sqlalchemy import select, func 
from src.core.models.usuario import Usuario
from src.core.errores.custom_errors import ConflictError


POR_PAGINA = 25

def create_sector(**kwargs):
  sector = Sector(**kwargs)
  if existe_nombre_sector (sector.nombre): 
    raise ConflictError ("Ya existe un sector con ese nombre")
  db.session.add(sector)
  db.session.commit()
  return sector

def read_sector(sector_id):
  return db.session.get(Sector, sector_id)

def list_sectores():
  stmt = select(Sector)
  return db.session.execute(stmt).scalars().all()

def update_sector(sector_id, **kwargs):
  sector = read_sector(sector_id)
  if sector is None:
    return None 

  if "nombre" in kwargs and existe_nombre_sector(kwargs["nombre"], excluir_id=sector_id):
    raise ConflictError("Ya existe un sector con ese nombre")
  
  campos_permitidos = {"nombre", "descripcion", "activo"}
  for campo, valor in kwargs.items():
    if campo in campos_permitidos: 
      setattr(sector, campo, valor)
  try:
    db.session.commit()
  except Exception:
    db.session.rollback()
    raise
  
  return sector


def delete_sector (sector_id):
  return update_sector(sector_id, activo=False)


def existe_nombre_sector(sector_nombre, excluir_id=None):
  query = select(Sector)
  for sector in db.session.scalars(query).all():
    if sector.id == excluir_id:
      continue
    if sector.nombre.strip().lower() == sector_nombre.strip().lower():
      return True
  return False

def funcionalidad_busqueda (nombre=None, activo=None, usuario_id=None, orden= "nombre", descendente= False, pagina=1):
  query = select(Sector)
  if nombre: 
    query = query.where(Sector.nombre.ilike(f"%{nombre}%"))

  if activo is not None: 
    query = query.where(Sector.activo == activo)

  if usuario_id is not None: 
    query = query.join(Sector.usuarios).where(Usuario.id == usuario_id)

  total = db.session.scalar(select(func.count()).select_from(query.subquery()))

  if orden == "creado_en":
    columna = Sector.creado_en
  else:
    columna = Sector.nombre

  if descendente:
    query = query.order_by(columna.desc())
  else:
    query = query.order_by(columna.asc())

  pagina = max(pagina, 1)
  query = query.limit(POR_PAGINA).offset((pagina - 1) * POR_PAGINA)

  return {
    "sectores": db.session.scalars(query).all(),
    "pagina": pagina,
    "total": total,
    "total_paginas": max((total + POR_PAGINA - 1) // POR_PAGINA, 1),
  }