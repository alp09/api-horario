from sqlmodel import Session

from institutoapi.bbdd.dao import dao_horario
from institutoapi.modelos import Horario, HorarioRequest
from institutoapi.validaciones import validar_horarios


def actualizar_por_codigo(
	sesion: Session,
	id_horario_editado: int,
	horario_editado: HorarioRequest,
) -> Horario | None:

	# Valida cada horario que se va a insertar en la BBDD con los demás horarios
	horarios_registrados = dao_horario.seleccionar_todos(sesion)
	validar_horarios([horario_editado], horarios_registrados, excluir_id=id_horario_editado)

	# Si no devuelve una excepción, los horarios son válidos y se insertan en la BBDD
	horario_actualizado = dao_horario.actualizar_por_codigo(sesion, id_horario_editado, horario_editado.dict())
	return horario_actualizado
