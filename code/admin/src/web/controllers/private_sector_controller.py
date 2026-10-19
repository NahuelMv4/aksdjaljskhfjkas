from flask import Blueprint, flash, redirect, render_template, request, url_for
from marshmallow import ValidationError
from src.core.errores.custom_errors import AppError
from src.core.services import sector_service
from src.web.schemas.sector_schema import sector_schema

priv_sector_bp = Blueprint("sectores", __name__, url_prefix="/sectores")

@priv_sector_bp.get("/")
def listar():
  nombre = request.args.get("nombre", "").strip()
  estado = request.args.get("estado", "")
  orden = request.args.get("orden", "nombre")
  descendente = request.args.get("dir") == "desc"
  pagina = request.args.get("pagina", 1, type=int)

  activo = None
  if estado == "activo":
    activo = True
  elif estado == "inactivo":
    activo = False

  resultado = sector_service.funcionalidad_busqueda(
    nombre=nombre,
    activo=activo,
    orden=orden,
    descendente=descendente,
    pagina=pagina,
  )

  filtros = {
    "nombre": nombre,
    "estado": estado,
    "orden": orden,
    "dir": "desc" if descendente else "asc",
  }
  return render_template("sector/sector.html", **resultado, filtros=filtros)


@priv_sector_bp.get("/<int:sector_id>/editar")
def editar(sector_id):
  sector = sector_service.read_sector(sector_id)
  if sector is None:
    flash("Sector no encontrado", "error")
    return redirect(url_for("sectores.listar"))
  return render_template("sector/sector_form.html", sector=sector)


@priv_sector_bp.post("/nuevo")
def crear():
  try:
    datos = sector_schema.load(request.form.to_dict())
    sector_service.create_sector(**datos)
  except ValidationError as err:
    flash(str(err.messages), "error")
    return render_template("sector/sector_form.html"), 400
  except AppError as err:
    flash(err.message, "error")
    return render_template("sector/sector_form.html"), err.status_code

  flash("Sector creado", "success")
  return redirect(url_for("sectores.listar"))


@priv_sector_bp.post("/<int:sector_id>/desactivar")
def desactivar(sector_id):
  sector = sector_service.delete_sector(sector_id)
  if sector is None:
    flash("Sector no encontrado", "error")
  else:
    flash("Sector desactivado", "success")
  return redirect(url_for("sectores.listar"))


@priv_sector_bp.post("/<int:sector_id>/reactivar")
def reactivar(sector_id):
  sector = sector_service.update_sector(sector_id, activo=True)
  if sector is None:
    flash("Sector no encontrado", "error")
  else:
    flash("Sector reactivado", "success")
  return redirect(url_for("sectores.listar"))

@priv_sector_bp.post("/<int:sector_id>/editar")
def actualizar(sector_id):
  sector = sector_service.read_sector(sector_id)
  if sector is None:
    flash("Sector no encontrado", "error")
    return redirect(url_for("sectores.listar"))

  try:
    datos = sector_schema.load(request.form.to_dict())
    sector_service.update_sector(sector_id, **datos)
  except ValidationError as err:
    flash(str(err.messages), "error")
    return render_template("sector/sector_form.html", sector=sector), 400
  except AppError as err:
    flash(err.message, "error")
    return render_template("sector/sector_form.html", sector=sector), err.status_code

  flash("Sector actualizado", "success")
  return redirect(url_for("sectores.listar"))