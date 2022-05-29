from pydantic import BaseModel, Field
from pydantic.schema import time


class TramoHorario(BaseModel):
	id: int
	descripcion: str = Field(max_length=50)
	hora_inicio: time
	hora_fin: time

	class Config:
		orm_mode = True
