import importlib
import logging
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from src.core.database import db
from src.core.models import Rol, Sector, Usuario
from src.core.services.security import hashear_password

def create_usuario(**kwargs):
    usuario = Usuario(**kwargs)
    db.session.add(usuario)
    db.session.commit()
    return usuario

logger = logging.getLogger(__name__)

ROL_ADMIN = "Administrador"
PER_PAGE_MAX = 25

_REFERENCIAS_OPERATIVAS = [
    ("src.core.models.pedido", "Pedido", "usuario_id"),
    ("src.core.models.revision", "Revision", "usuario_id"),
    ("src.core.models.configuracion_sistema", "ConfiguracionSistema", "actualizado_por_usuario_id"),
]

def _like(valor):
    """Auxiliar para escapar y armar patrones de búsqueda con LIKE."""
    return f"%{valor}%" 
 
class UsuarioError(Exception):
    def __init__(self, mensaje, errores=None):
        super().__init__(mensaje)
        self.errores = errores or {}

# paginación segura
class PaginationResult:
    """Clase auxiliar para manejar la paginación compatible con cualquier versión de SQLAlchemy."""
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total
        self.pages = max(1, (total + per_page - 1) // per_page)
        self.has_prev = page > 1
        self.has_next = page < self.pages
        self.prev_num = page - 1 if self.has_prev else None
        self.next_num = page + 1 if self.has_next else None

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


# consultas 
def _columnas_orden(orden):
    return {
        "creado_en": [Usuario.creado_en],
        "apellido": [Usuario.apellido, Usuario.nombre],
        "email": [Usuario.email],
    }.get(orden, [Usuario.creado_en])
 
def listar(filtros, orden="creado_en", sentido="desc", pagina=1, por_pagina=PER_PAGE_MAX):
    """Búsqueda con filtros combinables, orden y paginación del lado del servidor (máx. 25)."""
    por_pagina = max(1, min(int(por_pagina), PER_PAGE_MAX))
    stmt = select(Usuario).options(joinedload(Usuario.rol), joinedload(Usuario.sector))
    if filtros.get("email"):
        stmt = stmt.where(Usuario.email.ilike(_like(filtros["email"]), escape="\\"))
    if filtros.get("q"):
        patron = _like(filtros["q"])
        stmt = stmt.where(or_(
            Usuario.nombre.ilike(patron, escape="\\"),
            Usuario.apellido.ilike(patron, escape="\\"),
            (Usuario.nombre + " " + Usuario.apellido).ilike(patron, escape="\\"),
            (Usuario.apellido + " " + Usuario.nombre).ilike(patron, escape="\\"),
        ))
    if filtros.get("dni"):
        stmt = stmt.where(Usuario.dni.ilike(_like(filtros["dni"]), escape="\\"))
    if filtros.get("activo") is not None:
        stmt = stmt.where(Usuario.activo.is_(filtros["activo"]))
    if filtros.get("rol_id"):
        stmt = stmt.where(Usuario.rol_id == filtros["rol_id"])
    if filtros.get("sector_id"):
        stmt = stmt.where(Usuario.sector_id == filtros["sector_id"])
 
    columnas = _columnas_orden(orden)
    columnas = [c.desc() if sentido == "desc" else c.asc() for c in columnas]
    stmt = stmt.order_by(*columnas, Usuario.id)

    count_stmt = select(func.count()).select_from(stmt.order_by(None).subquery())
    total = db.session.scalar(count_stmt) or 0
    paginated_stmt = stmt.offset((pagina - 1) * por_pagina).limit(por_pagina)
    items = db.session.scalars(paginated_stmt).all()
    
    return PaginationResult(items, pagina, por_pagina, total)
 
def obtener(usuario_id):
    return db.session.get(Usuario, usuario_id)
 
def obtener_permisos_usuario(user_id):
    usuario = db.session.get(Usuario, user_id)
    if not usuario:
        return []
    return [permiso.codigo for permiso in usuario.rol.permisos]

def obtener_usuario_activo(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    return usuario if usuario and usuario.activo else None
 
def obtener_usuario_por_email(email):
    return db.session.execute(
        select(Usuario).where(func.lower(Usuario.email) == func.lower(email))
    ).scalars().first()
 
def sectores_asignables(incluir_id=None):
    """Sectores activos (más el actual del usuario, aunque esté inactivo) para los formularios."""
    cond = Sector.activo.is_(True)
    if incluir_id:
        cond = or_(cond, Sector.id == incluir_id)
    return db.session.execute(select(Sector).where(cond).order_by(Sector.nombre)).scalars().all()
 
# reglas
def _validar_reglas(datos, usuario=None, actor_id=None):
    errores = {}
    rol = db.session.get(Rol, datos.get("rol_id"))
    if rol is None:
        errores["rol_id"] = "El rol seleccionado no existe."
        return errores, None, None

    for campo, columna in (("email", func.lower(Usuario.email)), ("dni", Usuario.dni)):
        valor = datos[campo].lower() if campo == "email" else datos[campo]
        consulta = select(Usuario.id).where(columna == valor)
        if usuario is not None:
            consulta = consulta.where(Usuario.id != usuario.id)
        if db.session.execute(consulta).first():
            errores[campo] = (
                "Ya existe un usuario con ese correo electrónico." if campo == "email"
                else "Ya existe un usuario con ese DNI."
            )
 
    sector_id = datos.get("sector_id")
    sector_id = int(sector_id) if sector_id else None
    if sector_id is None:
        errores["sector_id"] = "Seleccioná un sector obligatorio."
    else:
        sector = db.session.get(Sector, sector_id)
        if sector is None:
            errores["sector_id"] = "El sector seleccionado no existe."
        else:
            cambia = (usuario is None or usuario.sector_id != sector_id or usuario.rol_id != rol.id)
            if cambia and not sector.activo:
                errores["sector_id"] = "No se puede asociar un usuario a un sector inactivo."

    if rol.nombre == ROL_ADMIN and datos.get("activo") is False:
        errores["activo"] = "Un Administrador no puede estar bloqueado."
    if usuario is not None and actor_id == usuario.id and rol.nombre != ROL_ADMIN:
        errores["rol_id"] = "No podés quitarte el rol de Administrador a vos mismo."
    if usuario is not None and actor_id == usuario.id and datos.get("activo") is False:
        errores["activo"] = "No podés bloquearte a vos mismo."
    return errores, rol, sector_id
 
def _fallar(errores):
    raise UsuarioError(next(iter(errores.values())), errores)
 
# CRUD DE USUARIOS
def crear(datos):
    errores, rol, sector_id = _validar_reglas(datos)
    if errores:
        _fallar(errores)
    usuario = Usuario(
        email=datos["email"], nombre=datos["nombre"], apellido=datos["apellido"], dni=datos["dni"],
        activo=datos["activo"], rol_id=rol.id, sector_id=sector_id,
        contrasenia=hashear_password(datos["password"]),
    )
    db.session.add(usuario)
    _guardar()
    logger.info("Usuario %s creado", usuario.id)
    return usuario
 
def actualizar(usuario_id, datos, actor_id):
    usuario = obtener(usuario_id)
    if usuario is None:
        raise UsuarioError("El usuario no existe.")
    errores, rol, sector_id = _validar_reglas(datos, usuario, actor_id)
    if errores:
        _fallar(errores)
 
    usuario.email = datos["email"]
    usuario.nombre = datos["nombre"]
    usuario.apellido = datos["apellido"]
    usuario.dni = datos["dni"]
    usuario.activo = datos["activo"]
    usuario.rol_id = rol.id
    usuario.sector_id = sector_id  # None si el rol no es Jefe de Servicio
    if datos.get("password"):
        usuario.contrasenia = hashear_password(datos["password"])
    _guardar()
    logger.info("Usuario %s actualizado por usuario %s", usuario.id, actor_id)
    return usuario
 
def tiene_operaciones(usuario_id):
    """True si el usuario figura en pedidos, revisiones u otras operaciones."""
    for modulo, clase, campo in _REFERENCIAS_OPERATIVAS:
        try:
            modelo = getattr(importlib.import_module(modulo), clase)
        except (ImportError, AttributeError):
            continue
        existe = select(modelo.id).where(getattr(modelo, campo) == usuario_id).limit(1)
        existe = db.session.execute(existe).first()
        
        if existe:
            return True
    return False
 
def eliminar(usuario_id, actor_id):
    usuario = obtener(usuario_id)
    if usuario is None:
        raise UsuarioError("El usuario no existe.")
    if tiene_operaciones(usuario.id):
        raise UsuarioError(
            "El usuario tiene pedidos, autorizaciones u otras operaciones asociadas: no puede eliminarse. "
            "Bloquealo para que no pueda ingresar."
        )
    db.session.delete(usuario)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UsuarioError("El usuario tiene registros asociados: bloquealo en lugar de eliminarlo.")
    logger.info("Usuario %s eliminado por usuario %s", usuario_id, actor_id)
 
def _guardar():
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UsuarioError("El correo o el DNI ya están registrados.", {"email": "Dato duplicado."})

def bloquear(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if usuario:
        usuario.activo = False
        db.session.commit()
    return usuario

def desbloquear(usuario_id):
    usuario = db.session.get(Usuario, usuario_id)
    if usuario:
        usuario.activo = True
        db.session.commit()
    return usuario