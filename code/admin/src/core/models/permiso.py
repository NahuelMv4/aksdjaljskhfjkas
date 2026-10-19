from src.core.enums import PermisoEnum
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import Enum as SQLEnum

class Permiso(Base):
  __tablename__ = "PERMISO"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  codigo: Mapped[PermisoEnum] = mapped_column(
    SQLEnum(
        PermisoEnum,
        values_callable=lambda x: [e.value for e in x],
        native_enum=False,
    ),
    unique=True,
    nullable=False,
  )
  roles: Mapped[List["Rol"]] = relationship(
    secondary="ROL_PERMISO", back_populates="permisos"
  )

  def __repr__(self):
    return f"<PERMISO(id={self.id}, codigo={self.codigo})>"