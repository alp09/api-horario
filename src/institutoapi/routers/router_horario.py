from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_horario
from institutoapi.bbdd.modelos import HorarioRequest, HorarioResponse
from institutoapi.excepciones.genericas import CodigoNoEncontrado
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/horarios",
	tags=["horarios"],
)


@router.get(
	path="/",
	response_model=list[HorarioResponse],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
)
def get_todos_los_horarios(
	sesion_bbdd: Session = Depends(get_sesion)
):
	horarios_encontrados = dao_horario.seleccionar_todos(sesion_bbdd)
	if not horarios_encontrados:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return horarios_encontrados


@router.post(
	path="/",
	response_model=list[HorarioResponse],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_logeado)],
)
def crear_horarios(
	horarios_nuevos: list[HorarioRequest],
	sesion_bbdd: Session = Depends(get_sesion)
):
	horarios_procesados = [horario.dict() for horario in horarios_nuevos]
	horarios_creados = dao_horario.insertar(sesion_bbdd, horarios_procesados)
	return horarios_creados


@router.put(
	path="/{id_horario}",
	response_model=HorarioResponse,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)],
)
def actualizar_horario_por_id(
	id_horario: int,
	horario_editado: HorarioRequest,
	sesion_bbdd: Session = Depends(get_sesion)
):
	horario_actualizado = dao_horario.actualizar_por_codigo(sesion_bbdd, id_horario, horario_editado.dict())
	if not horario_actualizado:
		raise CodigoNoEncontrado(id_horario)
	return horario_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)],
)
def borrar_horarios(
	id_horarios: list[int],
	sesion_bbdd: Session = Depends(get_sesion)
):
	horarios_eliminados = dao_horario.borrar(sesion_bbdd, id_horarios)
	if not horarios_eliminados:
		raise CodigoNoEncontrado(id_horarios)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{id_horario}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)],
)
def borrar_horario_por_id(
	id_horario: int,
	sesion_bbdd: Session = Depends(get_sesion)
):
	horario_eliminado = dao_horario.borrar(sesion_bbdd, [id_horario])
	if not horario_eliminado:
		raise CodigoNoEncontrado(id_horario)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
