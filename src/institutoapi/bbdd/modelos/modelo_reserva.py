from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from institutoapi.bbdd.modelos import TramoHorario, Asignatura, Profesor, Aula, Grupo


class Reserva(SQLModel, table=True):
	__tablename__ = "reserva"

	# Columnas
	id: int					= Field(primary_key=True)
	fecha: date				= Field()
	id_tramo: int			= Field(foreign_key="tramo_horario.id")
	codigo_asignatura: str	= Field(foreign_key="asignatura.codigo")
	codigo_profesor: str	= Field(foreign_key="profesor.codigo")
	codigo_aula: str		= Field(nullable=True, default=None, foreign_key="aula.codigo")
	codigo_grupo: str		= Field(nullable=True, default=None, foreign_key="grupo.codigo")

	# Relaciones
	tramo: TramoHorario 	= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	asignatura: Asignatura 	= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	profesor: Profesor 		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	aula: Aula 				= Relationship(sa_relationship_kwargs={"lazy": "joined"})
	grupo: Grupo 			= Relationship(sa_relationship_kwargs={"lazy": "joined"})


class ReservaRequest(SQLModel):

	# Campos
	fecha: date
	id_tramo: int
	codigo_asignatura: str	= Field(max_length=20)
	codigo_profesor: str	= Field(max_length=20)
	codigo_aula: str		= Field(max_length=20)
	codigo_grupo: str		= Field(max_length=20)


class ReservaResponse(SQLModel):

	# Campos
	id: int
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula
	grupo: Grupo
