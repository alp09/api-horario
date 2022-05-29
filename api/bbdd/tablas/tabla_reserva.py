from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..bbdd import Base


class Reserva(Base):
	__tablename__ = "reserva"

	# Columnas
	id					= Column(Integer, primary_key=True)
	id_fecha 			= Column(ForeignKey("fecha.fecha"))
	id_tramo			= Column(ForeignKey("tramo_horario.id"))
	codigo_asignatura	= Column(ForeignKey("asignatura.codigo"))
	codigo_profesor		= Column(ForeignKey("profesor.codigo"))
	codigo_aula			= Column(ForeignKey("aula.codigo"), nullable=True)
	codigo_grupo		= Column(ForeignKey("grupo.codigo"), nullable=True)

	# Relaciones
	fecha 		= relationship("Fecha", 		back_populates="reservas", lazy="joined")
	tramo 		= relationship("TramoHorario", 	back_populates="reservas", lazy="joined")
	asignatura 	= relationship("Asignatura", 	back_populates="reservas", lazy="joined")
	profesor 	= relationship("Profesor", 		back_populates="reservas", lazy="joined")
	aula 		= relationship("Aula", 			back_populates="reservas", lazy="joined")
	grupo 		= relationship("Grupo", 		back_populates="reservas", lazy="joined")
