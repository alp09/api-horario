from fastapi import HTTPException, status


class ProfesorImparteClasesEnOtraAula(HTTPException):

	def __init__(self, *, profesor: str, aula_nueva: str, aula_vieja: str, dia: int, tramo: int):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = f"El profesor {profesor} no puede impartir clases en {aula_nueva} porque ya tiene clases en {aula_vieja} el {dia} a {tramo}."


class SeImparteAsignaturaDistinta(HTTPException):

	def __init__(self, *, asignatura_nueva: str, asignatura_vieja: str, aula: str, dia: int, tramo: int):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = f"No se puede dar clases de {asignatura_nueva} en {aula} el {dia} a {tramo} porque ya se imparte {asignatura_vieja}."
