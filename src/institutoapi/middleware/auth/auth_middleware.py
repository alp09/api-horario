import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError

from institutoapi.config import ApiConfig as Cfg
from institutoapi.bbdd.modelos import Profesor
from institutoapi.excepciones.auth import UsuarioNoLogeado, PermisosInsuficientesError, SesionCaducadaError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def validar_profesor_logeado(jwt_token: str = Depends(oauth2_scheme)) -> Profesor:
	"""
	La dependencia de oauth2_scheme comprueba que en HEADER de la petición HTTP se encuentre
	un token en la clave Authorization. De ser así lo asigna al parámetro jwt_token.

	Valida que el token JWT sea válido. Para que un token JWT sea válido, se debe de poder decodificar con
	la misma clave secreta y algoritmo. Una vez decodificado, revisa que no esté caducado.

	:param jwt_token: el token JWT que se va a validar
	:raises UsuarioNoLogeado: si ocurre algún error durante la decodificación del token
	:raises SesionCaducadaError: si el token ha caducado
	:return: los datos del profesor que ha iniciado sesión
	"""

	# Intenta decodificar el token JWT
	try:
		payload = jwt.decode(jwt_token, Cfg.secret_key, Cfg.algoritmo)

	# Si da un error, envía una Excepción personalizada
	except DecodeError:
		raise UsuarioNoLogeado
	except ExpiredSignatureError:
		raise SesionCaducadaError

	return Profesor(**payload)


async def validar_profesor_es_admin(profesor_logeado: Profesor = Depends(validar_profesor_logeado)) -> Profesor:
	"""
	Valida que el profesor que ha iniciado sesión tiene permisos de administrador.
	Estos datos se guardan en el payload del token JWT, de ahí la dependencia con la función validar_profesor_logeado.

	:param profesor_logeado: los datos del profesor que ha iniciado sesión
	:raises PermisosInsuficientesError: si el profesor no tiene permisos de administrador
	"""
	if not profesor_logeado.es_admin:
		raise PermisosInsuficientesError
	return profesor_logeado
