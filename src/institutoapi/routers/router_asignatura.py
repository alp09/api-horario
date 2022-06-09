from fastapi import APIRouter, status, Depends, Response

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_asignatura
from institutoapi.bbdd.modelos import Asignatura
from institutoapi.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin


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
def get_todas_las_asignaturas(
	sesion_bbdd=Depends(get_sesion)
):
	asignaturas_encontradas = dao_asignatura.seleccionar_todas(sesion_bbdd)
	if not asignaturas_encontradas:
		raise SinRegistros
	return asignaturas_encontradas


@router.get(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_asignatura_por_codigo(
	codigo_asignatura: str,
	sesion_bbdd=Depends(get_sesion)
):
	asignatura_encontrada = dao_asignatura.seleccionar_por_codigo(sesion_bbdd, codigo_asignatura)
	if not asignatura_encontrada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return asignatura_encontrada


@router.post(
	path="/",
	response_model=list[Asignatura],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_asignaturas(
	asignaturas_nuevas: list[Asignatura],
	sesion_bbdd=Depends(get_sesion)
):
	asignaturas_procesadas = [asignatura.dict() for asignatura in asignaturas_nuevas]
	asignaturas_creadas = dao_asignatura.insertar(sesion_bbdd, asignaturas_procesadas)
	return asignaturas_creadas


@router.put(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_asignatura_por_codigo(
	codigo_asignatura: str,
	asignatura_editada: Asignatura,
	sesion_bbdd=Depends(get_sesion)
):
	asignatura_actualizada = dao_asignatura.actualizar_por_codigo(sesion_bbdd, codigo_asignatura, asignatura_editada.dict())
	if not asignatura_actualizada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return asignatura_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_asignatuas(
	codigos_asignaturas: list[str],
	sesion_bbdd=Depends(get_sesion)
):
	asignaturas_eliminadas = dao_asignatura.borrar(sesion_bbdd, codigos_asignaturas)
	if not asignaturas_eliminadas:
		raise CodigoNoEncontrado(codigos_asignaturas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_asignatura}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_asignatua_por_codigo(
	codigo_asignatura: str,
	sesion_bbdd=Depends(get_sesion)
):
	asignatura_eliminada = dao_asignatura.borrar(sesion_bbdd, [codigo_asignatura])
	if not asignatura_eliminada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
