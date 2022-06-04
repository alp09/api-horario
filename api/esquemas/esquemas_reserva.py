from datetime import date
from pydantic import BaseModel, Field, validator

from esquemas import TramoHorario, Asignatura, Profesor, Aula, Grupo


class ReservaIn(BaseModel):
	id: int | None
	fecha: date
	id_tramo: int
	codigo_asignatura: str		= Field(max_length=20)
	codigo_profesor: str		= Field(max_length=20)
	codigo_aula: str | None		= Field(max_length=20)
	codigo_grupo: str | None	= Field(max_length=20)

	@validator("fecha")
	def validar_fecha_no_esta_en_pasado(cls, fecha):
		assert not fecha < date.today(), "La fecha de la reserva no puede estar en el pasado"
		return fecha

	@validator("fecha")
	def validar_fecha_no_este_fin_de_semana(cls, fecha):
		# isoweekday() devuelve el día de la semana, siendo el lunes = 1 y el domingo = 7
		assert fecha.isoweekday() < 6, "No se puede hacer una reserva los fines de semana"
		return fecha


class ReservaOut(BaseModel):
	id: int | None
	fecha: date
	tramo: TramoHorario
	asignatura: Asignatura
	profesor: Profesor
	aula: Aula | None
	grupo: Grupo | None

	class Config:
		orm_mode = True
