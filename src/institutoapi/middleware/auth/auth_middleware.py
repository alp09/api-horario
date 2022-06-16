from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.modelos import Profesor
from institutoapi.bbdd.dao import dao_profesor
from institutoapi.excepciones.auth import PermisosInsuficientesError, UsuarioNoLogeado
from institutoapi.servicios import servicio_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def validar_profesor_logeado(jwt_token: str = Depends(oauth2_scheme), sesion: Session = Depends(get_sesion)) -> Profesor:
	"""
	La dependencia de oauth2_scheme comprueba que en HEADER de la petición HTTP se encuentre
	un token en la clave Authorization. De ser así lo asigna al parámetro jwt_token.

	Valida que el token JWT sea válido. Para que un token JWT sea válido, se debe de poder decodificar con
	la misma clave secreta y algoritmo. Una vez decodificado, revisa que no esté caducado.

	:param jwt_token: el token JWT que se va a validar
	:param sesion: la sesión con la que se va a hacer la consulta a la BBDD
	:return: los datos del profesor que ha iniciado sesión
	"""
	payload = servicio_jwt.decodificar_jwt_token(jwt_token)

	codigo_profesor = payload.get("sub", None)
	if codigo_profesor is None:
		raise UsuarioNoLogeado

	profesor_logeado = dao_profesor.seleccionar_por_codigo(sesion, codigo_profesor)
	if profesor_logeado is None:
		raise UsuarioNoLogeado

	return profesor_logeado


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
