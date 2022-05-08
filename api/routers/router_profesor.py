from fastapi import APIRouter, status

from api.esquemas.profesor import *
from api.excepciones.profesor import *
from api.servicios import servicio_profesor


# Definición del router
router = APIRouter(
	prefix="/profesores",
	tags=["profesores"]
)


@router.get("/", response_model=list[Profesor], status_code=status.HTTP_200_OK)
def get_todos():
	if resultado := servicio_profesor.get_todos():
		return resultado
	else:
		raise NoProfesoresEncontradosError


@router.get("/{codigo_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_por_codigo_profesor(codigo_profesor: str):
	if resultado := servicio_profesor.get_por_codigo(codigo_profesor):
		return resultado
	else:
		raise CodigoProfesorNoEncontradoError(codigo_profesor)


@router.get("/email/{email_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_por_email(email_profesor: str):
	if resultado := servicio_profesor.get_por_email(email_profesor):
		return resultado
	else:
		raise EmailProfesorNoEncontradoError(email_profesor)


@router.post("/", response_model=list[Profesor], status_code=status.HTTP_201_CREATED)
def insertar(profesores_nuevos: list[Profesor]):
	return servicio_profesor.insertar(profesores_nuevos)


@router.put("/{codigo_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def actualizar_por_codigo(codigo_profesor: str, profesor_editado: Profesor):
	profesor_actualizado = servicio_profesor.actualizar_uno(codigo_profesor, profesor_editado)
	if not profesor_actualizado:
		raise CodigoProfesorNoEncontradoError(codigo_profesor)
	return profesor_actualizado


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def borrar(codigos_profesores: list[str]):
	profesores_eliminados = servicio_profesor.borrar(codigos_profesores)
	if not profesores_eliminados:
		raise CodigoProfesorNoEncontradoError(codigos_profesores)


@router.delete("/{codigo_profesor}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_por_codigo(codigo_profesor: str):
	profesor_eliminado = servicio_profesor.borrar_uno(codigo_profesor)
	if not profesor_eliminado:
		raise CodigoProfesorNoEncontradoError(codigo_profesor)
