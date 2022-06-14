from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.bbdd.modelos import Profesor
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todos(sesion: Session) -> list[Profesor]:
	"""
	Selecciona todos los profesores registrados

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todos los profesores guardados
	"""
	sql = (
		select(Profesor)
		.order_by(Profesor.codigo)
	)

	profesores_seleccionados = sesion.exec(sql).all()
	return profesores_seleccionados


def seleccionar_por_codigo(sesion: Session, codigo_profesor: str) -> Profesor | None:
	"""
	Selecciona el profesor cuyo código sea igual a codigo_profesor

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_profesor: el código del profesor que se busca
	:return: el profesor si se encuentra o None si ningún profesor tiene asignado ese código
	"""
	sql = (
		select(Profesor)
		.where(Profesor.codigo == codigo_profesor)
	)

	profesor_seleccionado = sesion.exec(sql).one_or_none()
	return profesor_seleccionado


def seleccionar_por_email(sesion: Session, email_profesor: str) -> Profesor | None:
	"""
	Selecciona el profesor cuyo email sea igual a email_profesor

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param email_profesor: el email del profesor que se busca
	:return: el profesor si se encuentra o None si el email no pertenece a ningún profesor
	"""
	sql = (
		select(Profesor)
		.where(Profesor.email == email_profesor)
	)

	profesor_seleccionado = sesion.exec(sql).one_or_none()
	return profesor_seleccionado


def insertar(sesion: Session, datos_profesores: list[dict]) -> list[Profesor]:
	"""
	Inserta un registro en la tabla de Profesor por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param datos_profesores: los datos de los profesores que se van a insertar
	:return: los datos de los profesores insertados
	"""
	sql = (
		insert(Profesor)
		.values(datos_profesores)
		.returning(Profesor)
	)

	orm_stmt = select(Profesor).from_statement(sql)

	try:
		profesores_insertados = sesion.exec(orm_stmt).scalars().all()
		sesion.commit()
		return profesores_insertados

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_codigo(sesion: Session, codigo_profesor: str, datos_profesor: dict) -> Profesor:
	"""
	Actualiza los datos del profesor con codigo_profesor con el resto de datos del diccionario datos_profesor

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_profesor: el codigo del profesor que se va a actualizar
	:param datos_profesor: un diccionario con los datos actualizados del profesor
	:returns: los datos del profesor actualizado
	"""
	sql = (
		update(Profesor)
		.where(Profesor.codigo == codigo_profesor)
		.values(datos_profesor)
		.returning(Profesor)
	)

	orm_stmt = select(Profesor).from_statement(sql)

	try:
		profesor_actualizado = sesion.exec(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return profesor_actualizado

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, codigos_profesores: list[str]) -> list[str]:
	"""
	Borra todos los profesores cuyo código se encuentre en la lista de codigos_profesores

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigos_profesores: la lista de código de los profesores a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Profesor)
		.where(Profesor.codigo.in_(codigos_profesores))
		.returning(Profesor.codigo)
	)

	profesores_eliminados = sesion.exec(sql).scalars().all()
	sesion.commit()
	return profesores_eliminados
