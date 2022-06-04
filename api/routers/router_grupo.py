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
def get_todos_los_grupos():
	grupos_seleccionados = servicio_grupo.get_todos()
	if not grupos_seleccionados:
		raise SinRegistros
	return grupos_seleccionados


@router.get("/{codigo_grupo}", response_model=Grupo, status_code=status.HTTP_200_OK)
def get_grupo_por_codigo(codigo_grupo: str):
	grupo_seleccionado = servicio_grupo.get_todos()
	if not grupo_seleccionado:
		raise CodigoNoEncontrado(codigo_grupo)
	return grupo_seleccionado


@router.post("/", response_model=list[Grupo], status_code=status.HTTP_201_CREATED)
def crear_grupos(grupos_nuevos: list[Grupo]):
	grupos_creados = servicio_grupo.crear_grupos(grupos_nuevos)
	return grupos_creados


@router.put("/{codigo_grupo}", response_model=Grupo, status_code=status.HTTP_200_OK)
def actualizar_grupo_por_codigo(codigo_grupo: str, grupo_editado: Grupo):
	grupo_actualizado = servicio_grupo.actualizar_por_codigo(codigo_grupo, grupo_editado)
	if not grupo_actualizado:
		raise CodigoNoEncontrado(codigo_grupo)
	return grupo_actualizado


@router.delete("/", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_grupos(codigos_grupos: list[str]):
	grupos_eliminados = servicio_grupo.borrar_grupos(codigos_grupos)
	if not grupos_eliminados:
		raise CodigoNoEncontrado(codigos_grupos)


@router.delete("/{codigo_grupo}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
def borrar_grupo_por_codigo(codigo_grupo: str):
	grupo_eliminado = servicio_grupo.borrar_por_codigo(codigo_grupo)
	if not grupo_eliminado:
		raise CodigoNoEncontrado(codigo_grupo)
