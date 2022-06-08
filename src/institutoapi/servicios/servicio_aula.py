from institutoapi.bbdd.dao import dao_aula
from institutoapi.esquemas import Aula


def get_todas() -> list[Aula]:
	"""
	Llama a la función select_todas del dao_aula

	:return: una lista con todas las aulas encontradas
	"""
	aulas_seleccionadas = dao_aula.seleccionar_todas()
	return aulas_seleccionadas


def get_por_codigo(codigo_aula: str) -> Aula | None:
	"""
	Llama a la función select_por_id del dao_aula

	:param codigo_aula: el codigo del aula que se busca
	:return: el aula si se encuentra o None si ninguna aula tiene asignada ese código
	"""
	aula_seleccionada = dao_aula.seleccionar_por_codigo(codigo_aula)
	return aula_seleccionada


def crear_aulas(aulas_nuevas: list[Aula]) -> list[Aula]:
	"""
	Llama a la función insert del dao_aula con la lista de datos de aulas que se quiere insertar

	:param aulas_nuevas: los datos de las aulas que se quiere guardar
	:return: la representación de las aulas insertadas en la BBDD
	"""
	aulas_procesadas = [aula.dict() for aula in aulas_nuevas]
	aulas_creadas = dao_aula.insertar(aulas_procesadas)
	return aulas_creadas


def actualizar_por_codigo(codigo_aula: str, aula_editada: Aula) -> Aula | None:
	"""
	Llama a la función update_por_id del dao_aula con los datos del aula que se quiere actualizar

	:param codigo_aula: el código del aula que se va a actualizar
	:param aula_editada: los datos editados del aula
	:return: el aula actualizada o None si hubo algún error
	"""
	aula_actualizada = dao_aula.actualizar_por_codigo(codigo_aula, aula_editada.dict())
	return aula_actualizada


def borrar_aulas(codigos_aulas: list[str]) -> list[str]:
	"""
	Llama a la función delete del dao_aula con la lista de aulas que se quiere eliminar

	:param codigos_aulas: una lista que contiene todas las aulas que se quieren borrar
	:return: una lista con los códigos de las aulas que se han eliminado
	"""
	aulas_eliminadas = dao_aula.borrar(codigos_aulas)
	return aulas_eliminadas


def borrar_por_codigo(codigo_aula: str) -> bool:
	"""
	Llama a la función delete del dao_aula con el codigo del aula que se quiere borrar

	:param codigo_aula: el código del aula que se quiere borrar
	:return: True si el aula se ha eliminado o False si hubo un error (no existe)
	"""
	aula_eliminada = dao_aula.borrar([codigo_aula])
	return aula_eliminada.__len__() == 1
