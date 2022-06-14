from fastapi import HTTPException, status


class DatosInvalidosError(HTTPException):

	def __init__(self, mensaje: str):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = mensaje.split("\n")[0]


class IntegridadDatosError(HTTPException):

	def __init__(self, mensaje: str):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = mensaje
