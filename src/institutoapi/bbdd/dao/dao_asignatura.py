from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.bbdd.modelos import Asignatura
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todas(sesion: Session) -> list[Asignatura]:
	"""
	Selecciona todas las asignaturas registradas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todas las asignaturas guardadas
	"""
	sql = (
		select(Asignatura)
		.order_by(Asignatura.codigo)
	)

	asignaturas_seleccionadas = sesion.exec(sql).all()
	return asignaturas_seleccionadas


def seleccionar_por_codigo(sesion: Session, codigo_asignatura: str) -> Asignatura | None:
	"""
	Selecciona la asignatura cuyo código sea igual a codigo_asignatura

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_asignatura: el código de la asignatura que se busca
	:return: la asignatura si se encuentra o None si ninguna asignatura tiene asignado ese código
	"""
	sql = (
		select(Asignatura)
		.where(Asignatura.codigo == codigo_asignatura)
	)

	asignatura_seleccionada = sesion.exec(sql).one_or_none()
	return asignatura_seleccionada


def insertar(sesion: Session, asignatuas_nuevas: list[dict]) -> list[Asignatura]:
	"""
	Inserta un registro en la tabla de Asignatura por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param asignatuas_nuevas: los datos de las asignaturas que se van a insertar
	"""
	sql = (
		insert(Asignatura)
		.values(asignatuas_nuevas)
		.returning(Asignatura)
	)

	orm_stmt = select(Asignatura).from_statement(sql)

	try:
		asignaturas_insertadas = sesion.exec(orm_stmt).scalars().all()
		sesion.commit()
		return asignaturas_insertadas

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_codigo(sesion: Session, codigo_asignatura: str, datos_asignaturas: dict) -> Asignatura:
	"""
	Actualiza los datos de la asignatura con código indicado por codigo_asignatura con los datos del diccionario

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_asignatura: el codigo de la asignatura que se va a actualizar
	:param datos_asignaturas: un diccionario con los datos actualizados de la asignatura
	:returns: los datos de la asignatura actualizada
	"""
	sql = (
		update(Asignatura)
		.where(Asignatura.codigo == codigo_asignatura)
		.values(datos_asignaturas)
		.returning(Asignatura)
	)

	orm_stmt = select(Asignatura).from_statement(sql)

	try:
		asignatura_actualizada = sesion.exec(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return asignatura_actualizada

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, codigos_asignaturas: list[str]) -> list[str]:
	"""
	Borra todas las asignaturas cuyo código se encuentre en la lista de codigos_asignaturas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigos_asignaturas: la lista de código de las asignaturas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Asignatura)
		.where(Asignatura.codigo.in_(codigos_asignaturas))
		.returning(Asignatura.codigo)
	)

	asignaturas_borradas = sesion.exec(sql).scalars().all()
	sesion.commit()
	return asignaturas_borradas
