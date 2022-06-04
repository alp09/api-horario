from fastapi import APIRouter, status

from api.esquemas import ReservaIn, ReservaOut
from api.excepciones.genericas import CodigoNoEncontrado, SinRegistros
from api.servicios import servicio_reserva


# Definición del router
router = APIRouter(
	prefix="/reservas",
	tags=["reservas"]
)


@router.get("/", response_model=list[ReservaOut], status_code=status.HTTP_200_OK)
def get_todas_las_reservas():
	reservas_encontradas = servicio_reserva.get_todas()
	if not reservas_encontradas:
		raise SinRegistros
	return reservas_encontradas


@router.get("/{id_reserva}", response_model=ReservaOut, status_code=status.HTTP_200_OK)
def get_reserva_por_id(id_reserva: int):
	reserva_encontrada = servicio_reserva.get_por_id(id_reserva)
	if not reserva_encontrada:
		raise CodigoNoEncontrado(id_reserva)
	return reserva_encontrada


@router.post("/", response_model=list[ReservaOut], status_code=status.HTTP_201_CREATED)
def crear_reservas(reservas_nuevas: list[ReservaIn]):
	reserva_creada = servicio_reserva.crear_reservas(reservas_nuevas)
	return reserva_creada


@router.put("/{id_reserva}", response_model=list[ReservaOut], status_code=status.HTTP_200_OK)
def actualizar_reserva_por_id(id_reserva: int, reserva_editada: ReservaIn):
	reserva_actualizada = servicio_reserva.actualizar_por_id(id_reserva, reserva_editada)
	if not reserva_actualizada:
		raise CodigoNoEncontrado(id_reserva)
	return reserva_actualizada


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def borrar_reservas(id_reservas: list[int]):
	reservas_eliminadas = servicio_reserva.borrar_reservas(id_reservas)
	if not reservas_eliminadas:
		raise CodigoNoEncontrado(id_reservas)


@router.delete("/{id_reserva}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_reserva_por_id(id_reserva: int):
	reserva_eliminada = servicio_reserva.borrar_por_id(id_reserva)
	if not reserva_eliminada:
		raise CodigoNoEncontrado(id_reserva)
