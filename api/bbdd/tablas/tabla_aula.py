from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Aula(Base):
	__tablename__ = "aula"

	# Columnas
	codigo 		= Column(String(20), primary_key=True)
	descripcion = Column(String(255))

	# Relaciones
	horarios 	= relationship("Horario", back_populates="aula", lazy="noload")
	reservas	= relationship("Reserva", back_populates="aula", lazy="noload")

