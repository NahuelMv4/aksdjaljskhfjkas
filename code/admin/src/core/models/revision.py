from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey

class Revision(Base):
  __tablename__ = "REVISION"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  estado: Mapped[str] = mapped_column(nullable=False)
  revisado_en: Mapped[datetime] = mapped_column(
    DateTime, default=lambda: datetime.now(timezone.utc)
  )
  observacion: Mapped[str] = mapped_column(nullable=True)

  usuario_id: Mapped[int] = mapped_column(ForeignKey("USUARIO.id"), nullable=False)
  usuario: Mapped["Usuario"] = relationship(back_populates="revisiones")

  pedido_id: Mapped[int] = mapped_column(ForeignKey("PEDIDO.id"), nullable=False)
  pedido: Mapped["Pedido"] = relationship(back_populates="revisiones")

  def __repr__(self):
    return f"<REVISION(id={self.id}, estado={self.estado})>"