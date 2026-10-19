from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.core.services import sector_service
from src.web.schemas.sector_schema import sector_schema, lista_sectores_schema
from src.core.errores.custom_errors import BadRequestError, NotFoundError

bp_sector = Blueprint("api_sectores", __name__, url_prefix="/api/sectores")

@bp_sector.get("/")
def listar():
  nombre = request.args.get("nombre")
  orden = request.args.get("orden", "nombre")
  descendente = request.args.get("descendente") == "true"
  pagina = request.args.get("pagina", 1, type=int)    

  estado = request.args.get("activo")
  activo = None
  if estado == "true":
    activo = True
  elif estado == "false":
    activo = False

  resultado = sector_service.funcionalidad_busqueda(   
    nombre=nombre,
    activo=activo,
    orden=orden,
    descendente=descendente,
    pagina=pagina,                        
  )
  return jsonify({                                          
    "data": lista_sectores_schema.dump(resultado["sectores"]),
    "pagina": resultado["pagina"],
    "total": resultado["total"],
    "total_paginas": resultado["total_paginas"],
  }), 200

@bp_sector.get("/<int:sector_id>")
def obtener(sector_id):
  sector = sector_service.read_sector(sector_id)
  if sector is None:
    raise NotFoundError("Sector no encontrado")
  return jsonify(sector_schema.dump(sector)), 200

@bp_sector.post("/")
def crear():
  try:
    datos = sector_schema.load(request.get_json(silent=True) or {})
  except ValidationError as err:
    raise BadRequestError(err.messages)

  sector = sector_service.create_sector(**datos)
  return jsonify(sector_schema.dump(sector)), 201


@bp_sector.put("/<int:sector_id>")
def actualizar(sector_id):
  try:
    datos = sector_schema.load(request.get_json(silent=True) or {}, partial=True)
  except ValidationError as err:
    raise BadRequestError(err.messages)

  sector = sector_service.update_sector(sector_id, **datos)
  if sector is None:
    raise NotFoundError("Sector no encontrado")
  return jsonify(sector_schema.dump(sector)), 200


@bp_sector.delete("/<int:sector_id>")
def eliminar(sector_id):
  sector = sector_service.delete_sector(sector_id)
  if sector is None:
    raise NotFoundError("Sector no encontrado")
  return jsonify(sector_schema.dump(sector)), 200

