from src.core.errores.custom_errors import ConflictError, NotFoundError
from src.core.database import db
from src.core.models.personal import Personal
from sqlalchemy import select

def popular_personal(**kwargs):
    """Se agregan datos de personal desde el seeder"""
    try:
        personal = Personal(**kwargs)
        db.session.add(personal)
        db.session.commit()
        return personal
    except Exception as e:
        db.session.rollback()
        raise ConflictError("Ya existe personal con este DNI.")


def list_personal(filters: dict):
    """Obtiene una lista con todos los miembros del personal registrados en la base de datos.

    Returns:
        List[Personal]: Lista de instancias del modelo Personal.
    """
    stmt = select(Personal)
    if filters.get("dni"):
        stmt = stmt.where(Personal.dni.ilike(f"%{filters['dni']}%"))

    if filters.get("nombre"):
        stmt = stmt.where(Personal.nombre.ilike(f"%{filters['nombre']}%"))

    if filters.get("apellido"):
        stmt = stmt.where(Personal.apellido.ilike(f"%{filters['apellido']}%"))

    if filters.get("tipo_personal_id"):
        stmt = stmt.where(Personal.tipo_personal_id == filters["tipo_personal_id"])

    activo = filters.get("activo", True) 
    stmt = stmt.where(Personal.activo == activo)

    page = filters.get("page", 1)
    per_page = min(filters.get("per_page", 25), 25)
    
    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    return db.session.execute(stmt).scalars().all()


def find_personal_by_id(personal_id: int):
    """Busca y retorna un miembro del personal según su ID único.

    Args:
        personal_id (int): ID del miembro del personal a buscar.

    Returns:
        Personal: La instancia del modelo Personal encontrada.

    Raises:
        NotFoundError: Si no existe ningún miembro del personal con el ID especificado[cite: 20].
    """
    personal = db.session.get(Personal, personal_id)
    if not personal:
        raise NotFoundError("Miembro del personal no encontrado.")
    return personal


def create_personal(data: dict):
    """Registra un nuevo miembro del personal en la base de datos.

    Valida que no exista previamente un registro con el mismo DNI antes
    de persistir los datos.

    Args:
        data (dict): Diccionario con los datos validados del personal 
        -> (nombre, apellido, dni, tipo_personal_id, tipo_menu_id, sector_id).

    Returns:
        Personal: La instancia del modelo Personal creada y guardada con éxito.

    Raises:
        ConflictError: Si ya existe una persona registrada con el mismo DNI.
    """
    existe = db.session.execute(select(Personal).where(Personal.dni == data["dni"])).scalars().first()
    if existe:
        raise ConflictError("Ya existe una persona con el mismo DNI.")

    # Verificar Autorización: 403

    try:
        personal = Personal(**data)
        db.session.add(personal)
        db.session.commit()
        return personal
    except Exception as e:
        db.session.rollback()
        raise e

def update_personal(personal_id: int, **kwargs):
    """Actualiza parcialmente los datos de un miembro del personal en la base de datos[cite: 16].

    Busca al miembro por su ID y modifica únicamente los campos especificados 
    en los argumentos.

    Args:
        personal_id (int): ID del miembro del personal a actualizar.
        **kwargs: Pares de clave-valor con los atributos a modificar.

    Returns:
        Personal: La instancia del modelo Personal actualizada y guardada con éxito.

    Raises:
        NotFoundError: Si no se encuentra un miembro del personal con el ID provisto[cite: 16].
    """
    try:
        personal = db.session.get(Personal, personal_id)
        if not personal:
            raise NotFoundError("Miembro del personal no encontrado.")

        for key, value in kwargs.items():
            setattr(personal, key, value)
        db.session.commit()
        return personal
    except Exception as e:
        db.session.rollback()
        raise e


def delete_personal(personal_id: int):
    """Elimina un miembro del personal de la base de datos por su ID.

    Args:
        personal_id (int): ID del miembro del personal a eliminar.

    Returns:
        None

    Raises:
        NotFoundError: Si no se encuentra un miembro del personal con el ID provisto.
    """
    try:
        personal = db.session.get(Personal, personal_id)
        if not personal:
            raise NotFoundError("Miembro del personal no encontrado")
        db.session.delete(personal)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e