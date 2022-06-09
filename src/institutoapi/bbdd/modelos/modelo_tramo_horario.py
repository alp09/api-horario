from datetime import time
from sqlmodel import SQLModel, Field


class TramoHorario(SQLModel, table=True):
	__tablename__ = "tramo_horario"

	# Columnas
	id: int				= Field(primary_key=True)
	descripcion: str	= Field(max_length=50)
	hora_inicio: time
	hora_fin: time
