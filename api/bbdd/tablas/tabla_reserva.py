from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Reserva(Base):
	__tablename__ = "reserva"

	# Columnas
	id					= Column(Integer, primary_key=True)
	id_fecha			= Column(ForeignKey("fecha.fecha"))
	id_tramo			= Column(ForeignKey("tramo_horario.id"))
	codigo_asignatura	= Column(ForeignKey("asignatura.codigo"))
	codigo_profesor		= Column(ForeignKey("profesor.codigo"))
	codigo_aula			= Column(ForeignKey("aula.codigo"), nullable=True)
	codigo_grupo		= Column(ForeignKey("grupo.codigo"), nullable=True)

	# Relaciones
	fecha		= relationship("Fecha",			lazy="selectin", backref="reservas")
	tramo 		= relationship("TramoHorario", 	lazy="selectin")
	asignatura 	= relationship("Asignatura", 	lazy="selectin")
	profesor 	= relationship("Profesor", 		lazy="selectin")
	aula 		= relationship("Aula", 			lazy="selectin")
	grupo 		= relationship("Grupo", 		lazy="selectin")
