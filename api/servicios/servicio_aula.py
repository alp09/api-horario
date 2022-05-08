from api.bbdd.dao import dao_aula
from api.esquemas import Aula


def get_todas() -> list[Aula]:
	"""
	Llama a la funcion seleccionar_todas del dao_aula

	:return: una lista con todas las aulas encontradas
	"""
	return dao_aula.seleccionar_todas()


def get_por_codigo(codigo_aula: str) -> Aula | None:
	"""
	Llama a la funcion seleccionar_por_codigo del dao_aula

	:param codigo_aula: el codigo del aula que se busca
	:return: el aula si se encuentra o None si ninguna aula tiene asignada ese código
	"""
	return dao_aula.seleccionar_por_codigo(codigo_aula)


def insertar(datos_aulas: list[Aula]) -> list[Aula]:
	"""
	Llama a la funcion insertar del dao_aula con la lista de datos de aulas que se quiere insertar

	:param datos_aulas: los datos de las aulas que se quiere guardar
	:return: la representación de las aulas insertadas en la BBDD
	"""
	aulas_procesadas = [aula.dict() for aula in datos_aulas]
	return dao_aula.insertar(aulas_procesadas)


def actualizar_uno(codigo_aula: str, datos_aula: Aula) -> Aula | None:
	"""
	Llama a la funcion actualizar_por_codigo del dao_aula con los datos del aula que se quiere actualizar

	:param codigo_aula: el código del aula que se va a actualizar
	:param datos_aula: los datos actualizados del aula
	:return: los datos del aula actualizados o None si hubo algún error
	"""
	return dao_aula.actualizar_por_codigo(codigo_aula, datos_aula.dict())


def borrar(codigos_aulas: list[str]) -> list[str]:
	"""
	Llama a la funcion borrar del dao_aula con la lista de aulas que se quiere borrar

	:param codigos_aulas: una lista que contiene todas las aulas que se quieren borrar
	:return: una lista con los codigos de las aulas que se han borrado
	"""
	return dao_aula.borrar(codigos_aulas)


def borrar_uno(codigo_aula: str) -> bool:
	"""
	Llama a la funcion borrar del dao_aula con el codigo del aula que se quiere borrar

	:param codigo_aula: el código del aula que se quiere borrar
	:return: True si el aula se ha eliminado o False si hubo un error (no existe)
	"""
	aula_borrada = dao_aula.borrar([codigo_aula])
	return aula_borrada.__len__() == 1
