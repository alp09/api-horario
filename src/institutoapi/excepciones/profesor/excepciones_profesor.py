from fastapi import HTTPException
from starlette import status


class EmailProfesorNoEncontradoError(HTTPException):
	status_code = status.HTTP_404_NOT_FOUND

	def __init__(self, email_profesor: str):
		self.detail = f"El email {email_profesor} no pertenece a ningún profesor registrado"
