from fastapi import HTTPException
from starlette import status


class DatosInvalidosError(HTTPException):
	status_code = status.HTTP_409_CONFLICT

	def __init__(self, mensaje: str):
		self.detail = mensaje.split("\n")[0]


class IntegridadError(HTTPException):
	status_code = status.HTTP_409_CONFLICT

	def __init__(self, mensaje: str):
		self.detail  = mensaje
