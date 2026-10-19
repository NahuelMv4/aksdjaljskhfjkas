from src.core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey
from typing import Optional


class ConfiguracionSistema(Base):
  __tablename__ = "CONFIGURACION_SISTEMA"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  clave: Mapped[str] = mapped_column(unique=True, nullable=False)
  paginacion: Mapped[int] = mapped_column(nullable=False)
  mantenimiento: Mapped[bool] = mapped_column(default=False, nullable=False)
  mensaje_mantenimiento: Mapped[str] = mapped_column(nullable=True)
  actualizado_en: Mapped[datetime] = mapped_column(
    DateTime, 
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
  )
  
  actualizado_por_usuario_id: Mapped[Optional[int]] = mapped_column(ForeignKey("USUARIO.id"), nullable=True)
  actualizado_por_usuario: Mapped[Optional["Usuario"]] = relationship()