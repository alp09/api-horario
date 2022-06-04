from api.bbdd.dao import dao_reserva
from api.esquemas import ReservaIn, ReservaOut


def get_todos() -> list[ReservaOut]:
	reservas_encontrados = dao_reserva.seleccionar_todos()
	return reservas_encontrados


def insertar(reservas_nuevos: list[ReservaIn]) -> list[ReservaOut]:
	reservas_procesados = [reserva.dict(exclude_unset=True) for reserva in reservas_nuevos]
	reservas_insertados = dao_reserva.insertar(reservas_procesados)
	return reservas_insertados


def actualizar_por_codigo(id_reserva: int, datos_reserva: ReservaIn) -> ReservaOut | None:
	reserva_actualizado = dao_reserva.actualizar_por_codigo(id_reserva, datos_reserva.dict(exclude_unset=True))
	return reserva_actualizado


def borrar(id_reservas: list[int]) -> list[int]:
	reservas_borrados = dao_reserva.borrar(id_reservas)
	return reservas_borrados


def borrar_por_codigo(id_reserva: int) -> bool:
	reserva_borrado = dao_reserva.borrar([id_reserva])
	return reserva_borrado.__len__() == 1
