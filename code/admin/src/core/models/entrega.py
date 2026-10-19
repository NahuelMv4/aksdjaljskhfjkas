from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base
from typing import List


class Entrega(Base):
    __tablename__ = "ENTREGA"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    personal_id: Mapped[int] = mapped_column(ForeignKey("PERSONAL.id"), nullable=False)
    personal: Mapped["Personal"] = relationship(back_populates="entregas")

    solicitudes: Mapped[List["SolicitudComida"]] = relationship(back_populates="entrega")

    def __repr__(self):
        return f"<ENTREGA(id={self.id}, fecha={self.fecha})>"