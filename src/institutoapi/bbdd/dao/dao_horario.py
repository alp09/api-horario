from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, InternalError

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.tablas import Horario
from institutoapi.excepciones.bbdd import IntegridadError, DatosInvalidosError


def seleccionar_todos() -> list[Horario]:
	"""
	Selecciona todos los horarios registrados

	:return: una lista de todos los horarios guardados
	"""
	sql = (
		select(Horario)
		.order_by(Horario.id)
	)

	with get_sesion() as sesion:
		horarios_seleccionados = sesion.execute(sql).scalars().all()
		return horarios_seleccionados


def insertar(datos_horarios: list[dict]) -> list[Horario]:
	"""
	Inserta un registro en la tabla de Horario por cada diccionario de datos

	:param datos_horarios: los datos de los horarios que se van a insertar
	:return: los datos de los horarios insertados
	"""
	sql = (
		insert(Horario)
		.values(datos_horarios)
		.returning(Horario)
	)

	orm_stmt = (
		select(Horario)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			horarios_insertados = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return horarios_insertados

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def actualizar_por_codigo(id_horario: int, datos_horario: dict) -> Horario | None:
	"""
	Actualiza los datos del horario con id_horario con el resto de datos del diccionario datos_horario

	:param id_horario: el ID del horario que se va a actualizar
	:param datos_horario: un diccionario con los datos actualizados del horario
	:returns: los datos del horario actualizado
	"""
	sql = (
		update(Horario)
		.where(Horario.id == id_horario)
		.values(datos_horario)
		.returning(Horario)
	)

	orm_stmt = (
		select(Horario)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			horario_actualizado = sesion.execute(orm_stmt).scalars().one_or_none()
			sesion.commit()
			return horario_actualizado

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def borrar(id_horarios: list[int]) -> list[int]:
	"""
	Borra todos los horarios cuyo ID se encuentre en la lista de id_horarios

	:param id_horarios: la lista de ID de los horarios a borrar
	:return: una lista de todos los ID de horarios que se han eliminado
	"""
	sql = (
		delete(Horario)
		.where(Horario.id.in_(id_horarios))
		.returning(Horario.id)
	)

	with get_sesion() as sesion:
		id_horarios_eliminados = sesion.execute(sql).scalars().all()
		sesion.commit()
		return id_horarios_eliminados
