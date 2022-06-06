from fastapi import APIRouter, status, Depends, Response

from api.esquemas import Asignatura
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from api.servicios import servicio_asignatura


# Definición del router
router = APIRouter(
	prefix="/asignaturas",
	tags=["asignaturas"]
)


@router.get(
	path="/",
	response_model=list[Asignatura],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todas_las_asignaturas():
	asignaturas_encontradas = servicio_asignatura.get_todas()
	if not asignaturas_encontradas:
		raise SinRegistros
	return asignaturas_encontradas


@router.get(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_asignatura_por_codigo(codigo_asignatura: str):
	asignatura_encontrada = servicio_asignatura.get_por_codigo(codigo_asignatura)
	if not asignatura_encontrada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return asignatura_encontrada


@router.post(
	path="/",
	response_model=list[Asignatura],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_asignaturas(asignaturas_nuevas: list[Asignatura]):
	asignaturas_creadas = servicio_asignatura.crear_aulas(asignaturas_nuevas)
	return asignaturas_creadas


@router.put(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_asignatura_por_codigo(codigo_asignatura: str, asignatura_editada: Asignatura):
	asignatura_actualizada = servicio_asignatura.actualizar_por_codigo(codigo_asignatura, asignatura_editada)
	if not asignatura_actualizada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return asignatura_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_asignatuas(codigos_asignaturas: list[str]):
	asignatuas_eliminadas = servicio_asignatura.borrar_asignaturas(codigos_asignaturas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontrado(codigos_asignaturas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_asignatura}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_asignatua_por_codigo(codigo_asignatura: str):
	asignatura_eliminada = servicio_asignatura.borrar_por_codigo(codigo_asignatura)
	if not asignatura_eliminada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
