from fastapi import status, Depends, Response
from sqlmodel import Session

from institutoapi.bbdd import get_sesion
from institutoapi.bbdd.dao import dao_profesor
from institutoapi.excepciones.genericas import CodigoNoEncontradoError
from institutoapi.middleware.auth import validar_profesor_logeado, validar_profesor_es_admin
from institutoapi.modelos import Profesor
from institutoapi.respuestas import responses
from institutoapi.utils import APIRouter


# Definición del router
router = APIRouter(
	prefix="/profesores",
	tags=["profesores"],
	responses={
		**responses.no_autorizado,
	},
)


@router.get(
	path="/",
	response_model=list[Profesor],
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
	responses={
		**responses.sin_registros,
	},
)
def get_todos_los_profesores(
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesores_seleccionados = dao_profesor.seleccionar_todos(sesion_bbdd)
	if not profesores_seleccionados:
		return Response(status_code=status.HTTP_204_NO_CONTENT)
	return profesores_seleccionados


@router.get(
	path="/{codigo_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
	responses={
		**responses.id_no_encontrado
	}
)
def get_profesor_por_codigo(
	codigo_profesor: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesor_seleccionado = dao_profesor.seleccionar_por_codigo(sesion_bbdd, codigo_profesor)
	if not profesor_seleccionado:
		raise CodigoNoEncontradoError(codigo_profesor)
	return profesor_seleccionado


@router.get(
	path="/email/{email_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_logeado)],
	responses={
		**responses.id_no_encontrado,
	},
)
def get_profesor_por_email(
	email_profesor: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesor_seleccionado = dao_profesor.seleccionar_por_email(sesion_bbdd, email_profesor)
	if not profesor_seleccionado:
		raise CodigoNoEncontradoError(email_profesor)
	return profesor_seleccionado


@router.post(
	path="/",
	response_model=list[Profesor],
	status_code=status.HTTP_201_CREATED,
	dependencies=[Depends(validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.error_integridad_bbdd,
	},
)
def crear_profesores(
	profesores_nuevos: list[Profesor],
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesores_procesados = [profesor.dict() for profesor in profesores_nuevos]
	profesores_creados = dao_profesor.insertar(sesion_bbdd, profesores_procesados)
	return profesores_creados


@router.put(
	path="/{codigo_profesor}",
	response_model=Profesor,
	status_code=status.HTTP_200_OK,
	dependencies=[Depends(validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def actualizar_profesor_por_codigo(
	codigo_profesor: str,
	profesor_editado: Profesor,
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesor_actualizado = dao_profesor.actualizar_por_codigo(sesion_bbdd, codigo_profesor, profesor_editado.dict())
	if not profesor_actualizado:
		raise CodigoNoEncontradoError(codigo_profesor)
	return profesor_actualizado


@router.delete(
	path="/",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def borrar_profesores(
	codigos_profesores: list[str],
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesores_eliminados = dao_profesor.borrar(sesion_bbdd, codigos_profesores)
	if not profesores_eliminados:
		raise CodigoNoEncontradoError(codigos_profesores)
	return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
	path="/{codigo_profesor}",
	status_code=status.HTTP_204_NO_CONTENT,
	dependencies=[Depends(validar_profesor_es_admin)],
	responses={
		**responses.permisos_insuficientes,
		**responses.id_no_encontrado,
		**responses.error_integridad_bbdd,
	},
)
def borrar_profesor_por_codigo(
	codigo_profesor: str,
	sesion_bbdd: Session = Depends(get_sesion)
):
	profesor_eliminado = dao_profesor.borrar(sesion_bbdd, [codigo_profesor])
	if not profesor_eliminado:
		raise CodigoNoEncontradoError(codigo_profesor)
	return Response(status_code=status.HTTP_204_NO_CONTENT)
