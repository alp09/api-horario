from sqlmodel import SQLModel, Field


class Grupo(SQLModel, table=True):
	__tablename__ = "grupo"

	# Columnas
	codigo: str 		= Field(primary_key=True, max_length=20)
	descripcion: str 	= Field(max_length=255)
