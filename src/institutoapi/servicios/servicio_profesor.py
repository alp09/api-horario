from institutoapi.bbdd.dao import dao_profesor
from institutoapi.esquemas import Profesor


def get_todos() -> list[Profesor]:
	"""
	Llama a la función select_todos del dao_profesor

	:return: una lista con todos los profesores encontrados
	"""
	profesores_seleccionados = dao_profesor.seleccionar_todos()
	return profesores_seleccionados


def get_por_codigo(codigo_profesor: str) -> Profesor | None:
	"""
	Llama a la función select_por_id del dao_profesor

	:param codigo_profesor: el codigo del profesor que se busca
	:return: el profesor si se encuentra o None si ningún profesor tiene asignado ese código
	"""
	profesor_seleccionado = dao_profesor.seleccionar_por_codigo(codigo_profesor)
	return profesor_seleccionado


def get_por_email(email_profesor: str) -> Profesor | None:
	"""
	Llama a la función select_por_email del dao_profesor

	:param email_profesor: el email del profesor que se busca
	:return: el profesor si se encuentra o None si el email no pertenece a ningún profesor
	"""
	profesor_seleccionado = dao_profesor.seleccionar_por_email(email_profesor)
	return profesor_seleccionado


def crear_profesores(profesores_nuevos: list[Profesor]) -> list[Profesor]:
	"""
	Llama a la función insert del dao_profesor con la lista de datos de profesores que se quiere insertar

	:param profesores_nuevos: los datos de los profesores que se quiere guardar
	:return: la representación de los profesores insertados en la BBDD
	"""
	profesores_procesados = [profesor.dict() for profesor in profesores_nuevos]
	profesores_creados = dao_profesor.insertar(profesores_procesados)
	return profesores_creados


def actualizar_por_codigo(codigo_profesor: str, profesor_editado: Profesor) -> Profesor | None:
	"""
	Llama a la función update_por_codigo del dao_profesor con los datos del profesor que se quiere actualizar

	:param codigo_profesor: el código del profesor que se va a actualizar
	:param profesor_editado: los datos actualizados del profesor
	:return: el profesor actualizado o None si hubo algún error
	"""
	profesor_actualizado = dao_profesor.actualizar_por_codigo(codigo_profesor, profesor_editado.dict())
	return profesor_actualizado


def borrar_profesores(codigos_profesores: list[str]) -> list[str]:
	"""
	Llama a la función delete del dao_profesor con la lista de profesores que se quiere borrar

	:param codigos_profesores: una lista que contiene todos los profesores que se quieren borrar
	:return: una lista con los codigos de los profesores que se han eliminado
	"""
	profesores_eliminados = dao_profesor.borrar(codigos_profesores)
	return profesores_eliminados


def borrar_por_codigo(codigo_profesor: str) -> bool:
	"""
	Llama a la función delete del dao_profesor con el codigo del profesor que se quiere borrar

	:param codigo_profesor: el código del profesor que se quiere borrar
	:return: True si el profesor se ha eliminado o False si hubo un error (no existe)
	"""
	profesor_eliminado = dao_profesor.borrar([codigo_profesor])
	return profesor_eliminado.__len__() == 1
