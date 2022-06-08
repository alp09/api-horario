from fastapi import APIRouter, status, Depends, Response

from institutoapi.esquemas import Profesor
from institutoapi.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from institutoapi.excepciones.profesor import EmailProfesorNoEncontradoError
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from institutoapi.servicios import servicio_profesor


# Definición del router
router = APIRouter(
	prefix="/profesores",
	tags=["profesores"]
)


@router.get(
	path="/",
	response_model=list[Profesor],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todos_los_profesores():
	profesores_seleccionados = servicio_profesor.get_todos()
	if not profesores_seleccionados:
		raise SinRegistros
	return profesores_seleccionados


@router.get(
	path="/{codigo_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_profesor_por_codigo(codigo_profesor: str):
	profesor_seleccionado = servicio_profesor.get_por_codigo(codigo_profesor)
	if not profesor_seleccionado:
		raise CodigoNoEncontrado(codigo_profesor)
	return profesor_seleccionado


@router.get(
	path="/email/{email_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_profesor_por_email(email_profesor: str):
	profesor_seleccionado = servicio_profesor.get_por_email(email_profesor)
	if not profesor_seleccionado:
		raise EmailProfesorNoEncontradoError(email_profesor)
	return profesor_seleccionado


@router.post(
	path="/",
	response_model=list[Profesor],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_profesores(profesores_nuevos: list[Profesor]):
	profesores_creados = servicio_profesor.crear_profesores(profesores_nuevos)
	return profesores_creados


@router.put(
	path="/{codigo_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_profesor_por_codigo(codigo_profesor: str, profesor_editado: Profesor):
	profesor_actualizado = servicio_profesor.actualizar_por_codigo(codigo_profesor, profesor_editado)
	if not profesor_actualizado:
		raise CodigoNoEncontrado(codigo_profesor)
	return profesor_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_profesores(codigos_profesores: list[str]):
	profesores_eliminados = servicio_profesor.borrar_profesores(codigos_profesores)
	if not profesores_eliminados:
		raise CodigoNoEncontrado(codigos_profesores)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_profesor}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_profesor_por_codigo(codigo_profesor: str):
	profesor_eliminado = servicio_profesor.borrar_por_codigo(codigo_profesor)
	if not profesor_eliminado:
		raise CodigoNoEncontrado(codigo_profesor)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
