from pydantic import BaseModel, Field


class Aula(BaseModel):
	codigo: str 			= Field(max_length=20)
	descripcion: str 		= Field(max_length=255)
