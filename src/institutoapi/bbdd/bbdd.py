from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.future import Engine

from institutoapi.bbdd.utils import triggers


_engine: Engine


def inicializar_conexion(*, username, password, host, port, database, **kwargs) -> None:
	""" Inicializa la base de datos. """

	# Genera el engine
	global _engine
	_engine = create_engine(url=f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}", **kwargs)

	# Prepara los listener para rellenar los datos de la tabla dia_semana y tramo_horario
	triggers.generar_datos_tablas()

	# Genera las modelos de la BBDD si no existen
	SQLModel.metadata.create_all(bind=_engine)


def finalizar_conexion():
	""" Una vez se deja de usar el engine, se elimina """
	_engine.dispose()


def get_sesion() -> Session | None:
	"""
	Genera un objeto Session. Una vez se deja de usar, se ‘cierra’ la Session y se devuelve al Pool de conexión
	A diferencia de una Connection, estás permiten trabajar con objetos ORM (y otras muchas cosas...)
	"""
	if _engine is not None:
		with Session(bind=_engine) as sesion:
			yield sesion
