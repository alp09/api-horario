from fastapi import HTTPException, status


class IntegridadDatosError(HTTPException):

	def __init__(self, mensaje: str):
		self.status_code = status.HTTP_409_CONFLICT
		self.detail = mensaje
