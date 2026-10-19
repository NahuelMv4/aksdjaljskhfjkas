from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from typing import List

class Cupo(Base):
  __tablename__ = "CUPO"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  cantidad: Mapped[int] = mapped_column(nullable=False)
  creado_en: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc)
  )
  actualizado_en: Mapped[datetime] = mapped_column(
    DateTime, 
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )

  sector_id: Mapped[int] = mapped_column(ForeignKey("SECTOR.id"), nullable=False)
  sector: Mapped["Sector"] = relationship(back_populates="cupos")

  tipo_comida_id: Mapped[int] = mapped_column(ForeignKey("TIPO_COMIDA.id"), nullable=False)
  tipo_comida: Mapped["TipoComida"] = relationship(back_populates="cupos")

  registros_cupo: Mapped[List["RegistroCupo"]] = relationship(back_populates="cupo")

  def __repr__(self):
    return f"<CUPO(id={self.id}, cantidad={self.cantidad})>"