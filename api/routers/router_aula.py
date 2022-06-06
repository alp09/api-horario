from fastapi import APIRouter, status, Depends, Response

from api.esquemas import Aula
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from api.servicios import servicio_aula


# Definición del router
router = APIRouter(
	prefix="/aulas",
	tags=["aulas"]
)


@router.get(
	path="/",
	response_model=list[Aula],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todas_las_aulas():
	aulas_encontradas = servicio_aula.get_todas()
	if not aulas_encontradas:
		raise SinRegistros
	return aulas_encontradas


@router.get(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_aula_por_codigo(codigo_aula: str):
	aula_encontrada = servicio_aula.get_por_codigo(codigo_aula)
	if not aula_encontrada:
		raise CodigoNoEncontrado(codigo_aula)
	return aula_encontrada


@router.post(
	path="/",
	response_model=list[Aula],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_aulas(aulas_nuevas: list[Aula]):
	aulas_creadas = servicio_aula.crear_aulas(aulas_nuevas)
	return aulas_creadas


@router.put(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_aula_por_codigo(codigo_aula: str, aula_editada: Aula):
	aula_actualizada = servicio_aula.actualizar_por_codigo(codigo_aula, aula_editada)
	if not aula_actualizada:
		raise CodigoNoEncontrado(codigo_aula)
	return aula_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_aulas(codigos_aulas: list[str]):
	asignatuas_eliminadas = servicio_aula.borrar_aulas(codigos_aulas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontrado(codigos_aulas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_aula}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_aula_por_codigo(codigo_aula: str):
	aula_eliminada = servicio_aula.borrar_por_codigo(codigo_aula)
	if not aula_eliminada:
		raise CodigoNoEncontrado(codigo_aula)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
