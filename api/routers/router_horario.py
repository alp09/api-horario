from fastapi import APIRouter, status

from api.esquemas import Horario
from api.excepciones.genericas import CodigoNoEncontrado, SinRegistros
from api.servicios import servicio_horario


# Definición del router
router = APIRouter(
	prefix="/horarios",
	tags=["horarios"]
)


@router.get("/", response_model=list[Horario], status_code=status.HTTP_200_OK)
def get_todos():
	if resultado := servicio_horario.get_todos():
		return resultado
	else:
		raise SinRegistros


@router.post("/", response_model=list[Horario], status_code=status.HTTP_201_CREATED)
def insertar(horarios_nuevos: list[Horario]):
	return servicio_horario.insertar(horarios_nuevos)


@router.put("/{id_horario}", response_model=list[Horario], status_code=status.HTTP_200_OK)
def actualizar_por_codigo(id_horario: int, horario_editado: Horario):
	horario_actualizado = servicio_horario.actualizar_por_codigo(id_horario, horario_editado)
	if not horario_actualizado:
		raise CodigoNoEncontrado(id_horario)
	return horario_actualizado


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def borrar_todo(id_horarios: list[int]):
	horarios_eliminados = servicio_horario.borrar(id_horarios)
	if not horarios_eliminados:
		return CodigoNoEncontrado(id_horarios)


@router.delete("/{id_horario}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_por_codigo(id_horario: int):
	horario_eliminado = servicio_horario.borrar_por_codigo(id_horario)
	if not horario_eliminado:
		return CodigoNoEncontrado(id_horario)
