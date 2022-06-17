from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_grupo
from institutoapi.excepciones.genericas import CodigoNoEncontradoError
from institutoapi.middleware import auth_middleware as auth
from institutoapi.modelos import Grupo
from institutoapi.respuestas import responses
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/grupos",
	tags=["grupos"],
	responses={
		**responses.no_autorizado,
	},
)


@router.get(
	path="/",
	response_model=list[Grupo],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.sin_registros,
	},
)
def get_todos_los_grupos(
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupos_seleccionados = dao_grupo.seleccionar_todos(sesion_bbdd)
	if not grupos_seleccionados:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return grupos_seleccionados


@router.get(
	path="/{codigo_grupo}",
	response_model=Grupo,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.id_no_encontrado,
	},
)
def get_grupo_por_codigo(
	codigo_grupo: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupo_seleccionado = dao_grupo.seleccionar_por_codigo(sesion_bbdd, codigo_grupo)
	if not grupo_seleccionado:
		raise CodigoNoEncontradoError(codigo_grupo)
	return grupo_seleccionado


@router.post(
	path="/",
	response_model=list[Grupo],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.error_integridad_bbdd,
	},
)
def crear_grupos(
	grupos_nuevos: list[Grupo],
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupos_procesados = [grupo.dict() for grupo in grupos_nuevos]
	grupos_creados = dao_grupo.insertar(sesion_bbdd, grupos_procesados)
	return grupos_creados


@router.put(
	path="/{codigo_grupo}",
	response_model=Grupo,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def actualizar_grupo_por_codigo(
	codigo_grupo: str,
	grupo_editado: Grupo,
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupo_actualizado = dao_grupo.actualizar_por_codigo(sesion_bbdd, codigo_grupo, grupo_editado.dict())
	if not grupo_actualizado:
		raise CodigoNoEncontradoError(codigo_grupo)
	return grupo_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def borrar_grupos(
	codigos_grupos: list[str],
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupos_eliminados = dao_grupo.borrar(sesion_bbdd, codigos_grupos)
	if not grupos_eliminados:
		raise CodigoNoEncontradoError(codigos_grupos)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_grupo}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def borrar_grupo_por_codigo(
	codigo_grupo: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	grupo_eliminado = dao_grupo.borrar(sesion_bbdd, [codigo_grupo])
	if not grupo_eliminado:
		raise CodigoNoEncontradoError(codigo_grupo)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
