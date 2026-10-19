from src.core.enums import TipoComidaEnum
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import Enum as SQLEnum

class TipoComida(Base):
  __tablename__ = "TIPO_COMIDA"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nombre: Mapped[TipoComidaEnum] = mapped_column(
    SQLEnum(
      TipoComidaEnum,
      values_callable=lambda x: [e.value for e in x],
      native_enum=False
    ),
    unique=True,
    nullable=False
  )

  cupos: Mapped[List["Cupo"]] = relationship(back_populates="tipo_comida")
  pedidos: Mapped[List["Pedido"]] = relationship(back_populates="tipo_comida")

  def __repr__(self):
    return f"<TIPO_COMIDA(id={self.id}, nombre={self.nombre})>"