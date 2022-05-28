from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, InternalError

from api.bbdd import get_conexion, get_transaccion, get_sesion
from api.bbdd.tablas import Horario
from api.excepciones.bbdd import IntegridadError, DatosInvalidosError


def seleccionar_todos():
	sql = select(Horario)

	with get_sesion() as sesion:
		return sesion.scalars(sql).all()


def insertar(datos_horarios: list[dict]) -> list[Horario]:
	"""
	Inserta un registro en la tabla de Horario por cada diccionario de datos

	:param datos_horarios: los datos de los nuevos horarios
	:return: los datos de los horarios intertados
	"""
	sql = (
		insert(Horario)
		.values(datos_horarios)
		.returning(Horario)
	)

	try:
		with get_transaccion() as transaccion:
			return transaccion.execute(sql).all()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_horario: int, datos_horario: dict) -> Horario:
	"""
	Actualiza los datos del horario con codigo_horario con el resto de datos del diccionario datos_horario

	:param codigo_horario: el codigo del horario que voy a actualizar
	:param datos_horario: los datos acutalizados del horario
	:raises IntegridadError: en caso de que se viole la integridad de alguna clave
	:raises DatosInvalidosError: en caso de que los datos del horario actualizado no sean válidos
	:return: los datos del horario actualizado
	"""
	sql = (
		update(Horario)
		.where(Horario.id == codigo_horario)
		.values(datos_horario)
		.returning(Horario)
	)

	try:
		with get_conexion() as conexion:
			return conexion.execute(sql).one_or_none()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def borrar(id_horarios: list[int]) -> list[Horario]:
	"""
	Elimina los registros de la tabla Horario cuyo id se encuentre en la lista id_horarios

	:param id_horarios: los ID de los horarios que se quieren eliminar
	:return: los horarios eliminados
	"""
	sql = (
		delete(Horario)
		.where(Horario.id.in_(id_horarios))
		.returning(Horario)
	)

	with get_conexion() as conexion:
		return conexion.execute(sql).all()
