from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.modelos import Reserva
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todas(sesion: Session) -> list[Reserva]:
	"""
	Selecciona todas las reservas registradas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todas las reservas guardadas
	"""
	sql = (
		select(Reserva)
		.order_by(Reserva.id)
	)

	reservas_seleccionadas = sesion.exec(sql).all()
	return reservas_seleccionadas


def seleccionar_por_lista_id(sesion: Session, id_reservas: list[int]) -> list[Reserva]:
	"""
	Selecciona todas las reservas cuyo id se encuentre en la lista id_reservas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param id_reservas: la lista de ID de las reservas que se quieren consultar
	:return: las reservas encontradas
	"""
	sql = (
		select(Reserva)
		.where(Reserva.id.in_(id_reservas))
	)

	reservas_seleccionadas = sesion.exec(sql).all()
	return reservas_seleccionadas


def seleccionar_por_id(sesion: Session, id_reserva: int) -> Reserva | None:
	"""
	Selecciona la reserva cuyo código sea igual a codigo_aula

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param id_reserva: el ID de la reserva que se busca
	:return: el reserva si se encuentra o None si ninguna reserva tiene asignado ese código
	"""
	sql = (
		select(Reserva)
		.where(Reserva.id == id_reserva)
	)

	reserva_seleccionada = sesion.exec(sql).one_or_none()
	return reserva_seleccionada


def insertar(sesion: Session, datos_reservas: list[dict]) -> list[Reserva]:
	"""
	Inserta un registro en la tabla de Reserva por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
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
		reservas_creadas = sesion.execute(orm_stmt).scalars().all()
		sesion.commit()
		return reservas_creadas

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_id(sesion: Session, id_reserva: int, datos_reserva: dict) -> Reserva | None:
	"""
	Actualiza los datos de la reserva con id_reserva con los datos del diccionario

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
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
		reservas_actualizadas = sesion.execute(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return reservas_actualizadas

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, id_reservas: list[int]) -> list[int]:
	"""
	Borra todas las reservas cuyo código se encuentre en la lista de codigos_aulas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param id_reservas: la lista de ID de las reservas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Reserva)
		.where(Reserva.id.in_(id_reservas))
		.returning(Reserva.id)
	)

	reservas_eliminadas = sesion.execute(sql).scalars().all()
	sesion.commit()
	return reservas_eliminadas
