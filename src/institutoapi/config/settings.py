import os


class ApiConfig:
	# API
	base_url = "api_base_url"

	# Google client
	client_secret_file = os.path.join(os.getcwd(), os.path.dirname(__file__), "client_secret.json")

	# JWT
	algoritmo = "encripcion"
	secret_key = "super-secret-key"

	# BASE DATOS
	username = "db-user"
	password = "db-password"
	host 	 = "db-ip"
	port 	 = "db-port"
	database = "db-name"
