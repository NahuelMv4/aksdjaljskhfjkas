from src.core.enums import TipoMenuEnum
from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import Enum as SQLEnum

class TipoMenu(Base):
  __tablename__ = "TIPO_MENU"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  nombre: Mapped[TipoMenuEnum] = mapped_column(
      SQLEnum(
        TipoMenuEnum,
        values_callable=lambda x: [e.value for e in x],
        native_enum=False
      ),
      unique=True,
      nullable=False
    )

  lista_personal: Mapped[List["Personal"]] = relationship(back_populates="tipo_menu")
  solicitudes_comida: Mapped[List["SolicitudComida"]] = relationship(back_populates="tipo_menu")

  def __repr__(self):
    return f"<TIPO_MENU(id={self.id}, nombre={self.nombre})>"