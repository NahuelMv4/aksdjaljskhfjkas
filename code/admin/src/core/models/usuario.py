from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from typing import List

class Usuario(Base):
  __tablename__ = "USUARIO"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(unique=True, nullable=False)
  contrasenia: Mapped[str] = mapped_column(nullable=False)
  nombre: Mapped[str] = mapped_column()
  apellido: Mapped[str] = mapped_column()
  dni: Mapped[str] = mapped_column(unique=True)
  activo: Mapped[bool] = mapped_column(default=True)
  bloqueado: Mapped[bool] = mapped_column(default=False)
  creado_en: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc)
    )
  actualizado_en: Mapped[datetime] = mapped_column(
      DateTime, 
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc)
    )

  rol_id: Mapped[int] = mapped_column(ForeignKey("ROL.id"), nullable=False)
  rol: Mapped["Rol"] = relationship(back_populates="usuarios")

  sector_id: Mapped[int] = mapped_column(ForeignKey("SECTOR.id"), nullable=False)
  sector: Mapped["Sector"] = relationship(back_populates="usuarios")

  revisiones: Mapped[List["Revision"]] = relationship(back_populates="usuario")
  pedidos: Mapped[List["Pedido"]] = relationship(back_populates="usuario")

  def __repr__(self):
    return f"<USUARIO(id={self.id}, nombre={self.nombre}, dni={self.dni}, email={self.email})>"