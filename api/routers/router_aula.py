from fastapi import APIRouter, status, Response

from api.esquemas import Aula
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.servicios import servicio_aula


# Definición del router
router = APIRouter(
	prefix="/aulas",
	tags=["aulas"]
)


@router.get("/", response_model=list[Aula], status_code=status.HTTP_200_OK)
def get_todos():
	if resultado := servicio_aula.get_todas():
		return resultado
	else:
		raise SinRegistros


@router.get("/{codigo_aula}", response_model=Aula, status_code=status.HTTP_200_OK)
def get_por_codigo(codigo_aula: str):
	if resultado := servicio_aula.get_por_codigo(codigo_aula):
		return resultado
	else:
		raise CodigoNoEncontrado(codigo_aula)


@router.post("/", response_model=list[Aula], status_code=status.HTTP_201_CREATED)
def insertar(aulas_nuevas: list[Aula]):
	return servicio_aula.insertar(aulas_nuevas)


@router.put("/{codigo_aula}", response_model=Aula, status_code=status.HTTP_200_OK)
def actualizar_por_codigo(codigo_aula: str, aula_editada: Aula):
	aula_actualizada = servicio_aula.actualizar_uno(codigo_aula, aula_editada)
	if not aula_actualizada:
		raise CodigoNoEncontrado(codigo_aula)
	return aula_actualizada


@router.delete("/", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar(codigos_aulas: list[str]):
	asignatuas_eliminadas = servicio_aula.borrar(codigos_aulas)
	if not asignatuas_eliminadas:
		raise CodigoNoEncontrado(codigos_aulas)


@router.delete("/{codigo_aula}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_por_codigo(codigo_aula: str):
	aula_eliminada = servicio_aula.borrar_uno(codigo_aula)
	if not aula_eliminada:
		raise CodigoNoEncontrado(codigo_aula)
