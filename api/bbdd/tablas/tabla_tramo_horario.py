from sqlalchemy import Column, Integer, String, Time
from sqlalchemy.orm import relationship

from ..bbdd import Base


class TramoHorario(Base):
	__tablename__ = "tramo_horario"

	# Columnas
	id			= Column(Integer, primary_key=True)
	descripcion	= Column(String(50))
	hora_inicio	= Column(Time)
	hora_fin	= Column(Time)

	# Relaciones
	horarios 	= relationship("Horario", back_populates="tramo", lazy="noload")
	reservas 	= relationship("Reserva", back_populates="tramo", lazy="noload")
