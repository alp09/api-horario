from pydantic import BaseModel


class MensajeError(BaseModel):
	detail: str
