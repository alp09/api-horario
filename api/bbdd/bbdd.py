from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from api.config import path_archivo_settings

# Base usada para crear los modelos de tablas
Base = declarative_base()

# Variable que contiene el Engine de SQLAlchemy
engine: Engine

# Variable que contiene la sesión (para usar SQLAlchemy ORM)
Sessionmaker: sessionmaker


def inicializar_conexion():
	""" Inicializa la base de datos. """

	def generar_engine() -> Engine:
		"""
		Crea el objecto Engine que gestiona la conexión con la BBDD

		:return: devuelve el objeto Engine
		"""
		# Crea el configparser
		configparser = ConfigParser()
		configparser.read(path_archivo_settings)

		# Lee las variables necesarias
		username = configparser.get("DATABASE", "username")
		password = configparser.get("DATABASE", "password")
		host 	 = configparser.get("DATABASE", "host")
		port 	 = configparser.get("DATABASE", "port")
		database = configparser.get("DATABASE", "database")

		return create_engine(
			url=f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}",
			pool_size=5,
			max_overflow=10,
			future=True,
			echo=True
		)

	global engine, Sessionmaker
	engine = generar_engine()
	Sessionmaker = sessionmaker(bind=engine, future=True)


def cerrar_conexion():
	""" Cierra la conexión con la base de datos. """
	engine.dispose()


def get_conexion() -> Connection:
	""" Devuelve una conexión del Pool de conexiones del Engine """
	if engine is not None:
		return engine.connect()


def get_transaccion() -> Connection:
	""" Devuelve una conexión con una transacción iniciada """
	if engine is not None:
		return engine.begin()


def get_sesion() -> Session:
	""" Devuelve una sesión que controla la persistencia de objectos ORM """
	if Sessionmaker is not None:
		return Sessionmaker()
