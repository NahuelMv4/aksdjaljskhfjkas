from sqlalchemy import select, func
from src.core.database import db
from src.core.models.cupo import Cupo
from src.core.models.sector import Sector
from src.core.models.tipo_comida import TipoComida
from src.core.errores.custom_errors import NotFoundError, ConflictError

def get_cupos(sector_id=None, tipo_comida_id=None, page=1):
    """Obtiene una lista paginada de cupos con filtros opcionales."""
    
    # Inicia la consulta apuntando al modelo Cupo
    stmt = select(Cupo)

    if sector_id:
        stmt = stmt.where(Cupo.sector_id == sector_id)
    if tipo_comida_id:
        stmt = stmt.where(Cupo.tipo_comida_id == tipo_comida_id)

    # (Depende del Issue #10): Reemplazar este diccionario falso por la consulta real a la BD y agregar el import adecuado
    config_mock = {"elementos_por_pagina": 25}
    per_page = config_mock["elementos_por_pagina"]

    # Calcula el total de registros para armar la paginacion manual
    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.session.execute(total_stmt).scalar()

    # Ordena por sector y aplica limite y desplazamiento usando el per_page hardcodeado
    stmt = stmt.order_by(Cupo.sector_id.asc())
    stmt = stmt.offset((page - 1) * per_page).limit(per_page)
    
    items = db.session.execute(stmt).scalars().all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "pages": (total + per_page - 1) // per_page if total > 0 else 1
    }

def get_cupo_by_id(cupo_id: int) -> Cupo:
    """Busca un cupo por su ID."""
    
    # Busca el registro directamente por su clave primaria
    cupo = db.session.get(Cupo, cupo_id)
    
    # Corta la ejecucion con un error 404 si el registro no existe
    if not cupo:
        raise NotFoundError("El cupo solicitado no existe.")
        
    return cupo


def create_cupo(data: dict) -> Cupo:
    """Crea un nuevo cupo en el sistema validando reglas de negocio."""
    
    # Extrae los datos que ya vienen validados y limpios desde el controlador
    sector_id = data.get("sector_id")
    tipo_comida_id = data.get("tipo_comida_id")

    # Verifica la integridad referencial: el sector debe existir y estar activo
    sector = db.session.get(Sector, sector_id)
    if not sector or not sector.activo:
        raise NotFoundError("El sector especificado no existe o se encuentra inactivo.")

    # Verifica que el tipo de comida exista en la base de datos
    tipo_comida = db.session.get(TipoComida, tipo_comida_id)
    if not tipo_comida:
        raise NotFoundError("El tipo de comida especificado no existe.")

    # Regla de negocio core: evita registros duplicados para la misma combinacion de sector y comida
    stmt = select(Cupo).where(Cupo.sector_id == sector_id, Cupo.tipo_comida_id == tipo_comida_id)
    existente = db.session.execute(stmt).scalars().first()
    
    if existente:
        raise ConflictError("Ya existe un cupo vigente para este sector y tipo de comida.")

    # Desempaqueta los datos validados (**data) para crear la instancia y la guarda en BD
    nuevo_cupo = Cupo(**data)
    db.session.add(nuevo_cupo)
    db.session.commit()

    return nuevo_cupo


def update_cupo(cupo_id: int, **kwargs) -> Cupo:
    """Actualiza la cantidad de comensales de un cupo existente."""
    
    # Reutiliza la funcion de busqueda, que ya maneja el error 404 si no existe
    cupo = get_cupo_by_id(cupo_id)

    # Itera sobre los campos enviados y los actualiza de forma dinamica (como la cantidad)
    for key, value in kwargs.items():
        setattr(cupo, key, value)
        
    # Confirma la transaccion en la base de datos
    db.session.commit()
    
    return cupo