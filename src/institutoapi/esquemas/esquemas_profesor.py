from pydantic import BaseModel, Field


class Profesor(BaseModel):
	codigo: str 		= Field(max_length=20)
	nombre: str 		= Field(max_length=255)
	email: str | None 	= Field(None, max_length=255)
	es_admin: bool 		= Field(False)

	class Config:
		orm_mode = True
