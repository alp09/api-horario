from fastapi import HTTPException
from starlette import status


class DatosInvalidosError(HTTPException):

	def __init__(self, mensaje: str):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = mensaje.split("\n")[0]


class IntegridadError(HTTPException):

	def __init__(self, mensaje: str):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = mensaje
