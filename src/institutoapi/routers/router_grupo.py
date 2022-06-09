from fastapi import APIRouter, status, Depends, Response

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_grupo
from institutoapi.bbdd.modelos import Grupo
from institutoapi.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin


# Definición del router
router = APIRouter(
	prefix="/grupos",
	tags=["grupos"]
)


@router.get(
	path="/",
	response_model=list[Grupo],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_todos_los_grupos(
	sesion_bbdd=Depends(get_sesion)
):
	grupos_seleccionados = dao_grupo.seleccionar_todos(sesion_bbdd)
	if not grupos_seleccionados:
		raise SinRegistros
	return grupos_seleccionados


@router.get(
	path="/{codigo_grupo}",
	response_model=Grupo,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)]
)
def get_grupo_por_codigo(
	codigo_grupo: str,
	sesion_bbdd=Depends(get_sesion)
):
	grupo_seleccionado = dao_grupo.seleccionar_por_codigo(sesion_bbdd, codigo_grupo)
	if not grupo_seleccionado:
		raise CodigoNoEncontrado(codigo_grupo)
	return grupo_seleccionado


@router.post(
	path="/",
	response_model=list[Grupo],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def crear_grupos(
	grupos_nuevos: list[Grupo],
	sesion_bbdd=Depends(get_sesion)
):
	grupos_procesados = [grupo.dict() for grupo in grupos_nuevos]
	grupos_creados = dao_grupo.insertar(sesion_bbdd, grupos_procesados)
	return grupos_creados


@router.put(
	path="/{codigo_grupo}",
	response_model=Grupo,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def actualizar_grupo_por_codigo(
	codigo_grupo: str,
	grupo_editado: Grupo,
	sesion_bbdd=Depends(get_sesion)
):
	grupo_actualizado = dao_grupo.actualizar_por_codigo(sesion_bbdd, codigo_grupo, grupo_editado.dict())
	if not grupo_actualizado:
		raise CodigoNoEncontrado(codigo_grupo)
	return grupo_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_grupos(
	codigos_grupos: list[str],
	sesion_bbdd=Depends(get_sesion)
):
	grupos_eliminados = dao_grupo.borrar(sesion_bbdd, codigos_grupos)
	if not grupos_eliminados:
		raise CodigoNoEncontrado(codigos_grupos)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_grupo}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)]
)
def borrar_grupo_por_codigo(
	codigo_grupo: str,
	sesion_bbdd=Depends(get_sesion)
):
	grupo_eliminado = dao_grupo.borrar(sesion_bbdd, [codigo_grupo])
	if not grupo_eliminado:
		raise CodigoNoEncontrado(codigo_grupo)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
