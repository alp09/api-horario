from fastapi import HTTPException
from starlette import status


class SinRegistros(HTTPException):
	status_code = status.HTTP_204_NO_CONTENT

	def __init__(self):
		self.detail = "No se encontraron registros"


class CodigoNoEncontrado(HTTPException):
	status_code = status.HTTP_404_NOT_FOUND

	def __init__(self, codigo):
		self.detail = f"No hay ningún registro con el código {codigo}"
