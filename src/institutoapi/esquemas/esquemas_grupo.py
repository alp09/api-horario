from pydantic import BaseModel, Field


class Grupo(BaseModel):
	codigo: str 	 = Field(max_length=20)
	descripcion: str = Field(max_length=255)

	class Config:
		orm_mode = True
