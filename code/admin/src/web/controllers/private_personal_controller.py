from flask import Blueprint, flash, redirect, render_template, request, url_for
from src.core.errores.custom_errors import ConflictError, NotFoundError
from src.core.services import (
    personal_service,
    sector_service,
    tipo_menu_service,
    tipo_personal_service,
)

priv_personal_bp = Blueprint(
    "priv_personal", __name__, url_prefix="/private/personnel"
)


@priv_personal_bp.get("/")
def listar():
  filters = {}
  personal_list = personal_service.list_personal(filters)
  return render_template("personal/personal.html", personal=personal_list)


@priv_personal_bp.route("/crear", methods=["GET", "POST"])
def crear():
  if request.method == "POST":
    data = {
        "dni": request.form.get("dni"),
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "tipo_personal_id": int(request.form.get("tipo_personal_id")),
        "sector_id": (
            int(request.form.get("sector_id"))
            if request.form.get("sector_id")
            else None
        ),
        "tipo_menu_id": int(request.form.get("tipo_menu_id")),
    }

    try:
      personal_service.create_personal(data)
      flash("Miembro del personal creado exitosamente.", "success")
      return redirect(url_for("priv_personal.listar"))
    except ConflictError as e:
      flash(str(e), "error")
    except Exception as e:
      flash("Ocurrió un error inesperado al crear el registro.", "error")

  tipos_personal = tipo_personal_service.list_tipo_personal() 
  sectores = sector_service.list_sectores() 
  tipos_menu = tipo_menu_service.list_tipo_menu() 

  return render_template(
      "personal/personal_crear.html",
      tipos_personal=tipos_personal,
      sectores=sectores,
      tipos_menu=tipos_menu,
  )


@priv_personal_bp.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
  try:
    persona = personal_service.find_personal_by_id(id)
  except NotFoundError as e:
    flash(str(e), "error")
    return redirect(url_for("priv_personal.listar"))

  if request.method == "POST":
    kwargs = {
        "nombre": request.form.get("nombre"),
        "apellido": request.form.get("apellido"),
        "dni": request.form.get("dni"),
        "tipo_personal_id": int(request.form.get("tipo_personal_id")),
        "sector_id": (
            int(request.form.get("sector_id"))
            if request.form.get("sector_id")
            else None
        ),
        "tipo_menu_id": int(request.form.get("tipo_menu_id")),
    }

    try:
      personal_service.update_personal(id, **kwargs)
      flash("Personal actualizado correctamente.", "success")
      return redirect(url_for("priv_personal.listar"))
    except Exception as e:
      flash("Ocurrió un error al actualizar los datos.", "error")

  tipos_personal = tipo_personal_service.list_tipo_personal()
  sectores = sector_service.list_sectores()
  tipos_menu = tipo_menu_service.list_tipo_menu()

  return render_template(
      "personal/personal_editar.html",
      persona=persona,
      tipos_personal=tipos_personal,
      sectores=sectores,
      tipos_menu=tipos_menu,
  )


@priv_personal_bp.post("/eliminar/<int:id>")
def eliminar(id):
  try:
    personal_service.delete_personal(id)
    flash("Miembro del personal eliminado con éxito.", "success")
  except NotFoundError as e:
    flash(str(e), "error")
  except Exception as e:
    flash("No se pudo eliminar el registro.", "error")

  return redirect(url_for("priv_personal.listar"))