from fastapi import APIRouter, status, Depends, Response

from api.esquemas import ReservaIn, ReservaOut, Profesor
from api.excepciones.auth import PermisosInsuficientesError
from api.excepciones.genericas import CodigoNoEncontrado, SinRegistros
from api.middleware.auth import validar_profesor_logeado
from api.servicios import servicio_reserva


# Definición del router
router = APIRouter(
	prefix="/reservas",
	tags=["reservas"]
)


@router.get(
	path="/",
	response_model=list[ReservaOut],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todas_las_reservas():
	reservas_encontradas = servicio_reserva.get_todas()
	if not reservas_encontradas:
		raise SinRegistros
	return reservas_encontradas


@router.get(
	path="/{id_reserva}",
	response_model=ReservaOut,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_reserva_por_id(id_reserva: int):
	reserva_encontrada = servicio_reserva.get_por_id(id_reserva)
	if not reserva_encontrada:
		raise CodigoNoEncontrado(id_reserva)
	return reserva_encontrada


@router.post(
	path="/",
	response_model=list[ReservaOut],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_logeado)]
)
def crear_reservas(
	reservas_nuevas: list[ReservaIn],
	profesor_logeado: Profesor = Depends(validar_profesor_logeado)
):
	# Si el profesor que crea las reservas no es admin, se comprueba que reservas_nuevas sean para el profesor logeado
	# Dicho de otra forma, no se pueden hacer reservas para otro profesor si no eres administrador
	if not validar_profesor_tiene_permiso(profesor_logeado, reservas_nuevas):
		raise PermisosInsuficientesError

	# Si no hay errores, crea las reservas
	reservas_creadas = servicio_reserva.crear_reservas(reservas_nuevas)
	return reservas_creadas


@router.put(
	path="/{id_reserva}",
	response_model=list[ReservaOut],
	status_code=status.HTTP_200_OK,
)
def actualizar_reserva_por_id(
	id_reserva: int,
	reserva_editada: ReservaIn,
	profesor_logeado: Profesor = Depends(validar_profesor_logeado)
):
	# Recoge la reserva que se quiere actualizar
	reserva_encontrada = servicio_reserva.get_por_id(id_reserva)

	# Si la reserva no existe, devuelve un error CodigoNoEncontrado
	if not reserva_encontrada:
		raise CodigoNoEncontrado(id_reserva)

	# Comprueba que el profesor que intenta modificar la reserva sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, [reserva_encontrada]):
		raise PermisosInsuficientesError

	# Si tiene permisos para actualizar la reserva, continua con la operación
	reserva_actualizada = servicio_reserva.actualizar_por_id(id_reserva, reserva_editada)
	return reserva_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
)
def borrar_reservas(
	id_reservas: list[int],
	profesor_logeado: Profesor = Depends(validar_profesor_logeado)
):
	# Busca las reservas que se quieren eliminar
	reservas_encontradas = servicio_reserva.get_por_lista_id(id_reservas)

	# Si no encuentra ninguna, devuelve un error
	if not reservas_encontradas:
		raise CodigoNoEncontrado(id_reservas)

	# Comprueba que el profesor que intenta borrar la reservas sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, reservas_encontradas):
		raise PermisosInsuficientesError

	# Si el profesor puede eliminar las reservas que ha indicado, ejecuta el proceso
	servicio_reserva.borrar_reservas(id_reservas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{id_reserva}",
	status_code=status.HTTP_204_NO_CONTENT
)
def borrar_reserva_por_id(
	id_reserva: int,
	profesor_logeado: Profesor = Depends(validar_profesor_logeado)
):
	# Recoge la reserva que se quiere borrar
	reserva_encontrada = servicio_reserva.get_por_id(id_reserva)

	# Si la reserva no existe, devuelve un error CodigoNoEncontrado
	if not reserva_encontrada:
		raise CodigoNoEncontrado(id_reserva)

	# Comprueba que el profesor que intenta borrar la reserva sea administrador o el profesor que hizo la reserva
	if not validar_profesor_tiene_permiso(profesor_logeado, [reserva_encontrada]):
		raise PermisosInsuficientesError

	# Si tiene permisos para borrar la reserva, continua con la operación
	servicio_reserva.borrar_por_id(id_reserva)
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
