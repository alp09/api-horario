from api.bbdd.dao import dao_horario
from api.esquemas import Horario


def get_todos() -> list[Horario]:
	horarios_encontrados = dao_horario.seleccionar_todos()
	return horarios_encontrados


def insertar(horarios_nuevos: list[Horario]) -> list[Horario]:
	horarios_procesados = [horario.dict(exclude_unset=True) for horario in horarios_nuevos]
	return dao_horario.insertar(horarios_procesados)


def actualizar_por_codigo(id_horario: int, datos_horario: Horario) -> Horario | None:
	return dao_horario.actualizar_por_codigo(id_horario, datos_horario.dict())


def borrar(id_horarios: list[int]) -> list[int]:
	return dao_horario.borrar(id_horarios)


def borrar_por_codigo(id_horario: int) -> bool:
	horario_borrado = dao_horario.borrar([id_horario])
	return horario_borrado.__len__() == 1
