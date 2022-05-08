from sqlalchemy import select, insert, update, delete, bindparam
from sqlalchemy.exc import IntegrityError

from api.bbdd import get_conexion, get_transaccion
from api.bbdd.tablas import Asignatura
from api.excepciones.bbdd import IntegridadError


def seleccionar_todas() -> list[Asignatura]:
	"""
	Selecciona todas las asignaturas registradas

	:return: una lista de todas las asignaturas guardadas
	"""
	sql = select(Asignatura).order_by(Asignatura.codigo)

	with get_conexion() as conexion:
		return conexion.execute(sql).all()


def seleccionar_por_codigos(codigos_asignaturas: list[str]) -> list[Asignatura]:
	"""
	Selecciona todas las asignaturas cuyo código se encuentre en la lista codigos_asignaturas

	:param codigos_asignaturas: la lista de códigos de asignaturas que se quieren encontrar
	:return: una lista de todas las asignaturas encontradas
	"""
	sql = select(Asignatura).where(Asignatura.codigo.in_(codigos_asignaturas))

	with get_conexion() as conexion:
		return conexion.execute(sql).all()


def seleccionar_por_codigo(codigo_asignatura: str) -> Asignatura | None:
	"""
	Selecciona la asignatura cuyo código sea igual a codigo_asignatura

	:param codigo_asignatura: el código de la asignatura que se busca
	:return: la asignatura si se encuentra o None si ninguna asignatura tiene asignado ese código
	"""
	sql = select(Asignatura).where(Asignatura.codigo == codigo_asignatura)

	with get_conexion() as conexion:
		return conexion.execute(sql).one_or_none()


def insertar(datos_asignaturas: list[dict]) -> list[Asignatura]:
	"""
	Inserta un registro en la tabla de Asignatura por cada diccionario de datos

	:param datos_asignaturas: los datos de las asignaturas que se van a insertar
	:return: los datos de las asignaturas insertados
	"""
	sql = (
		insert(Asignatura)
		.values(datos_asignaturas)
		.returning(Asignatura)
	)

	try:
		with get_transaccion() as transaccion:
			return transaccion.execute(sql).all()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_asignatura: str, datos_asingaturas: dict) -> Asignatura:
	"""
	Actualiza los datos de la asignatura con código indicado por codigo_asignatura con los datos del diccionario

	:param codigo_asignatura: el codigo de la asignatura que se va a actualizar
	:param datos_asingaturas: un diccionario con los datos actualizados de la asignatura
	:returns: los datos de la asignatura actualizada

	Esta función no realiza una actualización por lotes porque no soporta devolver el resultado
	https://github.com/sqlalchemy/sqlalchemy/discussions/7980
	"""
	sql = (
		update(Asignatura)
		.where(Asignatura.codigo == codigo_asignatura)
		.values(datos_asingaturas)
		.returning(Asignatura)
	)

	try:
		with get_conexion() as conexion:
			return conexion.execute(sql).one_or_none()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def borrar(codigos_asignaturas: list[str]) -> list[str]:
	"""
	Borra todas las asignaturas cuyo código se encuentre en la lista de codigos_asignaturas

	:param codigos_asignaturas: la lista de código de las asignaturas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Asignatura)
		.where(Asignatura.codigo.in_(codigos_asignaturas))
		.returning(Asignatura.codigo)
	)

	with get_transaccion() as transaccion:
		return transaccion.scalars(sql).all()
