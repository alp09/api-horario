from fastapi import HTTPException
from starlette import status


class EmailProfesorNoEncontradoError(HTTPException):

	def __init__(self, email_profesor: str):
		self.status_code = status.HTTP_404_NOT_FOUND
		self.detail = f"El email {email_profesor} no pertenece a ningún profesor registrado"
