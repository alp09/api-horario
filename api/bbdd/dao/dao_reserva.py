from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, InternalError

from api.bbdd import get_sesion
from api.bbdd.tablas import Reserva
from api.excepciones.bbdd import IntegridadError, DatosInvalidosError


def seleccionar_todas() -> list[Reserva]:
	"""
	Selecciona todas las reservas registradas

	:return: una lista de todas las reservas guardadas
	"""
	sql = (
		select(Reserva)
		.order_by(Reserva.id)
	)

	with get_sesion() as sesion:
		reservas_seleccionadas = sesion.execute(sql).scalars().all()
		return reservas_seleccionadas


def seleccionar_por_id(id_reserva: int) -> Reserva | None:
	"""
	Selecciona el reserva cuyo código sea igual a codigo_aula

	:param id_reserva: el ID de la reserva que se busca
	:return: el reserva si se encuentra o None si ninguna reserva tiene asignado ese código
	"""
	sql = (
		select(Reserva)
		.where(Reserva.id == id_reserva)
	)

	with get_sesion() as sesion:
		reserva_seleccionada = sesion.execute(sql).scalars().one_or_none()
		return reserva_seleccionada


def insertar(datos_reservas: list[dict]) -> list[Reserva]:
	"""
	Inserta un registro en la tabla de Aula por cada diccionario de datos

	:param datos_reservas: los datos de las reservas que se van a insertar
	:return: los datos de las reservas insertados
	"""
	sql = (
		insert(Reserva)
		.values(datos_reservas)
		.returning(Reserva)
	)

	orm_stmt = (
		select(Reserva)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			reservas_creadas = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return reservas_creadas

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def actualizar_por_codigo(id_reserva: int, datos_reserva: dict) -> Reserva | None:
	"""
	Actualiza los datos de la reserva con id_reserva con los datos del diccionario

	:param id_reserva: el codigo de la reserva que se va a actualizar
	:param datos_reserva: un diccionario con los datos actualizados de la reserva
	:returns: los datos de la reserva actualizada
	"""
	sql = (
		update(Reserva)
		.where(Reserva.id == id_reserva)
		.values(datos_reserva)
		.returning(Reserva)
	)

	orm_stmt = (
		select(Reserva)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			reservas_actualizadas = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return reservas_actualizadas

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def borrar(id_reservas: list[int]) -> list[int]:
	"""
	Borra todas las reservas cuyo código se encuentre en la lista de codigos_aulas

	:param id_reservas: la lista de ID de las reservas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Reserva)
		.where(Reserva.id.in_(id_reservas))
		.returning(Reserva.id)
	)

	with get_sesion() as sesion:
		reservas_eliminadas = sesion.execute(sql).scalars().all()
		sesion.commit()
		return reservas_eliminadas
