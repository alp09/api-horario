from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_aula
from institutoapi.excepciones.genericas import CodigoNoEncontradoError
from institutoapi.middleware import auth_middleware as auth
from institutoapi.modelos import Aula
from institutoapi.respuestas import responses
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/aulas",
	tags=["aulas"],
	responses={
		**responses.no_autorizado,
	},
)


@router.get(
	path="/",
	response_model=list[Aula],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.sin_registros,
	},
)
def get_todas_las_aulas(
	sesion_bbdd: Session = Depends(get_sesion)
):
	aulas_encontradas = dao_aula.seleccionar_todas(sesion_bbdd)
	if not aulas_encontradas:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return aulas_encontradas


@router.get(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.id_no_encontrado,
	},
)
def get_aula_por_codigo(
	codigo_aula: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	aula_encontrada = dao_aula.seleccionar_por_codigo(sesion_bbdd, codigo_aula)
	if not aula_encontrada:
		raise CodigoNoEncontradoError(codigo_aula)
	return aula_encontrada


@router.post(
	path="/",
	response_model=list[Aula],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.error_integridad_bbdd,
	}
)
def crear_aulas(
	aulas_nuevas: list[Aula],
	sesion_bbdd: Session = Depends(get_sesion)
):
	aulas_procesadas = [aula.dict() for aula in aulas_nuevas]
	aulas_creadas = dao_aula.insertar(sesion_bbdd, aulas_procesadas)
	return aulas_creadas


@router.put(
	path="/{codigo_aula}",
	response_model=Aula,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	}
)
def actualizar_aula_por_codigo(
	codigo_aula: str,
	aula_editada: Aula,
	sesion_bbdd: Session = Depends(get_sesion)
):
	aula_actualizada = dao_aula.actualizar_por_codigo(sesion_bbdd, codigo_aula, aula_editada.dict())
	if not aula_actualizada:
		raise CodigoNoEncontradoError(codigo_aula)
	return aula_actualizada


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	}
)
def borrar_aulas(
	codigos_aulas: list[str],
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignatuas_eliminadas = dao_aula.borrar(sesion_bbdd, codigos_aulas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontradoError(codigos_aulas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_aula}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	}
)
def borrar_aula_por_codigo(
	codigo_aula: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	aula_eliminada = dao_aula.borrar(sesion_bbdd, [codigo_aula])
	if not aula_eliminada:
		raise CodigoNoEncontradoError(codigo_aula)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
