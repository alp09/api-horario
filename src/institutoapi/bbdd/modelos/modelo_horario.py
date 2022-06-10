from sqlmodel import SQLModel, Field, Relationship

from institutoapi.bbdd.modelos import DiaSemana, TramoHorario, Asignatura, Profesor, Aula, Grupo


class HorarioRequest(SQLModel):

	# Columnas
	id_dia: int					= Field(foreign_key="dia_semana.id")
	id_tramo: int				= Field(foreign_key="tramo_horario.id")
	codigo_asignatura: str 		= Field(foreign_key="asignatura.codigo", max_length=20)
	codigo_profesor: str 		= Field(foreign_key="profesor.codigo", max_length=20)
	codigo_aula: str | None 	= Field(nullable=True, default=None, foreign_key="aula.codigo", max_length=20)
	codigo_grupo: str | None 	= Field(nullable=True, default=None, foreign_key="grupo.codigo", max_length=20)


class Horario(HorarioRequest, table=True):
	__tablename__ = "horario"

	# Columnas
	id: int = Field(primary_key=True)

	# Relaciones
	dia: DiaSemana 			= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	tramo: TramoHorario 	= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	asignatura: Asignatura 	= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	profesor: Profesor 		= Relationship(sa_relationship_kwargs={"lazy": "joined", "innerjoin": True})
	aula: Aula | None 		= Relationship(sa_relationship_kwargs={"lazy": "joined"})
	grupo: Grupo | None 	= Relationship(sa_relationship_kwargs={"lazy": "joined"})


class HorarioResponse(SQLModel):

	# Columnas
	id: int

	# Relaciones
	dia: DiaSemana
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula | None
	grupo: Grupo | None
