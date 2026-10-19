from functools import wraps
from flask import abort, session
from src.core.services import usuario_service


def is_authenticated(session):
    return session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated(session):
            abort(401)
        return f(*args, **kwargs)
    return decorated_function


def check_permission(permission):
    user_email = session.get("user")
    user = usuario_service.obtener_usuario_por_email(user_email)
    permissions = usuario_service.obtener_permisos_usuario(user.id)
    return user is not None and permission in permissions

def check(permission):
    def decorator(f):
        @wraps(f)
        def decorated_funcion(*args, **kwargs):
            if not check_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_funcion
    return decorator