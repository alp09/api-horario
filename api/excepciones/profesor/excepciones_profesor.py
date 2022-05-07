from fastapi import HTTPException
from starlette import status


class NoProfesoresEncontradosError(HTTPException):
	status_code = status.HTTP_404_NOT_FOUND

	def __init__(self):
		self.detail = "No se encontraron profesores"


class CodigoProfesorNoEncontradoError(HTTPException):
	status_code = status.HTTP_404_NOT_FOUND

	def __init__(self, id_profesor):
		self.detail = f"No hay ningún profesor registrado con el código {id_profesor}"


class EmailProfesorNoEncontradoError(HTTPException):
	status_code = status.HTTP_404_NOT_FOUND

	def __init__(self, email_profesor: str):
		self.detail = f"El email {email_profesor} no pertenece a ningún profesor registrado"
