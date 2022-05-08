from pydantic import BaseModel, Field


class Profesor(BaseModel):
	codigo: str 			= Field(max_length=20)
	nombre_completo: str	= Field(max_length=255)
	email: str | None		= Field(None, max_length=255)
	es_admin: bool			= False
