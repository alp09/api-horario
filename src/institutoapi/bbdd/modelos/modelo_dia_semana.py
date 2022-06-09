from sqlmodel import SQLModel, Field


class DiaSemana(SQLModel, table=True):
	__tablename__ = "dia_semana"

	# Columnas
	id: int				= Field(primary_key=True)
	descripcion: str	= Field(max_length=20)
