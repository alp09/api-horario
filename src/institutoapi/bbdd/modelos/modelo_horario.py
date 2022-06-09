from sqlmodel import SQLModel, Field, Relationship

from institutoapi.bbdd.modelos import DiaSemana, TramoHorario, Asignatura, Profesor, Aula, Grupo


class Horario(SQLModel, table=True):

	# Columnas
	id: int						= Field(primary_key=True)
	id_dia: int					= Field(foreign_key="dia_semana.id")
	id_tramo: int 				= Field(foreign_key="tramo_horario.id")
	codigo_asignatura: str 		= Field(foreign_key="asignatura.codigo")
	codigo_profesor: str 		= Field(foreign_key="profesor.codigo")
	codigo_aula: str | None 	= Field(nullable=True, default=None, foreign_key="aula.codigo")
	codigo_grupo: str | None 	= Field(nullable=True, default=None, foreign_key="grupo.codigo")

	# Relaciones
	dia: DiaSemana 				= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	tramo: TramoHorario 		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	asignatura: Asignatura 		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	profesor: Profesor 			= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	aula: Aula | None			= Relationship(sa_relationship_kwargs={"lazy": "joined"})
	grupo: Grupo | None			= Relationship(sa_relationship_kwargs={"lazy": "joined"})


class HorarioRequest(SQLModel):

	# Campos
	id_dia: int
	id_tramo: int
	codigo_asignatura: str 		= Field(max_length=20)
	codigo_profesor: str 		= Field(max_length=20)
	codigo_aula: str | None 	= Field(max_length=20)
	codigo_grupo: str | None 	= Field(max_length=20)


class HorarioResponse(SQLModel):

	# Campos
	id: int
	dia: DiaSemana
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula | None
	grupo: Grupo | None
