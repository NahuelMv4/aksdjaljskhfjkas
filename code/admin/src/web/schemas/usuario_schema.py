"""Validaciones del lado del servidor (formato y longitud) para el módulo de usuarios."""
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NOMBRE_RE = re.compile(r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+(?:[ '\-][A-Za-zÁÉÍÓÚÜÑáéíóúüñ]+)*$")
DNI_RE = re.compile(r"^\d{7,8}$")
PASSWORD_MIN = 8
PASSWORD_MAX_BYTES = 72  # límite de bcrypt
ORDENES = ("creado_en", "apellido", "email")


def _entero(valor):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return None


def validar_usuario(form, es_edicion=False):
    """Valida el formulario de alta/edición.

    Returns:
        tuple: (datos_limpios, errores) con errores como dict campo -> mensaje.
    """
    errores = {}
    email = (form.get("email") or "").strip().lower()
    nombre = " ".join((form.get("nombre") or "").split())
    apellido = " ".join((form.get("apellido") or "").split())
    dni = (form.get("dni") or "").strip()
    password = form.get("password") or ""
    confirmacion = form.get("password_confirm") or ""

    if not email:
        errores["email"] = "El correo electrónico es obligatorio."
    elif len(email) > 255 or not EMAIL_RE.match(email):
        errores["email"] = "El correo electrónico no tiene un formato válido."

    for campo, valor, etiqueta in (("nombre", nombre, "El nombre"), ("apellido", apellido, "El apellido")):
        if not valor:
            errores[campo] = f"{etiqueta} es obligatorio."
        elif not 2 <= len(valor) <= 50:
            errores[campo] = f"{etiqueta} debe tener entre 2 y 50 caracteres."
        elif not NOMBRE_RE.match(valor):
            errores[campo] = f"{etiqueta} solo puede contener letras, espacios, apóstrofes y guiones."

    if not dni:
        errores["dni"] = "El DNI es obligatorio."
    elif not DNI_RE.match(dni):
        errores["dni"] = "El DNI debe tener 7 u 8 dígitos, sin puntos."

    if password or not es_edicion:  # en edición, vacío = conservar la actual
        if not password:
            errores["password"] = "La contraseña es obligatoria."
        elif len(password) < PASSWORD_MIN:
            errores["password"] = f"La contraseña debe tener al menos {PASSWORD_MIN} caracteres."
        elif len(password.encode("utf-8")) > PASSWORD_MAX_BYTES:
            errores["password"] = "La contraseña es demasiado larga."
        elif password != confirmacion:
            errores["password_confirm"] = "Las contraseñas no coinciden."

    activo_raw = form.get("activo", "1")
    if activo_raw not in ("1", "0"):
        errores["activo"] = "Valor de estado inválido."

    rol_id = _entero(form.get("rol_id"))
    if rol_id is None:
        errores["rol_id"] = "Seleccioná un rol."

    sector_raw = (form.get("sector_id") or "").strip()
    sector_id = _entero(sector_raw) if sector_raw else None
    if sector_raw and sector_id is None:
        errores["sector_id"] = "Sector inválido."

    datos = {
        "email": email, "nombre": nombre, "apellido": apellido, "dni": dni,
        "password": password, "activo": activo_raw != "0",
        "rol_id": rol_id, "sector_id": sector_id,
    }
    return datos, errores


def validar_cambio_rol(form):
    """Valida rol_id y sector_id (opcional) del formulario de cambio de rol."""
    errores, datos = {}, {}
    datos["rol_id"] = _entero(form.get("rol_id"))
    if datos["rol_id"] is None:
        errores["rol_id"] = "Seleccioná un rol válido."
    sector_raw = (form.get("sector_id") or "").strip()
    datos["sector_id"] = _entero(sector_raw) if sector_raw else None
    if sector_raw and datos["sector_id"] is None:
        errores["sector_id"] = "Sector inválido."
    return datos, errores


def validar_filtros(args):
    """Normaliza filtros, orden, sentido y página de la query string (valores inválidos se ignoran)."""
    filtros = {}
    for campo in ("email", "q", "dni"):
        valor = (args.get(campo) or "").strip()[:100]
        if valor:
            filtros[campo] = valor
    if args.get("activo") in ("1", "0"):
        filtros["activo"] = args.get("activo") == "1"
    for campo in ("rol_id", "sector_id"):
        valor = _entero(args.get(campo))
        if valor and valor > 0:
            filtros[campo] = valor
    orden = args.get("orden") if args.get("orden") in ORDENES else "creado_en"
    sentido = args.get("sentido") if args.get("sentido") in ("asc", "desc") else "desc"
    pagina = _entero(args.get("pagina"))
    return filtros, orden, sentido, pagina if pagina and pagina > 0 else 1