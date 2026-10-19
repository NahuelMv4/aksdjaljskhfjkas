from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from typing import List, Optional


class Personal(Base):
  __tablename__ = "PERSONAL"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nombre: Mapped[str] = mapped_column()
  apellido: Mapped[str] = mapped_column()
  dni: Mapped[str] = mapped_column(unique=True)
  activo: Mapped[bool] = mapped_column(default=True)
  creado_en: Mapped[datetime] = mapped_column(
      DateTime, default=lambda: datetime.now(timezone.utc)
    )
  actualizado_en: Mapped[datetime] = mapped_column(
      DateTime, 
      default=lambda: datetime.now(timezone.utc),
      onupdate=lambda: datetime.now(timezone.utc)
    )

  tipo_personal_id: Mapped[int] = mapped_column(ForeignKey("TIPO_PERSONAL.id"), nullable=False)
  tipo_personal: Mapped["TipoPersonal"] = relationship(back_populates="lista_personal")

  sector_id: Mapped[Optional[int]] = mapped_column(ForeignKey("SECTOR.id"), nullable=True)
  sector: Mapped[Optional["Sector"]] = relationship(back_populates="lista_personal")

  tipo_menu_id: Mapped[int] = mapped_column(ForeignKey("TIPO_MENU.id"), nullable=False)
  tipo_menu: Mapped["TipoMenu"] = relationship(back_populates="lista_personal")

  solicitudes_comida: Mapped[List["SolicitudComida"]] = relationship(back_populates="personal")
  entregas: Mapped[List["Entrega"]] = relationship(back_populates="personal")

  def __repr__(self):
    return f"<PERSONAL(id={self.id}, nombre={self.nombre}, apellido={self.apellido}, dni={self.dni})>"