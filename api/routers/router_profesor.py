from fastapi import APIRouter, status, Response

from api.esquemas import Profesor
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.excepciones.profesor import EmailProfesorNoEncontradoError
from api.servicios import servicio_profesor


# Definición del router
router = APIRouter(
	prefix="/profesores",
	tags=["profesores"]
)


@router.get("/", response_model=list[Profesor], status_code=status.HTTP_200_OK)
def get_todos_los_profesores():
	profesores_seleccionados = servicio_profesor.get_todos()
	if not profesores_seleccionados:
		raise SinRegistros
	return profesores_seleccionados


@router.get("/{codigo_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_profesor_por_codigo(codigo_profesor: str):
	profesor_seleccionado = servicio_profesor.get_por_codigo(codigo_profesor)
	if not profesor_seleccionado:
		raise CodigoNoEncontrado(codigo_profesor)
	return profesor_seleccionado


@router.get("/email/{email_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def get_profesor_por_email(email_profesor: str):
	profesor_seleccionado = servicio_profesor.get_por_email(email_profesor)
	if not profesor_seleccionado:
		raise EmailProfesorNoEncontradoError(email_profesor)
	return profesor_seleccionado


@router.post("/", response_model=list[Profesor], status_code=status.HTTP_201_CREATED)
def crear_profesores(profesores_nuevos: list[Profesor]):
	profesores_creados = servicio_profesor.crear_profesores(profesores_nuevos)
	return profesores_creados


@router.put("/{codigo_profesor}", response_model=Profesor, status_code=status.HTTP_200_OK)
def actualizar_profesor_por_codigo(codigo_profesor: str, profesor_editado: Profesor):
	profesor_actualizado = servicio_profesor.actualizar_por_codigo(codigo_profesor, profesor_editado)
	if not profesor_actualizado:
		raise CodigoNoEncontrado(codigo_profesor)
	return profesor_actualizado


@router.delete("/", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_profesores(codigos_profesores: list[str]):
	profesores_eliminados = servicio_profesor.borrar_profesores(codigos_profesores)
	if not profesores_eliminados:
		raise CodigoNoEncontrado(codigos_profesores)


@router.delete("/{codigo_profesor}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_profesor_por_codigo(codigo_profesor: str):
	profesor_eliminado = servicio_profesor.borrar_por_codigo(codigo_profesor)
	if not profesor_eliminado:
		raise CodigoNoEncontrado(codigo_profesor)
