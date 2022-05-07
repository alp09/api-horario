from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Profesor(Base):
	__tablename__ = "profesor"

	# Columnas
	codigo 			= Column(String(20), primary_key=True)
	nombre_completo = Column(String(255))
	email			= Column(String(255), unique=True)
	es_admin		= Column(Boolean, default=False)

	# Relaciones
	# horario			= relationship("Horario")
