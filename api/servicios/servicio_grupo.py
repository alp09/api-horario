from api.bbdd.dao import dao_grupo
from api.esquemas import Grupo


def get_todos() -> list[Grupo]:
	"""
	Llama a la función select_todos del dao_grupo

	:return: una lista con todos los grupos encontrados
	"""
	grupos_seleccionados = dao_grupo.seleccionar_todos()
	return grupos_seleccionados


def get_por_codigo(codigo_grupo: str) -> Grupo | None:
	"""
	Llama a la función select_por_id del dao_grupo

	:param codigo_grupo: el codigo del grupo que se busca
	:return: el grupo si se encuentra o None si ningún grupo tiene asignado ese código
	"""
	grupo_seleccionado = dao_grupo.seleccionar_por_codigo(codigo_grupo)
	return grupo_seleccionado


def crear_grupos(grupos_nuevos: list[Grupo]) -> list[Grupo]:
	"""
	Llama a la función insert del dao_grupo con la lista de datos de grupos que se quiere insertar

	:param grupos_nuevos: los datos de los grupos que se quiere guardar
	:return: la representación de los grupos insertados en la BBDD
	"""
	grupos_procesados = [grupo.dict() for grupo in grupos_nuevos]
	grupos_creados = dao_grupo.insertar(grupos_procesados)
	return grupos_creados


def actualizar_por_codigo(codigo_grupo: str, grupo_editado: Grupo) -> Grupo | None:
	"""
	Llama a la función update_por_id del dao_grupo con los datos del grupo que se quiere actualizar

	:param codigo_grupo: el código del grupo que se va a actualizar
	:param grupo_editado: los datos actualizados del grupo
	:return: el grupo actualizado o None si hubo algún error
	"""
	grupo_actualizado = dao_grupo.actualizar_por_codigo(codigo_grupo, grupo_editado.dict())
	return grupo_actualizado


def borrar_grupos(codigos_grupos: list[str]) -> list[str]:
	"""
	Llama a la función delete del dao_grupo con la lista de grupos que se quiere borrar

	:param codigos_grupos: una lista que contiene todos los grupos que se quieren borrar
	:return: una lista con los codigos de los grupos que se han borrado
	"""
	grupos_eliminados = dao_grupo.borrar(codigos_grupos)
	return grupos_eliminados


def borrar_por_codigo(codigo_grupo: str) -> bool:
	"""
	Llama a la función delete del dao_grupo con el codigo del grupo que se quiere borrar

	:param codigo_grupo: el código del grupo que se quiere borrar
	:return: True si el grupo se ha eliminado o False si hubo un error (no existe)
	"""
	grupo_eliminado = dao_grupo.borrar([codigo_grupo])
	return grupo_eliminado.__len__() == 1
