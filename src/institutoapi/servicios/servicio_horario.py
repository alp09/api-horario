from collections import defaultdict
from sqlmodel import Session

from institutoapi.bbdd.dao import dao_horario
from institutoapi.bbdd.modelos import Horario, HorarioRequest
from institutoapi.validaciones import validar_horarios


def insertar(
	sesion: Session,
	horarios_nuevos: list[HorarioRequest],
) -> list[Horario]:

	# Valida los horarios insertados. En caso de error devuelve una excepción
	horarios_registrados = dao_horario.seleccionar_todos(sesion)
	validar_horarios(horarios_nuevos, horarios_registrados)

	# Si no devuelve una excepción, los horarios son válidos y se insertan en la BBDD
	horarios_procesados = [horario.dict() for horario in horarios_nuevos]
	horarios_creados = dao_horario.insertar(sesion, horarios_procesados)
	return horarios_creados


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
