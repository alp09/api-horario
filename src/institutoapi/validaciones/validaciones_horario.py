from collections import defaultdict

from institutoapi.excepciones.horario import *


def validar_horarios(
	horarios_nuevos,
	horarios_guardados,
	*,
	excluir_id: int = None
):

	# Organiza los horarios por día y tramo
	horarios_organizados = defaultdict(lambda: defaultdict(list))
	for horario in horarios_guardados + horarios_nuevos:
		if not hasattr(horario, "id") or horario.id != excluir_id:
			horarios_organizados[horario.id_dia][horario.id_tramo].append(horario)

	# Por cada horario_nuevo, ejecuta las validaciones correspondientes con los horarios de su mismo día y tramo
	for horario in horarios_nuevos:

		# Se realiza una copia de los registros del mismo momento que el horario_nuevo
		# Esto se hace para después eliminar el horario_nuevo de la copia sin modificar la lista original
		horarios_del_mismo_momento = horarios_organizados[horario.id_dia][horario.id_tramo]
		horarios_del_mismo_momento.remove(horario)
		_ejecutar_validaciones(horario, horarios_del_mismo_momento, dia=horario.id_dia)


def validar_reservas(
	reservas_nuevas,
	reservas_almacenadas,
	horarios_almacenados,
	*,
	excluir_id: int = None
):

	# Organiza los horarios por día y tramo
	horarios_organizados = defaultdict(lambda: defaultdict(list))
	for horario in horarios_almacenados:
		horarios_organizados[horario.id_dia][horario.id_tramo].append(horario)

	# Organiza las reservas por fecha y tramo
	reservas_organizadas = defaultdict(lambda: defaultdict(list))
	for reserva in reservas_almacenadas + reservas_nuevas:
		if not hasattr(reserva, "id") or reserva.id != excluir_id:
			reservas_organizadas[reserva.fecha][reserva.id_tramo].append(reserva)

	# Por cada reserva_nueva, ejecuta las validaciones correspondientes con los horarios y reservas de la misma fecha y tramo
	for reserva in reservas_nuevas:

		# Extra los horarios del mismo día de la semana que la reserva
		horarios_del_mismo_momento = horarios_organizados[reserva.fecha.weekday() + 1][reserva.id_tramo]

		# Extrae las reservas de la misma fecha que la reserva que se va a validar
		# Además la elimina de la lista para no compararla consigo misma
		reservas_del_mismo_momento = reservas_organizadas[reserva.fecha][reserva.id_tramo]
		reservas_del_mismo_momento.remove(reserva)

		_ejecutar_validaciones(reserva, horarios_del_mismo_momento + reservas_del_mismo_momento, dia=reserva.fecha.weekday() + 1)


def _ejecutar_validaciones(registro_nuevo, registros_para_validar, dia):
	"""
	Valida que se cumplan varias condiciones entre el registro_nuevo y los registros_para_validar

	Estas condiciones son:
		- _validar_profesor_no_esta_en_otro_aula
		- _validar_no_se_imparte_varias_asignaturas_en_mismo_aula

	:param registro_nuevo: el registro que se quieren validar
	:param registros_para_validar: los registros contra los que se va a validar el registro_nuevo.
		Tienen que ser del mismo día y hora que el registro nuevo.
	"""

	# Valida cada registro que se va a insertar en la BBDD con los demás del mismo día y tramo
	for registro in registros_para_validar:
		_validar_profesor_no_esta_en_otro_aula(registro_nuevo, registro, dia)
		_validar_no_se_imparte_varias_asignaturas_en_mismo_aula(registro_nuevo, registro, dia)


def _validar_profesor_no_esta_en_otro_aula(registro_nuevo, registro_para_validar, dia):
	"""
	Valida que el registro_nuevo no sea del mismo profesor en un aula distinta

	:param registro_nuevo: el registro que se quiere guardar en la bbdd
	:param registro_para_validar: un registro ya guardado en la bbdd o que se quiere guardar junto con el registro_nuevo
	:raises ProfesorImparteClasesEnOtraAula: si el profesor ya tiene clases en otra aula en ese momento
	"""
	if registro_nuevo.codigo_profesor == registro_para_validar.codigo_profesor \
		and registro_nuevo.codigo_aula != registro_para_validar.codigo_aula:

		raise ProfesorImparteClasesEnOtraAula(
			dia=dia,
			tramo=registro_nuevo.id_tramo,
			profesor=registro_nuevo.codigo_profesor,
			aula_nueva=registro_nuevo.codigo_aula,
			aula_vieja=registro_para_validar.codigo_aula,
		)


def _validar_no_se_imparte_varias_asignaturas_en_mismo_aula(registro_nuevo, registro_para_validar, dia):
	"""
	Valida que el aula del nuevo_registro no se esté impartiendo varias asignaturas

	:param registro_nuevo: el registro que se quiere guardar en la bbdd
	:param registro_para_validar: un registro ya guardado en la bbdd o que se quiere guardar junto con el registro_nuevo
	:raises SeImparteAsignaturaDistinta: si ya se imparte una asignatura distinta a la indicada en registro_nuevo en el mismo aula
	"""
	if registro_nuevo.codigo_aula is not None \
		and registro_nuevo.codigo_aula == registro_para_validar.codigo_aula \
		and registro_nuevo.codigo_asignatura != registro_para_validar.codigo_asignatura:

		raise SeImparteAsignaturaDistinta(
			dia=dia,
			tramo=registro_nuevo.id_tramo,
			asignatura_nueva=registro_nuevo.codigo_asignatura,
			asignatura_vieja=registro_para_validar.codigo_asignatura,
			aula=registro_nuevo.codigo_aula,
		)
