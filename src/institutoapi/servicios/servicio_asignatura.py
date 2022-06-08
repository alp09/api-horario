from institutoapi.bbdd.dao import dao_asignatura
from institutoapi.esquemas import Asignatura


def get_todas() -> list[Asignatura]:
	"""
	Llama a la función select_todas del dao_asignatura

	:return: una lista con todas las asignaturas encontradas
	"""
	asignaturas_seleccionadas = dao_asignatura.seleccionar_todas()
	return asignaturas_seleccionadas


def get_por_codigo(codigo_asignatura: str) -> Asignatura | None:
	"""
	Llama a la función select_por_id del dao_asignatura

	:param codigo_asignatura: el código de la asignatura que se busca
	:return: la asignatura si se encuentra o None si ninguna asignatura tiene asignada ese código
	"""
	asignatura_seleccionada = dao_asignatura.seleccionar_por_codigo(codigo_asignatura)
	return asignatura_seleccionada


def crear_aulas(asignaturas_nuevas: list[Asignatura]) -> list[Asignatura]:
	"""
	Llama a la función insert del dao_asignatura con la lista de datos de asignaturas que se quiere insertar

	:param asignaturas_nuevas: los datos de las nuevas asignaturas que se quiere guardar
	:return: la representación de las asignaturas insertadas en la BBDD
	"""
	asignaturas_procesadas = [asignatura.dict() for asignatura in asignaturas_nuevas]
	asignaturas_creadas = dao_asignatura.insertar(asignaturas_procesadas)
	return asignaturas_creadas


def actualizar_por_codigo(codigo_asignatura: str, asignatura_editada: Asignatura) -> Asignatura | None:
	"""
	Llama a la función update_por_id del dao_asignatura con los datos de la asignatura que se quiere actualizar

	:param codigo_asignatura: el código de la asignatura que se va a actualizar
	:param asignatura_editada: los datos editados de la asignatura
	:return: la asignatura actualizada o None si hubo algún error
	"""
	asignatura_actualizada = dao_asignatura.actualizar_por_codigo(codigo_asignatura, asignatura_editada.dict())
	return asignatura_actualizada


def borrar_asignaturas(codigos_asignaturas: list[str]) -> list[str]:
	"""
	Llama a la función delete del dao_asignatura con la lista de asignaturas que se quiere borrar

	:param codigos_asignaturas: una lista que contiene todas las asignaturas que se quieren borrar
	:return: una lista con los codigos de las asignaturas que se han eliminado
	"""
	asignaturas_eliminadas = dao_asignatura.borrar(codigos_asignaturas)
	return asignaturas_eliminadas


def borrar_por_codigo(codigo_asignatura: str) -> bool:
	"""
	Llama a la función delete del dao_asignatura con el codigo de la asignatura que se quiere borrar

	:param codigo_asignatura: el código del asignatura que se quiere borrar
	:return: True si el asignatura se ha eliminado o False si hubo un error (no existe)
	"""
	asignatura_eliminada = dao_asignatura.borrar([codigo_asignatura])
	return asignatura_eliminada.__len__() == 1
