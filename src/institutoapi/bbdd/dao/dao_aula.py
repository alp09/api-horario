from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.modelos import Aula
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todas(sesion: Session) -> list[Aula]:
	"""
	Selecciona todas las aulas registradas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todas las aulas guardadas
	"""
	sql = (
		select(Aula)
		.order_by(Aula.codigo)
	)

	aulas_seleccionadas = sesion.exec(sql).all()
	return aulas_seleccionadas


def seleccionar_por_codigo(sesion: Session, codigo_aula: str) -> Aula | None:
	"""
	Selecciona el aula cuyo código sea igual a codigo_aula

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_aula: el código del aula que se busca
	:return: el aula si se encuentra o None si ninguna aula tiene asignado ese código
	"""
	sql = (
		select(Aula)
		.where(Aula.codigo == codigo_aula)
	)

	aula_seleccionada = sesion.exec(sql).one_or_none()
	return aula_seleccionada


def insertar(sesion: Session, datos_aulas: list[dict]) -> list[Aula]:
	"""
	Inserta un registro en la tabla de Aula por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param datos_aulas: los datos de las aulas que se van a insertar
	:return: los datos de las aulas insertados
	"""
	sql = (
		insert(Aula)
		.values(datos_aulas)
		.returning(Aula)
	)

	orm_stmt = select(Aula).from_statement(sql)

	try:
		aulas_creadas = sesion.exec(orm_stmt).scalars().all()
		sesion.commit()
		return aulas_creadas

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_codigo(sesion: Session, codigo_aula: str, datos_asingaturas: dict) -> Aula:
	"""
	Actualiza los datos del aula con código indicado por codigo_aula con los datos del diccionario

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
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

	orm_stmt = select(Aula).from_statement(sql)

	try:
		aula_actualizada = sesion.exec(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return aula_actualizada

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, codigos_aulas: list[str]) -> list[str]:
	"""
	Borra todas las aulas cuyo código se encuentre en la lista de codigos_aulas

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigos_aulas: la lista de código de las aulas a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Aula)
		.where(Aula.codigo.in_(codigos_aulas))
		.returning(Aula.codigo)
	)

	aulas_eliminadas = sesion.exec(sql).scalars().all()
	sesion.commit()
	return aulas_eliminadas
