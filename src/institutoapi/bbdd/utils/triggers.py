from sqlalchemy import event, DDL

from institutoapi.bbdd.tablas import DiaSemana, TramoHorario, Horario, Reserva


def generar_triggers():

	@event.listens_for(Horario.__table__, "after_create")
	def generar_trigger_horario_validar_clases_del_profesor(_, connection, **kwargs):
		validar_clases_del_profesor = DDL(""" 
			CREATE TRIGGER validar_clases_del_profesor
			BEFORE INSERT OR UPDATE 
			ON public.horario
			FOR EACH ROW
			EXECUTE FUNCTION public.check_horario_profesor_en_varias_aulas();
		""")
		validar_clases_del_profesor.execute(connection)

	@event.listens_for(Horario.__table__, "after_create")
	def generar_trigger_horario_validar_asignaturas_impartidas(_, connection, **kwargs):
		validar_asignaturas_impartidas = DDL(""" 
			CREATE TRIGGER validar_asignaturas_impartidas
			BEFORE INSERT OR UPDATE 
			ON public.horario
			FOR EACH ROW
			EXECUTE FUNCTION public.check_horario_varias_asignaturas_mismo_aula();
		""")
		validar_asignaturas_impartidas.execute(connection)

	@event.listens_for(Reserva.__table__, "after_create")
	def generar_trigger_reserva_validar_clases_del_profesor(_, connection, **kwargs):
		validar_clases_del_profesor = DDL(""" 
				CREATE TRIGGER validar_clases_del_profesor
				BEFORE INSERT OR UPDATE 
				ON public.reserva
				FOR EACH ROW
				EXECUTE FUNCTION public.check_reserva_profesor_en_varias_aulas();
			""")
		validar_clases_del_profesor.execute(connection)

	@event.listens_for(Reserva.__table__, "after_create")
	def generar_trigger_reserva_validar_asignaturas_impartidas(_, connection, **kwargs):
		validar_asignaturas_impartidas = DDL(""" 
				CREATE TRIGGER validar_asignaturas_impartidas
				BEFORE INSERT OR UPDATE 
				ON public.reserva
				FOR EACH ROW
				EXECUTE FUNCTION public.check_reserva_varias_asignaturas_mismo_aula();
			""")
		validar_asignaturas_impartidas.execute(connection)


def generar_datos_tablas():

	@event.listens_for(DiaSemana.__table__, "after_create")
	def generar_registros_tabla_dia_semana(_, connection, **kwargs):
		valores_tabla_dia_semana = DDL(""" 
				INSERT INTO dia_semana (descripcion) 
				VALUES ('lunes'), ('martes'), ('miércoles'), ('jueves'), ('viernes');
			""")
		valores_tabla_dia_semana.execute(connection)

	@event.listens_for(TramoHorario.__table__, "after_create")
	def generar_registros_tabla_tramo_horario(_, connection, **kwargs):
		valores_tabla_tramo_horario = DDL(""" 
				INSERT INTO tramo_horario (descripcion, hora_inicio, hora_fin) 
				VALUES
					('primera hora', 	'08:30', '09:30'),
					('segunda hora', 	'09:30', '10:30'),
					('tercera hora', 	'10:30', '11:30'),
					('recreo', 			'11:30', '12:00'),
					('cuarta hora', 	'12:00', '13:00'),
					('quinta hora', 	'13:00', '14:00'),
					('sexta hora', 		'14:00', '15:00');
			""")
		valores_tabla_tramo_horario.execute(connection)
