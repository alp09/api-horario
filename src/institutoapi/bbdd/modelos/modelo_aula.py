from sqlmodel import SQLModel, Field


class Aula(SQLModel, table=True):
	__tablename__ = "aula"

	# Columnas
	codigo: str			= Field(primary_key=True, max_length=20)
	descripcion: str	= Field(max_length=255)
