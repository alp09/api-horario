from datetime import date
from fastapi import APIRouter, status

from api.esquemas import HorarioIn, HorarioOut
from api.excepciones.genericas import CodigoNoEncontrado, SinRegistros
from api.servicios import servicio_horario


# Definición del router
router = APIRouter(
	prefix="/horarios",
	tags=["horarios"]
)


@router.get("/", response_model=list[HorarioOut], status_code=status.HTTP_200_OK)
def get_todos():
	horarios_encontrados = servicio_horario.get_todos()
	if not horarios_encontrados:
		raise SinRegistros
	return horarios_encontrados


@router.post("/", response_model=list[HorarioOut], status_code=status.HTTP_201_CREATED)
def insertar(horarios_nuevos: list[HorarioIn]):
	horario_creado = servicio_horario.insertar(horarios_nuevos)
	return horario_creado


@router.put("/{id_horario}", response_model=list[HorarioOut], status_code=status.HTTP_200_OK)
def actualizar_por_codigo(id_horario: int, horario_editado: HorarioIn):
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
