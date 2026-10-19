from flask import Blueprint, abort, current_app, flash, g, redirect, render_template, request, url_for
from src.core.services import usuario_service, rol_permiso_service
from src.core.services.usuario_service import UsuarioError
from src.web.helpers.auth import login_required, check
from src.web.schemas.usuario_schema import validar_filtros, validar_usuario
from src.core.services import sector_service, tipo_menu_service, rol_permiso_service

bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

def _args_url(filtros, orden, sentido):
    args = {k: v for k, v in filtros.items() if k != "activo"}
    if "activo" in filtros:
        args["activo"] = "1" if filtros["activo"] else "0"
    args.update(orden=orden, sentido=sentido)
    return args

def _valores(usuario):
    return {
        "email": usuario.email, "nombre": usuario.nombre, "apellido": usuario.apellido, "dni": usuario.dni,
        "activo": "1" if usuario.activo else "0", "rol_id": str(usuario.rol_id),
        "sector_id": str(usuario.sector_id or ""),
    }

@bp.get("")
@login_required
def listar():
    filtros, orden, sentido, pagina = validar_filtros(request.args)
    roles = rol_permiso_service.list_roles()
    por_pagina = current_app.config.get("PER_PAGE", usuario_service.PER_PAGE_MAX)
    paginacion = usuario_service.listar(filtros, orden, sentido, pagina, por_pagina)
    sectores = sector_service.list_sectores() 
    tipos_menu = tipo_menu_service.list_tipo_menu() 

    return render_template(
        "usuarios/index.html", paginacion=paginacion, filtros=filtros, orden=orden, sentido=sentido,
        args=_args_url(filtros, orden, sentido), sectores=sectores, tipos_menu=tipos_menu, roles=roles,)

@bp.get("/nuevo")
@login_required
def nuevo():
    roles = rol_permiso_service.list_roles()
    sectores = sector_service.list_sectores() 
    return render_template(
        "usuarios/form.html", usuario=None, valores={}, errores={},
        roles=roles, sectores=sectores, )

@bp.post("/nuevo")
@login_required
def crear():
    
    datos, errores = validar_usuario(request.form)
    if not errores:
        try:
            usuario = usuario_service.crear(datos)
        except UsuarioError as error:
            errores = error.errores or {"_general": str(error)}
        else:
            flash("Usuario creado correctamente.", "success")
            return redirect(url_for("usuarios.detalle", usuario_id=usuario.id))
    flash("Revisá los datos ingresados.", "danger")
    sectores = sector_service.list_sectores() 
    tipos_menu = tipo_menu_service.list_tipo_menu() 
    roles = rol_permiso_service.list_roles()
    return render_template(
        "usuarios/form.html", usuario=None, valores=request.form, errores=errores,
        sectores=sectores, tipos_menu=tipos_menu, roles=roles,
    )

@bp.get("/<int:usuario_id>")
@login_required
def detalle(usuario_id):
    """Detalle de un usuario."""
    usuario = usuario_service.obtener(usuario_id)
    if usuario is None:
        abort(404)
    return render_template(
        "usuarios/detalle.html", usuario=usuario,
        sectores=usuario_service.sectores_asignables(usuario.sector_id),
    )

@bp.get("/<int:usuario_id>/editar")
@login_required
def editar(usuario_id):
    usuario = usuario_service.obtener(usuario_id)
    roles = rol_permiso_service.list_roles()
    sectores = sector_service.list_sectores() 
    tipos_menu = tipo_menu_service.list_tipo_menu() 
    if usuario is None:
        abort(404)
    return render_template(
        "usuarios/editar.html", usuario=usuario, valores=_valores(usuario), errores={},
        roles=roles, sectores=sectores, tipos_menu=tipos_menu,
    )

@bp.post("/<int:usuario_id>/editar")
@login_required
def actualizar(usuario_id):
    usuario = usuario_service.obtener(usuario_id)
    if usuario is None:
        abort(404)
    datos, errores = validar_usuario(request.form, es_edicion=True)
    if not errores:
        try:
            usuario_service.actualizar(usuario_id, datos, g.usuario.id)
        except UsuarioError as error:
            errores = error.errores or {"_general": str(error)}
        else:
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.detalle", usuario_id=usuario_id))
    flash("Revisá los datos ingresados.", "danger")
    sectores = sector_service.list_sectores()
    roles = rol_permiso_service.list_roles()
    return render_template(
        "usuarios/editar.html", usuario=usuario, valores=request.form, errores=errores, sectores=sectores, roles=roles )

@bp.post("/<int:usuario_id>/eliminar")
@login_required
def eliminar(usuario_id):
    try:
        usuario_service.eliminar(usuario_id, g.usuario.id)
    except UsuarioError as error:
        flash(str(error), "danger")
        return redirect(url_for("usuarios.detalle", usuario_id=usuario_id))
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("usuarios.listar"))

@bp.route("/<int:usuario_id>/bloquear")
@login_required
def bloquear(usuario_id):
    usuario = usuario_service.bloquear(usuario_id)
    if usuario is None:
        flash("El usuario no existe.", "danger")
        return redirect(url_for("usuarios.listar"))
    flash("El usuario ha sido bloqueado exitosamente.", "warning")
    return redirect(url_for("usuarios.detalle", usuario_id=usuario.id))

@bp.route("/<int:usuario_id>/desbloquear")
@login_required
def desbloquear(usuario_id):
    usuario = usuario_service.desbloquear(usuario_id)
    if usuario is None:
        flash("El usuario no existe.", "danger")
        return redirect(url_for("usuarios.listar"))
    flash("El usuario ha sido desbloqueado exitosamente.", "success")
    return redirect(url_for("usuarios.detalle", usuario_id=usuario.id))