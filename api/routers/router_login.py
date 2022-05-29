"""
Oauth es un protocolo estándar de autorización que permite a una aplicación "acceso seguro designado".
En este caso estaría permitiendo el acceso a mi API a los datos del usuario de Google sin necesidad
de recibir las credenciales del usuario. Esto lo hace mediante tokens de autorización.

Cada proveedor tiene su propia implementación por lo que puede que estos pasos varíen un poco.
Los pasos a seguir para implementar el login con Google son:

1. Primero hay que registrar la aplicación de terceros (mi API) como cliente del servidor de autenticación.
	- Al hacerlo recibo unas credenciales únicas del servidor de autenticación (definidas en el archivo client_secret.json).
	- Estas credenciales las usaré después para demostrar quien soy al proveedor.

2. El cliente envía una petición al servidor de autenticación (la pantalla de login de Google).

3. El servidor de autenticación pregunta al usuario que se autentique (su correo y contraseña).

4. El servidor de autenticación pide permiso al usuario para autorizar a mi API:
	- Aquí se detalla que información del usuario se quiere acceder (los scopes que están más abajo)
	- Esto es igual que cuando una app del móvil te pide permiso para utilizar alguna parte de tu dispositivo.

5. El servidor de autenticación envía al cliente un token de autenticación único

6. El cliente envía este token de autorización de nuevo al servidor de autenticación.

7. El proveedor envía al cliente un token de acceso que le permite interactuar con otros proveedores en nombre del usuario.
	- En este caso me sirve para pedirle a la API de Google los datos del usuario

"""


from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from api.excepciones.auth import UsuarioNoRegistradoError
from api.servicios import servicio_login, servicio_jwt

# Definición del router
router = APIRouter(tags=["login"])


@router.get("/login")
def login(request: Request) -> RedirectResponse:

	# Recoge la URL del servidor de autorización
	url_login, state = servicio_login.get_url_login()

	# Guarda el estado para verificarlo más tarde
	request.session["state"] = state

	# Redirige a la URL recogida. Allí el usuario iniciará sesión con Google
	return RedirectResponse(url_login)


@router.get("/login/callback")
def login_callback(request: Request) -> str:

	# Recoge las variables necesarias para el objeto Flow
	url_servidor_autorizacion = request.url.__str__()
	state = request.session.get("state", None)

	# Recoge los datos del usuario que ha iniciado sesión
	datos_usuario = servicio_login.get_datos_usuario(url_servidor_autorizacion, state)
	email_usuario = datos_usuario["email"]

	# Valida que el usuario está registrado en la base de datos
	profesor = servicio_login.validar_usuario_logeado(email_usuario)

	# Si no lo está, devuelve una excepción Unauthorized.
	if profesor is None:
		raise UsuarioNoRegistradoError(email=email_usuario)

	# Si lo está genera el JWT token con los datos del usuario registrado
	dict_profesor = dict(profesor)
	return servicio_jwt.generar_jwt_token(dict_profesor)
