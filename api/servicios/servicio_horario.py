from api.bbdd.dao import dao_horario
from api.esquemas import HorarioIn, HorarioOut


def get_todos() -> list[HorarioOut]:
	horarios_encontrados = dao_horario.seleccionar_todos()
	return horarios_encontrados


def insertar(horarios_nuevos: list[HorarioIn]) -> list[HorarioOut]:
	horarios_procesados = [horario.dict(exclude_unset=True) for horario in horarios_nuevos]
	horarios_insertados = dao_horario.insertar(horarios_procesados)
	return horarios_insertados


def actualizar_por_codigo(id_horario: int, datos_horario: HorarioIn) -> HorarioOut | None:
	horario_actualizado = dao_horario.actualizar_por_codigo(id_horario, datos_horario.dict(exclude_unset=True))
	return horario_actualizado


def borrar(id_horarios: list[int]) -> list[int]:
	horarios_borrados = dao_horario.borrar(id_horarios)
	return horarios_borrados


def borrar_por_codigo(id_horario: int) -> bool:
	horario_borrado = dao_horario.borrar([id_horario])
	return horario_borrado.__len__() == 1
