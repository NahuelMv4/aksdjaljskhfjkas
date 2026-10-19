from src.core.enums import RolEnum
from src.core.database import Base
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

class Rol(Base):
  __tablename__ = "ROL"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nombre: Mapped[RolEnum] = mapped_column(
    SQLEnum(
      RolEnum,
      values_callable=lambda x: [e.value for e in x],
      native_enum=False
    ),
    unique=True,
    nullable=False
  )
  
  permisos: Mapped[List["Permiso"]] = relationship(secondary="ROL_PERMISO", back_populates="roles")
  usuarios: Mapped[List["Usuario"]] = relationship(back_populates="rol")

  def __repr__(self):
    return f"<ROL(id={self.id}, nombre={self.nombre})>"