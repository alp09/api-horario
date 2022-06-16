import os


class ApiConfig:

	# [API]
	api_protocol = "http"
	api_host 	 = "localhost"
	api_port 	 = 8000
	api_url  	 = f"{api_protocol}://{api_host}:{api_port}"

	# [CLIENTE GOOGLE]
	# google_login_callback es la URL a la que Google redirigirá a los usuarios que finalicen el inicio de sesión
	# Esta URL se configura durante el registro del cliente de Google API. Tendrá que ser en el mismo
	google_login_callback = "/login/callback"

	# client_secret_file es el path al archivo client_secret generado durante el registro del cliente de Google API
	# Por defecto está configurado para que coloques el fichero en el mismo directorio que este archivo
	client_secret_file = os.path.join(os.getcwd(), os.path.dirname(__file__), "client_secret.json")

	# [TOKEN JWT]
	# secret_key es la clave secreta generada para la aplicación
	secret_key = "secret_key"

	# algoritmo usado para firmar el token
	algoritmo = "HS256"

	# token_expire indica el tiempo de validez del token en minutos
	token_expire = 30

	# [BASE DE DATOS]
	# Sintaxis - dialect+driver://username:password@host:port/database
	# Ejemplo  - postgresql+psycopg2://postgres:postgres@localhost:5432/mydatabase
	db_url = "dialect+driver://username:password@host:port/database"

	# [Front End]
	# Lista los orígenes que tendrán permitidos hacer peticiones cross-origin (como una aplicación que consuma la API)
	origins = ["http://localhost:3000"]
