from fastapi import HTTPException
from starlette import status


class IntegridadError(HTTPException):
	status_code = status.HTTP_409_CONFLICT

	def __init__(self, mensaje: str):
		self.detail  = mensaje
