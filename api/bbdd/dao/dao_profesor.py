from sqlalchemy import select, insert, update, delete, bindparam
from sqlalchemy.exc import IntegrityError

from api.bbdd import get_conexion, get_transaccion
from api.bbdd.tablas import Profesor
from api.excepciones.bbdd import IntegridadError


def seleccionar_todos() -> list[Profesor]:
	"""
	Selecciona todos los profesores registrados

	:return: una lista de todos los profesores guardados
	"""
	sql = select(Profesor).order_by(Profesor.codigo)

	with get_conexion() as conexion:
		return conexion.execute(sql).all()


def seleccionar_por_codigos(codigos_profesores: list[str]) -> list[Profesor]:
	"""
	Selecciona todos los profesores cuyo código se encuentre en la lista codigos_profesores

	:param codigos_profesores: la lista de códigos de profesores que se quieren encontrar
	:return: una lista de todos los profesores encontrados
	"""
	sql = select(Profesor).where(Profesor.codigo.in_(codigos_profesores))

	with get_conexion() as conexion:
		return conexion.execute(sql).all()


def seleccionar_por_codigo(codigo_profesor: str) -> Profesor | None:
	"""
	Selecciona el profesor cuyo código sea igual a codigo_profesor

	:param codigo_profesor: el código del profesor que se busca
	:return: el profesor si se encuentra o None si ningún profesor tiene asignado ese código
	"""
	sql = select(Profesor).where(Profesor.codigo == codigo_profesor)

	with get_conexion() as conexion:
		return conexion.execute(sql).one_or_none()


def seleccionar_por_email(email_profesor: str) -> Profesor | None:
	"""
	Selecciona el profesor cuyo email sea igual a email_profesor

	:param email_profesor: el email del profesor que se busca
	:return: el profesor si se encuentra o None si el email no pertenece a ningún profesor
	"""
	sql = select(Profesor).where(Profesor.email == email_profesor)

	with get_conexion() as conexion:
		return conexion.execute(sql).one_or_none()


def insertar(datos_profesores: list[dict]) -> list[Profesor]:
	"""
	Inserta un registro en la tabla de Profesor por cada diccionario de datos

	:param datos_profesores: los datos de los profesores que se van a insertar
	:return: los datos de los profesores insertados
	"""
	sql = (
		insert(Profesor)
		.values(datos_profesores)
		.returning(Profesor)
	)

	try:
		with get_transaccion() as transaccion:
			return transaccion.execute(sql).all()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_profesor: str, datos_profesor: dict) -> Profesor:
	"""
	Actualiza los datos del profesor con código indicado por la key codigo_ con el resto de datos del diccionario

	:param codigo_profesor: el codigo del profesor que se va a actualizar
	:param datos_profesor: un diccionario con los datos actualizados del profesor
	:returns: los datos del profesor actualizado

	Esta función no realiza una actualización por lotes porque no soporta devolver el resultado
	https://github.com/sqlalchemy/sqlalchemy/discussions/7980
	"""
	sql = (
		update(Profesor)
		.where(Profesor.codigo == codigo_profesor)
		.values(datos_profesor)
		.returning(Profesor)
	)

	try:
		with get_conexion() as conexion:
			return conexion.execute(sql).one_or_none()

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def borrar(codigos_profesores: list[str]) -> list[str]:
	"""
	Borra todos los profesores cuyo código se encuentre en la lsita de codigos_profesores

	:param codigos_profesores: la lista de código de los profesores a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Profesor)
		.where(Profesor.codigo.in_(codigos_profesores))
		.returning(Profesor.codigo)
	)

	with get_transaccion() as transaccion:
		return transaccion.scalars(sql).all()
