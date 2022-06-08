from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from institutoapi.bbdd import get_conexion, get_transaccion
from institutoapi.bbdd.tablas import Aula
from institutoapi.excepciones.bbdd import IntegridadError


def seleccionar_todas() -> list[Aula]:
	"""
	Selecciona todas las aulas registradas

	:return: una lista de todas las aulas guardadas
	"""
	sql = (
		select(Aula)
		.order_by(Aula.codigo)
	)

	with get_conexion() as conexion:
		aulas_seleccionadas = conexion.execute(sql).all()
		return aulas_seleccionadas


def seleccionar_por_codigo(codigo_aula: str) -> Aula | None:
	"""
	Selecciona el aula cuyo código sea igual a codigo_aula

	:param codigo_aula: el código del aula que se busca
	:return: el aula si se encuentra o None si ninguna aula tiene asignado ese código
	"""
	sql = (
		select(Aula)
		.where(Aula.codigo == codigo_aula)
	)

	with get_conexion() as conexion:
		aula_seleccionada = conexion.execute(sql).one_or_none()
		return aula_seleccionada


def insertar(datos_aulas: list[dict]) -> list[Aula]:
	"""
	Inserta un registro en la tabla de Aula por cada diccionario de datos

	:param datos_aulas: los datos de las aulas que se van a insertar
	:return: los datos de las aulas insertados
	"""
	sql = (
		insert(Aula)
		.values(datos_aulas)
		.returning(Aula)
	)

	try:
		with get_transaccion() as transaccion:
			return transaccion.execute(sql).all()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_aula: str, datos_asingaturas: dict) -> Aula:
	"""
	Actualiza los datos del aula con código indicado por codigo_aula con los datos del diccionario

	:param codigo_aula: el codigo del aula que se va a actualizar
	:param datos_asingaturas: un diccionario con los datos actualizados del aula
	:returns: los datos del aula actualizada
	"""
	sql = (
		update(Aula)
		.where(Aula.codigo == codigo_aula)
		.values(datos_asingaturas)
		.returning(Aula)
	)

	try:
		with get_transaccion() as transaccion:
			return transaccion.execute(sql).one_or_none()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def borrar(codigos_aulas: list[str]) -> list[str]:
	"""
	Borra todas las aulas cuyo código se encuentre en la lista de codigos_aulas

	:param codigos_aulas: la lista de código de las aulas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Aula)
		.where(Aula.codigo.in_(codigos_aulas))
		.returning(Aula.codigo)
	)

	with get_transaccion() as transaccion:
		return transaccion.scalars(sql).all()
