from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey

class RegistroCupo(Base):
  __tablename__ = "REGISTRO_CUPO"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  estado: Mapped[str] = mapped_column(nullable=False)
  fecha: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc)
  )

  cupo_id: Mapped[int] = mapped_column(ForeignKey("CUPO.id"), nullable=False)
  cupo: Mapped["Cupo"] = relationship(back_populates="registros_cupo")

  solicitud_comida_id: Mapped[int] = mapped_column(ForeignKey("SOLICITUD_COMIDA.id"), nullable=False, unique=True)
  solicitud_comida: Mapped["SolicitudComida"] = relationship(back_populates="registro_cupo")

  def __repr__(self):
    return f"<REGISTRO_CUPO(id={self.id}, estado={self.estado})>"