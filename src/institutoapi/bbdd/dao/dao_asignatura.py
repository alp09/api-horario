from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from institutoapi.bbdd import get_conexion, get_transaccion
from institutoapi.bbdd.tablas import Asignatura
from institutoapi.excepciones.bbdd import IntegridadError


def seleccionar_todas() -> list[Asignatura]:
	"""
	Selecciona todas las asignaturas registradas

	:return: una lista de todas las asignaturas guardadas
	"""
	sql = (
		select(Asignatura)
		.order_by(Asignatura.codigo)
	)

	with get_conexion() as conexion:
		asignaturas_seleccionadas = conexion.execute(sql).all()
		return asignaturas_seleccionadas


def seleccionar_por_codigo(codigo_asignatura: str) -> Asignatura | None:
	"""
	Selecciona la asignatura cuyo código sea igual a codigo_asignatura

	:param codigo_asignatura: el código de la asignatura que se busca
	:return: la asignatura si se encuentra o None si ninguna asignatura tiene asignado ese código
	"""
	sql = (
		select(Asignatura)
		.where(Asignatura.codigo == codigo_asignatura)
	)

	with get_conexion() as conexion:
		asignatura_seleccionada = conexion.execute(sql).one_or_none()
		return asignatura_seleccionada


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
			asignaturas_insertadas = transaccion.execute(sql).all()
			return asignaturas_insertadas

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_asignatura: str, datos_asingaturas: dict) -> Asignatura:
	"""
	Actualiza los datos de la asignatura con código indicado por codigo_asignatura con los datos del diccionario

	:param codigo_asignatura: el codigo de la asignatura que se va a actualizar
	:param datos_asingaturas: un diccionario con los datos actualizados de la asignatura
	:returns: los datos de la asignatura actualizada
	"""
	sql = (
		update(Asignatura)
		.where(Asignatura.codigo == codigo_asignatura)
		.values(datos_asingaturas)
		.returning(Asignatura)
	)

	try:
		with get_transaccion() as transaccion:
			asignaturas_actualizadas = transaccion.execute(sql).one_or_none()
			return asignaturas_actualizadas

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
		asignaturas_borradas = transaccion.scalars(sql).all()
		return asignaturas_borradas
