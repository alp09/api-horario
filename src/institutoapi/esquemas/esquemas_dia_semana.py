from pydantic import BaseModel, Field


class DiaSemana(BaseModel):
	id: int
	descripcion: str = Field(max_length=20)

	class Config:
		orm_mode = True
