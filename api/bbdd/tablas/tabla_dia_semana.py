from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..bbdd import Base


class DiaSemana(Base):
	__tablename__ = "dia_semana"

	# Columnas
	id	 		= Column(Integer, primary_key=True)
	descripcion = Column(String(20))

	# Relaciones
	horario 	= relationship("Horario", back_populates="dia", lazy="noload")
