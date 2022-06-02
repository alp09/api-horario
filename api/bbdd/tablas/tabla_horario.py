from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Horario(Base):
	__tablename__ = "horario"

	# Columnas
	id					= Column(Integer, primary_key=True)
	id_dia				= Column(ForeignKey("dia_semana.id"))
	id_tramo			= Column(ForeignKey("tramo_horario.id"))
	codigo_asignatura	= Column(ForeignKey("asignatura.codigo"))
	codigo_profesor		= Column(ForeignKey("profesor.codigo"))
	codigo_aula			= Column(ForeignKey("aula.codigo"), nullable=True)
	codigo_grupo		= Column(ForeignKey("grupo.codigo"), nullable=True)

	# Relaciones
	dia 		= relationship("DiaSemana", 	lazy="selectin")
	tramo 		= relationship("TramoHorario", 	lazy="selectin")
	asignatura 	= relationship("Asignatura", 	lazy="selectin")
	profesor 	= relationship("Profesor", 		lazy="selectin")
	aula 		= relationship("Aula", 			lazy="selectin")
	grupo 		= relationship("Grupo", 		lazy="selectin")
