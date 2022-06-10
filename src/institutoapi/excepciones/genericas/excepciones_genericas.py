from fastapi import HTTPException
from starlette import status


class CodigoNoEncontrado(HTTPException):

	def __init__(self, codigos):
		self.status_code = status.HTTP_404_NOT_FOUND
		self.detail = f"No hay ningún registro con el ID: {codigos}"
