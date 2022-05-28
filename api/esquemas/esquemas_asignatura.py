from pydantic import BaseModel, Field


class Asignatura(BaseModel):
	codigo: str 	 = Field(max_length=20)
	descripcion: str = Field(max_length=255)

	class Config:
		orm_mode = True
