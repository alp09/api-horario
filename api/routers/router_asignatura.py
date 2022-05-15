from fastapi import APIRouter, status, Response

from api.esquemas import Asignatura
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.servicios import servicio_asignatura


# Definición del router
router = APIRouter(
	prefix="/asignaturas",
	tags=["asignaturas"]
)


@router.get("/", response_model=list[Asignatura], status_code=status.HTTP_200_OK)
def get_todos():
	if resultado := servicio_asignatura.get_todas():
		return resultado
	else:
		raise SinRegistros


@router.get("/{codigo_asignatura}", response_model=Asignatura, status_code=status.HTTP_200_OK)
def get_por_codigo(codigo_asignatura: str):
	if resultado := servicio_asignatura.get_por_codigo(codigo_asignatura):
		return resultado
	else:
		raise CodigoNoEncontrado(codigo_asignatura)


@router.post("/", response_model=list[Asignatura], status_code=status.HTTP_201_CREATED)
def insertar(asignaturas_nuevas: list[Asignatura]):
	return servicio_asignatura.insertar(asignaturas_nuevas)


@router.put("/{codigo_asignatura}", response_model=Asignatura, status_code=status.HTTP_200_OK)
def actualizar_por_codigo(codigo_asignatura: str, asignatura_editada: Asignatura):
	asignatura_actualizada = servicio_asignatura.actualizar_uno(codigo_asignatura, asignatura_editada)
	if not asignatura_actualizada:
		raise CodigoNoEncontrado(codigo_asignatura)
	return asignatura_actualizada


@router.delete("/", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar(codigos_asignaturas: list[str]):
	asignatuas_eliminadas = servicio_asignatura.borrar(codigos_asignaturas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontrado(codigos_asignaturas)


@router.delete("/{codigo_asignatura}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_por_codigo(codigo_asignatura: str):
	asignatura_eliminada = servicio_asignatura.borrar_uno(codigo_asignatura)
	if not asignatura_eliminada:
		raise CodigoNoEncontrado(codigo_asignatura)
