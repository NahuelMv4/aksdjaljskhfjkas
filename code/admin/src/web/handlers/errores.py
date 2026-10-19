from flask import render_template, request, jsonify
from dataclasses import dataclass

@dataclass
class ErrorHTTP:
    code: int
    message: str
    description: str

#401 unauthorized 
def unauthorized(e):    
    error = ErrorHTTP(
        code=401,
        message="Acceso no autorizado",
        description="No se ha proporcionado la autenticacion o esta no es valida"
    )
    return render_template('error.html', error=error), 401

#403 forbidden
def forbidden(e):
    if request.path.startswith('/api'):
        return jsonify({
            "error": "Acción no permitida",
            "code": 403
        }), 403

    error = ErrorHTTP(
        code=403,
        message="Acceso denegado",
        description="No tiene permisos para acceder a este recurso"
    )
    return render_template('error.html', error=error), 403

#404 not_found
def not_found(e):
    error = ErrorHTTP(
        code=404,
        message="No encontrado",
        description="El recurso solicitado no se encontro en el servidor"
    )
    return render_template('error.html', error=error), 404    


#500 internal_server_error
def internal_server_error(e):
    if request.path.startswith('/api'):
        return jsonify({
            "error": "Error interno del servidor",
            "code": 500
        }), 500
    
    error = ErrorHTTP(
        code=500,
        message="Error interno del servidor",
        description="El servidor encontro un error inesperado al procesar la solicitud"
    )
    return render_template('error.html', error=error), 500