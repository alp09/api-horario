from fastapi import HTTPException, status


class EmailNoEncontradoError(HTTPException):

	def __init__(self, email_profesor: str):
		self.status_code = status.HTTP_404_NOT_FOUND
		self.detail = f"El email {email_profesor} no pertenece a ningún profesor registrado"
