from pydantic import BaseModel

from esquemas import DiaSemana, TramoHorario, Asignatura, Profesor, Aula, Grupo


class Horario(BaseModel):
	id: int | None

	dia: DiaSemana
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula | None
	grupo: Grupo | None

	class Config:
		orm_mode = True
