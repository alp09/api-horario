from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError

from institutoapi.bbdd import get_conexion, get_transaccion
from institutoapi.bbdd.tablas import Grupo
from institutoapi.excepciones.bbdd import IntegridadError


def seleccionar_todos() -> list[Grupo]:
	"""
	Selecciona todos los grupos registrados

	:return: una lista de todos los grupos guardados
	"""
	sql = (
		select(Grupo)
		.order_by(Grupo.codigo)
	)

	with get_conexion() as conexion:
		grupos_seleccionados = conexion.execute(sql).all()
		return grupos_seleccionados


def seleccionar_por_codigo(codigo_grupo: str) -> Grupo | None:
	"""
	Selecciona el grupo cuyo código sea igual a codigo_grupo

	:param codigo_grupo: el código del grupo que se busca
	:return: el grupo si se encuentra o None si ningún grupo tiene asignado ese código
	"""
	sql = (
		select(Grupo)
		.where(Grupo.codigo == codigo_grupo)
	)

	with get_conexion() as conexion:
		grupo_seleccionado = conexion.execute(sql).one_or_none()
		return grupo_seleccionado


def insertar(datos_grupos: list[dict]) -> list[Grupo]:
	"""
	Inserta un registro en la tabla de Grupo por cada diccionario de datos

	:param datos_grupos: los datos de los grupos que se van a insertar
	:return: los datos de los grupos insertados
	"""
	sql = (
		insert(Grupo)
		.values(datos_grupos)
		.returning(Grupo)
	)

	try:
		with get_transaccion() as transaccion:
			grupos_insertados = transaccion.execute(sql).all()
			return grupos_insertados

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_grupo: str, datos_grupo: dict) -> Grupo:
	"""
	Actualiza los datos del grupo con codigo_grupo con el resto de datos del diccionario datos_grupo

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

	try:
		with get_transaccion() as transaccion:
			grupo_actualizado = transaccion.execute(sql).one_or_none()
			return grupo_actualizado

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)


def borrar(codigos_grupos: list[str]) -> list[str]:
	"""
	Borra todos los grupos cuyo código se encuentre en la lista de codigos_grupos

	:param codigos_grupos: la lista de código de los grupos a borrar
	:return: una lista de todos los códigos que se han eliminado
	"""
	sql = (
		delete(Grupo)
		.where(Grupo.codigo.in_(codigos_grupos))
		.returning(Grupo.codigo)
	)

	with get_transaccion() as transaccion:
		grupo_eliminado = transaccion.scalars(sql).all()
		return grupo_eliminado
