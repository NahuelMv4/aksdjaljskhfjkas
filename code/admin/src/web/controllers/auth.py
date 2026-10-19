from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import session 
from src.core.services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")


@auth_bp.route("/", methods=["POST"])
def autenticar():
    email = request.form.get("email")
    password = request.form.get("password")

    usuario = auth_service.autenticar(email, password)
    if usuario is None:
        flash("Credenciales inválidas", "danger")
        return redirect(url_for("auth.login"))

    session.clear()
    session["user"] = usuario.id
    session["nombre"] = usuario.nombre
    session["apellido"] = usuario.apellido
    session["sector_id"] = usuario.sector_id
    session["rol"] = usuario.rol.nombre.value
    session["permisos"] = [p.codigo.value for p in usuario.rol.permisos]
    return redirect(url_for("home"))


@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "success")
    return redirect(url_for("auth.login"))