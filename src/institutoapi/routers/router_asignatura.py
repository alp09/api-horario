from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_asignatura
from institutoapi.excepciones.genericas import CodigoNoEncontradoError
from institutoapi.middleware import auth_middleware as auth
from institutoapi.modelos import Asignatura
from institutoapi.respuestas import responses
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/asignaturas",
	tags=["asignaturas"],
	responses={
		**responses.no_autorizado,
	},
)


@router.get(
	path="/",
	response_model=list[Asignatura],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.sin_registros,
	},
)
def get_todas_las_asignaturas(
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignaturas_encontradas = dao_asignatura.seleccionar_todas(sesion_bbdd)
	if not asignaturas_encontradas:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return asignaturas_encontradas


@router.get(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_logeado)],
	responses={
		**responses.id_no_encontrado,
	},
)
def get_asignatura_por_codigo(
	codigo_asignatura: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignatura_encontrada = dao_asignatura.seleccionar_por_codigo(sesion_bbdd, codigo_asignatura)
	if not asignatura_encontrada:
		raise CodigoNoEncontradoError(codigo_asignatura)
	return asignatura_encontrada


@router.post(
	path="/",
	response_model=list[Asignatura],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.error_integridad_bbdd,
	},
)
def crear_asignaturas(
	asignaturas_nuevas: list[Asignatura],
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignaturas_procesadas = [asignatura.dict() for asignatura in asignaturas_nuevas]
	asignaturas_creadas = dao_asignatura.insertar(sesion_bbdd, asignaturas_procesadas)
	return asignaturas_creadas


@router.put(
	path="/{codigo_asignatura}",
	response_model=Asignatura,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def actualizar_asignatura_por_codigo(
	codigo_asignatura: str,
	asignatura_editada: Asignatura,
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignatura_actualizada = dao_asignatura.actualizar_por_codigo(sesion_bbdd, codigo_asignatura, asignatura_editada.dict())
	if not asignatura_actualizada:
		raise CodigoNoEncontradoError(codigo_asignatura)
	return asignatura_actualizada


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
def borrar_asignatuas(
	codigos_asignaturas: list[str],
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignaturas_eliminadas = dao_asignatura.borrar(sesion_bbdd, codigos_asignaturas)
	if not asignaturas_eliminadas:
		raise CodigoNoEncontradoError(codigos_asignaturas)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_asignatura}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(auth.validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def borrar_asignatua_por_codigo(
	codigo_asignatura: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	asignatura_eliminada = dao_asignatura.borrar(sesion_bbdd, [codigo_asignatura])
	if not asignatura_eliminada:
		raise CodigoNoEncontradoError(codigo_asignatura)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
