from sqlalchemy import Column, Date
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Fecha(Base):
	__tablename__ = "fecha"

	# Columnas
	fecha = Column(Date, primary_key=True)

	# Relaciones
	reservas = relationship("Reserva", lazy="select")
