from pydantic import BaseModel, Field

from esquemas import DiaSemana, TramoHorario, Asignatura, Profesor, Aula, Grupo


class HorarioIn(BaseModel):
	id_dia: int
	id_tramo: int
	codigo_asignatura: str		= Field(max_length=20)
	codigo_profesor: str		= Field(max_length=20)
	codigo_aula: str | None		= Field(max_length=20)
	codigo_grupo: str | None	= Field(max_length=20)


class HorarioOut(BaseModel):
	id: int | None
	dia: DiaSemana
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula | None
	grupo: Grupo | None

	class Config:
		orm_mode = True
