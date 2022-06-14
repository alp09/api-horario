from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select, insert, update, delete

from institutoapi.bbdd.modelos import Grupo
from institutoapi.excepciones.bbdd import IntegridadDatosError


def seleccionar_todos(sesion: Session) -> list[Grupo]:
	"""
	Selecciona todos los grupos registrados

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:return: una lista de todos los grupos guardados
	"""
	sql = (
		select(Grupo)
		.order_by(Grupo.codigo)
	)

	grupos_seleccionados = sesion.exec(sql).all()
	return grupos_seleccionados


def seleccionar_por_codigo(sesion: Session, codigo_grupo: str) -> Grupo | None:
	"""
	Selecciona el grupo cuyo código sea igual a codigo_grupo

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_grupo: el código del grupo que se busca
	:return: el grupo si se encuentra o None si ningún grupo tiene asignado ese código
	"""
	sql = (
		select(Grupo)
		.where(Grupo.codigo == codigo_grupo)
	)

	grupo_seleccionado = sesion.exec(sql).one_or_none()
	return grupo_seleccionado


def insertar(sesion: Session, datos_grupos: list[dict]) -> list[Grupo]:
	"""
	Inserta un registro en la tabla de Grupo por cada diccionario de datos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param datos_grupos: los datos de los grupos que se van a insertar
	:return: los datos de los grupos insertados
	"""
	sql = (
		insert(Grupo)
		.values(datos_grupos)
		.returning(Grupo)
	)

	orm_stmt = select(Grupo).from_statement(sql)

	try:
		grupos_insertados = sesion.exec(orm_stmt).scalars().all()
		sesion.commit()
		return grupos_insertados

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def actualizar_por_codigo(sesion: Session, codigo_grupo: str, datos_grupo: dict) -> Grupo:
	"""
	Actualiza los datos del grupo con codigo_grupo con el resto de datos del diccionario datos_grupo

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigo_grupo: el codigo del grupo que se va a actualizar
	:param datos_grupo: un diccionario con los datos actualizados del grupo
	:returns: los datos del grupo actualizado
	"""
	sql = (
		update(Grupo)
		.where(Grupo.codigo == codigo_grupo)
		.values(datos_grupo)
		.returning(Grupo)
	)

	orm_stmt = select(Grupo).from_statement(sql)

	try:
		grupo_actualizado = sesion.exec(orm_stmt).scalars().one_or_none()
		sesion.commit()
		return grupo_actualizado

	except IntegrityError as excepcion:
		raise IntegridadDatosError(excepcion.orig.pgerror)


def borrar(sesion: Session, codigos_grupos: list[str]) -> list[str]:
	"""
	Borra todos los grupos cuyo código se encuentre en la lista de codigos_grupos

	:param sesion: la sesión de bbdd con la que se va a realizar la operación
	:param codigos_grupos: la lista de código de los grupos a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Grupo)
		.where(Grupo.codigo.in_(codigos_grupos))
		.returning(Grupo.codigo)
	)

	grupo_eliminado = sesion.exec(sql).scalars().all()
	sesion.commit()
	return grupo_eliminado
