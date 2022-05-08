from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Grupo(Base):
	__tablename__ = "grupo"

	# Columnas
	codigo 		= Column(String(20), primary_key=True)
	descripcion = Column(String(255))

	# Relaciones
	horario 	= relationship("Horario")
