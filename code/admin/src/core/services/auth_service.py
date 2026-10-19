from sqlalchemy import select
import bcrypt

from src.core.database import db
from src.core.models.usuario import Usuario  


def _contrasenia_valida(guardada, ingresada):
    return bcrypt.checkpw(
        ingresada.encode("utf-8"),
        guardada.encode("utf-8")
    )


def autenticar(email, password):
    usuario = db.session.execute(
        select(Usuario).where(Usuario.email == email)
    ).scalars().first()

    if usuario is None:
        return None
    if not _contrasenia_valida(usuario.contrasenia, password):
        return None
    if usuario.bloqueado:
        return None
    return usuario