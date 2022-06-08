from fastapi import HTTPException
from starlette import status


class UsuarioNoRegistradoError(HTTPException):
	status_code = status.HTTP_401_UNAUTHORIZED

	def __init__(self, email):
		self.detail = f"El email {email} no está registrado en la organización"


class UsuarioNoLogeado(HTTPException):
	status_code = status.HTTP_401_UNAUTHORIZED

	def __init__(self):
		self.detail  = "Es necesario estar logeado para acceder al sitio"


class SesionCaducadaError(HTTPException):
	status_code = status.HTTP_401_UNAUTHORIZED

	def __init__(self):
		self.detail  = "La sesión ha caducado"


class PermisosInsuficientesError(HTTPException):
	status_code = status.HTTP_403_FORBIDDEN

	def __init__(self, mensaje=None):
		self.detail = mensaje or f"Se requiren permisos de administrador para realizar esa acción"
