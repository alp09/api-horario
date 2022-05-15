from fastapi import APIRouter, status, Response

from api.esquemas import Grupo
from api.excepciones.genericas import SinRegistros, CodigoNoEncontrado
from api.servicios import servicio_grupo


# Definición del router
router = APIRouter(
	prefix="/grupos",
	tags=["grupos"]
)


@router.get("/", response_model=list[Grupo], status_code=status.HTTP_200_OK)
def get_todos():
	if resultado := servicio_grupo.get_todos():
		return resultado
	else:
		raise SinRegistros


@router.get("/{codigo_grupo}", response_model=Grupo, status_code=status.HTTP_200_OK)
def get_por_codigo(codigo_grupo: str):
	if resultado := servicio_grupo.get_por_codigo(codigo_grupo):
		return resultado
	else:
		raise CodigoNoEncontrado(codigo_grupo)


@router.post("/", response_model=list[Grupo], status_code=status.HTTP_201_CREATED)
def insertar(grupos_nuevos: list[Grupo]):
	return servicio_grupo.insertar(grupos_nuevos)


@router.put("/{codigo_grupo}", response_model=Grupo, status_code=status.HTTP_200_OK)
def actualizar_por_codigo(codigo_grupo: str, grupo_editado: Grupo):
	grupo_actualizado = servicio_grupo.actualizar_uno(codigo_grupo, grupo_editado)
	if not grupo_actualizado:
		raise CodigoNoEncontrado(codigo_grupo)
	return grupo_actualizado


@router.delete("/", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar(codigos_grupos: list[str]):
	grupos_eliminados = servicio_grupo.borrar(codigos_grupos)
	if not grupos_eliminados:
		raise CodigoNoEncontrado(codigos_grupos)


@router.delete("/{codigo_grupo}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_por_codigo(codigo_grupo: str):
	grupo_eliminado = servicio_grupo.borrar_uno(codigo_grupo)
	if not grupo_eliminado:
		raise CodigoNoEncontrado(codigo_grupo)
