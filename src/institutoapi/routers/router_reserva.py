from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_reserva
from institutoapi.modelos import ReservaRequest, ReservaResponse, Profesor
from institutoapi.excepciones.auth import PermisosInsuficientesError
from institutoapi.excepciones.genericas import CodigoNoEncontradoError
from institutoapi.middleware.auth import validar_profesor_logeado
from institutoapi.servicios import servicio_reserva
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/reservas",
	tags=["reservas"],
)


@router.get(
	path="/",
	response_model=list[ReservaResponse],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
)
def get_todas_las_reservas(
	sesion_bbdd: Session = Depends(get_sesion)
):
	reservas_encontradas = dao_reserva.seleccionar_todas(sesion_bbdd)
	if not reservas_encontradas:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return reservas_encontradas


@router.get(
	path="/{id_reserva}",
	response_model=ReservaResponse,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
)
def get_reserva_por_id(
	id_reserva: int,
	sesion_bbdd: Session = Depends(get_sesion)
):
	reserva_encontrada = dao_reserva.seleccionar_por_id(sesion_bbdd, id_reserva)
	if not reserva_encontrada:
		raise CodigoNoEncontradoError(id_reserva)
	return reserva_encontrada


@router.post(
	path="/",
	response_model=list[ReservaResponse],
	status_code=status.HTTP_201_CREATED,
)
def crear_reservas(
	reservas_nuevas: list[ReservaRequest],
	profesor_logeado: Profesor = Depends(validar_profesor_logeado),
	sesion_bbdd: Session = Depends(get_sesion)
):
	# Si el profesor que crea las reservas no es admin, se comprueba que reservas_nuevas sean para el profesor logeado
	# Dicho de otra forma, no se pueden hacer reservas para otro profesor si no eres administrador
	if not validar_profesor_tiene_permiso(profesor_logeado, reservas_nuevas):
		raise PermisosInsuficientesError

	# Si no hay errores, crea las reservas
	reservas_creadas = servicio_reserva.insertar(sesion_bbdd, reservas_nuevas)
	return reservas_creadas


@router.put(
	path="/{id_reserva}",
	response_model=list[ReservaResponse],
	status_code=status.HTTP_200_OK,
)
def actualizar_reserva_por_id(
	id_reserva: int,
	reserva_editada: ReservaRequest,
	profesor_logeado: Profesor = Depends(validar_profesor_logeado),
	sesion_bbdd: Session = Depends(get_sesion)
):
	# Recoge la reserva que se quiere actualizar
	reserva_encontrada = dao_reserva.seleccionar_por_id(sesion_bbdd, id_reserva)

	# Si la reserva no existe, devuelve un error CodigoNoEncontradoError
	if not reserva_encontrada:
		raise CodigoNoEncontradoError(id_reserva)

	# Comprueba que el profesor que intenta modificar la reserva sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, [reserva_encontrada]):
		raise PermisosInsuficientesError

	# Si tiene permisos para actualizar la reserva, continua con la operación
	reserva_actualizada = servicio_reserva.actualizar_por_codigo(sesion_bbdd, id_reserva, reserva_editada)
	return reserva_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
)
def borrar_reservas(
	id_reservas: list[int],
	profesor_logeado: Profesor = Depends(validar_profesor_logeado),
	sesion_bbdd: Session = Depends(get_sesion)
):
	# Busca las reservas que se quieren eliminar
	reservas_encontradas = dao_reserva.seleccionar_por_lista_id(sesion_bbdd, id_reservas)

	# Si no encuentra ninguna, devuelve un error
	if not reservas_encontradas:
		raise CodigoNoEncontradoError(id_reservas)

	# Comprueba que el profesor que intenta borrar la reservas sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, reservas_encontradas):
		raise PermisosInsuficientesError

	# Si el profesor puede eliminar las reservas que ha indicado, ejecuta el proceso
	dao_reserva.borrar(sesion_bbdd, id_reservas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{id_reserva}",
	status_code=status.HTTP_204_NO_CONTENT
)
def borrar_reserva_por_id(
	id_reserva: int,
	profesor_logeado: Profesor = Depends(validar_profesor_logeado),
	sesion_bbdd: Session = Depends(get_sesion)
):
	# Recoge la reserva que se quiere borrar
	reserva_encontrada = dao_reserva.seleccionar_por_id(sesion_bbdd, id_reserva)

	# Si la reserva no existe, devuelve un error CodigoNoEncontradoError
	if not reserva_encontrada:
		raise CodigoNoEncontradoError(id_reserva)

	# Comprueba que el profesor que intenta borrar la reserva sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, [reserva_encontrada]):
		raise PermisosInsuficientesError

	# Si tiene permisos para borrar la reserva, continua con la operación
	dao_reserva.borrar(sesion_bbdd, [id_reserva])
	return Response(status_code=status.HTTP_204_NO_CONTENT)


def validar_profesor_tiene_permiso(profesor: Profesor, reservas: list) -> bool:
	"""
	Valida que el profesor esté autorizado para operar sobre las reservas indicadas

	:param profesor: el profesor que intenta trabajar con las reservas
	:param reservas: las reservas que se van a alterar
	:return: True si el profesor tiene permisos para realizar la operación o False si no
	"""
	# Si el profesor tiene permisos de administrador, devuelve True
	if profesor.es_admin:
		return True

	# Si no es administrador se comprueba que el profesor sea el propietario de las reservas
	reservas_no_autorizadas = [reserva for reserva in reservas if reserva.codigo_profesor != profesor.codigo]

	# Si no está autorizado para alguna de las reservas devuelve False
	return False if reservas_no_autorizadas else True
