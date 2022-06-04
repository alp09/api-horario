from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError, InternalError

from api.bbdd import get_sesion
from api.bbdd.tablas import Reserva
from api.excepciones.bbdd import IntegridadError, DatosInvalidosError


def seleccionar_todos() -> list[Reserva]:
	sql = select(Reserva)

	with get_sesion() as sesion:
		reservas_seleccionadas = sesion.execute(sql).scalars().all()
		return reservas_seleccionadas


def seleccionar_por_id(id_reserva: int) -> Reserva | None:
	sql = (
		select(Reserva)
		.where(Reserva.id == id_reserva)
	)

	with get_sesion() as sesion:
		reserva_seleccionada = sesion.execute(sql).scalars().one_or_none()
		return reserva_seleccionada


def insertar(datos_reservas: list[dict]) -> list[Reserva]:
	sql = (
		insert(Reserva)
		.values(datos_reservas)
		.returning(Reserva)
	)

	orm_stmt = (
		select(Reserva)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			reservas_creadas = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return reservas_creadas

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def actualizar_por_codigo(codigo_reserva: int, datos_reserva: dict) -> Reserva | None:
	sql = (
		update(Reserva)
		.where(Reserva.id == codigo_reserva)
		.values(datos_reserva)
		.returning(Reserva)
	)

	orm_stmt = (
		select(Reserva)
		.from_statement(sql)
		.execution_options(populate_existing=True)
	)

	try:
		with get_sesion() as sesion:
			reservas_actualizadas = sesion.execute(orm_stmt).scalars().all()
			sesion.commit()
			return reservas_actualizadas

	except IntegrityError as excepcion:
		raise IntegridadError(excepcion.orig.pgerror)
	except InternalError as excepcion:
		raise DatosInvalidosError(excepcion.orig.pgerror)


def borrar(id_reservas: list[int]) -> list[int]:
	sql = (
		delete(Reserva)
		.where(Reserva.id.in_(id_reservas))
		.returning(Reserva.id)
	)

	with get_sesion() as sesion:
		reservas_eliminadas = sesion.execute(sql).scalars().all()
		sesion.commit()
		return reservas_eliminadas
