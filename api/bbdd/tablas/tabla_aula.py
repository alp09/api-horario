from sqlalchemy import Column, String

from ..bbdd import Base


class Aula(Base):
	__tablename__ = "aula"

	# Columnas
	codigo 		= Column(String(20), primary_key=True)
	descripcion = Column(String(255))
