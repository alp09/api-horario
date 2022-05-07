import configparser
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import create_engine, Engine, Connection


# Base usada para crear los modelos de tablas
Base = declarative_base()

# Variable que contiene el Engine de SQLAlchemy
engine: Engine


def inicializar_conexion():
	""" Inicializa la base de datos. """

	def generar_engine() -> Engine:
		"""
		Crea el objecto Engine que gestiona la conexión con la BBDD

		:return: devuelve el objeto Engine
		"""
		from api.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE

		return create_engine(
			url=f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}",
			pool_size=5,
			max_overflow=10
		)

	global engine
	engine = generar_engine()


def cerrar_conexion():
	""" Cierra la conexión con la base de datos. """
	engine.dispose()


def get_conexion() -> Connection:
	""" Devuelve una conexión del Pool de conexiones del Engine """
	if engine is not None:
		return engine.connect()


def get_transaccion() -> None:
	""" Devuelve una conexión con una transacción iniciada """
	if engine is not None:
		return engine.begin()
