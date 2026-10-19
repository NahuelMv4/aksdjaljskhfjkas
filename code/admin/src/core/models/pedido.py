from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from typing import List

class Pedido(Base):
  __tablename__ = "PEDIDO"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  fecha_desde: Mapped[datetime] = mapped_column(nullable=False)
  fecha_hasta: Mapped[datetime] = mapped_column(nullable=False)
  estado: Mapped[str] = mapped_column(nullable=False)
  creado_en: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc)
  )
  actualizado_en: Mapped[datetime] = mapped_column(
    DateTime, 
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )

  tipo_comida_id: Mapped[int] = mapped_column(ForeignKey("TIPO_COMIDA.id"), nullable=False)
  tipo_comida: Mapped["TipoComida"] = relationship(back_populates="pedidos")

  usuario_id: Mapped[int] = mapped_column(ForeignKey("USUARIO.id"), nullable=False)
  usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")

  revisiones: Mapped[List["Revision"]] = relationship(back_populates="pedido")
  solicitudes_comida: Mapped[List["SolicitudComida"]] = relationship(back_populates="pedido")

  def __repr__(self):
    return f"<PEDIDO(id={self.id}, estado={self.estado})>"