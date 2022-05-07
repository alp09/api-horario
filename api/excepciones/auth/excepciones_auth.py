from fastapi import HTTPException
from starlette import status


class UsuarioNoRegistradoError(HTTPException):
	status_code = status.HTTP_401_UNAUTHORIZED

	def __init__(self, email):
		self.detail = f"Tu e-mail {email} estás registrado en la organización"
