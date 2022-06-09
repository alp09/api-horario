from fastapi import APIRouter, status, Depends, Response

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_aula
from institutoapi.bbdd.modelos import Aula
from institutoapi.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin


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
def get_todas_las_aulas(
	sesion_bbdd=Depends(get_sesion)
):
	aulas_encontradas = dao_aula.seleccionar_todas(sesion_bbdd)
	if not aulas_encontradas:
		raise SinRegistros
	return aulas_encontradas


@router.get(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_aula_por_codigo(
	codigo_aula: str,
	sesion_bbdd=Depends(get_sesion)
):
	aula_encontrada = dao_aula.seleccionar_por_codigo(sesion_bbdd, codigo_aula)
	if not aula_encontrada:
		raise CodigoNoEncontrado(codigo_aula)
	return aula_encontrada


@router.post(
	path="/",
	response_model=list[Aula],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_aulas(
	aulas_nuevas: list[Aula],
	sesion_bbdd=Depends(get_sesion)
):
	aulas_procesadas = [aula.dict() for aula in aulas_nuevas]
	aulas_creadas = dao_aula.insertar(sesion_bbdd, aulas_procesadas)
	return aulas_creadas


@router.put(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_aula_por_codigo(
	codigo_aula: str,
	aula_editada: Aula,
	sesion_bbdd=Depends(get_sesion)
):
	aula_actualizada = dao_aula.actualizar_por_codigo(sesion_bbdd, codigo_aula, aula_editada.dict())
	if not aula_actualizada:
		raise CodigoNoEncontrado(codigo_aula)
	return aula_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_aulas(
	codigos_aulas: list[str],
	sesion_bbdd=Depends(get_sesion)
):
	asignatuas_eliminadas = dao_aula.borrar(sesion_bbdd, codigos_aulas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontrado(codigos_aulas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_aula}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_aula_por_codigo(
	codigo_aula: str,
	sesion_bbdd=Depends(get_sesion)
):
	aula_eliminada = dao_aula.borrar(sesion_bbdd, [codigo_aula])
	if not aula_eliminada:
		raise CodigoNoEncontrado(codigo_aula)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
