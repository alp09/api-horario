from datetime import date

from pydantic import validator
from sqlmodel import SQLModel, Field, Relationship

from institutoapi.modelos import TramoHorario, Asignatura, Profesor, Aula, Grupo


class ReservaRequest(SQLModel):

	# Columnas
	fecha: date				= Field()
	id_tramo: int			= Field(foreign_key="tramo_horario.id")
	codigo_asignatura: str	= Field(foreign_key="asignatura.codigo", max_length=20)
	codigo_profesor: str	= Field(foreign_key="profesor.codigo", max_length=20)
	codigo_aula: str		= Field(nullable=True, default=None, foreign_key="aula.codigo", max_length=20)
	codigo_grupo: str		= Field(nullable=True, default=None, foreign_key="grupo.codigo", max_length=20)

	@validator("fecha")
	def validar_fecha_no_esta_en_pasado(cls, fecha):
		assert not fecha < date.today(), "La fecha de la reserva no puede estar en el pasado"
		return fecha

	@validator("fecha")
	def validar_fecha_no_este_fin_de_semana(cls, fecha):
		# isoweekday() devuelve el día de la semana, siendo el lunes = 1 y el domingo = 7
		assert fecha.isoweekday() < 6, "No se puede hacer una reserva los fines de semana"
		return fecha


class Reserva(ReservaRequest, table=True):
	__tablename__ = "reserva"

	# Columnas
	id: int					= Field(primary_key=True)

	# Relaciones
	tramo: TramoHorario		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	asignatura: Asignatura	= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	profesor: Profesor		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	aula: Aula				= Relationship(sa_relationship_kwargs={"lazy": "joined"})
	grupo: Grupo			= Relationship(sa_relationship_kwargs={"lazy": "joined"})


class ReservaResponse(SQLModel):

	# Columnas
	id: int

	# Relaciones
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula
	grupo: Grupo
