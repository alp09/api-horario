from sqlmodel import SQLModel, Field


class Asignatura(SQLModel, table=True):
	__tablename__ = "asignatura"

	# Columnas
	codigo: str 		= Field(primary_key=True, max_length=20)
	descripcion: str	= Field(max_length=255)
