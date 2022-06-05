import re
from fastapi import HTTPException
from starlette import status


class DatosInvalidosError(HTTPException):
	status_code = status.HTTP_409_CONFLICT

	def __init__(self, mensaje: str):
		self.detail = mensaje.split("\n")[0]


class IntegridadError(HTTPException):
	status_code = status.HTTP_409_CONFLICT

	def __init__(self, mensaje: str):
		mensaje_procesado = re.findall(r"\(.+?\)", mensaje)
		claves_extraidas = [re.sub("[()]", "", clave) for clave in mensaje_procesado]
		mensaje_final = f"Clave duplicada: {claves_extraidas[0].capitalize()} {claves_extraidas[1]} ya existe"
		self.detail = mensaje_final
