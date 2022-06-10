from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.future import Engine


# Variable que contiene el Engine de SQLAlchemy
engine: Engine


def inicializar_conexion():
	""" Inicializa la base de datos. """

	def generar_engine() -> None:
		"""
		Crea el objecto Engine que gestiona la conexión con la BBDD

		:return: devuelve el objeto Engine
		"""
		from institutoapi.config import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE

		global engine
		engine = create_engine(
			url=f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}",
		)

	def crear_tablas_y_triggers() -> None:
		""" Crea las modelos, funciones, triggers de la BBDD y datos iniciales """
		from institutoapi.bbdd.utils import functions, triggers

		# Prepara los listeners para que al crear las modelos se adjunten los triggers
		functions.generar_funciones()
		functions.generar_funciones_trigger()
		triggers.generar_triggers()

		# Prepara los listener para rellenar los datos de la tabla dia_semana y tramo_horario
		triggers.generar_datos_tablas()

		# Genera las modelos de la BBDD si no existen
		SQLModel.metadata.create_all(bind=engine)

	# Genera el engine
	generar_engine()

	# Ejecuta el código necesario para generar lo relacionado con la BBDD
	crear_tablas_y_triggers()


def cerrar_conexion():
	""" Cierra la conexión con la base de datos. """
	engine.dispose()


def get_sesion() -> Session:
	""" Devuelve una sesión que controla la persistencia de objectos ORM """
	if engine is not None:
		sesion = Session(bind=engine)
		try:
			yield sesion
		finally:
			sesion.close()
