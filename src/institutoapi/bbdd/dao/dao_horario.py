from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.modelos import Horario
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todos(sesion: Session) -> list[Horario]:
	"""
	Selecciona todos los horarios registrados

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todos los horarios guardados
	"""
	sql = (
		select(Horario)
		.order_by(Horario.id)
	)

	horarios_seleccionados = sesion.exec(sql).all()
	return horarios_seleccionados


def insertar(sesion: Session, datos_horarios: list[dict]) -> list[Horario]:
	"""
	Inserta un registro en la tabla de Horario por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
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
		horarios_insertados = sesion.execute(orm_stmt).scalars().all()
		sesion.commit()
		return horarios_insertados

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_codigo(sesion: Session, id_horario: int, datos_horario: dict) -> Horario | None:
	"""
	Actualiza los datos del horario con id_horario con el resto de datos del diccionario datos_horario

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
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
		horario_actualizado = sesion.exec(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return horario_actualizado

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, id_horarios: list[int]) -> list[int]:
	"""
	Borra todos los horarios cuyo ID se encuentre en la lista de id_horarios

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param id_horarios: la lista de ID de los horarios a borrar
	:return: una lista de todos los ID de horarios que se han eliminado
	"""
	sql = (
		delete(Horario)
		.where(Horario.id.in_(id_horarios))
		.returning(Horario.id)
	)

	id_horarios_eliminados = sesion.exec(sql).scalars().all()
	sesion.commit()
	return id_horarios_eliminados
