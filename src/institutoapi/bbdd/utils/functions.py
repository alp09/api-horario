from sqlalchemy import event, DDL

from institutoapi.bbdd.tablas import Horario, Reserva


def generar_funciones():

	@event.listens_for(Horario.__table__, "after_create")
	def generar_function_get_horario_fijo(_, connection, **kwargs):
		get_horario_fijo = DDL("""
			CREATE OR REPLACE FUNCTION public.get_horario_fijo(p_dia integer, p_tramo integer, p_asignatura text DEFAULT NULL::text, p_profesor text DEFAULT NULL::text, p_aula text DEFAULT NULL::text, p_grupo text DEFAULT NULL::text)
			RETURNS TABLE(dia text, tramo text, asignatura text, c_asignatura text, profesor text, c_profesor text, aula text, c_aula text, grupo text, c_grupo text)
			LANGUAGE sql
			AS $function$
			
			SELECT 
				dia_semana.descripcion, 
				tramo_horario.descripcion, 
				asignatura.descripcion, asignatura.codigo, 
				profesor.nombre, profesor.codigo, 
				aula.descripcion, aula.codigo, 
				grupo.descripcion, grupo.codigo

			FROM horario

			INNER JOIN dia_semana ON horario.id_dia = dia_semana.id
			INNER JOIN tramo_horario ON horario.id_tramo = tramo_horario.id
			INNER JOIN asignatura ON horario.codigo_asignatura = asignatura.codigo
			INNER JOIN profesor ON horario.codigo_profesor = profesor.codigo
			INNER JOIN aula ON horario.codigo_aula = aula.codigo
			INNER JOIN grupo ON horario.codigo_grupo = grupo.codigo

			WHERE horario.id_dia = p_dia
			  AND horario.id_tramo = p_tramo
			  AND (p_asignatura IS null OR horario.codigo_asignatura = p_asignatura) 
			  AND (p_profesor IS null OR horario.codigo_profesor = p_profesor)
			  AND (p_aula IS null OR horario.codigo_aula = p_aula)
			  AND (p_grupo IS null OR horario.codigo_grupo = p_grupo)

			$function$

		""")
		get_horario_fijo.execute(connection)

	@event.listens_for(Reserva.__table__, "after_create")
	def generar_function_get_clases_del_dia(_, connection, **kwargs):
		get_clases_del_dia = DDL("""
			CREATE OR REPLACE FUNCTION public.get_clases_del_dia(p_fecha date, p_tramo integer, p_asignatura text DEFAULT NULL::text, p_profesor text DEFAULT NULL::text, p_aula text DEFAULT NULL::text, p_grupo text DEFAULT NULL::text)
			RETURNS TABLE(dia text, tramo text, asignatura text, c_asignatura text, profesor text, c_profesor text, aula text, c_aula text, grupo text, c_grupo text)
			LANGUAGE sql
			AS $function$
			
			SELECT 
				dia_semana.descripcion, 
				tramo_horario.descripcion, 
				asignatura.descripcion, asignatura.codigo, 
				profesor.nombre, profesor.codigo, 
				aula.descripcion, aula.codigo, 
				grupo.descripcion, grupo.codigo

			FROM (
				SELECT h.id_dia, h.id_tramo, h.codigo_asignatura, h.codigo_profesor, h.codigo_aula, h.codigo_grupo
				FROM horario AS h					
				WHERE h.id_dia = EXTRACT(dow FROM p_fecha)
			UNION
				SELECT EXTRACT(dow FROM r.fecha) AS id_dia, r.id_tramo, r.codigo_asignatura, r.codigo_profesor, r.codigo_aula, r.codigo_grupo
				FROM reserva AS r
				WHERE r.fecha = p_fecha
			) clases

			INNER JOIN dia_semana ON clases.id_dia = dia_semana.id
			INNER JOIN tramo_horario ON clases.id_tramo = tramo_horario.id
			INNER JOIN asignatura ON clases.codigo_asignatura = asignatura.codigo
			INNER JOIN profesor ON clases.codigo_profesor = profesor.codigo
			INNER JOIN aula ON clases.codigo_aula = aula.codigo
			INNER JOIN grupo ON clases.codigo_grupo = grupo.codigo

			WHERE clases.id_tramo = p_tramo
			  AND (p_asignatura IS null OR clases.codigo_asignatura = p_asignatura) 
			  AND (p_profesor IS null OR clases.codigo_profesor = p_profesor)
			  AND (p_aula IS null OR clases.codigo_aula = p_aula)
			  AND (p_grupo IS null OR clases.codigo_grupo = p_grupo)

			$function$
		""")
		get_clases_del_dia.execute(connection)


