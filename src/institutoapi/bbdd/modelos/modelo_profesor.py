from pydantic import EmailStr
from sqlmodel import SQLModel, Column, Field, String


class Profesor(SQLModel, table=True):
	__tablename__ = "profesor"

	# Columnas
	codigo: str 			= Field(primary_key=True, max_length=20)
	nombre: str 			= Field(max_length=255)
	email: EmailStr | None 	= Field(sa_column=Column(String(255), unique=True))
	es_admin: bool 			= Field(default=False)
