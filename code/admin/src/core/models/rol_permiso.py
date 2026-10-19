from sqlalchemy import Column, ForeignKey, Table
from src.core.database import Base

rol_permiso = Table(
    "ROL_PERMISO",
    Base.metadata,
    Column("rol_id", ForeignKey("ROL.id"), primary_key=True),
    Column("permiso_id", ForeignKey("PERMISO.id"), primary_key=True),
)