def generar_funciones_trigger():

	@event.listens_for(Horario.__table__, "after_create")
	def generar_trigger_function_check_horario_profesor_en_varias_aulas(_, connection, **kwargs):
		check_horario_profesor_en_varias_aulas = DDL("""
			CREATE OR REPLACE FUNCTION public.check_horario_profesor_en_varias_aulas()
			 RETURNS trigger
			 LANGUAGE plpgsql
			AS $function$

			DECLARE
				dia_registrado			dia_semana.descripcion%%TYPE;
				tramo_registrado		tramo_horario.descripcion%%TYPE;
				profesor_registrado		profesor.nombre%%TYPE;
				aula_registrada			aula.descripcion%%TYPE;

			BEGIN

				/*
					Esta función la usa el trigger_validar_horario_del_profesor.
					Su propósito es que al insertar / actualizar un horario,
					 valide que el profesor no tenga ese día, a esa hora, clases en un aula distinta.
				*/

				-- Si especifica un aula, verifica que no se esté impartiendo otra asignatura
				IF NEW.codigo_aula IS NOT null THEN

					-- Busca registros de ese día, hora y profesor en un aula distinta
					SELECT horario_registrado.dia, horario_registrado.tramo, horario_registrado.profesor, horario_registrado.aula
					INTO dia_registrado, tramo_registrado, profesor_registrado, aula_registrada
					FROM get_horario_fijo(p_dia => NEW.id_dia, p_tramo => NEW.id_tramo, p_profesor => NEW.codigo_profesor) AS horario_registrado
					WHERE horario_registrado.c_aula != NEW.codigo_aula
					LIMIT 1;
	
					-- Si se encuentra un registro en un aula distinta, se devuelve una excepción
					IF found THEN
						RAISE EXCEPTION 'El profesor %% no puede impartir clases en %% porque ya tiene clases en %% el %% a %%.',
							profesor_registrado, NEW.codigo_aula, aula_registrada, dia_registrado, tramo_registrado;
					END IF;
					
				END IF;
				
				-- Si no se encontró nada, se devuelven los datos entrantes
				RETURN NEW;

			END$function$
		""")
		check_horario_profesor_en_varias_aulas.execute(connection)

	@event.listens_for(Horario.__table__, "after_create")
	def generar_trigger_function_check_horario_varias_asignaturas_mismo_aula(_, connection, **kwargs):
		check_horario_varias_asignaturas_mismo_aula = DDL("""
			CREATE OR REPLACE FUNCTION public.check_horario_varias_asignaturas_mismo_aula()
			 RETURNS trigger
			 LANGUAGE plpgsql
			AS $function$

			DECLARE
				dia_registrado			dia_semana.descripcion%%TYPE;
				tramo_registrado		tramo_horario.descripcion%%TYPE;
				asignatura_registrada	asignatura.descripcion%%TYPE;
				aula_registrada			aula.descripcion%%TYPE;

			BEGIN

				/*
					Esta función la usa el trigger_validar_asignatura_impartida_en_aula.
					Su propósito es que al insertar / actualizar un horario, valide que en el aula del nuevo registro 
					no se esté impartiendo ese día, a esa hora, otra asignatura distinta.
				*/

				-- Si especifica un aula, verifica que no se esté impartiendo otra asignatura
				IF NEW.codigo_aula IS NOT null THEN

					-- Busca registros de ese día, hora y aula en los que se esté dando una asignatura distinta
					SELECT horario_registrado.dia, horario_registrado.tramo, horario_registrado.asignatura, horario_registrado.aula
					INTO dia_registrado, tramo_registrado, asignatura_registrada, aula_registrada
					FROM get_horario_fijo(p_dia => NEW.id_dia, p_tramo => NEW.id_tramo, p_aula => NEW.codigo_aula) AS horario_registrado
					WHERE horario_registrado.c_asignatura != NEW.codigo_asignatura
					LIMIT 1;
	
					-- Si se encuentra un registro con una asignatura distinta, se devuelve una excepción
					IF found THEN
						RAISE EXCEPTION 'No se puede dar clases de %% en %% el %% a %% porque ya se imparte %%.',
							NEW.codigo_asignatura, aula_registrada, dia_registrado, tramo_registrado, asignatura_registrada;
					END IF;
					
				END IF;
				
				RETURN NEW;

			END$function$
		""")
		check_horario_varias_asignaturas_mismo_aula.execute(connection)

	@event.listens_for(Reserva.__table__, "after_create")
	def generar_trigger_function_check_reserva_profesor_en_varias_aulas(_, connection, **kwargs):
		check_reserva_profesor_en_varias_aulas = DDL("""
			CREATE OR REPLACE FUNCTION public.check_reserva_profesor_en_varias_aulas()
			 RETURNS trigger
			 LANGUAGE plpgsql
			AS $function$

			DECLARE
				dia_registrado			dia_semana.descripcion%%TYPE;
				tramo_registrado		tramo_horario.descripcion%%TYPE;
				profesor_registrado		profesor.nombre%%TYPE;
				aula_registrada			aula.descripcion%%TYPE;

			BEGIN

				/*
					Esta función la usa el trigger_validar_horario_del_profesor.
					Su propósito es que al insertar / actualizar un horario,
					 valide que el profesor no tenga ese día, a esa hora, clases en un aula distinta.
				*/

				-- Busca registros de ese día, hora y profesor en un aula distinta
				SELECT horario_registrado.dia, horario_registrado.tramo, horario_registrado.profesor, horario_registrado.aula
				INTO dia_registrado, tramo_registrado, profesor_registrado, aula_registrada
				FROM get_clases_del_dia(p_dia => NEW.fecha, p_tramo => NEW.id_tramo, p_profesor => NEW.codigo_profesor) AS horario_registrado
				WHERE horario_registrado.c_aula != NEW.codigo_aula
				LIMIT 1;

				-- Si no se encontró nada, se devuelven los datos entrantes
				IF NOT found THEN
					RETURN NEW;

				-- Si se encuentra un registro en un aula distinta, se devuelve una excepción
				ELSE
					RAISE EXCEPTION 'El profesor %% no puede impartir clases en %% porque ya tiene clases en %% el %% a %%.',
						profesor_registrado, NEW.codigo_aula, aula_registrada, dia_registrado, tramo_registrado;
				END IF;

			END$function$
		""")
		check_reserva_profesor_en_varias_aulas.execute(connection)

	@event.listens_for(Reserva.__table__, "after_create")
	def generar_trigger_function_check_reserva_varias_asignaturas_mismo_aula(_, connection, **kwargs):
		check_reserva_varias_asignaturas_mismo_aula = DDL("""
			CREATE OR REPLACE FUNCTION public.check_reserva_varias_asignaturas_mismo_aula()
			 RETURNS trigger
			 LANGUAGE plpgsql
			AS $function$

			DECLARE
				dia_registrado			dia_semana.descripcion%%TYPE;
				tramo_registrado		tramo_horario.descripcion%%TYPE;
				asignatura_registrada	asignatura.descripcion%%TYPE;
				aula_registrada			aula.descripcion%%TYPE;

			BEGIN

				/*
					Esta función la usa el trigger_validar_asignatura_impartida_en_aula.
					Su propósito es que al insertar / actualizar un horario, valide que en el aula del nuevo registro
					no se esté impartiendo ese día, a esa hora, otra asignatura distinta.
				*/

				-- Busca registros de ese día, hora y aula en los que se esté dando una asignatura distinta
				SELECT horario_registrado.dia, horario_registrado.tramo, horario_registrado.asignatura, horario_registrado.aula
				INTO dia_registrado, tramo_registrado, asignatura_registrada, aula_registrada
				FROM get_clases_del_dia(p_dia => NEW.fecha, p_tramo => NEW.id_tramo, p_aula => NEW.codigo_aula) AS horario_registrado
				WHERE horario_registrado.c_asignatura != NEW.codigo_asignatura
				LIMIT 1;

				-- Si no se encontró nada, se devuelven los datos entrantes
				IF NOT found THEN
					RETURN NEW;

				-- Si se encuentra un registro con una asignatura distinta, se devuelve una excepción
				ELSE
					RAISE EXCEPTION 'No se puede dar clases de %% en %% el %% a %% porque ya se imparte %%.',
						NEW.codigo_asignatura, aula_registrada, dia_registrado, tramo_registrado, asignatura_registrada;
				END IF;

			END$function$
		""")
		check_reserva_varias_asignaturas_mismo_aula.execute(connection)
