from enum import Enum

class TipoPersonalEnum(str, Enum):
  RESIDENTE = "Residente"
  FIJO = "Personal Fijo"

class TipoComidaEnum(str, Enum):
  DESAYUNO = "Desayuno"
  ALMUERZO = "Almuerzo"
  MERIENDA = "Merienda"
  CENA = "Cena"

class TipoMenuEnum(str, Enum):
  GENERAL = "General"
  VEGETARIANO = "Vegetariano"
  CELIACO = "Celiaco"

class RolEnum(str, Enum):
  ADMINISTRADOR = "Administrador"
  JEFE_SERVICIO = "Jefe de Servicio"
  SERVICIO_ALIMENTACION = "Servicio de Alimentación"
  SECTOR_COMEDOR = "Sector Comedor"


class PermisoEnum(str, Enum):
  USER_INDEX = "user_index"  # listar usuarios
  USER_NEW = "user_new"  # crear usuario
  USER_SHOW = "user_show"  # ver detalle de usuario
  USER_UPDATE = "user_update"  # actualizar usuario
  USER_DESTROY = "user_destroy"  # eliminar usuario