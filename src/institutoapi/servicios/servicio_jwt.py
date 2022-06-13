import jwt
from datetime import datetime, timedelta

from institutoapi.config import ApiConfig as Cfg


def generar_jwt_token(datos: dict) -> str:
	"""
	Genera un token con la información del usuario y un tiempo de caducidad de 30 minutos

	:param datos: los datos que se quieren guardar en el payload
	:return: el token jwt como string
	"""
	payload = datos.copy()
	payload.update({"exp": datetime.now() + timedelta(minutes=30)})

	jwt_token = jwt.encode(payload, Cfg.secret_key, Cfg.algoritmo)
	return jwt_token


def decodificar_jwt_token(token: str) -> dict:
	"""
	Decodifica el JWT token

	:param token: el token que se va a decodificar
	:return: el payload del token
	"""
	payload = jwt.decode(token, Cfg.secret_key, Cfg.algoritmo)
	return payload
