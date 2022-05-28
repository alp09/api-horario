from fastapi import APIRouter, status

from api.esquemas import Horario
from api.servicios import servicio_horario


# Definición del router
router = APIRouter(
	prefix="/horarios",
	tags=["horarios"]
)


@router.get("/", response_model=list[Horario], status_code=status.HTTP_200_OK)
def get_todos():
	return servicio_horario.get_todos()


@router.post("/", response_model=list[Horario], status_code=status.HTTP_201_CREATED)
def insertar(horarios_nuevos: list[Horario]):
	return servicio_horario.insertar(horarios_nuevos)


@router.put("/", response_model=list[Horario], status_code=status.HTTP_200_OK)
def actualizar_por_codigo(id_horario: int, horario_actualizado: Horario):
	return servicio_horario.actualizar_por_codigo(id_horario, horario_actualizado)


@router.delete("/")
def borrar_todo(id_horarios: list[int]):
	return servicio_horario.borrar(id_horarios)
