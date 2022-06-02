from sqlalchemy import Column, Integer, String

from ..bbdd import Base


class DiaSemana(Base):
	__tablename__ = "dia_semana"

	# Columnas
	id	 		= Column(Integer, primary_key=True)
	descripcion = Column(String(20))
