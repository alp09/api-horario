from sqlmodel import Session

from institutoapi.bbdd.dao import dao_horario, dao_reserva
from institutoapi.modelos import Reserva, ReservaRequest
from institutoapi.validaciones import validar_reservas


def insertar(
	sesion: Session,
	reservas_nuevas: list[ReservaRequest],
) -> list[Reserva]:

	# Valida los horarios insertados. En caso de error devuelve una excepción
	horarios_registrados = dao_horario.seleccionar_todos(sesion)
	reservas_registradas = dao_reserva.seleccionar_todas(sesion)
	validar_reservas(reservas_nuevas, reservas_registradas, horarios_registrados)

	# Si no devuelve una excepción, los horarios son válidos y se insertan en la BBDD
	reservas_procesadas = [reserva.dict() for reserva in reservas_nuevas]
	reservas_creadas 	= dao_reserva.insertar(sesion, reservas_procesadas)
	return reservas_creadas


def actualizar_por_codigo(
	sesion: Session,
	id_reserva_editada: int,
	reserva_editada: ReservaRequest,
) -> Reserva | None:

	# Valida cada horario que se va a insertar en la BBDD con los demás horarios
	horarios_registrados = dao_horario.seleccionar_todos(sesion)
	reservas_registradas = dao_reserva.seleccionar_todas(sesion)
	validar_reservas([reserva_editada], reservas_registradas, horarios_registrados, excluir_id=id_reserva_editada)

	# Si no devuelve una excepción, los horarios son válidos y se insertan en la BBDD
	reserva_actualizada = dao_reserva.actualizar_por_id(sesion, id_reserva_editada, reserva_editada.dict())
	return reserva_actualizada
