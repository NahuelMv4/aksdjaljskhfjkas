from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from src.core.errores.custom_errors import BadRequestError
from src.web.schemas.personal_schema import personal_schema, lista_personal_schema
from src.core.services import personal_service
from src.web.schemas.personal_filter_schema import personal_filter_schema

personal_bp = Blueprint("personal", __name__, url_prefix="/api/personnel")


@personal_bp.get("/")
def index():
    """Endpoint para listar personal con filtros y paginación.

    Response: Lista en formato JSON con los datos serializados de todo el personal 
                  y código HTTP 200.
    """
    try:
        filters = personal_filter_schema.load(request.args.to_dict())
    except ValidationError as err:
        raise BadRequestError(err.messages)

    personal_list = personal_service.list_personal(filters)
    return jsonify(lista_personal_schema.dump(personal_list)), 200


@personal_bp.get("/<int:id>")
def show(id):
    """Endpoint para buscar un miembro del personal por su ID único.

    URL Params:
        id (int): ID del miembro del personal a consultar.

    Response: Objeto JSON con los datos del personal encontrado y código HTTP 200.

    Raises:
        404: Si no existe un miembro del personal con el ID provisto.
    """
    personal = personal_service.find_personal_by_id(id)
    return jsonify(personal_schema.dump(personal)), 200


@personal_bp.post("/")
def store():
    """Endpoint para registrar un nuevo miembro del personal.

    Expected JSON Body:
        {
            "nombre": "string",
            "apellido": "string",
            "dni": "string",
            "tipo_personal_id": int,
            "tipo_menu_id": int,
            "sector_id": int (opcional)
        }

    Response: Objeto JSON con los datos del personal creado y código HTTP 201.
        
    Raises:
        400: Si el JSON está mal formado o falla la validación del Schema.
        409: Si ya existe una persona registrada con el mismo DNI.
    """
    json_data = request.get_json()
    if not json_data:
        raise BadRequestError({"error": "No se proveyeron datos JSON"})

    try:
        data = personal_schema.load(json_data)
    except ValidationError as err:
        raise BadRequestError(err.messages)

    personal = personal_service.create_personal(data)
    return jsonify(personal_schema.dump(personal)), 201


@personal_bp.patch("/<int:id>")
def update(id):
    """Endpoint para actualizar parcialmente un miembro del personal existente.

    URL Params:
        id (int): ID único del miembro del personal a modificar.

    Expected JSON Body (Campos opcionales para actualización parcial):
        {
            "nombre": "string",
            "apellido": "string",
            "dni": "string",
            "tipo_personal_id": int,
            "tipo_menu_id": int,
            "sector_id": int (opcional/null)
        }

    Response: Objeto JSON con los datos actualizados del personal y código HTTP 200.

    Raises:
        400: Si el JSON está mal formado o falla la validación del Schema.
        404: Si el ID provisto no existe en la base de datos.
    """
    json_data = request.get_json()
    if not json_data:
        raise BadRequestError({"error": "No se proveyeron datos JSON"})

    try:
        data = personal_schema.load(json_data, partial=True)
    except ValidationError as err:
        raise BadRequestError(err.messages)

    personal = personal_service.update_personal(id, **data)
    return jsonify(personal_schema.dump(personal)), 200


@personal_bp.delete("/<int:id>")
def destroy(id):
    """Endpoint para eliminar un miembro del personal por su ID.

    URL Params:
        id (int): ID único del miembro del personal a eliminar.

    Response: Objeto JSON con un mensaje de éxito y código HTTP 200.

    Raises:
        404: Si el ID provisto no existe en la base de datos.
    """
    personal_service.delete_personal(id)
    return jsonify({"message": "Personal eliminado con éxito"}), 200