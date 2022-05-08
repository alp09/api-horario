from api.bbdd.dao import dao_asignatura
from api.esquemas import Asignatura


def get_todas() -> list[Asignatura]:
	"""
	Llama a la funcion seleccionar_todas del dao_asignatura

	:return: una lista con todas las asignaturas encontradas
	"""
	return dao_asignatura.seleccionar_todas()


def get_por_codigo(codigo_asignatura: str) -> Asignatura | None:
	"""
	Llama a la funcion seleccionar_por_codigo del dao_asignatura

	:param codigo_asignatura: el codigo de la asignatura que se busca
	:return: la asignatura si se encuentra o None si ninguna asignatura tiene asignada ese código
	"""
	return dao_asignatura.seleccionar_por_codigo(codigo_asignatura)


def insertar(datos_asignaturas: list[Asignatura]) -> list[Asignatura]:
	"""
	Llama a la funcion insertar del dao_asignatura con la lista de datos de asignaturas que se quiere insertar

	:param datos_asignaturas: los datos de las asignaturas que se quiere guardar
	:return: la representación de las asignaturas insertadas en la BBDD
	"""
	asignaturas_procesadas = [asignatura.dict() for asignatura in datos_asignaturas]
	return dao_asignatura.insertar(asignaturas_procesadas)


def actualizar_uno(codigo_asignatura: str, datos_asignatura: Asignatura) -> Asignatura | None:
	"""
	Llama a la funcion actualizar_por_codigo del dao_asignatura con los datos de la asignatura que se quiere actualizar

	:param codigo_asignatura: el código de la asignatura que se va a actualizar
	:param datos_asignatura: los datos actualizados de la asignatura
	:return: los datos de la asignatura actualizados o None si hubo algún error
	"""
	return dao_asignatura.actualizar_por_codigo(codigo_asignatura, datos_asignatura.dict())


def borrar(codigos_asignaturas: list[str]) -> list[str]:
	"""
	Llama a la funcion borrar del dao_asignatura con la lista de asignaturas que se quiere borrar

	:param codigos_asignaturas: una lista que contiene todas las asignaturas que se quieren borrar
	:return: una lista con los codigos de las asignaturas que se han borrado
	"""
	return dao_asignatura.borrar(codigos_asignaturas)


def borrar_uno(codigo_asignatura: str) -> bool:
	"""
	Llama a la funcion borrar del dao_asignatura con el codigo del asignatura que se quiere borrar

	:param codigo_asignatura: el código del asignatura que se quiere borrar
	:return: True si el asignatura se ha eliminado o False si hubo un error (no existe)
	"""
	asignatura_borrada = dao_asignatura.borrar([codigo_asignatura])
	return asignatura_borrada.__len__() == 1
