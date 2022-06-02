from sqlalchemy import Column, String

from ..bbdd import Base


class Grupo(Base):
	__tablename__ = "grupo"

	# Columnas
	codigo 		= Column(String(20), primary_key=True)
	descripcion = Column(String(255))
