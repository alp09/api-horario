from api.bbdd.dao import dao_horario
from api.esquemas import HorarioIn, HorarioOut


def get_todos() -> list[HorarioOut]:
	"""
	Llama a la función select_todos del dao_horario

	:return: una lista con todas los horarios encontrados
	"""
	horarios_encontrados = dao_horario.seleccionar_todos()
	return horarios_encontrados


def crear_horarios(horarios_nuevos: list[HorarioIn]) -> list[HorarioOut]:
	"""
	Llama a la función insert del dao_horario con la lista de datos de horarios que se quiere insertar

	:param horarios_nuevos: los datos de los nuevos horarios que se quiere guardar
	:return: la representación de los horarios insertadas en la BBDD
	"""
	horarios_procesados = [horario.dict(exclude_unset=True) for horario in horarios_nuevos]
	horarios_insertados = dao_horario.insertar(horarios_procesados)
	return horarios_insertados


def actualizar_por_id(id_horario: int, horario_editado: HorarioIn) -> HorarioOut | None:
	"""
	Llama a la función update_por_id del dao_horario con los datos del horario que se quiere actualizar

	:param id_horario: el ID del horario que se va a actualizar
	:param horario_editado: los datos editados del horario
	:return: el horario actualizado o None si hubo algún error
	"""
	horario_actualizado = dao_horario.actualizar_por_codigo(id_horario, horario_editado.dict(exclude_unset=True))
	return horario_actualizado


def borrar_horarios(id_horarios: list[int]) -> list[int]:
	"""
	Llama a la función delete del dao_horario con la lista de horarios que se quiere borrar

	:param id_horarios: una lista que contiene todos los ID de horarios que se quieren borrar
	:return: una lista con los ID de los horarios que se han eliminado
	"""
	horarios_borrados = dao_horario.borrar(id_horarios)
	return horarios_borrados


def borrar_por_id(id_horario: int) -> bool:
	"""
	Llama a la función delete del dao_horario con el ID del horario que se quiere borrar

	:param id_horario: el ID del horario que se quiere borrar
	:return: True si el horario se ha eliminado o False si hubo un error (no existe)
	"""
	horario_borrado = dao_horario.borrar([id_horario])
	return horario_borrado.__len__() == 1
