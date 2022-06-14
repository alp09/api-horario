from fastapi import HTTPException, status


class UsuarioNoRegistradoError(HTTPException):

	def __init__(self, email):
		self.status_code = status.HTTP_401_UNAUTHORIZED
		self.detail = f"El email {email} no está registrado en la organización"


class UsuarioNoLogeado(HTTPException):

	def __init__(self):
		self.status_code = status.HTTP_401_UNAUTHORIZED
		self.detail  = "Es necesario estar logeado para acceder al sitio"


class SesionCaducadaError(HTTPException):

	def __init__(self):
		self.status_code = 419 	# Login timeout - No es estándar
		self.detail  = "La sesión ha caducado"


class PermisosInsuficientesError(HTTPException):

	def __init__(self, mensaje=None):
		self.status_code = status.HTTP_403_FORBIDDEN
		self.detail = mensaje or f"Se requiren permisos de administrador para realizar esa acción"
