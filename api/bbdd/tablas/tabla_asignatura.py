from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Asignatura(Base):
	__tablename__ = "asignatura"

	# Columnas
	codigo 		= Column(String(20), primary_key=True)
	descripcion = Column(String(255))

	# Relaciones
	horario 	= relationship("Horario", back_populates="asignatura", lazy="noload")
