from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, InternalError

from api.bbdd import get_sesion
from api.bbdd.tablas import Horario
from api.excepciones.bbdd import IntegridadError, DatosInvalidosError


def seleccionar_todos() -> list[Horario]:
	sql = select(Horario)

	with get_sesion() as sesion:
		horarios_seleccionados = sesion.execute(sql).scalars().all()
		return horarios_seleccionados


def insertar(datos_horarios: list[dict]) -> list[Horario]:
	sql = (
		insert(Horario)
		.values(datos_horarios)
		.returning(Horario)
	)

	orm_stmt = (
		select(Horario)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			horarios_insertados = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return horarios_insertados

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_horario: int, datos_horario: dict) -> Horario | None:
	sql = (
		update(Horario)
		.where(Horario.id == codigo_horario)
		.values(datos_horario)
		.returning(Horario)
	)

	orm_stmt = (
		select(Horario)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			horario_actualizado = sesion.execute(orm_stmt).scalars().one_or_none()
			sesion.commit()
			return horario_actualizado

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def borrar(id_horarios: list[int]) -> list[int]:
	sql = (
		delete(Horario)
		.where(Horario.id.in_(id_horarios))
		.returning(Horario.id)
	)

	with get_sesion() as sesion:
		id_horarios_eliminados = sesion.execute(sql).scalars().all()
		sesion.commit()
		return id_horarios_eliminados
