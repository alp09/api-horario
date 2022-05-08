from api.bbdd.dao import dao_profesor
from api.esquemas.profesor import *


def get_todos() -> list[Profesor]:
	"""
	Llama a la funcion seleccionar_todos del dao_profesor

	:return: una lista con todos los profesores encontrados
	"""
	return dao_profesor.seleccionar_todos()


def get_por_codigo(codigo_profesor: str) -> Profesor | None:
	"""
	Llama a la funcion seleccionar_por_codigo del dao_profesor

	:return: el profesor código se encuentra o None si ningún profesor tiene asignado ese código
	"""
	return dao_profesor.seleccionar_por_codigo(codigo_profesor)


def get_por_email(email_profesor: str) -> Profesor | None:
	"""
	Llama a la funcion seleccionar_todos del dao_profesor

	:return: el profesor si se encuentra o None si el email no pertenece a ningún profesor
	"""
	return dao_profesor.seleccionar_por_email(email_profesor)


def insertar(datos_profesores: list[Profesor]) -> list[Profesor]:
	"""
	Llama a la funcion borrar del insertar con la lista de datos de profesores que se quiere insertar

	:param datos_profesores: los datos de los profesores que se quiere guardar
	:return: la representación de los profesores insertados en la BBDD
	"""
	profesores_procesados = [profesor.dict() for profesor in datos_profesores]
	return dao_profesor.insertar(profesores_procesados)


def actualizar_uno(codigo_profesor: str, datos_profesor: Profesor) -> Profesor | None:
	"""
	Llama a la funcion actualizar del dao_profesor con los datos del profesor que se quiere actualizar

	:param codigo_profesor: el código del profesor que se va a actualizar
	:param datos_profesor: los datos actualizados del profesor
	:return: True si el profesor se ha actualizado o False si no
	"""
	return dao_profesor.actualizar_por_codigo(codigo_profesor, datos_profesor.dict())


def borrar(codigos_profesores: list[str]) -> list[str]:
	"""
	Llama a la funcion borrar del dao_profesor con la lista de profesores que se quiere borrar

	:param codigos_profesores: una lista que contiene todos los profesores que se quieren borrar
	:return: un set que contiene los codigos de los profesores que se han borrado
	"""
	return dao_profesor.borrar(codigos_profesores)


def borrar_uno(codigo_profesor: str) -> bool:
	"""
	Llama a la funcion borrar del dao_profesor con el codigo del profesor que se quiere borrar

	:param codigo_profesor: el código del profesor que se quiere borrar
	:return: True si el profesor se ha eliminado o False si hubo un error (no existe)
	"""
	profesor_eliminado = dao_profesor.borrar([codigo_profesor])
	return profesor_eliminado.__len__() == 1
