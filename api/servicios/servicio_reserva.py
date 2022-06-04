from api.bbdd.dao import dao_reserva
from api.esquemas import ReservaIn, ReservaOut


def get_todas() -> list[ReservaOut]:
	"""
	Llama a la función select_todas del dao_reserva

	:return: una lista con todas las reservas encontradas
	"""
	reservas_encontradas = dao_reserva.seleccionar_todas()
	return reservas_encontradas


def get_por_id(id_reserva: int) -> ReservaOut | None:
	"""
	Llama a la función select_por_id del dao_reserva

	:param id_reserva: el ID de la reserva que se busca
	:return: la reserva si se encuentra o None si ninguna dao_reserva tiene asignada ese ID
	"""
	reserva_encontrada = dao_reserva.seleccionar_por_id(id_reserva)
	return reserva_encontrada


def crear_reservas(reservas_nuevas: list[ReservaIn]) -> list[ReservaOut]:
	"""
	Llama a la función insert del dao_reserva con la lista de datos de reservas que se quiere insertar

	:param reservas_nuevas: los datos de las nuevas reservas que se quiere guardar
	:return: la representación de las reservas insertadas en la BBDD
	"""
	reservas_procesadas = [reserva.dict(exclude_unset=True) for reserva in reservas_nuevas]
	reservas_insertadas = dao_reserva.insertar(reservas_procesadas)
	return reservas_insertadas


def actualizar_por_id(id_reserva: int, reserva_editada: ReservaIn) -> ReservaOut | None:
	"""
	Llama a la función update_por_id del dao_reserva con los datos de la reserva que se quiere actualizar

	:param id_reserva: el ID de la reserva que se va a actualizar
	:param reserva_editada: los datos editados de la reserva
	:return: la reserva actualizada o None si hubo algún error
	"""
	reserva_actualizada = dao_reserva.actualizar_por_codigo(id_reserva, reserva_editada.dict(exclude_unset=True))
	return reserva_actualizada


def borrar_reservas(id_reservas: list[int]) -> list[int]:
	"""
	Llama a la función delete del dao_reserva con la lista de reservas que se quiere borrar

	:param id_reservas: una lista que contiene todas las reservas que se quieren borrar
	:return: una lista con los codigos de las reservas que se han eliminado
	"""
	reservas_borrados = dao_reserva.borrar(id_reservas)
	return reservas_borrados


def borrar_por_id(id_reserva: int) -> bool:
	"""
	Llama a la función delete del dao_reserva con el ID de la reserva que se quiere borrar

	:param id_reserva: el ID del reserva que se quiere borrar
	:return: True si el reserva se ha eliminado o False si hubo un error (no existe)
	"""
	reserva_borrado = dao_reserva.borrar([id_reserva])
	return reserva_borrado.__len__() == 1
