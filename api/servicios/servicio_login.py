from google_auth_oauthlib.flow import Flow		# Google ofrece una librería que facilita el flujo OAuth
from googleapiclient.discovery import build

from api.config import BASE_URL, path_archivo_google
from api.esquemas import Profesor
from api.servicios import servicio_profesor


# Los scopes son los distintos permisos que voy a solicitar
SCOPES = [
	"openid",
	"https://www.googleapis.com/auth/userinfo.profile",
	"https://www.googleapis.com/auth/userinfo.email"
]


def get_url_login() -> str:
	"""
	Recoge la URL del servidor de autorización con unos parámetros concretos

	:return: la URL del servidor de autorización
	"""

	# Crea el objeto Flow con la configuración adecuada
	cliente_api = Flow.from_client_secrets_file(
		path_archivo_google,
		redirect_uri=f"{BASE_URL}/login/callback",
		scopes=SCOPES
	)

	# Recoge la URL del servidor de autenticación
	return cliente_api.authorization_url(
		include_granted_scopes="true",
		access_type="offline"
	)


def get_datos_usuario(url_servidor_token: str, state: str) -> dict:
	"""
	A partir del token de autorización, consigo el token de acceso para recoger la información del usuario
	Esto lo hace construyendo un servicio y haciendo una petición GET a la API Oauth de Google

	:param url_servidor_token: la URL del servidor de autorización
	:param state: el estado generado durante el login. Usado para verificar que la petición se generó desde el mismo cliente
	:return: los datos del usuario que se ha iniciado sesión
	"""

	# Esta vez hay que añadirle el state a la configuración inicial para que lo valide
	cliente_api = Flow.from_client_secrets_file(
		path_archivo_google,
		redirect_uri=f"{BASE_URL}/login/callback",
		scopes=SCOPES,
		state=state
	)

	# [5] Usa el token enviado por el servidor de autenticación para
	# recoger el token de acceso [7] que usaré con los proveedores de recursos
	cliente_api.fetch_token(authorization_response=url_servidor_token)

	# Realizo una petición a la API de Google de oauth2, usando las credenciales que he conseguido
	with build("oauth2", "v2", credentials=cliente_api.credentials) as servicio_user_info:
		return servicio_user_info.userinfo().get().execute()


def validar_usuario_logeado(email: str) -> Profesor | None:
	"""
	Valida que el email del usuario que ha iniciado sesión
	es un usuario registrado en la base de datos

	:param email: el email del usuario que ha iniciado sesión
	:return: el profesor si se encontró o None si no existe
	"""
	return servicio_profesor.get_por_email(email)
