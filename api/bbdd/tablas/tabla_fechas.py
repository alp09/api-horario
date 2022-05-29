from sqlalchemy import Column, Date, String, text
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Fecha(Base):
	__tablename__ = "fecha"

	# Columnas
	fecha 		= Column(Date, primary_key=True)

	# Relaciones
	reservas 	= relationship("Reserva", back_populates="fecha", lazy="noload")
