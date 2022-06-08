import os
from configparser import ConfigParser

path_root = os.getcwd()
path_carpeta_archivos = os.path.join(path_root, os.path.dirname(__file__), "archivos")

# Archivo configuración de la app
archivo_settings = "settings.cfg"
path_archivo_settings = os.path.join(path_carpeta_archivos, archivo_settings)

# Archivo configuración cliente Google
archivo_google = "client_secret.json"
path_archivo_google = os.path.join(path_carpeta_archivos, archivo_google)

# Lee los archivos para extraer los valores
configparser = ConfigParser()
configparser.read(path_archivo_settings)

# [APP]
BASE_URL	= configparser.get("APP", "base_url")
SECRET_KEY	= configparser.get("APP", "secret_key")

# [JWT]
ALGORITMO 	= configparser.get("JWT", "algoritmo")

# [DATABASE]
DB_USERNAME = configparser.get("DATABASE", "username")
DB_PASSWORD = configparser.get("DATABASE", "password")
DB_HOST 	= configparser.get("DATABASE", "host")
DB_PORT 	= configparser.get("DATABASE", "port")
DB_DATABASE = configparser.get("DATABASE", "database")
