import os


class ApiConfig:

	# [API]
	api_host 	 = "localhost"
	api_port 	 = 8000
	api_base_url = f"http://{api_host}:{api_port}"

	# [Cliente Google]
	client_secret_file 	  = os.path.join(os.getcwd(), os.path.dirname(__file__), "client_secret.json")
	google_login_callback = "/login/callback"

	# [Tokens JWT]
	secret_key 		= "secret_key"
	algoritmo 		= "HS256" 	# Algoritmo válido para PyJWT
	token_expire 	= 30 		# Minutos hasta que el token JWT caduca

	# [Base de datos]
	# Sintaxis - dialect+driver://username:password@host:port/database
	db_url = "dialect+driver://username:password@host:port/database"

	# EJEMPLOS:
	# psycopg2 			 - postgresql+psycopg2://db_username:db_password@db_host:db_port/db_database
	# mysqlclient 		 - mysql+mysqldb://db_username:db_password@db_host:db_port/db_database
