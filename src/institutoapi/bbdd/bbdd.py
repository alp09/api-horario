from sqlalchemy import create_engine
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker


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
		from institutoapi.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE

		return create_engine(
			url=f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}",
			pool_size=5,
			max_overflow=10,
			future=True
		)

	def crear_tablas_y_triggers() -> None:
		""" Crea las tablas, funciones, triggers de la BBDD y datos iniciales """
		from institutoapi.bbdd.utils import functions, triggers

		# Prepara los listeners para que al crear las tablas se adjunten los triggers
		functions.generar_funciones()
		functions.generar_funciones_trigger()
		triggers.generar_triggers()

		# Prepara los listener para rellenar los datos de la tabla dia_semana y tramo_horario
		triggers.generar_datos_tablas()

		# Genera las tablas de la BBDD si no existen
		Base.metadata.create_all(bind=engine)

	global engine, Sessionmaker

	# Genera el engine
	engine = generar_engine()

	# Genera el session factory
	Sessionmaker = sessionmaker(bind=engine, future=True, expire_on_commit=False)

	# Ejecuta el código necesario para generar lo relacionado con la BBDD
	crear_tablas_y_triggers()


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
