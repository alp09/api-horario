from api.bbdd.dao import dao_grupo
from api.esquemas import Grupo


def get_todos() -> list[Grupo]:
	"""
	Llama a la funcion seleccionar_todos del dao_grupo

	:return: una lista con todos los grupos encontrados
	"""
	return dao_grupo.seleccionar_todos()


def get_por_codigo(codigo_grupo: str) -> Grupo | None:
	"""
	Llama a la funcion seleccionar_por_codigo del dao_grupo

	:param codigo_grupo: el codigo del grupo que se busca
	:return: el grupo código se encuentra o None si ningún grupo tiene asignado ese código
	"""
	return dao_grupo.seleccionar_por_codigo(codigo_grupo)


def insertar(datos_grupos: list[Grupo]) -> list[Grupo]:
	"""
	Llama a la funcion insertar del dao_grupo con la lista de datos de grupos que se quiere insertar

	:param datos_grupos: los datos de los grupos que se quiere guardar
	:return: la representación de los grupos insertados en la BBDD
	"""
	grupos_procesados = [grupo.dict() for grupo in datos_grupos]
	return dao_grupo.insertar(grupos_procesados)


def actualizar_uno(codigo_grupo: str, datos_grupo: Grupo) -> Grupo | None:
	"""
	Llama a la funcion actualizar_por_codigo del dao_grupo con los datos del grupo que se quiere actualizar

	:param codigo_grupo: el código del grupo que se va a actualizar
	:param datos_grupo: los datos actualizados del grupo
	:return: los datos actualizados del grupo o None si hubo algún error
	"""
	return dao_grupo.actualizar_por_codigo(codigo_grupo, datos_grupo.dict())


def borrar(codigos_grupos: list[str]) -> list[str]:
	"""
	Llama a la funcion borrar del dao_grupo con la lista de grupos que se quiere borrar

	:param codigos_grupos: una lista que contiene todos los grupos que se quieren borrar
	:return: una lista con los codigos de los grupos que se han borrado
	"""
	return dao_grupo.borrar(codigos_grupos)


def borrar_uno(codigo_grupo: str) -> bool:
	"""
	Llama a la funcion borrar del dao_grupo con el codigo del grupo que se quiere borrar

	:param codigo_grupo: el código del grupo que se quiere borrar
	:return: True si el grupo se ha eliminado o False si hubo un error (no existe)
	"""
	grupo_eliminado = dao_grupo.borrar([codigo_grupo])
	return grupo_eliminado.__len__() == 1
