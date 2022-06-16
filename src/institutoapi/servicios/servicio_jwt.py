import jwt
from datetime import datetime, timedelta

from institutoapi.modelos import Profesor
from institutoapi.config import ApiConfig as Cfg
from institutoapi.excepciones.auth import UsuarioNoLogeado, SesionCaducadaError


def generar_jwt_token(profesor_logeado: Profesor) -> str:
	"""
	Genera un token con la información del usuario y un tiempo de caducidad de 30 minutos

	:param profesor_logeado: los datos del profesor que se quieren guardar en el payload
	:return: el token jwt como string
	"""
	payload = {
		"sub": profesor_logeado.codigo,
		"exp": datetime.now() + timedelta(minutes=Cfg.token_expire)
	}

	jwt_token = jwt.encode(payload, Cfg.secret_key, Cfg.algoritmo)
	return jwt_token


def decodificar_jwt_token(jwt_token: str) -> dict:
	"""
	Decodifica el JWT token

	:param jwt_token: el token que se va a decodificar
	:raises UsuarioNoLogeado: si ocurre algún error durante la decodificación del token
	:raises SesionCaducadaError: si el token ha caducado
	:return: el payload del token
	"""

	# Intenta decodificar el token JWT
	try:
		payload = jwt.decode(jwt_token, Cfg.secret_key, Cfg.algoritmo)

	# Si da un error, envía una Excepción personalizada
	except jwt.ExpiredSignatureError:
		raise SesionCaducadaError

	# Si es una excepción distinta a las anteriores, devuelvo un error genérico
	except jwt.PyJWTError:
		raise UsuarioNoLogeado

	# Si no hubo errores, devuelvo el payload
	else:
		return payload
