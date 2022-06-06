from fastapi import APIRouter, status, Depends, Response

from api.esquemas import HorarioIn, HorarioOut
from api.excepciones.genericas import CodigoNoEncontrado, SinRegistros
from api.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from api.servicios import servicio_horario


# Definición del router
router = APIRouter(
	prefix="/horarios",
	tags=["horarios"]
)


@router.get(
	path="/",
	response_model=list[HorarioOut],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todos_los_horarios():
	horarios_encontrados = servicio_horario.get_todos()
	if not horarios_encontrados:
		raise SinRegistros
	return horarios_encontrados


@router.post(
	path="/",
	response_model=list[HorarioOut],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_logeado)]
)
def crear_horarios(horarios_nuevos: list[HorarioIn]):
	horarios_creados = servicio_horario.crear_horarios(horarios_nuevos)
	return horarios_creados


@router.put(
	path="/{id_horario}",
	response_model=HorarioOut,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_horario_por_id(id_horario: int, horario_editado: HorarioIn):
	horario_actualizado = servicio_horario.actualizar_por_id(id_horario, horario_editado)
	if not horario_actualizado:
		raise CodigoNoEncontrado(id_horario)
	return horario_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_horarios(id_horarios: list[int]):
	horarios_eliminados = servicio_horario.borrar_horarios(id_horarios)
	if not horarios_eliminados:
		raise CodigoNoEncontrado(id_horarios)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{id_horario}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_horario_por_id(id_horario: int):
	horario_eliminado = servicio_horario.borrar_por_id(id_horario)
	if not horario_eliminado:
		raise CodigoNoEncontrado(id_horario)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
